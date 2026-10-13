# Issue09 integrated candidate for fresh review

**Subsequent Standards correction:** duma approved Spec but required a real final-renderer format smoke and an Issue09 ai-log entry. The earlier self-check1 N/A interpretation below is superseded by [actual gpt-oss smoke and documentation correction](../real-smoke/REPORT.md), run on identical frozen `cb4f1c9` product bytes. Fresh correction Reviewer is `nova-r09fix-gigi`; all prior scripted results remain historical evidence, not real-model claims.

Frontend source checkpoint: `ee383e5dacab62897bb4e4ec24963e8fdff3f7c6`, branch `lat/09-tufte-design`. Base: Main `0718466a1dae475417f61f622f796ddf77429d27`. The frozen evidence head will be supplied through HCOM; review the **full `0718466...frozen-head` diff**, not only the latest source checkpoint. Fresh Main-assigned Reviewer: `nova-r09sol-duma`. This is implementer evidence; independent review and integrated QA remain required.

Main released integration at HCOM9157, and the existing UP-03/Issue05 AC1 correction at HCOM9639/9664. QA05's final report and freeze release arrived at HCOM9802. No Main source, shared decisions, EXECUTION, ai-log, backend, merge, push or extra agent was changed/started by romi.

## Behavior and ownership

- The approved D02 Tufte direction remains: warm paper, local Noto Serif TC at16px, paragraph-aligned Citation margin notes, collapsed Trace/thinking, fixed0–10K meters, necessary interactions only. Draft and font bytes match `f15f792`.
- The #03 typed `Chunk` source endpoint drives the table renderer: reconstructed captions/meaning/headers/rows, full page provenance, and a visible uncertainty notice with unchanged raw text when reconstruction failed. The inherited `test:source` command is retained and passes.
- The #05 contract supplies ready Document overview, actual summary-stage n/N, Section/Group/Document source kinds and covered Sections, and Trace's `summary_level`/`dropped_chunk_count`. No source metadata or processing totals are invented in production. Ready overview remains persistent beside desktop chat. Long overviews scroll within a bounded, keyboard-focusable sidebar panel; at≤900px the overview uses normal page flow.
- Approved `Answer.tsx` is byte-identical to `e8b266c`: safe Markdown, decoded raw-offset mapping, Unicode/code-point spans, CR/CRLF boundaries. Current-request source loading guards and restart404 stale-state clearing remain intact.
- Changed production paths: `frontend/src/{App,Shared,SourceContent,SourceDialog,Trace,styles}.tsx/.css`, package script integration and rebuilt `frontend/dist`. `events.ts`, SourceContent table logic, backend/parser/prompts/cache/test semantics remain from0718466. Historic evidence is preserved. [Preservation check](preservation.json).

## Persistent overview RED→GREEN

QA05's independent final reproduction used six ordinary short Global queries at1280×720, then scrolled to the current conversation/composer, with no open source modal: mounted=true, scrollY1433, overview top−1110.640625/bottom−1014.859375, intersectsViewport=false. [Original geometry copy](qa05-provenance/takeover-ui-overview-scroll-failure.json), [original screenshot copy](qa05-provenance/takeover-ui-overview-scroll-failure.png), [origin paths/hashes](qa05-provenance/originals.json). Final QA05 report remains in Main's `docs/verification/ticket-05/qa/takeover-report.md`; its AC1 is incomplete until independently revalidated after reviewed09 integration.

The implementer also served Main's frozen bundle read-only on8191 and reproduced an off-screen overview after six Global turns. The old09 sticky sidebar already passed the short-overview case, but the long-overview panel was unbounded: top−2945.859375/bottom628.046875 while the composer was visible. The correction contains the panel, preserving all its text via internal scrolling.

|1280×720 scenario|Before|After|
|---|---|---|
|Main six ordinary Global turns/composer|Entire overview off-screen; independent QA05 and implementer reproduction|09 panel top380.109375/bottom648.15625, readable, contained, composer visible|
|09 long overview/composer|Panel extends above viewport by2945.86px|Panel top380.109375/bottom648.15625, readable, contained, composer visible|
|Overview internal scroll|Unbounded panel|Same contained bounds; later overview text remains reachable|
|Source closed with Escape|Short09 overview already remained visible|Panel remains visible; citation focus restoration retained|
|390×844 phone|Normal page flow|Overview readable by scrolling; composer reachable; no horizontal overflow; source usable|

[Main RED measurements](viewport-main-before-measurements.json), [09 RED measurements](viewport-before-measurements.json), [GREEN measurements](viewport-after-measurements.json), [GREEN summary](viewport-after-summary.json), [six-turn GREEN screenshot](evidence/viewport-after-six-short-Global-composer.png), [long-overview GREEN](evidence/viewport-after-long-overview-composer.png), [phone overview](evidence/viewport-after-phone-overview.png). Screenshots were visually inspected. Intentional source-modal occlusion is not scored as a persistence failure. Phone access by page scrolling is explicitly distinct from desktop viewport persistence.

## Executed checks

|Check|Result/evidence|
|---|---|
|Full current cross-ticket backend suite|**265 PASS**,2 eval deselected;280.32s. [Log](pytest.txt). Real local bge-m3 where configured; no cloud LLM quality claim.|
|Real public HTTP/UI contracts|**29 PASS /119 commands**. [Summary](public-after-summary.json), [commands](public-after-commands.json), [observed responses/progress](public-after-responses.json).|
|Viewport/phone/source contract suite|**6 measured scenarios PASS /92 commands**, plus nonzero drop-count, Document Summary typing and phone source assertions. [Summary](viewport-after-summary.json), [commands](viewport-after-commands.json).|
|Previous broad browser suite|**148 assertions PASS /157 commands**. [Commands](adjacent/browser-commands.json); desktop1440×900, laptop1280×720 and phone390×844, local fonts with external requests blocked.|
|Reviewed M1/m1/m2 regressions|**10 PASS /98 commands**: entity/escape/list/quote/emoji marker positions, stale source success/error/finally, restart404 clearing and reupload. [Summary](review-corrections/after-summary.json).|
|Reviewed CR/CRLF regressions|**6 PASS /57 commands**. [Summary](crlf/after-summary.json). Historic before/after files were not overwritten.|
|Existing typed source SSR check|PASS. [Log](source-display.txt).|
|TypeScript / generated event parity|PASS. [Typecheck](typecheck.txt), [event types](event-types.txt).|
|Runtime event schemas|79 frontend-fixture and120 observed public events validate against current backend `EVENT_ADAPTER`; zero invalid. [Record](event-validation.json).|
|Ruff check / format|PASS for src/tests/scripts/eval. [Lint](ruff.txt), [format](format.txt). New browser harnesses pass their own Ruff check, with documented exemptions for embedded JS line lengths and root-dependent fixture imports. [Harness lint](harness-ruff.txt).|
|Production build|PASS; repeated build reproduces **all107 files byte-for-byte**. [Build](build.txt), [repeat log](build-reproducible.txt), [SHA256 manifest](dist-manifest.json).|
|Git whitespace/preservation|PASS; backend/shared source, draft/fonts, approved marker renderer and historic regression evidence unchanged. [Preservation](preservation.json).|

`public-server.py` uses the existing `create_app(Application(...))` seam. Parser, Chunker, Summary Tree, Index, retrieval, source lookup, budget guard, background jobs and SSE are real; Ollama bge-m3 runs locally. Only the external LLM adapter returns labelled scripted text. The browser merely clones responses for observation and uses actual upload/fill/Ask/Trace/citation/close controls. It asserts all96 rendered Table2 cells equal the parser payload, actual short-document Section and22-Section Group sources/page ranges/covered Sections, actual n/N/readiness, uncertain Table7 raw source, fixed10K meters and Escape/focus. [Server](public-server.py), [browser runner](public-browser.py), [call types](public-llm-call-types.json). Scripted token counts, answers, summaries and thinking are not live-model measurements or Golden Facts.

The frontend-only `viewport-browser.py` and older suites inject labelled HTTP fixtures to exercise UI state/rare contracts. The viewport fixture sends Global plans, S citations, Summary source fields and drop_count3; its long/phone source additionally exercises Document Summary typing. This is presentation-contract evidence, not an actual backend Document-level routing claim.

The first real-endpoint GREEN run passed25/27 checks but expected Section sources for LightRAG, whose deliberately long scripted summaries actually selected Group. Those two failures were test-scenario assumptions, not a production defect; [archived ledger](public-adapter-assumption/public-after-summary.json). A separate one-Section document now makes that scenario explicit, while22 Sections exercise Group. The old-bundle RED ledger also includes those ambiguous Section expectations; use its table/progress/Trace/source failures for UI regression evidence, not a backend routing conclusion. [Old-bundle RED](public-before-summary.json). Preliminary harness quoting/timeouts were corrected before the completed runs; source-close controls and final real Escape/focus checks pass.

## Main AGENTS pre-review self-check

1. **Actual gpt-oss once when changing model-output format:** N/A to this integration: no model prompt, output schema, LLM request or budget/format producer changed. Real model output quality was not rerun or claimed. Historic live Q3 and QA05's current live Q1 failures remain evidence; final quality belongs to11. New assertions use explicitly scripted external responses.
2. **Prompt neutrality/generalization:** Production prompt-bearing modules are byte-identical to0718466; targeted search of router/answer_generator/summary_tree/context_packer finds no LightRAG/GraphRAG/Table2/64.8/74.4/Q1–Q3 literals. Generic authored one-/22-Section and uncertain-table PDFs exercise public sources beyond the primary paper. Literal fixture data stays in verification scripts only.
3. **Chinese continuity/numbers/question script:** Preserved Markdown renderer plus148 adjacent,10 reviewed and6 newline assertions cover Chinese, emoji, entities, lists and CR/CRLF boundaries; long overview shows Traditional Chinese paragraphs with64.8% intact. Public Chinese question/answer presentation is scripted, not a claim that gpt-oss consistently follows Traditional script. Every actual Table2 source cell matches the backend's typed numbers. QA05's real script/semantic failures remain11 scope.
4. **Document layouts:** Current265-test suite includes two-column order, figure labels, captions below tables and boxed/styled heading cases (see test_ingestion.py/test_tables.py/test_review_regressions.py). Public browser additionally opens actual LightRAG typed Table2 and an authored uncertain table. Parser unchanged; no new unsupported layout or40-page unseen-paper quality claim.
5. **Cross-ticket tests/cache version:** Full265 tests ran after rebase onto0718466, including ingestion/jobs/router/summary/table/cache/failure/event integrations. Processing/cache source and fingerprints are unchanged; no new processing module/config requires a pipeline version change. Frontend Source rendering/types do not affect cached upload products. Dist was rebuilt and byte-checked separately.

Actual current session evidence: **gpt-6.1-sol /high /workspace-write /on-request**, from the latest rollout `turn_context`; developer escalation reviewer is `auto_review`. [Sanitized runtime record](runtime.json). No startup flag is treated as proof of the actual runtime.

Owned8190/8191 servers are stopped, ports checked closed, final browser session closed, and public fixture/cache temporary directory removed. No cloud LLM or container was used. [Cleanup record](cleanup.json), [public server transport log](public-server-log.txt). The inactive private UV download cache is retained.

## Reproduction and handoff limits

From this worktree, with local Ollama bge-m3 available:

```sh
UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync python docs/verification/ticket-09/integration/public-server.py
python3 docs/verification/ticket-09/integration/public-browser.py after
python3 docs/verification/ticket-09/integration/viewport-browser.py after
python3 docs/verification/ticket-09/run-browser-checks.py docs/verification/ticket-09/integration/adjacent
python3 docs/verification/ticket-09/integration/approved-regressions.py review-corrections
python3 docs/verification/ticket-09/integration/approved-regressions.py crlf
```

Use a cold owned `/private/tmp/nova-i09-public/cache` for public summary-progress assertions; cache hits correctly omit processing stages. Browser scripts run sequentially in `nova-i09`. Main RED separately used a read-only static server of Main `frontend/dist` on8191. [Regression wrapper](approved-regressions.py) adapts output/fixture paths only and records original-script hashes.

Pending gates: duma's fresh full review; independent integrated Issue09/affected Issue05 QA on Main's final integratedSHA. Historical CJK provisional-italic readability note remains for QA (explicit provisional status exists). Reload during processing still loses the in-memory jobID; no new current-job endpoint is introduced. Real Golden Facts, model script/format reliability and final N=3 quality remain11. This report does not close those gates.

Suggested Main-owned ai-log entry: “QA05 showed overview DOM retention did not meet UP-03 viewport persistence after six ordinary Global turns. Issue09 integrated the approved Tufte sidebar and added bounded/internal overview scrolling; measured desktop RED→GREEN and phone/source regressions pass. A scripted-summary test initially assumed a Section level where the actual backend selected Group; separate short/long documents corrected the test without changing production routing. Live model quality remains a separate11 gate.”
