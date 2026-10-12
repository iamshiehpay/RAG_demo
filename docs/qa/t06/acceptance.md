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
