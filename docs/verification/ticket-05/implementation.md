# Ticket #05 implementation verification

Binding scope: Summary Tree upload processing, Global answers, provenance/cache/progress, persistent overview and S-source lookup. D01 applies; D02 only blocks #09 final design.

UI mode: Extension. Existing fonts, colors, forms, SSE flows and Citation controls are preserved. Add a minimal overview before Conversation and page-range/covered-Section metadata to the source panel; no redesign or extra interaction.

## Milestone 1

- RED: first upload test failed because ready.document_summary was None; then passed with the builder.
- RED: Global test retrieved three Chunks; then passed after branching before Context Packer/query embedding.
- RED: long Document test had no Group Summary; then passed with adjacent grouping.
- Targeted tests: `uv run pytest -q tests/integration/test_summary_tree.py tests/integration/test_router_synthesis.py::test_extraction_losing_citation_ids_fails_without_final_answer tests/integration/test_review_regressions.py::test_real_10k_prompt_cap_failure_is_an_application_error_without_final tests/integration/test_ingestion_jobs.py::test_pipeline_version_and_content_changes_reprocess_the_document` → 9 passed.
- `npm run typecheck --prefix frontend` and `npm run build --prefix frontend` → PASS; generated event types and dist updated.

Full suite, live eval, Cloud concurrency measurement and browser evidence will be added before review.

## Milestone 2

- First full deterministic suite: `uv run pytest -q` → 198 passed, 2 eval tests deselected (246.16s). Follow-up tests explicitly exercise default concurrency=4, configured concurrency=2, min/proportional/max Section targets, and summary-failure swap/cache protection. Final suite follows below.
- Cloud probe: `uv run python -m scripts.measure_summary_concurrency --output eval/reports/summary-concurrency-20261013.json` → all 32/32 calls succeeded, no truncation, no budget violation. At concurrency 1/2/4/8: wall 8.82/4.31/2.64/2.10s. The probe ran short prompts and overlapped a live eval, so it demonstrates successful in-flight concurrency through 8, not a universal service limit or controlled benchmark. Confirmed default 4 stays unchanged.
- Initial and two intermediate live eval reports preserve outcomes. Q1 all facts passed in `summary-tree-global-q1-format-intermediate.md`; Chinese language and exactly-three-sentences passed in every report. Some semantic Judge checks failed, including nonverbatim ellipsis excerpts. One Chinese answer confused retrieval API-call cost with incremental updates; Global-only prompt now explicitly separates these operation metrics. Final report will record post-fix results.

## Browser acceptance

- Production factory on `http://127.0.0.1:8160`, committed dist; real bge-m3 and gpt-oss:120b-cloud. Isolated agent-browser session `t05-summary`.
- Uploaded LightRAG, observed `摘要 · 25/25` and disabled question input until Document Summary finished. `overview-ready.png` shows the ready overview (the screenshot occurred after completion, not during progress).
- Asked Q1, received Global `[S#]` answer, opened S5: Source title `p.3–4 · 3.1 GRAPH-BASED TEXT INDEXING`, Section Summary and covered title visible. Overview remained present after answer and source open; `global-summary-source.png` captures the complete page.
- DOM checks at 1440×900 and 1280×720: overview/source present, no horizontal overflow. Browser errors and console empty. Source/ask HTTP calls returned 200, upload 202.
- Browser and backend process were stopped after checks. UI acceptance exercised the Summary Tree/provenance flow; no final #09 design claim.
