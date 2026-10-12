# Golden Facts evaluation

Created: 2026-10-12T15:01:08.718432+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Label: lookup-skeleton

Revision: 085aac06afa7e718522f8acb11f1c819823dc708

Uncommitted changes: no

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: #06 exported cases if available; otherwise fixed spike cases

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 0/1 (0.0%) |
| Q1 | motivation | judge | 1/1 (100.0%) |
| Q1 | graph_indexing | judge | 0/1 (0.0%) |
| Q1 | dual_level | judge | 1/1 (100.0%) |
| Q1 | incremental_update | judge | 0/1 (0.0%) |
| Q1 | experiments | judge | 1/1 (100.0%) |
| Q1 | conclusion | judge | 0/1 (0.0%) |
| Q2 | question_type | events | 0/1 (0.0%) |
| Q2 | retrieval_methods | judge | 0/1 (0.0%) |
| Q2 | retrieval_cost | judge | 0/1 (0.0%) |
| Q2 | incremental_update | judge | 0/1 (0.0%) |
| Q2 | table1_overall | judge | 0/1 (0.0%) |
| Q2 | table3_case_study | judge | 0/1 (0.0%) |
| Q2 | not_all_datasets | forbidden | 0/1 (0.0%) |
| Q3 | question_type | events | 1/1 (100.0%) |
| Q3 | high_term | contains | 1/1 (100.0%) |
| Q3 | low_term | contains | 1/1 (100.0%) |
| Q3 | origin_term | contains | 0/1 (0.0%) |
| Q3 | table2_baseline | judge | 1/1 (100.0%) |
| Q3 | ablation_meaning | judge | 0/1 (0.0%) |
| Q3 | mix_low_overall | judge | 0/1 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/1 (0.0%) |
| Q3 | not_all_best | forbidden | 1/1 (100.0%) |
| ZH_COST | question_type | events | 0/1 (0.0%) |
| ZH_COST | chinese_answer | judge | 1/1 (100.0%) |
| ZH_COST | retrieval_cost | judge | 1/1 (100.0%) |
| ZH_COST | numbers_unchanged | judge | 1/1 (100.0%) |
| LIMITATIONS | citation_sections | events | 0/1 (0.0%) |
| LIMITATIONS | question_type | events | 0/1 (0.0%) |
| LIMITATIONS | evaluation_limit | judge | 0/1 (0.0%) |
| LIMITATIONS | retrieval_tradeoff | judge | 0/1 (0.0%) |
| LIMITATIONS | not_universally_best | judge | 0/1 (0.0%) |
| LIMITATIONS | no_invented_limit | forbidden | 1/1 (100.0%) |
| ABSENT_HOTPOT | question_type | events | 1/1 (100.0%) |
| ABSENT_HOTPOT | fixed_reply | judge | 0/1 (0.0%) |
| ABSENT_LICENSE | question_type | events | 1/1 (100.0%) |
| ABSENT_LICENSE | fixed_reply | judge | 0/1 (0.0%) |
| ABSENT_GPU | question_type | events | 1/1 (100.0%) |
| ABSENT_GPU | fixed_reply | judge | 0/1 (0.0%) |
| ROUTER_01 | question_type | events | 0/1 (0.0%) |
| ROUTER_02 | question_type | events | 0/1 (0.0%) |
| ROUTER_03 | question_type | events | 0/1 (0.0%) |
| ROUTER_04 | question_type | events | 0/1 (0.0%) |
| ROUTER_05 | question_type | events | 0/1 (0.0%) |
| ROUTER_06 | question_type | events | 0/1 (0.0%) |
| ROUTER_07 | question_type | events | 1/1 (100.0%) |
| ROUTER_08 | question_type | events | 1/1 (100.0%) |
| ROUTER_09 | question_type | events | 1/1 (100.0%) |
| ROUTER_10 | question_type | events | 1/1 (100.0%) |
| ROUTER_11 | question_type | events | 1/1 (100.0%) |
| ROUTER_11 | history_supported | events | 0/1 (0.0%) |
| ROUTER_12 | question_type | events | 0/1 (0.0%) |
| ROUTER_12 | history_supported | events | 0/1 (0.0%) |
| JUDGE_ASSERTED | semantic_contract | judge | 1/1 (100.0%) |
| JUDGE_NEGATED | semantic_contract | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q1 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Total evaluation latency_ms: 9602.34

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is a Retrieval‑Augmented Generation (RAG) framework that enhances large language models by integrating graph‑structured knowledge into the text‑indexing and retrieval pipeline, thereby overcoming the flat‑data representations and fragmented answers of prior RAG systems [C1][C2]. |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The system introduces a **dual‑level retrieval** mechanism: a low‑level stage that fetches precise information about specific entities and their relations, and a high‑level stage that retrieves broader topics and themes, enabling both detailed and conceptual coverage of user queries [C2]. |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Table 2 compares LightRAG with a baseline “NaiveRAG” across four metrics (Comprehensiveness, Diversity, Empowerment, Overall). Using the baseline as the reference, LightRAG consistently achieves higher percentages in every metric and domain (e.g., Overall scores rise from 32.4 % to 67.6 % in Agriculture, from 38.8 % to 61.2 % in CS, from 15.2 % to 84.8 % in Legal, and from 40.0 % to 60.0 % in the Mix set) [C3]. |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 934 | 3000 | 10000 | 3208.14 | stop |
| 2 | judge | low | 1205 | 980 | 186 | 1000 | 10000 | 902.90 | stop |
| 3 | judge | low | 1200 | 975 | 103 | 1000 | 10000 | 1116.90 | stop |
| 4 | judge | low | 1202 | 977 | 173 | 1000 | 10000 | 852.20 | stop |
| 5 | judge | low | 1208 | 983 | 131 | 1000 | 10000 | 869.26 | stop |
| 6 | judge | low | 1217 | 992 | 328 | 1000 | 10000 | 1650.83 | stop |
| 7 | judge | low | 1201 | 976 | 95 | 1000 | 10000 | 823.52 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) framework that enhances large language models by integrating graph‑structured knowledge into the text‑indexing and retrieval pipeline, thereby overcoming the flat‑data representations and fragmented answers of prior RAG systems [C1][C2].  
The system introduces a **dual‑level retrieval** mechanism: a low‑level stage that fetches precise information about specific entities and their relations, and a high‑level stage that retrieves broader topics and themes, enabling both detailed and conceptual coverage of user queries [C2].  
To keep the knowledge base current, LightRAG includes an **incremental update algorithm** that quickly incorporates new data, maintaining relevance in dynamic environments [C2].  
All code has been released open‑source on GitHub [C1].

**Experimental evaluation** was conducted on four heterogeneous datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens) [C5].  
Table 2 compares LightRAG with a baseline “NaiveRAG” across four metrics (Comprehensiveness, Diversity, Empowerment, Overall). Using the baseline as the reference, LightRAG consistently achieves higher percentages in every metric and domain (e.g., Overall scores rise from 32.4 % to 67.6 % in Agriculture, from 38.8 % to 61.2 % in CS, from 15.2 % to 84.8 % in Legal, and from 40.0 % to 60.0 % in the Mix set) [C3].  
These results demonstrate that the graph‑augmented, dual‑level retrieval substantially improves both the **accuracy** and **efficiency** of information retrieval compared with flat‑vector baselines.

The appendix details the **methodology** for extracting entities and relationships with LLMs, the prompt templates used, and the evaluation dimensions applied to benchmark LightRAG against baselines [C5].  
A concrete retrieval‑and‑generation example (Figure 3) shows how a query about “metrics most informative for evaluating movie recommendation systems” is processed: the LLM extracts low‑ and high‑level keywords, which then drive the dual‑level retrieval before generation [C5].

In summary, LightRAG proposes a graph‑empowered, dual‑level RAG architecture that delivers more comprehensive, diverse, and empowered responses while remaining fast and adaptable to new data, with empirical gains confirmed across multiple domains. [C1][C2][C3][C5]</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 13563.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | FAIL | Required claim not asserted |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | LightRAG consistently beats GraphRAG on all measured dimensions. In the head‑to‑head evaluation (Section 7), LightRAG’s win rates are markedly higher than GraphRAG’s for Comprehensiveness (e.g., 74 % vs 26 % in one setting and 58.4 % vs 41.6 % in another), Diversity (e.g., 77 % vs 24 % and 67.6 % vs 32.4 %), Empowerment (e.g., 74.8 % vs 25.2 % and 54 % vs 46 %), and Overall performance (e.g., 75.2 % vs 24.8 % and 57.6 % vs 42.4 %)[C2]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 668 | 3000 | 10000 | 3782.23 | stop |
| 2 | judge | low | 966 | 741 | 131 | 1000 | 10000 | 985.23 | stop |
| 3 | judge | low | 1003 | 778 | 75 | 1000 | 10000 | 808.88 | stop |
| 4 | judge | low | 963 | 738 | 90 | 1000 | 10000 | 789.79 | stop |
| 5 | judge | low | 1002 | 777 | 87 | 1000 | 10000 | 976.01 | stop |
| 6 | judge | low | 984 | 759 | 162 | 1000 | 10000 | 1001.90 | stop |
| 7 | judge | low | 964 | 739 | 268 | 1000 | 10000 | 1640.62 | stop |

### Finalized answer

<pre>LightRAG consistently beats GraphRAG on all measured dimensions. In the head‑to‑head evaluation (Section 7), LightRAG’s win rates are markedly higher than GraphRAG’s for Comprehensiveness (e.g., 74 % vs 26 % in one setting and 58.4 % vs 41.6 % in another), Diversity (e.g., 77 % vs 24 % and 67.6 % vs 32.4 %), Empowerment (e.g., 74.8 % vs 25.2 % and 54 % vs 46 %), and Overall performance (e.g., 75.2 % vs 24.8 % and 57.6 % vs 42.4 %)[C2].  

The authors attribute LightRAG’s advantage to its dual‑level retrieval paradigm, which combines low‑level entity retrieval with high‑level topic retrieval via graph‑based text indexing. This hierarchical approach captures both detailed and abstract information, yielding richer, more diverse responses—especially on large, complex corpora such as the Legal, Agriculture and CS datasets[C3].  

While both systems are graph‑enhanced RAGs (GraphRAG extracts entities and relationships into a graph, LightRAG also uses a graph but adds the dual‑level retrieval layer), LightRAG’s architecture leads to superior performance across the four evaluation dimensions, particularly in handling high‑token, complex queries where comprehensive understanding and response variety are critical[C1][C3].</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 10055.10

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *All percentages are taken directly from Table 2, which reports the performance of ablated LightRAG versions compared with NaiveRAG across four test domains (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C3].* |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1230 | 3000 | 10000 | 4630.55 | stop |
| 2 | judge | low | 1074 | 849 | 284 | 1000 | 10000 | 1493.50 | stop |
| 3 | judge | low | 1075 | 850 | 118 | 1000 | 10000 | 931.09 | stop |
| 4 | judge | low | 1086 | 861 | 123 | 1000 | 10000 | 973.51 | stop |
| 5 | judge | low | 1086 | 861 | 113 | 1000 | 10000 | 845.28 | stop |
| 6 | judge | low | 1062 | 837 | 110 | 1000 | 10000 | 937.88 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (performance relative to NaiveRAG)**  

| Ablation | Domain | Comprehensiveness | Diversity | Empowerment | Overall |
|----------|--------|-------------------|-----------|-------------|---------|
| **Full LightRAG** (baseline) | Agriculture | 67.6 % | 76.4 % | 67.6 % | 67.6 % |
| | CS | 61.6 % | 62.0 % | 61.2 % | 61.2 % |
| | Legal | 83.6 % | 86.4 % | 83.6 % | 84.8 % |
| | Mix | 61.2 % | 67.6 % | 57.2 % | 60.0 % |
| **LightRAG‑High** (high‑level retrieval only) | Agriculture | 65.2 % | 72.8 % | 64.0 % | 64.8 % |
| | CS | 57.2 % | 63.2 % | 57.6 % | 56.0 % |
| | Legal | 76.4 % | 83.2 % | 77.2 % | 78.0 % |
| | Mix | 59.6 % | 64.0 % | 52.4 % | 57.6 % |
| **LightRAG‑Low** (low‑level retrieval only) | – (values not provided in the excerpt) | – | – | – | – |

*All percentages are taken directly from Table 2, which reports the performance of ablated LightRAG versions compared with NaiveRAG across four test domains (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C3].*</pre>

## ZH_COST — repetition 1

Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Sub-queries: []

Total evaluation latency_ms: 9724.74

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| chinese_answer | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。GraphRAG 在檢索階段必須遍歷大量社群：它產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫[C4]。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫[C4]。此外，LightRAG 透過結合圖結構與向量化表示，避免了在檢索前處理大量資訊的需求，進一步降低了檢索開銷[C5]。 |
| retrieval_cost | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 在檢索階段必須遍歷大量社群：它產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫[C4]。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫[C4]。 |
| numbers_unchanged | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 在檢索階段必須遍歷大量社群：它產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫[C4]。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫[C4]。 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2625 | 2400 | 418 | 3000 | 10000 | 2292.68 | stop |
| 2 | judge | low | 842 | 617 | 290 | 1000 | 10000 | 1211.50 | stop |
| 3 | judge | low | 889 | 664 | 404 | 1000 | 10000 | 1433.43 | stop |
| 4 | judge | low | 874 | 649 | 336 | 1000 | 10000 | 1358.14 | stop |

### Finalized answer

<pre>LightRAG 的檢索成本遠低於 GraphRAG。GraphRAG 在檢索階段必須遍歷大量社群：它產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫[C4]。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫[C4]。此外，LightRAG 透過結合圖結構與向量化表示，避免了在檢索前處理大量資訊的需求，進一步降低了檢索開銷[C5]。因此，LightRAG 在檢索階段的 token 使用量與 API 呼叫次數皆顯著少於 GraphRAG。</pre>

## LIMITATIONS — repetition 1

Question: 這篇論文有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: 這篇論文有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 4447.55

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| citation_sections | events | FAIL | 0 distinct cited Sections; requires 2 |  |
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| evaluation_limit | judge | FAIL | Required claim not asserted |  |
| retrieval_tradeoff | judge | FAIL | Required claim not asserted |  |
| not_universally_best | judge | FAIL | Required claim not asserted |  |
| no_invented_limit | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2565 | 2340 | 239 | 3000 | 10000 | 1345.89 | stop |
| 2 | judge | low | 637 | 412 | 75 | 1000 | 10000 | 747.93 | stop |
| 3 | judge | low | 654 | 429 | 71 | 1000 | 10000 | 677.79 | stop |
| 4 | judge | low | 637 | 412 | 75 | 1000 | 10000 | 702.41 | stop |
| 5 | judge | low | 634 | 409 | 131 | 1000 | 10000 | 803.58 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Total evaluation latency_ms: 2014.82

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2312 | 2087 | 132 | 3000 | 10000 | 891.14 | stop |
| 2 | judge | low | 616 | 391 | 115 | 1000 | 10000 | 955.72 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Total evaluation latency_ms: 1685.47

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2356 | 2131 | 103 | 3000 | 10000 | 752.64 | stop |
| 2 | judge | low | 617 | 392 | 79 | 1000 | 10000 | 751.79 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Total evaluation latency_ms: 1897.95

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2176 | 1951 | 152 | 3000 | 10000 | 895.88 | stop |
| 2 | judge | low | 616 | 391 | 115 | 1000 | 10000 | 810.87 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Total evaluation latency_ms: 3876.67

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 851 | 3000 | 10000 | 3691.76 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) framework that enhances large language models by integrating graph‑structured text indexing and a dual‑level retrieval mechanism, addressing the flat‑data representations and fragmented answers of existing RAG systems[C1][C2].  
The system performs **low‑level retrieval** (precise entity and relationship information) and **high‑level retrieval** (broader topics and themes), allowing it to capture complex inter‑dependencies among entities and deliver more coherent, context‑rich responses[C2].  
Key contributions include (i) the incorporation of graph‑based knowledge structures for comprehensive information retrieval, (ii) improved retrieval efficiency that reduces response times, and (iii) an incremental update algorithm that enables rapid adaptation to new data in dynamic environments[C2].  
LightRAG’s code has been released as open‑source software on GitHub[C1].  

Experimental evaluation on four domains—Agriculture, Computer Science (CS), Legal, and a mixed set—shows that LightRAG consistently outperforms the NaiveRAG baseline across multiple metrics. For example, in the Agriculture domain LightRAG achieves 67.6 % comprehensiveness versus 32.4 % for NaiveRAG, and 76.4 % diversity versus 23.6 % for NaiveRAG; similar gains are observed for empowerment and overall scores across all domains[C3][C4].  

The datasets used contain 12 Agriculture documents (2,017,886 tokens), 10 CS documents (2,306,535 tokens), 94 Legal documents (5,081,069 tokens), and 61 mixed‑domain documents (619,009 tokens)[C5].  
The methodology details how large language models extract entities and relationships from these documents, the prompt templates employed, and the evaluation dimensions used to compare LightRAG against baselines[C5].  
A concrete retrieval‑augmented generation example (Figure 3) demonstrates the process: given the query “What metrics are most informative for evaluating movie recommendation systems?”, the LLM extracts low‑ and high‑level keywords that guide the dual‑level retrieval before generation[C5].  </pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Lookup; expected: Global

Standalone Question: 這篇在講什麼？

Sub-queries: []

Total evaluation latency_ms: 2895.11

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2729 | 2504 | 608 | 3000 | 10000 | 2736.01 | stop |

### Finalized answer

<pre>這篇文件主要介紹 **LightRAG**——一種結合圖結構與向量表示的檢索增強生成（Retrieval‑Augmented Generation）框架。  
- 文章先以「Beekeeper」實體說明如何從原始文本中抽取實體、屬性與關係，並展示系統的整體架構圖[C1]。  
- 接著闡述 **雙層檢索範式（dual‑level retrieval paradigm）**，將查詢分為 **低層檢索（Low‑Level Retrieval）**（針對具體實體及其屬性）與 **高層檢索（High‑Level Retrieval）**（聚合多個實體以回應抽象、概念性問題），並說明系統如何同時支援 **Specific Queries**（具體實體查詢）與 **Abstract Queries**（概念性、主題性查詢）[C2]。  
- 為了驗證 LightRAG 的效能，文件列出在多個資料集上與 **Naive RAG、RQ‑RAG、HyDE** 等最先進基線的比較實驗，說明評估方法與產生的問題集[C3]。  
- 最後提供相關參考文獻，涵蓋圖‑文本嵌入、RAG 系統與圖神經網路等領域的最新研究[C4][C5]。  

總結來說，本文探討如何透過圖‑向量混合、雙層檢索機制提升 RAG 系統在處理具體與抽象查詢時的準確性與概念化能力。</pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Lookup; expected: Global

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Total evaluation latency_ms: 2144.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2345 | 2120 | 449 | 3000 | 10000 | 1931.04 | stop |

### Finalized answer

<pre>- **LightRAG introduces graph‑based text indexing**: documents are segmented, entities and their relationships are extracted with LLMs, and a knowledge graph \( \hat D = (\hat V,\hat E) \) is built to capture global inter‑dependencies [C3].

- **Dual‑level retrieval (low‑level and high‑level) is employed**: the system first extracts low‑level and high‑level keywords from the query, then uses both levels to retrieve relevant pieces from the graph‑enhanced index, improving comprehensiveness [C2][C1].

- **Integration of graph structures with vector representations** enables efficient retrieval of related entities and their relationships, leading to faster response times while preserving contextual relevance [C1].

- **An incremental update algorithm keeps the index current**: new data can be incorporated quickly, allowing LightRAG to stay effective in rapidly changing environments [C1].

- **Extensive experiments show considerable gains in retrieval accuracy and efficiency** compared with existing RAG approaches, and a case‑study demonstrates LightRAG’s superiority over a baseline NaiveRAG in terms of comprehensiveness, diversity, and empowerment [C5].

- **The framework is open‑source** and publicly available at https://github.com/HKUDS/LightRAG [C1].</pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 4440.10

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 1056 | 3000 | 10000 | 4258.80 | stop |

### Finalized answer

<pre>**Overall performance**

- LightRAG consistently achieves higher win‑rates than GraphRAG on all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) across the datasets reported. For the first dataset LightRAG’s scores are 54.4 % vs 45.6 % (Comprehensiveness), 77.2 % vs 22.8 % (Diversity), 58.8 % vs 41.2 % (Empowerment) and 54.8 % vs 45.2 % (Overall); similar advantages appear in the remaining datasets [C2].

**Diversity and large‑scale corpora**

- LightRAG shows a pronounced lead in the Diversity metric, especially on the large Legal dataset, indicating it can generate a wider range of responses where diverse content is critical [C3].
- In the biggest corpora (Agriculture, CS, Legal), which contain millions of tokens and complex language, LightRAG markedly outperforms GraphRAG, highlighting its strength in handling extensive, intricate knowledge bases [C3].

**Mechanistic differences**

- Both systems are graph‑enhanced RAG approaches, but GraphRAG extracts entities and relationships, aggregates nodes into communities, and answers high‑level queries by traversing those communities [C1].
- LightRAG employs a dual‑level retrieval paradigm that combines low‑level retrieval of specific entities with high‑level retrieval of broader topics. This hierarchical, graph‑based indexing is credited with its superior comprehensiveness, diversity, and empowerment [C1][C3].

**Conclusion**

Taken together, the quantitative results and qualitative analysis indicate that LightRAG surpasses GraphRAG in overall answer quality, especially in diversity and complex‑query handling on large‑scale datasets, thanks to its dual‑level, graph‑based retrieval architecture. [C2][C3][C1]</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 1959.78

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2479 | 2254 | 172 | 3000 | 10000 | 1754.27 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Lookup; expected: Synthesis

Standalone Question: How do the experiments support the paper&#x27;s claims?

Sub-queries: []

Total evaluation latency_ms: 3600.69

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2692 | 2467 | 706 | 3000 | 10000 | 3403.63 | stop |

### Finalized answer

<pre>The experimental results directly demonstrate the advantages claimed for LightRAG.

* **Higher win‑rates across all evaluation dimensions** – Table 1 shows that LightRAG consistently achieves substantially larger win‑rates than the NaïveRAG, RQ‑RAG and HyDE baselines on the four datasets (Agriculture, CS, Legal, Mix) for comprehensiveness, diversity, empowerment and overall performance, with win‑rates ranging from ≈ 60 % to ≈ 86 % compared with the baselines’ 15 %–38 % [C1].

* **Ablation study confirms the contribution of each component** – Table 2 compares the full LightRAG model with NaïveRAG under “high‑retrieval” and “low‑retrieval” settings. Even when retrieval is weakened, LightRAG still outperforms the NaïveRAG reference, indicating that the dual‑level retrieval and entity‑relationship extraction are effective contributors to the observed gains [C2].

* **Qualitative superiority in diversity, empowerment and overall answer quality** – The “Winner” analyses in Section 9 state that LightRAG’s answers are judged superior in diversity (covering a broader set of metrics with nuanced explanations), empowerment (providing deeper insight into metric functions and trade‑offs), and overall comprehensiveness, directly supporting the claim that LightRAG delivers richer, more informative responses than competing methods [C3].

* **Cost‑effectiveness** – Figure 2 (described in the same section) compares token usage and API calls between GraphRAG and LightRAG on the Legal dataset. LightRAG requires far fewer tokens (≈ 1 400 × 2 versus 610 × 1 000 for GraphRAG) and fewer API calls, confirming the claim that LightRAG is more economical while maintaining performance [C3].

* **Robustness across diverse data scales** – The dataset statistics in Table 4 show that experiments were conducted on four corpora of varying size (from 12 to 94 documents and 2 M to 5 M tokens). LightRAG’s consistent superiority across these heterogeneous datasets reinforces the claim of broad applicability [C5].

Together, these quantitative and qualitative experiments substantiate the paper’s central assertions that LightRAG improves retrieval‑augmented generation in terms of accuracy, answer richness, and computational efficiency.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 5143.06

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1503 | 3000 | 10000 | 4924.35 | stop |

### Finalized answer

<pre>**Ablated‑version results (using NaiveRAG as the reference)**  

| Domain | Metric | NaiveRAG | LightRAG (ablated) |
|--------|--------|----------|--------------------|
| **Agriculture** | Comprehensiveness | 32.4 % | 67.6 % |
| | Diversity | 23.6 % | 76.4 % |
| | Empowerment | 32.4 % | 67.6 % |
| | Overall | 32.4 % | 67.6 % |
| **CS** | Comprehensiveness | 38.4 % | 61.6 % |
| | Diversity | 38.0 % | 62.0 % |
| | Empowerment | 38.8 % | 61.2 % |
| | Overall | 38.8 % | 61.2 % |
| **Legal** | Comprehensiveness | 16.4 % | 83.6 % |
| | Diversity | 13.6 % | 86.4 % |
| | Empowerment | 16.4 % | 83.6 % |
| | Overall | 15.2 % | 84.8 % |
| **Mix** | Comprehensiveness | 38.8 % | 61.2 % |
| | Diversity | 32.4 % | 67.6 % |
| | Empowerment | 42.8 % | 57.2 % |
| | Overall | 40.0 % | 60.0 % |

**High‑ablation setting (NaiveRAG‑High vs. LightRAG‑High)**  

| Domain | Metric | NaiveRAG‑High | LightRAG‑High |
|--------|--------|---------------|---------------|
| Agriculture | Comprehensiveness | 34.8 % | 65.2 % |
| | Diversity | 27.2 % | 72.8 % |
| | Empowerment | 36.0 % | 64.0 % |
| | Overall | 35.2 % | 64.8 % |
| CS | Comprehensiveness | 42.8 % | 57.2 % |
| | Diversity | 36.8 % | 63.2 % |
| | Empowerment | 42.4 % | 57.6 % |
| | Overall | 44.0 % | 56.0 % |
| Legal | Comprehensiveness | 23.6 % | 76.4 % |
| | Diversity | 16.8 % | 83.2 % |
| | Empowerment | 22.8 % | 77.2 % |
| | Overall | 22.0 % | 78.0 % |
| Mix | Comprehensiveness | 40.4 % | 59.6 % |
| | Diversity | 36.0 % | 64.0 % |
| | Empowerment | 47.6 % | 52.4 % |
| | Overall | 42.4 % | 57.6 % |

**Low‑ablation setting** – the table lists only the NaiveRAG‑Low columns (no LightRAG‑Low values are provided in the excerpt).  

All figures are taken directly from Table 2 of the paper, which reports the performance of the ablated LightRAG variants across four evaluation dimensions and four data domains [C3].</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Standalone Question: What datasets were used?

Sub-queries: []

Total evaluation latency_ms: 1141.87

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2641 | 2416 | 126 | 3000 | 10000 | 925.16 | stop |

### Finalized answer

<pre>The experiments used four UltraDomain benchmark datasets: **Agriculture**, **CS** (computer science), **Legal**, and **Mix**[C1][C5].</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Sub-queries: []

Total evaluation latency_ms: 5815.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2528 | 2303 | 1437 | 3000 | 10000 | 5642.14 | stop |

### Finalized answer

<pre>55.6% [C4]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Total evaluation latency_ms: 1001.78

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2156 | 1931 | 101 | 3000 | 10000 | 761.85 | stop |

### Finalized answer

<pre>LightRAG needs just a single API call for the entire retrieval phase[C3].</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Standalone Question: 那 LightRAG 呢？

Sub-queries: []

Total evaluation latency_ms: 3576.32

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2144 | 1919 | 662 | 3000 | 10000 | 3431.86 | stop |

### Finalized answer

<pre>LightRAG 是一种 **图结构增强的检索‑生成（RAG）系统**，它在文本索引和检索阶段引入了知识图谱，以克服传统 RAG 仅使用平面向量表示导致的上下文碎片化问题[C1]。  

- **双层检索范式**：系统同时进行低层（具体实体）和高层（抽象概念）检索，能够从细粒度和全局视角捕获信息[C1]。  
- **图‑向量融合**：通过将实体及其关系的图结构与向量表示相结合，实现对相关实体及其关联的高效检索，提升响应速度并保持上下文相关性[C1]。  
- **增量更新算法**：支持对新数据的及时加入，使系统在快速变化的数据环境中保持有效和响应迅速[C1]。  
- **性能优势**：在全面性、 多样性、赋能性和整体表现四个评估维度上，LightRAG 均显著优于传统的纯块检索方法（如 NaiveRAG、HyDE、RQRAG），在大规模语料（如 Legal 数据集）中胜率可达约 50% 以上，体现了图‑增强 RAG 在捕获复杂语义依赖方面的优势[C3]。  
- **实际效果**：实验表明 LightRAG 在机器学习指标覆盖范围更广、信息多样性更高、内容更具赋能作用，归功于其层次化检索范式和精准的实体‑关系抽取能力[C4]。  
- **效率与成本**：通过知识图谱实现快速、相关的文档检索，双层检索满足不同用户需求，同时降低了 LLM 推理成本，整体提升了检索与生成的速度和质量[C5]。  

综上，LightRAG 通过图结构索引、双层检索和增量更新，实现了在大规模、复杂查询场景下的高效、全面且具备赋能性的检索‑生成能力。</pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Lookup; expected: Synthesis

Standalone Question: 那它跟 GraphRAG 比呢？

Sub-queries: []

Total evaluation latency_ms: 2812.09

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2619 | 2394 | 678 | 3000 | 10000 | 2684.54 | stop |

### Finalized answer

<pre>LightRAG 在各项评估维度上均优于 GraphRAG。  
- 在 **Comprehensiveness、Diversity、Empowerment** 以及 **Overall** 四个维度的胜率上，LightRAG 的得分均高于 GraphRAG（例如，Comprehensiveness 为 54.4% vs 45.6%，Diversity 为 77.2% vs 22.8% 等）[C2]。  
- 在具体答案比较中，LightRAG 被评为 **Diversity、Empowerment** 以及 **Overall** 的获胜者，说明其在提供多样化、赋能读者以及整体质量方面更具优势[C3]。  
- **成本方面**，检索阶段 LightRAG 只使用不到 100 个 token 并仅需一次 API 调用，而 GraphRAG 需要 610 × 1,000 = 610,000 个 token 并产生数百次 API 调用，导致显著的检索开销[C4]。  
- 在 **增量更新** 阶段，LightRAG 只需将新抽取的实体和关系并入已有图结构，几乎没有额外开销；而 GraphRAG 必须拆除并重新生成全部社区报告，代价约为 1,399 × 2 × 5,000 ≈ 14 百万 token，成本极高[C5]。  

综上，LightRAG 在回答质量和运行成本两方面均显著优于 GraphRAG。</pre>

## JUDGE_ASSERTED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Total evaluation latency_ms: 0.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 634 | 409 | 85 | 1000 | 10000 | 895.22 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Total evaluation latency_ms: 0.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 648 | 423 | 114 | 1000 | 10000 | 755.25 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
