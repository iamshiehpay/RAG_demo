# Issue 14 — Standards-axis review

Candidate: `d455f50d69d8061cc2aad7ff160d36f192c544d2` against base `5f5e35f`; HEAD matches the candidate and the worktree is clean.

## Result: no findings

The implementation follows the accepted scope and lifecycle rules in `docs/adr/2026-10-14-langgraph-ask.md:5-11` and `.scratch/chat-with-document/issues/14-langgraph-ask.md:13-18`. `src/chat_document/ask_graph.py:34-87` keeps service/Document references on the request-scoped workflow object; graph state contains only transient ask data, with no checkpoint. Lines 96-146 use the capacity-one bridge, acknowledge yielded events, drain before completion/error, own and join the producer under shielding, and narrowly unwrap LangGraph cancellation. `src/chat_document/answer_generator.py:121-145` closes the existing native gateway iterator and retains its retry behavior. `src/chat_document/application.py:260-300` keeps public error mapping and `_asking` cleanup in `finally`.

Final/history timing is intentional: `ask_graph.py:238-260` validates and records the successful answer before Final, then emits Trace; `tests/integration/test_ask_stream_lifecycle.py:197-209` explicitly covers close-after-Final retaining history. The six public lifecycle cases cover disconnect, provider/consumer cancellation, repeated cancellation, paused-delta close, and task cleanup (`tests/integration/test_ask_stream_lifecycle.py:16-243`).

Evidence chronology is represented accurately: `docs/verification/ticket-14/verification.md:143-148` labels the live smoke as pre-final-correction; lines 132-141 record final targeted lifecycle evidence, and lines 178-190 record the frozen-source suite (333 passed, 3 eval deselected, zero skipped). I did not rerun tests. No LSP tool was available; a read-only source scan found no eval/exec, shell execution, pickle loading, or hardcoded-secret patterns in changed Python files.
