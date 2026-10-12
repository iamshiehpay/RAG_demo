# Live Router QA follow-up #1672

Base: integrated main `79aac57`. Date: 2026-10-13 (Asia/Taipei).

The original scripted tests hid a live defect: Ollama Cloud ignored the `format` contract and
the prompt did not name all three JSON keys. Most real responses therefore fell back to Lookup,
even when the model identified Synthesis in its thinking. The corrected Router now explicitly
names the keys and allowed values, shows a minimal example, distinguishes ablation/table Lookup
from cross-Section comparisons, and requests a short plan rather than an answer. Schema `format`
is still sent. Router remains `think=low`, `num_predict=600`; no budget was increased.

## Parsing and observable failures

- The known `type` alias is accepted, extra `answer` / `answer_format` fields are ignored, and
  absent Sub-queries normalize to an empty list. Classification and valid rewrites survive.
- Missing/blank Standalone Question defaults to the original question only without history.
  With history it is a failed plan, recorded as `missing_rewrite`.
- Failed plans use visible Lookup fallback with `plan_source=fallback` and a reason:
  `invalid_json`, `invalid_plan`, `missing_rewrite`, or `length`. Genuine Router Lookup has
  `plan_source=router`, `fallback_reason=null`. Both the plan event and Router call Trace carry
  this metadata; the Trace UI displays the plan source and any fallback reason.
- Nine exact raw outputs from `router-probe-q2.txt` / `router-probe-others.txt` are preserved in
  `tests/integration/data/router_qa_raw.json` with source filename/line. The 12-case probe only
  recorded key names, so additional shape tests reconstruct those cases without claiming they
  are verbatim outputs. Missing rewrites with history, answer-only objects and extra keys are
  covered by deterministic tests. The first five origin tests failed before implementation.

## The 600-token Q3 hit

The old trace had `think=low`, `prompt_eval_count=934`, estimated prompt 1,259 including safety,
and `eval_count=600`, `done_reason=length`. This was not a prompt-budget overflow. QA did not
capture partial Router content or complete thinking, so the split between thinking and JSON
tokens cannot be recovered and no exact token-level cause is claimed. The old prompt was
underspecified and treated ablation performance as decomposition across Sections; direct old
Q3 probes produced four long Sub-queries. The new prompt explicitly routes a table's ablation
results to Lookup and bounds the requested JSON. Both new live checks terminate within the
unchanged reservation: the browser Q3 Router uses **63 output tokens**, `stop`, despite a larger
1,244-token model-reported prompt with two rounds of history.

## Live verification

`uv run pytest -q -m eval tests/integration/test_router_smoke_eval.py`: **1 passed in 14.27s**.
The canonical 12 `router_regression.CASES` yield **12/12 correct Question Types**, **zero parse
fallbacks**, **zero length fallbacks**, and **52–179 generated tokens** per call. Both history
cases resolve LightRAG; Chinese/English question language is retained. Raw JSON, plans, thinking,
token counts and latency are saved in [live-router-smoke.json](live-router-smoke.json).
Default pytest excludes this test with the `eval` marker. A fallback Lookup cannot count as a
correct classification in the smoke report. #08 was notified of the additive event/Trace fields;
Router.plan and CASES tuple interfaces remain unchanged.

The browser used real local bge-m3 and real `gpt-oss:120b-cloud`, serving the rebuilt frontend at
`http://127.0.0.1:8120` through a temporary recording Application. The recorder only saves emitted
events; it does not alter planning, retrieval or generation.

| Input | Live plan and evidence | Router output |
| --- | --- | --- |
| Compare LightRAG with GraphRAG | Synthesis; three method/cost/update Sub-queries; retrieved original cost paragraph containing `610` and incremental-update paragraphs | 82 tokens, stop |
| 那它的成本呢？ | Lookup; rewritten as `LightRAG和GraphRAG的成本是多少？`, in Chinese, with named referents | 89 tokens, stop |
| Performance of ablated versions of LightRAG | Genuine Lookup; no Sub-queries or fallback, original table evidence retrieved | 63 tokens, stop |

Complete event tapes: [Q2](live-browser/ask-1.json), [follow-up](live-browser/ask-2.json),
[Q3](live-browser/ask-3.json). Screenshots: [Q2 Trace](live-browser/q2-trace.png),
[follow-up Trace](live-browser/followup-trace.png), [Q3 Trace](live-browser/q3-trace.png).
Screenshots were visually inspected; no browser errors were reported. These checks establish
Router and retrieval behavior, not Golden Facts answer quality; table reconstruction remains #03.

An earlier valid Q2 plan used a broad cost query and retrieved only the Table 3 caption. The
retrieval-system comparison instruction now explicitly names token/API-call cost and incremental
updates; the final live evidence includes the cost paragraph. Earlier rewrite instructions also
allowed an English-history follow-up to remain English or retain a pronoun. The prompt now
specifies named referents and adds a language reminder to the current question; the smoke asserts
these properties instead of accepting schema-valid JSON alone.

## Final checks

- `uv run pytest -q`: **61 passed, 1 eval deselected, 6 existing deprecation warnings, 65.45s**.
- Scoped ruff check and format (`src tests scripts/generate_event_types.py`): PASS, 30 files.
- Generated backend/frontend event parity, frontend typecheck and production build: PASS.
- `git diff --check`: PASS. Updated `frontend/dist/` is included in the fix commit.
- The isolated browser and backend were stopped; no Vite process was started.
