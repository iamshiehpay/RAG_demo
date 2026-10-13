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

## Final candidate checks in progress

Stable source/test candidate is d7d77e8 (on e59e096); the additional commit only
adds the authored same-PDF regression and implementation evidence. Recorded
source-invariants.json compares every shared application/cache/event/frontend
file byte for byte to pre-rebase1d21023 and all 14 #02 parser definitions (including
_Line and heading/flow/wrap helpers) by AST to integrated e59e096: all identical.
The source/test SHA-256 values and Python/dependency/PDF versions are persisted.
Final ruff, event parity, TypeScript, source-render and production build: PASS.
All rebuilt frontend/dist file SHA-256 values equal committed assets; no dist
edit required during these corrections or the rebase. Original #03 frontend
features/assets relative to Main remain part of this branch and path list.

## Remaining at source checkpoint

Full suite, final ruff/parity/typecheck/build/source-render checks, exact affected
paths and independent post-rebase review follow. No cloud LLM/prompt tuning,
frontend source changes or servers/browser resources created for these corrections.
Q3 answer quality remains #11's scope; earlier numerical/forbidden failures remain
honestly recorded in existing eval evidence, not counted as passed here.

## Final implementation verification

Tested stable source/test candidate: **d7d77e8** on integrated **e59e096**.
No source/test changes after the checks below; the final evidence commit contains
only this report and recorded logs/metadata. Exact affected paths from the whole
Issue03 branch relative to e59e096 are in `affected-paths.txt`.

| Check | Result | Artifact |
|---|---|---|
| Full deterministic suite | **PASS: 238 passed, 2 deselected, 224.84s** | full-suite.txt |
| Combined existing ingestion/table uploads | **PASS: 78 passed, 64.47s** | combined-upload-initial.txt |
| New combined CJK/page/table/heading test | **PASS: 1 passed, 0.55s** | combined-interaction.txt |
| LightRAG source Section/numeric preservation | **PASS: 421/421; no missing/extra, same Sections/pages** | numeric-preservation.json |
| Ruff lint | **PASS** | ruff-check.txt |
| Ruff format | **PASS: 46 files formatted** | ruff-format.txt |
| Backend/frontend event parity | **PASS** | event-parity.txt |
| TypeScript typecheck | **PASS** | typecheck.txt |
| SourceContent rendered table/raw limitation behavior | **PASS** | source-display.txt |
| Vite production build | **PASS** | frontend-build.txt |
| Rebuilt versus committed dist file SHA-256 parity | **PASS: all identical** | dist-parity.json |
| #02 parser definitions and prior #03 shared files preserved | **PASS** | source-invariants.json |

Commands (project root unless specified):

```sh
UV_CACHE_DIR=/private/tmp/nova-i03-uv uv run --no-sync pytest -q -p no:cacheprovider
UV_CACHE_DIR=/private/tmp/nova-i03-uv uv run --no-sync ruff check src tests scripts/generate_event_types.py scripts/measure_table_reading.py
UV_CACHE_DIR=/private/tmp/nova-i03-uv uv run --no-sync ruff format --check src tests scripts/generate_event_types.py scripts/measure_table_reading.py
UV_CACHE_DIR=/private/tmp/nova-i03-uv uv run --no-sync python scripts/generate_event_types.py --check
npm run typecheck --prefix frontend
npm run test:source --prefix frontend
# frontend working directory:
npm exec -- vite build --outDir /private/tmp/nova-i03-dist
# project root:
.venv/bin/python docs/verification/ticket-03/review-round2/compare_source.py /private/tmp/nova-i03-base-e59e096/src
```

The uv cache override avoids writes to the sandbox-excluded user cache; --no-sync
uses the project's existing locked environment. `environment.json` records Python,
package versions, source/test SHA and exact PDF SHA-256. Source/numeric comparison
uses a git archive of exact e59e096. Full suite excludes the two cloud eval tests;
**no cloud LLM calls** or additional Q3 prompt tuning were performed.

## Remaining scope and cleanup

Independent post-rebase approval is pending from nova-r03-hazu. Pre-rebase
Round 3 independently approved N1/R1/R2, but that does not substitute for final
integration approval. The grouped-table fallback can retain a close short list
inside already uncertain raw source (text preserved); independent reviewer
classified it as non-blocking. Q3 live answer quality remains owned by #11;
existing failed numeric/forbidden evaluations are preserved, not represented as
passed by deterministic upload/renderer tests. Current frontend source/display
behavior is unchanged from the prior independently reviewed #03 candidate.

No servers, browser tabs, ports, shared service changes, main/other-worktree edits,
merge, push, or delegated agents were created by this implementer. All temporary
archives/build/cache belong to `/private/tmp/nova-i03-*` and are removed once
final evidence is saved; reviewer-owned `/private/tmp/nova-r03-*` remain untouched.
