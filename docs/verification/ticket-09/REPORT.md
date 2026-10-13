# Issue 09 candidate handoff

Current correction candidate: `32926292e3735f18561bfea23ec83c0278ca46d7`. See [CRLF correction](crlf/REPORT.md) for the delta against approved `71925e2`, and [earlier review corrections](review-corrections/REPORT.md) for M1/m1/m2 evidence. The remainder of this report records the first candidate and its checks. Historical `frontend/review/DESIGN.md` pending-approval wording is preserved as draft evidence; D02 v1 is the current approved direction.

This is implementation evidence for Main nova to assign independent review and QA. It is not an Issue done claim, independent review, independent QA, or integration approval.

Source checkpoint: `7e71bd22e06a6e5f82af5742e39a12fc387f6a18`, branch `lat/09-tufte-design`, worktree `/Users/shiehpay/Desktop/resume/rag/.worktrees/09-tufte-design`. Rebase baseline: `d56e092138f6d5c87c75e042caf4f79e0db6989c`. The rebased design checkpoint is `c4728a1`; original draft `f15f792` remains available in Git, and its `frontend/review/` evidence and font sources remain byte-for-byte unchanged.

D02 v1 records the user's approval to finalize the existing direction. Main's assignment takes precedence over the historical draft's pending-approval text. This is an Extension of the approved design: warm paper, Noto Serif TC 16px, paragraph-aligned margin Citation, collapsed Trace/thinking, explicit fixed 0–10K token bars, no decorative animation. No requirement, decision, event contract, backend source, main checkout, or other worktree was modified.

## Candidate behavior

- Main's background upload POST acceptance and subsequent progress subscription are preserved. Progress takes priority over an older ready Document; questions stay disabled while processing. Failed uploads retain the previous Document/turns. Successful ready replaces Document and clears conversation/input/source. Lost progress offers reconnect; a missing job after restart permits selecting the PDF again.
- Retry clears provisional text/thinking and replaces the latest failed turn. Rejected input is restored for editing, with no Retry button or provisional styling. Failed answers are cleared and use the shared error state.
- Safe Markdown retains raw-HTML suppression and the default safe URL transform. Citations use only the supplied map and retain full page ranges in margin notes, accessible labels, source dialog, and retrieved Chunk disclosures.
- Unverified uses backend structured spans, converting Python code-point offsets to Markdown UTF-16 positions. Annotation happens on parsed nodes, so code, links, table cells, and escaped text remain intact. Identical verified prose is not flagged by text matching. Labels have spacing on both sides; ordinary uses of the word/link “Unverified” are not reclassified as backend marks.
- Routing Trace retains plan source, fallback reason, rewrite language mismatch/router rewrite, discarded extraction lines, actual counts, think, latency, done reason, and backend invalid Citation count. Every call uses the same 10,000-token scale; thinking is collapsed and empty thinking disclosures are omitted.

## Paths and state ownership

| Path | Responsibility |
| --- | --- |
| `frontend/src/App.tsx` | Upload/ask/reconnect state and composition of approved components; source loading/error lifecycle |
| `frontend/src/Answer.tsx` | Safe Markdown, Citation buttons/margin notes, structured Unverified annotation |
| `frontend/src/Shared.tsx` | Page range, upload progress, stages, error/Retry, Unverified, thinking, fixed 10K bar |
| `frontend/src/Trace.tsx` | Routing diagnostics, LLM metrics, collapsed thinking, retrieved Chunks |
| `frontend/src/SourceDialog.tsx` | Native modal, full page ranges, focus restoration, retained optional table/Section Summary seam |
| `frontend/src/styles.css`, `frontend/src/fonts/` | Approved design and local fonts |
| `frontend/dist/` | Rebuilt production assets, including `index-DCWbu3pj.js` and `index-DqdgCMNN.css` |
| `docs/verification/ticket-09/` | New implementer harness, logs, screenshots and this report |

`frontend/src/events.ts` and `frontend/src/sse.ts` are unchanged from the assigned main baseline. Backend models remain the event source of truth.

## Checks

Environment: actual Codex session model `gpt-6.1-sol`, effort `high`, workspace-write sandbox, recorded approval policy `on-request`, escalation reviewer `auto_review`. Session rollout: `~/.codex/sessions/2026/10/13/rollout-2026-10-13T08-57-27-01a132c3-adb9-7940-b006-2a5686d9ca2b.jsonl`. Node `v23.11.0`, npm `11.5.2`, Vite `6.4.4`, uv `0.7.2`, Python `3.12.10`, pytest `9.1.1`, agent-browser `0.27.0`/Chromium.

Commands were run from the worktree root. `UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache` avoids writes to the restricted shared uv cache. The old local environment initially lacked the declared `opencc` dependency; `uv sync --locked` installed it without changing the lockfile.

| Check | Result and evidence |
| --- | --- |
| `npm run typecheck --prefix frontend` | PASS after final source change |
| `npm run build --prefix frontend` | PASS; [build.txt](build.txt) |
| Rebuild then `git diff --exit-code -- frontend/dist` | PASS, no difference from committed distribution |
| `UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync python scripts/generate_event_types.py --check` | PASS, generated event parity |
| `UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync pytest` | PASS: 192 tests, 2 eval deselected, 6 existing dependency warnings, 116.15s; [pytest.txt](pytest.txt). Backend is unchanged by the later Markdown fix. |
| `uv run --no-sync ruff check src tests scripts/generate_event_types.py` with the same cache variable | PASS |
| `uv run --no-sync ruff format --check src tests scripts/generate_event_types.py` with the same cache variable | PASS, 43 files |
| `git diff --check` | PASS |
| Saved browser harness on final production dist | PASS: 156 commands, 148 PASS assertions; [browser-commands.json](browser-commands.json). All command exit codes zero; console/errors empty. |
| Scripted event model validation | PASS: all 79 captured events validated with backend `EVENT_ADAPTER`; [fixture-events.json](fixture-events.json), [event-validation.txt](event-validation.txt) |
| Real LightRAG upload → Q3 → margin Citation → source → Trace | UI PASS; actual upload 202, progress/ask/source 200. [live-checks.json](live-checks.json), [live-q3.txt](live-q3.txt), [live-source-title.txt](live-source-title.txt). This run preceded the last Markdown annotation fix and had no Unverified spans. |

The browser harness exercised desktop 1440×900, laptop 1280×720 and small 390×844, external HTTPS blocked while localhost served local fonts, no page overflow, Citation layout and source full range, Escape/focus return, measured bar ratios at 1,800/10K and 9,990/10K, provisional/retry/error/rejected, Unicode/repeated-prose spans, Markdown code/table/link/entity marks, no-thinking, failed upload retention, replacement upload, reconnect, and restart recovery. These are implementation checks, not independent QA.

The harness initially measured a closed Trace. The CLI also did not activate a partially/offscreen summary reliably. The final harness waits for the correct new turn and brings the Trace control into the viewport before clicking/measuring. Original draft harness/evidence were preserved. Fixtures explicitly identify themselves as scripted review content and are never imported by production.

## Evidence and reproduction

Start the rebuilt backend on the assigned port:

```sh
UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8190
python3 docs/verification/ticket-09/run-browser-checks.py
```

The saved harness uses browser session `nova-i09`. Close that session and stop the owned server after reproduction. For real UI validation, reload without fixture injection, select `data/lightrag.pdf`, ask Q3, open a Citation, then Trace.

Key screenshots:

- [03-q3-trace-10k.png](evidence/03-q3-trace-10k.png): approved layout, routing diagnostics and fixed bars.
- [04-source-range.png](evidence/04-source-range.png): scripted pp.8–9 source dialog.
- [05-q3-1280.png](evidence/05-q3-1280.png), [05-q3-390.png](evidence/05-q3-390.png): laptop and mobile.
- `06-provisional/retry/error/rejected/unverified/markdown/no-thinking.png`: explicit state evidence under `evidence/`.
- [12-markdown-spans-focused.png](evidence/12-markdown-spans-focused.png): final code/table/link/entity annotations.
- `02-background-upload.png`, `07-replacing-document.png`, `08-reconnect-progress.png`, `09-restart-recovery.png`: latest upload states.
- [10-live-q3.png](evidence/10-live-q3.png), [11-live-source.png](evidence/11-live-source.png): actual backend/model run.

## Remaining integration and independent checks

Main was `03e6f361b1b6ecf283a55ffd9f57304d5a28762b` at final inventory, newer than the assigned baseline. Other trees: #02 `26600be`, #03 `f7268f9`, #05 `14e783d`; the #04 tree had already been removed by Main. Only this assigned branch was rebased/committed. No merge, push, other-agent spawn, or Issue status update was performed.

Main must integrate/rebase onto its chosen updated main, including later #03/#05 contracts, regenerate events if those owners change models, rebuild, and require re-review. This baseline exposes parsing/chunking/embedding/complete upload stages and Chunk sources; actual summary progress, Summary source metadata, and structured Table Chunk metadata are not supplied yet. Existing shared presentation seams are retained; production data was not fabricated to fill them. Null Document Summary is explicitly described as unavailable.

The real Q3 answer contains existing table interpretation errors, including an incorrect Agriculture `-Origin` comparison and incorrectly assigned table values. It is UI evidence only and does not establish Golden Facts quality. The exact answer is retained in `live-q3.txt`; #03/#11 must address and evaluate that behavior on integration.

Main must assign the distinct Reviewer (Opus 5.5 medium) and QA (GPT 6.1 medium). `/implement` requests review, but spawning duplicate reviewer/QA agents was explicitly disallowed for this worker.

## Cleanup and AI-log entry for Main

Owned uvicorn PID `64988` shut down cleanly; browser `nova-i09` closed. No listener remains on 8190 or 5190. No Vite process/container was started. Ignored local dependencies/cache remain; temporary paths are `/private/tmp/nova-i09-uv-cache`, `/private/tmp/nova-i09-pytest.log`, `/private/tmp/nova-i09-final-build.log`, `/private/tmp/nova-i09-rebuild.log`.

Suggested shared `docs/ai-log.md` entry (Main owns that file):

> 2026-10-13 / #09: The approved Tufte draft was rebased onto integrated #04/#06/#07 behavior. An initial Unverified implementation inserted labels into raw Markdown; checking code/table/link/entity cases exposed that labels could become code content or disturb Markdown syntax. Parsed-node annotation using backend Unicode spans corrected this. Browser implementation checks passed for emoji offsets, repeated verified/unverified prose, code/table/link/entity labels, and ordinary “Unverified” text. The browser CLI needed explicit viewport positioning before Trace/Citation clicks; the saved harness was corrected without weakening the geometric assertions. Real Q3 still showed existing backend table-reading errors, preserved as evidence and referred to the pending table/final eval integrations.
