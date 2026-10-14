# Ticket #12 D16 follow-up evidence (2026-10-14)

Frontend only. All answers in the screenshots come from the scripted `/api/ask` harness (`frontend/review/scripted-events.js`); no model, cloud or `.cache` call was made.

- `replay-cost-*.png` and `replay-q3-*.png` are **replays of stored real model output** pasted by the user in the feedback (items 6 and 8), rebuilt into Markdown from the rendered paste. They are not fresh model runs. The Q3 text keeps the recorded factual FAIL ("All ablated models achieve lower win-rates than the full LightRAG ..."); that is an answer-quality finding, not a layout issue.
- `before/` holds the pre-change screenshots, `checks-before-1440-spacing.json` (new assertions run against the old dist with `window.__collectFailures = true`: 23 FAIL) and `measurements.json`.
- `followup-run.txt` is the output of `frontend/review/followup.sh` (real mouse and keyboard through agent-browser): 65 PASS, 0 FAIL. `checks/*.json` are the `checks.js` results for six scenarios at 1440, 920 and 390.
- Reproduce: serve `frontend/dist` (for example `PYTHONPATH=src uvicorn chat_document.api:create_app --factory --port 8121`), then `frontend/review/followup.sh http://127.0.0.1:8121 <session>`.
