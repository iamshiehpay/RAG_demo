# Ticket #01 acceptance evidence

Worktree: `rag/.worktrees/01-walking-skeleton`; branch: `lat/01-walking-skeleton`; base: `940744f`.

## Reproduction and results

All checks ran on 2026-10-12 with local Ollama and real `bge-m3`. Deterministic tests substitute only a scripted recording LLM; the browser run used the real `gpt-oss:120b-cloud` model and the committed production frontend.

| Acceptance criterion | Command / interaction | Result |
| --- | --- | --- |
| One-command website; browser upload enables questions | `uv run uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101`; `agent-browser --session t01-kava open http://127.0.0.1:8101`; upload `data/lightrag.pdf` | PASS. 16 virtual Sections, 37 Chunks; Ready and enabled Question field. |
| Q3 streams; clickable Citation shows original and page | Enter `Performance of ablated versions of LightRAG`, click Ask; click `View C3, page 8, Virtual Section 8` | PASS. 173 delta events; 164 provisional DOM text updates (9 → 1,673 characters); 8 Citation buttons; clicked source shows Table 2 text and page 8. |
| Trace estimate, actual prompt, think, 10K bar, Chunks/scores | Scroll Trace into viewport and click `.trace > summary` | PASS. Estimate 2,043, `prompt_eval_count` 1,818, `think=medium`, output reservation 3,000; meter 5,043/10,000; five Chunk scores. Model thinking is collapsed. |
| Recorded fake calls stay within 10K | `uv run pytest tests/integration/test_operations.py::test_upload_document_and_ask_with_real_embedding_and_recorded_llm -q` | PASS. Independently recomputes o200k_harmony counts + 300; every call + 3,000 reservation ≤ 10,000. |
| Forced budget failure emits error and no final | `uv run pytest tests/integration/test_operations.py::test_guard_emits_error_without_final_or_llm_call -q` | PASS. Budget set to 1; `budget_exceeded`; no final; zero LLM calls. |
| HTTP/SSE event order | `uv run pytest tests/integration/test_http.py -q` | PASS, 2 tests. Ask order is plan → retrieval → citation_map → delta → delta → final → trace. Upload ends ready; source lookup works; unknown source explicitly returns 404. |
| TS events match backend models | `uv run python scripts/generate_event_types.py --check`; `uv run pytest tests/integration/test_event_types.py -q` | PASS. Types generated from Pydantic serialization schema; exact stale-file comparison. |

Full deterministic suite: `uv run pytest -q` → **10 passed in 6.01s**. No cloud LLM calls in this suite. Its cases additionally cover scanned Document rejection, >1,000-token questions, truncated/incomplete LLM streams and Citation markers split across stream frames.

Other checks:

- `uv run ruff check src tests scripts/generate_event_types.py` → all checks passed.
- `uv run ruff format --check src tests scripts/generate_event_types.py` → 20 files already formatted.
- `npm run typecheck --prefix frontend` → passed.
- `npm run build --prefix frontend` → passed; production `frontend/dist/` included in commit.
- `npm run dev --prefix frontend -- --host 127.0.0.1` → Vite serves on 5101. HTTP check confirmed frontend source and `/api/sources/unknown-id` proxy to backend 8101 (404 JSON `Source not found.`).
- `agent-browser --session t01-kava errors` → no uncaught page errors.
- Browser DOM assertions → all PASS in `browser-evidence.json`; no horizontal overflow at 1280×900.
- Browser session, FastAPI PID 34125, and Vite were stopped. `lsof -nP -iTCP:8101 -iTCP:5101 -sTCP:LISTEN` returned no listeners.

## Evidence artifacts

- `browser-evidence.json`: assertions and real model token/latency metrics, with thinking omitted from saved evidence.
- `q3-source-trace.png`: full Document-answer/source view.
- `q3-trace-viewport.png`: expanded Trace and source heading at 1280×900.

During the first real Q3 run the model used `【C3】` despite the ASCII marker rule. A regression test failed before the Citation formatter repair and passed afterwards; markers now normalize across frame boundaries. The first truncation implementation also lost failed-call Trace; a failing application-level assertion led to retaining Trace with the error. Both corrections are in `docs/ai-log.md`.

The browser tool's click did not dispatch an event to an offscreen summary. Scrolling it into the viewport and clicking verified the real native disclosure; no product change was needed.

## Scope and limitations

All #01 acceptance criteria are demonstrated. This slice is synchronously processed and Lookup-only. Page-based virtual Sections and raw table extraction deliberately remain: the real model's table interpretation is incomplete and may be wrong. Table reconstruction, complete Golden Facts, invalid-Citation validation and automatic retry belong to later tickets. The #01 UI does not claim those guarantees. No push, main-checkout edit or merge was performed.
