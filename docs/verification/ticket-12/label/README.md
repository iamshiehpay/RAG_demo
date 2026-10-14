# Ticket #12: shortcut heading removed (2026-10-14)

Human request: remove the visible 「LightRAG 論文範例問題」 text. Frontend only; answers come from the scripted `/api/ask` harness (`frontend/review/scripted-events.js`), no model, cloud or `.cache` call.

Change: `frontend/src/Shortcuts.tsx` no longer renders the heading span. The group keeps `role="group"` with `aria-label` (「LightRAG 論文範例問題」 for LightRAG documents, 「範例問題」 for others). No CSS change was needed: the row sits directly under the composer hint with the same spacing.

## Commands and results
- `npm run typecheck`, `npm run build`, `npm run test:source`, `npm run check:events`: all pass (build rebuilt `frontend/dist`).
- `pytest -q tests/integration/test_http.py tests/integration/test_event_types.py`: 6 passed.
- Server: `PYTHONPATH=src:. .venv/bin/uvicorn chat_document.api:create_app --factory --port 8121`, then
  `ONLY='shortcuts narrow checks' zsh frontend/review/followup.sh http://127.0.0.1:8121 nova-uifix-label docs/verification/ticket-12/label/run`
  -> `followup-run.txt`: 38 PASS, 0 FAIL (shortcut section incl. click-send once, aria-disabled guard, focus kept, other document gets one general question with accessible name 範例問題; 390 no page overflow; `checks.js` for 7 scenarios at 1440, 920 and 390, including the new "no visible heading, accessible name matches" assertion).
- `dom-assertions.txt`: DOM probe at 1440 and 390: role=group, aria-label set, no aria-labelledby, group text is only the five questions, `body.innerText` does not contain 範例問題, five buttons, no horizontal overflow.
- Screenshots: `after-1440.png`, `after-390.png`. Extra harness screenshots under `run/`.
- `pytest-full.txt`: the single full-suite run.
