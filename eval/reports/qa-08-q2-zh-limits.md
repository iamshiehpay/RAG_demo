# Golden Facts evaluation

Created: 2026-10-12T17:37:48.549482+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: qa-08-gap7

Revision: f38cf47ae990dc6a57d7d807bbd0ef2eb64f9c3f

Uncommitted changes: yes

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: chat_document.router_regression.CASES (#06 canonical 12 cases)

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
| ZH_COST | question_type | events | 1/1 (100.0%) |
| ZH_COST | chinese_answer | judge | 1/1 (100.0%) |
| ZH_COST | retrieval_cost | judge | 1/1 (100.0%) |
| ZH_COST | numbers_unchanged | judge | 1/1 (100.0%) |
| LIMITATIONS | citation_sections | events | 0/1 (0.0%) |
| LIMITATIONS | question_type | events | 1/1 (100.0%) |
| LIMITATIONS | evaluation_limit | judge | 0/1 (0.0%) |
| LIMITATIONS | retrieval_tradeoff | judge | 0/1 (0.0%) |
| LIMITATIONS | not_universally_best | judge | 0/1 (0.0%) |
| LIMITATIONS | no_invented_limit | forbidden | 1/1 (100.0%) |

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

Sub-queries: [&#x27;LightRAG vs GraphRAG architecture&#x27;, &#x27;LightRAG vs GraphRAG performance&#x27;, &#x27;LightRAG vs GraphRAG limitations&#x27;]

Ask latency_ms: 5103.33

Judge latency_ms: 10008.90

Total evaluation latency_ms: 15127.53

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | and 54.8 % vs. 45.2 % overall)[C2] |
| table1_cs_overall | judge | FAIL | Required claim not asserted |  |
| table1_legal_overall | judge | FAIL | Required claim not asserted |  |
| table1_mix_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | LightRAG consistently outperforms GraphRAG on the four evaluation dimensions that were measured (comprehensiveness, diversity, empowerment, and overall). |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | LightRAG consistently outperforms GraphRAG on the four evaluation dimensions that were measured (comprehensiveness, diversity, empowerment, and overall).  <br><br>- In the first set of results, LightRAG’s win‑rates are roughly three‑quarters of the comparisons (e.g., 74 % vs. 26 % for comprehensiveness, 76 % vs. 24 % for diversity, 74.8 % vs. 25.2 % for empowerment, and 75.2 % vs. 24.8 % overall) whereas GraphRAG lags behind with roughly one‑quarter win‑rates[C2].  <br>- In the second set of results, LightRAG still leads, though the gap narrows (e.g., 54.4 % vs. 45.6 % for comprehensiveness, 77.2 % vs. 22.8 % for diversity, 58.8 % vs. 41.2 % for empowerment, and 54.8 % vs. 45.2 % overall)[C2].  <br><br>These figures indicate that LightRAG provides more comprehensive, diverse, and empowering answers, and achieves a higher overall performance than GraphRAG across the evaluated datasets. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 137 | 600 | 10000 | 858.55 | stop |
| 2 | answer | medium | 1537 | 1312 | 865 | 3000 | 10000 | 3731.71 | stop |
| 3 | judge | low | 1002 | 777 | 95 | 1000 | 10000 | 977.09 | stop |
| 4 | judge | low | 1039 | 814 | 53 | 1000 | 10000 | 820.24 | stop |
| 5 | judge | low | 999 | 774 | 100 | 1000 | 10000 | 1184.41 | stop |
| 6 | judge | low | 1015 | 790 | 145 | 1000 | 10000 | 1205.57 | stop |
| 7 | judge | low | 1015 | 790 | 132 | 1000 | 10000 | 1050.65 | stop |
| 8 | judge | low | 1015 | 790 | 128 | 1000 | 10000 | 982.29 | stop |
| 9 | judge | low | 1015 | 790 | 88 | 1000 | 10000 | 889.32 | stop |
| 10 | judge | low | 1007 | 782 | 138 | 1000 | 10000 | 1033.37 | stop |
| 11 | judge | low | 1000 | 775 | 430 | 1000 | 10000 | 1865.96 | stop |

### Finalized answer

<pre>LightRAG consistently outperforms GraphRAG on the four evaluation dimensions that were measured (comprehensiveness, diversity, empowerment, and overall).  

- In the first set of results, LightRAG’s win‑rates are roughly three‑quarters of the comparisons (e.g., 74 % vs. 26 % for comprehensiveness, 76 % vs. 24 % for diversity, 74.8 % vs. 25.2 % for empowerment, and 75.2 % vs. 24.8 % overall) whereas GraphRAG lags behind with roughly one‑quarter win‑rates[C2].  
- In the second set of results, LightRAG still leads, though the gap narrows (e.g., 54.4 % vs. 45.6 % for comprehensiveness, 77.2 % vs. 22.8 % for diversity, 58.8 % vs. 41.2 % for empowerment, and 54.8 % vs. 45.2 % overall)[C2].  

These figures indicate that LightRAG provides more comprehensive, diverse, and empowering answers, and achieves a higher overall performance than GraphRAG across the evaluated datasets.  

Both systems share the same underlying infrastructure (nano vector database, GPT‑4o‑mini for LLM operations, a chunk size of 1200, and a gleaning parameter of 1) and are evaluated using the same multi‑dimensional LLM‑based comparison method[C1]. However, the empirical win‑rate results show LightRAG’s superiority in practice.</pre>

## ZH_COST — repetition 1

Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Sub-queries: [&#x27;LightRAG 檢索成本機制&#x27;, &#x27;GraphRAG 檢索成本機制&#x27;, &#x27;LightRAG 與 GraphRAG 成本比較&#x27;]

Ask latency_ms: 4013.54

Judge latency_ms: 4334.86

Total evaluation latency_ms: 8356.65

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| chinese_answer | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。  <br>在檢索階段，GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且需逐一遍歷社群，導致「數百」次 API 呼叫，檢索開銷相當大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，極大降低了 token 消耗與 API 呼叫次數[C3]。  <br>此外，LightRAG 透過結合圖結構與向量表示，避免了事先處理大量資訊的需求，進一步減少了檢索時的資源開銷[C4]。 |
| retrieval_cost | judge | PASS | Required claim supported by verbatim evidence | 在檢索階段，GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且需逐一遍歷社群，導致「數百」次 API 呼叫，檢索開銷相當大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫 |
| numbers_unchanged | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且需逐一遍歷社群，導致「數百」次 API 呼叫，檢索開銷相當大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 846 | 507 | 146 | 600 | 10000 | 1004.39 | stop |
| 2 | answer | medium | 1923 | 1698 | 455 | 3000 | 10000 | 2480.99 | stop |
| 3 | judge | low | 849 | 624 | 300 | 1000 | 10000 | 1241.66 | stop |
| 4 | judge | low | 896 | 671 | 267 | 1000 | 10000 | 1586.81 | stop |
| 5 | judge | low | 881 | 656 | 345 | 1000 | 10000 | 1506.40 | stop |

### Finalized answer

<pre>LightRAG 的檢索成本遠低於 GraphRAG。  
在檢索階段，GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且需逐一遍歷社群，導致「數百」次 API 呼叫，檢索開銷相當大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，極大降低了 token 消耗與 API 呼叫次數[C3]。  
此外，LightRAG 透過結合圖結構與向量表示，避免了事先處理大量資訊的需求，進一步減少了檢索時的資源開銷[C4]。</pre>

## LIMITATIONS — repetition 1

Question: 這篇論文有什麼限制？

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 這篇論文的限制是什麼？

Sub-queries: [&#x27;論文 方法學 限制&#x27;, &#x27;實驗 設計 限制&#x27;, &#x27;結果 解釋 限制&#x27;]

Ask latency_ms: 2826.48

Judge latency_ms: 2287.75

Total evaluation latency_ms: 5116.93

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| citation_sections | events | FAIL | 0 distinct cited Sections; requires 2 |  |
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| evaluation_limit | judge | FAIL | Required claim not asserted |  |
| retrieval_tradeoff | judge | FAIL | Required claim not asserted |  |
| not_universally_best | judge | FAIL | Required claim not asserted |  |
| no_invented_limit | forbidden | PASS | Exact fixed refusal contains no asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 838 | 499 | 180 | 600 | 10000 | 1173.97 | stop |
| 2 | answer | medium | 2213 | 1988 | 141 | 3000 | 10000 | 1110.80 | stop |
| 3 | judge | low | 652 | 427 | 69 | 1000 | 10000 | 793.02 | stop |
| 4 | judge | low | 669 | 444 | 71 | 1000 | 10000 | 713.40 | stop |
| 5 | judge | low | 652 | 427 | 73 | 1000 | 10000 | 781.33 | stop |

### Finalized answer

<pre>文件中未提及</pre>


## Judge semantic probes (excluded from Golden Facts result)

## JUDGE_ASSERTED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 811.74

Total evaluation latency_ms: 811.74

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 811.74 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 867.80

Total evaluation latency_ms: 867.80

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 867.80 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
