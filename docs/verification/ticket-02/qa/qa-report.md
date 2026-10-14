# QA report: ticket #02 (structure-aware parsing and chunking), integrated main 3a15958

QA agent model: claude-sonnet-5-5. Date 2026-10-13. Repo source untouched; no commits; only this directory added.
Scripts lived in the session scratchpad (`scratchpad/qa02/`), outputs copied here.

## Runs

- `uv run pytest -q`: 173 passed, 2 deselected (eval), 96.9 s.
- `uv run pytest tests/integration/test_ingestion.py -q`: 32 passed.
- Real server on 127.0.0.1:8204 (uvicorn from main checkout, real Ollama bge-m3 + gpt-oss cloud), real browser via agent-browser. Server and browser stopped; 8204-8206 free; shared Ollama daemon left running.

## Acceptance criteria

| # | AC | Verdict | Evidence |
|---|---|---|---|
| 1 | LightRAG: all main chapters Introduction..Conclusion + Appendix | PASS | `lightrag-structure.txt`: 28 Sections incl. 1 INTRODUCTION, 2, 3 (split number/title merged), 3.1-3.4, 4, 4.1-4.5, 5, 5.1-5.2, 6 CONCLUSION, 7 APPENDIX + 7.1-7.4 (7.3.1-7.3.4). No figure-label fake Sections. |
| 2 | No References in Chunks; Appendix Chunks flagged | PASS | `lightrag-checks.txt`: pages 11-12 (references) have zero Chunks; no bibliography strings in any Chunk; every Chunk on p13+ belongs to an `is_appendix` Section and vice versa. |
| 3 | No Chunk crosses Section; none over target except single long paragraph | PASS | Default 500: max Chunk text 493 tokens, max with Section title context 513 (title prefix is not counted against the target; observation only). Targets 250 and 800 also give zero over-target Chunks (`lightrag-structure-target250/800.txt`). Chunk page ranges always within Section range. |
| 4 | Image-only PDF gives error event on upload | PASS | Own generated 2-page image-only PDF: SSE `error` code `invalid_document`, "no text layer; scanned PDFs are not supported." UI shows it (`ui-error-scanned.png`, `ui-error-texts.txt`), Question box disabled. |
| 5 | Heading-free PDF processed with virtual Sections and askable | PASS | `generated-pdfs-structure.txt`: 4 virtual Sections, 4 Chunks. UI: asked "zorblax reading number 33", answer 133 with `[C3] p.4-5 Virtual Section 3`; click opens original Chunk (`ui-noheadings-*.png`). |
| 6 | Citation side-note shows page + Section title | PASS | UI LightRAG Q3: "[C3] p.7-8 4.3 ABLATION STUDIES (RQ2)"; click opens "Source p.7 4.3 ABLATION STUDIES (RQ2)" with original text (`ui-lightrag-answer.png`, `ui-lightrag-source.png`). Also two-column and Chinese docs. Minor: source header says "p.7" while side-note says "p.7-8" (start page vs range). |

## Extra items (EXECUTION.md)

| Item | Verdict | Evidence |
|---|---|---|
| Corrupt/non-PDF errors shown in UI, distinct text | PASS | Non-PDF renamed .pdf: "Please upload a valid PDF Document."; truncated LightRAG (50% of bytes): "...this PDF is damaged."; scanned: no-text-layer text. All visible in `role=alert`, three different messages (`ui-error-texts.txt`). A valid PDF uploaded afterwards succeeded. |
| Truncated PDF not reported as "no text layer" | PASS | Truncated LightRAG -> "damaged"; small truncated PDF repaired and accepted. |
| Overlap start snaps to word/sentence boundary | PASS (English/mixed) / see F1 (CJK) | 1500-word single sentence: every overlap begins on a whole word (`word-and-mixed-split.txt`). Mixed 。！？/English text splits only at sentence ends. CJK defect below. |
| Known limits deferred to #10 (figure step labels, unnumbered headings in frames) | NOT_EXECUTED | Not exercised by LightRAG output (no fake Sections found); left to #10 as agreed. |

## Test-list rows mapped to #02

| Row | Verdict | Note |
|---|---|---|
| PA-01 | PASS | Same evidence as AC1-3. |
| PA-02 | FAIL (part b/c) | (a) bold/size heading detection incl. two-column numbered headings and 12pt-agnostic: PASS (`generated-pdfs-structure.txt`, twocol: 5 Sections, References dropped, column order correct). (d) config changes chunking (250/65 Chunks, 500/41, 800/31): PASS. (b)/(c) sentence-boundary split of oversized paragraphs: PASS for English and mixed; FAIL for CJK text with line-wrap newlines, see F1. Overlap size is ~6-11% of the Chunk (sentence-start snapping), "about 10%" acceptable. |
| PA-03 | PASS | AC5. |
| UP-04 | PASS (#02 scope) | Scanned plus corrupt/non-PDF: error event, UI shows reason, input disabled, re-upload works. Not-hanging-on-progress confirmed. |
| CT-01 | PASS (#02 scope) | Side-note page + Section and click-through verified; 404 / table form belong to other tickets (NOT_EXECUTED here). |
| RV-04 (Chunk size part) | PASS | Target change via `chunk_token_target`; README documents `CHUNK_TOKEN_TARGET`. |

## Findings

### F1 (FAIL, defect, medium-low): oversized CJK paragraph cut mid-sentence when the 500-token cut coincides with a sentence end

Location: `src/chat_document/chunker.py`, `_paragraphs`: `if end == hard_end:` treats "best sentence boundary happens to equal `hard_end`" the same as "no boundary found", then falls back to the last whitespace before `hard_end`. Chinese PDFs contain line-wrap `\n` inside sentences, so the fallback cuts mid-sentence (and the next overlap then also begins mid-sentence because `_overlap_start` has no CJK fallback).

Reproduction:
1. `uv run python scratchpad/qa02/gen.py` creates `qa-chinese.pdf` (one 5,000-token paragraph of 。-terminated sentences).
2. `uv run python scratchpad/qa02/zh.py <pdf>` shows Chunks 1, 5, 7 of 12 ending mid-sentence (e.g. `...鐵含量在區域1`), Chunk 2 starting at `顯示，月球玄武岩...` (`chinese-overlap.txt`).
3. `cause.py` shows `hard_end` (498) is itself a sentence boundary.
4. Randomised Chinese text with 60-char line wraps: 80 of 1,848 pieces (4.3%) not ending at 。; English 0 of 803 (`sentence-boundary-repro.txt`).
Impact: violates "only split at sentence boundary" for CJK; retrieval still works (UI answered the number question correctly with C4/C5). Suggested fix: use a "found" flag instead of comparing to `hard_end`.

### Observations (not failures)

- O1: a truncated PDF that MuPDF can repair (small test: 3 of 6 pages) is accepted as Ready with only a server-side warning; the user is not told pages are missing (documented behaviour in README: "repaired PDFs ... accepted with a logged warning").
- O2: raw line-wrap `\n` remains inside CJK text and numbers (e.g. `區域1\n4中`); harmless to the answer test but can hurt embedding quality.
- O3: Table 2 text is in Chunks of section 4.3 (`table2-section43.txt`) but is flat cell-per-line text; structure rebuild is #03, not judged here. Answer quality for Q3 with real gpt-oss was wrong on several numbers (also #03/#11).

## Counts

Rows evaluated: 6 AC (6 PASS), 4 extra items (3 PASS, 1 NOT_EXECUTED), 6 mapped test-list rows (5 PASS, 1 FAIL via F1). UNPROVEN: none.

## Evidence files (this directory)

lightrag-structure*.txt, lightrag-checks.txt, table2-section43.txt, generated-pdfs-structure.txt, chinese-overlap.txt, sentence-boundary-repro.txt, word-and-mixed-split.txt, ui-error-texts.txt, ui-*.png.
