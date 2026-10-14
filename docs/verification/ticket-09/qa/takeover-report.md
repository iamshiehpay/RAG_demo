# Issue09 independent integrated QA

**The four Issue09 acceptance criteria are supported on frozen Main `3432aa09ee7d9fcbdc9199ff9f0ee685961102e3`.** No current frontend defect was found. The prepared batch records 21 PASS and one UNPROVEN recovery limitation (T09-08). This report does not close the tracker issue or waive the limitation; Main owns final integration verification and closure. Real Q3 answer completeness remains FAIL for Issue11.

QA: nova-qa09-hero, session `01a13326-0261-7142-b38a-bd663e5dc854`. Actual recorded runtime independently verified before preparation and again at completion: gpt-6.1-sol / medium / workspace-write / on-request. [Runtime](takeover-runtime.json). No subagents, product/dependency/tracker/EXECUTION edits, commits, merges or pushes. Other agents' changes were preserved.

The [22-scenario batch](takeover-scenarios.md) was written from existing requirements before source/browser execution and reconciled against both final independent review inventories before execution. Main release #10547 supplied the exact SHA. All 345 approved product paths match before and after QA: [initial identity](takeover-source-identity.json), [final identity](takeover-final-source-identity.json). Backend tests, typed-source SSR and reviewed source/build evidence were reused only after inspecting their provenance and proving source identity; no blanket backend rerun was needed.

## Acceptance evidence

| Criterion | Verdict | Evidence and limit |
|---|---|---|
| AC1 approved draft direction | PASS | D02 v1 direct-user approval of `f15f792`; current screenshots preserve its paper/serif/margin-note direction. Historical draft approval is documentary evidence, not current browser evidence. |
| AC2 shared components used in current UI | PASS | Actual progress/readiness/overview/Citation/source/Trace plus independently controlled provisional/final/retry/error/Unverified/thinking/responsive/race states. [Scripted ledger](takeover-scripted-commands.json), [supplement ledger](takeover-supplement-commands.json), [final-format ledger](takeover-final-commands.json), [remaining states](takeover-remaining-commands.json). Controlled outputs are presentation-contract evidence only. |
| AC3 browser upload → Q3 → margin Citation + token bars; offline local fonts | PASS for UI | Real browser file selection, question entry, Ask, Trace and source controls; original FastAPI-served committed dist. [Live commands](takeover-live-browser-commands.json), [answer display](takeover-live-display.json), [actual Trace meters](takeover-live-trace.json), [Table source screenshot](takeover-live-source.png). Fresh-process local-font probe with external HTTPS blocked: [font resource record](takeover-final-fonts.json), [font screenshot](takeover-final-fresh-fonts.png). All observed resources are localhost, Noto Serif TC is loaded, body 16px, no decorative animation. Q3 semantics separately FAIL below. |
| AC4 rebuilt/committed frontend and generated event parity | PASS | All 107 committed dist files byte-identical to a fresh isolated locked-dependency build: [parity](takeover-build-parity.json), [build](takeover-isolated-build.txt), [install](takeover-isolated-install.txt). Independently reran event-generation check: backend/frontend match. Reviewed integration event/build evidence remains same-source. No repo dependencies or dist files mutated. |

## Per-scenario outcomes

Every row below applies to the exact released SHA above. New browser observations and reused deterministic evidence are distinguished in the batch.

| Scenario | Verdict | Evidence / practical limit |
|---|---|---|
| T09-01 | PASS | D02 and visually inspected current live/scripted screenshots. |
| T09-02 | PASS UI; quality FAIL | Real LightRAG upload/Q3, four inline and margin C Citations, actual Table 2 source and Trace. |
| T09-03 | PASS | Fresh process, loaded local Noto Serif TC resources, 16px body, animations=0. |
| T09-04 | PASS | Actual meters 1425/10000 and 8784/10000; measured prompt/reserve widths agree. Controlled 9990/10000 case additionally passes. |
| T09-05 | PASS | Actual embedding 0→43 in batches8, summary through27/27 including Group layer; ready only after completion; observer records UI gating. [Progress proof](takeover-progress-proof.json). SSE captures parsing/chunking; instantaneous phases are not claimed as prolonged visible paints. |
| T09-06 | PASS | Six ordinary Global turns at1280×720: overview top380.109375/bottom648.15625, readable=true, scrollY3479; composer reached. [Geometry](takeover-final-global-geometry.json), [screenshot](takeover-final-six-global-overview.png). Phone follows approved page-scroll flow, not a new sticky redesign. |
| T09-07 | PASS | Actual scan error→cached valid upload recovery; controlled summary/embed upload faults→disabled composer→new-upload recovery; failed replacement preserves old ready Document, successful replacement clears old conversation. Backend atomicity/cache variants reuse same-source265-test evidence. |
| T09-08 | UNPROVEN resume support | Controlled upload hold→browser reload reproduces loss of frontend job identity and unavailable composer; [screenshot](takeover-supplement-mid-upload-reload.png). No new endpoint, resume support, acceptance waiver or successful real interrupted-job recovery is claimed. Main must retain the known limitation and assess its existing scope. |
| T09-09 | PASS | Real Table 2: all102 rendered header/data cells equal retrieved typed source; source header p.8§4.3. Controlled spanning source shows pp.8–9. [Live proof](takeover-live-proof.json). |
| T09-10 | PASS | Section Summary source range/content/coverage browser rendering; actual Section provenance behavior reuses same-source independent QA05 evidence. |
| T09-11 | PASS UI | Literal S1 opens Group Summary pp.2–12 and both covered Sections; typed Document Summary also tested. [S screenshot](takeover-final-literal-S1.png). Long-document routing/provenance relies on inspected same-source backend evidence, not the fixture. |
| T09-12 | PASS | Uncertain Table source shows limitation and preserved raw text without fabricated cells. Actual parser flags reuse same-source #03 evidence; stochastic answer notice quality not certified by fixture. |
| T09-13 | PASS | Provisional Citation opens before final, explicit provisional label; final removes tentative state. Actual native SSE citation_map precedes deltas. |
| T09-14 | PASS rendering | Correct sentence marks across LF/CR/CRLF/mixed newline, entities, escape, emoji, quote, list, table/code/link; D01 uncited/refusal unmarked. Invalid-ID removal/count producer reuses unchanged validator evidence; no live invalid-ID output observed. |
| T09-15 | PASS | Script/unsafe-scheme Markdown is inert; structured spans preserve safe Markdown/code/table/link rendering. |
| T09-16 | PASS | Retry clears old tentative text; successful retry replaces it; double length failure leaves no truncated answer. Backend retry guards reuse unchanged tests. |
| T09-17 | PASS | Visible answer-error retry, retained rejected input, latest-turn retry guard and upload-error recovery. Router/embed/budget failure producers reuse same-source backend evidence; UI shared error branch independently exercised. |
| T09-18 | PASS | Old source success/error cannot change pending/current C2; closed dialog stays closed; restart404 clears old Document/turn/source; source404 clear accessible error, no stale source. |
| T09-19 | PASS | Actual thinking initially collapsed; controlled expansion works; no-thinking fixture produces no empty panel. |
| T09-20 | PASS | Visually inspected1440×900,1280×720,390×844; no horizontal overflow; phone margins below answer, source fits; long live Markdown table wraps within available width. |
| T09-21 | PASS bounded usability | Labels/snapshot, visible focus, keyboard Tab modal cycle, Escape/close restores Citation focus; phone source close. Not a comprehensive WCAG audit. |
| T09-22 | PASS | Exact-source committed assets, fresh107-file build parity, generated event parity, Python-served actual browser flow. |

## Actual model behavior and limits

[Native responses](takeover-live-responses.json), [transparent model frames](takeover-live-model-frames.json), [final answer](takeover-live-answer.md) and [proof](takeover-live-proof.json) preserve real requests/responses. Recorder delegates to Ollama unchanged; parser, Chunker, embedding, Summary Tree, retrieval, Gateway, SSE and sources are real. Calls:25 Section Summary,1 Group Summary,1 Document Summary,1 Router,1 Answer. All29 end `stop`; maximum estimated prompt+reserve8784/10000, provider prompt+reserve8559; estimates conservative and eval_count within reservation. Cached recovery makes no additional model calls.

Raw model content used fullwidth Citation brackets `【C9】`; the existing producer normalizes these before streaming. Raw-after-bracket-normalization equals deltas, and deltas equal final exactly. The model exercised Markdown heading/table/list, valid C Citations, U+2011 hyphens and U+202F spaces. It did not exercise invalid IDs, Unverified or CRLF; those remain labelled controlled checks.

**Q3 semantic completeness FAIL (N=1 observation).** The generated table omits the full-system rows and the answer never explicitly states Mix `-Low`64.8>full60.0 or Agriculture `-Origin`74.4>full67.6. Actual typed Table 2 source includes the relevant full-system rows. This finding was sent to Main for Issue11; no judge/N=3 score or quality PASS is inferred from the scripted samples. Fresh full model evaluation belongs to that gate.

## Harness and resource limitations

Initial35 UI assertions included three invalid QA assumptions: expecting English `Document` in the Traditional processing reason, requiring native modal focus always have a dialog DOM ancestor (Chrome alternates Close with browser-level/body focus, never another background control), and requiring the always-mounted empty overview placeholder disappear after restart. Corrected assertions all pass in the14-check supplement. Initial ledgers remain intact. A later source404 assertion incorrectly required arbitrary server-detail text; corrected two-check rerun verifies the clear accessible fixed message and focus restoration. [Correction ledger](takeover-source404-correction-commands.json).

Supplemental timeout1 came from an owned held-fetch fixture surviving between runners; clean reload fixed it. Timeout2 used requestAnimationFrame in a hidden tab; the bounded next-command assertion fixed it. The final-format run passed5 checks then native reload timed out while QA05 independently reported tab resets. Main serialized remaining browser windows; all remaining states completed without close/restart. [Resource audit](takeover-browser-resource-audit.json). Exactly ONE actual own-session close occurred for fresh fonts; duplicate archived ledgers do not represent two calls. All commands target nova-qa09; no close--all/shared Chrome kill/repair. Cross-session reset cause remains UNKNOWN, not a product defect claim. Both UI batches complete; Main11000 completed sequential browser closure per its saved proof.

Native sandbox blocked socket write, process inspection, own-server signal and Trash access. No automatic approval-review rejection occurred. Exact authorized launch/signal/Trash actions subsequently passed escalation; process inspection was not retried. [Cleanup record](takeover-cleanup.json). The initial main-workspace TypeScript attempt lacked installed Markdown dependencies; isolated `npm ci` from the committed lock and build/typecheck passed, without repo dependency changes.

Owned8290 server stopped (exit143; connection refused), all four temporary paths moved to Trash, no containers. Main11000 completed sequential exact-session browser closure, both exit0; proof `.lat/briefs/nova-qa-browser-cleanup.md` (Main attribution, no QA09 reopen). Evidence/scripts remain under owned `takeover-*`; no remaining source-sensitive execution is planned. Main must review these results and the known limitation before tracker closure.
