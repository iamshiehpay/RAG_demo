# Ticket #06 acceptance evidence

Branch: `lat/06-router-synthesis`; implementation base: `cf49802`.

## Deterministic acceptance

`uv run pytest -q`: **32 passed**, 30.27 seconds (final run; earlier run 35.53 seconds). Scripted, recording LLM; real local Ollama bge-m3. No cloud LLM calls. Existing #01 scripts were extended with malformed Router JSON to keep their original Lookup/answer behavior; separate #06 tests exercise valid plans.

Each command below names the relevant test in `tests/integration/test_router_synthesis.py` (run with `uv run pytest tests/integration/test_router_synthesis.py::<name> -q`). All are included in the green full suite.

| Requirement | Evidence | Result |
|---|---|---|
| Plan includes Question Type, Standalone Question, Sub-queries | `test_router_plan_drives_answer_and_is_recorded_with_json_schema`; browser Trace screenshot | PASS |
| Malformed JSON falls back to Lookup | `test_malformed_router_json_falls_back_to_lookup_with_original_question` | PASS |
| Question >1,000 tokens rejected, zero LLM calls | `test_too_long_question_has_explicit_rejection_event_and_zero_calls`; Pydantic event roundtrip; generated TS parity | PASS |
| Latest 2 rounds, each ≤500 tokens | `test_router_history_keeps_only_two_rounds_each_at_most_500_tokens` inspects recorded prompt; `test_successful_turns_supply_history_to_later_follow_up` checks stored successful history | PASS |
| Q2 Sub-queries retrieve cost and incremental-update evidence | `test_q2_sub_queries_cover_cost_and_incremental_update_in_document_order`, LightRAG PDF + real bge-m3; also checks unique IDs, Document order and answer excerpts | PASS |
| Oversized evidence extracted in batches; Citations resolve to original Chunks | `test_oversized_synthesis_extracts_facts_and_keeps_original_citation_sources`, top-k=30 forces >6K evidence; all guarded requests ≤10K | PASS |
| Extracted facts still too large → merge again | `test_extracted_facts_are_reduced_again_when_they_still_do_not_fit`, four extraction calls then answer, original C1/C20 retained | PASS |
| Configurable top-k; defaults 5 / 3 / 2; Global transitional path | `test_configurable_top_k_counts_and_global_temporarily_uses_synthesis` verifies Lookup=2, Synthesis=1+4 per Sub-query and dedupe, Global uses Synthesis=1 | PASS |
| Router timeout stops before retrieval | `test_router_transport_failure_stops_before_query_embedding`, only ingestion embed call, one failed Router trace | PASS |
| Query embedding failure stops before answer | `test_query_embedding_failure_does_not_start_answer_generation` | PASS |
| Extraction loses Citation IDs → error, no final | `test_extraction_losing_citation_ids_fails_without_final_answer` | PASS |
| 12 live Router regressions in eval report if #08 merged | #08 was not merged at verification (`main=62a7b80`). Exported unchanged labeled spike cases in `router_regression.py`; #08 agreed to consume them and `ConversationTurn` history, and forwards Gateway schema kwargs. Later merge runs the integrated report. | CONDITIONAL / NOT EXECUTED |

TDD tracer evidence: the initial plan test failed against #01 because the Standalone Question stayed `What about it?`; after Router integration it passed. The rejection test failed with event `error` before the explicit event was added. Q2 evidence initially lacked `610` before Sub-query retrieval; it passed after Context Packer integration. Forced overflow initially emitted `budget_exceeded`; it passed after cited batch extraction.

## Other checks

- `uv run ruff check src tests scripts/generate_event_types.py`: PASS.
- `uv run ruff format --check src tests scripts/generate_event_types.py`: PASS.
- `uv run python scripts/generate_event_types.py --check`: PASS, backend/frontend event models match.
- `npm run typecheck --prefix frontend`: PASS.
- `npm run build --prefix frontend`: PASS; regenerated `frontend/dist/` committed.
- `git diff --check`: PASS.

## Browser acceptance

Isolated `agent-browser --session t06-check`, Chrome headless at 1280×720, `http://127.0.0.1:8120`, serving committed build. Temporary app used real bge-m3 with delayed ScriptedLLM; this validates UI integration rather than live-model classification or answer quality.

Path: upload a one-page text PDF → ask comparison → observe planning / retrieval / thinking → expand Trace → submit 1,002-token question → inspect rejection. The mutation observer recorded `判斷問題類型` → `檢索` → `思考中` → `Answer complete`; separate screenshots captured each waiting stage. Trace visibly showed Synthesis, a complete Standalone Question and two Sub-queries. No browser errors or console errors; no horizontal overflow.

The first rejection check caught that `consumeEvents` did not recognize `rejected` as terminal: its completion error overwrote the reason. After repair/rebuild, the same check showed `問題過長，請縮短問題`, `Question must not exceed 1,000 tokens.`, zero retry buttons, restored editable input, and no overflow. This correction is recorded in `docs/ai-log.md`.

Evidence: `planning.png`, `retrieval.png`, `thinking.png`, `trace-plan.png`, `rejected.png` in this directory. Browser and task-owned backend processes were stopped after verification. No Vite process started.

## Integration boundaries

Global deliberately follows Synthesis until #05. Neighbor/Table Chunk linking remains #03; retries, Citation Validator and thinking events remain #07. The final Tufte design remains #09. #08 owns live eval/report wiring. Top-k environment names: `LOOKUP_TOP_K`, `SYNTHESIS_TOP_K`, `SUB_QUERY_TOP_K`; invalid/non-positive values fail settings validation at startup.

## Independent review follow-up (#1256)

The independent reviewer requested changes after confirming the original 32-test suite. The corrected suite has **43 passing tests**, 65.70 seconds, still using real local bge-m3 without cloud LLM calls. This section supersedes earlier claims about strict Router sub-query validation and the original synthetic recursive output size.

- `tests/integration/test_router_review.py::test_schema_valid_router_plan_preserves_follow_up_rewrite` passes five cases (Synthesis with 0 / 1 / 8 Sub-queries; Lookup / Global with spurious Sub-queries). All five failed before normalization. The valid Standalone Question now survives.
- `test_extraction_normalizes_citations_discards_headings_and_filters_sentinel` failed before correction, then passed: `[C1, C3]` and `【C3†L1-L4】` are canonicalized; headings, uncited lines and the sentinel are filtered and counted in each call's `discarded_fact_lines` Trace field. A batch without relevant facts does not destroy facts from another batch; if the entire extraction returns no cited facts, it fails honestly.
- `test_lookup_with_large_top_k_fits_without_extraction` failed before correction, then passed with top-k=30: whole Chunks are selected by rank within the exact answer capacity; only Router and answer calls occur. Batch extraction starts only for Synthesis whose original evidence exceeds 6K. Global is explicitly converted to Synthesis only for its transitional context path pending #05; the visible plan remains Global.
- `test_truncated_router_falls_back_but_retains_its_failed_trace` failed before correction, then passed: Router length failures use Lookup fallback while its length Trace remains recorded. Other truncated calls use call-specific messages, including Fact extraction.
- `test_explicit_history_does_not_modify_session_history` passes: explicit eval history leaves successful session rounds unchanged.
- `test_scripted_llm_honors_output_reservation_including_thinking` failed before ScriptedLLM enforcement, then passed for both strings and explicit thinking/content frames. Output over the reservation emits `done_reason=length`.
- The recursive reduction test now uses seven tall synthetic pages and multiple first-pass results of fewer than 1,000 tokens each. Their total exceeds 6K; subsequent calls reduce it again. Every extraction Trace reports at most 1,000 generated tokens and `stop`. Its former unrealistic 3,500-token scripted batches were removed.
- Q2 coverage now has a negative control through `ask`: Lookup with top-k=3 on the Standalone Question does not contain `610`; the Synthesis Sub-queries retrieve the cost Chunk. HTTP tests assert all three plan fields and that oversized rejection is the only event, with no final or model calls.
- Numeric history, Sub-query, evidence and top-k limits plus conservative packing allowances are named in `policy.py`. Type generation, ruff, formatting, TypeScript and frontend rebuild all pass. The new Trace count is displayed in the frontend.

Browser follow-up: `trace-filtered-facts.png` captures the rebuilt frontend on LightRAG, with three extraction calls showing discarded-line counts **2, 1, 1** and the full Synthesis plan. The UI completes successfully and reports no browser errors. The temporary scripted adapter supplies each batch independently because Sub-query union can add Chunks beyond the standalone top-k; an initial fixed two-batch fixture ran out of replies and was replaced. Browser and backend were stopped after this check.

## Integrated live QA follow-up (#1672)

Independent live QA on main `79aac57` found that the original scripted checks hid near-miss JSON
and silent Lookup fallback. [Live Router follow-up](live-router-followup.md) documents the repair,
exact raw fixtures, opt-in 12-case smoke, fallback provenance, and real-cloud browser evidence.
Review #1974 found that the earlier 12/12 and browser results used a prompt tuned to the cases.
The current neutral prompt scores 12/12 canonical and 8/8 held-out, but live browser acceptance
is **FAIL**: Q2 misses cost/update passages; Q3 after history is Synthesis and changes language.
The linked follow-up report records both scores and failures. The 600-token reservation is unchanged.
