# #12 D16 correction report (implementer Sonnet 5.5 high, a3163cdebee042bed)

Commits:
- 9a0715e fix(frontend): Keep inline list spaces, end drags on unmount and harden shortcut focus (includes the rebuilt dist)
- e73485d docs: Add ticket 12 follow-up final full-suite output

Findings:
1. HIGH, whitespace: trimStructuralWhitespace now drops only newline-only text beside block children, and trims only before a nested ul/ol. A new tightlist scenario asserts exact li.textContent: "see this and that now C1", "A B", "中文 粗體 文字". It runs at 1440, 920 and 390.
2. MEDIUM, drag: the drag stores pointerId and ends when buttons===0 or the pointer differs. An effect resets the drag when the separator unmounts. A followup.sh real-drag→800→release→1440 check asserts no .resizing, no data-dragging, no hover resize, and user-select restored.
3. MEDIUM, re-verification: the README has a one-line pointer to Main's manual-qa-checklist.md; that file was not touched.
4. LOW, del and links: del keeps line-through (asserted by computed style; not visually confirmed in the screenshot). Links are slate with ↗; citations are unchanged.
5. LOW, shortcut focus: aria-disabled plus a guarded click; focus stays on the shortcut (asserted).
6. LOW, shortcut border: #8B8576 gives 3.52:1 (asserted ≥3).
7. LOW, separator ARIA: aria-controls="source-pane" and aria-valuetext "來源欄寬 N 像素".
8. LOW, README count corrected to 24.
9. NIT, mirror check replaced by an observable weight/stroke difference.
10. Red baselines:
    - followup-f8abe50-focused.txt: 3 FAIL (stuck .resizing, user-select none, tight-list text). The hover-without-button resize did NOT reproduce on f8abe50.
    - The old-dist run was stopped early and is kept as partial (followup-before.txt).
    - The run-6 1-FAIL log is kept.

Run-6 diagnosis: a harness premise, not production.
- Before a frame: pane 720, aria-valuemax 720, chat 22, left 250.
- After one forced frame: pane 382, aria-valuemax 382, chat 360, left 250.
- 382 = min(720, 1000−250−8−360). followup.sh now forces a frame after each viewport change.

Checks:
- build OK; typecheck OK; test:source OK; check:events OK
- pytest test_http + test_event_types: 6 passed
- followup.sh run 7: 75 PASS / 0 FAIL (checks.js for replay-cost, replay-q3, spacing, tightlist, compare, unverified and error at 1440/920/390, no overflow)
- Full suite: run once at HEAD 9a0715e from the worktree cwd, imports from the worktree src. 327 passed, 3 deselected, 0 skipped, 6 warnings, 270.75s, exit 0 (followup/pytest-final.txt).

Limitations:
- Headless frame production is needed for resize checks.
- Using aria-disabled is a trade-off.
- No screen reader, Firefox or Safari testing.
- Replay and scripted data only; no real model answer.

Resources:
- Stopped: uvicorn 8121 (PID 46030), http.server 8122/8123 (PIDs 55428/55430), agent-browser nova-uifix, and a lingering followup.sh. Ports 8121–8123 are free.
- Scratch remains in /private/tmp/claude-501/.
- 8101 and 8201 were never touched; no cloud calls; no .cache writes.
