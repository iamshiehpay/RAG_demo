# Chat with Document

Upload one PDF with a text layer, ask a question, and open its `[C#]` Citations to check the original text and page number. Trace shows retrieved Chunks, cosine similarity and each LLM call's Context Budget.

## Run locally

Prerequisites: Python 3.12+, [uv](https://docs.astral.sh/uv/getting-started/installation/), and a running [Ollama](https://ollama.com/) daemon. No Node.js or API key is needed to run the committed frontend.

Prepare Ollama once:

```sh
ollama signin
ollama pull bge-m3
```

The answer model is `gpt-oss:120b-cloud`, accessed through the local daemon's native `/api/chat`. Your Ollama account must have cloud-model access. Embedding stays local; retrieved Document text is sent to Ollama Cloud to generate answers.

From this repository, start the whole website with one command:

```sh
uv run uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101
```

Open **http://127.0.0.1:8101**. Upload a PDF, wait for Ready, then ask a question. Expand Trace to inspect tokens and retrieved Chunks. Click a Citation to open the source below the conversation. `OLLAMA_BASE_URL` can override the daemon address (default `http://localhost:11434`).

Download the fixed LightRAG test Document before testing or demoing:

```sh
bash scripts/fetch_data.sh
```

Example question (Q3): `Performance of ablated versions of LightRAG`.

## Current scope (#01, #02, #03, #04, #05, #06, #07)

Upload returns HTTP 202 with a `job_id` and `events_url` after receiving the PDF bytes. Processing runs independently in a background job; GET `events_url` streams parsing → chunking → embedding n/N → complete, ending in `ready` or `error`. Progress can be replayed after disconnecting, and the UI offers reconnection if the progress stream is interrupted. A lost progress job (for example after server restart) releases upload controls and asks the user to choose the PDF again; HTTP 409 displays its backend detail. The question box explains why it is disabled during processing, and the backend rejects asks until ready. A successful replacement swaps Document/Index and clears conversation state together; a failed replacement retains the current Document and conversation. Concurrent replacement attempts, including during an active ask, receive HTTP 409.

Ingestion results are stored atomically in gitignored `.cache/`: complete Document metadata/Chunks, embedding vectors and Summary Tree. The cache key includes the PDF content hash, `PIPELINE_VERSION` in `cache.py`, and processing configuration (embedding model, effective Chunk token target and summary model). The version is `ingest-v2` plus a digest of parser, table reconstruction, Chunker, embedder, domain models, cache format, tokenizer and numeric-policy sources, so changes automatically invalidate prior records on restart. Re-uploading the same content, even with a new filename or after restarting, skips parsing/Chunking/embedding/summary generation and emits `ready` directly. New processing modules must join `PIPELINE_SOURCES` when integrated; #03 includes `tables.py` and `embedder.py`; #05 includes its Summary Tree builder, summary context, answer prompt, adapter and shared Gateway dependencies. Invalid cache records are reprocessed. Failed ingestion cannot publish a partial cache entry. A cache write failure logs a warning and still publishes the fully built Document; a later upload simply reprocesses it. Answers and conversation history are never cached. The production factory anchors this cache to the repo root, independent of the working directory; application-level tests inject temporary cache directories when exercising it.

Relative font sizes and bold heading lines identify Sections; split Section numbers/titles and wrapped titles are combined, including numbered body-size small-caps subsections. Two-column pages are ordered by column and position; short labels inside caption-identified figures are filtered while captioned tables become separate Table Chunks. References are excluded, Appendix is retained and labelled, and heading-free Documents use fixed-length virtual Sections. Whole paragraphs are packed into roughly 500-token Chunks within each Section; only oversized paragraphs split at English/Chinese sentence boundaries with about 10% overlap, snapping to complete words when needed. Chunk page ranges follow their actual paragraphs. A guarded JSON Router produces Question Type, Standalone Question and Sub-queries in one low-thinking call. Lookup selects five primary Chunks, adds reciprocal table/paragraph links, then fills remaining budget with adjacent Chunks by primary rank. Synthesis retrieves three for the Standalone Question and two per Sub-query, deduplicated with linked tables/paragraphs in Document order. Trace counts Chunks omitted for lack of budget. Global bypasses query embedding and Chunk retrieval, selects the most detailed complete Summary Tree level that fits the answer prompt, and generates an answer with [S#] Citations in the requested format and language. Context Packer batches oversized evidence into cited facts and merges them again when needed, retaining original Citation IDs. Active Document and conversation state remain in memory and reset on restart or successful replacement upload.

Upload builds Section Summaries (~15% of original text, target 80–500 tokens) concurrently; `SUMMARY_CONCURRENCY` sets the maximum in-flight calls (default 4; positive integer), or pass `summary_concurrency` to `Application`. Heading-only Sections with zero Chunks are skipped, while Table-only Sections are included. Oversized Sections are split before the 8,500-token prompt cap, summarized in parts and merged. Adjacent Group Summaries are built when a level exceeds the conservative answer capacity after reserving both supported question fields and prompt overhead (within the 6,000-token evidence cap), continuing until it fits. The unchanged Section level remains available for shorter questions. The Document Summary appears as 文件概覽 after ready and remains visible throughout the conversation. Summary sources show page ranges and the covered Section titles; provenance stores all original Chunk IDs. Uncertain-table reconstruction warnings survive every summary and remain visible in its source text. Truncated/empty/failed summaries fail upload before Document publication or cache writes. Cache keys include the summary model and pipeline sources, and cache hits restore the full tree. Trace identifies the Global summary level.

Coordinate table reconstruction retains caption, dataset/metric labels and comparison baselines. Tables above 2,000 tokens split between rows with repeated headers; ambiguous layouts keep raw text with「結構未能可靠重建」and the answer prompt requires disclosure. Citation source views render reconstructed tables as tables and display a limitation hint for raw fallbacks. Table 1/2 cells and Q3 evidence coverage have deterministic tests; Q3 live measurements are in `eval/reports/table-reconstruction-q3-n3.md` and `eval/reports/table-reconstruction-q3-generic-n3.md` (both record remaining answer-quality failures; the held-out Table 1 answer is recorded in `eval/reports/table-reconstruction-heldout.md`). Summary Tree and the final Tufte design are later tickets. Streamed text is provisional until `final`. A truncated answer retries once with `think=low`, clearing the first attempt and showing「重新產生中」. If that retry also fails, the UI clears partial text and shows a retry button. Router, query-embedding and answer connection failures stop downstream work and emit a terminal error (preceded by available Trace records). Connection errors identify the Router, query embedding or answer stage and advise checking the local Ollama daemon. Manual Retry is available on the latest turn. Invalid Citation IDs are removed, their sentence offsets are sent as structured Unverified spans for UI badges「未驗證 · Unverified」, and Trace counts the invalid occurrences; answer text and conversation history contain no UI markup; uncited sentences are not flagged (D01). Space-separated Citations and ranges are normalized, with ranges expanded only when every ID is supplied. Streamed model thinking appears in collapsed Trace details.


Conversation history stays in memory. Only the latest two successful rounds reach Router, capped at 500 tokens per round; answer generation receives the Standalone Question, evidence and current question as its language reference. The current question controls answer language. Questions over 1,000 tokens emit an explicit `rejected` event without calling an LLM.
Chinese answers preserve the current question's Traditional/Simplified script; ambiguous
shared characters default to Traditional Chinese. Source numbers remain unchanged.

Router names the JSON keys in its prompt and also sends the schema through Ollama `format`.
It tolerates the observed `type` alias and extra keys. A missing Standalone Question uses the
original question only without history; with history it records a failed rewrite. Trace shows
`plan_source` (`router` or `fallback`) and any `fallback_reason`, so fallback Lookup is visible.
The output reservation remains 600 tokens including thinking.
If a rewrite switches between Chinese and non-Chinese script, the current question is used
while preserving Question Type and Sub-queries. Trace records `rewrite_language_mismatch`
and the original `router_standalone_question`; no second Router call or translation is made.
For a dependent follow-up this may leave its reference unresolved, which the flag makes
visible. This script check does not distinguish languages using the same script.

Chunk size can be configured using the `CHUNK_TOKEN_TARGET` environment variable (default 500), or the keyword-only `chunk_token_target` argument to `Application`. The same value is validated by `RetrievalSettings.from_env()` and bounds virtual Sections too. Valid PDFs without a text layer are rejected as scanned Documents. Non-PDF and unreadable damaged inputs receive a distinct invalid-PDF reason; repaired PDFs with readable text are accepted with a logged warning. Citation side-notes show page ranges and Section titles, and open the original Chunk.

Retrieval counts can be configured using `LOOKUP_TOP_K`, `SYNTHESIS_TOP_K`, and `SUB_QUERY_TOP_K` environment variables (defaults 5, 3, and 2), or by passing `RetrievalSettings` to `Application` for eval. Values must be positive integers.

Every LLM call goes through the same Gateway: `o200k_harmony` counts the prompt, 300 tokens cover template overhead, and the policy reserves output including model thinking. Router JSON schema tokens are included in the estimate as well. Answer calls use `think=medium`, reserve 3,000 tokens and enforce the 6,700 raw-prompt-token cap. The Gateway raises before calling the adapter when the Context Budget would exceed 10,000. Trace records the estimate including the safety margin alongside Ollama's actual counts.

## Checks

The deterministic suite exercises the upload/ask application operations with a scripted, recording LLM and **real local bge-m3**. Ollama and bge-m3 must be available; the tests do not silently skip them. The suite also contains HTTP/SSE contract tests and a generated-event-type parity check. It does not call the cloud LLM.

```sh
bash scripts/fetch_data.sh
uv run pytest
uv run ruff check src tests scripts/generate_event_types.py
uv run ruff format --check src tests scripts/generate_event_types.py
uv run python scripts/generate_event_types.py --check
```

The default suite excludes cloud LLM evaluations. Run the 12-case live Router smoke explicitly:

```bash
uv run pytest -q -m eval tests/integration/test_router_smoke_eval.py
```

This requires the local Ollama daemon and cloud login. It records raw responses, plans and token
traces in a new timestamped `eval/reports/router-smoke-*.json`, resolved against the repository
root. It reports the 12 canonical cases and eight held-out cases separately, requiring at least
10/12 and 7/8 correct types, no fallbacks, and resolved historical topics. OpenCC (dev dependency)
flags Simplified-to-Traditional changes in Chinese rewrites; unchanged/shared characters are
inconclusive. Existing evidence files are never overwritten by the smoke.

## Frontend development

Node.js 20.19+ is needed only to edit/build the frontend. FastAPI serves committed `frontend/dist/`; Vite development runs on port 5101 and proxies `/api` to backend port 8101.

```sh
npm ci --prefix frontend
npm run dev --prefix frontend
npm run typecheck --prefix frontend
npm run build --prefix frontend
```

After changing frontend source, rebuild and commit `frontend/dist/`. After changing backend event models, regenerate `frontend/src/events.ts`:

```sh
uv run python scripts/generate_event_types.py
```

## Implementation seams

`src/chat_document/application.py` owns `upload_document` and `ask`; HTTP starts background upload through `start_upload` and subscribes through `upload_events`. HTTP and tests consume the same typed event streams. `ingestion.py` owns replayable job progress; `cache.py` owns versioned atomic ingestion records. `events.py` is the event-contract source of truth. Separate modules own PDF parsing, Chunking, embedding, Index, Router, Context Packer, LLM adapters/Gateway, Answer Generator and Citation mapping. `ScriptedLLM` records complete guarded requests and can simulate stream fragments or failures. These modules let later tickets extend their paths without changing the two application seams.
