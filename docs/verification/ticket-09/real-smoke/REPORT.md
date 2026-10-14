# Issue09 Standards correction: real final-renderer smoke

**Real format smoke PASS; semantic quality not scored.** Executed on frozen product source `cb4f1c9a164a40243a38358e59f2ed5c126bcf7c` after the final Markdown/Unverified/CRLF fixes. All **345 tracked product/frontend/backend/test/eval/script/config paths** are byte-identical to that source. [Identity hashes](product-identity.json). Only documentation and verification artifacts change in this correction.

Main released the exclusive cloud window and own8190/browser `nova-i09` at HCOM10232, accepted the small generic document at10255, and authorized the exact AI-log entry plus observed result. Fresh correction Reviewer: `nova-r09fix-gigi`, review base `cb4f1c9`; previous Reviewer duma does not re-review. This evidence addresses duma's Standards gate; it is not an independent QA verdict or an Issue09 completion claim.

## Genuine execution

The unchanged existing `tests/integration/test_tables.py::authored_table_pdf()` generated a one-page generic measured-values PDF. [Input provenance/hash](input.json). No compatible cache was supplied or assumed; the private cold cache uses the current real processing identity. The natural question contains no expected numbers or Citation IDs:

> 請用繁體中文簡述這份文件的實驗測量結果，以條列列出實驗、準確率與成本，並附引用。

`Application` used the actual local **OllamaEmbedder/bge-m3**, guarded **OllamaLLM/gpt-oss:120b-cloud** and existing upload/summary/router/answer/source/SSE code. `RecordingOllama` transparently delegates the exact request to `super().stream(request)`, stores returned adapter frames, then yields each frame unchanged. No scripted/fake LLM, fixed embeddings, response routes, output rewrite or expectation-fitted prompt was used. [Recorder](server.py), [local daemon model metadata](model-metadata.json), [raw model frames](model-frames.json).

The browser loaded committed `frontend/dist`, uploaded the PDF, filled the question, clicked Ask, inspected the answer, opened Trace, clicked a Citation and closed the source with Escape. Its fetch wrapper only clones actual responses for observation. **29 commands, zero failed**, successful final answer; Trace and thinking initially collapsed, source showed `p.1 · 1 Results`, and Escape returned focus to the citation. [Browser runner](browser.py), [command ledger](browser-commands.json), [display](display.json), [Trace display](trace-display.json), [source display](source-display.json), [actual source payload](source.json).

Raw API records: [upload SSE](upload.sse), [ask SSE](ask.sse), [observed HTTP responses](responses.json), [raw model answer/final event](answer.json). The raw answer is exactly equal to the backend final answer; no invalid IDs or Unverified spans occurred. Router selected **Global**, with `summary_level=section`, real `[S1]` metadata and no Chunk retrieval. That route is observed, not forced by the harness.

Raw `.sse` files preserve the native final blank event terminator. `git diff --check` reports their new blank line at EOF; this is intentional protocol evidence and was not trimmed. The earlier typecheck-log blank was ordinary console whitespace and was removed separately.

## All-call budgets and termination

Every real call used the production guard and native Ollama counters. Output reservation includes reasoning. [Complete proof/call ledger](proof.json).

|Call|think|Estimated prompt|Output reservation|Estimated total|Ollama prompt_eval_count|eval_count|Actual prompt + reservation|done_reason|
|---|---|---:|---:|---:|---:|---:|---:|---|
|Section Summary|low|493|1200|1693|268|117|1468|stop|
|Document Summary|low|515|2500|3015|290|105|2790|stop|
|Router|low|864|600|1464|525|150|1125|stop|
|Answer|medium|892|3000|3892|667|275|3667|stop|

**4/4 calls stop**, no length, retry or provider failure; every estimated and actual prompt-plus-reservation total is≤10,000. Maximum estimated total3892, actual total3667. The browser Trace's two ask meters show1464/10000 and3892/10000; upload calls are retained in the all-call ledger rather than omitted from the accounting.

## Observed rendering coverage and limits

Observed real answer: **three Traditional Chinese Markdown bullet items**, each with `[S1]`, decimal values and percent signs. The model used **U+202F narrow no-break spaces** and **U+3000 ideographic spaces**, both preserved by the final renderer. The visible list has three inline Citation buttons and three paragraph-aligned margin notes. It uses local Noto Serif TC16px and has no horizontal overflow at1280×720. The real Section Summary source and full Trace were displayed. Screenshots were visually inspected: [answer](evidence/answer.png), [Trace](evidence/trace.png), [source](evidence/source.png).

This run **did not** produce `[C#]` citations, invalid IDs, Unverified spans, CR/CRLF, emoji, escaped Markdown/entities, code, headings or Markdown tables. No rare format was fabricated, forced into the question or claimed as real coverage. The inherited deterministic148/10/6 browser suites remain evidence for those boundary/race/newline paths. Real LightRAG Q3 browser acceptance remains independent QA09 after integration; stochastic script reliability, semantic failures and final Golden Facts N=3 remain Issue11. The simple observed numbers are shown transparently, with no new general answer-quality or Golden Facts score.

## Standards documentation correction

Appended Main's exact supplied `.lat/briefs/nova-i09-ai-log-entry.md` to branch `docs/ai-log.md`, followed by this observed result/evidence link. The entry records decoded-position/Unicode/newline corrections, source races/restart state, QA05 mounted-versus-visible overview, and the mistaken Section-level fixture expectation. Existing ai-log prefix and all production paths remain unchanged. Independent fresh review must verify this bounded ownership extension and the correction delta from `cb4f1c9`.

[Exact-entry/prefix proof](ai-log-provenance.json). Owned server8190 and browser are closed, temporary PDF/cache removed, and four completed cloud calls recorded. [Cleanup](cleanup.json), [server transport log](server-log.txt), [genuine processing-cache identity](cache-provenance.json). No compatible pre-existing cache was used.

The previous integration self-check incorrectly marked the real-renderer requirement N/A because the producer/prompt was unchanged. Duma's Standards finding establishes that the rule also applies to the Markdown/Citation/Unicode consumer. That interpretation is corrected here; historical scripted results remain labelled as such. An evidence-only trailing blank in the earlier `typecheck.txt` was removed, preserving command/result text. No new tests, build, prompts, facts, source changes or acceptance criteria were introduced.

## Reproduction

From this worktree with logged-in local Ollama and bge-m3:

```sh
UV_CACHE_DIR=/private/tmp/nova-i09-uv-cache uv run --no-sync python docs/verification/ticket-09/real-smoke/server.py
python3 docs/verification/ticket-09/real-smoke/browser.py
```

Use the owned cold `/private/tmp/nova-i09-real-smoke-cache` to reproduce all four calls. These commands invoke the cloud and require Main's workload allocation; they should not be rerun merely to repeat successful verification. Browser scripts use only `nova-i09`. The server script recreates the PDF from the unchanged existing fixture. Cleanup proof and final resource state are recorded alongside this report.
