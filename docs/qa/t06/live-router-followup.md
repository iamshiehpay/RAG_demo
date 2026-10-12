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

## Browser: original neutral-prompt failures

Real local bge-m3 and real gpt-oss served the rebuilt frontend at `http://127.0.0.1:8120`.
The temporary Application records emitted events without changing execution.

| Check | Final neutral result | Status |
| --- | --- | --- |
| Q2 type/Sub-queries | Genuine Synthesis; architecture, performance, limitations/maintenance queries; 103 Router tokens, stop | PASS |
| Q2 required retrieval | Neither the paragraph containing `610` nor incremental-update passages appear in retrieved evidence | **FAIL — deferred to #11** per Levi #2066; not a #06 blocker |
| Follow-up `那它的成本呢？` | Lookup; `LightRAG 的成本是多少？` in Traditional Chinese; 78 Router tokens, stop | PASS |
| Q3 after these two rounds | Synthesis; English input rewritten as `LightRAG 的消融版本的性能如何？`; 134 tokens, stop, no fallback | **FAIL language**, PASS completion/budget; Synthesis accepted by Levi #2066 under the ambiguity rule |

The first solar-example browser run found incremental-update text but missed cost. The final
freight-example run missed both; these results were reported to Levi without restoring
Golden-Fact-specific prompt instructions. The direct canonical Q3 has no history and passes,
but the actual browser history context did not preserve language. These failures remain
historical evidence; the language repair below supersedes that #06 failure. The 20-case smoke
score is not substituted for the browser checks. Golden Facts answer quality is not accepted
by this repair; live Q2 retrieval tuning waits for real Sections and neighbor/table links in #11.

Current event tapes: [Q2](live-browser/ask-1.json), [follow-up](live-browser/ask-2.json),
[Q3](live-browser/ask-3.json). Inspected screenshots: [Q2](live-browser/q2-trace.png),
[follow-up](live-browser/followup-trace.png), [Q3](live-browser/q3-trace.png).
No browser errors were reported. Browser/backend were stopped; no Vite process was started.

## Prior deterministic checks

- `uv run pytest -q`: **64 passed, 1 eval deselected, 6 existing warnings, 67.49s**.
- Scoped ruff check/format (`src tests scripts/generate_event_types.py`): PASS, 31 files.
- Event type parity, frontend typecheck/production build and `git diff --check`: PASS.
- Frontend build is unchanged: the Literal refinement only changes generated source types.

## Current-question language repair (#2066)

Answer Generator now receives the current user question independently of the Standalone
Question. Its prompt explicitly gives the current question control over answer language;
Context Packer uses exactly the same messages for selection and recursive capacity checks.
The added language reference is counted, including when a long current question would make
an otherwise fitting context exceed the prompt cap.

When the Router rewrite switches between Chinese and non-Chinese script, the backend retains
Question Type, plan source and Sub-queries, uses the current question for retrieval, and records
`rewrite_language_mismatch=true` plus `router_standalone_question` in both plan and call Trace.
The UI displays the warning and raw rewrite. No second Router call or translation is used.
A dependent follow-up can lose its resolved reference when the current question replaces the
rewrite; the explicit flag exposes this limitation. Languages sharing a script are not detected.

Four new deterministic cases first failed, then passed: both cross-script directions with one
Router call and preserved type; Chinese history + English Q3 with an English language reference;
and a context that only exceeds capacity after the current-question reference is counted.
Older tests that expected English rewrites of Chinese questions now use same-language fixtures
for their original purpose, or explicitly assert the flag and retained raw rewrite.

The live browser sequence used real bge-m3 and gpt-oss again: Q2 → `那它的成本呢？` → English Q3.
The prior event tapes above were preserved; new events are in a separate directory.

| Check | New live result | Status |
| --- | --- | --- |
| Chinese follow-up | Lookup, `LightRAG 的成本是多少？`; 72 Router tokens, stop | PASS |
| Q3 standalone/type | `What is the performance of ablated versions of LightRAG?`; genuine Synthesis, 95 Router tokens, stop | PASS; Synthesis accepted |
| Q3 answer language | English answer, no Chinese characters; 1,498 generated tokens, stop | PASS |
| Q3 call budgets | Router 1,814/10,000, answer 4,820/10,000 estimated + reservation | PASS |

This live run did not trigger the mismatch branch; the deterministic tests force that failure
and verify its recorded correction. It proves the original browser history sequence now
answers in English, not that every future model rewrite will be valid. Answer/table accuracy
remains outside this repair's acceptance claim.

New event tapes: [Q2](language-browser/ask-1.json), [follow-up](language-browser/ask-2.json),
[Q3](language-browser/ask-3.json). The inspected [Q3 screenshot](language-browser/q3-trace.png)
shows the English answer and expanded Router Trace budget. Browser errors: none. The task's
browser and backend were stopped; no Vite process was started.

Final checks: **68 passed, 1 eval deselected, 6 existing warnings, 66.74s**; ruff check/format
(32 files), generated event parity, frontend typecheck/build and `git diff --check` pass.
The frontend was rebuilt and its changed `dist/` is included.

## Traditional/Simplified answer-script repair (#2269)

The branch fast-forwarded to main `b005721` before this repair. Independent QA had all seven
live #06 checks passing, but found a Simplified Chinese answer to `那它的成本呢？` despite
a Traditional/shared-character current question. The previous instruction specified language,
without explicitly preserving its Chinese script.

The production change is six lines in `answer_messages`: use Router's existing CJK detection
and append the current-question Traditional/Simplified preservation rule, defaulting ambiguous
shared characters to Traditional Chinese. Number-preservation instructions remain unchanged.
Context Packer already counts these exact messages, so this new rule is budgeted automatically.
No production converter, extra call, Router rule, event contract or frontend behavior changed.

Three prompt tests initially failed, then passed (Traditional, Simplified and the exact shared-
character follow-up). An English current question does not inherit the rule from a Chinese
rewrite. The dev-only recorded-answer check uses OpenCC in the existing smoke module; the
20-case Router smoke has no answers and therefore gains no answer calls. It flags the prior
independent QA answer, but the repeated browser answer passes. An observed false positive
(`群` → `羣`, both Traditional) was reproduced in a failing test and corrected by normalizing
Traditional variants with `t2tw` for comparison. Actual answers are never converted.

Live browser: upload LightRAG → Q2 → `那它的成本呢？`, once, using real bge-m3 and gpt-oss.
The answer contains `檢索階段`, `個 token`, `實體與關係`, and `社群結構`, and passes the
dev-only script check. Router returned genuine Synthesis with a named LightRAG rewrite,
163 tokens/stop. The answer used 363 tokens/stop. Estimated + reserved budgets were
1,719 and 4,626 / 10,000. Raw Sub-query text is retained, including model-generated Simplified
characters; this repair targets the answer. The screenshot was inspected; browser errors: none.
Browser/backend stopped; no Vite process. Golden Facts quality remains deferred.

Evidence: [Q2 events](script-browser/ask-1.json), [follow-up events](script-browser/ask-2.json),
[OpenCC check](script-browser/script-check.json), [browser screenshot](script-browser/followup.png).

Final checks: **76 passed, 1 eval deselected, 6 existing warnings, 112.20s**. Ruff check/format,
generated event parity, frontend typecheck/build and `git diff --check` pass. The frontend build
is unchanged. The smoke answer helper checks recorded answers without adding Cloud calls.
