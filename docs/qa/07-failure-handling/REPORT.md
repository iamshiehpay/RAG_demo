# #07 acceptance evidence

Implementation checkpoint: `e3a0c45`, branch `lat/07-failure-handling`, base `f5be286`.

## Commands and results

- `uv run pytest -q tests/integration/test_failure_handling.py`: **22 passed**, 9.25s. Real local bge-m3; recorded ScriptedLLM.
- `uv run pytest -q`: **98 passed, 1 deselected**, 102.12s. Cloud eval excluded. Six existing dependency deprecation warnings.
- `uv run ruff check src tests scripts/generate_event_types.py`: PASS.
- `uv run ruff format --check src tests scripts/generate_event_types.py`: PASS (33 files).
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `npm run typecheck --prefix frontend`: PASS.
- `npm run build --prefix frontend`: PASS; regenerated dist committed.

## Ticket acceptance criteria

| Criterion | Result | Evidence |
| --- | --- | --- |
| Content followed by length retries low once, then final | PASS | `test_length_with_content_retries_low_once_and_finalizes_only_replacement`; same prompt, 3,000 reservation, medium→low, only replacement in final/history; screenshots 01–03 |
| Two truncations end with error, no final | PASS | `test_two_lengths_end_in_error_without_final_or_successful_history`; trace retains router and both answers before terminal error; screenshot 04 |
| C99 sentence Unverified; Trace count 1 | PASS | `test_invalid_citation_flags_only_its_sentence_and_counts_in_trace`; screenshot 03 has valid C1, removed C99, inline marker and Invalid Citations: 1 |
| Query Embedder connection failure emits error | PASS | `test_transport_failure_stops_downstream_work_and_same_question_can_retry`, embedding × connection/timeout; no retrieval/citation_map/answer call |
| Provisional style, clearing retry, error retry button resubmits | PASS | Browser screenshots 01–05; retry DOM answer empty/status 重新產生中/provisional=true; error DOM answer empty/retry enabled; manual recovery errors=0/turns=2/provisional=false |

Extra confirmed coverage: D01 uncited sentences and fixed unsupported response are not flagged; duplicate invalid occurrences count individually; trailing Citations belong to preceding sentences; decimal numbers survive. Space lists and valid ranges normalize across individual-character frames, while invalid/reversed/mixed/huge ranges do not expand. Thinking events reach the stream and preserve split Citation markers. Router, query Embedder and answer connection/timeout each stop downstream processing and recover on the same question. Empty, disconnected and unterminated low retries never finalize. Existing Router length fallback remains unchanged and its regression tests pass.

TDD failure evidence: initial retry test observed error instead of retry; double-length test observed trailing trace instead of terminal error; C99 test observed unvalidated output; four normalization variants failed; thinking test observed no thinking events; trailing-Citation test incorrectly flagged the following sentence. Each was fixed at the existing application/Gateway/Citation seams before its passing run.

## Browser acceptance

Chrome for Testing 154, agent-browser isolated session `t07-failure`, built frontend at `http://127.0.0.1:8170`. Initial viewport 1280×720; focused thinking replay used browser default 1280×577. Screenshots were visually inspected. No browser page errors or horizontal overflow. Thinking details were collapsed by default, keyboard Enter revealed the model text (08), and mouse activation closed the visible disclosure. Screenshot 06 shows Router timeout; 07 shows same-question recovery with old error removed. All task servers and browser processes were stopped.

This is a controlled failure-state acceptance, not a cloud-model quality evaluation: only the LLM adapter is scripted; Application, Gateway budget guard, event serialization, HTTP/SSE, React, Citation validation and local bge-m3 are real. Query-embedding and answer transport failures are covered deterministically; browser transport recovery specifically exercised Router timeout.

## Reproduce the browser fixture

```sh
uv run uvicorn server:app --app-dir docs/qa/07-failure-handling --host 127.0.0.1 --port 8170
```

Upload any small text-layer PDF, ask a question, inspect the paused provisional text, then release it with `curl -X POST http://127.0.0.1:8170/qa/release/first`. Inspect the empty retry state; release its replacement with `curl -X POST http://127.0.0.1:8170/qa/release/retry`. The final contains C1 and invalid C99. The next question truncates twice; its Retry question button recovers. The following question fails Router timeout; retry recovers again. Stop the server when done. The fixture is isolated from production routes.

Remaining work: independent reviewer, then requested integration rebase/verification. No unresolved #07 acceptance items. Final #09 visual design remains owned by #09.
