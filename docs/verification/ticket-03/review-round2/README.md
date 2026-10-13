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

## Remaining validation

Full suite, frontend typecheck/build/parity/source display and post-#02 rebase
interaction validation are pending at this checkpoint. Main owns integration;
no merge/push, self-review, subagent spawning, cloud eval or Q3 prompt tuning.
