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

## Current walking skeleton scope (#01)

Upload processes synchronously in the request. Each page is a virtual Section, paragraphs are packed into roughly 500-token Chunks, and dense retrieval returns the top five Chunks. Prompt excerpts follow Document order. All questions currently use Lookup. State is in memory and resets on restart or replacement upload.

Section detection, table reconstruction, background ingestion/cache, Summary Tree, Router, automatic retries/Citation validation, Golden Facts eval and the final Tufte design are later tickets. Q3 currently demonstrates the complete streaming/Citation flow; precise Table 2 interpretation is not an acceptance claim for this slice. A truncated or interrupted answer fails without becoming final; the UI clears provisional text and provides a retry button.

Every LLM call goes through the same Gateway: `o200k_harmony` counts the prompt, 300 tokens cover template overhead, and the policy reserves output including model thinking. Answer calls use `think=medium`, reserve 3,000 tokens and enforce the 6,700 raw-prompt-token cap. The Gateway raises before calling the adapter when the Context Budget would exceed 10,000. Trace records the estimate including the safety margin alongside Ollama's actual counts.

## Checks

The deterministic suite exercises the upload/ask application operations with a scripted, recording LLM and **real local bge-m3**. Ollama and bge-m3 must be available; the tests do not silently skip them. The suite also contains two HTTP/SSE contract tests and a generated-event-type parity check. It does not call the cloud LLM.

```sh
bash scripts/fetch_data.sh
uv run pytest
uv run ruff check src tests scripts/generate_event_types.py
uv run ruff format --check src tests scripts/generate_event_types.py
uv run python scripts/generate_event_types.py --check
```

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

`src/chat_document/application.py` owns `upload_document` and `ask`; HTTP and tests consume their typed event streams. `events.py` is the event-contract source of truth. Separate modules own PDF parsing, Chunking, embedding, Index, LLM adapters/Gateway, Answer Generator and Citation mapping. `ScriptedLLM` records complete guarded requests and can simulate stream fragments or failures. These modules let later tickets extend their paths without changing the two application seams.
