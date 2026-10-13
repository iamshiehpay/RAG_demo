# Issue11 Main integration verification

Released Main commit: `db64d844a58ee854f855848c90dd599e69b8a34c` (Main15369). Production source is identical to independently reviewed `f089caee00f68cc2ea77b516c095a9530cc5a580`; the later worker checkpoint50eab20 preserves documentary findings. Main-owned dirty tracker and documentary edits are preserved. Worker does not edit source, tests, settings, tracker or commit in Main.

D10A accepts only the named unit/population, neighboring-Chunk chronology and uncited-conclusion limitations, with the nonobserved Global instruction risk recorded. It does not relabel raw Golden Facts or all Citations PASS. D09 assigns final website acceptance to the user/manual checklist after these checks; this report does not certify UI QA.

## Exact Main environment and commands

Working directory: `/Users/shiehpay/Desktop/resume/rag`.

```
git rev-parse HEAD
git diff f089caee00f68cc2ea77b516c095a9530cc5a580 -- src tests frontend eval scripts pyproject.toml uv.lock
PYTHONPATH=src:. .venv/bin/python -m pytest -q
```

Recorded environment: Python3.12.10, pytest9.1.1, pytest-asyncio1.4.0, PyMuPDF1.28.2, tiktoken0.14.0, numpy2.5.4, httpx0.28.1, FastAPI0.143.0, uvicorn0.54.0, OpenCC1.4.2. Actual import `/Users/shiehpay/Desktop/resume/rag/src/chat_document/application.py`; executableMain`.venv/bin/python`. Both required dataPDFs present. Exact JSON in integration-environment.json. One deterministic suite runs on this frozen source; live/cloud eval is not rerun. Completed once: **327 passed,3eval deselected,zero skipped,6warnings,263.68seconds,exit0**. Required fixtures were present and no required tests skipped. Full console evidence: integration-full-suite.txt. No second suite or cloud N3 ran.

## Named current cache transfer and public hits

Only two current manifest payloads transferred from Issue11 worktree into Main`.cache`:833ea057185857ffe9ebc55321a245c0c2765d32f8b43ded5b2b24e00f8c6802.json (LightRAG) andeefa4dc0c41f780b997cd7024b870ac6d669b1ae61dae3820641c21fcfeac0bc.json (second). Atomic exclusive link publication; differing existing or concurrent collisions would fail without overwrite. Both new transfers succeeded; all other cache files preserved. Currentpipeline`ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f`; effective500/dense0/Lookup5/Synthesis3/Sub2/answermedium/Summaryconcurrency4 matches current manifest.

Public `Application.upload_document` in Main for each actual PDF returns exactly Ready. Native-profile external adapters fail if generation or embedding is attempted, so an unexpected miss cannot secretly call Cloud or embed. Both hits have0LLMcalls/0embeddingcalls/0guardedcalls. Observed Ready events/transfers/settings in integration-cache-hits.json; original worker caches retained until named ownership handoff. No answers or conversations transferred/cached. Native finalN3 remains the corrected report, not rerun here.

## Manual readiness and resources

The existing user-managed server at http://127.0.0.1:8101 uses PID61511, Main cwd and Main `.venv` uvicorn `chat_document.api:create_app --factory`, started2026-10-13 21:59:19Taipei after the db64 merge (Main15459/levi15454). Worker did not start, stop, restart or claim ownership of it. GET root, its built JS/CSS assets and a bundled font each returned HTTP200; command/cwd and response evidence are in integration-http-readiness.json. No8102server was started. These HTTP checks do not certify UI behavior or final manual acceptance.

D11-chat-layout-redesign.md was read. It records the approved UI direction; implementation owner/time remain pending. No redesign or source work began. D09 final user/manual QA remains pending; levi guides the user. D10 named limitations remain recorded as raw failures.

Eight historical cache payloads and nine worker context files were copied to Main ignored `.lat/retained/issue11/meme`, with manifest.json describing provenance and settings. Originals remain in the worker worktree; historical and synthetic/invalid fixtures are explicitly not current/native acceptance proof. The two current payloads remain in Main `.cache` and the worker originals remain until Main removes the worktree.

Eleven named expendable worker fixtures/caches/helpers/clean-clone paths were moved reversibly to `/Users/shiehpay/.Trash/nova-i11-meme-20261013`. Exact moved and retained paths are in integration-cleanup.json. Main-owned temporary ai-log files and reviewer evidence were preserved. Worker worktree/branch, ignored .venv/data/cache and tracked evidence remain for Main's final cleanup. Existing8101PID61511, unrelated8201PID86391 and sharedOllama were not mutated.

All suite/cache commands are complete; no worker-owned active command, child workload, browser or server remains. Main already closed Bela after saved review. No additional test, model call or source edit occurred during cleanup. Worker committed nothing in Main; Main owns final documentary checkpoint, manual acceptance recording and agent/worktree removal.

Main verified this handoff, closed both recorded agents, moved generated worker files and archived context originals to Trash, removed the clean merged worktree and safely deleted `lat/11-tuning-and-acceptance` (50eab20). The eight historical cache payloads and nine context files remain in the ignored archive; both current Main cache payloads and the existing8101 user server are preserved. The task card is archived. No worker remains needed for this delivered implementation. Final D09 manual results are still pending; Issue11 remains ready-for-human, not fully accepted.
