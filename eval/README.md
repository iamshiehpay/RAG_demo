# Golden Facts evaluation

Run the real application operations and judge with local Ollama (`bge-m3`) and
`gpt-oss:120b-cloud`:

```sh
uv run pytest -m eval -s
```

This uploads `data/lightrag.pdf`, asks Q1–Q3, a Chinese cost question, a Synthesis
limitations question, three unanswerable questions and the 12 router regression
questions. It also runs two fixed-answer, real-judge semantic probes (affirmative
and negated forbidden claims). Reports are written to `eval/reports/` even when
Golden Facts fail. A failing fact makes the eval test fail after saving the report.
Default `uv run pytest` excludes the `eval` marker and uses scripted LLMs.

```sh
uv run pytest -m eval -s --eval-repeats 3
uv run pytest -m eval -s --eval-cases Q3 --eval-label ablation-experiment
```

Options: `--eval-document PATH`, `--eval-report PATH`, `--eval-label NAME`,
`--eval-cases Q1,Q2,Q3`, `--eval-repeats N` (positive integer, default 1).
`--eval-record-only` records an honest baseline without requiring all facts to
pass; the report still says FAIL for failing facts. It does not certify quality.

```sh
uv run pytest -m eval -s --eval-record-only --eval-label lookup-skeleton \
  --eval-report eval/reports/lookup-skeleton-baseline.md
```

The first baseline uses the unchanged #01 Lookup-only application. Missing
Global/Synthesis routing and history are recorded as failures. #06's exported
`router_regression.CASES` becomes the canonical question source when integrated;
before that, the unchanged `spikes/think_level_probe.py` cases are used. The runner
passes explicit `ConversationTurn` history when `Application.ask` supports it,
and passes an empty history for independent questions. It never changes retrieval
or answer generation.

`GoldenFact` rejects numeric `contains` definitions. Term checks normalize Unicode
hyphens (including U+2011), whitespace, full-width characters and percent spacing.
Numbers always use a semantic judge and numeric evidence anchors; normalizing
percentages is tested separately so numeric substring checks remain forbidden.
Judge calls use the production Gateway's `judge` policy. Requirements about the
answer itself (language or fixed reply) are evaluated as answer properties, not
claims the answer must explicitly make about itself. Each matching claim must
include a nonempty, contiguous, verbatim answer excerpt. Numeric excerpts must
contain the required variant, dataset, metric and values, while the judge checks
assignment and comparison direction. Forbidden claims count only when asserted;
explicit denial is not a violation. Invalid JSON, invented excerpts, failed calls
and truncation fail closed. Fixed refusals follow binding D01 (Chinese or English)
and reject additional invented content.

`RecordingGateway` captures all LLM traces, including ingestion, router, retries,
answers and judges. Reports include every call's estimated prompt tokens, actual
`prompt_eval_count`, `eval_count`, output reservation, Context Budget, think,
latency and `done_reason`. Missing counts remain `None`; they are not fabricated.
Each fact has a per-run result/evidence and an N-run pass rate. Only final events
supply answers; provisional content from failed requests is never judged.

To add another Document's Golden Facts (#10), create `EvaluationCase` definitions
and call `run_evaluation(application, gateway, document_path, cases, repeats=N)`,
then `write_report(report, path)`. The application and judge must share the
`RecordingGateway` so the report accounts for all calls.

`lookup-skeleton-initial.md` preserves an initial checker-prompt defect (correct
Chinese/fixed-reply properties were mistaken for self-asserted factual claims).
`lookup-skeleton-baseline.md` supersedes it after the checker regression fix.
`lookup-q3-n3.md` records three real Q3 runs at the original harness checkpoint.
`lookup-skeleton-property-intermediate.md` records the next probe, which identified
that the judge also needed the explicit expected fixed sentence. The final baseline
supplies it; `refusal-checker-probe.md` verifies all three refusals with the real LLM.
The N=3 report includes one truncated Judge call, marked as a failed fact; this is
not an answer-generation success claim.
