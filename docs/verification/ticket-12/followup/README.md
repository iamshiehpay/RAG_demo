# Ticket #12 D16 follow-up evidence (2026-10-14)

Frontend only. All answers in the screenshots come from the scripted `/api/ask` harness (`frontend/review/scripted-events.js`); no model, cloud or `.cache` call was made.

- `replay-cost-*.png` and `replay-q3-*.png` are **replays of stored real model output** pasted by the user in the feedback (items 6 and 8), rebuilt into Markdown from the rendered paste. They are not fresh model runs. The Q3 text keeps the recorded factual FAIL ("All ablated models achieve lower win-rates than the full LightRAG ..."); that is an answer-quality finding, not a layout issue.
- `before/` holds the pre-change screenshots, `checks-before-1440-spacing.json` (new assertions run against the old dist with `window.__collectFailures = true`: 24 FAIL) and `measurements.json`.
- `followup-run.txt` is the output of `frontend/review/followup.sh` (real mouse and keyboard through agent-browser): 75 PASS, 0 FAIL (after review corrections). `checks/*.json` are the `checks.js` results for six scenarios at 1440, 920 and 390.
- Reproduce: serve `frontend/dist` (for example `PYTHONPATH=src uvicorn chat_document.api:create_app --factory --port 8121`), then `frontend/review/followup.sh http://127.0.0.1:8121 <session>`.

## Review corrections (after f8abe50)
- Red baselines kept under `before/`: `followup-f8abe50-focused.txt` (tight-list inline whitespace loss and the drag left stuck after the separator unmounts mid-drag, both measured against the f8abe50 dist), `followup-run6-1fail.txt` (a harness-only failure: headless Chrome re-evaluates media queries only when a frame is produced, so `followup.sh` now forces a frame after each viewport change), and `followup-before.txt` (a partial run against the abd7fc7 dist that was stopped early).
- Final green run: `followup-run.txt` (75 PASS, 0 FAIL); `pytest-full.txt` is from the earlier candidate and `pytest-final.txt` is the run after the corrections.
- 使用者人工重驗請依 `docs/verification/final-acceptance/manual-qa-checklist.md` 的 D8–D11 情境（該檔由 Main 維護，待整合）。
