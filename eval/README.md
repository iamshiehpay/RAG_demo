# Golden Facts evaluation

中文操作入口見 [開發與評估指南](../docs/development.md)。較新的 N=3 評估與失敗分析見 [issue11-correction 結論](reports/issue11-correction/conclusions.md)；下方 baseline 名稱描述各開發階段，不代表目前所有程式版本都已重新評估。

Run the application operations and Judge with local Ollama (`bge-m3`) and
`gpt-oss:120b-cloud`:

```sh
uv run pytest -m eval -s
```

This uploads `data/lightrag.pdf` and asks Q1–Q3, a three-sentence Chinese Global summary, a Chinese cost question, a
Synthesis limitations question, three unanswerable questions and the 12 Router
regression questions. Reports go to `eval/reports/` before asserting the Golden
Facts result. Default `uv run pytest` excludes live eval and uses scripted LLMs.
Two real-Judge semantic probes are reported separately and never affect the
Golden Facts PASS/FAIL or its per-fact rates.

```sh
uv run pytest -m eval -s --eval-repeats 3
uv run pytest -m eval -s --eval-cases Q3 --eval-label ablation-experiment
```

Options: `--eval-document PATH`, `--eval-report PATH`, `--eval-label NAME`,
`--eval-cases Q1,Q2,Q3`, `--eval-repeats N` (positive integer, default 1).
`--eval-record-only` saves failures without requiring all facts to pass; the
report still says FAIL. It does not certify answer quality.

```sh
uv run pytest -m eval -s --eval-record-only --eval-label router-provenance \
  --eval-report eval/reports/router-provenance-baseline.md
```

The integrated harness uses #06's canonical `router_regression.CASES` directly,
converts role/content pairs to `ConversationTurn` history, and supplies empty
history for independent questions. Evaluation history does not change session
history. Global uses the best-fitting complete Summary Tree level and performs no Chunk retrieval.
Select `--eval-cases Q1,Q1_ZH_THREE_SENTENCES` for summary coverage, language and format. Git provenance falls back to `unknown` for zip
delivery. Historical Lookup-only reports describe the earlier #01 application.

Classification passes only for `PlanEvent.plan_source="router"` and the expected
Question Type. A fallback Lookup never earns a classification pass; its fact row
shows `FALLBACK`, and each run records `fallback_reason`. Missing provenance fails
closed. Follow-up checks replace the old “history accepted” check: the Standalone
Question must differ from the input and resolve the canonical referents/context.
`rewrite_language_mismatch=True` fails the follow-up rewrite check, even when
the visible question contains the expected terms. Reports show the flag and
`router_standalone_question` so the raw mismatched rewrite remains reviewable.
`router_regression.FOLLOW_UP_STANDALONE_TERMS` defines case 11's LightRAG retrieval
cost and case 12's LightRAG/GraphRAG comparison. Report headers state this policy.

`GoldenFact` rejects numeric `contains` definitions. Term matching normalizes
Unicode hyphens, whitespace, full-width characters and percent spacing. Judge
excerpts must occur in the answer after normalizing typographic hyphens and
whitespace (including markdown hard breaks, U+202F and NBSP); words, case,
punctuation and Citation markers remain required. Invented text still fails.
Numeric facts require model/variant, dataset, metric and value context plus
variant/value association in the same clause/row or corresponding table column.
Full `LightRAG` does not match `LightRAG-High`. The Judge checks meaning and
comparison direction. Variant anchors accept standalone `-Low`/`-Origin`,
compound `LightRAG-Low` (including Unicode hyphens), and spaced `LightRAG Low`
or `LightRAG -Low`. Integer percentages may omit `.0` (`60%` equals `60.0%`).
Table 1 is checked separately for each dataset. Q3 requires a used Citation
resolving to the matching Table Chunk when `kind="table"` / `table_label`
metadata is available. Until #03 supplies that metadata, it falls back to a
Chunk on p.8 or containing `Table 2`; this fallback does not prove table structure.

The COST fact fails closed on shorthand or omitted terminology: its excerpt must
include the numeric anchor `610` (as in `610 × 1,000` or `610,000`) and literal
`API`. Equivalent `610k`/`61萬` or “one call”/“一次呼叫” without `API` currently
fail the deterministic anchors even if the Judge recognizes the correct meaning.

Forbidden claims fail only when asserted; negations and quotations of the wrong
claim do not count. Judge JSON, transport or truncation failures fail closed.
BudgetExceeded is labeled `HARNESS_BUG` (an upstream arrangement bug), separate
from ordinary answer-quality failure. Fixed refusals are checked deterministically
against `policy.FIXED_REFUSALS`, tolerating one final period/。 and rejecting extra
content. They never call a Judge.

`RecordingGateway` captures all LLM traces, including ingestion, Router, retries,
answers and Judges. Reports include estimated/actual prompt tokens, eval_count,
output reservation, Context Budget, think, latency and done_reason for every call.
Each question separately reports ask latency (embedding/LLM/application), Judge
call latency and total evaluation latency. Only final events supply answers;
provisional text from failed operations is never judged.

For #10, define `EvaluationCase`/`GoldenFact` values and call
`run_evaluation(application, gateway, document_path, cases, repeats=N)`, then
`write_report(report, path)`. Share the `RecordingGateway` between the application
and Judge so all calls are accounted for.

## Report provenance

`router-provenance-baseline.md` is the historical #06 baseline for Q1–Q3 and the 12
canonical Router cases, collected after review request #1785 and integration
of #06's provenance/parser fix from committed source with clean provenance. Every earlier
report below is **superseded** and preserved only as measurement/history evidence:

| Report | Why superseded |
|---|---|
| lookup-skeleton-initial.md | Language/refusal properties were treated as self-asserted facts. |
| lookup-skeleton-property-intermediate.md | Judge lacked the exact expected refusal sentence. |
| lookup-skeleton-refusal-intermediate.md | Judge falsely treated an exact refusal as a forbidden assertion. |
| lookup-skeleton-prereview.md | Pre-review whitespace check, overly broad Table 1 fact and other findings. |
| lookup-skeleton-baseline.md | Clean post-#1370 Lookup-only measurement; predates compound-variant fix and #06 integration. |
| router-integrated-baseline.md | Pre-provenance #06 measurement incorrectly credited fallback Lookup and only checked history acceptance. |
| lookup-q3-n3.md | N=3 evidence at the original harness checkpoint; includes one failed truncated Judge call. |
| refusal-checker-probe.md | Older successful real refusal probe; refusals now use deterministic checks. |
