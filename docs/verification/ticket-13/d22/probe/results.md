# D22 controlled diagnostic: stop after failed extraction gate

Two new live gpt-oss calls completed. Exact frozen direct answer and full-context evidence-ledger task both returned `文件中未提及`. The extraction prerequisite failed: no subject/variant definition, quotation or qualified author claim was emitted. No generic answer candidate was created or executed, no repetitions/held-out controls were run, and no repair or deployment is claimed. Six calls remain unused; no automatic continuation is authorized by this protocol.

| Condition | Declared task | Estimated prompt | Output reservation | Estimated total | Provider prompt | Provider output | Provider total | Terminal |
|---|---|---:|---:|---:|---:|---:|---:|---|
| condition-17 | Exact D21 baseline direct answer | 4104 | 3000 | 7104 | 3879 | 249 | 4128 | stop |
| condition-42 | Full-context evidence extraction | 4262 | 3000 | 7262 | 4037 | 412 | 4449 | stop |

Raw requests, all response frames, final answers, complete sources/original Chunks and gateway events/Trace are preserved in the condition JSON files. `call-accounting.json` counts the two started/completed calls, with no replay or upstream calls counted as new. Zero transport errors, length failures, retry calls or new LLM judges. Existing medium/3000 answer budget policy was used for both tasks; the low/1000 product fact-extraction policy was not substituted.

## Controlled variables and support

The new baseline messages exactly equal D21's frozen answer request. Across the two new calls the full user message, question, source order, seven source records, original Chunks, format=None, medium, num_predict=3000, model, temperature=0 and streaming settings are unchanged. The extraction condition only appends a declared generic system task; its additional instruction increases the prompt token count. The entire context is present, including C5's definition that original text was removed in -Origin and the authors' qualified statement that original text often contains irrelevant information that can introduce response noise.

Independent assessment is owned by Muko under `../assessment/`; its preregistered rubric was written before reading these outputs. Both outputs have neutral condition IDs, but task instructions in raw requests necessarily reveal the condition when inspected. This is partial output blinding, not fully blinded assessment.

## What this does and does not show

The tested full-context ledger instruction was insufficient to elicit the known supported qualified caveat. Exact refusal is also reproduced on a fresh baseline request. These observations do not prove a root cause, that all extraction designs fail, that prompt-only repair is impossible, or that an additional product-model call is required.

The extraction condition still inherits the baseline answering instructions and an applicability/refusal gate. It asks for evidence relevant to the current limitations question rather than an unconditional inventory. Failure therefore cannot distinguish inability to extract subject/quote/qualifiers from rejecting the evidence's applicability before emitting it, or instruction competition. We cannot label this a clean independent extraction-stage test. Captured thinking is retained for traceability, not used as causal proof. No model-reliability claim follows from one observation per condition.

Suggested next step for Main's decision: separately authorize one preregistered unconditional full-context subject/statement/qualifier inventory that does not classify applicability or compose an answer, then independently assess that inventory before any answer-stage experiment. That is a future prompt/task variant and was not executed after this failure. A public-path change, if eventually supported, still needs its own controlled regression and independent review; this fixed-source probe bypasses Router/retrieval and cannot explain the user's uncaptured original Global/Section observation.

## Scope and cleanup

Gina wrote only `docs/verification/ticket-13/d22/probe/**`. No product source, ordinary tests, caches, PDF ingestion, Golden Facts, frontend/site/server, retrieval, model or budgets changed. All D21/D18 failures remain retained. No services, ports, /tmp files or background probe processes remain; Main Python reused with PYTHONDONTWRITEBYTECODE=1. This cleanup information was sent to Main for its shared task card. Assessor owns its separate assessment artifacts. Commit, if made after coordination, contains only owned diagnostic evidence; no push/merge.
