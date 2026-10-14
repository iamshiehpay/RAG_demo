# Issue05 independent review corrections — implementation handoff

Owner: nova-i05-sari. Independent reviewer: nova-r05-guru. Main/integration: nova.
Branch/worktree: `lat/05-summary-tree-global`, `/Users/shiehpay/Desktop/resume/rag/.worktrees/05-summary-tree-global`.
Original review range: `d56e092138f6d5c87c75e042caf4f79e0db6989c..14e783dd89d379798dcd9fc607e04aafe88d8f3d`.
Correction base: `14e783dd89d379798dcd9fc607e04aafe88d8f3d`. Candidate is the commit containing this report; resolve with `git log -1 --format=%H -- docs/verification/ticket-05/corrections/implementation.md`.

This is implementation verification, not independent review or integrated QA. No merge, push, rebase, subagents, cloud tuning, requirements/GoldenFacts changes, or frontend edits. Prior reports and evaluation artifacts remain unchanged.

## Verified session/tool settings

- HCOM binds `nova-i05-sari` to Codex session `01a132cd-e8ef-7441-a8c0-4775d66eea70`, correct worktree and `lat/05-summary-tree-global` branch; `nova-r05-guru` is the separate reviewer.
- The current session's `turn_context` records model **gpt-6.1-sol**, effort **high**, approval policy **on-request**, sandbox **workspace-write**, network access enabled. Current runtime developer permissions specify **approvals_reviewer=auto_review**, with cwd/hcom/temp writable and shared git metadata outside the worktree. Both pieces of evidence were reported to Main before edits; neither is replaced with a guessed setting.
- Python 3.12.10; uv 0.7.2; ruff 0.17.0; Node v23.11.0; npm 11.5.2.

## Per-finding correction map

| Finding | Resulting behavior | Regression/verification |
|---|---|---|
| H1 | Global instructions are Document-agnostic: requested format/language, whole-Document coverage, supported main ideas/findings, baselines/qualifiers/exceptions, operation-specific metrics. No graph/indexing/retrieval/update/expected-data instructions. | `test_global_non_rag_document_uses_generic_whole_document_prompt` uploads a rainfall Document and checks the actual guarded answer request. Original candidate fails on `graph indexing`. |
| M1 | `Application.ask` explicitly passes `sources="summary"` only from Global; `AnswerGenerator` and `select_summary_context` use the same explicit contract. Citation examples are generated from the source prefix without replacements or evidence scanning. | Lookup and Synthesis variants of `test_literal_summary_marker_in_chunk_keeps_chunk_citations` fail at the original candidate with an Unverified S citation; both pass with C citations. |
| M2 | Upload/failure assertions inspect complete `llm.calls`, success paths check exact summary types/counts, cache replay snapshots total calls. Shared `SummaryScriptedLLM.ask_stream` routes customized ask scripts after one upload-summary dispatch. | Existing ingestion/jobs/HTTP/operations checks strengthened. A temporary baseline cache-hit mutation silently runs Section/Document generation before ready: old test passes; new test fails `4 != 2`. Final unmutated test passes. |
| L1 | Summary progress reserves the Document step initially, discovers Group totals at each level, advances after each Group and Document generation, and reaches n/N only after the Document Summary call and completed-tree assignment. | `test_summary_progress_advances_during_group_and_document_calls`; existing upload/HTTP tests assert Section/Document progress. Original candidate fails because it ends at Section N/N. Totals are dynamic because levels depend on actual outputs. |
| L2 | Upload creates intermediate complete levels against conservative answer capacity. Original Section level remains available; selector still checks actual complete prompt and evidence. No tree calls occur at answer time. | `test_supported_long_global_question_uses_upload_built_group_and_short_uses_sections`: Section evidence lies between 5K and 6K; short selects Section, exactly 1,000-token current question selects Group; actual request guard passes, all Chunk/Section provenance is complete, source resolves to Group, no retrieval Chunks, only router+answer after ask starts. Original candidate selects Document. |
| L3 | Recursive mechanisms are exercised without altering production budgets. Cancellation/failure waits for all started siblings and preserves prior Document/cache. | Multiple Section merge rounds; multiple Group levels; Section and Group non-reduction defenses; concurrent failure and upload cancellation tests. Non-reduction injection deliberately simulates a pathological provider ignoring output reservation, and is not claimed as valid output-budget evidence. |
| L4 | Group min/max/ratio, Section merge target and Document target are named policy constants; no budget values changed. | Existing min/proportional/max Section tests and recursive/Group request checks. Policy source remains in cache identity. |
| L5 | Every split part, recursive merge and final Section call carries `Section: <title>`; repeated-title overhead is deducted before splitting/packing. | `test_each_oversized_section_part_and_merge_retains_section_title` and recursive merge assertions; all recorded valid requests stay within 10K. Original candidate fails repeated-title assertions. |
| L6 | Adapter request semantics and answer prompt/capacity dependencies invalidate upload cache. | `llm_adapter.py` and `answer_generator.py` added to PIPELINE_SOURCES. Public-operation `test_adapter_and_answer_prompt_semantics_invalidate_upload_cache` verifies unchanged replay count and reprocessing after each dependency fingerprint changes; original candidate fails adapter fingerprint check. |

## L2 budget decision and upload cost

Main accepted the arrangement in HCOM #6150; reviewer accepted the intended checks in #6158. Upload capacity derives from `BUDGET_TABLE["answer"].prompt_limit` (6,700), `CONTEXT_EVIDENCE_TOKEN_LIMIT` (6,000), two `QUESTION_TOKEN_LIMIT` reservations (1,000 each), actual explicit-summary prompt overhead with the Chinese-language rule, and the shared join allowance (32). The current computed evidence target is 4,364 tokens, not a hard-coded threshold. It is recalculated from prompt/policy dependencies; changes invalidate upload caches.

This adds Group calls for Documents whose Section layer fits a short question but exceeds this conservative target. It preserves the original detail for short questions, gives supported long questions a complete intermediate layer, and bounds answer work to existing router+answer calls. A ~3K Section layer still needs no Group (real LightRAG upload regression with scripted summaries checks no groups). The maximum source capacity is conservative; actual selector checks remain authoritative, and every LLM call still crosses the unchanged shared budget guard. No input/evidence is silently truncated by this change.

## Dependency and evidence limits

Acceptance success tests use **real local Ollama bge-m3** and **scripted LLM responses through the real LLMGateway**, real parser/chunker/cache, and public upload/ask operations. This includes literal markers, generic prompt, long-question selection, Group/Document progress, titled oversized split, adapter/prompt cache identity, and multi-level provenance. Existing `test_summary_tree.py` real-bge tests continue to cover upload, Global/no-query-embedding, disk replay, oversized Section, concurrency and length targets.

Only the exceptionally large 32-page recursive merge probe and pathological-provider non-reduction probes use fixed fake embedding vectors to isolate timing/failure/recursion. The sibling failure/cancellation probe uses real bge-m3. These edge probes supplement real-bge acceptance; they do not prove retrieval or cloud semantic quality. The ordinary recursive probe uses ScriptedLLM's actual output-reservation enforcement. The pathological-provider probe explicitly bypasses output adherence to test termination.

No real cloud calls were made. **#11 quality is NOT_EXECUTED for the new generic prompt**. The earlier final live report remains FAIL (Q1 6/8; Chinese 9/10) under the previous topic-fitted prompt. Q1 and Chinese-format facts must be rerun under the generic prompt, together with the required second Document. Neither earlier passes nor scripted responses establish new semantic quality. GoldenFacts/checkers were not changed.

## Commands and outcomes

All Python commands set `UV_CACHE_DIR=/private/tmp/nova-i05-uv-cache` and use `uv run --no-sync`.

- Exact original candidate replay: `PYTHONPATH=/private/tmp/nova-i05-baseline/src uv run --no-sync pytest -q tests/integration/test_summary_corrections.py -k 'literal or non_rag or supported_long or retains or semantics'` → **6 expected failures** on the target defects; code in the isolated package came from `git archive 14e783d src`. See `original-red.txt`. Initial discovery probes used fixed fake embedding vectors; final success counterparts use real bge-m3.
- Original progress replay: same isolated package with `-k progress` → **1 expected failure**, `original-l1-red.txt`.
- M2 mutation: only the isolated baseline cached branch is changed to `async for ignored in self.summary_builder.build(document): pass` before publication. Original cache test at its archived path, `--asyncio-mode=auto` → **1 passed** (`m2-old-mutant.txt`); updated cache test against the same mutant → **expected failure at total call count** (`m2-new-mutant.txt`). No mutation is present in candidate code.
- Focused initial edge/protocol suite → **13 passed**, 19.02s (`corrections-green.txt`, fake embedding supporting probes).
- Required real-bge acceptance/fake edge suite: `uv run --no-sync pytest -q tests/integration/test_summary_corrections.py` → **13 passed**, 90.43s (`real-corrections-green.txt`). Final complete suite below also includes later provenance assertions.
- HTTP progress after replacing old event-count assertion: `uv run --no-sync pytest -q tests/integration/test_http.py::test_upload_http_emits_ready_or_error_and_serves_committed_frontend` → **1 passed**, 1.63s (`http-progress-green.txt`).
- `uv run --no-sync ruff check src tests scripts/generate_event_types.py scripts/measure_summary_concurrency.py eval/golden_facts.py` → **PASS** (`ruff.txt`).
- `uv run --no-sync ruff format --check` over the same paths → **PASS**, 49 files (`format-check.txt`).
- `uv run --no-sync python scripts/generate_event_types.py --check` → **PASS** (`event-parity.txt`).
- `npm run typecheck --prefix frontend` → **PASS** (`typecheck.txt`). Frontend source/generated contract/dist unchanged, so rebuild/browser acceptance is not required by these corrections and was not rerun.
- First full suite: `uv run --no-sync pytest -q` → **215 passed / 1 failed / 2 eval tests deselected**, 272.26s (`full-tests.txt`). The sole failure was the preexisting fixed count of seven upload stage events; the added Document progress step requires eight. It is replaced with stage-order and exact Section/Document progress assertions, without weakening ready/error/source/frontend behavior.
- Final full suite: `uv run --no-sync pytest -q` → **PASS: 216 passed, 2 deselected, 6 warnings in 278.62s (0:04:38)** (`final-full-tests.txt`); real local bge-m3 for existing and new acceptance success paths. Explicit fake embedding edge probes are identified above.

## Changed paths and integration invariants

Production: `src/chat_document/{answer_generator,application,cache,policy,summary_context,summary_tree}.py`.
Test support: `tests/integration/fixtures.py`.
Tests: `tests/integration/{test_summary_corrections,test_summary_tree,test_ingestion,test_ingestion_jobs,test_http,test_operations,test_failure_handling,test_router_review,test_router_synthesis,test_review_regressions}.py`.
Evidence: `docs/verification/ticket-05/corrections/`; appended `docs/ai-log.md`. Exact candidate paths are recorded in `changed-files.txt`.

- #02 parser integration: retain zero-Chunk exclusion, Section original paragraphs for targets, original Section order/title/page contract; rerun heading-only, Section target, split/title tests.
- #03 integration: retain Table Chunks in evidence, target calculation and complete `chunk_ids`; Global must emit empty retrieval and never query embedding. Reconcile only the non-Global RetrievalEvent/drop-count changes when Main orders rebase. Parser/table/policy/helper fingerprints must invalidate stale Summary Trees. Rerun cache/recursive/Group tests after integration.
- #09 integration: preserve persistent overview, S Citation clicks, Summary kind/Section titles/pages/text and Trace.summary_level; summary progress now includes Group/Document completion and dynamic totals. No frontend edits were made here. Main owns common-component merge and dist rebuilding.
- Transactional publication, cancellation awaiting, invalid Citation policy, medium answer/low retry and fixed refusal remain shared behavior and are exercised by full regression suite.

## Cleanup and next step

No task backend/browser/container/service was started or changed; no shared services were stopped. All validation processes completed before handoff. Authorized Git staging required automatic-review sandbox escalation for the worktree index under the parent repository; staging succeeded. Isolated mutation package and UV cache are task-namespaced under `/private/tmp/nova-i05-*`; mutation files are never committed. Candidate is submitted directly to guru for targeted independent review, cc Main. Main owns later sequential #02→#03→#05 integration and separately assigned integrated QA.
