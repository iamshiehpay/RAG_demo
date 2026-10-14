# Independent narrow transition: FAIL on candidate and baseline

Reviewer lori; native session `01a13822-11fd-7f11-bf7c-dd5c1992df7e`, turn_context line8 in `/Users/shiehpay/.codex/sessions/2026/10/14/rollout-2026-10-14T09-58-39-01a13822-11fd-7f11-bf7c-dd5c1992df7e.jsonl`: gpt-6.1-sol, medium, workspace-write, on-request. No children/model/provider calls. Browser agent-browser0.27.0; bundled Chrome154.0.8037.57 headless. Owned session `nova-label-review` only, viewport390×844.

## Exact path

Candidate `1c364b8128c1b6dca476f41b13cb28a177dc7e8b` (product8e15852), worker server8121. Open page, set viewport, inject `frontend/review/scripted-events.js` through `eval --stdin`, upload `data/lightrag.pdf`. Set uncertain-table, type/submit it, open C1, Escape, set compare, type/submit, open reconstructed C2, Escape. First Escape succeeds and compare submits. C2 screenshot shows reconstructed grid, no uncertain-table note. Second Escape command returns success; following snapshot times out35s, DOM eval and plain URL command time out8s. No q3 typing/submission happened. Exact post-upload commands/results: `narrow-transition/commands.txt`; screenshots01/02.

Bounded diagnostics mapped own daemon32263 to Chrome39902 through its established localhostCDP59809 connection and PPID. Chrome39902 started10:12:39 after daemon launch10:10:13; before any reviewer reset, /json/list returned only blank/NewTab targets, with product target gone (`post-stall-targets.json`). This supports browser target loss/relaunch, not an existing merely hidden textarea.

Raw CDP bypass comparison used this proven owned browser. `direct-cdp.mjs` preserves mouse coordinates, genuine keydown/up, file-input upload and exact runtime commands. Candidate again reached uncertain→Escape→compare→reconstructedC2. Screenshot `cdp-reconstructed.png` confirms source grid. After Escape, Runtime.evaluate timed out8s; /json/list timed out3s (empty `post-cdp-stall-targets.json` records absence, not success). Chrome39902 measured98.6% CPU. This is browser-level unresponsiveness, beyond an AX snapshot/daemon-only failure; no specific application loop is proven.

Main provided8122, exact baseline58586f7 dist. Fresh same owned session; same fixture and same rawCDP program, via:

`REVIEW_PREFIX=baseline- REVIEW_URL=http://127.0.0.1:8122/ REVIEW_CDP_PORT=60665 node docs/verification/ticket-12/overview/review/narrow-transition/direct-cdp.mjs`

Baseline also reaches reconstructedC2, then Escape→Runtime.evaluate8s timeout; Chrome56524, PPID56480,91.8% CPU. See `baseline-direct-cdp.txt` and `baseline-cdp-reconstructed.png`. Both JS SHA256 values are recorded in `assets.json`.

## Conclusion and limits

FAIL on both exact candidate and baseline; no demonstrated D21 regression, no proof q3 submits once on either run. Candidate is not an end-to-end interaction PASS. Fresh-page warning checks do not waive this failure. Root cause could involve Chromium/browser operation or application interaction; source inspection alone does not establish it. No application/backend fix attempted; no Global extension, physical IME, other browser, provider, broad suite or build.

## Cleanup and inventory

Close command timed out5s for both hung browsers. Proven owned diagnostic51620, Chrome39902/56524 and daemon32263/56480 were terminated; daemons that ignored SIGTERM received SIGKILL. Proven profile directories9ffeae57… and6bf9a28b… were already absent when explicit cleanup checked them; no rmtree operation is claimed. Own nova-label-review runtime sidecars were removed. `cleanup.txt` records full proven paths and final absence results. Unknown initial browser-profile path preserved. Worker server8121, Main baseline8122 and default/qa06b untouched. Evidence contains commands.txt, direct-cdp.mjs, candidate/baseline direct-cdp.txt, target diagnostics, assets.json, cleanup.txt and four screenshots. No git commit/push; Main owns integration.
