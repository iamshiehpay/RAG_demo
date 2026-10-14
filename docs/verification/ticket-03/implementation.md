# Ticket #03 implementation and acceptance evidence

Original implementation checkpoints: `ba21a31`, `fef26f5`, `d6a075e` (original base `3a15958`); branch
`lat/03-table-reconstruction`. Rebased onto main `d56e092` (includes #04 at `4eee3d2`); review correction checkpoint `bd8f0f7`. Current acceptance is in `review-corrections/README.md`. No main merge or push. Numeric settings remain
500-token prose Chunks, 2,000-token table row groups, Lookup 5, Synthesis 3/2,
and the existing guarded LLM policies.

## Deterministic and UI acceptance

Historical pre-review `uv run pytest -q`: **179 passed, 2 eval tests deselected**, 131.36s after the generic-table fix (baseline suite: 116.03s). Final rebased acceptance: **208 passed, 2 deselected**, 184.59s; see `review-corrections/pytest.txt`.
Real local bge-m3 and recording ScriptedLLM; no cloud LLM in this suite.
The following application-operation tests ran successfully in that command:

| Criterion | Evidence | Result |
|---|---|---|
| AC1: Table 1 and Table 2 every numeric cell | `test_tables.py:31` and `:86`: all 128 cells per table with baseline/variant, dataset and metric association | PASS |
| AC2: p9 cost table has no `_` noise | `test_tables.py:86`: cost Table Chunk preserves 610, 1,000, <100, 1,399, Textract and Cextract; no `_` | PASS |
| AC3: Q3 prompt includes Table 2 and §4.3 discussion | `test_tables.py:185`: reciprocal links, real dense top-five Table 2 hit, one-primary-hit Lookup expansion, complete discussion and Semantic Graph paragraph, ordered and deduplicated prompt within budget | PASS |
| AC4: failed reconstruction retains original values and limitation | `test_tables.py:134`: authored missing cell, raw values retained, flag and answer prompt rule; browser source warning and raw display in `ui/README.md` | PASS |
| AC5: >2K table split by rows with repeated headers | `test_tables.py:162`: 230-row authored table, no headings, all rows retained exactly once, repeated caption/three headers, every Table Chunk ≤2K | PASS |
| AC6: Q3 Golden Facts including forbidden recorded | `eval/reports/table-reconstruction-q3-n3.md`; live command below | PASS (report recorded; quality FAIL) |
| Extra: retrieved budget omissions in Trace | `test_tables.py:219` and `:237`: Lookup/Synthesis retrieval and final Trace count every omitted whole Chunk; no extraction for these fitting-path tests | PASS |
| Extra: typed eval/source contract | `Chunk.kind="table"`, `table_label="Table 2"`; harness automatically uses real Table Chunk Citations | PASS |
| Extra: heading-only parents and no duplicate table prose | existing ingestion tests plus `test_tables.py:31`, `:159`; no cells lost when moved to Table Chunks | PASS |
| Extra: Q2 cost/update evidence | `test_q2_sub_queries_collectively_retrieve_cost_updates_and_community_rebuild`: Sub-query top-two union covers costs, updates and GraphRAG rebuild; Standalone top-three lacks 610 cost; answer prompt contains all | PASS |

Additional passing checks:

```sh
uv run ruff check src tests scripts/generate_event_types.py
uv run ruff format --check src tests scripts/generate_event_types.py
uv run python scripts/generate_event_types.py --check
npm run typecheck --prefix frontend
npm run build --prefix frontend
```

Browser integration: real PDF parser, real local bge-m3, source HTTP API,
committed frontend dist, scripted Citation-bearing answer. Desktop/narrow-screen
and malformed-table evidence lives in `ui/`. This is source-rendering evidence;
real answer quality is measured separately. Browser session and port 8130 server
were stopped after recording.

Live command (only the Golden Facts test file, avoiding unrelated Router smoke):

```sh
uv run pytest -m eval -s eval/test_live.py --eval-cases Q3 --eval-repeats 3 \
  --eval-record-only --eval-label table-reconstruction-q3-n3 \
  --eval-report eval/reports/table-reconstruction-q3-n3.md
```

The authorized follow-up runs Q3 N=3 and then one held-out Table 1 question in
the same Application/Gateway session. Reproducer: `uv run python -m
scripts.measure_table_reading` (move the existing output reports first; the script
refuses to overwrite them). The original session used the same runner from an
untracked `/private/tmp/t03-live-followup.py` orchestration script.

## Implementation paths after review corrections

- #04 background upload uses `Application._ingest`: parser → Chunker → Index,
  with cached complete results and swap-on-success unchanged. `pdf_parser.py:457`
  passes page widths to table recognition. Sections own tables independently
  of direct prose; heading-only Sections remain metadata.
- `tables.py:212` identifies captioned regions in their page/text column. `_rows:22`
  clusters geometric rows; `_paired_grid:33` checks paired numbers/subheaders;
  `_rectangular_grid:190` checks coordinate alignment, numeric cells and row labels.
  `_collect:144` stops at body prose and can scan above a below-table caption.
  Labelled prose cells retain uncertain case-study evidence. Caption-centred row
  labels are not clipped. Table 4 and two-column/caption-below upload regressions
  are included in the review-correction report.
- `table_text:275` repeats dataset/metric at paired cells. Comparison headers
  consistently say candidate for Table 1 and variant for Table 2. `_clean:102`
  removes math underscore separators/suffixes from raw and reconstructed cells,
  preserving identifier underscores. Unknown layouts retain source text and
  the shared LIMITATION marker; no LLM table rearrangement exists.
- `pdf_parser.py:356` removes detected table lines from prose and anchors Table
  metadata at the first source line, respecting Section/References boundaries.
  `:314` builds virtual Table metadata directly from the current Chunk fields,
  without selecting another source by a duplicated label.
- `chunker.py:91` creates typed Table Chunks and reciprocal Table N mention links.
  `tables.py:294` splits rows with repeated caption/header. Oversized uncertain
  physical lines are split by a character-preserving token bound, repeating the
  limitation on every group. Chunk and Table both default reconstruction to false.
- `context_packer.py:87`: rank primary hits → deduplicate → add reciprocal
  links → Lookup-only adjacent Chunks by seed rank → fit whole Chunks → sort
  in Document order. Added evidence keeps real cosine scores. Fitting-path
  omissions increment the request's `dropped_chunk_count`. Larger Synthesis
  evidence remains intact for the existing fact-extraction path at `:148`.
- `application.py:220` emits the typed retrieval result and propagates the count
  to success/error Trace events. Count state is local to the ask operation.
  The existing Gateway/Answer retry and Citation-validation paths remain intact.
  `events.py:44` / `:77` define both event fields; generated `events.ts` passes parity.
- `answer_generator.py:16` requires comparison baseline before conclusions,
  reference/full-row inclusion, same-metric/dataset comparisons and trend exceptions,
  paired-win-rate meaning, and disclosure of uncertain reconstruction. The
  existing guarded medium → low retry remains unchanged.
- Citation click → `App.tsx:91` source fetch → `:128` `SourceContent.tsx:4`:
  text source → preformatted prose; reconstructed table → caption/head/body;
  uncertain table → limitation note and raw text. Table scrolling is local to
  its accessible focusable region (`styles.css:55`). `Trace.tsx:10` shows
  budget omissions; `App.tsx:68` / `:77` handles retrieval/final Trace counts.

## Live measurement limitation

The Q3 report was collected from clean source at fef26f5. Table 2 citation,
Lookup classification, variant terms and comparison baseline pass 3/3. Both
numeric exceptions pass 0/3, and the forbidden claim passes 2/3. No call was
truncated. This report satisfies AC6 recording but does not certify Q3 answer
quality. The quality limitation was reported to Levi before requesting review.

Levi #4532 authorized one generic source/prompt fix and one follow-up. The clean
follow-up at d6a075e has the same rates: numeric exceptions 0/3 and forbidden
2/3, with typed citations/baseline/type/terms 3/3. No truncation/budget failure
occurred. The held-out Table 1 Legal HyDE/LightRAG answer correctly associates
Diversity 20.0%/80.0% and Empowerment 26.0%/74.0% with a real Table 1 Citation.
Reports: `table-reconstruction-q3-generic-n3.md`,
`table-reconstruction-heldout.md`. Per the ruling, remaining Q3 quality failures
are a #11 item; no further live iteration was attempted.

## Decisions and integration follow-up

Levi ruling #4395 aligned the previous per-Sub-query term co-occurrence assertion
with AGENTS' collective Sub-query coverage requirement; rationale is recorded in
`docs/ai-log.md`. No retrieval-count or Chunk-size tuning was performed.

Completed at rebase: `cache.py:15` includes `tables.py` and `embedder.py` in `PIPELINE_SOURCES`. An authored-PDF upload regression verifies typed-table cache round-tripping and a miss after changing either processing source. Both #04 background-upload behavior and #03 retrieval/drop state were retained; no numeric policy tuning or extra cloud evaluation occurred.
