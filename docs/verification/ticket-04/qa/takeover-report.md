# Independent #04 acceptance supplement

Reviewer: nova-qa04-kilo. Date: 2026-10-13. Result: **PASS for all five #04 issue acceptance criteria** on integrated main d56e092138f6d5c87c75e042caf4f79e0db6989c. No production source changes, commit, merge, push, implementation dispatch, EXECUTION edits, or issue-status edits performed. Earlier QA evidence is preserved and treated as historical, not used to infer a current PASS.

## Version and environment

Main advanced during QA to cd3e30379c1ff6366414767dd8d270d891c45d13 (EXECUTION documentation only). `git diff d56e092 HEAD -- src frontend tests pyproject.toml uv.lock` was empty before release and again after cleanup. `takeover-source-sha256.json` records final baseline file hashes. Pipeline identity: `ingest-v2-14206dc69e410c1088d5905ea74ae522a00eb35fa150b509087e231873818ea5`.

Actual session rollout: gpt-6.1-sol, medium effort, workspace-write, approval_policy on-request, approvals_reviewer auto_review. Python 3.12.10, pytest 9.1.1, httpx 0.28.1, FastAPI 0.143.0, PyMuPDF 1.28.2, tiktoken 0.14.0, numpy 2.5.4, uvicorn 0.54.0, agent-browser 0.27.0, shared Ollama 0.23.3. Real local bge-m3 used for successful ingestion and retrieval. ScriptedLLM adapter used for deterministic answer/state tests; no cloud LLM acceptance claimed.

## Bounded takeover audit

`git worktree list --porcelain` plus `git -C <each> status --short` and `log -1`:

| Worktree | Exact candidate | State / pending evidence |
| --- | --- | --- |
| main | d56e092138f6d5c87c75e042caf4f79e0db6989c | EXECUTION modified by main; original ticket-04/qa untracked |
| #02 | 7d209b71c319677b6d5dbdf86f945140cf2f1f5b | Clean; matches N1 re-review request; task deliverable placeholder stale; pending independent review |
| #03 | f7268f9337a6287f21a2eed6e54dd9d919a15699 | Clean; task candidate matches; pending re-review after corrections; Q3 quality limitations retained |
| #04 | cf9c904b5a45f80d3b724d2b3cddf6450c9e5cc1 | Clean; integrated in main; task still says awaiting-review; interrupted independent acceptance pending at takeover |
| #05 | 14e783dd89d379798dcd9fc607e04aafe88d8f3d | Clean; task candidate matches; independent review pending; real eval not all passing |
| #09 | f15f79248ac367c4fec55b62dc766c2fbde78b99 | Clean; historical task says awaiting-user; D02 explicitly approves; nova-i09-romi active finalization |

HCOM inventory showed active #02 read-only reviewer mige and #09 implementation agent romi. Therefore **no-global-source-writer claim was not established** and was reported to nova. Main source was unchanged throughout this QA. `ps` was sandbox-denied; `lsof -nP -iTCP -sTCP:LISTEN` found no 8110–8189 listeners initially. Existing 8201 server, browser daemons, Ollama and other services were left untouched. Checked AGENTS.md, CLAUDE.md, CONTEXT.md, PRD, issue #04, test-list, D01–D03, task cards, review/re-review and prior acceptance/evidence. No LAT recovery activated.

## Independently chosen scenarios

Before execution, the requirement scenarios were: cold UI upload while dependency is pending; observe an intermediate completed batch; backend ask bypass while pending; ready transition; identical-byte renamed upload in a fresh Application; content and pipeline-version changes; terminal success/error; scanned and corrupt uploads; failed replacement preservation; embedding failure with no cache residue and successful retry; successful replacement clearing conversation, history and Citation source; repeated answers not cached. Summary Tree parts remain outside this integrated baseline.

Temporary harness `takeover-server.py` supplies real Recording OllamaEmbedder with a release gate/fault at the dependency seam and ScriptedLLM. It serves the unchanged committed production dist through the production FastAPI factory on 8180. QA-only diagnostics are temporary routes; the harness moves the factory's static mount after those routes. No app source or frontend is patched. Browser actions use isolated session `nova-qa04`, actual file chooser upload, question fill/click and Citation click. API diagnostics/control do not substitute for UI acceptance.

## Acceptance results

| #04 criterion | Result | Current execution evidence |
| --- | --- | --- |
| Upload immediately responds; live progress updates | PASS | Browser resource timing 37.5 ms while first Embedder call held (`takeover-upload-timing.txt`, `takeover-cold-held.json`); UI 0/41 then 8/41 (`takeover-01-embedding-0.png`, `takeover-02-embedding-8.png`); replay stages parsing/chunking/embedding/complete and batches 0,8,16,24,32,40,41 (`takeover-cold-replay.sse`) |
| Questions disabled with reason before processing completes | PASS | Actual UI processing snapshot and screenshots; reason Chinese text visible; ready textbox enabled and reason absent (`takeover-03-ready.png`); direct POST ask yields only document_not_ready (`takeover-ask-held.sse`) |
| Second same-file upload calls neither Embedder nor LLM, directly ready | PASS | Focused persisted-cache fresh-Application test; independent renamed fresh-Application ready-only event (`takeover-independent-cache.json`); UI identical-file re-upload produces identical Document, no new Embedder or LLM calls (`takeover-cold-ready.json`, `takeover-warm-ready.json`) |
| Pipeline version change reprocesses same file | PASS | Focused version/content, effective-target, legacy-cache regressions; independent A→B scenario calls real embedding and all stages, with third cache record after changed content (`takeover-independent-cache.json`) |
| HTTP progress terminates ready or error | PASS | Focused HTTP ready/error tests, replay/cancellation tests; complete cold replay ends exactly once in ready; UI scanned/corrupt/embedding faults finish with visible errors and available uploader |

## Applicable test-list rows

| Row | Result and precise scope |
| --- | --- |
| UP-01 | #04 portion PASS (immediate HTTP, parsing/chunking/embedding/complete, terminal events). Full combined row NOT_EXECUTED: summary n/N and overview require #05; baseline ready.document_summary is null. |
| UP-02 | PASS: actual browser live 0/41→8/41, disabled question/reason until ready, then enabled. |
| UP-04 | Invalid/scanned upload error and successful recovery PASS in tests and replacement UI (`takeover-04-scan-retained.png`, `takeover-05-corrupt.png`). Cold UI scan with no prior Document NOT_EXECUTED in this round. Retaining prior ready Document permits asking after failed replacement, per swap-on-success requirement; do not apply cold-empty disabled expectation to this state. |
| UP-05 | Embedding failure, no new cache, prior state retained, retry PASS (`takeover-06-embedding-error.png`, before/after-failure JSON, focused mid-batch failure tests). Summary failure UI NOT_EXECUTED (#05 absent). |
| UP-06 | #04 cache hash/version/config, dependency bypass, UI re-upload PASS. Full Summary Tree/overview equivalence NOT_EXECUTED (#05 absent). |
| UP-07 | PASS: focused test verifies repeated identical questions call LLM four times and cache bytes remain identical. |
| UP-08 | PASS for readiness rejection, Document/Index/history replacement tests, and actual UI clearing old answer/Trace/Citation/source/question upon ready (`takeover-07-replacement-processing.png`, `takeover-08-replacement-ready.png`, `takeover-replacement-ui.txt`). Overview switching NOT_EXECUTED (#05 absent). |
| UP-03 / summary rows / QA-09 | NOT_EXECUTED: not claimed as #04 acceptance; overview/Summary Tree/full real Q1–Q3 demo require later integrations/eval. |

Scanned/corrupt/embedding replacement errors visibly retain old conversation/source; retry reaches new ready with articles=0, sources=0, question empty, disabled=false and no disabled reason. Diagnostic assertions verify no added cache after injected embedding failure; history stays 1 on failure, resets to 0 after success, and Document ID changes. Browser error collection is empty (`takeover-browser-errors.txt`). Selected screenshots were visually inspected. This is behavior/path coverage, not instrumented percentage coverage.

## Commands and outcomes

- `uv run pytest -q tests/integration/test_ingestion_jobs.py tests/integration/test_http.py`: did not execute pytest; uv cache protected-path access denied. Preserved `takeover-pytest-04.txt`. Switched to existing virtualenv without changing settings or environment packages.
- `.venv/bin/python -m pytest -q tests/integration/test_ingestion_jobs.py tests/integration/test_http.py`: **23 passed, 6 warnings, 12.39 s**, `takeover-pytest-04-direct.txt`.
- `.venv/bin/python -m pytest -q`: **192 passed, 2 deselected, 6 warnings, 116.54 s**, `takeover-pytest-full.txt`. Eval deselected; no real cloud quality claim.
- `.venv/bin/python /private/tmp/nova-qa04-independent.py`: exit 0; four independently asserted cache scenarios PASS, `takeover-independent-cache.json` and copied `takeover-independent.py`.
- `.venv/bin/python /private/tmp/nova-qa04-server.py`: temporary server; real bge-m3 cold upload 41 Chunks in batches [8,8,8,8,8,1]. Copied harness retained as `takeover-server.py`.
- `agent-browser --session nova-qa04 open/snapshot/upload/fill/click/wait/screenshot/eval/errors/close`: actual browser acceptance. Initial launch denied state-directory write; normal on-request escalation accepted. One stale file-input ref was rejected; refreshed snapshot/ref and retried before corrupt-error capture. No acceptance inferred from rejected action.
- Browser UI warm re-upload counters asserted equal; SSE cold replay terminal/batch sequence asserted; failure and replacement diagnostics asserted. No source modified to accomplish these checks.

## Implementation paths exercised

- `application.py:74,84,87,95,111,121,137,221`: background task/busy state, replay, publish/reset, shutdown, public upload, cache hit/miss, parser/Chunker/batches/Index, optional cache writes, typed failures, readiness guard and uncached answers. Existing tests cover cancellation before startup, disconnect independence, active-ask exclusion, unreadable cache, bad vectors, mid-batch failure, cache-write failure.
- `cache.py:25,53,59,86`: source-derived version, hash/version/config identity, validated read/miss recovery, atomic write cleanup; fresh-Application persisted reuse and invalidation.
- `ingestion.py:19,25`: ordered journal, live/replay subscription, terminal stop.
- `api.py:49,69,78,85,89`: factory/cache anchoring/static UI, 202/409, progress 404/SSE, ask guard, Citation source. HTTP tests cover transport and readiness; no current browser restart/409 replay claim.
- `frontend/src/App.tsx`: native upload → followUpload stage/ready/error, question readiness/reason, error recovery, successful state reset, retained failed replacement, actual ask/Citation source. `Shared.tsx` UploadProgress is visibly used. Current hard-restart reconnect and 409 UI are NOT_EXECUTED in this round; earlier evidence remains historical.

## Cleanup and next step

Task-owned browser `nova-qa04` closed; task-owned 8180 server stopped by interrupting its exact exec session. `lsof -nP -iTCP:8180 -sTCP:LISTEN` returned no listener. Shared Ollama and other services unchanged. Temporary task cache removed after evidence capture; reproducible harness/script are preserved in owned QA directory. No current #04 blocker found. Main was notified when version-sensitive checks completed, allowing #02 integration. Main owns status/merge decisions and subsequent integrated regression; #05 combined rows require later execution rather than inheriting this PASS.
