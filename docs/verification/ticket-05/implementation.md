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
