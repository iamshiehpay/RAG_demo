# Ticket #02 — second review fixes (#3351)

Base: `109bab3` (main with #08 eval harness). Implementation checkpoint after rebase: `1466714`. Final evidence head is supplied in the HCOM re-review request. Previous [review report](review-fixes.md) and browser tapes describe the earlier candidate; no new browser/cloud run is claimed here.

## N1 — prose and headings inside drawings

The generated shaded-box upload first failed because five wrapped paragraph lines vanished. The generated page-frame upload separately failed because `1 Introduction` vanished and the Document became a virtual Section.

Text extraction now gathers the complete typography and shared-row geometry before any figure-label filtering. Candidate Figure regions are discarded when they contain a heading or body-size paragraph flow: multiple lines in a block with a sentence ending or predominantly wide lines. Per-line filtering also explicitly preserves heading candidates and Section numbers. A decorative page border and a shaded paragraph box therefore do not erase Document content.

Regression evidence through `Application.upload_document`, real PyMuPDF and local bge-m3:

- `test_shaded_prose_above_a_figure_caption_preserves_every_line`: RED, then PASS; all six unique prose markers and the real Section survive.
- `test_page_frame_does_not_remove_the_section_heading`: RED, then PASS; the heading survives, is not virtual, and the body remains.
- `test_figure_labels_are_filtered_without_discarding_short_prose_or_table_cells`: still PASS.
- `test_lightrag_sections_exclude_references_and_keep_appendix`: still PASS; LightRAG Figure 1 `Beekeeper` / `Query + LLM` fragments remain absent; table text and §4.3 provenance remain intact.

## N2 — period-ending numbered headings

`test_numbered_all_caps_period_headings_keep_their_own_appendix_content` first failed with all evidence under `7 Appendix`. It now passes for both an inline `7.2 CASE EXAMPLE OF LIGHTRAG.` and a split `7.4` / `CASE STUDY OF NAIVERAG.`. A trailing period is allowed only for numbered uppercase/small-caps heading candidates; ordinary sentence filtering remains.

The LightRAG upload regression also requires actual §7.2 and §7.4 titles. Their content now belongs to those Sections, rather than §7.1 / §7.3.4. Current corpus: **28 Sections, 25 with paragraphs, 41 Chunks, maximum 493 tokens**. Table 2 remains in §4.3.

## N3 — empty-Section summary contract

`Section`'s code docstring records the binding contract: **Sections with zero Chunks are excluded from Summary Tree input. Builders skip them and summarize only Sections containing source Chunks.** Heading-only parents (§3, §5, §7.3) remain metadata with zero paragraphs/Chunks. No summary behavior is added to #02; #05 implements the builder exclusion.

## N4 — logs and configuration validation

- Corrected `批次数量` to `批次數量`; #02 10-12 entries precede #06 10-13 entries. Rebase conflict resolution preserves all #06/#08/#02 log content and arranges dated sections chronologically.
- Removed Application's duplicate `< 1` check. An explicit constructor override is routed through validated `RetrievalSettings` before storage, preserving explicit-argument precedence while enforcing the existing Pydantic `gt=0` rule. A direct zero-target probe raises the `chunk_token_target` validation error; configured packing and HTTP env tests pass.

## Verification after rebase

- Before rebase, `uv run pytest tests/integration/test_ingestion.py tests/integration/test_http.py -q`: **32 passed**.
- Full `uv run pytest -q`: **141 passed, 2 deselected**, 90.81 s; six existing dependency deprecation warnings. Includes #08 eval unit/integration tests; live/cloud eval stays opt-in.
- `uv run ruff check src tests eval scripts`: PASS.
- `uv run ruff format --check src tests eval scripts`: PASS, 60 files.
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `npm run build` in `frontend/`: PASS (`tsc --noEmit` + Vite), dist byte-identical to committed output.
- `git diff --check`: PASS.

No owned backend/browser process was started for this round. The prior live answer's raw-table numerical errors remain preserved as historical evidence for #03/#11; no Golden Facts pass is claimed.

## Implementation paths at the checkpoint

- `src/chat_document/pdf_parser.py:120`: extract complete line typography and geometry → infer body size → reject prose/heading-containing Figure regions → filter remaining short figure labels while preserving headings/numbers.
- `src/chat_document/pdf_parser.py:188`: `_contains_prose` protects heading-containing page frames and body-size multi-line sentence flow/wide lines. `:84` continues caption-associated drawing/image candidates with Table-caption protection.
- `src/chat_document/pdf_parser.py:204`: relative typography heading detection, with the narrowly scoped numbered-uppercase trailing-period exception; `:227` handles split numbers/titles and wrapped headings.
- `src/chat_document/pdf_parser.py:285`: paragraph/Section boundaries, References exclusion and Appendix state; `:372` open/repair/no-text failure handling remains intact.
- `src/chat_document/models.py:15`: Section metadata and zero-Chunk Summary Tree input contract.
- `src/chat_document/application.py:39`: Settings and explicit target resolution through Pydantic validation; `:62` upload → parser → chunker → embedder → ready/error unchanged.
- `tests/integration/test_ingestion.py:331`, `:342`, `:353`: shaded prose, page frame and period-heading upload regressions. LightRAG test also requires real §7.2/§7.4.

All N1–N4 items have evidence above; independent re-review remains pending.
