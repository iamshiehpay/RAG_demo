# #03 independent re-review — nova-r03-hazu

- Reviewer: nova-r03-hazu, claude-opus-5-5, effort medium (launch args `--model claude-opus-5-5 --effort medium`, `CLAUDE_EFFORT=medium`)
- Skill child contexts (/code-review Standards + Spec sub-agents): both launched as model opus / effort medium; both self-reported `claude-opus-5-5, effort=medium`. No substitutions.
- Range: d56e092138f6d5c87c75e042caf4f79e0db6989c..f7268f9337a6287f21a2eed6e54dd9d919a15699 (7 commits, full scope), branch lat/03-table-reconstruction, worktree clean before and after.
- Source read-only. Probes only under /private/tmp/nova-r03-* (base/head `git archive` snapshots + /private/tmp/nova-r03-probe). No ports used.

## Verdict: CHANGES_REQUESTED

All 7 prior findings and the #04 cache item are fixed. One new **major** parser regression (headings below a table are absorbed into the table region, deleting the Section) plus one should-fix false-caption trigger.

## Findings

### 1. [major] Heading directly below a table is swallowed into the Table region; the Section disappears
- Path: `src/chat_document/tables.py:144-183` (`_collect`), consumed by `pdf_parser.py:388-397` (table lines skipped before `_section_title`).
- Trigger: caption-above table followed, within `2.2 × row height`, by a numbered/bold heading whose size is ≤ 1.2 × table font (e.g. 9pt table, 10pt same-as-body `2 METHOD DETAILS`). `_collect` only stops on caption, size > 1.2×, gap, or prose; a short heading is none of those.
- Result at head: the heading line becomes a table row → table is no longer rectangular → `reconstructed=False` with `結構未能可靠重建`; heading text is moved into Table raw text; `_sections` never sees the heading, so Section "2 METHOD DETAILS" vanishes and its paragraphs merge into §1 (Section structure / "Chunk 不跨越 Section" contract broken). Base d56e092 keeps the Section.
- Reproduction: `GAP=14 V=head .venv/bin/python -I /private/tmp/nova-r03-probe/adversarial.py heading_after_table` (and `V=base` for comparison); results in `/private/tmp/nova-r03-probe/probe-results.txt`. Also reproduced at GAP=20.
- Related (same root cause, minor): short non-prose body lines right after a table (list items `(a) Alpha subset`, equations) are absorbed the same way, turning a valid grid into an uncertain table and removing that text from Section prose (`adversarial.py list_after_table`).
- Fix direction: stop collection at any line `pdf_parser._section_title/_heading` would treat as a heading (pass heading line indices or a predicate into `reconstruct_tables`), and once a grid has formed stop at rows that break its cell count/column alignment or font size instead of degrading the whole table. Add authored-PDF upload regressions for heading-after-table and list-after-table asserting the Section survives and the table stays reconstructed.

### 2. [should-fix / minor] Prose line that starts with "Table N." / "Figure N:" becomes a caption and steals the paragraph block
- Path: `tables.py:12` (`CAPTION` matches any line start), `tables.py:222-229` (`caption_lines` = every line in the same block, including lines before the match).
- Trigger: a wrapped body line beginning `Table 1. Every value…` (sentence boundary at line start) in a paragraph immediately above a grid whose real caption is below it.
- Result: the whole paragraph block becomes the caption of a `reconstructed=True` Table 1; the paragraph leaves Section prose; the real caption `Table 1: …` stays as a prose paragraph. Text is retained (in the Table Chunk) but caption/label attribution is wrong. If the stolen block were > 2,000 tokens, `split_table` would raise `ValueError("Table caption leaves no room…")` and fail the upload.
- Reproduction: `adversarial.py prose_line_starts_with_table` (head vs base in probe-results.txt).
- Fix direction: accept a caption only when the match is the first line of its block (or a line with distinct caption font/size), and take caption lines from the match onward, not the whole block. Regression test.

### Minor / smells (non-blocking)
- `pdf_parser.py:323,335` reconstructs `table_text`'s private prefix layout to `removeprefix` raw text; any format change in `tables.table_text` silently corrupts virtual-Section raw text. Prefer carrying `raw_text` on the Chunk or a `Table` field.
- `frontend/src/SourceContent.tsx:7` hard-codes the LIMITATION string (backend has one constant).
- `context_packer.py:91-95` deleted the "Global uses Synthesis until #05" note but Global still takes the non-Lookup branch (see integration risks).
- `application.py:260-262` reuses `retrieved` for two types; `ContextPacker.retrieve` returns a wire `RetrievalEvent`.

## Verified items
| Item | Result | Evidence |
|---|---|---|
| Prior 1 centred caption / Table 4 | FIXED | head parse: Table 4 reconstructed, rows `Total Documents 12/10/94/61`, `Total Tokens …`, header `Statistics`; 7.1 prose no longer contains labels |
| Prior 2 caption-below / two-column | FIXED for tested shapes | tests `:372 :381 :485`; probe: caption-below grid keeps following prose |
| Prior 3 limitation test in user message | FIXED | `test_tables.py:161` asserts raw Table Chunk in `messages[-1]`; `npm run test:source` passes |
| Prior 4 `_` cleanup generic | FIXED | `_clean` applied to raw and cells; Figure 2 cost grid has no `_` |
| Prior 5 baseline/candidate header | FIXED | Table 1 header `baseline / candidate`, meaning line consistent; Table 2 `variant` |
| Prior 6 Synthesis bound | FIXED | `test_router_synthesis.py:130-135` subset of seeds + links |
| Prior 7 oversized raw line | FIXED | binary-search split, test `:403` |
| Data association + numeric preservation | PASS | LightRAG, all Chunks base vs head: numeric-token multiset identical (421 = 421, no missing, no extra); Table 1/2 16×6 with dataset/metric per cell; Sections/titles/pages identical to base, only table text moved |
| Caption above/below/centred/gutter | PASS for LightRAG + authored tests; FAIL for heading/list-after-table (Finding 1) and prose false caption (Finding 2) |
| Uncertain fallback | PASS | Table 3, Table 5, Figure 2 keep raw text + marker; prompt rule uses LIMITATION; UI note |
| Oversized rows | PASS | reconstructed splits at rows with caption/header; raw lines split by character bound |
| Cache identity | PASS | `PIPELINE_SOURCES` includes tables.py, embedder.py (policy.py, tokens.py already); test `:445` |
| Retrieval linking/order/drops | PASS | seeds → reciprocal links → Lookup neighbors by seed rank → whole-Chunk fit → Document order; drop count in RetrievalEvent and all Trace paths (success + 4 error paths); events parity OK |
| #04 lifecycle preservation | PASS | application.py diff touches only `ask`; upload/background/cache swap untouched |
| GoldenFact prompt leakage | NONE | answer_generator rules and tables.py meaning contain no 64.8/60.0/74.4/67.6/50.4/49.6/-Low/-Origin/NaiveRAG/LightRAG literals; baseline name comes from parsed header |
| Q3 quality | Recorded honestly (numeric exceptions 0/3, forbidden 2/3), deferred to #11; not counted against #03 |

## Checks actually run (f7268f9)
- `uv run pytest -q -p no:cacheprovider` → **208 passed, 2 deselected**, 174.62s, exit 0
- `uv run ruff check src tests scripts/generate_event_types.py scripts/measure_table_reading.py` → All checks passed
- `uv run ruff format --check …` → 46 files already formatted
- `uv run python scripts/generate_event_types.py --check` → parity
- `npm run test:source --prefix frontend` → passed
- `npx vite build --outDir /private/tmp/nova-r03-dist` → byte-identical to committed `frontend/dist` assets (`index-C29a4zR-.js`, `index-CwqF2Lty.css`)
- Base vs head section/numeric comparison on data/lightrag.pdf (`/private/tmp/nova-r03-probe/sections.py`, `numbers.py`)
- Adversarial authored-PDF probes (`/private/tmp/nova-r03-probe/adversarial.py`, results `probe-results.txt`)
- No cloud LLM calls, no servers started.

## Corrected implementation path list
Upload:
1. `Application.upload_document` → #04 background `_ingest` → `ProcessingCache.load` (identity = content hash + `PIPELINE_VERSION` over pdf_parser/tables/embedder/chunker/models/cache/tokens/policy + processing config) → hit: publish cached typed Chunks; miss: continue.
2. `parse_pdf` → `_lines` (block ordering, two-column split, **figure-label filtering happens before table detection**) → `reconstruct_tables(lines, page_widths)`:
   per `CAPTION` line (any line start, Table|Figure) → `_column_bounds` (full width / left column / right column via gutter) → `caption_lines` (same block) → `_collect` below (stops: gap, caption, size jump, unlabelled prose) → if no ≥2-cell row, `_collect` above → `_paired_grid` | `_rectangular_grid` (alignment, numeric data, nonnumeric row label) | uncertain raw (`_clean`) → `TableRegion(anchor=min index)`. Skipped when < 2 rows or no ≥2-cell row (lines stay prose).
3. `_sections`: table lines skipped before heading detection (Finding 1 path); anchor attaches Table to current Section unless References-excluded; `flush_section` keeps table-only Sections; no headings → `_virtual_sections` (re-chunk, rebuild Table from Chunk fields, `removeprefix` raw).
4. `chunk_sections`: `add_tables` at `paragraph_index` (flushes prose) → `split_table` (≤2K whole; reconstructed by rows; raw by line then character bound; `ValueError` if caption alone ≥2K → upload error path) → reciprocal label links text↔table.
5. Embed batches → `ProcessingCache.save` → Ready.
Ask:
6. Router (guarded) → `ContextPacker.retrieve`: rank all Chunks → Lookup top-k | Synthesis/Global(fallthrough) top-k + Sub-query top-k with max score → dedupe → seeds by score → linked Chunks → Lookup-only neighbors → if Lookup or ≤6,000: greedy whole-Chunk fit, count drops; else keep all for extraction → Document order → `RetrievalEvent(dropped_chunk_count)`.
7. Citation map → `pack` (Synthesis > 6,000 → fact extraction) → answer prompt (baseline/same-metric/limitation rules) → guarded medium → low retry on length → Citation validation → Final → Trace with dropped count; BudgetExceeded / HTTP / ValueError / unexpected each emit Trace(dropped count) + Error.
UI:
8. Citation click → source fetch → `SourceContent`: text `<pre>` | reconstructed caption/meaning/thead/tbody (scroll region) | uncertain limitation note + raw. Trace shows dropped count from retrieval then final Trace.

## Outstanding integration risks
- #02 corrections land first: `_sections`/`_lines`/heading rules in pdf_parser.py overlap directly with #03's table-line skip and anchor logic; Finding 1 interacts with any heading-rule change. Rebase review required.
- #05 Summary Tree: table content is now removed from `Section.paragraphs` into `Section.tables`; Section Summaries built only from paragraphs would drop Table 1/2/4 content from Q1. #05 must summarise Table Chunks/`section.tables`. Also Global still falls into the Synthesis retrieval branch here; #05 must route Global before `retrieve`.
- `ContextPacker.retrieve` now returns `RetrievalEvent` (was `list[RetrievedChunk]`); any #06/#07/#08 caller or test written against the list must adapt.
- #10 second document (two-column, different template) exercises `_column_bounds`/caption heuristics on real geometry not yet tested; Findings 1–2 are most likely to surface there.
- Cache: any further parser module split must be added to `PIPELINE_SOURCES`.

## Next step
Implementer (GPT6.1 high) fixes Finding 1 (required) and Finding 2 (should-fix) with authored-PDF upload regressions; then rebase onto integrated #02 and request a rebase re-review.

---

# Round 2 re-review — e9deece (on f7268f9), range d56e092..e9deece

Reviewer nova-r03-hazu, claude-opus-5-5 medium. No sub-agents this round (focused fix re-review; full-scope /code-review children from round 1 still apply to the unchanged d56e092..f7268f9 portion). Snapshot `/private/tmp/nova-r03-fix` (git archive e9deece).

## Verdict: CHANGES_REQUESTED (one new major regression introduced by the R1 fix)

## Round-1 findings
| Finding | Status | Evidence |
|---|---|---|
| R1 heading below table | FIXED | `pdf_parser.py:475-484` computes heading indices with the same `_section_title` loop; `tables.py:155-156` stops `_collect` at them. Probe `heading_after_table` (GAP=14): Section "2 METHOD DETAILS" restored, Table 1 reconstructed=True with 3 rows. |
| R1 related: list/equation after table | FIXED | `tables.py:166-175`; probe `list_after_table`: list stays prose, table reconstructed. |
| R2 prose "Table N." false caption | FIXED | `tables.py:232-243` skips a match preceded in its block by same-typography lines; `caption_lines` now `j >= i`. Probe `prose_line_starts_with_table`: real caption used, paragraph stays prose. |

## New finding
### N1. [major] Mid-table group/divider row truncates a formed grid while keeping reconstructed=True
- Path: `src/chat_document/tables.py:166-175` (new grid-stop rule).
- Trigger: rectangular table whose data rows are split by a nonnumeric single-cell group row after at least one data row, e.g. rows `Base/Ours/Large` → `Proprietary models` → `GPT 13.1 24.2 36.3`, `Claude 14.5 25.6 37.7` (common grouped-model layout in ML papers; likely in #10).
- Result at e9deece: collection stops at the divider; Table Chunk is `reconstructed=True` with only the first 3 rows and no limitation marker; the divider and following data rows become a Section paragraph with one cell per line (`Proprietary models\nGPT\n13.1\n…`), losing row/column association. An answer would treat the incomplete table as reliable. f7268f9 kept all rows (as uncertain raw); base kept everything as prose.
- Reproduction: `GAP=14 V=fix <worktree>/.venv/bin/python -I /private/tmp/nova-r03-probe/adversarial.py mid_group` (compare `V=head`); recorded in `/private/tmp/nova-r03-probe/probe-results-fix.txt`.
- Note: a divider right after the header (before any data row) is fine (`group_rows` probe → whole table uncertain, all rows retained).
- Fix direction: before stopping on a nonnumeric row, look ahead — if the following rows within the gap re-form grid-compatible numeric rows (same cell count/column alignment), keep collecting (either keep the divider as a group label or mark the region uncertain with raw retained). Stop only when the nonnumeric row is not followed by more grid rows. Authored upload regression asserting every numeric cell after the divider stays in a Table Chunk, never in prose, and reconstructed=True never accompanies dropped rows.

## Minor / notes
- `pdf_parser.py:475-484` runs `_section_title` over all lines once more (O(n) extra pass) — fine.
- A bold, single-cell, non-shared-row line inside a table (e.g. bold group label) is now classified as a heading and stops the table; this matches base parser behaviour (it was already a heading at d56e092), so not a regression, but it is the same family as N1 for #10.

## Checks run on e9deece
- Adversarial probes base/head/fix: heading_after_table, prose_line_starts_with_table, list_after_table, group_rows, mid_group → `/private/tmp/nova-r03-probe/probe-results-fix.txt`.
- LightRAG: numeric-token multiset base vs fix identical (421/421, none missing/extra); Section list identical head vs fix (`sections-head.txt` / `sections-fix.txt`); table Chunks unchanged (Table 1, 2, 3, Figure 2, Table 4, Table 5).
- `uv run ruff check src tests` pass; `ruff format --check src tests` 44 files formatted.
- Full suite at e9deece (worktree HEAD e9deece, src/tests clean vs commit): `uv run pytest -q -p no:cacheprovider` → 214 passed, 2 deselected, 359.26s, exit 0 (`/private/tmp/nova-r03-probe/pytest-fix.txt`).
- New tests reviewed: `test_heading_immediately_after_table_keeps_section_and_reconstructed_cells`, `test_short_list_or_equation_after_grid_stays_in_section_prose`, `test_wrapped_table_reference_keeps_prose_and_real_caption_and_upload_succeeds[long]`, `test_distinct_caption_typography_within_body_block_keeps_prior_prose`. None covers a divider between data rows.

## Path list delta
`parse_pdf` → `_lines` → heading-index pass (`_section_title`, consumed lines) → `reconstruct_tables(heading_lines)` → per caption: same-block same-typography predecessor ⇒ skip; caption lines from match onward → `_collect` stops at heading index / gap / caption / size jump / formed-grid-broken-by-nonnumeric-row (N1) / unlabelled prose → above fallback → grid or uncertain. Remaining path list unchanged from round 1.

---

# Round 3 targeted re-review — 1d21023 (on e9deece), range d56e092..1d21023

Reviewer nova-r03-hazu, claude-opus-5-5 medium; no sub-agents. Snapshot `/private/tmp/nova-r03-n1`.

## Verdict: APPROVE (pre-rebase candidate 1d21023). A rebase review onto integrated #02 (e59e096) is still required.

- N1 FIXED: `tables.py:144-166` `_grid_follows` looks ahead from a nonnumeric row that breaks a formed grid. It keeps the row when the next rows (within the gap, not a heading, caption, size change or prose) re-form the grid. Otherwise the existing stop applies. Probe `mid_group`: all rows, including the divider and GPT/Claude, are retained as uncertain raw with the marker; nothing leaks into prose.
- R1/R2 interactions still GREEN: probes heading_after_table, prose_line_starts_with_table, list_after_table, group_rows, plus new `trailing_note` ("Higher is better" stays prose; table reconstructed) → `/private/tmp/nova-r03-probe/probe-results-n1.txt`.
- Minor (non-blocking): `mid_group_list`. When a list immediately follows a grouped (uncertain) table, the list lines are absorbed into the uncertain raw text instead of prose. The text is retained and the table was already uncertain. Acceptable; consider for #10/#11.
- New test `test_group_divider_inside_table_keeps_all_later_numeric_cells_as_uncertain_source[caption-above|caption-below]` checks the public upload: every later cell is in the Table Chunk, and the divider and later rows are absent from prose.
- LightRAG: numeric multiset base vs 1d21023 identical (421/421), Section list identical to f7268f9/e9deece, table Chunks unchanged.
- Full suite at 1d21023 (src/tests clean vs commit): `uv run pytest -q -p no:cacheprovider` → **216 passed, 2 deselected**, 243.64s, exit 0 (`/private/tmp/nova-r03-probe/pytest-n1.txt`).

Remaining: rebase onto e59e096 and run the rebase review. Focus for that review: `_sections`, `_lines` and heading rule interactions with the #03 heading-index pass and table-line skip, cache PIPELINE_SOURCES, page provenance for Table Chunks, and the integration risks from round 1 (#05 summaries over `section.tables`, Global routing, `RetrievalEvent` return type).

---

# Round 4 — post-#02 integration review: final dcbc937 (source = d7d77e8) on main e59e096

Reviewer nova-r03-hazu, claude-opus-5-5 medium; no sub-agents. Snapshots `/private/tmp/nova-r03-main` (e59e096), `/private/tmp/nova-r03-rb` (d7d77e8).

## Verdict: APPROVE (final head dcbc937, range e59e096..dcbc937)

- dcbc937 vs d7d77e8: docs only (`docs/verification/ticket-03/post-issue02/*`); src/tests/frontend/scripts/eval identical.
- `git range-diff d56e092..1d21023 e59e096..d7d77e8 -- src`: commits 2–7 are identical (`=`). Commit 1 differs only in conflict context: it now sits next to #02's `_body_continuation_target` and `_wraps_line` helpers. Merged `_sections` keeps #02's `pending: list[_Line]`, the CJK wrap join in `flush_paragraph` and the `_continues_on_next_page`/`page_first` paragraph rules, plus #03's table-line skip, anchor attachment and `current.tables`.
- application.py, cache.py, events.py, context_packer.py, answer_generator.py, models.py, tables.py and frontend are byte-identical to approved 1d21023. chunker.py = #02 CJK overlap/sentence changes + #03 `add_tables`/links (no overlap). Frontend src+dist are identical to f7268f9 (dist verified against a fresh build in round 1). Cache `PIPELINE_SOURCES` is unchanged and still covers pdf_parser/tables/embedder/chunker/models/cache/tokens/policy; #02 added no new parser module.
- LightRAG main e59e096 vs d7d77e8:
  - Numeric multiset is identical (421/421).
  - Section ids, titles and page ranges are identical.
  - Paragraph/char deltas occur only in the six table-owning Sections: 4.2, 4.3, 4.4, 4.5, 7.1 and 7.3.4.
  - #02's cross-page joins (4.5, 7.2) are preserved.
- N1/R1/R2 adversarial probes at d7d77e8 are identical to approved 1d21023 (`probe-results-rb.txt`).
- New test `test_cjk_page_continuation_and_close_table_heading_preserve_numbers_and_provenance` passes; #02's `test_lightrag_page_top_tables_do_not_enter_previous_page_body` passes with #03 tables.
- Full suite at d7d77e8 (src/tests clean): `uv run pytest -q -p no:cacheprovider` → **238 passed, 2 deselected**, 250.49s, exit 0 (`/private/tmp/nova-r03-probe/pytest-rb.txt`). ruff check pass; event parity pass at dcbc937.

Residual (non-blocking, carried forward):
- the mid_group_list minor from round 3;
- #05 must summarise `section.tables` and route Global before `retrieve`;
- #10 real two-column geometry is still untested;
- Q3 numeric quality is deferred to #11.

Approval extension: **5d6204c** (on dcbc937). The only change is to docs/verification/ticket-03/post-issue02/README.md (+11/−6, recording this approval and cleanup). src/tests/frontend/scripts/eval/pyproject/uv.lock are identical to dcbc937 (= d7d77e8). Final approved head: **5d6204c**.
