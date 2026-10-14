# #12 D16 scoped correction review — Standards axis (fresh Opus 5.5 medium, a117b2dd06dd5cac7), f8abe50..e73485d

Verdict: APPROVE. All 7 prior Standards findings FIXED; no blocking new issue.

Prior findings:
1. HIGH whitespace: FIXED. Answer.tsx now trims narrowly. Harness tight section passed. Own adversarial probes rendered correctly:
   - adjacent em
   - soft break
   - adjacent strongs
   - fenced code in li (exact pre)
   - adjacent citations
   - loose list
   - nested list after bold
   - CJK with no added spaces
   - blockquote and table
   - del/link
2. MEDIUM stuck drag: FIXED (App.tsx:105-133). pointerId plus buttons===0, and an effect on separatorShown. Harness unmount check passed.
3. LOW shortcut focus: FIXED (Shortcuts.tsx:23-25). aria-disabled plus a guarded click; 1 ask per activation; focus kept.
4. LOW border contrast: FIXED, 3.52:1.
5. LOW separator ARIA: FIXED (aria-controls=source-pane, aria-valuetext).
6. LOW README count: FIXED (24).
7. NIT mirror check: FIXED (now a behavioural weight/stroke difference).
- The Spec LOW is addressed too: del/s keep line-through, links get ↗, citations get no arrow.

followup.sh frame(): legitimate; the assertion is not weakened (chat>=360, scrollWidth<=innerWidth, max<=382). Direct measurement 1440→1000 with a 2s wait and no frame gave max 382, pane 382, chat 360, so the layout is correct either way.

Hard rules OK:
- Contract freeze: no changes to src/, tests/, scripts/ or events.ts.
- Dist parity: 107 files SHA-256 identical (temp outDir build).
- No external URLs, keyframes, animation or transition.

Non-blocking:
- NIT App.tsx:116: a move from a different pointerId ends the drag; ignoring it would be better (rare, nothing stuck).
- NIT followup/README.md:7 says "six scenarios", but there are now seven (tightlist).
- Info: aria-disabled shortcuts stay in the Tab order when unavailable (documented trade-off).

Ran:
- typecheck, test:source, check:events
- pytest test_http + test_event_types: 6 passed
- ONLY='drag unmount tight' followup.sh on 8126: 31 PASS / 0 FAIL
- adversarial probes

Inspected: pytest-final.txt (327 passed), followup-run.txt (75/0), before/ baselines.

Not verified:
- followup.sh sections shortcuts, drag920, narrow and checks (relied on saved output)
- no screen reader, Firefox or Safari
- no visual review of screenshots
- D8–D11 checklist reference

Resources: http.server on 8126 (PID 79606) stopped; session nova-uifix-rstd closed; no cloud calls; 8101 and 8201 not touched.
