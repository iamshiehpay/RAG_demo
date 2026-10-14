# #07 review-fix acceptance evidence

Independent review #3297 requested six corrections. Implementation checkpoint `5e7e75c` includes all six, rebased onto main `109bab3`. The initial report and screenshots 01–08 remain as historical evidence; this report supersedes their acceptance conclusion.

## Results

| Review finding | Correction and evidence |
| --- | --- |
| Natural prose containing 未驗證 produced a false badge and UI text polluted history | FinalEvent carries structured Unicode code-point UnverifiedSpan offsets. Answer/history stay clean; React uses Array.from to apply spans. Screenshot 10: one badge only on the invalid-C99 sentence, including its emoji; the natural 未驗證 phrase stays ordinary prose. |
| Batch extraction discarded valid Citation ranges | CitationText receives the batch's allowed Citation map. Oversized Synthesis regression uses real local bge-m3 and checks ranges survive into the final answer prompt. |
| Abbreviations split invalid-Citation sentences; removal left double spaces | Sentence boundaries recognize vs., e.g., i.e. and et al.; flagged sentences collapse excess spaces. Application-level regressions cover all four and clean offsets. |
| Router and query embedding transport errors used answer_failed | Stage-specific router_failed, embedding_failed and answer_failed codes. Six connection/timeout regressions verify downstream work stops and same-question retry recovers. Screenshot 12 shows Router connection failure, local Ollama daemon guidance and enabled Retry. |
| Retry deltas lost the 重新產生中 label | A persistent retrying Turn flag retains the label throughout provisional replacement text. Screenshot 09 pauses after a retry delta, before final: 重新產生中 · 暫定, provisional=true, no badges. |
| An older failed Turn could be retried after newer successful Turns | Only the latest Turn has a Retry button, with the same guard in ask. Screenshot 11: three Turns, old error preserved, old Retry buttons=0. Screenshot 13: latest failed Turn recovers in place, one Turn, no error. |

Ranges remain all-or-nothing: if any ID is absent, the whole range is invalid. The independent reviewer accepted this rule. No partial valid range is silently retained.

## Verification

- `uv run pytest -q tests/integration/test_failure_handling.py`: **28 passed** before rebase; included again in the full integrated suite.
- `uv run pytest -q`: **138 passed, 2 deselected**, 130.40s after rebase and fixture correction. The opt-in live eval tests were excluded by project configuration. Six existing dependency deprecation warnings.
- `uv run ruff check src tests scripts/generate_event_types.py`: PASS.
- `uv run ruff format --check src tests scripts/generate_event_types.py`: PASS.
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `npm run typecheck --prefix frontend`: PASS before rebase.
- `npm run build --prefix frontend`: PASS after rebase, including TypeScript check; regenerated dist matches the committed review-fix assets.

Integration exposed one #08 test fixture that supplied only one truncated answer. It now supplies both the initial and low-retry truncations, asserts three calls (Router, answer, answer), low retry and no Judge. The first full run was 137 passed / 1 failed; the final run above passed. No eval implementation changed.

## Browser verification and reproduction

Chrome for Testing 154, built frontend, isolated agent-browser sessions, 1280×720. Screenshots 09–13 were visually inspected. Fresh connection/recovery run had no browser page errors or horizontal overflow. All task-owned QA servers and browser sessions were stopped; port 8170 has no listener.

This verifies controlled failure states. Only the LLM adapter is scripted; Application, Gateway, budget guard, event serialization, SSE, React, Citation validation and local bge-m3 are real. It does not evaluate cloud-model answer quality.

```sh
uv run uvicorn server:app --app-dir docs/qa/07-failure-handling --host 127.0.0.1 --port 8170
```

Upload a small text-layer PDF and ask a question. Release `first`, then `retry` using POST requests to `/qa/release/{gate}`. The second gate shows replacement text while status remains 重新產生中 · 暫定 (09). Release `retry_final` to see the final structured badge (10). The next question truncates twice. Submit another question to get a later success; the older error then has no Retry button (11). Stop the server.

```sh
uv run uvicorn connection_server:app --app-dir docs/qa/07-failure-handling --host 127.0.0.1 --port 8170
```

Upload the PDF and ask a question. The first Router call fails with ConnectError (12). Use Retry question to recover in the same Turn (13). The captured run used an equivalent temporary wrapper with these exact scripts; connection_server.py preserves it for reproduction. Stop the server when finished.

No unresolved #07 acceptance item remains. Independent re-review is pending; final #09 visual design remains owned by #09.
