# Ticket #01 independent-review fixes

Reviewed head: `31281abf89b15c8499968853e7ad3cf4a0d170dc`. Review request #166 required eight corrections. This report records the follow-up validation on 2026-10-12; the original acceptance evidence remains in [acceptance.md](acceptance.md).

## Changes and regression coverage

| Finding | Correction | Regression in `tests/integration/test_review_regressions.py` |
| --- | --- | --- |
| Decimal and abbreviation corruption in oversized paragraphs | Latin sentence boundaries require whitespace; CJK boundaries permit zero-width splitting. Chunks slice the original text. | `test_uploaded_oversized_paragraph_keeps_decimals_and_abbreviations` uploads a real PDF containing `64.8`, `60.0`, and `e.g.` in a paragraph over 500 tokens. |
| Token slicing corrupts Unicode and loses required overlap | Oversized paragraphs split at complete character boundaries, prefer sentence boundaries, and retain approximately 10% overlap. | `test_uploaded_cjk_paragraph_splits_on_characters_with_overlap` uploads a CJK PDF, checks no U+FFFD, bounded Chunks, and 40–50-token shared overlap. |
| Missing production-budget boundary evidence | Test the actual 10,000-token budget and answer prompt cap of 6,700. | `test_real_10k_budget_rejects_prompt_one_token_over_answer_cap` rejects 6,701 raw tokens before the adapter runs and accepts exactly 6,700. `test_real_10k_prompt_cap_failure_is_an_application_error_without_final` verifies application error/no-final/zero-call behavior. |
| Citation variants cannot be clicked | Normalize comma lists and line-suffixed markers across streaming frames; prompt requests adjacent markers. | `test_comma_and_line_suffixed_citations_normalize_across_frames` checks `[C1, C3]` and `【C3†L1-L4】`, final sources, and matching streamed text. |
| Trace loses previous calls | Accumulate all call records, including when a later call is rejected by the guard. | `test_ask_accumulates_traces_from_every_gateway_call`, two parametrized cases. |
| Terminal frame leaves adapter open | Wrap the adapter iterator with `contextlib.aclosing`; its HTTP stream closes when generation exits. | `test_terminal_llm_frame_closes_adapter_before_ask_finishes` checks the adapter's `finally` ran before the operation completed. |
| Duplicated constants and frontend margin | Centralize question limit, Context Budget, safety margin, and Chunk policy. Add backend `safety_margin` to the Trace schema and regenerate TypeScript; UI displays this field. | Existing recorded-call integration assertions check the shared margin. Event-schema parity and browser evidence verify the new field. |
| Unexpected exceptions drop SSE | Both public operations emit a generic error and log internal details. Unexpected LLM failure retains its Trace. | `test_unexpected_upload_exception_emits_generic_error` and `test_unexpected_llm_exception_emits_generic_error_and_trace`. |

Decimal, CJK, Citation, Trace/closure, and unexpected-error regressions reproduced failures before the relevant fixes. The unexpected-error pair was also run against the reviewed application/Gateway files, restoring the working files afterward: both failed with the injected RuntimeError, then passed after the correction. The actual-budget tests strengthen evidence for the existing guard. Corrections and discoveries are recorded in `docs/ai-log.md`.

## Validation

- `uv run pytest -q`: **20 passed in 9.46s**. Real local `bge-m3`; scripted LLM for deterministic assertions. No cloud calls in the suite.
- `uv run ruff check src tests scripts/generate_event_types.py`: passed.
- `uv run ruff format --check src tests scripts/generate_event_types.py`: 22 files already formatted.
- `uv run python scripts/generate_event_types.py --check`: passed.
- `npm run typecheck --prefix frontend`: passed.
- `npm run build --prefix frontend`: passed; rebuilt production asset `index-CSJFhpCJ.js` included.
- `git diff --check`: passed.

## Real browser and cloud recheck

Started FastAPI on 8101, served the rebuilt production frontend, uploaded LightRAG, and asked `Performance of ablated versions of LightRAG` using real `gpt-oss:120b-cloud`. Generation completed with 152 delta events. Clicking C3 opened the source on page 8. Expanding Trace showed the backend-provided safety margin and 10K meter, with no horizontal overflow at 1280×900. The browser reported no uncaught page errors.

| Metric | Value |
| --- | --- |
| Estimated prompt, including margin | 2,075 |
| Backend safety margin | 300 |
| Actual `prompt_eval_count` | 1,850 |
| Output reservation | 3,000 |
| Reserved Context Budget usage | 5,075 / 10,000 |
| Actual `eval_count` | 1,491 |
| Think / completion | medium / stop |
| Latency | 4.49s |

Artifacts: [review-browser-evidence.json](review-browser-evidence.json) contains eight passing assertions and model metrics; [review-trace-viewport.png](review-trace-viewport.png) shows the expanded Trace. The isolated `t01-kava` browser and FastAPI process were stopped. `lsof -nP -iTCP:8101 -iTCP:5101 -sTCP:LISTEN` returned no listeners.

## Scope retained

The follow-up addresses all eight required findings. Truncated-PDF classification remains for #02; clearing the current Document on upload remains for #04. Optional naming suggestions were deferred as requested. This remains the Lookup-only walking skeleton with virtual Sections and raw table text; later tickets own table reconstruction, Golden Facts, routing, and Citation validation/retry.
