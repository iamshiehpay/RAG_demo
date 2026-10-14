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
- The prior `pytest-full.txt` had only an invocation header and was interrupted; preserved verbatim as `pytest-full-interrupted.txt`. It is not a passing result. A fresh complete run is recorded separately in `pytest-full.txt`.

## D19 continuation provenance

The stopped Claude implementation produced commit `119a352c8adf164f02dea41a4783e52edc0d3cf2`, including source, dist, browser assertions and browser evidence above. Codex `nova-label-kune` took exclusive ownership after Main release (message 18002); source was already correct and was preserved without rewriting. The existing successful browser evidence is reused because the source and rebuilt dist are identical. The `overflow: true` DOM field is the successful no-page-overflow predicate used by that probe, not an overflow finding.

Fresh Codex checks: typecheck and test:source passed. The `npm run check:events` wrapper hit filesystem denial reading the external uv cache; running the same script directly with `../.venv/bin/python ../scripts/generate_event_types.py --check` passed. `npm run build` passed and produced no diff to dist. No LLM smoke is required for this static presentation change; scripted browser answers are not answer-quality evidence. Existing synthetic IME evidence in `../review.md` and `../followup/review/completion.md` remains applicable because Composer and its handlers are unchanged; physical IME and screen-reader testing were not performed.

Resource inventory: no app/server/browser process launched by this continuation; reserved ports 8121–8129 unused. New ordinary temporary paths: none. Old unknown scratch paths were preserved. Fresh reviewer sessions and their native paths are recorded in `reviewer-runtime.md`; no reviewer children were launched. Main owns integration/tracker and 8101; #13 backend and D18 remain outside this delta.

Fresh ordinary suite completed: `PYTHONPATH=src:. .venv/bin/pytest -q`, exit 0, **327 passed, 3 eval deselected, zero skipped**, 6 warnings, 279.91s. Raw output: `pytest-full.txt`. No product source changed during this run. Independent review remains deferred after the human pause on Claude calls; this candidate is not review-approved.
