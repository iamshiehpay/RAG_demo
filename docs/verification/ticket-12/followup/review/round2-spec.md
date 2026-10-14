# #12 D16 scoped correction review — Spec axis (fresh Opus 5.5 medium, ac754edf4085d7776), f8abe50..e73485d

Verdict: APPROVE. All 3 prior Spec findings are fixed and every D16 item still passes; nothing new breaks a hard rule.

Prior findings:
1. HIGH whitespace: FIXED (Answer.tsx:41-68). The tightlist fixture passes 7 cases at 1440/920/390. The reviewer's own probe kept soft breaks, bold before a nested list, a task item, "64.8 % / 35.2 % (Mix)[C1] and 1,399 社群", ~~gone~~ **kept** [link], loose ordered lists, blockquotes and paragraphs intact; no text was glued together and no number was split.
2. LOW del/s and link cue: FIXED. styles.css:122 restores line-through and :127 adds ↗; citations are buttons; 0 underlined elements.
3. MEDIUM re-verification pointer: FIXED, with a caveat. The README points to manual-qa-checklist.md D8–D11, but those rows are UNCOMMITTED in Main's working tree. Main must commit them at integration.
4. Info: the filename heuristic is unchanged and acceptable.

D16 items:
- Source pane: PASS (unmount reset at App.tsx:128-133; pointerId/buttons check at :115-116; 390 overlay, Escape and focus OK).
- Composer: PASS.
- Five shortcuts: PASS (exact strings; one ask per click, double click or triple click; none sent while generating; honest set for other Documents; border ≥3:1).
- Removals and underlines: PASS.
- Spacing and replays: PASS (the bad Q3 claim is kept unedited; no overflow).
- Hard rules: OK.

New (non-blocking):
- N1, likely pre-existing and not proven on f8abe50: a Markdown hard break (`a␠␠\n b`) inside an li renders an extra blank line, caused by <br> followed by a \n text node under pre-wrap. Rare in model output.
- N2: the D8–D11 rows are only in Main's working tree.

Verified:
- typecheck, test:source and check:events pass.
- pytest (2 targeted files): 6 passed.
- A scratch rebuild matches the committed dist (diff -r clean).
- followup.sh on 8125: 75 PASS / 0 FAIL.
- Inspected pytest-final.txt (HEAD 9a0715e, 327 passed, 0 skipped, exit 0).

Not verified: full-suite rerun, screen reader, Firefox, Safari, real model calls, physical IME, and N1 on f8abe50.

Resources: http.server on 8125 (PID 79135) and the nova-uifix-rspec session were stopped. Ports 8101 and 8201 were not touched.
