# Ticket #05 review request

Base: d56e092138f6d5c87c75e042caf4f79e0db6989c
Implementation head: 8ec7093f619554fd98428e407c2d70a0e146baf9; final evidence head supplied in HCOM request
Branch: lat/05-summary-tree-global
Worktree: /Users/shiehpay/Desktop/resume/rag/.worktrees/05-summary-tree-global

## Acceptance evidence

1. Overview after processing and throughout conversation: upload test `test_upload_builds_proportional_section_summaries_and_overview`; live browser `overview-ready.png` and `global-summary-source.png`. Ready carries Document Summary; DOM remains present after Q1 and S-source open. PASS.
2. Q1 Global/S-citations/source page range: `test_global_uses_summary_sources_without_query_embedding_and_cache_reuses_tree` proves empty Chunk retrieval, zero query embedding, medium answer call, S1 resolving to p.1–2 summary. Live browser Q1 resolves S5 to p.3–4 §3.1. Eval classification Global passes in all reports. PASS.
3. Section Summary length settings: parametrized `test_section_summary_length_target_covers_minimum_proportional_and_maximum` checks min 80, intermediate 15% target, max 500 in both stored metadata and prompt; fixed low/num_predict=1200 retains thinking budget. PASS (final suite 203/203).
4. Group Summary: `test_long_document_builds_adjacent_groups_and_global_uses_best_fitting_layer` uploads 22 real Sections with scripted summaries exceeding 6K; adjacent Groups preserve ordered Section provenance, Global uses group:1, source lists covered Sections, all recorded requests ≤10K. PASS.
5. Second upload no summary LLM: cache-replay test reloads from disk in a new Application with an empty ScriptedLLM, restores exact Summary Tree, has no embedding/LLM calls and emits ready directly. PASS.
6. Q1 + Chinese three-sentence case/report: Q1_ZH_THREE_SENTENCES added to eval/golden_facts.py; all initial/intermediate/final reports committed with traces and per-fact outcomes. Format and language pass in every earlier report; Q1 all facts pass in format-intermediate. Final result follows below; semantic failures are retained honestly per AC6. PASS for recording requirement, not a claim of uniformly passing quality.

Extra assigned coverage: zero-Chunk heading parents skipped on real LightRAG; >8,500-token Section split into source summaries then merged with all calls ≤10K; summary n/N holds asks disabled; default 4/configured 2 concurrency tested; truncated-summary replacement retains prior Document and creates no partial cache; cache digest contains summary modules, helper dependency and Gateway budgets; Cloud 1/2/4/8 probe committed (32/32 successful, default unchanged).

## Implementation paths at final head

- Upload HTTP/application entry: api.py:80 → application.py:89 background job → application.py:157 processing. Cache hit: application.py:168 restores full Document/Tree and publishes ready. Miss: parse/chunk/embed → application.py:198 build summaries → optional atomic cache → application.py:213 single publication point.
- Configuration: application.py:75 accepts keyword concurrency or SUMMARY_CONCURRENCY; SummaryTreeBuilder defaults to 4 at summary_tree.py:49, using the policy source. Summary domain/provenance: models.py:55 and models.py:70.
- Summary builder: summary_tree.py:144 excludes zero-Chunk Sections. Tasks use a semaphore; as_completed emits summary n/N, then returns Document-order summaries. Finally cancels/awaits siblings on failure/cancellation. Section original text controls 15% targets (overlap excluded); all Table Chunks still enter evidence.
- Oversized Section: summary_tree.py:72 computes available raw-prompt capacity, splits without losing characters, summarizes parts, merges partials (recursively if huge), then produces one Section Summary with every Chunk ID.
- Groups/Document: summary_tree.py:108 packs adjacent summaries; build adds Group levels only over 6K and requires meaningful reduction. Document Summary builds from the final fitting layer. Every generation uses original LLMGateway, which raises on over-budget/length and rejects empty text in builder.
- Global ask: application.py:287 branches before query embedding/Context Packer. summary_context.py:23 chooses first complete layer passing 6K evidence and actual 6,700-token answer-prompt caps. Emits retrieval=[] then S citation map before answer, preserves shared answer retry/thinking/validation/history, records level in trace at application.py:342.
- Summary source lookup: application.py:241 resolves Sections, all Group levels and Document source by stable ID; unknown source retains existing 404 API behavior.
- Source-aware prompt: answer_generator.py:37 adapts only S-source context, preserves Lookup/Synthesis general prompt, current-question language/format, medium initial generation and unchanged low retry at answer_generator.py:90.
- Failure/recovery: summary_tree.py:55 empty/length/transport propagation; application.py:216 maps ingestion failures before publication; prior Document remains; close cancels job and sibling summaries. Nonreducing Groups fail explicitly. User retry is a fresh upload, no partial cache. Ask failure/retry paths remain existing application.py:347 / AnswerGenerator.generate.
- Cache: cache.py:15 source digest includes summary_tree, summary_context, context_packer helper and llm_gateway; application config adds summary model; cache.py:76 rejects records without a Summary Tree. Cache stores full Document model; responses are not cached.
- Events/UI: events.py:10 adds summary stage, events.py:76 adds summary_level; regenerated frontend/src/events.ts. App.tsx:142 persistent overview; App.tsx:168 summary kind/covered titles and page range; Shared.tsx progress label; Trace.tsx summary level. Dist rebuilt and committed.
- Eval/tests: eval/golden_facts.py:275 adds Chinese format/language case, checker logic unchanged. tests/integration/test_summary_tree.py is application-seam coverage; fixtures.py adapter supplies upload summaries while retaining complete calls and ask_calls for legacy ask assertions.

## Integration notes / limits

- No Router, Citation validator, failure policy, table parser or Lookup expansion changes. Context Packer has only a stale-comment update. No main checkout changes, merge, push or self code-review.
- #03 in parallel changes ContextPacker.retrieve to return RetrievalEvent and adds dropped_chunk_count/Table Chunk metadata. Reconcile the non-Global branch during the requested rebase after review; Summary Tree already consumes all Chunks (including table-only Sections), not only paragraphs.
- #09 pending D02; UI is the ticket-authorized minimal implementation. Agreed SummarySource common fields are section/page_start/page_end/text plus kind and section_titles; #09 SourceDialog should preserve them.
- Browser/backend 8160 stopped; probe/eval/test processes complete before review submission.

## Final live evaluation result

Clean code revision 8ec7093: final report is FAIL; Q1 6/8 checks, Chinese summary 9/10. Q1 dual_level fails due to a Judge ellipsis excerpt; conclusion is matched=false in both. Format/language and Global classification pass. All 48 recorded LLM calls stop successfully and maximum reserved usage is 8,045/10,000. Earlier Q1 8/8 is preserved in format-intermediate report. This meets the explicit AC6 reporting criterion and is not an all-pass quality claim. Command: `uv run pytest -q -m eval eval/test_live.py --eval-cases Q1,Q1_ZH_THREE_SENTENCES --eval-label summary-tree-global-final --eval-report eval/reports/summary-tree-global-q1.md` → exit 1 from Golden Facts assertion, report written.

## Final deterministic / static verification

- `uv run pytest -q` → **203 passed, 2 eval tests deselected**, 209.40s; scripted LLM, real local bge-m3.
- `uv run ruff check src tests scripts/generate_event_types.py scripts/measure_summary_concurrency.py eval/golden_facts.py` → PASS.
- `uv run ruff format --check src tests scripts/generate_event_types.py scripts/measure_summary_concurrency.py eval/golden_facts.py` → PASS (48 files).
- `uv run python scripts/generate_event_types.py --check` → backend/frontend event types match.
- `npm run typecheck --prefix frontend` and `npm run build --prefix frontend` → PASS; dist is committed.
- Expanded summary tests all pass within the full suite, including min/proportional/max targets, configured/default concurrency and summary-failure replacement/cache protection. All six ticket criteria are implemented and evidenced; AC6 quality results remain mixed as reported above.
