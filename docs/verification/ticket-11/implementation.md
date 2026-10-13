# Issue11 implementation and evidence

Base: `7cf91851f9f86527d69c95910f9eadd58cf7b357`; branch `lat/11-tuning-and-acceptance`.
Formal D05 window: 2026-10-13 18:33:01–21:33:01 Taipei. Main release HCOM14083 superseded the original read-only hold. Runtime native session `01a132fb-ce96-78d2-8c04-4cd08fb37bd2`, turn `01a134d2-a177-74d3-a226-49a9db4dfbe5`: gpt-6.1-sol/high/workspace-write/on-request. No substitution.

## Effective controls and flow

- `settings.py`/`policy.py`: selected defaults are Chunk500, Lookup5, Synthesis3, Sub-query2, dense BM25 weight0, answer medium with unchanged3000 reservation, Summary concurrency4. `Application` and HTTP factory consume environment settings; explicit injected settings remain supported. Eval records the actual Application configuration and pipeline identity.
- `Application.upload_document`: parsing/chunking/real local embedding → summary generation → atomic ingestion cache/publication. Both newly built and cached Index objects receive BM25 weight. The cache keeps source-derived versioning; final two-document evidence uses actual current-version records, not experiment-era trees.
- `Index.query`: cosine remains the reported source similarity. Configured lexical matches use weighted reciprocal-rank fusion; `ranking_score` separately controls selection/dedup across queries. Lexically empty queries use dense RRF scale when hybrid is configured. `ContextPacker` respects the ranking score and retains source-order prompt layout, table links/neighbors and existing bounded extraction.
- `AnswerGenerator`: one copy of identical current/Standalone Question, labelled as the user-language reference; different follow-up questions retain both. Configured low/medium reaches the native Gateway; length retry remains low with the same reservation and replaces provisional output.
- `Application.ask`: HTTP status failures are distinguished from timeout/connection errors. Invalid query embeddings and fact-extraction errors receive the actual stage code. Existing failed-turn/no-history publication behavior remains.
- `eval`: optional native Judge reasons and continuous exact answer excerpts, existing numeric binding unchanged; Q1 and Chinese Q1 share the existing universal-GraphRAG forbidden criterion. Chinese answer-script result is separate measured quality. Selected cases deselect unrelated cloud workloads. Reports distinguish functional operations from raw D05 semantic rates and audit all completed calls/length attempts.
- `Trace.tsx`/generated events/committed dist: highest retrieved cosine and optional separate RRF value. Existing paper/serif/Citation-margin design and CSS retained. Extension workflow followed previously read web-design-engineer calibration/Tufte recipe; no new visual direction.
- `fetch_data.sh`: pinned PDF hashes, verified existing files, atomic verified download publication. README describes source-checkout Python/Ollama startup, committed frontend, local/cloud data flow, settings, eval and known limitations.

## Experiments and limitations

`eval/reports/issue11/retrieval-controlled.json` is the valid36-row matrix: identical frozen actual Router Q2/Q3 plans across Chunk256/500/800, k3-3-2/5-3-2/7-5-3 and BM25 weights0/.1/.25/.5. It transparently reuses unchanged original Chunks/vectors from an older ingestion version; those Summary Trees do not establish final cache readiness. Selected500/dense/5-3-2 has MRR1 and all three measured Table2/cost/update context predicates true. These narrow retrieval predicates are not answer Golden Facts.

The initial matrix changed Router plans between Chunk sizes and selected800. The first attempted control accidentally regenerated plans because an AI edit did not match its target; `retrieval-control-diagnostic.json` is explicitly INVALID CONTROL. Both results remain historical evidence. The corrected control selected500/dense. `retrieval-controlled.md`'s generic final locator sentence refers to initial retrieval.json; the authoritative controlled raw data is the controlled JSON.

`answer-low.md`/`answer-medium.md` compare actual Q2/Q3 N1 at800/dense, not the final500 setting. Low6/20 versus medium8/20 fact passes; both functional, no formal Router/Answer length. Medium retained provisionally; this tiny exploratory comparison is not a robustness claim. Final N3 separately measures500.

`concurrency.json`: eight short guarded native calls per1/2/4/8; all completed with stop and measured maximum in-flight1/2/4/8. Wall128.84/44.73/23.26/8.20s. Some probe activity overlapped this worker's own ingestion activity; timings are uncontrolled and cannot establish relative production throughput or a universal service ceiling. Default4 retained conservatively.

## Deterministic and presentation evidence

- `full-suite-final.txt`:325PASS,3eval deselected,258.19s. One full suite before independent Review; initial325-test run had320PASS/5FAIL, retained in `full-suite.txt`.
- `corrected-targeted.txt`:18PASS. Actual initial failures exposed assumptions in scripted adapter settings, Chinese-only fixture language, duplicated-question label and the fixture's evidence budget. Corrections preserve their intended assertions; no real fact results were regraded.
- `targeted.txt`, `ruff.txt`, `typecheck.txt`, `build.txt`, `event-parity.txt`: meaningful public upload/ask tests, static checks and committed bundle/event parity.
- `trace-extension.txt`/`.png`: owned presentation-only browser, scripted external LLM and real bge-m3/public text PDF; highest cosine0.4431 matches the single retrieved Chunk. Screenshot inspected. Build `index-BwNgBchD.js`/`index-DRyMGEGM.css`. Automation clicks did not submit; observed DOM composer.requestSubmit used. No claim of independent UI QA or actual provider accounting. Own sessionnova-i11 and8320PID11380 closed; Main independently verified no listener.

## Pre-review self-checks

1. Native model format: low/medium experiments and final native Judge responses exercise changed consumer behavior. Scripted display fixtures remain explicitly separate.
2. Prompt fitting: no test-document names, expected Golden Fact numbers or regression labels added to production instructions. Held-out native question evidence is recorded separately before freeze.
3. Chinese: full suite retains sentence/line/number regressions; real Chinese N3 preserves script-following misses as quality defects. OpenCC checks opposing forms and CJK presence; shared forms remain inconclusive.
4. Layout: existing real LightRAG and109-page second-document processing plus deterministic two-column/caption/figure/bordered-heading regressions. No parser changes in Issue11. Preexisting mixed-font numeral/heading misassociation is still a limitation.
5. Shared paths: branch fast-forwarded before work; all325 tests pass including other tickets. Current source-derived cache identity covers changed ingestion modules; final two caches/hits are independently recorded by the driver. Main tracker/test-list/QA-owned evidence untouched.

## Final delivery

Final N3 reports and cache manifest: `eval/reports/issue11/final-lightrag.*`, `final-second.*`, `cache-manifest.json`, `conclusions.md`. All27actual answers completed, operationalPASS/rawqualityFAIL.170LightRAG+107second calls, maxestimated9617/9847 and reported9392/9580; zeroformalRouter/Answerlength. Two summarylengths discarded/retried and one Judge length retained as failedfact. Secondnumeric targetCitation2/3 includes validC9pointingwrongTable10; Main notified, no semanticCitationPASS. Raw numeric0/3 despite manuallymatchingTable9; global1/3. Currentcaches/hits preserved for Main. Clean-clone smoke and exact frozen candidate/reviewer identity follow. Semantic/forbidden failures are reportable under D05/D06; 10K, grounded source IDs, fixed refusal and functional failure remain hard constraints. No self-review or independent-QA certification is claimed here. Main owns integration and Zoru owns final P01–P18 execution.

Held-out native smoke: `heldout-native.json` and `heldout-probe.py` use a fresh calibration Document and four questions absent from Golden Facts. English and traditional-Chinese counts/duration correct withC1, absentmanufacturerfixedrefusal; simplifiedquestionstillcontains traditionalforms (knownscriptdefect).10nativecalls,maxestimated3868/reported3643,allstop. An initial AI fixture used single-line text_pdf and clipped the duration off-page; `heldout-clipped-fixture.json` is INVALIDcomplete-sourceproof. Corrected one-page textbox asserts fit and reuses the samePDFbytes forpubliccache reupload. No productionpromptchange or qualityloop.
