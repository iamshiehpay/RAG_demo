# Chat with Document

Upload one PDF with a text layer, ask questions, and check the Section/page Citations against the original source. Global questions use the upload-time Summary Tree; Synthesis retrieves across Sub-queries; Lookup retrieves original Chunks and linked tables/paragraphs. Answers stream provisionally until completion. Trace exposes routing, retrieval, thinking, tokens, discarded evidence and retries.

## Start locally — Python and Ollama

Install **Python 3.12+** and [Ollama](https://ollama.com/). Start the local Ollama daemon, then prepare its models/account once:

```sh
ollama signin
ollama pull bge-m3
```

The account needs access to `gpt-oss:120b-cloud`. No API key or Node.js is required to run the committed frontend. Embeddings run locally with `bge-m3`; Document excerpts and summaries are sent to Ollama Cloud for text generation. Only PDFs with a text layer are supported; scanned, non-PDF and unreadable damaged files receive upload errors.

From a clean repository checkout:

```sh
python3 --version                 # must be 3.12 or newer
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101
```

Open **http://127.0.0.1:8101**. FastAPI serves the committed `frontend/dist/`, including local Noto Serif TC fonts. Choose a PDF, wait for Ready and its Document overview, then Ask. `OLLAMA_BASE_URL` overrides the daemon URL (default `http://localhost:11434`). On Windows, substitute `.venv\Scripts\python.exe` for `.venv/bin/python`.

If [uv](https://docs.astral.sh/uv/) is already installed, the locked equivalent is:

```sh
uv run --frozen --no-dev uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101
```

## Fixed test Documents

Download both public pinned versions (requires bash, curl and network):

```sh
bash scripts/fetch_data.sh
```

The script verifies SHA-256 on new and existing files and only publishes a complete verified download. A mismatching existing file is reported rather than silently accepted. PDFs are not committed.

| Document | Fixed source | Local path |
|---|---|---|
| LightRAG | [arXiv 2410.05779v3](https://arxiv.org/pdf/2410.05779v3) | `data/lightrag.pdf` |
| Long non-RAG industrial robotics review | [arXiv 2603.06749v1](https://arxiv.org/pdf/2603.06749v1), 109 pages | `data/industrial-robotics.pdf` |

Try `Summarize this document.`, `Compare LightRAG with GraphRAG.`, or `Performance of ablated versions of LightRAG`. A Chinese question receives a Chinese answer; numeric source values are preserved. A dependent follow-up is rewritten by the same Router call using only the latest two successful rounds, each capped at 500 tokens.

## Processing, Citations and budgets

Uploads return HTTP 202 and background SSE progress: parsing → chunking → embedding in batches of eight → summaries n/N → complete. Ready enables questions; a failed replacement retains the previous Document/conversation. Section-aware Chunks do not cross Sections; References are removed, Appendices retained. Coordinate-reconstructed tables keep their labels/baselines; uncertain reconstruction is flagged in source and answer instructions.

Section Summaries retain original source IDs. Long Documents have Group layers; Global chooses the most detailed complete layer fitting its question. `[C#]` opens original Chunks; `[S#]` opens summary content, page range and covered Sections. Invalid IDs are removed with an explicit Unverified sentence marker, never silently made trustworthy. Uncited sentences are not automatically marked (D01).

Every text-generation call crosses one budget guard: `o200k_harmony` prompt estimate plus 300-token template margin plus output reservation must stay within **10,000**. Router uses low/600, answers reserve 3,000 including thinking, Judge low/1,000. Trace and eval report both estimated and provider counts. `done_reason=length` fails that attempt; answer retries once with low, replacing provisional text. Discarded summary attempts may also retry without publishing truncated drafts. Questions over 1,000 tokens are rejected before LLM calls.

The ingestion-only cache lives in `.cache/`, keyed by PDF content, source-derived pipeline version, embedding/summary models and effective Chunk target. It stores Document/Chunks/vectors/Summary Tree atomically. It stores no answers or conversation history. Source or ingestion-setting changes invalidate incompatible records. Final cache manifests and observed zero-model-call reuploads are recorded in `eval/reports/issue11/cache-manifest.json`; actual caches stay gitignored and must be retained/transferred for a demo.

## Settings and reproducible evaluation

Environment controls are read by the HTTP factory and Application/eval. Explicit `RetrievalSettings` injection is also supported. Current defaults and chosen experiment results are documented in `AGENTS.md` and `eval/reports/issue11/`.

| Variable | Purpose |
|---|---|
| `CHUNK_TOKEN_TARGET` | Section-local paragraph target; experiments compare 256/500/800 |
| `LOOKUP_TOP_K` | Lookup primary hits before table links/neighbors |
| `SYNTHESIS_TOP_K`, `SUB_QUERY_TOP_K` | Main question/Sub-query hit counts |
| `BM25_WEIGHT` | 0=dense; 0–1 weighted reciprocal-rank fusion of dense and BM25 |
| `ANSWER_THINK` | `low` or `medium`, keeping the same 3,000 reservation |
| `SUMMARY_CONCURRENCY` | Positive upload Summary call concurrency (default four) |

BM25 uses a basic Unicode word tokenizer; Chinese queries without English lexical overlap keep dense ranking. Cosine and weighted RRF scores are distinguished in Trace. The concurrency experiment measures short guarded prompts; success through a tested in-flight count does not prove a universal cloud service ceiling.

Install developer tools with `uv sync --frozen`, or `pip install pytest pytest-asyncio opencc ruff` in the environment. Run from the repository root:

```sh
PYTHONPATH=src:. uv run --frozen pytest
PYTHONPATH=src:. uv run --frozen pytest -m eval -s --eval-cases Q1,Q2,Q3 --eval-repeats 3
PYTHONPATH=src:. uv run --frozen pytest -m eval -s --eval-cases SECOND_NUMBER,SECOND_SUMMARY --eval-repeats 3
```

Default tests use scripted LLMs plus actual local bge-m3; Ollama must be running. They do not call the cloud LLM. `-m eval` is opt-in. `--eval-cases` excludes unrelated live tests; the 20-case Router smoke remains separately runnable with `tests/integration/test_router_smoke_eval.py`. Reports include each fact's raw rate, evidence/reason, effective settings/pipeline, all LLM counts/reservations/latencies/done reasons, separate functional status and all length attempts. Semantic/forbidden FAIL remains a known defect under D05; it is never relabelled PASS. Functional failures remain failures.

The Issue11 driver uses the same Application/Gateway, real PDF processing and models, with reusable ingestion caches:

```sh
PYTHONPATH=src:. uv run --frozen python -m scripts.tune retrieval
PYTHONPATH=src:. uv run --frozen python -m scripts.tune retrieval-controlled
PYTHONPATH=src:. uv run --frozen python -m scripts.tune answers
PYTHONPATH=src:. uv run --frozen python -m scripts.measure_summary_concurrency --output eval/reports/issue11/concurrency.json
PYTHONPATH=src:. uv run --frozen python -m scripts.tune final
```

Final selected settings must match production defaults/environment before `final`. Tuning and final eval were bounded to three elapsed hours by D05; the final reports preserve measured defects rather than promising 100%. Final reports completed 27 actual answers with operational PASS and raw Golden Facts FAIL; all nine absent-answer runs passed fixed-refusal checks. No formal Router/Answer call truncated. The second-document numeric source-Citation check passed 2/3: one valid reference pointed to a different table. Detailed causes and manual numeric comparisons are in `eval/reports/issue11/conclusions.md`.

## Known limitations

- Reloading the page during an unfinished upload loses the frontend job identity; automatic resume across that reload is **UNPROVEN**. Keep the page open through Ready; select/upload again if needed. Restart also clears the active in-memory Document and conversation. No resume endpoint or persistence feature is claimed.
- Answer completeness, exact Chinese script following, universal comparison overclaims and some missing per-bullet Citations have been observed. Inspect original sources; current raw N=3 outcomes/failure analysis are in the final reports. UI/table rendering PASS does not establish answer-quality PASS.
- Judge excerpts can be nonverbatim, and the numeric binder can falsely reject correct values or falsely accept reversed table direction. Raw checker results and manual source comparisons remain separate; facts are not silently regraded.
- Mixed-font split numeric headings can attach the numeral to the wrong Section; uncertain tables keep their raw text and warning. This preexisting parser/provenance limitation is documented, not reported as passed.
- The second Document postdates the original August 2025 gpt-oss release, but exact hosted model weights/training provenance are opaque and **not proven**. No claim that the hosted model could never have seen it is made.
- Only one active Document, local execution, text-layer PDFs; no Docker, OCR, cloud deployment, RAG frameworks or conversation summaries.

## Frontend development

Only developers need Node.js 20.19+. The approved paper/serif/Citation-margin design is preserved.

```sh
npm ci --prefix frontend
npm run dev --prefix frontend          # Vite 5101 proxies /api to backend 8101
npm run typecheck --prefix frontend
npm run build --prefix frontend
PYTHONPATH=src:. uv run python scripts/generate_event_types.py --check
```

After frontend edits, rebuild and commit `frontend/dist/`. `events.py` defines the SSE contract and generates `frontend/src/events.ts`. The Application's upload/ask seams own all processing; HTTP only transports their events. A standalone Python wheel does not include frontend assets; run from the full source checkout as shown above.
