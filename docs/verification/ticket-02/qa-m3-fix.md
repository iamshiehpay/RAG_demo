# Ticket #02 — M3 measured text-flow correction

Main nova requested M3 in HCOM #6616 after nova-r02-mige's Re-review 2.
Previous candidate: `582d07e7f50e993cac8131e8b21946068b541d06`.
Main/source base remains `03e6f361b1b6ecf283a55ffd9f57304d5a28762b`.
The original full review base remains `d56e092138f6d5c87c75e042caf4f79e0db6989c`.
Earlier R1/R2 reports and replay evidence are preserved unchanged.

## RED → GREEN through public upload

- `UV_CACHE_DIR=/private/tmp/nova-i02-uv-cache uv run --no-sync pytest -q tests/integration/test_ingestion.py -k actual_column_or_text_width`:
  **2 failed** before production edits. Asymmetric margins (textbox x=50–480)
  retained three layout newlines in completed CJK prose. On the two-column
  fixture (left x=50–296, right x=316–562), the left column normalized correctly
  while the right retained newlines. The tests compare exact Section paragraphs,
  paragraph page provenance and resulting Chunk text.
- The symmetric-margin calculation is removed. `_measured_flow_width` uses
  actual aligned same-style text, excluding captions/shared rows/numeric-only
  lines and keeping within the measured block band. Completed prose with a
  nearly full final line can now establish flow in either column and with
  asymmetric margins. The page-leading continuation reference also considers
  the measured preceding page's body flow; it is separate from the same-page
  wrap reference, preserving the short running-header negative.
- The focused M3/R1/R2/160-fact/short-overlap subset passed **20 tests** before
  adding the second two-column length. The final ingestion suite passed
  **53 tests**, 27.62 s, five existing PyMuPDF warnings. It includes exact
  96- and 120-character prose in both columns and 172-character asymmetric
  single-column prose. No existing assertion or fixture was weakened.

Only `pdf_parser.py`, ingestion fixtures/tests and #02 evidence/AI log changed.
`chunker.py`, Application/cache/events/frontend sources are unchanged for M3.
The replay runner accepts an optional output path to preserve previous evidence.

## Original QA fixture/cache replay

Command (with the same environment prefix above):

```text
uv run --no-sync python docs/verification/ticket-02/replay_r1_r2.py <original-qa-chinese.pdf> docs/verification/ticket-02/qa-m3-cache-replay.json
```

PASS: **11 Chunks**, maximum **498 tokens**, **11/11** sentence endings,
**160/160** numeric facts and unbroken source measurement phrases, short
concluding paragraph retained. Fresh/replay embedding calls **2/0**, fresh
Application disk replay emits only `ready`, restores identical Sections/Chunks
and updates the filename; **0 LLM calls**. Both Applications closed and the
temporary processing cache removed. [Recorded result](qa-m3-cache-replay.json).
The source-derived processing identity automatically includes the parser fix.

Implementer/environment versions and fixture hashes match the previous
[R1/R2 report](qa-r1-r2-fix.md). No ports, browser/server processes, containers
or shared-service changes. No cloud LLM or independent QA is claimed.
The pre-existing long-sentence overlap and cross-column page-continuation
limitations remain as independently recorded; they are not expanded here.

## Stable checkpoint

Source and regression checkpoint:
`2ee613b2a537d55d9ae3bda7edf414787c33779c`, on
`lat/02-structure-aware-chunking`. It follows the previously reviewed
`582d07e7f50e993cac8131e8b21946068b541d06`; base remains `03e6f361` as
Main confirmed. The M3 delta is limited to the measured parser flow reference,
public-upload regressions and owned evidence. No rebase is needed.

Ruff check/format: PASS (**65 files**, including replay runner); backend/frontend
event parity and `git diff --check`: PASS. The documented replay command with
the optional M3 output path was also rerun and passed on this checkpoint.
Source/tests are unchanged during the complete final suite run; its result and
independent re-review handoff are appended after it finishes.

## Final verification and re-review handoff

- `UV_CACHE_DIR=/private/tmp/nova-i02-uv-cache uv run --no-sync pytest -q`:
  **213 passed, 2 deselected**, 258.96 s, six existing dependency warnings.
  This includes all **53 ingestion tests**; source and tests stayed at
  `2ee613b2a537d55d9ae3bda7edf414787c33779c` throughout the run.
- Ruff check/format, backend/frontend event parity and `git diff --check` all
  passed on this source checkpoint. Production-path comparison against the
  previous `582d07e` confirms M3 changes only `pdf_parser.py`.
- Independent reviewer `nova-r02-mige` (same Opus 5.5 medium session, no child
  contexts this round) confirmed M3 fixed with no new findings in HCOM #6931
  and Re-review 3 of Main's `.lat/briefs/nova-r02-review.md`. Its archived-source
  probes cover right-column lengths 95/96/97/119/120 and asymmetric margins;
  labelled rows retain separators. LightRAG parse is byte-identical to
  `582d07e`, retaining R1 closure and genuine §4.5/§7.2 joins. Its ingestion
  suite passed **53 tests** (39.34 s); static checks also passed.
- Final reviewer approval is pending inspection of this committed evidence
  and the final documentation head supplied by HCOM; it is not claimed yet.
  Main owns integrated independent QA and merge. No self-review, merge or push.
- Applications/processing caches were closed and removed. The task-local uv
  cache is removed before handoff. No servers, browsers, ports, containers or
  shared-service changes were introduced.
