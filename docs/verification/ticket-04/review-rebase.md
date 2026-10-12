# #04 review corrections and #02 integration

Base: `3a15958` (main after #02 integration). Implementation checkpoint: `e799915`.
The rebase retains #02's parser/Chunker calls, effective target validation, Section
metadata and all its tests, plus #04's background processing and swap-on-success.
#04 job tests now live in `tests/integration/test_ingestion_jobs.py`.

## Verification

- `uv run pytest -q`: **192 passed, 2 deselected**, 189.00 seconds;
  [full output](rebase-pytest.txt). Local bge-m3 is real; cloud LLM calls excluded.
- `uv run pytest -q tests/integration/test_ingestion_jobs.py tests/integration/test_http.py`:
  **23 passed**.
- Ruff check, formatting, generated event parity, TypeScript and production build:
  **PASS**. Event types were regenerated after #02 integration; dist was rebuilt.
- Native browser on FastAPI port 8150, isolated `t04-review`, 1280 × 577: **PASS**.
  Task-only gates held real bge-m3 between batches; production source has no QA routes.

| Review item | Correction and evidence | Result |
| --- | --- | --- |
| Major: stale cache after target/schema changes | Key records effective `chunk_token_target`; ingest-v2 derives from parser/Chunker/models/cache/token/policy source digest. Target-change, legacy-pipeline and Section metadata cache roundtrip regressions pass. Failed replacement preserves old state after rebase. | PASS |
| Embedding stays at 0/N | Batches of 8 Chunks emit strictly increasing `completed`, ending at N; new batch-progress test uses real bge-m3. Native UI shows `Embedding · 8/32` before the held second batch is released. | PASS |
| Invalid vectors have generic error | ValueError during embedding is `embedding_failed`; invalid/zero-vector cases pass. HTTP errors mention Ollama only during embedding. | PASS |
| Cache writes discard ready Document | Cache write failures warn and continue to ready. Regression verifies existing records unchanged, no temp entry and fresh processing on the next upload. Mid-batch connection failure still publishes no partial cache. | PASS |
| 404 reconnect stuck; 409 detail lost | Actual hard restart interrupts SSE, exposes reconnect, then GET old job receives 404. Upload controls are released, reconnect disappears, and error says choose PDF again. HTTP 409 displays exact backend detail. Successful re-upload after restart clears the error. | PASS |
| Cwd-dependent cache directory | API factory anchors `.cache/` beside the repo frontend. Factory HTTP test changes cwd to a temporary directory and verifies its Document cache record is written only at repo root. | PASS |

Optional cleanup: shared Document publication helper; `UploadBusy` is a distinct
Exception. `UploadProgress` retains the `busy` prop agreed with #09.

## Browser evidence

- [Live intermediate progress, disabled question and reason](ui/07-live-batches.png)
- [Same-content cache hit](ui/08-cache-hit.png)
- [Exact 409 detail](ui/09-conflict-detail.png)
- [Interrupted SSE / reconnect](ui/10-disconnected-upload.png)
- [404 after restart / controls recovered](ui/11-restart-recovered.png)
- [Cached Document ready after restart](ui/12-post-restart-cache-ready.png)

[Initial cache-hit stats](ui/cache-hit-stats.json) show four batches of 8 for the
32-Chunk cold upload and no additional calls for its re-upload.
[Before/after comparison](ui/cache-hit-comparison.json) confirms identical
dependency counts when switching back from another Document through cache.
[Post-restart cache stats](ui/post-restart-cache.json) show zero embedding and
zero LLM calls in a new Application, with the persisted Document ready.

Browser error collection contained no uncaught errors. The interrupted SSE and
404 response were deliberately injected failure cases. Screenshots were visually
inspected; no horizontal overflow was observed. All task servers/browser sessions
and temporary harness files/cache were cleaned up; port 8150 has no listener.

## Extension seams

Source digest covers currently integrated ingestion modules. #03 must add its new
`tables.py` to `PIPELINE_SOURCES` (communicated to its owner); #05 must add Summary
Tree builder sources and attach its data to serialized Document before publication.
The shared publish helper is the single place to populate Document Summary in ready.
Neither future feature is implemented by #04. No unresolved #04 review items.
