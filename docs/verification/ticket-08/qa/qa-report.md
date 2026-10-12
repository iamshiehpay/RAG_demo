# QA report: ticket #08 Eval harness and Golden Facts

Model: claude-sonnet-5-5. Tree: main checkout at 11968fd (HEAD moved to f38cf47 during QA; that diff is EXECUTION.md only).
Method: independent probes with scripted judges, one live run of the documented command (cloud calls), and a read of the committed baseline and runner code.

## Summary

PASS 18, FAIL 0, UNPROVEN 3, NOT_EXECUTED 3 (the latter belong to other tickets).
The harness did not misjudge in any case I checked. The Golden-Fact failures in the live runs are answer-quality failures (retrieval and answering belong to other tickets) and are expected at this stage.

## 1. Deterministic

- `uv run pytest -q`: 110 passed, 2 deselected, 95s. Eval is excluded by `addopts = "-m 'not eval'"`.
- `uv run pytest -m eval --collect-only -q`: 2 of 112 collected, both live: `eval/test_live.py::test_golden_facts_live` and `tests/integration/test_router_smoke_eval.py`.
- Checker unit tests (`tests/unit/test_eval_*.py`, `tests/integration/test_eval_runner.py`) are in the 110 passed.
- My own probe, `probe-output.txt` (script: scratchpad/probe.py), was run with fake judges:
  - A "-High 64.8" answer does not satisfy the Mix `-Low` fact (FAIL, context missing). The same holds for the Agriculture `-Origin` fact.
  - Wrong direction, wrong dataset and a missing metric all FAIL.
  - Invented judge evidence FAILs ("not a nonempty verbatim excerpt").
  - A forbidden claim that is asserted FAILs. A negated claim PASSes, as does a judge answer with matched=false.
  - `GoldenFact("x","contains","64.8")` and `"67.6%"` raise ValueError.
  - Cost equivalence: "610 x 1,000", "610,000" and the Chinese form all PASS. "610k" and "61 萬" FAIL.
  - Refusals: the exact `FIXED_REFUSALS` sentence PASSes, with or without one final period. The refusal plus extra content FAILs, and the wrong language FAILs.

## 2. Golden Facts fidelity (eval/golden_facts.py vs AGENTS.md)

I checked the Table 1 and Table 2 numbers against `data/lightrag.pdf`.

| AGENTS item | Harness | Verdict |
|---|---|---|
| Q1 six topics | motivation, graph_indexing, dual_level, incremental_update, experiments, conclusion | Match |
| Q1 forbidden | `NOT_ALL_BEST` is also attached to Q1 | Stricter than AGENTS, which lists forbidden only for Q2 and Q3. Low risk. |
| Q2 retrieval, cost, incremental update, Table 1, Table 3, forbidden | All present | Match |
| Q2 Table 1 | Split into 4 per-dataset Overall facts: Agri 54.8/45.2, CS 52.0/48.0, Legal 52.8/47.2, Mix 49.6/50.4 | Values match the PDF. Stricter than AGENTS, which gives only the Mix numbers. |
| Q2 cost: 610x1,000, <100 tokens, 1 API call | Anchors `610`, `100`, `API` are required literally in the evidence | Stricter. "610k", "61 萬" and "一次呼叫" without "API" FAIL even if the meaning is right (documented in eval/README.md). 610,000 is accepted. |
| Q2 forbidden "wins on all datasets" | `not_all_datasets` | Match |
| Q3 `-Origin` term and Table 2 baseline | `-High`, `-Low`, `-Origin` terms, `table2_baseline`, `ablation_meaning`, citation check | Match, plus extras |
| Q3 Mix `-Low` 64.8 vs 60.0, Agri `-Origin` 74.4 vs 67.6 | Matches the PDF. Variant-to-value binding is enforced per clause or table column. | Match |
| Q3 forbidden | `NOT_ALL_BEST` | Match |
| Absent answers, 3 questions | HotpotQA (zh), license (en), GPU hours (zh). Checked deterministically against `FIXED_REFUSALS`. | Match. The English question requires the English fixed sentence (AGENTS says answer in the question's language). |
| Router 12 questions | `router_regression.CASES`, each question verbatim in `spikes/think_level_probe.py` | Match |
| Gap 7 Chinese and limitations | `ZH_COST` and `LIMITATIONS` exist | Present |

Looser or stricter notes:
- `contains` is a plain substring check on normalized text. "NaiveRAG-High" counts as "-High".
- `contains` rejects any requirement containing a digit, so even "Table 2" is rejected. Harmless.
- No eval case exists for the test-list row QA-02 ("三句話、中文總結"). It belongs to #05 and #08 and is not required by the #08 ticket text.

## 3. Live run (documented command)

```
uv run pytest -m eval -s --eval-record-only --eval-repeats 3 \
  --eval-cases Q3,ABSENT_HOTPOT,ABSENT_LICENSE,ABSENT_GPU \
  --eval-label qa-08 --eval-report eval/reports/qa-08-q3-absent-n3.md
```

I also ran Q2, ZH_COST and LIMITATIONS once and wrote `eval/reports/qa-08-q2-zh-limits.md`.

Report contents:
- Per-fact pass/fail rows are present.
- N=3 pass rates appear in the "Per-fact pass rates" table. For example, Q3 `high_term` is 3/3, `low_term` is 0/3, and the three absent cases are 3/3.
- Every call shows estimated_prompt_tokens, prompt_eval_count, eval_count, num_predict, context_budget, latency_ms and done_reason.
- Ask latency, judge latency and total latency are listed separately per run.
- I parsed all 45 calls in the Q3 and absent report. The maximum estimated prompt plus num_predict is 5,388, so none is over 10K. There are no `length` done_reasons. The estimate is always at least prompt_eval_count.
- The "Upload LLM calls" table is empty, as expected before #05.

Spot checks of judge verdicts, which I confirmed by reading the answers:
1. Q2 `not_all_datasets` (forbidden) FAILed. The judge quoted "LightRAG consistently outperforms GraphRAG on the four evaluation dimensions...". The quote is verbatim and the answer does assert universal superiority, so the verdict is right.
2. ZH_COST `retrieval_cost` PASSed. The evidence is verbatim: "610 個二層社群...總計約 610,000 個 token ... 不到 100 個 token ... 一次 API 呼叫". The 610,000 equivalence and the semantics are correct.
3. Q3 `mix_low_overall` and `ablation_meaning` FAILed because the answer never mentions `-Low` or `-Origin`. Correct. `table2_baseline` FAILed because the answer labels full-LightRAG numbers as "ablated". Defensible.
4. Judge probes `JUDGE_ASSERTED` and `JUDGE_NEGATED` were 3/3 in the Q3 run and 1/1 in the Q2 run. Both semantic outcomes were correct.

## 4. router-provenance-baseline.md and fallback scoring

- The report shows 12 router cases. All 12 classify correctly with plan_source=router, and there are no fallbacks.
- ROUTER_11 and ROUTER_12 `standalone_rewrite` both PASS, with rewrite_language_mismatch=False.
- Runner code: `question_type` passes only if `plan_source=="router"` and the type matches. A fallback is marked `fallback=True` and shows as FALLBACK. Missing provenance fails closed. `standalone_rewrite` also requires `not rewrite_language_mismatch`. `tests/unit/test_eval_plan.py` covers all of this and passes.
- This closes #06 AC7.
- The committed baseline does not include ZH_COST, LIMITATIONS or ABSENT. Those are only in the superseded Lookup-only reports and in my qa-08 reports.

## 5. Verdicts

Acceptance criteria:
- AC1, one command and a markdown report: PASS.
- AC2, deterministic checks (invented evidence, U+2011 and "67.6 %", `-High` 64.8 not satisfying `-Low`): PASS.
- AC3, per-call tokens and latency, and N=3 rates: PASS.
- AC4, committed baseline with honest results: PASS (`Result: FAIL` is recorded).

Gaps:
- Gap 7 Chinese and limitations eval items: PASS in code. Live 1x run: ZH_COST 4/4. LIMITATIONS ran, with quality failures that are not a harness problem.
- Gap 9 numeric `contains` rejected: PASS.
- Gap 9 negation-safe forbidden: PASS.
- Gap 9 eval excluded from default pytest: PASS.
- `rewrite_language_mismatch` scoring: PASS.
- 610,000 equivalence: PASS. The 610k and "一次呼叫" forms are an intentional limitation.

Mapped test-list rows:
- EV-01, EV-02, EV-03, EV-04, RT-02 and QA-08 (ROUTER_11/12): PASS.
- BG-03: PASS for the fields (the harness reports them).
- QA-01, QA-03, QA-04, QA-05: PASS as harness definitions. Answer quality is out of scope here. Q1 runs on the transitional path until #05.
- EV-05: partly UNPROVEN. The default exclusion is PASS, but I did not test the message when Ollama is down.
- UNPROVEN:
  - The Ollama-down message in EV-05.
  - QA-02, because no eval case exists for it.
  - TR-04, the highest-similarity trace, which I did not examine.
- EV-06 (#11), D2-03 (#10) and QA-06/QA-07 as full verdicts: NOT_EXECUTED. QA-06 and QA-07 are covered only by the harness cases.

Observations, none of them FAILs:
- `-m eval` also runs `tests/integration/test_router_smoke_eval.py`. It ignores `--eval-cases`, adds about 40 seconds, and writes an untracked `eval/reports/router-smoke-*.json` on every run. I moved my two to this directory.
- When the judge returns matched=false, its reasoning is not recorded, so some FAIL rows give little context.
