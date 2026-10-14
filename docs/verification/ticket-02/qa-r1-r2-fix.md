# Ticket #02 — R1/R2 correction (nova-i02-vera)

Requested by Main nova in HCOM #5685 after independent re-review by
nova-r02-mige (Opus 5.5 medium). Starting branch `lat/02-structure-aware-chunking`,
head `7d209b71c319677b6d5dbdf86f945140cf2f1f5b`; review base
`d56e092138f6d5c87c75e042caf4f79e0db6989c`. Earlier review/QA evidence is unchanged.

## Public-upload RED → GREEN evidence

All regressions exercise `Application.upload_document` with real PyMuPDF, real
local bge-m3 and ScriptedLLM. No internal parser mock or live cloud LLM is used.

- R1: `pytest -q tests/integration/test_ingestion.py -k page_top` initially gave
  **4 failed**. Generated Table/Figure captions and a CJK running header were
  joined into the page-1 body; real LightRAG §4.2 swallowed Table 1. The final
  tests also check §4.4/Table 3, exact page-6/page-8 body provenance, retained
  caption/header content, and genuine §4.5 p.9–10 / Appendix §7.2 p.13–14 joins.
  After the fix, `-k 'page_top or page_break'`: **8 passed**.
- R2: `-k labelled_cjk` initially gave **2 failed**: labelled decimal rows and
  equal-width list items lost their newlines. Requiring a shorter final line
  fixed those cases. Adding a shorter-final-value row reproduced **1 failed,
  2 passed**, so consecutive CJK label/numeric-cell rows are also excluded from
  normalization. Exact source paragraph and Chunk text are asserted.
- Combined focused checks: **16 passed** before the shorter-final-value case.
  Initial complete ingestion suite: **49 passed**, 17.34 s, five existing PyMuPDF
  deprecation warnings. Existing 160-sentence coverage, bounded Chunks,
  numeric-only rows, Latin spacing and short CJK sentence overlaps are retained.
- Original QA replay revealed a nearly full-width final prose line: raggedness
  alone retained genuine layout newlines. A new public-upload regression failed
  first; page/column-width evidence plus a completed final sentence now also
  permits normalization. The focused prose/labelled-row/number-wrap subset then
  passed **5 tests**. The 160-sentence test now also requires every measurement
  phrase (`區域N中達到V個單位`) in the source text without removing newlines.
  Punctuation-adjacent layout separators are retained. The original replay checks this
  stronger source condition too; its runner is [replay_r1_r2.py](replay_r1_r2.py).

R1/R2 production changes are confined to `pdf_parser.py`; `chunker.py`, Application,
cache, event and frontend sources are unchanged. The source-derived processing
identity invalidates previous parser records automatically.

Final rebase, complete checks, original QA fixture/cache replay, environment,
candidate hashes and independent reviewer verdict are recorded below after
completion. These are implementer checks, not independent QA.

## Limits

Continuation recognition remains conservative: an ambiguous short unfinished
CJK page-leading line can stay separate when there is insufficient flow evidence.
The pre-existing two-column cross-page left-edge limitation and large-sentence
overlap fallback remain. Figure/frame edge cases deferred to #10 are unchanged.
No new cloud LLM/Golden Facts evaluation or browser QA is claimed.

## Rebased candidate and environment

- Rebased onto current main `03e6f361b1b6ecf283a55ffd9f57304d5a28762b`, without
  conflicts. Final source checkpoint: `26600be7077f84e57ea5e4c9d0a292bb36434307`;
  R1/R2 commit before the final-line correction: `acfea43f06e640842137265e4ee453af5de5b233`.
  Independent re-review covers the complete original `d56e092..candidate` range,
  including prior F1/N1 corrections; Main receives the final documentation head.
- Implementer session: `nova-i02-vera`, rollout
  `01a132c6-9bf7-79b0-ace1-16c674326736`, actual `gpt-6.1-sol`, effort `high`.
  Session `turn_context` reports `workspace-write`, network enabled and
  `approval_policy=on-request`; the active instruction layer specifies
  `auto_review` for escalations. This discrepancy was reported to Main.
- macOS 26.2 arm64; Python 3.12.10; uv 0.7.2; PyMuPDF 1.28.2; tiktoken 0.14.0;
  numpy 2.5.4; pytest 9.1.1; Ruff 0.17.0; FastAPI 0.143.0; httpx 0.28.1.
- Commands use `UV_CACHE_DIR=/private/tmp/nova-i02-uv-cache uv run --no-sync`
  with the existing locked environment. Default uv cache access was denied by
  the workspace sandbox; no dependencies or shared services were changed.
- Original QA PDF SHA-256:
  `5e6db1bb64b839cfceb2414e86c96e5ea2ac6647d22d35adf9c0e4774e0510d8`.
  LightRAG PDF SHA-256:
  `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`.
- `uv run --no-sync python docs/verification/ticket-02/replay_r1_r2.py <original-qa-chinese.pdf>`:
  PASS on final source. Fresh/replay embedding calls **2/0**, replay events only
  `ready`, identical Sections/Chunks, renamed Document preserved, **11 Chunks**,
  maximum **498 tokens**, **11/11** sentence endings, **160/160** numeric facts
  and unbroken source measurement phrases, concluding paragraph retained,
  **0 LLM calls**. [Replay record](qa-r1-r2-cache-replay.json). Both Applications
  were closed and the temporary processing cache removed.
- Ruff check and format: PASS, **65 files** including the persisted replay
  runner. Backend/frontend event parity and `git diff --check`: PASS.

## Final verification

- `UV_CACHE_DIR=/private/tmp/nova-i02-uv-cache uv run --no-sync pytest -q`:
  **210 passed, 2 deselected**, 119.37 s, six existing dependency deprecation
  warnings. This includes all **50 ingestion tests** on the final source
  checkpoint above. Source and tests remained unchanged throughout this run.
- `uv run --no-sync ruff check src tests eval scripts docs/verification/ticket-02/replay_r1_r2.py`:
  PASS. Corresponding `ruff format --check`: PASS, **65 files**.
- `uv run --no-sync python scripts/generate_event_types.py --check`: PASS.
- `git diff --check`: PASS. A source-path comparison against the previous
  reviewed `7d209b7` confirms only `pdf_parser.py` changed for R1/R2; shared
  Application/cache/events/frontend production sources are untouched.
- No backend/browser process, ports, containers or shared-service mutations.
  The temporary replay script and task-local uv cache are removed before
  handoff; the reproducible runner and result are retained in this directory.

Earlier full-suite and ingestion runs while the supplemental regression was
being developed are superseded. Independent review is requested from
`nova-r02-mige`; Main owns the subsequent independent integrated QA and merge.
