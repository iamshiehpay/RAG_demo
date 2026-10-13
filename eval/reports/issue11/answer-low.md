# Golden Facts evaluation

Created: 2026-10-13T11:02:49.471210+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Functional operations: PASS (separate from D05 semantic rates)

Call audit: {&quot;budget_violations&quot;: 0, &quot;calls&quot;: 18, &quot;length_attempts&quot;: [], &quot;maximum_estimated_prompt_plus_reservation&quot;: 7377, &quot;maximum_reported_prompt_plus_reservation&quot;: 7152, &quot;missing_reported_prompt_counts&quot;: 0, &quot;router_answer_length_attempts&quot;: 0}

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 7cf91851f9f86527d69c95910f9eadd58cf7b357

Uncommitted changes: yes

Pipeline version: ingest-v2-d6cc86232977edb2c4cd1a1e6fd3deb5755d2b0e85e3a858d999fd23b1e62058

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Created: 2026-10-13T11:02:49.470185+00:00

Label: answer-think-low

Effective settings: {&quot;answer_think&quot;: &quot;low&quot;, &quot;bm25_weight&quot;: 0.0, &quot;chunk_token_target&quot;: 800, &quot;lookup_top_k&quot;: 5, &quot;sub_query_top_k&quot;: 2, &quot;summary_concurrency&quot;: 4, &quot;synthesis_top_k&quot;: 3}

Peak guarded calls by type: {&quot;router&quot;: 1, &quot;answer&quot;: 1, &quot;judge&quot;: 1}

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q2 | question_type | events | 1/1 (100.0%) |
| Q2 | retrieval_methods | judge | 0/1 (0.0%) |
| Q2 | retrieval_cost | judge | 0/1 (0.0%) |
| Q2 | incremental_update | judge | 0/1 (0.0%) |
| Q2 | table1_agriculture_overall | judge | 0/1 (0.0%) |
| Q2 | table1_cs_overall | judge | 0/1 (0.0%) |
| Q2 | table1_legal_overall | judge | 0/1 (0.0%) |
| Q2 | table1_mix_overall | judge | 0/1 (0.0%) |
| Q2 | table3_case_study | judge | 0/1 (0.0%) |
| Q2 | not_all_datasets | forbidden | 0/1 (0.0%) |
| Q3 | required_source_citation | events | 1/1 (100.0%) |
| Q3 | question_type | events | 0/1 (0.0%) |
| Q3 | high_term | contains | 1/1 (100.0%) |
| Q3 | low_term | contains | 1/1 (100.0%) |
| Q3 | origin_term | contains | 1/1 (100.0%) |
| Q3 | table2_baseline | judge | 0/1 (0.0%) |
| Q3 | ablation_meaning | judge | 0/1 (0.0%) |
| Q3 | mix_low_overall | judge | 0/1 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/1 (0.0%) |
| Q3 | not_all_best | forbidden | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG architecture vs GraphRAG architecture&#x27;, &#x27;LightRAG vs GraphRAG performance and scalability&#x27;, &#x27;LightRAG and GraphRAG maintenance and update requirements&#x27;]

Ask latency_ms: 23248.06

Judge latency_ms: 61969.99

Total evaluation latency_ms: 85280.23

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer discusses win‑rate comparisons between LightRAG and GraphRAG and does not mention GraphRAG traversing communities nor LightRAG retrieving with dual‑level keywords (entities and topics). |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer discusses win‑rates and performance metrics but never mentions Section 4.5, token counts (610 × 1,000), fewer than 100 tokens, or API calls, so it does not state the required claim. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer provides performance comparison data and does not mention Section 4.5, community rebuilding, or incremental graph updates, so it neither states nor affirms the required claim. |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| Agriculture 45.2 % \| 54.8 % \| + 9.6 % \| |
| table1_cs_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| Agriculture 45.2 % \| 54.8 % \| + 9.6 % \|<br>\| \| CS 48.0 % \| 52.0 % \| + 4.0 % \|<br>\| \| Legal 47.2 % \| 52.8 % \| + 5.6 % \|<br>\| \| Mix 50.4 % \| 49.6 % \| +  0.8 % \| |
| table1_legal_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | **Overall** \| Agriculture 45.2 % \| 54.8 % \| + 9.6 % \|<br>\| \| CS 48.0 % \| 52.0 % \| + 4.0 % \|<br>\| \| Legal 47.2 % \| 52.8 % \| + 5.6 % \|<br>\| \| Mix 50.4 % \| 49.6 % \| +  0.8 % \| |
| table1_mix_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| Agriculture 45.2 % \| 54.8 % \| + 9.6 % \|<br>\| \| CS 48.0 % \| 52.0 % \| + 4.0 % \|<br>\| \| Legal 47.2 % \| 52.8 % \| + 5.6 % \|<br>\| \| Mix 50.4 % \| 49.6 % \| +  0.8 % \|<br> |
| table3_case_study | judge | FAIL | Required claim not asserted: The answer discusses Table 1 and overall win‑rates, never references Table 3, Section 4.4, pages 8‑9, or a case‑study LLM judge, so it does not state the required claim. |  |
| not_all_datasets | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | The paper evaluates LightRAG against GraphRAG on four datasets (Agriculture, CS, Legal, Mix) ... In every cell of Table 1 the win‑rate for LightRAG (the “candidate”) is higher than the win‑rate for GraphRAG (the “baseline”), indicating that LightRAG consistently outperforms GraphRAG across all metrics and datasets[C4].<br><br>\| Metric / Dataset \| GraphRAG win % \| LightRAG win % \| Difference (LightRAG − GraphRAG) \|<br>\|------------------\|----------------\|----------------\|-----------------------------------\|<br>\| **Comprehensiveness** \| Agriculture 45.6 % \| 54.4 % \| +8.8 % \|<br>\| \| CS 48.4 % \| 51.6 % \| +3.2 % \|<br>\| \| Legal 48.4 % \| 51.6 % \| +3.2 % \|<br>\| \| Mix 50.4 % \| 49.6 % \| + 0.8 % \|<br>\| **Diversity** \| Agriculture 22.8 % \| 77.2 % \| + 54.4 % \|<br>\| \| CS 40.8 % \| 59.2 % \| + 18.4 % \|<br>\| \| Legal 26.4 % \| 73.6 % \| + 47.2 % \|<br>\| \| Mix 36.0 % \| 64.0 % \| + 28.0 % \|<br>\| **Empowerment** \| Agriculture 41.2 % \| 58.8 % \| + 17.6 % \|<br>\| \| CS 45.2 % \| 54.8 % \| + 9.6 % \|<br>\| \| Legal 43.6 % \| 56.4 % \| + 12.8 % \|<br>\| \| Mix 50.8 % \| 49.2 % \| +  1.4 % \|<br>\| **Overall** \| Agriculture 45.2 % \| 54.8 % \| + 9.6 % \|<br>\| \| CS 48.0 % \| 52.0 % \| + 4.0 % \|<br>\| \| Legal 47.2 % \| 52.8 % \| + 5.6 % \|<br>\| \| Mix 50.4 % \| 49.6 % \| +  0.8 % \|<br><br>**Key observations**<br><br>1. **Consistent superiority** – LightRAG achieves higher win rates than GraphRAG for every metric on every dataset, showing a uniform advantage rather than isolated strengths[C4]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 160 | 600 | 10000 | 4525.55 | stop |
| 2 | answer | low | 4017 | 3792 | 923 | 3000 | 10000 | 18002.99 | stop |
| 3 | judge | low | 1648 | 1423 | 133 | 1000 | 10000 | 4079.74 | stop |
| 4 | judge | low | 1710 | 1485 | 120 | 1000 | 10000 | 22777.62 | stop |
| 5 | judge | low | 1645 | 1420 | 137 | 1000 | 10000 | 7891.21 | stop |
| 6 | judge | low | 1708 | 1483 | 242 | 1000 | 10000 | 6753.41 | stop |
| 7 | judge | low | 1713 | 1488 | 328 | 1000 | 10000 | 7536.90 | stop |
| 8 | judge | low | 1706 | 1481 | 382 | 1000 | 10000 | 6192.51 | stop |
| 9 | judge | low | 1707 | 1482 | 498 | 1000 | 10000 | 2714.91 | stop |
| 10 | judge | low | 1653 | 1428 | 190 | 1000 | 10000 | 1251.28 | stop |
| 11 | judge | low | 1646 | 1421 | 766 | 1000 | 10000 | 2772.40 | stop |

### Finalized answer

<pre>**Overall comparison**

The paper evaluates LightRAG against GraphRAG on four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall). In every cell of Table 1 the win‑rate for LightRAG (the “candidate”) is higher than the win‑rate for GraphRAG (the “baseline”), indicating that LightRAG consistently outperforms GraphRAG across all metrics and datasets[C4].

| Metric / Dataset | GraphRAG win % | LightRAG win % | Difference (LightRAG − GraphRAG) |
|------------------|----------------|----------------|-----------------------------------|
| **Comprehensiveness** | Agriculture 45.6 % | 54.4 % | +8.8 % |
| | CS 48.4 % | 51.6 % | +3.2 % |
| | Legal 48.4 % | 51.6 % | +3.2 % |
| | Mix 50.4 % | 49.6 % | + 0.8 % |
| **Diversity** | Agriculture 22.8 % | 77.2 % | + 54.4 % |
| | CS 40.8 % | 59.2 % | + 18.4 % |
| | Legal 26.4 % | 73.6 % | + 47.2 % |
| | Mix 36.0 % | 64.0 % | + 28.0 % |
| **Empowerment** | Agriculture 41.2 % | 58.8 % | + 17.6 % |
| | CS 45.2 % | 54.8 % | + 9.6 % |
| | Legal 43.6 % | 56.4 % | + 12.8 % |
| | Mix 50.8 % | 49.2 % | +  1.4 % |
| **Overall** | Agriculture 45.2 % | 54.8 % | + 9.6 % |
| | CS 48.0 % | 52.0 % | + 4.0 % |
| | Legal 47.2 % | 52.8 % | + 5.6 % |
| | Mix 50.4 % | 49.6 % | +  0.8 % |

**Key observations**

1. **Consistent superiority** – LightRAG achieves higher win rates than GraphRAG for every metric on every dataset, showing a uniform advantage rather than isolated strengths[C4].  
2. **Largest gaps in Diversity** – The most pronounced improvements are seen in the Diversity dimension, especially on the Agriculture (‑54.4 % point) and Legal (‑47.2 % point) datasets, highlighting LightRAG’s ability to generate a broader range of responses[C4].  
3. **Smallest margin on Mix Overall** – The narrowest advantage occurs for the Mix dataset’s Overall score (‑0.8 % point), indicating that while LightRAG still leads, the performance gap narrows when datasets are more heterogeneous[C4].  
4. **Qualitative support** – The authors’ narrative reinforces these quantitative results, stating that LightRAG “consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts” and that it “shows a clear advantage, significantly surpassing GraphRAG”[C5].  

**Conclusion**

Across all evaluated dimensions and corpora, LightRAG demonstrates a measurable and consistent performance edge over GraphRAG, with especially strong gains in response diversity and a modest but universal lead in overall quality.</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Synthesis; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: [&#x27;LightRAG ablation study results&#x27;, &#x27;performance metrics of LightRAG ablated models&#x27;, &#x27;comparison of LightRAG variant performance&#x27;]

Ask latency_ms: 5928.85

Judge latency_ms: 8439.46

Total evaluation latency_ms: 14378.88

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C5 |
| question_type | events | FAIL | Expected Lookup; actual Synthesis; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The ablation study compares three LightRAG variants (each missing one component) with the NaiveRAG baseline. For every metric and dataset the table reports the NaiveRAG win rate and the variant win rate (percentage). ... *Each cell shows “baseline win rate / variant win rate” as reported in Table 2.* |
| ablation_meaning | judge | FAIL | Required claim not asserted: The answer describes -High and -Low as removing high‑level and low‑level retrieval respectively, which matches those parts, but describes -Origin as removing origin‑level indexing, not original text, and does not state that the full LightRAG combines both retrieval levels. Therefore the claim is not fully asserted. |  |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer provides the -Low Overall win rate for Mix (64.8%) but does not state the full LightRAG overall win rate (60.0%) nor explicitly compare them, so the claim is not fully asserted or matched. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer provides the -Origin Overall win rate of 74.4% for Agriculture but does not state the full LightRAG overall win rate of 67.6% nor assert that 74.4% is higher, so the claim is not fully presented or affirmed. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 173 | 600 | 10000 | 1276.17 | stop |
| 2 | answer | low | 4377 | 4152 | 1063 | 3000 | 10000 | 4105.13 | stop |
| 3 | judge | low | 1829 | 1604 | 349 | 1000 | 10000 | 1966.79 | stop |
| 4 | judge | low | 1830 | 1605 | 242 | 1000 | 10000 | 1464.72 | stop |
| 5 | judge | low | 1889 | 1664 | 406 | 1000 | 10000 | 2135.46 | stop |
| 6 | judge | low | 1890 | 1665 | 281 | 1000 | 10000 | 1745.54 | stop |
| 7 | judge | low | 1817 | 1592 | 144 | 1000 | 10000 | 1126.95 | stop |

### Finalized answer

<pre>The ablation study compares three LightRAG variants (each missing one component) with the NaiveRAG baseline. For every metric and dataset the table reports the NaiveRAG win rate and the variant win rate (percentage). The results are:

| Variant (omitted module) | Metric | Agriculture (NaiveRAG / variant) | CS (NaiveRAG / variant) | Legal (NaiveRAG / variant) | Mix (NaiveRAG / variant) |
|---|---|---|---|---|---|
| **‑High** (high‑level retrieval removed) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
|  | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
|  | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
|  | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (low‑level retrieval removed) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
|  | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
|  | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
|  | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (origin‑level indexing removed) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
|  | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
|  | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
|  | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

*Each cell shows “baseline win rate / variant win rate” as reported in Table 2.*  
These figures illustrate how removing the high‑level retrieval, low‑level retrieval, or origin‑level indexing modules reduces LightRAG’s advantage over NaiveRAG, with the **‑Origin** variant showing the largest drop in performance across most metrics and datasets. [C5]</pre>
