# Issue 09 CRLF correction

Source checkpoint: `32926292e3735f18561bfea23ec83c0278ca46d7`, correction base `71925e2b2e6dd197a582c0cdd7e271d4ea2c6ee9`, branch `lat/09-tufte-design`. Main request #7311 authorizes this frontend-only r1 correction now; #03/#05 integration rebase remains on hold. Source is frozen for kobe's independent delta re-review. This is implementer evidence, not final integrated QA or an Issue done claim.

## Change

`frontend/src/Answer.tsx` preserves CR and CRLF text verbatim when aligning Markdown source offsets to its parsed text value. Previously it converted both to LF, failed alignment and appended Unverified after the entire node, falsely placing it beside the next valid cited sentence. CR and CRLF also reset the line-prefix state, preserving mapping through list indentation and blockquote prefixes. This changes two executable lines plus one explanatory comment; code-point conversion, entity/escape decoding, node targeting, Citation rendering, safety behavior and styles are unchanged.

Rebuilt distribution: `index-DK3xdWks.js`; CSS and font files unchanged. New commit subjects follow `type: Capitalized description`. No historical commit was rewritten. No backend, tests, shared decisions, other worktrees, original draft or previous correction evidence was edited; no agents, merge, push or rebase.

## Actual-browser red/green

[Harness](browser-regressions.py) uses normal upload/ask controls and explicitly scripted SSE answers. It covers six cases: plain CRLF, lone CR, CRLF with entity/emoji, CRLF blockquote, escaped punctuation in a CRLF list, and a bad sentence midway through a CRLF list continuation. Each DOM assertion requires exactly one marker, preceding text ending at the bad claim, following text starting with the valid claim, and the valid Citation after the marker in the same paragraph.

- RED: all six assertions fail against a byte-identical snapshot of approved `71925e2`'s `frontend/dist/`, served locally on 8191. 57 commands; expected harness exit 1. The marker's preceding sibling is the valid sentence's final period in every case. [Summary](before-summary.json), [commands](before-commands.json).
- GREEN: all six assertions pass against the corrected production bundle served by FastAPI on 8190. 57 commands; exit 0; console and page errors empty. [Summary](after-summary.json), [commands](after-commands.json).
- Visual checks: [plain CRLF](evidence/after-crlf.png), [list continuation](evidence/after-middle-list.png), with corresponding `before-*` screenshots. The marker follows the bad claim before the next valid sentence/Citation.

One initial green-run assertion incorrectly required the preceding text node to equal the claim: Markdown also coalesces earlier valid punctuation into that node. The assertion now checks its ending and the following valid sentence. Both RED and GREEN were rerun with this identical finalized harness; the red snapshot came from `git archive 71925e2 frontend/dist`, so no worktree rollback was needed.

## Preserved behavior and validation

- Existing adjacent browser harness: 157 commands, 148 assertions pass; console/page errors empty. Upload/reconnect/restart, provisional/retry/error/rejection, safe Markdown, code/table/link/entity/Unicode spans, Citation/full ranges/Escape focus, Trace/fixed bars, desktop/laptop/mobile and local fonts remain covered. [Commands](adjacent/browser-commands.json); prior harness and prior evidence were not modified.
- All 79 scripted events match backend `EVENT_ADAPTER`: [validation](adjacent/event-validation.txt).
- Typecheck, event parity, whitespace check and byte parity for styles/fonts/draft/previous correction evidence/backend/tests/scripts pass: [static checks](static-checks.json).
- Production build passes: [build output](build.txt). Separate fresh build matches all 107 committed distribution files by path/SHA256: [inventory](dist-parity.json).
- Prior full backend deterministic suite result remains 192 passed/2 eval deselected, as recorded in the parent report; it was not rerun for this two-line frontend delta. No live LLM or embedding call was made. No frontend unit/SSR test was added.

Reproduce GREEN with the owned server and browser session `nova-i09`:

```sh
UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8190
python3 docs/verification/ticket-09/crlf/browser-regressions.py after
python3 docs/verification/ticket-09/run-browser-checks.py docs/verification/ticket-09/crlf/adjacent
```

For RED, archive approved `71925e2`'s `frontend/dist/` into `/private/tmp/nova-i09-crlf-before`, serve that folder with `python3 -m http.server 8191`, and invoke the harness with `before http://127.0.0.1:8191`. PDFs remain ignored and are used only to activate the scripted upload control.

## Handoff and cleanup

Await independent delta review, then Main's explicit #03/#05 integration checkpoint and mandatory integrated review/QA. Existing m5 and reload-during-upload limitations remain assigned to final QA; this pass does not change their scope.

Owned FastAPI PID 90080 and static snapshot server shut down cleanly; `nova-i09` browser closed. Ports 8190/8191/5190 are no longer listening. Temporary snapshot/rebuild paths `/private/tmp/nova-i09-crlf-before` and `/private/tmp/nova-i09-crlf-dist` remain for reproduction. No other agent's process was touched.

Suggested shared AI-log entry for Main: Independent review exposed a CRLF mismatch between raw Markdown alignment and parsed text, shifting an unsupported sentence marker onto later valid content. Preserving newline widths and treating CR/CRLF as line starts fixed six actual-browser regressions, with 148 existing browser assertions preserved. The mid-continuation fixture assertion was corrected for coalesced text nodes, and both red/green phases reran against the same assertions. Source remains gated on independent delta review and later integrated QA.
