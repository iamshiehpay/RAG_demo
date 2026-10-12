# Ticket #02 — review fixes for Levi #2626

Implementation checkpoint: `ed121cfb39e9c89ea259e23e5a983b62fb805406` on `lat/02-structure-aware-chunking`, rebased first onto main `f5be286afa66a3a216a15d298efecb575d6d54c8`. The final evidence commit is given in the HCOM re-review request. The [first report](report.md) remains historical evidence for the earlier candidate.

## Review findings and regressions

All parser regressions operate through `Application.upload_document`, real generated PDF bytes, and real local bge-m3. Ask regressions use the recording ScriptedLLM at the native LLM seam.

| Finding | Result and evidence |
|---|---|
| C1 wrapped heading | PASS: `test_wrapped_and_number_only_headings_keep_the_complete_title` retains both lines and the number. Same-font/style lines within 1.5 line heights merge. LightRAG's complete paper title is distinct from §2. |
| C2 Appendix after References | PASS: `test_appendices_after_references_resume_indexing` covers `A Proof of Theorem`, `Supplementary Material` and `補充資料`; each is labelled Appendix and keeps its body while bibliography text stays excluded. |
| C3 two columns | PASS: `test_two_column_reading_order_keeps_same_size_bold_headings_and_provenance` uses row-interleaved authoring and three Sections. Column/position ordering and splitting same-row cross-column blocks keep all four prose markers in the correct Section. |
| S1 figure fragments | PASS: `test_figure_labels_are_filtered_without_discarding_short_prose_or_table_cells` preserves a real short sentence, Figure/Table captions, table header, `64.8` cell and table-related paragraph. Figure caption plus visual-region geometry identifies short labels; mathematical/table symbols remain. LightRAG's `Beekeeper`, `Query + LLM` and isolated control glyphs are excluded. |
| S2 lone `1.` | PASS: split number/title merging precedes sentence punctuation rejection; the generated `1.` / `Introduction` case keeps the full title. |
| S3 small-caps subsections | PASS: `test_body_size_numbered_small_caps_subsection_forms_a_chunk_boundary` uses body-size `4.3` / `ABLATION STUDY`. Numbering plus capitalization/bold/relative size identifies headings without fixed font sizes. LightRAG Table 2 is confined to §4.3; p.8 Chunks exist. |
| C4 Sub-query coverage / adapter dispatch | PASS: `test_each_q2_sub_query_retrieves_its_required_evidence_in_its_own_top_two` covers cost and incremental update independently, using the public ask operation with Lookup top-k=2. Each requires all terms in one retrieved Chunk. Combined Synthesis still preserves/expands baseline evidence, deduplicates and sorts by Document order. Extraction fixtures branch on `request.call_type == "fact_extraction"`, supplied by Gateway. |
| C5 readable repaired PDF | PASS: `test_readable_repaired_pdf_is_accepted_and_logged` accepts a readable repaired PDF and requires a warning. Open/zero-page failures are invalid PDFs. No-text Documents remain unsupported: a repaired no-text input receives a damaged-PDF reason, distinct from a normal scanned PDF. |
| C6 same-size bold headings / References-only | PASS: two-column regression covers simultaneous headings and same-size bold Methods/Results. `test_references_only_document_reports_no_indexable_text` requires a clear References-only error and no stored Document. |
| Configured virtual Section size | PASS: `test_configured_target_also_bounds_virtual_sections` and `test_settings_from_env_control_real_and_virtual_chunk_bounds` verify an 80-token bound. `RetrievalSettings.from_env()` validates the env value; explicit Application target remains compatible and takes precedence. HTTP factory delegates config parsing to Settings. |
| AI log style | PASS: the three #02 historical entries are Traditional Chinese, separated by blank lines; the review corrections are appended with the failing evidence and changed repair policy. |

Heading-only parent Sections are retained as metadata with zero Chunks when a subsection immediately follows. LightRAG now has **26 Sections (23 with text), 40 Chunks, maximum 493 tokens**. No Chunk crosses a Section; References-only pages 11–12 remain excluded and Appendix content remains indexed.

## Automated verification

- Initial generated parser review cases: **10 failed, 1 passed**, before implementing fixes; includes heading, Appendix, layout, figure, repair and virtual-size failures.
- First parser check: `uv run pytest tests/integration/test_ingestion.py -q`: **24 passed** (before adding the Settings case).
- `uv run pytest tests/integration/test_router_synthesis.py tests/integration/test_router_review.py tests/integration/test_ingestion.py tests/integration/test_http.py -q`: **53 passed**.
- Final `uv run pytest -q`: **104 passed, 1 deselected**, 83.20 s. Six existing PyMuPDF/Starlette dependency deprecation warnings; no failed test. Real local embeddings; cloud eval excluded.
- `uv run ruff check src tests scripts`: PASS.
- `uv run ruff format --check src tests scripts`: PASS, 33 files.
- `uv run python scripts/generate_event_types.py --check`: PASS; event contract unchanged.
- `npm run build` in `frontend/`: PASS (`tsc --noEmit` and Vite). Rebuilt `dist/` is byte-identical to committed output, so no new dist diff.
- `git diff --check`: PASS.

## Production browser verification

Chrome via isolated `agent-browser --session t02-vida`; default `chat_document.api:create_app` on localhost:8110; real PyMuPDF, local bge-m3, native Ollama Cloud Router and answer adapter. No ScriptedLLM in this browser run.

Question: `What does Section 4.3 say about the ablated LightRAG variants?`

- Upload reaches `lightrag.pdf · 40 Chunks · Ready`.
- Router: Lookup, no fallback; answer reaches `Answer complete`.
- Side-note `[C4] · p.8` displays `4.3 ABLATION STUDIES (RQ2)`: [desktop screenshot](evidence/review-lightrag-sidebar.png).
- Click opens original Chunk with `Source · p.8 · 4.3 ABLATION STUDIES (RQ2)` and raw `-Low`/`-Origin` rows: [source screenshot](evidence/review-lightrag-source.png), [answer/source text](evidence/review-live-answer-and-source.txt).
- At 1440 px, sidebar width 220 px and document scroll width 1440 px. At 390 px, document scroll width 390 px; answer bottom 1639.66 px, notes top 1663.66 px. Notes appear below the answer; source remains accessible: [mobile screenshot](evidence/review-lightrag-mobile.png).
- Browser runtime errors: none. Trace opened with keyboard activation; model thinking stays collapsed. [Trace screenshot](evidence/review-lightrag-trace.png), [visible metrics](evidence/review-live-trace.txt).

| Call | think | Estimated prompt + reservation | Reported prompt / output | Latency | done_reason |
|---|---|---|---|---|---|
| Router | low | 832 + 600 = 1,432 / 10,000 | 493 / 104 | 1.46 s | stop |
| Answer | medium | 2,281 + 3,000 = 5,281 / 10,000 | 2,056 / 1,118 | 4.79 s | stop |

**Known live answer failure, preserved:** the model still misreads raw Table 2 rows and claims every ablation underperforms the full model. This does not pass Q3 Golden Facts. #03 table reconstruction and #11 evaluation remain responsible for that problem; this run proves the assigned parser/Citation provenance and browser layout only. No prompt tuning or unrelated feature was added.

Backend 8110 and browser session t02-vida were stopped after verification. No push, merge, main checkout or other worktree edit.

## Implementation path list at the checkpoint

- `src/chat_document/api.py:44` constructs real adapters and validated Settings; `src/chat_document/application.py:39` resolves Settings/explicit target, `:62` clears state → parses → chunks → embeds → stores ready state. `:77` maps DocumentError to the upload error event without a stored Document.
- `src/chat_document/pdf_parser.py:340` open/type/zero-page/password checks → repaired warning → text extraction → distinct no-text error → Sections. `:35` infers paired prose columns, splits grouped cross-column lines, orders column-major within full-width bands. `:84` identifies Figure-caption visual regions with Table-caption protection. `:120` extracts line typography/pages and filters figure labels/control glyphs; shared baseline checks stay within a column.
- `src/chat_document/pdf_parser.py:175` relative-size/bold/numbered-capital heading detection; `:195` merges split numbers and wrapped titles. `:253` flushes paragraphs/Sections, enters References exclusion, resumes at lettered/supplementary Appendix and carries Appendix state. `:237` creates virtual Sections using the same configured target.
- `src/chat_document/settings.py:10` frozen validated retrieval/Chunk settings and env parsing. `src/chat_document/llm_adapter.py:15` backward-compatible request call-type metadata; `src/chat_document/llm_gateway.py:66` supplies the authoritative call type without changing budget policy or transport payload.
- `src/chat_document/models.py:15` compatible Section provenance metadata; `src/chat_document/chunker.py:90` paragraph packing and per-Chunk page ranges, `:55` oversized sentence splitting, `:28` complete-word/sentence overlap.
- `frontend/src/Answer.tsx:3` live short-marker source buttons and used Citation notes; `:15` page ranges and Section text. `frontend/src/styles.css:27` existing responsive sidebar layout. No frontend source changes were required for the second review.
- `tests/integration/test_ingestion.py:208` generated review regressions; `tests/integration/test_router_synthesis.py:152` direct top-two Sub-query coverage. Recording extraction adapters now dispatch by call type.

All requested #2626 fixes have evidence above. Final independent re-review is pending; final design remains #09 under D02.
