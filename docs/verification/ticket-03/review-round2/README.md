# Issue03 second independent-review corrections

Owner: nova-i03-polo (gpt-6.1-sol, high). Reviewer: nova-r03-hazu, separate/read-only.
Starting branch: lat/03-table-reconstruction at f7268f9337a6287f21a2eed6e54dd9d919a15699,
base d56e092138f6d5c87c75e042caf4f79e0db6989c.
Full review read: main `.lat/briefs/nova-r03-review.md` (both findings and integration risks).
This is implementation evidence, not independent approval.

## Corrections and authored public-upload regressions

- R1: parser computes heading-line indices with the same `_section_title` used
  during Section construction, including consumed split/wrapped lines, then
  supplies them to tables. No table→parser dependency, new module, cache omission,
  or copied heading rules. Close numbered heading retains its Section and source
  table stays reconstructed. Formed numeric grids stop at unrelated nonnumeric
  lines that break grid structure; malformed/misaligned numeric cells stay in raw
  uncertain evidence. Lists and equations remain Section prose.
- R2: wrapped references with preceding same-style block lines do not open a
  caption. Distinct caption typography can still start a legitimate caption
  within a block; only the matched line and subsequent caption lines are consumed.
  Prior prose stays prose, caption-below keeps correct attribution. A paragraph
  over 2K tokens above a damaged table now reaches Ready and retains raw cells.

All authored regressions use Application.upload_document with real local bge-m3,
ScriptedLLM (recording guarded fake cloud dependency), real parser/chunker/ingestion.
No external model decision/quality guarantee is claimed by these integration tests.
No frontend source changes; existing source renderer checks still required.

## RED→GREEN

Commands below use `UV_CACHE_DIR=/private/tmp/nova-i03-uv uv run --no-sync` because
normal `uv run` cannot open the sandbox-excluded default uv cache. That setup error
was replaced before RED evidence collection; it is not counted as reproduction.

| Behavior | RED version/result | GREEN result | Evidence |
|---|---|---|---|
| Close numbered heading below table | f7268f9 + authored test: table_reconstructed false | PASS | r1-heading-red.txt / r1-heading-green.txt |
| Close short list/equation | R1 heading correction only: both tables uncertain | PASS, both source lines stay prose | r1-list-equation-red.txt / r1-green.txt |
| Wrapped prose Table reference | R1 correction, before caption fix: wrong caption | PASS | r2-red.txt / r2-green.txt |
| >2K wrapped paragraph + damaged row | same pre-caption-fix source: Error rather than Ready | PASS, retains uncertain raw values | r2-red.txt / r2-green.txt |

Each selected command: `pytest tests/integration/test_tables.py -q -k <heading_immediately|short_list_or_equation|wrapped_table_reference>`.
Targeted combined R1 `-k 'heading_immediately or short_list_or_equation or uncertain_table or equal_cell_counts'`: 5 passed.
All Table tests: `pytest tests/integration/test_tables.py -q`: 23 passed, 33.54s.
Ruff check/format and event parity: PASS (separate log files).
`compare_source.py /private/tmp/nova-r03-base/src`: baseline d56e092 vs corrected
working source, 421 numerical tokens on both sides, no missing/extra, identical
Section titles/page ranges (`numeric-preservation.json`). Existing labelled Table
1/2 every-cell assertions and Table 4/statistics remain passing in table-suite.txt.

## Additional checkpoint verification

All six new regressions were rerun unchanged against an isolated `git archive
f7268f9` source/test snapshot: **6 failed, 17 deselected**, 7.55s. Failures are
the actual target behaviors, including Error rather than Ready for the large
stolen paragraph (`exact-f7268f9-red.txt`), not environment/import failures.
TypeScript check and source static rendering: PASS. Vite production build to
`/private/tmp/nova-i03-dist`: PASS; all rebuilt file SHA-256 hashes equal committed
`frontend/dist` (`dist-parity.json`). No frontend files needed changes.

## Remaining validation

Full suite, frontend typecheck/build/parity/source display and post-#02 rebase
interaction validation are pending at this checkpoint. Main owns integration;
no merge/push, self-review, subagent spawning, cloud eval or Q3 prompt tuning.

## Independent round-2 result and N1 correction

Independent reviewer nova-r03-hazu reported CHANGES_REQUESTED at e9deece.
R1 heading/list/equation and R2 wrapped-caption/large upload findings were fixed;
N1 found an internal nonnumeric group label after data rows prematurely ended the
grid, leaving later numeric cells in prose and reporting reconstructed=True.
Main full report: `.lat/briefs/nova-r03-review.md`, Round 2 section.

Authored caption-above AND caption-below public uploads reproduce N1 on an
isolated exact e9deece git archive: **2 failed, 23 deselected**, 2.30s
(`group-divider-red.txt`). Failures assert the wrongly reconstructed truncated
table, not setup/import failures. `_grid_follows` now checks contiguous future
rows against the already formed numeric grid, preserving gap/heading/caption/
font/body-prose boundaries. A resumed grid retains the divider and every later
numeric cell as uncertain raw Table evidence, with no numeric rows leaking to
prose. It handles upward caption-below collection in the same way. No table
numbers or model/system identities are hard-coded in production rules.

Own full suite on e9deece: **214 passed, 2 deselected**, 345.26s
(`full-suite-before-rebase.txt`). Independent reviewer separately ran 214 passed,
2 deselected, 359.26s; that does not approve N1. This source checkpoint adds the
N1 fix and two regressions; updated targeted/table-suite evidence follows.
Final integration still waits for Main's #02 signal and subsequent full-scope
independent rebase review. No merge/push or cloud prompt changes.

N1 corrected targeted command (`-k 'group_divider or heading_immediately or
short_list_or_equation or wrapped_table_reference or distinct_caption or
uncertain_table or equal_cell_counts'`): **10 passed, 15 deselected**, 11.42s
(`group-divider-green.txt`). Full updated table file: **25 passed**, 51.51s
(`table-suite-group-fix.txt`). Ruff check/format: PASS. Updated baseline numerical/
Section comparison: 421/421, no missing/extra, same Sections
(`numeric-preservation-group-fix.json`, corrected working source before checkpoint).
