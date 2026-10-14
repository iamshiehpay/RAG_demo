# Standards-axis correction review

**Scope:** `d455f50d69d8061cc2aad7ff160d36f192c544d2` → `24fba2647c1b159049bf015bf63ca21a089cbcb6`, correction diff only.

**Documented-standard breaches: none.** The production hunk implements the Issue 14 request-start readiness capture alongside the captured `index`/`Document`, with validation consuming that snapshot. It leaves the LangGraph exception bounded as D24/ADR require. The test uses the public Application ask/upload seams and the actual graph for both Lookup and Global; evidence distinguishes baseline PASS, former-candidate RED, corrected targeted GREEN, and the corrected 335-pass suite. `ai-log.md` records the readiness finding and correction accurately. Prior 20 live calls are not presented as evidence for the readiness correction; narrow-screen remains explicitly unresolved.

**Documentation chronology note (minor):** `docs/verification/ticket-14/verification.md:218-219` says the final suite “runs” before review, while lines 231-240 record that it has completed. Change to “ran” (or equivalent) to avoid a stale prospective tense in the final frozen report.

**Judgment call, non-blocking:** `src/chat_document/ask_graph.py:59` makes `AskWorkflow` read the private `Application._active_upload` lifecycle field. The one-time snapshot is coherent and narrowly justified here, but it couples workflow initialization to Application internals (Feature Envy/private-state smell). If readiness rules grow, expose an Application-owned readiness snapshot. No correction is required for this bounded change.

Read-only review; no tests, provider calls, or full suite were run for this review.
