# Ticket #02 — third review fixes (#3699)

Base: `109bab37a7e9f1a6d7f18a3c3f1d6874c7bd3907`. Implementation checkpoint: `b851d3da5c6e5409c530fa97d673a4936c4db459`. Final evidence head is supplied in the HCOM request. Main's #07 advance to `9538b88` is acknowledged; this candidate keeps the requested review base until Levi requests rebase.

## M1 — styled Figure labels

The generated upload first failed because bold body-size `LLM`, body-size `LLM AGENT` and larger `Dual-level Retrieval` survived; the larger label opened a Section and captured the Figure caption and continued Introduction.

Figure-region protection now requires an actual numbered Section opening or body-size paragraph flow. Page-frame-sized regions are excluded geometrically before caption clipping, preserving numbered and unnumbered headings. Remaining short labels inside eligible Figure regions are removed before Section detection regardless of boldness or size. `_is_figure_label` centralizes that decision; sentence-end punctuation and width/word/frame thresholds are shared or named.

- `test_bold_and_larger_figure_labels_do_not_create_sections_or_enter_prose`: RED then PASS. Exactly `1 Introduction`; all three labels absent; caption and before/after prose retained with correct provenance.
- `test_page_frame_does_not_remove_the_section_heading`: PASS for both numbered and unnumbered titles.
- Shaded paragraph preservation, ordinary short prose/Table-cell protection and actual LightRAG Figure 1 label exclusion remain PASS.

## M2 — numbered uppercase body sentences

Generated inline and split-number uploads first failed because `2 GPU HOURS.` and `3. THE SOFTWARE IS PROVIDED AS IS.` became Sections. The trailing-period exception now also requires a typography difference: bold, mixed-size small-caps, a different font from the dominant body font, or a larger size. Uniform body-style numbered sentences remain paragraphs.

- `test_numbered_uppercase_body_sentences_do_not_open_sections`: both variants RED then PASS; every marker remains in Introduction.
- Positive inline/split appendix heading fixture uses bold/different-font styling and passes.
- Real LightRAG §7.2/§7.4 mixed-size small-caps headings remain detected; their trailing title periods are removed. Table 2 provenance remains §4.3, p.8.

## Current acceptance and checks

`uv run pytest tests/integration/test_ingestion.py -q`: **32 passed**, 10.99 s. Uses real generated PDFs, PyMuPDF, local bge-m3 and public Application upload/ask operations. ScriptedLLM substitutes only the native LLM seam.

| Assigned criterion | Current evidence |
| --- | --- |
| LightRAG main Sections through Conclusion and Appendix | `test_lightrag_sections_exclude_references_and_keep_appendix` passes; 28 Sections, 25 with paragraphs, 41 Chunks, maximum 493 tokens. |
| References excluded; Appendix retained and labelled | LightRAG and generated References/Appendix regressions pass, including lettered and supplementary forms. |
| Section-confined bounded Chunks; configurable paragraph packing | Relative-heading, configured-target and environment tests pass; long paragraphs alone split, with English/Chinese sentence and whole-word overlap checks. |
| Generated image-only PDF reports missing text layer | `test_image_only_document_reports_missing_text_layer_before_embedding` passes. Invalid/no-text reasons remain distinct; readable repaired PDFs remain accepted and logged. |
| Heading-free PDF gets bounded virtual Sections and is askable | `test_heading_free_document_uses_bounded_virtual_sections_and_can_be_asked` and configured virtual target tests pass. |
| Citation side-note shows page and Section | Existing implementation unchanged; prior committed browser evidence in [review fixes](review-fixes.md) remains historical UI evidence. No new browser run is claimed. |

- Full `uv run pytest -q`: **145 passed, 2 deselected**, 134.26 s; six existing dependency deprecation warnings. Includes #08 eval harness tests; cloud/live eval remains opt-in.
- `uv run ruff check src tests eval scripts`: PASS.
- `uv run ruff format --check src tests eval scripts`: PASS, 60 files.
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `npm run build` in `frontend/`: PASS (`tsc --noEmit` + Vite); dist unchanged.
- `git diff --check`: PASS.

No owned backend/browser process was started this round. No Golden Facts pass is claimed. Historical raw-table answer errors remain evidence for #03/#11. Table reconstruction, background ingestion/cache, Summary Tree and final design remain their assigned tickets. The zero-Chunk Section exclusion contract for #05 remains unchanged.

## Implementation paths at b851d3d

- `src/chat_document/pdf_parser.py:90`: caption-associated drawing/image candidates, Table-caption protection and page-frame exclusion.
- `src/chat_document/pdf_parser.py:130`: complete extraction → body typography inference → candidate protection → label filtering; `:202` short-label helper; `:210` body paragraph-flow and actual numbered-opening protection; `:233` numbered-opening check.
- `src/chat_document/pdf_parser.py:241`: heading style and sentence-ending guards; `:271` merge split numbers/wrapped titles and normalize final periods.
- `src/chat_document/pdf_parser.py:329`: Section/paragraph transitions, References exclusion and Appendix state; `:313` configured virtual fallback; `:416` PDF opening/repair/no-text errors.
- `src/chat_document/chunker.py:90`: Section-confined packing; `:55` oversized paragraph splitting; `:28` whole-word/sentence overlap.
- `src/chat_document/application.py:39`: keyword-only settings/target validation; `:61` synchronous upload → parse → chunk → embed → ready/error. Unchanged this round, seam shared with #04.
- `tests/integration/test_ingestion.py:350`, `:381`, `:395`: frame, styled Figure labels and numbered body-sentence regressions; `:361` positive period-ending appendix headings; `:29` real LightRAG checks.

M1 and M2 have passing regressions. Independent re-review remains pending.
