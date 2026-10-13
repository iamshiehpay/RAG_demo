# Issue05 independent integrated QA

**Verdict: FAIL — AC1 persistent overview is not visible while the conversation scrolls.** Source-sensitive checks are complete on `0718466a1dae475417f61f622f796ddf77429d27`; Main may release the freeze for the reviewed Issue09 correction. Issue05 requires independent revalidation of the affected UI after that integration. No production source, tests, frontend, configuration, dependencies, issue files or EXECUTION were edited; no commit/merge/push/subagents.

QA `nova-qa05-vonu`, session `01a13307-1860-7031-b456-aec65b4dfb60`: actual gpt-6.1-sol/medium/workspace-write/on-request previously verified and preserved in Main setup evidence. Model remained unchanged. Fresh initial/correction Review inventories were read before execution; requirements and path mapping are in [scenario batch](takeover-scenarios.md). Main supplied release HCOM9155. [Source identity](takeover-source-identity.json) independently verifies all 75 approved source/test/frontend/script/config hashes against the integrated workspace. Dirty files are QA-owned artifacts only, as expected for evidence creation.

## Findings requiring follow-up

1. **AC1 / UP-03, deterministic UI failure.** At 1280×720, upload the 18-Section fixture, complete six ordinary short Global questions, then scroll to the current conversation/composer. The overview is mounted but entirely outside the viewport: scrollY1433, top−1110.640625, bottom−1014.859375, intersectsViewport=false. No source panel was open in this reproduction. Thus content retention does not meet “during conversation always visible.” [Screenshot](takeover-ui-overview-scroll-failure.png), [measured geometry](takeover-ui-overview-scroll-failure.json). The earlier exact1000-token question also exposed this; the ordinary-query reproduction establishes that the problem is not limited to an extreme question or an opened source panel. Main assigned correction exclusively to romi/Issue09 with fresh review and affected independent QA; sari remains frozen.
2. **Current-source live quality remains FAIL.** Fresh real gpt-oss report: [Q1 + Chinese format](takeover-live-q1.md), [execution log](takeover-live-q1.txt). English **5/8**, Chinese **6/10**, N=1. Both routes are Global; exact three-sentence format passes. Chinese output is Simplified despite the Traditional prompt and explicitly asserts higher win rates against GraphRAG across all four datasets and all four metrics; its forbidden checker correctly fails. English experiments fails because the judge supplied a nonverbatim excerpt although the answer contains experiments. Other failed fact rows are preserved without reinterpretation. English conclusion content is present but the checker reports “Required claim not asserted”; this is not evidence that its content is absent. Chinese `chinese_summary` also fails despite Chinese text; record that checker judgment separately from the observed script mismatch. Do not turn scripted orchestration passes into semantic quality claims. Main/sari received the raw evidence; Issue11 retains quality/evaluator investigation and final all-fact N=3 gate.

## Per-acceptance verdict

| AC | Verdict | Evidence and practical limit |
|---|---|---|
| 1 Overview on ready and visible throughout chat | **FAIL** | Immediate ready overview and retained content PASS: upload/recovery/replay snapshots. Scroll-visible persistence FAIL: ordinary six-turn screenshot/geometry above. |
| 2 Q1 Global, S citation with page range and summary | **PASS** | Actual browser Section source p.2 and Group source p.1–18 with all 18 covered Sections and summary; fresh live Q1 Global and S citations. [Section source](takeover-ui-section-source.png), [Group source 1280](takeover-ui-group-source-1280.png), corresponding `.txt` snapshots. Scripted browser answer verifies UI/transport, not answer semantics. |
| 3 Target 15%, min80/max500 | **PASS** | Integrated deterministic min/proportional/max tests and independent public target/provenance probe; formal Section low/1200 budget. This verifies configured target, not that every stochastic summary hits the exact target. |
| 4 Group construction, deepest fitting level, all budgets | **PASS** | Real-bge public 18-Section boundary: short→Section, exact1000-token current question→Group1; no ask-time summary/embedding calls. Full original Chunk/Section provenance. Supplemental expensive 48-Section public upload with fixed embeddings builds 10→2 Groups; monotonic completion61/61 only after complete tree. Existing integrated recursive/heading/table/progress regressions also pass. |
| 5 Cache second upload suppresses summaries | **PASS** | Independent fresh-Application replay uses zero embedding AND zero ALL LLM calls, identical Document/tree. Actual browser reupload after fresh server start restores Group tree and overview with zero calls: before/after replay JSON; snapshot. Content/version/config and source-semantic identity regressions pass. |
| 6 Q1 and Chinese-format recorded in eval report | **PASS (reporting), quality FAIL** | Fresh report names exact0718466, real adapters, every fact/call/latency; English5/8, Chinese6/10. No all-fact pass or final N=3 claim. 49 cloud calls all `stop`, maximum estimated prompt+reserve8338/10000. |

## Executed batch and evidence

| Scenario | Judgment | Evidence |
|---|---|---|
| 01 | FAIL for scroll-visible overview; upload/progress/readiness PASS | `takeover-ui-upload-progress.txt/.png`, immediate overview/Section source/replay snapshots and explicit failure geometry |
| 02 | PASS | Browser Q1/Section source; independent empty-retrieval Global/call ledger; live report |
| 03 | PASS | Full suite target tests and `ordinary_full_source_and_target` in public JSON |
| 04 | PASS | Independent heading-only parent excluded, Table-only child included, two full-source summaries and source warning preserved |
| 05 | PASS | Integrated oversized split/title/recursive merge regressions; original Chunk IDs preserved |
| 06 | PASS | Independent 10 legal Table Chunks/820 data rows, 1245tokens each, two raw Section batches: every complete caption/header/row-bearing Chunk appears exactly once; full source IDs and headings; original defect closed |
| 07 | PASS | Real-bge Group boundary plus supplemental 48-Section 10→2 layers; complete per-level source sets and formal budgets |
| 08 | PASS for short/exact1000 boundary | Independent public and actual browser Group source for exact1000 current question; standalone rewrite in recorded public probe is494tokens, not an independent exact1000 standalone probe. Maximum-question capacity is also covered by integrated regression/source guard; no unsupported independent max-standalone claim. |
| 09 | PASS | Per-level provenance assertions, original source resolution, actual Section/Group browser page-range/covered-list display |
| 10 | PASS orchestration; real unseen-document semantics NOT_EXECUTED | Independent non-RAG fixture and integrated generic prompt/literalS Lookup/Synthesis regressions. Scripted output cannot certify real-model unseen-document factual accuracy. |
| 11 | PASS | Independent all-call replay plus browser fresh-server replay; `takeover-ui-before-replay.json`→`takeover-ui-after-replay.json` |
| 12 | PASS | Independent public pipeline version/chunk-target invalidation; full suite content/config and adapter/answer-prompt fingerprint regressions |
| 13 | PASS | Independent two Global asks plus Lookup; router/answer each time; cache hashes unchanged |
| 14 | PASS application/concurrency/progress/failure paths; injected model-failure UI NOT_EXECUTED | Independent Section/Group/Document failure+full recovery, cancellation/no partial state; suite semaphore4/2/sibling cancellation/nonreducing-provider regressions. Scan error UI proves general error/recovery separately. |
| 15 | PASS | Upload switch removes old conversation/source/overview; premature ask rejected by independent cancellation probe and full suite. Failed replacement intentionally retains previous ready Document, never publishes failed scan. |
| 16 | FAIL quality; PASS honest AC6 reporting | Exact-source live report; no checker weakening or semantic reinterpretation |
| 17 | PASS integrated regressions and scan browser recovery | Full parser/chunker suite; actual no-text-layer browser error and valid cached upload recovery |
| 18 | PASS | All labelled Table1/2/cost/link/order/drop/large-row/Chinese-source regressions plus independent long table and browser uncertain C1 raw Table source with limitation |
| 19 | PASS | Full ingest/cache/job suite plus independent failures and no-call replay |
| 20 | PASS deterministic/static/event/type; browser length-retry/invalidS NOT_EXECUTED | Full failure/event contracts, ruff/format/type/source-render checks. Retry/invalid-citation visible-state acceptance remains its owning ticket scope; no fabricated UI pass. |

Primary public operations use actual PyMuPDF, real local bge-m3, and the real guarded Gateway with a labelled scripted adapter. The recursive expensive fixture alone uses fixed embeddings and is explicitly supplemental. [Probe script](takeover-probe.py), [complete call/source ledger](takeover-public-probes.json), [results](takeover-public-probes.txt). Maximum scripted estimated prompt+reserve:9371/10000. [Failure/identity script](takeover-failure-probe.py), [failure ledger](takeover-failure-probes.json), [result](takeover-failure-probes.txt). [Fixture hashes](takeover-fixture-hashes.json); scripts recreate temporary fixtures.

Browser: original committed FastAPI-served `frontend/dist`, localhost8270, Chrome session nova-qa05, 1440×900 and1280×720. User actions were upload/fill/Ask/citation/Trace/scroll; API diagnostic calls inspected counters/source state only. Screenshots were visually inspected. The overview uses a normal page block, so being mounted or reachable by scrolling back is not a visibility PASS. No horizontal overflow observed; page errors/console artifacts empty. Network captures include successful source requests. Offscreen CLI ref clicks initially did not trigger Group source; actual scroll-to-button then click did, and the final Group screenshot/snapshot are from that successful request. No app citation defect is inferred from the automation's initial offscreen action.

## Commands and checks

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider`: **265 passed, 2 eval deselected**,253.24s. [Log](takeover-pytest.txt).
- `.venv/bin/ruff check src tests eval scripts`, `.venv/bin/ruff format --check src tests eval scripts`: exit0. Corresponding `takeover-ruff.txt`, `takeover-format.txt`.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/generate_event_types.py --check`, frontend `npm run typecheck`, `npm run test:source`: exit0; corresponding events/typecheck/source-display logs. Shell startup emitted sandbox warnings for unrelated zsh cache writes; checks themselves passed.
- `PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 .venv/bin/python docs/verification/ticket-05/qa/takeover-probe.py` and `takeover-failure-probe.py`: exit0.
- Fresh live command: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -m eval eval/test_live.py --eval-cases Q1,Q1_ZH_THREE_SENTENCES --eval-report docs/verification/ticket-05/qa/takeover-live-q1.md --eval-label qa05-integrated-0718466 --eval-record-only -s`: execution exit0/record-only; report FAIL. Record-only exit0 is not an answer-quality pass.
- Build not repeated in-place because QA cannot edit committed dist. Approved same-source production build evidence is reused, with all75integrated hashes independently verified; bundled assets served in actual browser.

## Approval and harness corrections

Original browser escalation was automatically rejected; exact command/reason preserved in [approval block](takeover-browser-approval-block.md). Main proved direct authorization and the exact-SHA/full-brief prerequisites, submitted the same direct launch, and automatic review allowed it; [.lat resolution](../../../../.lat/briefs/nova-qa05-browser-release.md). QA resumed only after reading resolution; no workaround.

Independent harness first assumed a Lookup source must be prose; actual valid table retrieval disproved that assumption. Corrected assertion accepts either original Chunk kind; [first-run evidence](takeover-harness-first-run.txt). The diagnostic route initially followed the frontend static mount and returned404; those invalid JSONs were not used as cache evidence. QA reordered only its own harness diagnostic route, restarted its owned server, and repeated fresh-server browser replay with valid counters (zero/zero). No production bug inferred or source changed.

Cleanup and final source-freeze release evidence will be appended below before completion.

## Final cleanup / freeze release

Final HEAD independently still0718466a1dae475417f61f622f796ddf77429d27; all75source hashes rechecked unchanged. Browser nova-qa05 closed; QA-owned server PID49775 terminated after verifying localhost8270 ownership. Generated QA temporary fixtures/caches removed; evidence/scripts/hashes retained. No containers/shared resources used. [Cleanup ledger](takeover-cleanup.json). Source-sensitive checks finished; Main may integrate the reviewed Issue09 fix and schedule affected revalidation. Issue05 remains FAIL/incomplete pending that UI correction; quality failures retain Issue11 ownership.
