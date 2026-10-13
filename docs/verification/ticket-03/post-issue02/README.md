# Issue03 verification after integrated Issue02

Owner: nova-i03-polo, gpt-6.1-sol/high. Independent reviewer: nova-r03-hazu.
Main authorized rebase onto e59e0960af0fe5a2cd315148fb173ebcbeff7d34.
Pre-rebase #03: 1d210237fbcb3ea0b75234c27933e39d69ce55b4, independently APPROVE
for N1/R1/R2 (full review in main .lat/briefs/nova-r03-review.md, Round 3).
Rebased source checkpoint: 2bb424acd21e2e5eac0b86dbf067e1d946dc3cc5.
This report is implementation/verification evidence, not independent approval.

## Rebase resolution and preserved behavior

The first of nine replayed commits conflicted in pdf_parser.py and docs/ai-log.md.
The parser conflict was #02's body-continuation/wrapping helpers versus #03's
`_sections(..., tables)` signature. The resolution preserves all #02 helpers and
uses the table-aware signature; `_Line` pending paragraphs, measured flow, CJK
normalization, caption/label/numeric guards and page provenance remain unchanged.
Both AI-log append blocks remain. The remaining eight commits replayed cleanly.
No requirements/acceptance changes, commits omitted, merge/push, or main edits.

`git diff --stat 1d21023 2bb424a -- src/chat_document/application.py
src/chat_document/cache.py src/chat_document/events.py frontend`: **empty**.
The prior #03 cache fingerprint entries tables.py/embedder.py remain; #04 upload
lifecycle and #03 retrieval-drop counts/typed source display are byte-identical.
`git diff e59e096 2bb424a -- src/chat_document/pdf_parser.py`: only #03 imports,
typed table virtual Sections, table-aware Section anchors/skip and heading-index
handoff. No #02 body/flow/line/heading rule was replaced. #02 chunker sentence-bound,
CJK overlap and numeric separator corrections are retained with table insertion.

## Combined public-upload checks

- `UV_CACHE_DIR=/private/tmp/nova-i03-uv uv run --no-sync pytest
  tests/integration/test_ingestion.py tests/integration/test_tables.py -q`:
  **78 passed**, 64.47s (`combined-upload-initial.txt`). Covers all #02 numeric/CJK/
  measured-flow/page-provenance cases and all 25 #03 table cases without editing
  existing #02 tests or weakening assertions.
- New same-PDF integration test:
  `test_cjk_page_continuation_and_close_table_heading_preserve_numbers_and_provenance`.
  Real parser/chunker/background ingestion/local bge-m3, ScriptedLLM adapter (no
  cloud quality claim). A CJK source number split across two pages becomes 14 and
  retains paragraph/Chunk provenance p.1–2; nearby numeric table stays reconstructed
  at p.2 in Section 1; same-size bold numbered heading below it keeps Section 2.
  Integrated candidate: **1 passed, 25 deselected**, 0.55s (`combined-interaction.txt`).
  Exact pre-rebase 1d21023 source + current authored test/fixture: target CJK source
  assertion fails (`combined-interaction-pre-rebase-red.txt`). No setup failure.
- Source comparison versus exact integrated main e59e096 archived under own
  `/private/tmp/nova-i03-base-e59e096`: LightRAG **421/421** numerical tokens,
  no missing/extra, identical Section titles/page ranges (`numeric-preservation.json`).
  Existing Table 1/2 every labelled cell, Table 4/statistics, raw fallback, row
  splitting, lookup linking/order, drops, synthesis coverage tests remain intact.

## Remaining at source checkpoint

Full suite, final ruff/parity/typecheck/build/source-render checks, exact affected
paths and independent post-rebase review follow. No cloud LLM/prompt tuning,
frontend source changes or servers/browser resources created for these corrections.
Q3 answer quality remains #11's scope; earlier numerical/forbidden failures remain
honestly recorded in existing eval evidence, not counted as passed here.
