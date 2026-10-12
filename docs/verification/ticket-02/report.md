> Historical first-review evidence at 41aabfa, before #2626 findings. Parser counts, repair policy and paths below describe that candidate. See [review fixes](review-fixes.md) for current verification.

# Ticket #02 verification

Base: `b005721` (main, including #06). Branch: `lat/02-structure-aware-chunking`.
Verification date: 2026-10-13. The final head is supplied in the review request.

The implementation keeps synchronous upload and the existing event contract. Section fields are extended compatibly with paragraph page ranges, `is_appendix`, and `is_virtual`. Chunk IDs/event fields remain unchanged. `Application` accepts both `settings` and `chunk_token_target`; the default HTTP factory passes both environment settings.

## Acceptance evidence

The focused command was:

```sh
uv run pytest tests/integration/test_router_synthesis.py tests/integration/test_router_review.py tests/integration/test_ingestion.py -q
```

Result: **35 passed** in 91.94 seconds, using real local bge-m3 and a recording ScriptedLLM. The scripted LLM substitutes model answers/plans; these checks prove parsing, retrieval orchestration, source provenance and budgets, not cloud answer quality.

| Requirement | Result | Evidence in the focused suite |
| --- | --- | --- |
| LightRAG main Sections from Introduction through Conclusion and Appendix | PASS | `test_lightrag_sections_exclude_references_and_keep_appendix` asserts all seven titled main Sections. The parser yields nine nonempty Sections including front matter/Abstract. |
| References excluded; Appendix retained and labelled | PASS | The same test excludes bibliography pages 11–12 from Chunk ranges, checks Appendix labels for pages 13–16 and retains Table 4 headers as content. Generated `structured_pdf` also excludes a unique bibliography marker while retaining its Appendix on the same page. |
| Chunks confined to Sections and bounded by configured size | PASS | `test_relative_headings_preserve_paragraphs_section_boundaries_and_pages` checks Section markers, intact paragraph packing and page ranges at body sizes 8/13. `test_configured_chunk_size_packs_whole_paragraphs_without_overlap` checks exact reconstruction without overlap at 35/60 tokens and coexisting retrieval settings. LightRAG yields 31 Chunks, maximum 498 tokens. |
| Generated image-only PDF emits upload error | PASS | `test_image_only_document_reports_missing_text_layer_before_embedding` inserts a bitmap and asserts parsing → error, a scanned/no-text reason, no ready Document or LLM call. Browser displays the same reason: [scanned upload](evidence/scanned-upload.png). |
| Heading-free PDF uses virtual Sections and remains askable | PASS | `test_heading_free_document_uses_bounded_virtual_sections_and_can_be_asked` checks multiple <=500-token virtual Sections, successful final answer/Citation and source page/title parity. |
| Citation side-note shows page and Section title | PASS | Browser shows `[C1] · p.1–2` / `1 Introduction`. Its button opens the original Chunk: [desktop](evidence/citation-sidebar.png), [source](evidence/citation-source.png), [mobile](evidence/citation-mobile.png). |
| Gap 2: corrupt/non-PDF uploads display a clear error | PASS | `test_invalid_document_has_a_distinct_error_from_missing_text_layer` covers non-PDF, empty and truncated bytes. Browser displays the damaged-PDF and non-PDF reasons: [damaged upload](evidence/invalid-upload.png), [non-PDF upload](evidence/non-pdf-upload.png). A subsequent valid upload succeeds. |
| Review deferral: truncated/invalid PDF is distinct from missing text layer | PASS | The same regression reproduced the #01 misclassification before the fix. Open/repair validation now precedes text extraction; the invalid error does not mention text layers. |
| Review deferral: oversized paragraph overlap snaps to a word/sentence boundary | PASS | `test_long_paragraph_overlap_starts_on_a_complete_word` checks complete unique Latin words, <=500-token Chunks and about 10% overlap. `test_long_paragraphs_split_at_sentence_boundaries_with_overlap` covers English and Chinese. Existing decimal/abbreviation and sentence-less CJK regressions also pass in the full suite. |

## Integration and final checks

- `uv run pytest -q`: **82 passed, 1 deselected**, 72.60 seconds. The deselected test is cloud eval; no cloud LLM was called by the deterministic suite.
- `uv run pytest tests/integration/test_http.py -q`: **4 passed**, including the real default factory reading `CHUNK_TOKEN_TARGET=35` with `LOOKUP_TOP_K=1` present.
- `uv run ruff check src tests scripts/generate_event_types.py`: passed.
- `uv run ruff format --check src tests scripts/generate_event_types.py`: 33 files already formatted.
- `uv run python scripts/generate_event_types.py --check`: backend/frontend types match. #02 does not change `events.py` or generated event fields.
- `git diff --check`: passed.
- `npm run typecheck --prefix frontend` and `npm run build --prefix frontend`: passed; rebuilt `frontend/dist` is committed.

The #06 fixtures now preserve their guarantees without page-level assumptions: Q2 Synthesis strictly expands and preserves baseline evidence while retaining cost/update/community, deduplication, Document order and prompt checks. Extraction fixtures choose IDs from each actual evidence batch and respond to all batches (three for this corpus), still requiring multiple calls, original source Citations, filtering and guarded budgets. The Router and production ask behavior were preserved.

## Browser acceptance

- URL: `http://127.0.0.1:8110`, FastAPI serving the rebuilt production frontend.
- Browser: isolated agent-browser Chrome session `t02-vida`, 1440×900 and 390×844.
- Adapter configuration: real local bge-m3; scripted Router/answer responses, so model quality is outside this UI check.
- Paths: damaged upload → scanned upload → non-PDF upload → successful structured upload → ask → Citation sidebar → original source click.
- Desktop measurement: answer right edge <= sidebar left edge, `noOverlap=true`, horizontal `overflow=false`.
- Mobile measurement: `overflow=false`, sidebar moves below answer, original source is reachable.
- Browser `errors` and `console`: empty. Screenshots were visually inspected.
- All ticket-started backend/browser processes are stopped before review delivery.

## Implementation paths at the review head

- `src/chat_document/api.py:45`: factory receives both environment settings; `:57` wraps synchronous upload events in SSE.
- `src/chat_document/application.py:39`: combined keyword-only configuration and positive Chunk target guard; `:58` parsing → chunking → embedding → ready; DocumentError → invalid_document, other ingestion failures → error; `:91` retains #06 Router/packing/answer paths.
- `src/chat_document/pdf_parser.py:200`: open/repair/type/password validation → normal text extraction → no-text or Sections. `:28` extracts typed text lines and relative font statistics. `:67` heading filtering; `:81` combines separate numbers/titles. `:117` flushes paragraph/Section boundaries, enters References exclusion, resumes at Appendix and propagates Appendix state. `:101` falls back to bounded virtual Sections.
- `src/chat_document/models.py:15`: backward-compatible Section metadata; `:27` unchanged Chunk fields and title-prefixed context.
- `src/chat_document/chunker.py:90`: per-Section paragraph packing and exact Chunk page ranges. `:55` splits only oversized paragraphs; `:14` keeps Unicode characters bounded; `:28` snaps approximately 10% overlap to sentence/word starts, with character-safe fallback for sentence-less CJK.
- `frontend/src/Answer.tsx:3`: live marker mapping and only-used Citation notes; `:15` displays page range/Section and uses the existing source callback. `frontend/src/styles.css:27` supplies minimal responsive positioning; #09 owns final design.
- `tests/integration/test_ingestion.py:18`: requirement-based upload/ask regressions. `test_router_synthesis.py:94`, `:139`, `:360` and `test_router_review.py:38`: parser-dependent #06 fixture integration. `test_http.py:40`: default factory configuration.

## Limits and remaining work

No unresolved assigned acceptance item. Table reconstruction remains #03, background ingestion/cache #04 and final design #09. D02 remains pending and blocks #09 finalization only. PDF validation conservatively rejects repaired Documents; PyMuPDF's `is_repaired` represents major structural repair, not an exhaustive PDF validator. Second-document generalization remains #10. Cloud answer/Golden Facts evaluation was not run or claimed for this ticket.
