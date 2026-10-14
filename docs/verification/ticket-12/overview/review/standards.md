# Independent Standards review

Verdict: **PASS for Standards only; zero findings. D21 review approval is scoped to this delta.**

Fixed comparison: `58586f786bc507c1b8e1d933974e1e4eb7c46bf6...1c364b8128c1b6dca476f41b13cb28a177dc7e8b`. Commits: 119a352, 08d86f6, 8e15852, 1c364b8. Working frontend matches the fixed candidate.

Hard documented-standard breaches: **none found**. Possible baseline smells: **none warrant a finding**. Tooling-enforced matters were not re-reviewed as style findings.

D21 supersedes AGENTS/CONTEXT's older visible Document Summary rule. `frontend/src/DocumentPane.tsx:10` retains upload/progress/error controls while removing the entire overview. `frontend/src/Shortcuts.tsx:21` preserves the accessible group name without a visible replacement heading; questions, filtering and click guard are unchanged. `frontend/src/SourceContent.tsx:5` centralizes the exact approved warning; its conditional raw-source rendering at line 30 and `frontend/src/AnswerProcess.tsx:149` preserve AGENTS' requirement to disclose uncertain Table Chunk structure. Separate rendering locations do not justify another abstraction. Summary provenance remains in `frontend/src/SourcePane.tsx:35`; source lookup still includes Section, Group and Document summaries in `src/chat_document/application.py:254`.

Build output and committed dist support AGENTS' rebuild requirement: `frontend/dist/index.html:3` points to index-CDC2lj04.js, whose inspected content retains the accessible name and shared warning, with no overview rendering classes. Existing evidence records 327 passed/3 deselected and final isolated narrow checks 7 PASS/0 FAIL. These were inspected, not rerun.

Limits: no tests/builds/browser/server/provider calls, children or source mutations. Scripted fixtures demonstrate UI behavior only. The earlier interrupted reconstructed-source → Escape → next-question transition is not resolved by isolated scenario resets; Spec's independent check must classify it. Physical IME/screen reader and integration remain unverified here. Overview evidence is an untracked, evolving documentation tail, separate from the fixed source candidate.

Paths inspected: AGENTS.md; CONTEXT.md; Main D21/D20/D16; approved-overview temporary brief; issue 12; frontend/src/{DocumentPane,Shortcuts,SourceContent,SourcePane,Composer,App,AnswerProcess,Shared,events,styles}; frontend/review/{checks.js,followup.sh,scripted-events.js}; frontend/scripts/test_source_content.mjs; dist index/JS; api.py/application.py source-route excerpts; docs/ai-log.md search; overview README/build/pytest/runtime/browser logs/global-390 assertions/ready-1440 and uncertain-390 images; label README/continuation/runtime/checks/DOM provenance.

Runtime: native session 01a13822-11fd-7cc3-89f8-ca2c5bdbf99b, turn_context line 8; gpt-6.1-sol, medium, workspace-write, on-request (auto_review reviewer).

Final disposition (Main message 18890): independent Spec reports zero findings and reproduces the transition failure on baseline and candidate; no D21 regression is demonstrated. Next-question continuation remains unproven. Main retains the operational FAIL for D09. Standards PASS stands; scoped D21 approval grants no all-UI-QA waiver. No additional inspection or execution performed.
