# QA report: ticket #07 失敗處理與串流狀態

- QA agent: `claude-opus-5-5` (LAT QA, high effort)
- Date: 2026-10-13
- Version tested: integrated `main` at `79c82a8` (code = `9538b88`). Working tree was clean except `.scratch/chat-with-document/EXECUTION.md`, which another agent changed; QA did not touch it.
- Committed `frontend/dist/` is up to date. A rebuild to scratch gives identical asset hashes (`index-dWzrijR7.js`, `index-l3yoQyrv.css`). `tsc --noEmit` passes. `npm run check:events` reports "Backend and frontend event types match."

## How the checks were run

| Layer | Setup |
|---|---|
| pytest | Full suite: `uv run pytest -q` gave **138 passed, 2 deselected**. #07 file: `tests/integration/test_failure_handling.py` gave **28/28 passed** (`pytest-full.txt`, `pytest-failure-handling.txt`). |
| Real path (port 8207) | `uvicorn chat_document.api:create_app --factory` with real `gpt-oss:120b-cloud` and real `bge-m3`. Real browser via agent-browser (headless Chrome). Uploaded `data/lightrag.pdf`, which gave 37 Chunks. |
| Scripted path (port 8208) | QA-only launcher, kept outside the repo at `<scratchpad>/qa_launcher.py`. It runs the real `create_app(Application(...))`, the real `LLMGateway`/`AnswerGenerator`/Citation Validator and real `bge-m3`. The LLM is a subclass of the repo's `ScriptedLLM` with runtime-pushed scripts, gates and injected `httpx.ConnectError`/`ReadTimeout`. Embedder faults come from a wrapper around the real `OllamaEmbedder`. **The UI checks on this port use scripted model output, not real gpt-oss.** |
| Real-adapter connection failure (port 8209) | QA-only launcher at `<scratchpad>/dead_port_launcher.py`. It uses the real `OllamaLLM` and `OllamaEmbedder`, repointed at the closed port `127.0.0.1:9`. This produces a genuine `httpx.ConnectError` without stopping the shared Ollama daemon. |

## Acceptance criteria

| # | AC | Result | Evidence |
|---|---|---|---|
| 1 | First answer has content and ends with `done_reason=length`; the retry succeeds; events include `retry` and end with `final` | PASS | pytest `test_length_with_content_retries_low_once...`. SSE sequence `plan→retrieval→citation_map→thinking→delta→retry→thinking→delta→final→trace`. Retry runs with `think=low`. `final` contains only the second attempt's text. Trace done_reasons are `stop, length, stop` (`scripted-sse-checks.json` A) |
| 2 | Two truncations in a row end in `error` with no `final` | PASS | pytest `test_two_lengths_end_in_error...`. SSE ends with `error` `answer_failed`, `has_final=false` (`scripted-sse-checks.json` B) |
| 3 | Answer cites nonexistent `[C99]`: that sentence is marked Unverified in `final`, and Trace invalid count is 1 | PASS | pytest `test_invalid_citation_flags_only_its_sentence...`. SSE: `unverified_text=["這句引用了不存在的編號。"]` and `invalid_citation_count=1`. The valid sentence containing 「未驗證」 is not flagged (`scripted-sse-checks.json` C) |
| 4 | Embedder connection failure emits `error` | PASS | pytest `[ConnectError-embedding]`, `[ReadTimeout-embedding]`. SSE `embedding_failed`, with no retrieval and no answer call. Real adapter at a dead port also gives `embedding_failed` (`real-adapter-dead-port.txt`) |
| 5 | UI: provisional text is visibly styled; `retry` clears it; an error shows a Retry button that re-asks | PASS | `01-real-provisional-streaming.png` (italic and muted, status 「回答中 · 暫定」) changes to `02-real-final.png` (normal). `A2-retry-cleared-regenerating.png` shows an empty answer and 「重新產生中」. `B1-double-length-error-retry-button.png` leads to `B2-manual-retry-recovered.png` (same turn replaced, 2 turns total) |

## Gap items owned by #07 (EXECUTION.md)

| Gap | Result | Evidence |
|---|---|---|
| `thinking` event in the backend; Trace shows it collapsed by default | PASS | Real SSE had 42 `thinking` events, all before the first `delta` (`real-sse-contract.json`). `details.trace` and every `details.thinking-content` report `open=false` (`real-stream-poll.log` probe and `03-real-trace-open-thinking-collapsed.png`). Expanded view: `04-real-thinking-expanded.png` |
| Normalising `[C1 C3]` and `[C1–C3]`; a range that reaches past the map is rejected whole | PASS | Split across frames: `[C1` / ` C3]` gives `[C1][C3]`; `【C2` / `–C4】` gives `[C2][C3][C4]`; `[C1-C2]` gives `[C1][C2]`. All render as clickable citations (`D1`/`D2` screenshots). Clicking `[C4]` opens "Source · p.8" (`D3-range-citation-C4-source.png`). `[C1–C99]` is removed whole: that sentence is marked Unverified and the count is 1, with no partial expansion (`scripted-sse-checks.json` D) |
| EV-05: connection error at ask time | PASS | Injected errors give `router_failed`, `embedding_failed` and `answer_failed`, each with "Check that the local Ollama daemon is running, then retry". The UI shows the message and a Retry button, and Retry recovers in all three cases (`E1*`, `E2*`, `E3*` screenshots). Real adapters at a dead port behave the same (`real-adapter-dead-port.txt`). The real daemon was not stopped, as instructed |

## test-list.md rows mapped to #07

| Row | Result | Notes and evidence |
|---|---|---|
| FL-01 | PASS | Covered by AC1 and AC5. The UI goes from attempt-one provisional (`A1`) to cleared with 「重新產生中」 (`A2`), then to 「重新產生中 · 暫定」 with the replacement text (`A3`), then to final (`A4`). Trace in the UI lists 3 calls: `router low stop`, `answer medium length`, `answer low stop` |
| FL-02 | PASS | No `final`. The UI answer is `""` after the error, so the partial text "Second truncated partial answer" is gone (`b2-state.txt`, `B1`) |
| FL-03 | PASS | Real gpt-oss. Every poll during streaming had class `provisional-text` and italic style, with no final styling before `final` (`real-stream-poll.log`). In a separate real curl run, the concatenated deltas equal the `final` answer (`real-sse-contract.json`) |
| FL-04 | PASS | Covered by AC3. UI: `.unverified-sentence` wraps only the `[C99]` sentence and carries the 「未驗證 · Unverified」 mark. Valid `[C1]`/`[C2]` stay clickable with correct pages, and no sentence is silently deleted. The Trace shows "Invalid Citations: 1" (`C1-invalid-citation-unverified-trace.png`, `c-answer-html.txt`) |
| FL-05 | PASS (per D01) | An uncited factual sentence is not marked. The fixed replies 「文件中未提及」 and "Not mentioned in the document." are not marked, and their count is 0 (`fl05-d01-checks.json`). In C, "An uncited opening sentence." is also unmarked |
| FL-06 | PASS | Router, embedding and answer each tested with ConnectError and ReadTimeout. Router and embedding failures make no retrieval and no answer call. The answer failure happens mid-stream and its partial text is cleared (`E3a` to `E3`). Retry resends the same question and completes, with no leftover error or provisional text (`e*-retry-state.txt`) |
| FL-07 (#07 part: `retry` and `thinking`) | PASS | Real order: `plan→retrieval→citation_map→thinking→delta→final→trace`. Scripted runs without `thinking` (C, D) cause no UI errors. `citation_map` arrives before the first `delta`, and deltas restart after `retry`. TS types match the backend. Note: on failure the backend sends `trace` before `error`, which the frontend handles |
| TR-04 (#07 part: invalid count) | PASS | "Invalid Citations: N" appears in the Trace. The highest-similarity display is out of #07 scope (#01 shows per-Chunk cosine; refinement is deferred to #11) |

## Known deferrals (NOT_EXECUTED, by instruction)

- Upload-time Ollama failure shows only a generic `ingestion_failed` message. Owned by #04.
- Classification of `HTTPStatusError` and `ValueError` stages. Owned by #11.

## Non-blocking observations

1. After an error, the status line "Answer failed" keeps the `status provisional` (italic) class. This is cosmetic; the answer text itself is cleared. Suggest #09.
2. When the model leaves no space between sentences, the Unverified mark runs straight into the next sentence ("…Unverified**An** uncited…", `C1-invalid-citation-unverified-trace.png`). This is cosmetic. Suggest #09.
3. Upload on integrated main labels all LightRAG Sections "Virtual Section N", meaning heading detection fell back. This is outside #07 scope (#02).
4. Tooling note: agent-browser clicks on the Ask button below the fold did not register until it was scrolled into view. This is a QA-harness artifact, not an app bug.

## Totals

16 PASS (5 AC, 3 gap items, 8 test-list rows), 0 FAIL, 0 UNPROVEN, 2 NOT_EXECUTED (deferred to #04 and #11).

## Cleanup

All processes QA started are stopped: servers on 8207, 8208 and 8209, and agent-browser sessions `qa07` and `qa07s`. `lsof` shows no listeners on 8207–8209. The Ollama daemon was never stopped or restarted (`/api/tags` returns 200). No repo source was modified, nothing was committed, and `.worktrees/` was not touched.
