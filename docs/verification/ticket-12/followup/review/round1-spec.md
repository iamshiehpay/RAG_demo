# #12 D16 follow-up — Spec axis review (fresh Opus 5.5 medium, ad7de6e3ff716dff9), head f8abe50

Verdict (Spec): CHANGES REQUESTED

1. HIGH: Answer.tsx:43,52 `trimStructuralWhitespace` deletes spaces inside list items. Trailing whitespace before any inline element (strong/code/a/Citation) is trimmed, and whitespace-only text between inline elements is dropped. Reproduced in the browser on the committed dist:
   - `- The **full** model wins [C1]` renders as "Thefull model winsC1"
   - ``- run `npm i` now`` renders as "runnpm i now"
   - `- see **A** **B** here` renders as "seeAB here"
   This rewrites answer text and breaks the inline flow. Fix: trim only before nested ul/ol or block children; add list-item fixtures with mid-sentence bold, code and adjacent strongs.
2. MEDIUM: D16 checklist "補充原D1–D7人工清單的受影響情境供使用者再驗" is missing from the follow-up evidence.
3. LOW: styles.css:121 blanket `text-decoration:none` also strips `<del>` strikethrough and link cues. Exempt del, and give links a non-underline cue.
4. LOW/info: Shortcuts.tsx:12 chooses the shortcut set by filename `/lightrag/i`. An arXiv-named upload gets only the general question. Honest and documented.

Per item:
- Source pane: PASS.
- Composer: PASS.
- Five shortcuts: PASS (exactly one ask per click; non-LightRAG case honest).
- Removal of the two strings and underlines: PASS.
- Spacing: PASS apart from finding 1.
- No overflow at 1440/920/390: PASS.

Verified:
- typecheck, test:source, check:events.
- pytest test_http + test_event_types: 6 passed.
- No backend changes.
- followup.sh FAILS=0 (18 checks.js scenario runs).
- Own whitespace probe (Node and browser).

Not verified (Standards axis): dist parity, contrast, text-stroke fallback, React cleanup. Noted in passing: `dragging` can stay true if the separator unmounts mid-drag.

Resources: http.server on 8123 (PID 12436) and browser session nova-uifix-review, both stopped.
