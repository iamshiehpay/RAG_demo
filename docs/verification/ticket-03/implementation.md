# Ticket #03 implementation and acceptance evidence

Implementation checkpoints: `ba21a31`, `fef26f5`, `d6a075e` (base `3a15958`); branch
`lat/03-table-reconstruction`. No main merge or push. Numeric settings remain
500-token prose Chunks, 2,000-token table row groups, Lookup 5, Synthesis 3/2,
and the existing guarded LLM policies.

## Deterministic and UI acceptance

`uv run pytest -q`: **179 passed, 2 eval tests deselected**, 131.36s after the generic-table fix (baseline suite: 116.03s).
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

## Implementation paths at head

- Upload continues through `application.py:62` unchanged: parser → chunker →
  Index. `pdf_parser.py:451` invokes coordinate-table recognition; Sections own
  tables independently of direct prose, including Sections with zero Chunks.
- `tables.py:99` identifies captioned regions from text coordinates.
  `_rows:22` clusters geometric rows; `_paired_grid:33` verifies cell counts,
  positions, numeric values and repeated model headers, producing dataset ×
  metric × named comparison associations. `table_text:170` repeats dataset/metric
  at every numeric pair; `_paired_grid:33` derives the unmodified named system
  row when other labels are shortened variants. No model names or Golden Fact
  numbers are inserted by the generic rule. Regular rectangular grids also use
  row/column layout. Unknown shapes retain all detected raw text and default
  `reconstructed=False`; no LLM table rearrangement exists. Figure-captioned
  grids such as the cost table are retained and math `_` artifacts removed.
- `pdf_parser.py:350` excludes table lines from prose, inserts Table metadata at
  the caption's Section/paragraph position and respects References exclusion.
  `:314` preserves Table typing in virtual Sections.
- `chunker.py:91` creates Table Chunks at their source insertion point, adds
  model fields defined in `models.py:15` / `:47`, and links matching Table N
  mentions in both directions. `tables.py:189` splits oversized tables between
  complete rows; every group repeats caption/header. Raw fallbacks retain the
  limitation flag across splits.
- `context_packer.py:87`: rank primary hits → deduplicate → add reciprocal
  links → Lookup-only adjacent Chunks by seed rank → fit whole Chunks → sort
  in Document order. Added evidence keeps real cosine scores. Fitting-path
  omissions increment the request's `dropped_chunk_count`. Larger Synthesis
  evidence remains intact for the existing fact-extraction path at `:148`.
- `application.py:95` emits the typed retrieval result and propagates the count
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

After rebasing onto merged #04, add `tables.py` and `embedder.py` to its `PIPELINE_SOURCES` digest
(kano confirmed). Existing parser/chunker/model digest changes already invalidate
older ingestion caches. No parser settings or upload-flow edits were introduced.
