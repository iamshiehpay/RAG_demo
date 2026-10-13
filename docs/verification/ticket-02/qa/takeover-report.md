# Independent integrated QA — Issue02

**Verdict: PASS, six acceptance criteria; no new production defect.** Exact tested main: `e59e0960af0fe5a2cd315148fb173ebcbeff7d34`. Source freeze was released to Main in HCOM after every source-sensitive check and browser/server cleanup. Later Main integrations are outside this verdict.

Agent `nova-qa02-zeme`, session `01a132e6-dea4-7aa0-8584-c09cef29c766`: actual rollout `turn_context` confirms **gpt-6.1-sol / medium / workspace-write / on-request**. Its developer permission layer uses automatic approval review for escalations. Runtime record: `/Users/shiehpay/.codex/sessions/2026/10/13/rollout-2026-10-13T09-35-53-01a132e6-dea4-7aa0-8584-c09cef29c766.jsonl`. No configuration changes or model substitutions for acceptance work. I did not implement Issue02.

Read AGENTS/CLAUDE/CONTEXT, PRD, Issue02, requirement test-list, all three shared decisions, original failed QA, PA02/R1/R2/M3 corrections, and final independent review. Historical evidence was preserved. All acceptance uses my own executions and assertions through Application upload/ask/source and the actual served frontend; historical claims supply regression targets only.

## Acceptance and requirement mapping

| AC | Independent result | Evidence |
|---|---|---|
| 1 All LightRAG main Sections and Appendix | PASS | Real original PDF uploaded: 28 Sections, 41 Chunks; Introduction through Conclusion, split-number architecture heading, Appendix present. `takeover-independent.json`, case lightrag.pdf. |
| 2 References excluded, Appendix retained/marked | PASS | Zero Chunks on bibliography pages11–12; distinctive bibliography text absent; p13+ Sections flagged Appendix. Independently generated Courier Documents also exclude BIBLIOGRAPHY markers and retain Appendix. |
| 3 Section boundaries, configured bounds and paragraph packing | PASS | Every Chunk's title, Section ID and page range agree; body tokens≤target. Courier9pt/14pt relative/bold headings and target64 preserve whole paragraphs without overlap. Mixed long paragraph targets256/500/800 give7/4/3 Chunks, all end on supported punctuation. `takeover-structure.json`, `takeover-independent.json`. |
| 4 Image-only upload error | PASS | Independently generated actual image-only PDF: error before embedding, no published Document; browser displays no-text-layer/scanned reason and disabled Question. `takeover-scan-error.png`; independent error/recovery records. |
| 5 Heading-free Document usable and askable | PASS | Own two-page PDF: six virtual Sections. Two App asks each produce validated Citation+Trace; actual browser asks and opens original virtual-Section text. `takeover-noheading-citations.png`, `takeover-noheading-source.png`. |
| 6 Citation side-note page+Section | PASS | Actual UI: original LightRAG p8 §4.3, p7–8 §4.3, and own genuine p1–2 Section1 side-notes; source opens complete original text. `takeover-lightrag-source-ui.txt`, `takeover-crosspage-ui.txt`, corresponding screenshots. |

| Existing test-list ID | Result and precise scope |
|---|---|
| PA-01 | PASS: AC1–3, real LightRAG provenance and own Section-marker Documents. |
| PA-02 | PASS: original archived 160-fact regression; complete sentence endings, all facts and source measurement phrases, overlap, relative typography, mixed punctuation/config and whole-paragraph packing. |
| PA-03 | PASS: six virtual Sections; App and real-browser ask/source. |
| UP-04 | PASS: scan, invalid-content and half-truncated original LightRAG produce distinct errors; App recovery after each; browser recovers by uploading heading-free PDF after the error sequence. |
| UP-02 / UP-06 | PASS for integrated #04 scope: browser processing disables Question with explanation; ready enables it. Restarted Application/browser re-upload uses persistent cache: zero real embedding batches, zero scripted LLM calls. Summary progress/tree is NOT_PRESENT at this SHA. |
| UP-07 | PASS deterministic repeated heading-free asks: four ScriptedLLM calls, separate finals/traces. No live answer-quality claim. |
| CT-01 | PASS for #02/#01 source labels/click-through, complete source text/ranges and unknown-source HTTP404. Structured Table rendering is NOT_PRESENT (#03). Source panel title range is DEFERRED #09 below. |

## Independent regression coverage

- Original Chinese PDF SHA256 `5e6db1bb64b839cfceb2414e86c96e5ea2ac6647d22d35adf9c0e4774e0510d8`, independently read and hashed in my approved context. Original fixture path is recorded in `takeover-independent.py` and environment JSON. **160/160** complete facts and unbroken measurement phrases; **11 Chunks**, max **498 tokens**, all eleven end at 。; all ten adjacent shared suffix/prefix overlaps are **31 tokens**. Short concluding paragraph retained. Fresh upload embeds in two batches; fresh Application disk replay restores identical Sections/Chunks under a renamed filename with no embedding or LLM calls.
- Real LightRAG R1 negatives: §4.2 conclusions remain p6 only; §4.4 unfinished prose remains p8 only, neither absorbs the next-page caption. Genuine §4.5 p9–10 and Appendix§7.2 p13–14 paragraphs retain combined provenance. Independent raw-PDF checks and public source HTTP record in `takeover-source-provenance.json`.
- Own Table7/Figure8/CJK-running-header page-leading interruptions remain separate from unfinished prose. Genuine same-column English and Chinese paragraphs span p1–2 with matching paragraph and Chunk provenance. Chinese may retain a layout newline while remaining one paragraph; this is not a lost fact or page split.
- Own labelled decimal rows (including shorter final row) and numeric-only years retain separators. New asymmetric/right-column widths and completed CJK paragraph lengths preserve exact text. These stimuli differ from the implementation fixture values.
- Browser LightRAG disk replay after stopping/restarting only my server returns ready with **28 Sections/41 Chunks**, **zero embed batches/zero LLM calls** (`takeover-cache-before.json`, `takeover-cache-after.json`, `takeover-cache-ui.txt`). Original frontend interactions reset previous conversation/source on the new Document. No browser errors recorded.

## Commands and environment

Use `UV_CACHE_DIR=/private/tmp/nova-qa02-uv-cache` with all uv commands; default uv cache access was sandbox-denied, so an owned temp cache was used without dependency changes.

- `uv run --no-sync pytest -q`: **213 passed,2 deselected**,152.20s, six existing dependency warnings (`takeover-pytest.log`). Real local bge-m3; cloud eval excluded.
- Ruff check and format of src/tests/eval/scripts and existing replay runner: PASS,65 files. Event generator `--check`: PASS. `npm --prefix frontend run typecheck`: PASS (`takeover-static.log`).
- `npx vite build --outDir /private/tmp/nova-qa02-dist --emptyOutDir` then `diff -r dist /private/tmp/nova-qa02-dist`: PASS (`takeover-dist-build.log`); production dist untouched.
- `uv run --no-sync python docs/verification/ticket-02/qa/takeover-independent.py`: PASS,24 recorded scenarios. `takeover-structure.py`: PASS, two additional independently authored typography/packing scenarios. JSON retains Documents/events for inspection.
- QA server: `uv run --no-sync uvicorn takeover-server:app --app-dir docs/verification/ticket-02/qa --host 127.0.0.1 --port 8250`. Actual `agent-browser --session nova-qa02` with open/upload/fill/click/snapshot/screenshot. Scripts supply Citation responses only; no Golden Facts/live gpt-oss quality is claimed.
- macOS26.2 arm64,Python3.12.10,PyMuPDF1.28.2,tiktoken0.14.0,numpy2.5.4,pytest9.1.1,Ruff0.17.0,FastAPI0.143.0,httpx0.28.1,Ollama0.23.3. PDF hashes and settings: `takeover-environment.json`.

## Limits and process corrections

Source panel heading still shows `Source · p.1` when side-note/metadata/text span p1–2. This is the explicitly deferred #09 title-range item; no Issue02 downgrade or fix. Table2 remains raw flattened text at this SHA; structured tables, Summary Tree/overview, summary progress, Global summary Citation acceptance and live Golden Facts were **NOT_PRESENT/NOT_EXECUTED**, never simulated as delivered.

Prior documented long-CJK-sentence overlap fallback and right-column→next-page-left-column continuation remain limits; the original 160-fact and same-column stimuli pass. They are not promoted into new fixes by this QA.

One role deviation occurred: I spawned a bounded read-only `repo-scout` path-discovery child under the repo delegation instruction. Its role configuration declared gpt-6-luna/low; actual runtime settings were unverified, so it did not meet the no-substitution requirement. Main required exclusion. **All child conclusions were excluded from acceptance**; I independently read every used App/API/cache/ScriptedLLM signature and independently hashed/verified the original PDF in the approved context. No child performed acceptance, edits or browser work; no further delegation.

Probe-only corrections: numeric-only PDF can retain its isolated heading as fallback content, so row preservation checks test the exact row sequence within source; a genuine Chinese page continuation can retain its newline, so that assertion checks paragraph/provenance and normalized complete text. No production change resulted. QA audit route initially followed the static catch-all and returned404; the evidence-only server route was reordered and cache audit rerun successfully. Superseded404 state files were removed. Native browser refs sometimes missed long-page controls; the observed exact inline Citation selector succeeded. A stalled own wait command was stopped; no other agents' processes were touched.

## Cleanup and next step

Own browser `nova-qa02` closed. Own server PIDs85185/23545 stopped; port8250 has no listener. Shared Ollama remains running0.23.3. Owned temporary cache/build directories removed; remaining generated probe PDFs moved to macOS Trash at Main request; no `/private/tmp/nova-qa02-*` resources remain. The retained independent/structure scripts create their temporary directory and regenerate these PDFs; the original historical QA fixture remains untouched outside ownership. No production/test/frontend/dependency/issue/EXECUTION edits, merge, commit or push. Pre-existing coordination changes and another reviewer's evidence preserved. Main owns checklist/status updates and evidence checkpoint; acceptance is complete.
