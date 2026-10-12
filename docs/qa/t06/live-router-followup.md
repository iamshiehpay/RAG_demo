# Router live QA and evaluation-validity repair

Base: integrated main `79aac57`. Date: 2026-10-13 (Asia/Taipei).

Review #1974 found that the earlier repair (`f9f1651`) taught Q2 and other regression labels in
its prompt. Its 12/12 score and targeted cost/update retrieval were tuned regression results,
not evidence of generalisation. The prior report [live-router-smoke.json](live-router-smoke.json)
is retained as historical evidence; the smoke no longer overwrites it.

The current prompt has no LightRAG/RAG names, ablation/dataset examples, token/API-call query
instructions, or Golden Fact topics. It uses generic scope rules: one table/figure result is
Lookup; comparisons may cover mechanisms, costs, maintenance/update aspects. The JSON example
is rail versus sea freight. An initial neutral solar/wind example overlapped one new follow-up's
domain, so the example changed to freight while all eight new questions and labels stayed fixed.
No held-out error was used to change a question or label. Both neutral runs are retained below.

## Parsing, metadata and budget

The parser fixes confirmed by review remain: the known `type` alias and extra keys are tolerated;
valid classification/rewrite survives. Missing rewrite defaults to the question only without
history; with history it records `missing_rewrite`. Failed plans are visible Lookup fallbacks.

Both PlanEvent and Router LLMCallTrace carry `plan_source` and `fallback_reason`. The latter is
now a Literal union of `length`, `invalid_json`, `invalid_plan`, `missing_rewrite`, or null, also
reflected in regenerated TypeScript. Genuine Router Lookup is `router`/null. Trace displays
origin and any reason. Router still uses `think=low`, `num_predict=600`; the budget was not raised.
Nine exact old probe outputs plus reconstructed key-only shapes remain deterministic fixtures.

## Corrected Q3 evidence

The old QA trace has `prompt_eval_count=934`, estimated prompt 1,259 including safety,
`eval_count=600`, `done_reason=length`. It contains the **full** Router thinking:
`Need to answer synthesis: compare ablated versions. Provide subqueries.`
This is 14 `o200k_harmony` tokens, so roughly 586/600 output tokens were content. Long/runaway
JSON/Sub-queries are the likely cause, rather than excessive thinking. Partial JSON was not
captured, so its exact form is unknown. The previous claim that thinking was incomplete was
wrong and is corrected here and in ai-log. The small prompt did not exceed its budget.

## Live smoke

`uv run pytest -q -s -m eval tests/integration/test_router_smoke_eval.py`: **1 passed in 20.99s**.

| Set | Genuine correct types | Fallbacks | Rewrite/script failures | Generated tokens |
| --- | --- | --- | --- | --- |
| Canonical CASES | 12/12 | 0 | 0 | 75–160 |
| Eight held-out questions | 8/8 | 0 | 0 | 91–184 |

The held-out set mixes Chinese/English, all three types, and weather-sensor/energy follow-ups.
Its cases are absent from CASES and the final prompt. These are small, single-run validation
samples; the browser results below show they do not cover all history-dependent behavior.

Current report: [freight-example smoke](../../../eval/reports/router-smoke-20261012T162145462813Z.json).
Earlier exploratory neutral run: [solar-example smoke](../../../eval/reports/router-smoke-20261012T161722133754Z.json).
Reports include the actual prompt, raw JSON, history, expected labels, plans, rewrite checks,
thinking, tokens and latency. Each run uses a repository-root-resolved timestamped path under
`eval/reports/`, created exclusively; running from another cwd cannot overwrite committed docs.

The follow-up guard requires the historical topic, not just an entity already in the question:
canonical case 11 must contain cost/API-related terms. It returned `LightRAG 的檢索成本是多少？`.
Dev-only OpenCC s2t flags Simplified-to-Traditional changes, including `检索成本`; shared or
ambiguous characters are inconclusive. Three deterministic tests through Router prove that a
name-only follow-up and Simplified rewrite fail the guard while a complete Traditional rewrite
passes. Smoke is excluded from default pytest. Existing addopts/markers are preserved for #08.

## Browser: remaining acceptance failures

Real local bge-m3 and real gpt-oss served the rebuilt frontend at `http://127.0.0.1:8120`.
The temporary Application records emitted events without changing execution.

| Check | Final neutral result | Status |
| --- | --- | --- |
| Q2 type/Sub-queries | Genuine Synthesis; architecture, performance, limitations/maintenance queries; 103 Router tokens, stop | PASS |
| Q2 required retrieval | Neither the paragraph containing `610` nor incremental-update passages appear in retrieved evidence | **FAIL** |
| Follow-up `那它的成本呢？` | Lookup; `LightRAG 的成本是多少？` in Traditional Chinese; 78 Router tokens, stop | PASS |
| Q3 after these two rounds | Synthesis rather than Lookup; English input rewritten as `LightRAG 的消融版本的性能如何？`; 134 tokens, stop, no fallback | **FAIL type/language**, PASS completion/budget |

The first solar-example browser run found incremental-update text but missed cost. The final
freight-example run missed both; these results were reported to Levi without restoring
Golden-Fact-specific prompt instructions. The direct canonical Q3 has no history and passes,
but the actual browser history context does not. Overall browser acceptance remains **FAIL**;
the 20-case smoke score is not substituted for these failed checks. Golden Facts answer quality
is not accepted by this repair.

Current event tapes: [Q2](live-browser/ask-1.json), [follow-up](live-browser/ask-2.json),
[Q3](live-browser/ask-3.json). Inspected screenshots: [Q2](live-browser/q2-trace.png),
[follow-up](live-browser/followup-trace.png), [Q3](live-browser/q3-trace.png).
No browser errors were reported. Browser/backend were stopped; no Vite process was started.

## Final deterministic checks

- `uv run pytest -q`: **64 passed, 1 eval deselected, 6 existing warnings, 67.49s**.
- Scoped ruff check/format (`src tests scripts/generate_event_types.py`): PASS, 31 files.
- Event type parity, frontend typecheck/production build and `git diff --check`: PASS.
- Frontend build is unchanged: the Literal refinement only changes generated source types.
