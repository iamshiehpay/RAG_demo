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

Production changes are confined to `pdf_parser.py`; `chunker.py`, Application,
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
