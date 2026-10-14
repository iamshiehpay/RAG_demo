# Independent Issue03 integrated QA

Reviewer: nova-qa03-tiki. Actual runtime verified in session turn_context:
`gpt-6.1-sol`, `medium`, `workspace-write`, `on-request`, reviewer `auto_review`.
Session `01a132f2-a494-73d1-b0cb-04a7899bcd93`; no model substitution, child agents,
source edits, dependency changes, commits, merges, or pushes.

Released source baseline: **5d6204cf78e3fe166abfc7bf719c1d0cf8118189**.
Main made documentation-only checkpoint **ca8a02c747086b6aabd2d05e34a5a0b90be59708**
during QA. `git diff --name-only 5d6204c HEAD -- src tests frontend scripts eval
uv.lock pyproject.toml` was empty; current HEAD is recorded in
`takeover-source-freeze.txt`. This explains the live report's ca8a02c revision.
Its dirty-state flag records these untracked QA artifacts; no tested source was dirty.
Environment/package versions and fixed PDF hash are in `takeover-environment.json`.

Requirements read: AGENTS.md, CLAUDE.md, CONTEXT.md, PRD, Issue03, test-list,
shared .lat decisions, own task card, nova-r03-review (all four rounds), round2 and
post-issue02 integration evidence, and prior Q3/held-out eval reports.

## Acceptance criteria

| AC | Status | Independent evidence |
|---|---|---|
| 1: every Table1/Table2 cell matches fixed PDF | PASS | Viewed fixed PDF p7/p8; independent PyMuPDF word-coordinate extraction compared all 128 labelled paired cells (256 numerical values), comparison/metric/dataset association, without importing test constants. `takeover-labelled-cells.json`, `takeover-independent.py` |
| 2: p9 cost has no spurious underscores | PASS | Full integrated real-bge-m3 test verifies cost chunk, numeric strings, Textract/Cextract; 421-token comparison retains original numbers. `takeover-full-suite.txt` |
| 3: public Q3 answer prompt contains Table2 and §4.3 discussion | PASS | Independent Application upload/ask with actual bge-m3 + recording ScriptedLLM. Table2 plus Semantic Graph discussion present in actual user prompt. `takeover-q3-prompt.txt`, `takeover-q3-events.json`; integrated reciprocal-link/order/budget tests also passed |
| 4: uncertain table retains raw rows and actual browser limitation | PASS | Independently authored missing-cell and internal-divider PDFs retain all numerical rows in uncertain Table Chunks; browser upload → ask → click Citation shows raw values and bilingual limitation. `takeover-authored-probes.json`, `takeover-uncertain-browser.txt`, `takeover-uncertain.png`; prompt limitation regression passed |
| 5: >2000-token table splits by rows with repeated headings | PASS | Independent 310-row authored PDF: multiple reconstructed Table Chunks, <=2000 tokens each, same headers, all 310 rows retained. `takeover-authored-probes.json`; integrated 230-row test also passed |
| 6: Q3 Golden Facts including forbidden claim honestly reported | PASS (reporting) | Fresh real N=3 run and historical results explicitly retained below. This is **not a passing final quality gate**. `takeover-q3-live-n3.md` |

## Current and historical live quality

Fresh run uses actual `gpt-oss:120b-cloud` and `bge-m3`, Application upload/ask
and Gateway judge; full answers, per-fact evidence, per-call tokens/latency and
judge semantic probes are recorded. Command exited **1**, because Golden Facts
failed, without record-only mode or relaxed assertions.

| Fresh Q3 fact | Pass rate |
|---|---|
| Table2 Citation, Lookup router, -High/-Low/-Origin terms | 3/3 each |
| Table2 baseline | 1/3 |
| Ablation meaning | 0/3 |
| Mix -Low Overall > full | 0/3 |
| Agriculture -Origin Overall > full | 0/3 |
| No forbidden all-best assertion | 2/3 |

The forbidden failure explicitly says all ablated versions attain lower rates
than full LightRAG across all datasets. Several baseline/meaning judge failures
include nonverbatim or ellipsis-containing evidence; the checker correctly
refuses to count them. They do not establish that every corresponding answer
is semantically wrong, but they are failed checks and remain failed.
Historical `eval/reports/table-reconstruction-q3-n3.md` (fef26f5) and
`table-reconstruction-q3-generic-n3.md` (d6a075e) both report FAIL: the two numeric
exceptions and ablation meaning 0/3, forbidden pass 2/3. Historical held-out
Legal HyDE comparison was correct; it does not cancel Q3 failures.
**Final Q3 quality remains FAIL/open under #11; no waiver or scripted-live pass claim.**

## Independent adversarial and integration checks

Ten authored table examples PASS: caption above, caption below, cross-column,
continued table on a second page, heading directly after table, trailing list,
internal group-divider, wrapped body Table reference, missing-cell uncertain,
and 310-row oversized. Assertions retain every numeric value in Table Chunks;
heading/list/body reference stay appropriately available; internal divider
remains explicitly uncertain. Cross-page case has an explicit continued caption
and repeated heading, not a claim of unrestricted uncaptained table merging.

Independent CJK single-column and two-column full text/decimal preservation and
cross-page paragraph/table provenance PASS (`takeover-cjk-independent.*`).
Existing #02 measured-flow/page-top tests, #04 cache identity (including table
and embedder code changes), cache-hit/failure/background/cancellation lifecycle,
question-table reciprocal links, and retrieval-drop event/Trace counts all pass
in the full integrated deterministic suite.

Source baseline e59e096 versus released source: **421 numeric tokens = 421**,
no missing/extra tokens; Section titles and page spans equal. This is a parsed
Chunk numeric multiset preservation claim, not a count of every number in raw
PDF pages (References are excluded and text legitimately repeats elsewhere).
`takeover-numeric-preservation.json` grounds this comparison; the labelled-cell
check separately guards association errors that multisets cannot detect.

## Commands/results

All executed in repository root, except Vite build in frontend. Existing locked
Python environment used with a task-owned UV cache and `--no-sync`.

- `UV_CACHE_DIR=/private/tmp/nova-qa03-uv uv run --no-sync pytest -q -p no:cacheprovider`: **238 passed, 2 deselected**, 173.94s, exit0; `takeover-full-suite.txt` (PyMuPDF deprecation warnings only).
- `UV_CACHE_DIR=/private/tmp/nova-qa03-uv uv run --no-sync ruff check src tests scripts/generate_event_types.py scripts/measure_table_reading.py`: PASS; `takeover-lint.txt`.
- Same prefix, `ruff format --check` same paths: PASS; `takeover-format.txt`.
- Same prefix, `python scripts/generate_event_types.py --check`: PASS; `takeover-event-parity.txt`.
- `npm run typecheck --prefix frontend`: PASS; `takeover-typecheck.txt`.
- `npm run test:source --prefix frontend`: PASS; `takeover-source-display.txt`.
- `npm exec -- vite build --outDir /private/tmp/nova-qa03-dist`: PASS; `takeover-build.txt`.
- SHA256 comparison of all rebuilt vs committed dist files: identical; `takeover-dist-parity.json`.
- `.venv/bin/python /private/tmp/nova-qa03-work/independent.py`: PASS; preserved script/log/data under takeover-independent/labelled-cells/authored-probes/q3-*.
- `.venv/bin/python /private/tmp/nova-qa03-work/cjk.py`: PASS; `takeover-cjk-independent.*`.
- `git archive e59e096 src` to task-owned temp snapshot, then `.venv/bin/python docs/verification/ticket-03/review-round2/compare_source.py /private/tmp/nova-qa03-base/src`: PASS; `takeover-numeric-preservation.json`.
- Same UV prefix, `pytest -q -s -p no:cacheprovider -m eval eval/test_live.py --eval-cases Q3 --eval-repeats 3 --eval-label nova-qa03-integrated --eval-report docs/verification/ticket-03/qa/takeover-q3-live-n3.md`: **FAIL exit1**, 56.60s; `takeover-q3-live-command.txt`.

Actual browser: agent-browser 0.27.0 session `nova-qa03`, local FastAPI committed
dist on port8260, real bge-m3 + ScriptedLLM choosing actual parsed Citation IDs.
No mock network/source payload or model-generated table cells. Table2: 16 rows,
6 columns, page8 Section4.3; body width1265 <= viewport1280. Viewed both screenshots.
Browser errors/console empty. Scripted answer intentionally checks source/UI only;
its omission of an answer limitation is not a live behavior result.

One independent oversized fixture initially resized a PDF page after inserting
caption/heading, shifting them relative to later data. Corrected the task-owned
fixture to create the tall page before inserting content; then it passed. This
was a fixture defect, not a product regression. Two browser selector attempts
failed; fresh snapshots/observed refs completed the actions.

## Cleanup and next step

Browser session nova-qa03 closed. Task-owned uvicorn on port8260 stopped with
SIGINT; no ports8261–8269 or containers used. Per Main cleanup request #8095, all five task-owned temporary roots
(base/cache/dist/uv/work) were moved to the user Trash at
`/Users/shiehpay/.Trash/nova-qa03-01a132f2-a494-73d1-b0cb-04a7899bcd93`.
Reproducible authored scripts, server script/log, test logs, and numerical/event
results remain in owned takeover evidence. No shared service changes.
Evidence remains uncommitted for Main's checkpoint. Own task card only updated.
Source-sensitive checks COMPLETE; Main notified that source freeze can release.
No new parser/frontend implementation findings. Main/#11 should address fresh
Q3 quality and judge evidence shortcomings and retain a passing final Golden
Facts gate; next integrations may proceed under Main's coordination.

Cleanup completed: no `/private/tmp/nova-qa03-*` roots remain; TCP ports8260–8269
have no listeners. Browser already closed and uvicorn exited0; full-suite,
independent probes, build, and live-eval commands completed. Manifest/resource
confirmation: `takeover-cleanup-manifest.json`, `takeover-cleanup-resources.json`.
No further acceptance checks were run during cleanup.
