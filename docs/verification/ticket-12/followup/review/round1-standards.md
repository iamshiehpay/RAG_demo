# #12 D16 follow-up — Standards axis review (fresh Opus 5.5 medium, afc1a0552985d7f39), head f8abe50

Verdict (Standards): CHANGES REQUESTED

1. HIGH: Answer.tsx:39-51 `trimStructuralWhitespace`. It drops whitespace-only text in `li` (line 43) and trims before ANY element (line 47). Reproduced:
   - `- see **this** and *that* now [C1]` → "seethis andthat now"
   - `` - `alpha` `beta` gamma `` → "alphabeta gamma"
   - `- **A** **B**` → "AB"
   - links: "linkexample here"
   - CJK: `中文 **粗體** 文字` → "中文粗體 文字"
   Not affected: pre/code, td, blockquote, paragraphs.
2. MEDIUM: App.tsx:113-144, 223-226. If the separator unmounts mid-drag (crossing the 900px breakpoint), `dragging`/`dragStart` get stuck: `.workspace.resizing` persists, nothing can be selected, and hovering without a button pressed resizes the pane. Fix: reset when the separator stops rendering; end the drag on `buttons === 0`; check `pointerId`.
3. LOW: Shortcuts.tsx:310-311. Focus falls to BODY after activating a shortcut, because the button becomes disabled.
4. LOW: styles.css:414. Shortcut button border #D8D2C2 on #FBFAF6 is 1.44:1 (the text is 8.6:1).
5. LOW: App.tsx:223-226. The separator has no aria-controls and no aria-valuetext.
6. LOW: followup/README.md:5 says 23 FAIL before; the JSON contains 24.
7. NIT: checks.js asserts `webkitTextStrokeWidth > 0`, which mirrors the implementation.

OK:
- Double-submit guard (reset in finally; held generation plus Enter sends nothing).
- Clamping at 901/960/1199/1200/1280 keeps chat ≥ 360px.
- localStorage still works when storage throws.
- IME guard.
- Citation buttons have a focus ring.
- text-stroke fallback.
- No external fonts, CDN or animation.
- Contract freeze.

Ran:
- typecheck, test:source, check:events.
- pytest test_http + test_event_types: 6 passed.
- Dist parity: temp build, all 107 files SHA-256 identical.
- followup.sh 65/0 on port 8124.
- Adversarial probes.
- Inspected pytest-full.txt (327 passed).

Not confirmed:
- A specific "3 earlier bound failures" set. followup.sh was never run red against the old dist, so its interaction checks have no failing baseline. checks.js has a before-run with 24 FAIL.
- No SR/Firefox/Safari.

Resources: http.server on 8124 (PID 14600) and browser session nova-uifix-std, both stopped.
