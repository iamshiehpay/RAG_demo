# Ticket 14 correction — scoped Spec review

**Candidate:** `24fba2647c1b159049bf015bf63ca21a089cbcb6` against `d455f50d69d8061cc2aad7ff160d36f192c544d2` only.

**Verdict: No findings.** The prior P2 is corrected; the delta stays within the approved ask-orchestration scope.

Issue #14 requires preserving the not-ready/no-Document precheck and existing ask behavior (`.scratch/chat-with-document/issues/14-langgraph-ask.md:7-9,16`); D24 excludes upload migration and preserves request behavior (`.lat/decisions/D24-langgraph-ask-refactor.md:5,9`). `AskWorkflow` now snapshots readiness synchronously beside its captured index and Document (`src/chat_document/ask_graph.py:57-59`), and `validate` checks that snapshot (`:149-157`). This prevents a request that began during replacement from passing validation against the old captured index after the replacement publishes.

The added public-seam regression covers both Lookup and Global: it holds replacement processing, starts the ask, then allows upload to complete before graph validation; it checks rejection, no ask LLM calls/history, and that the next ask cites sources from the replacement Document (`tests/integration/test_ask_stream_lifecycle.py:246-298`). This directly covers the corrected race and recovery without adding product behavior.

The recorded correction evidence reports 2 baseline passes, 2 candidate REDs, 59 targeted passes, and 335 final ordinary-suite passes (`docs/verification/ticket-14/verification.md:200-240`). I inspected these records and did not rerun tests, the full suite, or provider calls.
