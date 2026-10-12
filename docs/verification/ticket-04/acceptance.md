# Ticket #04 acceptance evidence

Scope: background Document ingestion, upload progress, versioned processing cache,
backend readiness guard, replacement state, and minimal upload UI. Summary Tree
and its progress events remain assigned to #05; final visual design remains #09.

## Automated verification

Run from the assigned worktree with local Ollama and bge-m3 available:

```sh
uv run pytest -q
uv run ruff check src tests scripts/generate_event_types.py
uv run ruff format --check src tests scripts/generate_event_types.py
uv run python scripts/generate_event_types.py --check
npm run typecheck --prefix frontend
npm run build --prefix frontend
```

Final deterministic suite: **151 passed, 2 deselected** in 119.26 seconds. Output is preserved in [pytest.txt](pytest.txt). No cloud
LLM calls were made. Ruff, formatting, generated event parity, TypeScript and
production frontend build passed. The built `frontend/dist/` is committed.

| Acceptance criterion / assigned gap | Evidence | Result |
| --- | --- | --- |
| Upload returns immediately; progress updates live | `test_upload_http_returns_202_while_embedding_is_pending_and_blocks_ask` returns 202 within a 2-second timeout while real bge-m3 is held at the dependency seam; browser processing screenshot shows the live GET SSE stage | PASS |
| Questions disabled with explanation until ready | Processing browser state has `#question.disabled=true`, progress `Embedding · 0/1`, and「文件處理中，完成後才能提問。」; ready removes the explanation and enables the question box | PASS |
| Same content bypasses Embedder and LLM | `test_same_document_uses_persisted_cache_without_embedding_or_llm` uses a fresh Application, emits only `ready`, restores identical Chunks/vectors, and records zero dependency calls | PASS |
| Pipeline version invalidates cache | `test_pipeline_version_and_content_changes_reprocess_the_document` verifies both version and PDF-content changes execute every processing stage and call real embedding again | PASS |
| HTTP progress ends in ready or error | `test_upload_http_emits_ready_or_error_and_serves_committed_frontend` exercises both terminal paths; `test_upload_returns_job_before_embedding_and_progress_replays_to_ready` checks replay ends at the same terminal event | PASS |
| Backend rejects asks before ready | Initial and replacement processing tests emit only `document_not_ready`; no Router/LLM calls occur | PASS |
| Failed upload preserves current Document | Replacement test retains Document, Index and history; browser failed-replacement state retains its prior answer and enables asking against the retained Document | PASS |
| Successful replacement resets Document/Index/history | Replacement test verifies fresh Index, empty history and failed lookup of old Chunk IDs; browser clears prior answer/source/question state on ready | PASS |
| Embedding failure is stage-specific | Failure injection yields `embedding_failed` with local Ollama daemon guidance, no ready/cache entry, and a successful full retry | PASS |
| No partial cache; answers never cached | Publication-failure test verifies existing records are unchanged and temporary entries removed; unreadable-cache test reprocesses; repeat-answer test records four LLM calls with different scripted answers and byte-identical cache contents | PASS |
| Background lifetime is independent of subscriber | Disconnect/replay test completes after closing the first subscriber; shutdown tests terminate with `ingestion_cancelled`, including cancellation before worker startup | PASS |
| Concurrent replacement cannot corrupt active state | HTTP pending-upload case returns 409 for a second upload; active-ask test rejects replacement until the ask iterator is closed | PASS |

## Browser acceptance

Environment: committed production frontend served by FastAPI on
`http://127.0.0.1:8150`, isolated agent-browser session `t04-ingest`, 1280-pixel-wide browser viewport (screenshots are 1280 × 577).
The QA Application used real local bge-m3 with an externally controlled release
gate and recording ScriptedLLM for one answer. Gates and QA endpoints existed
only in the temporary harness, never in the production API.

Paths: empty → upload/embedding → ready → ask → scanned replacement error → new
replacement/embedding → ready. Browser error collection was empty; processing
and ready states had no horizontal overflow. Screenshots were visually inspected.

- [Empty / disabled](ui/01-empty.png)
- [Processing / live stage and reason](ui/02-processing.png)
- [Ready / question enabled](ui/03-ready.png)
- [Failed replacement / old answer retained](ui/04-failed-replacement.png)
- [Replacement processing / question disabled](ui/05-replacement-processing.png)
- [Replacement ready / old answer cleared](ui/06-replacement-ready.png)

All task-started backend/browser processes were stopped. No other worktrees,
main checkout, Ollama daemon, or shared processes were changed.

## Integration seam

The cache stores the full serialized Document alongside embeddings; #05 can add
Summary Tree fields to Document, build summaries before publication, populate
`ReadyEvent.document_summary` on both cache branches, and bump `PIPELINE_VERSION`.
Job IDs identify progress streams and may differ from persisted Document IDs.
Jobs/progress are memory-only and reset on server restart; ingestion records
persist. API factory enables `.cache/`; application tests inject isolated caches.

#02 integration will retain its effective Chunk target in parsing/Chunking and
include it in `processing_config`, then rerun the full suite before merge.
