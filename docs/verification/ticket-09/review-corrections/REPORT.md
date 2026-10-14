# Issue 09 review corrections

Stable source checkpoint: `f27904854500570a3c4d6117a2eaf1ef4b336394`, branch `lat/09-tufte-design`, worktree `/Users/shiehpay/Desktop/resume/rag/.worktrees/09-tufte-design`. Delta starts at previous candidate `417fd02`; assigned integrated base remains `d56e092`. Main authorized the M1/m1/m2 correction pass; no further rebase, merge, push, spawn, requirements change, backend edit or Issue status change occurred. Source is frozen for independent re-review. This report is implementer evidence, not independent acceptance.

## Review dispositions

| Finding | Correction and evidence |
| --- | --- |
| M1: Unverified labels moved beyond a bad sentence when Markdown source differs from decoded text | `Answer.tsx` now aligns source UTF-16 offsets to decoded text offsets. It uses the same CommonMark decoding utility as the installed Markdown parser for backslash escapes and named/numeric entities, handles newline normalization, and skips stripped list indentation/blockquote prefixes. Labels split the parsed text at the mapped sentence boundary. Browser checks cover all three reviewer cases, blockquotes and numeric entities with an earlier emoji; each label immediately follows the bad sentence and precedes the next valid Citation. |
| m1: missing upload job retained an askable stale Document after restart | `App.tsx` clears Document, turns, question and source on progress HTTP 404. The error still tells the user to choose the PDF again. A previously ready Document plus a lost/reconnected upload now leaves questions disabled, old conversation/source absent and PDF selection enabled. Reupload restores ready gating. Ordinary failed uploads still retain the previous Document and conversation. |
| m2: late source success/error/finally changed a newer dialog | A monotonic request token invalidates source requests whenever the dialog closes or a newer request starts. Response data, error and loading changes apply only to the current token. Holding C1, closing it, opening held C2 and resolving C1 first leaves C2 loading; resolving C2 displays only C2. A later C1 failure cannot alter C2 or add an error. |
| m3: historical draft says approval pending | Original draft evidence is deliberately byte-identical to `f15f792`; D02 v1 records the approved direction. The parent handoff now explicitly distinguishes current corrections from historical candidate/draft records. |
| m4: frontend unit/SSR test suggestion | Withdrawn by Reviewer because the PRD excludes frontend unit tests. These regressions run through real browser controls against the production bundle; no frontend unit/SSR framework or test was introduced. |
| m5: rejected question heading/CJK provisional styling | No scope change. The adjacent browser checks again verify input restoration, rejected state and visible provisional/retry statuses. Independent QA remains responsible for final presentation acceptance. |

Code/HTML and genuinely unalignable text keep the existing adjacent-node fallback, preserving Markdown syntax. Code/table/link/entity annotations and ordinary `Unverified` links remain covered by the adjacent harness. The new explicit dependency `micromark-util-decode-string@2.0.1` was already installed transitively; the lockfile adds only its direct declaration and does not change the dependency graph.

## Red/green evidence

The complete pre-fix run served `417fd02`'s committed `index-DCWbu3pj.js` while source corrections were unbuilt. It recorded 98 commands, eight expected failing assertions and two passing assertions. The corrected `index-evYKEORE.js` run recorded 98 commands, all ten assertions passing and no console/page errors. [Before summary](before-summary.json), [before commands](before-commands.json), [after summary](after-summary.json), [after commands](after-commands.json).

The five sentence-boundary cases assert one marker, exact immediately preceding bad sentence, following valid sentence and Citation order in the same rendered paragraph. Source-race checks control both responses independently and check current title, text, error and loading. Restart checks require removal of the prior ready Document/conversation and disabled asking, followed by successful reupload. All answers and source metadata in these fixtures are explicitly scripted frontend evidence, not model quality or backend extraction evidence.

Early browser CLI runs were interrupted after native Escape; they are not counted. The complete targeted runs use the visible Close control. The separate adjacent suite successfully exercises native Escape and focus restoration. No production workaround was introduced for the interrupted automation.

Key screenshots: [corrected escaped punctuation](evidence/after-escape.png), [entity](evidence/after-entity.png), [list](evidence/after-list.png), [blockquote](evidence/after-quote.png), [numeric entity plus emoji](evidence/after-numeric-emoji.png), [late C1 error ignored](evidence/after-source-race-True.png), [restart clears stale document](evidence/after-restart.png). Corresponding `before-*` images preserve red evidence.

## Adjacent checks and static validation

- Existing full browser harness: 157 commands, 148 passing assertions, zero failed commands; [log](adjacent/browser-commands.json). Desktop 1440×900, laptop 1280×720, mobile 390×844; safe Markdown, Unicode/repeated prose spans, code/table/link marks, provisional/retry/error/rejection, Citation page ranges, Escape/focus restoration, Trace/router diagnostics, collapsed thinking and fixed 0–10K bars, failed upload retention, replacement and reconnect/restart states. Console/page errors were empty. The only harness change adds an optional output directory and closes its own browser, preserving the first candidate's evidence.
- All 79 captured events validate against the unchanged backend `EVENT_ADAPTER`: [result](adjacent/event-validation.txt), [events](adjacent/fixture-events.json).
- TypeScript typecheck, event generation parity, whitespace check, original draft/font byte parity and baseline `events.ts`/`sse.ts` byte parity pass: [commands/results](static-checks.json).
- `npm run build --prefix frontend` passed. A separate Vite build into `/private/tmp/nova-i09-corrections-dist` matches all 107 `frontend/dist/` files by path and SHA256: [inventory](dist-parity.json). The new built JS is `index-evYKEORE.js`; CSS/fonts are unchanged.
- Backend production/tests were not modified in this pass. The prior full deterministic run remains 192 passed, 2 eval deselected, documented in [the first candidate report](../REPORT.md) and [pytest log](../pytest.txt); it was not rerun as a correction-pass result. No live LLM or embedding calls were needed for these frontend changes.

Reproduction (owned port/session only):

```sh
UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8190
python3 docs/verification/ticket-09/review-corrections/browser-regressions.py after
python3 docs/verification/ticket-09/run-browser-checks.py docs/verification/ticket-09/review-corrections/adjacent
```

The session remains `gpt-6.1-sol`, high effort, workspace-write, recorded approval policy on-request, developer escalation reviewer auto_review; original rollout evidence is linked in the parent report. Sandbox escalation was needed for the browser socket and local Git metadata outside the worktree's writable root. No automatic approval rejection occurred.

## Remaining ownership and cleanup

Main must authorize the later rebase onto its integrated #02/#03/#05 contracts, regenerate types/rebuild as needed, and require independent review/QA of that final version. Real Group/Document Summary progress and Table/Section Summary source metadata remain later integrated acceptance; this correction does not invent production metadata. Reload loses the in-memory upload job ID; there is no current-job discovery endpoint on this baseline, so reload during upload remains a recorded integration limitation, outside the authorized frontend correction scope. The previously captured real Q3 table-reading errors remain backend/final-eval work, not a passing Golden Facts claim.

Owned uvicorn PID 5851 shut down cleanly; browser session `nova-i09` was closed by both complete harness runs. No Vite process or container was started. Temporary rebuild output `/private/tmp/nova-i09-corrections-dist`, npm cache `/private/tmp/nova-i09-npm-cache` and uv cache `/private/tmp/nova-i09-uv-cache` remain for reproduction. Other agents' processes and paths were not changed.

Suggested shared `docs/ai-log.md` entry for Main:

> 2026-10-13 / #09 review: Parsed-node Unverified annotation preserved Markdown syntax but a fallback appended labels after an entire decoded text node. Independent review exposed escaped punctuation, entity and indented-list examples where this labeled the later valid sentence. Real-browser red/green checks drove a raw-to-decoded offset map, placing the label immediately after the unsupported claim. The same review exposed stale source-response and restarted-upload state races; request identity and explicit missing-job cleanup fixed them. Ten targeted and 148 adjacent browser assertions passed. Prior draft evidence remains preserved; independent review and integrated QA still gate completion.
