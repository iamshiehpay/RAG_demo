# #12 D16 UI follow-up — completion / merge request (fugu)

**Candidate:** branch lat/12-chat-layout, worktree .worktrees/12-chat-layout, clean.
- HEAD e73485d, base main abd7fc7 (ff).
- Commits: 8a85bf6 (feat + dist), e13a947 (docs), f8abe50 (docs), 9a0715e (fix + dist), e73485d (docs).
- Changed: frontend/src (App, Answer, Composer, Shortcuts[new], styles.css), frontend/dist, frontend/review (checks.js, scripted-events.js, DESIGN.md, followup.sh[new]), docs/verification/ticket-12/followup/**.
- No changes to src/, tests/, scripts/, events.ts or pyproject.

**Runtime proof** (from each child's own response metadata; parent coordinator 129cbb66 is opus-5-5/medium/auto):
- Implementer a3163cdebee042bed: claude-sonnet-5-5 / effort high.
- Review 1 Spec ad7de6e3ff716dff9: claude-opus-5-5 / medium.
- Review 1 Standards afc1a0552985d7f39: claude-opus-5-5 / medium.
- Correction review Spec ac754edf4085d7776: claude-opus-5-5 / medium.
- Correction review Standards a117b2dd06dd5cac7: claude-opus-5-5 / medium.
- Child transcripts have no permissionMode field; the parent's 'auto' is observed separately.
- Locators: /private/tmp/claude-501/-Users-shiehpay-Desktop-resume-rag--worktrees-12-chat-layout/129cbb66-f517-4752-8f41-d1bf01142d0d/tasks/<id>.output

**Reviews** (full reports in .lat/briefs/):
- Round 1 (abd7fc7..f8abe50):
  - Spec CHANGES REQUESTED (fugu-12-review-spec.md)
  - Standards CHANGES REQUESTED (fugu-12-review-standards.md)
  - HIGH: list-item whitespace deletion. MEDIUM: stuck drag on mid-drag unmount, re-verification pointer. LOWs/NIT.
- Corrections at 9a0715e (fugu-12-correction-report.md).
- Round 2, scoped (f8abe50..e73485d), fresh contexts:
  - Spec APPROVE (fugu-12-rereview-spec.md)
  - Standards APPROVE (fugu-12-rereview-standards.md)

**Tests:**
- Final full suite once at 9a0715e, worktree cwd and src imports: 327 passed / 3 deselected / 0 skipped / exit 0, 270.75s (followup/pytest-final.txt).
  - The earlier 327 at f8abe50 (pytest-full.txt) is historical.
- followup.sh final run 7: 75 PASS / 0 FAIL. Both reviewers reproduced it (75/0 on 8125; 31/0 focused on 8126).
- Red evidence kept in followup/before/:
  - checks.js on the old dist: 24 FAIL
  - followup-f8abe50-focused.txt: 3 FAIL
  - followup-run6-1fail.txt
  - partial old-dist run
- Run-6 failure was a harness timing premise (headless resize before a produced frame). Production layout was verified correct by direct measurement: 1440→1000 gives max 382, pane 382, chat 360.
- Dist parity was verified by both rounds of Standards reviewers (temp build, identical hashes).
- No cloud/provider calls, no .cache writes, no new N3.

**Path inventory:**
- Covered:
  - source pane: drag, keyboard, pointercancel, release outside, mid-drag unmount at the breakpoint, window resize at 1440/1000/920, collapse/expand, absurd stored width, throwing storage
  - 390 overlay, focus and Escape
  - shortcuts: no doc, uploading, Ready, generating, double click, triple click, error, non-LightRAG document, focus retention
  - composer: Enter, Shift+Enter, synthetic IME
  - replay-cost, replay-q3, spacing, tightlist, compare, unverified, error at 3 widths
- Not covered: real model answers, physical IME, screen reader, Firefox/Safari. The retry, provisional, markdown, budget and missing-source scenarios were not rerun in this follow-up.

**Known limitations / non-blocking:**
- The shortcut set is chosen by filename (/lightrag/i).
- aria-disabled shortcuts stay in the Tab order.
- A second pointerId ends the drag.
- README says "six scenarios" (now seven).
- N1: a Markdown hard break inside an li gives an extra blank line, likely pre-existing.
- The del strike is asserted by computed style only.
- The recorded Q3 factual FAIL is unchanged (outside the UI scope).

**For Main at integration:** commit the D8–D11 rows in docs/verification/final-acceptance/manual-qa-checklist.md (they are only in Main's working tree); merge; run one post-merge full suite; then user manual QA per D09.

**Resources:**
- Every child-started server (8121–8126) and browser session is stopped; 8121–8126 have no listeners.
- Scratch files remain under /private/tmp/claude-501/ and the scratchpad.
- The worktree holds the copied .cache/data/.venv/node_modules (gitignored); remove it after merge.
- 8101 and 8201 were never touched.
