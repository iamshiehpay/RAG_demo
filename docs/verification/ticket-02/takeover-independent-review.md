# #02 independent re-review (nova-r02-mige)

- Reviewer: nova-r02-mige, claude-opus-5-5, effort medium (launch `--model claude-opus-5-5 --effort medium`, env `CLAUDE_EFFORT=medium`).
- /code-review child contexts (both read-only, general-purpose): Standards and Spec. Their transcripts record `"model":"claude-opus-5-5"` and `"effort":"medium"` on every turn (8 Standards turns, 17 Spec turns). Resources: Spec probe scripts in `/private/tmp/claude-501/mige-spec/` (probe.py, probe2.py, probe3.py). No ports, servers or containers.
- Range: base `d56e092138f6d5c87c75e042caf4f79e0db6989c`, head `7d209b71c319677b6d5dbdf86f945140cf2f1f5b`. Commits: c29e9d1, 93d0bbb, cd83ea2, ffa7d2b, 66c9ae6, 7d209b7. Main is now cd3e303, which adds only docs after d56e092.

## Verdict: CHANGES_REQUESTED

### R1 — Major — cross-page continuation joins prose to a Table caption at the top of the next page (real LightRAG regression)

- **Path:** `src/chat_document/pdf_parser.py:336-346` (`_continues_on_next_page`), used at `:449-451` and `:358`.
- **Trigger:** the last prose line of page N has no sentence-ending punctuation, and page N+1 starts with a caption in the same font and at the same left edge. The rule never checks that the next page's first block is body text, even though #4773 asked to merge only when "the next page's first block continues it".
- **Evidence:** `data/lightrag.pdf`, parsed with `parse_pdf` at the base commit and at the head commit. The paragraph count drops from 138 to 134. Two of the four new joins are correct (§4.5 p.9→10 and §7.2 p.13→14). The other two are wrong:
  - §4.2: "...we draw the following conclusions:\nTable 1: Win rates (%) of baselines v.s. LightRAG ..." The paragraph's provenance becomes (6,7), although all of its prose is on p.6.
  - §4.4: "...hierarchical retrieval paradigm, which combines in-depth\nTable 3: Case Study: Comparison Between LightRAG and the Baseline Method GraphRAG." The sentence's real continuation ("explorations of related entities ...") stays a separate paragraph, so the sentence is now spliced to an unrelated caption.
  - Both sections feed the Q2 and Q3 Golden Facts (Table 1 win rates, Table 3 case study).
- **Generated triggers (Spec probe):**
  - A page-2 `Figure 3: An overview of the pipeline` caption is merged into the body paragraph, which is tagged (1,2).
  - A CJK running header `期刊名稱 第十卷` is glued in with no separator: `…觀察記錄期刊名稱 第十卷繼續的內容。`
- **Expected:** Table/Figure caption lines, and lines that don't continue body text (such as running headers), are never used as continuation targets. Add a regression that checks the LightRAG §4.2/§4.4 paragraphs or a generated caption-at-page-top case, plus a running-header negative.

### R2 — Major — N1 is only partly closed: CJK rows with a label and a value are still concatenated

- **Path:** `src/chat_document/pdf_parser.py:349-364` (`_wraps_line`) and `:383-395` (separator decision).
- **Trigger:** each line is compared with its own block's width. When every line in a block has a similar width, every line meets the 90% threshold. Rows that mix CJK labels and numbers fail `_NUMERIC_LINE`, so they are treated as line wraps.
- **Repro (I ran it myself):** `parse_pdf(paragraph_pdf("區域甲 1.2\n區域乙 3.4\n區域丙 5.6", cjk=True))` returns `['區域甲 1.2區域乙 3.4區域丙 5.6']`. Two full-width list items ending `…1` and `…2` are glued in the same way. This is the #4773 data-corruption class with a label added to each row; the existing tests only cover numeric-only rows.
- **Expected:** decide whether a line is a genuine wrap from evidence that a row-shaped block cannot satisfy. For example, require the block to wrap against a wider reference than itself (column or page text width), or require the block to have a shorter final line. Add a labelled-row regression next to the stacked-value cases.

### Non-blocking (Minor / notes)

- **N-a (Minor):** `chunker.py:39-54`. When the last CJK sentence before the cut is longer than the ~10% overlap window, the next Chunk starts mid-sentence: with ~110-character sentences at target 500, Chunks 2-4 begin `武岩含量…`. This matches the QA PA-02 fix request ("else character start"), and every Chunk still ends on a sentence. I'm recording it, not blocking on it.
- **N-b (Minor):** two-column continuation (the right column on page N continues in the left column on page N+1) fails the left-edge check (`<= 2*size`), so the paragraph still splits there. This is not a regression; it matters for the two-column second document (#10).
- **Standards (judgement calls):**
  - `_continues_on_next_page` repeats the unnamed 0.5 / 2×size style tolerances from the heading-continuation logic (~:307-311). A shared `_same_style` helper would remove the duplication.
  - `chunker.py:42` hard-codes `"。！？"` again, separately from `SENTENCE_BOUNDARY`.
  - `flush_paragraph` builds a synthetic string just to reuse the `_CJK_LINE_WRAP` regex.
  - `_Line.block_bbox` copies block data onto every line (Data Clumps).
  - In the tests, `count_tokens(sentence) < 50` is a fixture precondition, not a behaviour check.
  - `page_continuation_pdf` is imported inside the function body.
  - No hard breach of AGENTS.md: no hard-coded font size, PyMuPDF/tiktoken only, CJK and English sentence enders both handled, CONTEXT vocabulary used.

### Verified OK

- **F1 (original CJK sentence regression):** closed for the QA shape. The 160-sentence wrapped regression passes, and so does the short-sentence overlap regression.
- **Numeric-only rows:** decimal/year, repeated full-width years and grouped integers keep their `\n`. A `…共計` / `2024` numeric-only line also keeps its `\n`, and `…共計` / `2024年完成。` joins correctly (Spec probe).
- **Cross-page provenance:** a genuine continuation gives `paragraph_pages` (1,2) and Chunk `page_start`/`page_end` (1,2). Finished-sentence controls stay separate.
- **#04 shared behaviour:** no changes to application, cache, events or frontend in the diff. Parser and chunker edits are covered by #04's processing identity, which is derived from the source.

## Commands and results (head 7d209b7)

- `uv run ruff check src tests eval scripts`: PASS. `uv run ruff format --check src tests eval scripts`: PASS (64 files).
- `uv run pytest -q tests/integration/test_ingestion.py`: 42 passed, 15.92 s. I did not re-run the full suite; the implementer reported 202 passed / 2 deselected.
- LightRAG base-vs-head diff: scratchpad `cmp.py`, `diff.py` and `show.py` (run with `uv run python -I`). The base source was extracted with `git archive d56e092 src`.
- Labelled-row repro: scratchpad `rows.py`.

## Implementation paths (actual)

- `src/chat_document/pdf_parser.py:21-25`: wrap ratio, CJK ranges, `_CJK_LINE_WRAP` and `_NUMERIC_LINE`.
- `src/chat_document/pdf_parser.py:38, 168`: `_Line.block_bbox`.
- `src/chat_document/pdf_parser.py:336-346`: `_continues_on_next_page` (R1, N-b).
- `src/chat_document/pdf_parser.py:349-364`: `_wraps_line` (R2).
- `src/chat_document/pdf_parser.py:377-399`: `flush_paragraph` line joining.
- `src/chat_document/pdf_parser.py:447-456`: page/block flush decision.
- `src/chat_document/chunker.py:36-45`: CJK overlap start (N-a).
- `src/chat_document/chunker.py:69-90`: explicit sentence-boundary-found handling (the F1 fix).
- `tests/integration/fixtures.py:37-52`: `page_continuation_pdf`. `tests/integration/test_ingestion.py:418-539`: new regressions.

## Next step

Main dispatches an Implementer for R1 and R2, each fix with a RED→GREEN regression (R1 should include a LightRAG real-PDF assertion). After that, re-review the same range plus the fix commits.

---

# Re-review 2 (nova-r02-mige): R1/R2 fixes

- Reviewer: the same session. The parent process args are `claude --model claude-opus-5-5 --effort medium` and `CLAUDE_EFFORT=medium`. I reviewed inline and spawned no child contexts this round.
- Range: full original range `d56e092..582d07e7f50e993cac8131e8b21946068b541d06`, rebased onto main `03e6f361`. `git range-diff` shows commits 1-6 are identical to the version I reviewed in round 1 (c29e9d1..7d209b7 → 102c810..a969dd6). New commits: acfea43 and 26600be (fixes), 582d07e (docs). I reviewed the source delta `a969dd6..26600be`.

## Verdict: CHANGES_REQUESTED (one new Medium; R1 and R2 are closed)

### R1 — FIXED
On `data/lightrag.pdf`, compared with base d56e092: 138 → 136 paragraphs. The only joins left are the two genuine ones, §4.5 (9,10) and §7.2 (13,14). The §4.2 and §4.4 paragraphs no longer absorb the Table 1 or Table 3 caption, and their provenance is back to (6,6) and (8,8). Generated Figure, Table and CJK running-header cases are covered by public-upload tests.

### R2 — FIXED for the reported triggers
- `區域甲 1.2 / 區域乙 3.4 / 區域丙 5.6`, the short-final-row variant, and equal-width list items all keep their separators.
- Cells separated by a gap with no space character also stay separate. They come out as separate lines: `區域甲\n1.2\n…`.

### M3 — Medium (new regression from 26600be/acfea43): CJK line wraps are no longer joined when a block's final line is nearly full and the block doesn't use symmetric single-column margins

- **Path:** `src/chat_document/pdf_parser.py:177-180` (the `flow_width` estimate) and `:203-216` (`flowing_block`), which gate `_wraps_line` at `:405`.
- **Cause:** `flow_width` assumes symmetric margins.
  - Single column: page width − 2·left.
  - Two columns: half the page width − (x mod half the page width). For the right column this gives about 279 pt on A4, while the real column is about 246 pt.
  - A block whose final line ends with a full stop and is nearly full therefore fails the `>= 90% flow_width` branch. It isn't ragged either, so `flowing_block` is False and every same-block CJK wrap keeps `\n`. This is exactly the PA-02 behaviour that let "區域1\n4" split a number.
- **Triggers** (scratchpad `fullfinal.py`, `asym.py`):
  - Two-column page, right-column textbox x=316–562, CJK paragraph of 96 or 120 characters ending in `。`: lines come back as `[24,24,24,24]`. The previous candidate a969dd6 returned `[96]`, and the left column still returns `[96]`.
  - Single column with asymmetric margins, textbox x=50–480 on A4, four full lines: `[43,43,43,43]`. a969dd6 returned `[172]`.
  - About 10% of paragraphs end on a ≥90%-full line, so this hits right-column CJK paragraphs in two-column documents. AGENTS.md requires a two-column second document and lists a Chinese PDF as a bonus.
- **Expected:** use a measured reference, not an assumed-symmetric one. Options: the widest body line in the same column or block band on the page, or the column extent from `_ordered_blocks`. Add right-column and asymmetric-margin regressions next to `test_genuine_cjk_wrap_with_a_full_final_line_keeps_source_text_intact`.
- **Standards note:** the `flow_width` one-liner with the modulo expression is hard to read (possible Mysterious Name / magic expression). A named helper would make the column assumption visible.

### Notes (non-blocking)
- **Pre-existing:** a CJK wrap before line-initial punctuation (`記錄\n。`) keeps `\n`, because `。` isn't in `_CJK_LINE_WRAP`. It's unchanged since a969dd6 and is mostly a fixture artifact, since real typesetting forbids `。` at the start of a line.
- **Round-1 minors:** N-a (mid-sentence CJK overlap start) and N-b (a two-column paragraph that continues from the right column into the next page's left column still splits) are unchanged and remain non-blocking.

## Commands and results (head 582d07e)
- `uv run ruff check src tests eval scripts`: PASS. `ruff format --check`: PASS (64 files).
- `uv run pytest -q`: **210 passed, 2 deselected**, 177.47 s, with 6 existing warnings.
- LightRAG base-vs-head: scratchpad `cmp.py` → `h2.json`. Other probes in the scratchpad: `twocol.py`, `fullfinal.py`, `asym.py`, `r2probe.py`; previous-candidate source in `prev1/` (a969dd6). No ports, services or processes left running. Tree clean.

## Implementation paths (actual, head 582d07e)
- `pdf_parser.py:26-27`: `_LABELLED_NUMERIC_ROW`, `_CAPTION`.
- `pdf_parser.py:44-46`: `_Line.flow_width`, `page_first`, `flowing_block`.
- `pdf_parser.py:177-180`: `flow_width` estimate (M3).
- `pdf_parser.py:200-216`: page-first and flowing-block marking (M3).
- `pdf_parser.py:362-374`: `_body_continuation_target` (R1).
- `pdf_parser.py:377-390`: `_continues_on_next_page` caption, colon and target guards (R1).
- `pdf_parser.py:393-417`: `_wraps_line` flowing and labelled-row guards (R2).
- `pdf_parser.py:501-505`: flush after a page-first line that isn't a body continuation (R1).
- `chunker.py`: unchanged since round 1.
- `tests/integration/fixtures.py:55-67`: `page_top_interruption_pdf`.
- `tests/integration/test_ingestion.py:551-634`: R1/R2 regressions and the LightRAG real-PDF check.

## Next step
The Implementer fixes M3 with right-column and asymmetric-margin RED→GREEN regressions. After that I re-review only the M3 delta plus the LightRAG and probe re-runs.

---

# Re-review 3 (nova-r02-mige): M3 delta on source 2ee613b (interim)

- Same session; Opus 5.5 at medium effort; no child contexts this round. Source delta reviewed: `26600be..2ee613b`, which touches `src/chat_document/pdf_parser.py`, `tests/integration/fixtures.py` and `tests/integration/test_ingestion.py`. Base is main `03e6f36`, unchanged.
- **M3: FIXED.** The symmetric-margin `flow_width` estimate is gone. `_measured_flow_width` (pdf_parser.py:250) now takes the widest same-style, left-aligned line on the page whose right edge does not pass the block's right edge plus 2×size. It excludes shared-row lines, captions and numeric-only lines. `_aligned_style` (:241) now holds the same-style test that `_continues_on_next_page` used to inline. `continuation_width` (:230-237) gives a page-first line the previous page's measured body width, which keeps the R1 running-header protection. `page_first` is now recomputed after the figure-label filter.
- **My probes against an archive of 2ee613b:**
  - `fullfinal.py`: right-column paragraphs of 95, 96, 97, 119 and 120 characters now join the same way as the left column: `[96]` and `[120]`, against `[24×4]` and `[24×5]` at 582d07e.
  - `asym.py`: the asymmetric single-column case gives `[172]`, against `[43×4]`.
  - `twocol.py`: unchanged.
  - R2 `rows.py`: labelled rows keep their separators.
  - LightRAG: the parse at 2ee613b is byte-identical to the 582d07e parse (`h3.json` = `h2.json`), so the R1 closure and the genuine joins at §4.5 and §7.2 are preserved.
- **Tests:** the new `test_cjk_full_final_lines_use_the_actual_column_or_text_width` covers the asymmetric-margin case and the 96- and 120-character two-column cases through public upload. It checks exact paragraphs, page provenance and Chunk text. `uv run pytest -q tests/integration/test_ingestion.py` gives **53 passed** (39.34 s). `ruff check` and `ruff format --check src tests` pass.
- **Implementation paths for M3:** `pdf_parser.py:44-45` (flow_width / continuation_width fields), `:199-201` (per-line measurement), `:230-237` (page_first and continuation_width after the filter), `:241-248` `_aligned_style`, `:251-263` `_measured_flow_width`, `:403` (continuation_width in the target check), `:417` (`_aligned_style` in the continuation check). Tests: `fixtures.py:70-86`, `test_ingestion.py:638-654`.
- **Status:** no new findings. Final APPROVE is pending vera's final documentation head plus my inspection of the full-suite evidence at that SHA.

---

# Final verdict (nova-r02-mige): APPROVE

- **Final head:** `e59e0960af0fe5a2cd315148fb173ebcbeff7d34`. Source and tests are at `2ee613b2a537d55d9ae3bda7edf414787c33779c`. Rebase base is main `03e6f361b1b6ecf283a55ffd9f57304d5a28762b`, confirmed as the merge-base. The full review range is `d56e092..e59e096`.
- **Docs-only head commit:** `e59e096` changes only `docs/verification/ticket-02/qa-m3-fix.md`. `git diff 2ee613b e59e096 -- src tests` is empty, and the tree is clean.
- **Full-suite evidence (inspected, not re-run, per #6625):** `qa-m3-fix.md` reports `uv run --no-sync pytest -q` → **213 passed, 2 deselected**, 258.96 s, with source and tests held at 2ee613b. I checked this against the tree in three ways:
  - `pytest --collect-only` at the head gives **213/215 collected (2 deselected)**, which matches the reported count.
  - It also matches my own 210 passed at 582d07e plus the 3 new M3 parametrized cases.
  - My own 53-test ingestion run on this source passed.
- **Findings status:**
  - F1 / N1 (numeric-only columns), R1 (captions/headers across pages, LightRAG §4.2/§4.4), R2 (labelled CJK rows) and M3 (measured column width): all closed, each verified by the independent probes in Re-reviews 2 and 3.
  - Shared #04 behaviour is preserved: there are no application, cache, event or frontend source changes, and the parser identity is source-derived.
- **Still open, all non-blocking:**
  - N-a: a long CJK sentence can make an overlap start mid-sentence; this matches the QA-specified "else character start".
  - N-b: a paragraph that continues from the right column into the next page's left column still splits (relevant to #10).
  - A line-initial `。` keeps its `\n`; this is a fixture artifact.
  - Standards judgement calls from round 1.
- **Implementation paths (final):**
  - `src/chat_document/pdf_parser.py`:
    - `:21-27` regexes and constants.
    - `:44-46` `_Line` flow, page and flowing fields.
    - `:199-216` measured flow and the flowing-block test.
    - `:230-263` page_first / continuation_width, `_aligned_style`, `_measured_flow_width`.
    - `:393-445` `_body_continuation_target`, `_continues_on_next_page`, `_wraps_line`.
    - `:~455-470` `flush_paragraph` joining.
    - `:~532-536` flush decision.
  - `src/chat_document/chunker.py:36-45` (CJK overlap start) and `:69-90` (boundary-found flag).
  - Tests: `tests/integration/fixtures.py` and `tests/integration/test_ingestion.py:~421-654`.
- **Cleanup:** I started no processes, ports or services. My probes are kept in the session scratchpad (`m3/`, `prev1/`, `base1/`, `*.py`, `h*.json`) and in `/private/tmp/claude-501/mige-spec/`.
- **Next step:** Main runs the separate integrated QA and handles the merge.
