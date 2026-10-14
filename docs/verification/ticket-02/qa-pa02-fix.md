# Ticket #02 — PA-02 / F1 correction

Historical F1 candidate. HCOM #4773 confirmed this correction and requested a geometry guard for numeric columns; the current candidate and verification are recorded in [N1 correction](qa-n1-fix.md).

Requested in HCOM #4427 after independent QA on integrated main. Base: `056b3e46d8410b946de8b36b46ea14b6b79651c2`. Implementation checkpoint: `3cf7405f23a5d1c43ff8a3b865467477629870a5`. Final evidence head is supplied in the review request. Original [QA report](qa/qa-report.md) remains unchanged as failure evidence.

## Changes and regression evidence

All new regressions exercise `Application.upload_document` with generated, text-layer PDFs, real PyMuPDF and local bge-m3. No internal parser/chunker mock or LLM call is used.

| Failure | RED evidence | Result after correction |
| --- | --- | --- |
| Wrapped Chinese sentence cut at a newline when its valid sentence end exactly equals the token hard end | Generated 160-sentence lunar-basalt paragraph fails the all-Chunk sentence-ending assertion. | `_paragraphs` distinguishes a found sentence end from `None`; equality with the token cut keeps the sentence boundary. Every Chunk is bounded and consists of complete source sentences; all 160 sentences remain covered. |
| Short CJK sentence within overlap window skipped by the minimum-overlap heuristic | Alternating long sentences and `完成1！`-style 3-token sentences fails the complete-sentence Chunk-start assertion with the old overlap condition. | Starts after 。！？ are accepted even for a short overlap. Test checks bounded Chunks and a complete shared sentence between each adjacent pair. Outside a usable sentence start, existing Unicode-character / Latin-word fallback remains. |
| PDF line wraps split CJK text/numbers | Source/Chunk assertion fails on `區域1\n4` and `4\n9`. | In a CJK-containing paragraph only, remove newlines flanked by CJK/digit characters. `區域14` and `49` survive intact, while `Sample 14\nstayed stable.` and `Sample\n14` keep their Latin spacing. Pure Latin/table paragraphs retain their existing text. |

Existing English sentence, decimal/abbreviation, whole-word overlap and sentence-less CJK tests remain covered. The latter still permits character splitting when no sentence boundary fits. Section/page metadata, paragraph boundaries, upload events and Application configuration/seams are unchanged.

## Verification before #04 integration

- `uv run pytest tests/integration/test_ingestion.py -q`: **35 passed**, 11.28 s.
- Earlier focused English/Chinese/oversized-character tests: **13 passed** before line normalization; normalization-focused checks: **5 passed**. Final complete suite covers all of them together.
- Full `uv run pytest -q`: **176 passed, 2 deselected**, 144.38 s; six existing dependency deprecation warnings.
- `uv run ruff check src tests eval scripts`: PASS.
- `uv run ruff format --check src tests eval scripts`: PASS, 61 files.
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `git diff --check`: PASS.

Re-ran the QA agent's original `qa-chinese.pdf` through the public upload operation with real bge-m3: **ready; 11 Chunks; maximum 498 tokens; 11/11 Chunks ending at 。; 160/160 numeric facts preserved; short concluding paragraph retained**.

No frontend/event change or browser/backend process was needed for this fix. No live LLM/Golden Facts evaluation is claimed. #04 confirms its source-derived processing identity includes parser/chunker files, so these changes automatically invalidate old records after merge/restart; effective Chunk target remains in its configuration identity.

## Implementation paths

- `src/chat_document/chunker.py:28`: token-bounded overlap window → usable sentence start (CJK short sentence accepted) → existing word/character fallback.
- `src/chat_document/chunker.py:57`: oversized paragraph splitting → explicit optional sentence boundary → whitespace/character fallback only when no boundary was found.
- `src/chat_document/pdf_parser.py:21`: CJK/digit line-wrap character classes; `:347`: same-paragraph flush removes matching CJK wraps before storing source text, preserving original page provenance.
- `tests/integration/test_ingestion.py:418`: 160-sentence wrapped-Chinese boundary/source-coverage regression; `:444`: numeric wrap and Latin spacing regression; `:462`: short-sentence overlap regression.

Awaiting independent review. Repaired-PDF acceptance, source panel page-range formatting, title-token accounting and #10 figure/frame edge cases remain the agreed notes/deferrals.

## Rebase onto integrated #04

Per HCOM #4584, the review request above is superseded by a candidate on `4eee3d20ebd09838cf450458b99bed058edc21f9`. Rebased implementation: `c538e66`; source/evidence checkpoint before this addendum: `830af11`. Only the AI log conflicted, and both #04 and #02 entries were preserved. Application, cache, events and frontend code are byte-identical to this integrated main.

- Full `uv run pytest -q`: **195 passed, 2 deselected**, 212.02 s; six existing dependency warnings.
- Ruff check/format: PASS, 64 files; event parity and `git diff --check`: PASS.
- Original QA Chinese PDF through background ingestion with a temporary real processing cache: first upload makes 2 native bge-m3 batches; a fresh Application reload emits only ready, makes 0 embedding calls, restores identical Sections/Chunks and updates the filename. The replay still contains 11 sentence-ending Chunks, maximum 498 tokens, all 160 numeric facts. [Recorded replay checks](qa-pa02-cache-replay.json).
- #04's source-derived identity includes parser/chunker, so the changed source invalidates old records on restart; no cache code/version override was added. The temporary verification cache was removed and both Applications closed.

Final integrated head is supplied in the superseding review request. No server/browser process or new live LLM evaluation was needed.
