# Ticket #02 — N1 numeric columns and cross-page paragraphs

Requested in HCOM #4773 after the independent reviewer confirmed PA-02/F1 fixed. Base: `d56e092138f6d5c87c75e042caf4f79e0db6989c`. Implementation checkpoints: `ffa7d2b` (geometry and page continuation) and `66c9ae6` (grouped numeric rows). Final evidence head is supplied in the re-review request. The [earlier F1 report](qa-pa02-fix.md) and original QA failure evidence remain historical records.

## Changes and regression evidence

All regressions use generated text-layer PDFs through `Application.upload_document`, real PyMuPDF and real local bge-m3. The empty ScriptedLLM records that ingestion makes no LLM call.

| Failure | RED evidence | Correction and public-operation checks |
| --- | --- | --- |
| CJK-containing blocks concatenate stacked decimal/year values | `區域 數值\n1.2\n3.4\n2023\n2024` becomes `區域 數值1.23.420232024`. | Keep each source line's block bbox. Join only vertically consecutive lines in the same block, or eligible page continuations, when the previous line occupies at least 90% of its block width. Preserve numeric-only rows even if they occupy the full width. Three cases assert exact source paragraph and Chunk equality: decimal/year values, repeated full-width years, and grouped integers. |
| Numeric-only detection misses digit-grouping spaces | The additional case `區域 數值\n1 234\n2 345` fails with concatenated rows; the first two numeric cases pass. | Treat whitespace as part of a numeric-only line. All three cases plus the positive CJK wrap/Latin-spacing case pass: **4 passed**, 1.68 s. |
| Paragraphs always end at page boundaries | English and Chinese unfinished-sentence cases fail; the already-finished controls pass. | Adjacent pages continue the paragraph when the previous line has no sentence-ending punctuation, is not numeric-only, and the next line has matching typography and an aligned left edge. Section headings still flush before this decision. Four cases assert paragraph count, original content, source page ranges and Chunk pages. Finished sentences remain separate paragraphs; continuations retain `(1, 2)`. |

The positive `區域1\n4` / `4\n9` fixture now uses long lines that satisfy the geometry rule, retaining its exact number and Latin-spacing assertions. An existing packing fixture now explicitly ends its intended separate paragraph with a period; its paragraph count, reconstruction and token-bound assertions were retained.

The final geometry subset (two original numeric cases, positive wraps, the 160-sentence boundary regression and four page cases) passed **8 tests**, 44.84 s. The earlier focused ingestion/HTTP/background-job checks passed **64 tests**, 20.58 s; the complete suite below includes the final width metric and third numeric case.

## Final verification

- `git rebase main`: branch already current with the base above.
- `uv run pytest -q`: **202 passed, 2 deselected**, 134.75 s; six existing dependency deprecation warnings. This is the complete run after the grouped-number correction. An earlier run was interrupted to add that regression and is not used as final evidence.

- `uv run ruff check src tests eval scripts`: PASS.
- `uv run ruff format --check src tests eval scripts`: PASS, 64 files.
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `git diff --check`: PASS.

`uv run python /private/tmp/t02-n1-replay.py` re-ran the original QA `qa-chinese.pdf` through public background ingestion with a temporary real processing cache. First upload made **2** native bge-m3 batches; a fresh Application hit disk cache, emitted only ready, made **0** embedding calls and restored identical Sections/Chunks with the new filename. Both runs retained **11/11** sentence-ending Chunks, **498** maximum tokens, **160/160** numeric facts and the short concluding paragraph, with no LLM call. [Recorded checks and pipeline identity](qa-n1-cache-replay.json). Both Applications were closed and the temporary cache removed.

No Application, cache, event or frontend source changes. No live LLM/Golden Facts evaluation is claimed. Parser/chunker changes are included in #04's source-derived processing identity and invalidate prior cache records on restart; no version override was introduced. No server/browser process was started for this correction.

## Implementation paths

- `src/chat_document/pdf_parser.py:25`: numeric-only line detection, including grouping spaces.
- `src/chat_document/pdf_parser.py:336`: adjacent-page continuation eligibility.
- `src/chat_document/pdf_parser.py:349`: geometry and numeric-row guards for genuine wraps.
- `src/chat_document/pdf_parser.py:383`: paragraph assembly makes per-line separator decisions.
- `src/chat_document/pdf_parser.py:449`: page/block boundary handling; paragraph page provenance is preserved.
- `tests/integration/test_ingestion.py:444`: genuine CJK wraps and retained Latin spacing.
- `tests/integration/test_ingestion.py:474`: exact stacked-value source/Chunk regression.
- `tests/integration/test_ingestion.py:484`: English/Chinese page continuations and finished-sentence controls.

The reviewer already confirmed F1 and randomized overlap checks in #4773. Figure/frame edge cases remain deferred to #10 as agreed; no additional parsing feature is introduced here.
