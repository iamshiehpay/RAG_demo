# Golden Facts evaluation

Created: 2026-10-13T11:04:29.500107+00:00

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

Created: 2026-10-13T11:04:29.499060+00:00

Label: answer-think-medium

Effective settings: {&quot;answer_think&quot;: &quot;medium&quot;, &quot;bm25_weight&quot;: 0.0, &quot;chunk_token_target&quot;: 800, &quot;lookup_top_k&quot;: 5, &quot;sub_query_top_k&quot;: 2, &quot;summary_concurrency&quot;: 4, &quot;synthesis_top_k&quot;: 3}

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
| Q2 | table3_case_study | judge | 1/1 (100.0%) |
| Q2 | not_all_datasets | forbidden | 0/1 (0.0%) |
| Q3 | required_source_citation | events | 1/1 (100.0%) |
| Q3 | question_type | events | 0/1 (0.0%) |
| Q3 | high_term | contains | 1/1 (100.0%) |
| Q3 | low_term | contains | 1/1 (100.0%) |
| Q3 | origin_term | contains | 1/1 (100.0%) |
| Q3 | table2_baseline | judge | 1/1 (100.0%) |
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

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG vs GraphRAG performance and scalability&#x27;, &#x27;LightRAG vs GraphRAG limitations and maintenance&#x27;]

Ask latency_ms: 5153.59

Judge latency_ms: 9915.25

Total evaluation latency_ms: 15104.43

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer only describes LightRAG&#x27;s dual-level retrieval but does not state that GraphRAG traverses communities, so the full claim is not present. |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer never states the token counts (610 000 vs &lt;100) or mentions API calls; thus it does not assert the required claim. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer discusses performance metrics and qualitative assessment, but does not state anything about GraphRAG rebuilding communities or LightRAG incrementally updating its graph, so the claim is not addressed. |  |
| table1_agriculture_overall | judge | FAIL | Required claim not asserted: The answer does not provide the specific Agriculture Overall win rates of 54.8% for LightRAG and 45.2% for GraphRAG, nor does it mention these exact values, so the claim is not explicitly stated. |  |
| table1_cs_overall | judge | FAIL | Required claim not asserted: The answer does not provide the specific CS overall win‑rate values of 52.0% for LightRAG and 48.0% for GraphRAG, nor does it state that LightRAG&#x27;s rate is higher. It only gives generic performance descriptions and numbers for the Legal set. |  |
| table1_legal_overall | judge | FAIL | Required claim not asserted: The answer reports LightRAG&#x27;s Overall win rate on Legal as 84.8% and GraphRAG&#x27;s as 52.8%, not the claimed 52.8% for LightRAG and 47.2% for GraphRAG, thus the required claim is not stated or affirmed. |  |
| table1_mix_overall | judge | FAIL | Required claim not asserted: The answer states LightRAG has higher win‑rate percentages than GraphRAG across all domains and does not provide the specific Mix Overall values 49.6% and 50.4%, nor does it claim LightRAG is lower. Therefore the required claim is not asserted or matched. |  |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | A case‑study comparison (Table 3) shows LightRAG beating GraphRAG in every judged dimension—Comprehensiveness, Diversity, Empowerment, and Overall—according to an LLM judge [C4][C5]. |
| not_all_datasets | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | Across the four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) and all four test sets (Agriculture, CS, Legal, Mix), LightRAG consistently achieves higher win‑rate percentages than GraphRAG. For example, on the Legal set LightRAG’s win rates are 83.6 % (Comprehensiveness), 86.4 % (Diversity), 83.6 % (Empowerment) and 84.8 % (Overall) versus GraphRAG’s 51.6 %, 73.6 %, 56.4 % and 52.8 % respectively [C2]. Similar advantages appear in the other domains, with LightRAG’s win rates ranging from roughly 60 %–70 % while GraphRAG hovers around the 45 %–55 % range.<br><br>**Summary**<br><br>LightRAG outperforms GraphRAG on all measured metrics and datasets, achieving substantially higher win rates, especially on the largest (Legal) corpus. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 128 | 600 | 10000 | 978.71 | stop |
| 2 | answer | medium | 3589 | 3364 | 657 | 3000 | 10000 | 3682.29 | stop |
| 3 | judge | low | 1306 | 1081 | 176 | 1000 | 10000 | 1006.75 | stop |
| 4 | judge | low | 1368 | 1143 | 101 | 1000 | 10000 | 928.44 | stop |
| 5 | judge | low | 1303 | 1078 | 123 | 1000 | 10000 | 857.54 | stop |
| 6 | judge | low | 1366 | 1141 | 155 | 1000 | 10000 | 1070.47 | stop |
| 7 | judge | low | 1371 | 1146 | 146 | 1000 | 10000 | 1070.99 | stop |
| 8 | judge | low | 1364 | 1139 | 190 | 1000 | 10000 | 1230.71 | stop |
| 9 | judge | low | 1365 | 1140 | 179 | 1000 | 10000 | 1156.19 | stop |
| 10 | judge | low | 1311 | 1086 | 229 | 1000 | 10000 | 1128.30 | stop |
| 11 | judge | low | 1304 | 1079 | 383 | 1000 | 10000 | 1465.85 | stop |

### Finalized answer

<pre>**Performance on quantitative benchmarks**

- Across the four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) and all four test sets (Agriculture, CS, Legal, Mix), LightRAG consistently achieves higher win‑rate percentages than GraphRAG. For example, on the Legal set LightRAG’s win rates are 83.6 % (Comprehensiveness), 86.4 % (Diversity), 83.6 % (Empowerment) and 84.8 % (Overall) versus GraphRAG’s 51.6 %, 73.6 %, 56.4 % and 52.8 % respectively [C2]. Similar advantages appear in the other domains, with LightRAG’s win rates ranging from roughly 60 %–70 % while GraphRAG hovers around the 45 %–55 % range.

- The overall win‑rate gap widens on the largest dataset (Legal), where baseline (non‑graph) methods obtain only about 20 % wins while LightRAG dominates; GraphRAG, although graph‑based, still lags behind LightRAG in this scenario [C3].

**Qualitative assessment**

- A case‑study comparison (Table 3) shows LightRAG beating GraphRAG in every judged dimension—Comprehensiveness, Diversity, Empowerment, and Overall—according to an LLM judge [C4][C5].

**Underlying reasons**

- Both systems use graph‑based retrieval, but LightRAG’s “dual‑level retrieval paradigm” (low‑level entity retrieval plus high‑level topic retrieval) is credited with delivering broader coverage and more varied responses, which translates into higher scores on Diversity and Empowerment [C3].

- The authors explicitly state that LightRAG “consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts,” highlighting its strength in handling millions of tokens and intricate queries [C3].

**Summary**

LightRAG outperforms GraphRAG on all measured metrics and datasets, achieving substantially higher win rates, especially on the largest (Legal) corpus. The advantage is attributed to LightRAG’s hierarchical, dual‑level retrieval design, which yields more comprehensive, diverse, and empowering responses than GraphRAG’s graph‑only approach. [C2][C3][C4][C5]</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Synthesis; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: [&#x27;LightRAG ablation study results&#x27;, &#x27;performance metrics of LightRAG ablated models&#x27;, &#x27;comparison of LightRAG variants&#x27;]

Ask latency_ms: 6832.57

Judge latency_ms: 5903.86

Total evaluation latency_ms: 12749.18

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C5 |
| question_type | events | FAIL | Expected Lookup; actual Synthesis; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | **Source:** Table 2 of the ablation study, which lists “NaiveRAG / variant win rate (baseline / variant, %)” for each metric and dataset[C5]. |
| ablation_meaning | judge | FAIL | Required claim not asserted: The answer lists ablation results for -High, -Low, and -Origin but does not explicitly state that -High removes high-level retrieval, -Low removes low-level retrieval, or -Origin removes original text, nor does it describe the full LightRAG combining both retrieval levels. |  |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer provides the -Low Overall win rate for Mix as 64.8% but does not state the full LightRAG overall win rate of 60.0% for Mix, so the required comparison is missing. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer provides the -Origin Overall win rate of 74.4% for Agriculture but does not give the full LightRAG overall win rate (67.6%) nor state that 74.4% is higher, so the required claim is not fully presented. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 172 | 600 | 10000 | 1116.35 | stop |
| 2 | answer | medium | 4377 | 4152 | 1251 | 3000 | 10000 | 5147.10 | stop |
| 3 | judge | low | 1641 | 1416 | 308 | 1000 | 10000 | 1354.06 | stop |
| 4 | judge | low | 1642 | 1417 | 197 | 1000 | 10000 | 1091.80 | stop |
| 5 | judge | low | 1702 | 1477 | 240 | 1000 | 10000 | 1291.07 | stop |
| 6 | judge | low | 1703 | 1478 | 231 | 1000 | 10000 | 1255.90 | stop |
| 7 | judge | low | 1629 | 1404 | 143 | 1000 | 10000 | 911.03 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (compared against NaiveRAG)**  

| Variant (baseline / ablated) | Metric | Agriculture (baseline / variant %) | CS (baseline / variant %) | Legal (baseline / variant %) | Mix (baseline / variant %) |
|---|---|---|---|---|---|
| **NaiveRAG / ‑High** | Comprehensiveness | 34.8 / 65.2 | 42.8 / 57.2 | 23.6 / 76.4 | 40.4 / 59.6 |
|  | Diversity | 27.2 / 72.8 | 36.8 / 63.2 | 16.8 / 83.2 | 36.0 / 64.0 |
|  | Empowerment | 36.0 / 64.0 | 42.4 / 57.6 | 22.8 / 77.2 | 47.6 / 52.4 |
|  | Overall | 35.2 / 64.8 | 44.0 / 56.0 | 22.0 / 78.0 | 42.4 / 57.6 |
| **NaiveRAG / ‑Low** | Comprehensiveness | 36.0 / 64.0 | 43.2 / 56.8 | 19.2 / 80.8 | 36.0 / 64.0 |
|  | Diversity | 28.0 / 72.0 | 39.6 / 60.4 | 13.6 / 86.4 | 33.2 / 66.8 |
|  | Empowerment | 34.8 / 65.2 | 42.8 / 57.2 | 16.4 / 83.6 | 35.2 / 64.8 |
|  | Overall | 34.8 / 65.2 | 43.6 / 56.4 | 18.8 / 81.2 | 35.2 / 64.8 |
| **NaiveRAG / ‑Origin** | Comprehensiveness | 24.8 / 75.2 | 39.2 / 60.8 | 16.4 / 83.6 | 44.4 / 55.6 |
|  | Diversity | 26.4 / 73.6 | 44.8 / 55.2 | 14.4 / 85.6 | 25.6 / 74.4 |
|  | Empowerment | 32.0 / 68.0 | 43.2 / 56.8 | 17.2 / 82.8 | 45.2 / 54.8 |
|  | Overall | 25.6 / 74.4 | 39.2 / 60.8 | 15.6 / 84.4 | 44.4 / 55.6 |

*Interpretation* – In every case the ablated LightRAG variant achieves a higher win‑rate than the NaiveRAG baseline, indicating that even when one component (high‑level retrieval, low‑level retrieval, or the original graph‑based indexing) is removed, LightRAG still outperforms the baseline across all four datasets and all four evaluation dimensions.  

**Source:** Table 2 of the ablation study, which lists “NaiveRAG / variant win rate (baseline / variant, %)” for each metric and dataset[C5].</pre>
