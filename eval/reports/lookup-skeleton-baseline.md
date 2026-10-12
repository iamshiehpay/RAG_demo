# Golden Facts evaluation

Created: 2026-10-12T15:09:31.748999+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Label: lookup-skeleton

Revision: 980c45e8eb1c2efdfd8de90def085babc035ca53

Uncommitted changes: no

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: #06 exported cases if available; otherwise fixed spike cases

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 0/1 (0.0%) |
| Q1 | motivation | judge | 0/1 (0.0%) |
| Q1 | graph_indexing | judge | 0/1 (0.0%) |
| Q1 | dual_level | judge | 1/1 (100.0%) |
| Q1 | incremental_update | judge | 0/1 (0.0%) |
| Q1 | experiments | judge | 0/1 (0.0%) |
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
| Q3 | low_term | contains | 0/1 (0.0%) |
| Q3 | origin_term | contains | 0/1 (0.0%) |
| Q3 | table2_baseline | judge | 0/1 (0.0%) |
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
| ABSENT_HOTPOT | fixed_reply | judge | 1/1 (100.0%) |
| ABSENT_LICENSE | question_type | events | 1/1 (100.0%) |
| ABSENT_LICENSE | fixed_reply | judge | 1/1 (100.0%) |
| ABSENT_GPU | question_type | events | 1/1 (100.0%) |
| ABSENT_GPU | fixed_reply | judge | 1/1 (100.0%) |
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

Total evaluation latency_ms: 13696.65

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The system combines low‑level retrieval (precise entity‑level information) with high‑level retrieval (broader topics) |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The authors evaluate LightRAG on four heterogeneous datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens) [C5].<br><br>Performance is measured across three dimensions—Comprehensiveness, Diversity, and Empowerment—and an aggregated Overall score. Using NaiveRAG as the reference baseline, LightRAG consistently achieves higher percentages in all dimensions. For example, in the “Mix” domain, LightRAG attains 61.2 % Comprehensiveness versus 38.8 % for NaiveRAG, 67.6 % Diversity versus 32.4 %, 57.2 % Empowerment versus 42.8 %, and an Overall score of 60.0 % versus 40.0 % [C3]. Similar gains are observed across the other domains and under different ablation settings (High, Low, Origin), confirming that the graph‑vector integration and dual‑level retrieval improve both accuracy and efficiency [C3][C4]. |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 594 | 3000 | 10000 | 4346.17 | stop |
| 2 | judge | low | 1122 | 897 | 132 | 1000 | 10000 | 1772.08 | stop |
| 3 | judge | low | 1117 | 892 | 100 | 1000 | 10000 | 959.70 | stop |
| 4 | judge | low | 1119 | 894 | 125 | 1000 | 10000 | 1531.33 | stop |
| 5 | judge | low | 1125 | 900 | 117 | 1000 | 10000 | 1522.65 | stop |
| 6 | judge | low | 1134 | 909 | 434 | 1000 | 10000 | 2551.23 | stop |
| 7 | judge | low | 1118 | 893 | 73 | 1000 | 10000 | 785.78 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism. The system combines low‑level retrieval (precise entity‑level information) with high‑level retrieval (broader topics) to capture complex inter‑dependencies among entities, thereby producing more coherent and context‑rich responses [C1][C2].  

The authors evaluate LightRAG on four heterogeneous datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens) [C5].  

Performance is measured across three dimensions—Comprehensiveness, Diversity, and Empowerment—and an aggregated Overall score. Using NaiveRAG as the reference baseline, LightRAG consistently achieves higher percentages in all dimensions. For example, in the “Mix” domain, LightRAG attains 61.2 % Comprehensiveness versus 38.8 % for NaiveRAG, 67.6 % Diversity versus 32.4 %, 57.2 % Empowerment versus 42.8 %, and an Overall score of 60.0 % versus 40.0 % [C3]. Similar gains are observed across the other domains and under different ablation settings (High, Low, Origin), confirming that the graph‑vector integration and dual‑level retrieval improve both accuracy and efficiency [C3][C4].  

An incremental update algorithm allows LightRAG to incorporate new data quickly, keeping the system responsive in dynamic environments [C1]. The framework’s implementation, including entity and relationship extraction prompts for large language models, is detailed in the appendix [C5]. LightRAG’s code has been open‑sourced on GitHub [C1].  

Overall, the document presents LightRAG as a fast, scalable, and graph‑empowered RAG system that outperforms a flat‑representation baseline (NaiveRAG) across multiple domains and evaluation metrics.</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 13500.57

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | FAIL | Required claim not asserted |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | The quantitative results in the paper show that LightRAG consistently achieves higher win‑rates than GraphRAG across all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) and across the four test corpora (Agriculture, CS, Legal, and a fourth dataset).  <br><br>- In the **Comprehensiveness** column, LightRAG’s win‑rates range from 48.4 % to 54.4 %, whereas GraphRAG’s range is 40.4 % to 45.6 %[C2].  <br>- For **Diversity**, LightRAG scores between 59.2 % and 77.2 %, while GraphRAG’s scores lie between 22.8 % and 40.8 %[C2].  <br>- In **Empowerment**, LightRAG’s win‑rates are 54.8 %– 58.8 %, compared with GraphRAG’s 41.2 %– 45.2 %[C2].  <br>- The **Overall** metric follows the same pattern: LightRAG attains 49.6 %– 54.8 % versus GraphRAG’s 45.2 %– 48.0 %[C2].  <br><br>These figures demonstrate that LightRAG outperforms GraphRAG on every metric and in every dataset. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 923 | 3000 | 10000 | 5689.10 | stop |
| 2 | judge | low | 1383 | 1158 | 160 | 1000 | 10000 | 1260.72 | stop |
| 3 | judge | low | 1420 | 1195 | 57 | 1000 | 10000 | 1405.61 | stop |
| 4 | judge | low | 1380 | 1155 | 100 | 1000 | 10000 | 838.63 | stop |
| 5 | judge | low | 1419 | 1194 | 170 | 1000 | 10000 | 1184.81 | stop |
| 6 | judge | low | 1401 | 1176 | 143 | 1000 | 10000 | 1089.83 | stop |
| 7 | judge | low | 1381 | 1156 | 438 | 1000 | 10000 | 1861.69 | stop |

### Finalized answer

<pre>**Overall performance**

The quantitative results in the paper show that LightRAG consistently achieves higher win‑rates than GraphRAG across all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) and across the four test corpora (Agriculture, CS, Legal, and a fourth dataset).  

- In the **Comprehensiveness** column, LightRAG’s win‑rates range from 48.4 % to 54.4 %, whereas GraphRAG’s range is 40.4 % to 45.6 %[C2].  
- For **Diversity**, LightRAG scores between 59.2 % and 77.2 %, while GraphRAG’s scores lie between 22.8 % and 40.8 %[C2].  
- In **Empowerment**, LightRAG’s win‑rates are 54.8 %– 58.8 %, compared with GraphRAG’s 41.2 %– 45.2 %[C2].  
- The **Overall** metric follows the same pattern: LightRAG attains 49.6 %– 54.8 % versus GraphRAG’s 45.2 %– 48.0 %[C2].  

These figures demonstrate that LightRAG outperforms GraphRAG on every metric and in every dataset.

**Reasons for LightRAG’s advantage**

The authors attribute LightRAG’s superiority to its **dual‑level retrieval paradigm**. LightRAG combines low‑level retrieval of specific entities with high‑level retrieval of broader topics, leveraging graph‑based text indexing to capture both detailed and abstract information. This mechanism yields a “significant advantage in the Diversity metric, particularly within the larger Legal dataset” and “enhances response variety and complex‑query handling”[C3].  

In contrast, GraphRAG relies on a single‑level graph‑enhanced retrieval that extracts entities and relationships but does not employ the same hierarchical retrieval strategy, leading to comparatively lower performance, especially on large‑scale corpora with millions of tokens[C3].

**Qualitative description**

Both systems use an LLM (GPT‑4o‑mini) for entity extraction and graph construction, and both operate on a nano vector database with a fixed chunk size of 1200 tokens[C1]. However, LightRAG’s additional hierarchical retrieval layer enables it to “traverse communities” more effectively and produce more comprehensive answers, which is reflected in the higher win‑rates across all evaluation dimensions[C1][C3].  

**Summary**

- **Performance:** LightRAG beats GraphRAG on Comprehensiveness, Diversity, Empowerment, and Overall win‑rates in every dataset examined.  
- **Mechanism:** LightRAG’s dual‑level (low‑level + high‑level) retrieval and graph‑based indexing give it a broader contextual grasp and greater response diversity, especially for large, complex corpora.  
- **Implication:** For tasks requiring thorough, diverse, and empowering answers—particularly on large‑scale datasets—LightRAG is the more effective graph‑enhanced RAG system.  

All statements are drawn directly from the supplied document excerpts.</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 15429.56

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | FAIL | Term missing |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | FAIL | Required claim not asserted |  |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1701 | 3000 | 10000 | 7350.32 | stop |
| 2 | judge | low | 1583 | 1358 | 151 | 1000 | 10000 | 1219.97 | stop |
| 3 | judge | low | 1584 | 1359 | 102 | 1000 | 10000 | 1624.17 | stop |
| 4 | judge | low | 1595 | 1370 | 268 | 1000 | 10000 | 1800.27 | stop |
| 5 | judge | low | 1595 | 1370 | 173 | 1000 | 10000 | 2219.43 | stop |
| 6 | judge | low | 1571 | 1346 | 94 | 1000 | 10000 | 1034.94 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (using NaiveRAG as the reference baseline)**  

| Dataset | Metric | NaiveRAG (baseline) | LightRAG (ablated) |
|--------|--------|---------------------|--------------------|
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

*These figures compare the original NaiveRAG system with the ablated LightRAG version (i.e., LightRAG with certain components removed). LightRAG consistently achieves higher percentages across all four evaluation dimensions and all four domains.*  

**High‑level‑only ablation (NaiveRAG‑High vs. LightRAG)**  

| Dataset | Metric | NaiveRAG‑High | LightRAG (high‑level ablation) |
|--------|--------|--------------|---------------------------------|
| **Agriculture** | Comprehensiveness | 34.8 % | 65.2 % |
| | Diversity | 27.2 % | 72.8 % |
| | Empowerment | 36.0 % | 64.0 % |
| | Overall | 35.2 % | 64.8 % |
| **CS** | Comprehensiveness | 42.8 % | 57.2 % |
| | Diversity | 36.8 % | 63.2 % |
| | Empowerment | 42.4 % | 57.6 % |
| | Overall | 44.0 % | 56.0 % |
| **Legal** | Comprehensiveness | 23.6 % | 76.4 % |
| | Diversity | 16.8 % | 83.2 % |
| | Empowerment | 22.8 % | 77.2 % |
| | Overall | 22.0 % | 78.0 % |
| **Mix** | Comprehensiveness | 40.4 % | 59.6 % |
| | Diversity | 36.0 % | 64.0 % |
| | Empowerment | 47.6 % | 52.4 % |
| | Overall | 42.4 % | 57.6 % |

*These results show that even when only the high‑level retrieval component is retained, LightRAG still outperforms the NaiveRAG baseline across all metrics and domains.*  

All numbers are taken from Table 2 in the paper, which reports the performance of ablated LightRAG versions using NaiveRAG as the reference point[C3].</pre>

## ZH_COST — repetition 1

Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Sub-queries: []

Total evaluation latency_ms: 8600.46

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| chinese_answer | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。  <br>在檢索階段，GraphRAG 必須先產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000）且因為需要逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索成本極低[C4]。 |
| retrieval_cost | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。  <br>在檢索階段，GraphRAG 必須先產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000）且因為需要逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索成本極低[C4]。 |
| numbers_unchanged | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 必須先產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000）且因為需要逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2625 | 2400 | 469 | 3000 | 10000 | 3930.65 | stop |
| 2 | judge | low | 948 | 723 | 258 | 1000 | 10000 | 1209.87 | stop |
| 3 | judge | low | 995 | 770 | 464 | 1000 | 10000 | 1865.37 | stop |
| 4 | judge | low | 980 | 755 | 339 | 1000 | 10000 | 1412.51 | stop |

### Finalized answer

<pre>LightRAG 的檢索成本遠低於 GraphRAG。  
在檢索階段，GraphRAG 必須先產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000）且因為需要逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索成本極低[C4]。  

此外，LightRAG 透過結合圖結構與向量化表示，避免了在檢索前處理大量資訊的需求，進一步降低了檢索階段的資源消耗[C5]。  

因此，兩者的主要差異在於：GraphRAG 需要大量 token（數十萬）與多次 API 呼叫，而 LightRAG 僅使用少量 token（&lt;100）與單一次 API 呼叫，檢索成本相差數個量級。</pre>

## LIMITATIONS — repetition 1

Question: 這篇論文有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: 這篇論文有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 4817.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| citation_sections | events | FAIL | 0 distinct cited Sections; requires 2 |  |
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| evaluation_limit | judge | FAIL | Required claim not asserted |  |
| retrieval_tradeoff | judge | FAIL | Required claim not asserted |  |
| not_universally_best | judge | FAIL | Required claim not asserted |  |
| no_invented_limit | forbidden | PASS | Exact fixed refusal contains no asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2565 | 2340 | 204 | 3000 | 10000 | 1215.06 | stop |
| 2 | judge | low | 677 | 452 | 63 | 1000 | 10000 | 1333.14 | stop |
| 3 | judge | low | 694 | 469 | 65 | 1000 | 10000 | 1229.53 | stop |
| 4 | judge | low | 677 | 452 | 62 | 1000 | 10000 | 863.69 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Total evaluation latency_ms: 4281.39

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2312 | 2087 | 132 | 3000 | 10000 | 971.76 | stop |
| 2 | judge | low | 660 | 435 | 111 | 1000 | 10000 | 933.83 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Total evaluation latency_ms: 4432.42

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | Not mentioned in the document. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2356 | 2131 | 86 | 3000 | 10000 | 1460.82 | stop |
| 2 | judge | low | 661 | 436 | 108 | 1000 | 10000 | 766.72 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Total evaluation latency_ms: 3935.48

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2176 | 1951 | 169 | 3000 | 10000 | 1090.57 | stop |
| 2 | judge | low | 660 | 435 | 101 | 1000 | 10000 | 776.66 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Total evaluation latency_ms: 4623.63

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 495 | 3000 | 10000 | 2350.98 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism (low‑level for specific entities and relationships, high‑level for broader topics) to capture complex inter‑dependencies and produce more coherent, context‑rich responses[C1][C2].  
The system integrates graph structures with vector representations, enabling efficient retrieval of related entities and their relations while supporting rapid incremental updates for new data[C1][C2].  
Experimental results on four domains (Agriculture, CS, Legal, Mix) show that LightRAG substantially outperforms the NaiveRAG baseline across three evaluation dimensions—Comprehensiveness, Diversity, and Empowerment—and in overall scores; for example, in the Agriculture domain LightRAG achieves 67.6 % overall versus 32.4 % for NaiveRAG, and similar gains are observed in the other domains[C3][C4].  
The datasets used comprise 12 Agriculture documents (≈2.02 M tokens), 10 CS documents (≈2.31 M tokens), 94 Legal documents (≈5.08 M tokens), and 61 Mix documents (≈0.62 M tokens)[C5].  
LightRAG’s methodology, including entity/relationship extraction, prompt templates, and evaluation criteria, is detailed in the appendix, and the full implementation is released as open‑source software at https://github.com/HKUDS/LightRAG[C1].</pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Lookup; expected: Global

Standalone Question: 這篇在講什麼？

Sub-queries: []

Total evaluation latency_ms: 6616.86

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2729 | 2504 | 633 | 3000 | 10000 | 3972.09 | stop |

### Finalized answer

<pre>這篇文件介紹了 **LightRAG** 框架——一種結合圖結構與向量表示的檢索增強生成（Retrieval‑Augmented Generation）模型。  
- 透過 **雙層檢索範式**（low‑level 與 high‑level）同時支援 **具體查詢**（針對特定實體與屬性）與 **抽象查詢**（概念性、主題性問題）[C2]。  
- 系統先從查詢中抽取 **局部關鍵字** 與 **全域關鍵字**，再分別以向量資料庫匹配實體與關聯，利用圖‑向量的協同提升檢索相關性[C2]。  
- 文件展示了以 **“Beekeeper（養蜂人）”** 為例的實體與關係抽取過程，說明如何從原始文本中生成實體類型、描述與關聯資訊，並以圖形索引支援檢索[​C1]。  
- 為評估 LightRAG 的高層次意義建構（sensemaking）能力，作者將其與 Naive RAG、RQ‑RAG、HyDE 等多個最新基線模型進行比較，並在多個資料集上產生 125 題測試問題[​C3]。  
- 最後列出相關研究與技術參考文獻，涵蓋圖‑文本嵌入、RAG 評估與圖神經網路等領域[​C4]。  

總結來說，本文說明了 LightRAG 如何透過圖與向量的結合，提供從低層實體檢索到高層概念摘要的多層次檢索能力，並在實驗中證明其相較於現有 RAG 方法的優勢。</pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Lookup; expected: Global

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Total evaluation latency_ms: 2432.02

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2345 | 2120 | 494 | 3000 | 10000 | 2265.67 | stop |

### Finalized answer

<pre>- LightRAG is a Retrieval‑Augmented Generation (RAG) framework that integrates **graph structures** into the text indexing and retrieval pipeline, enabling the system to capture entities and their relationships rather than relying on flat representations[C1].  

- The architecture consists of a **dual‑level retrieval system**: a low‑level retriever for fine‑grained keywords and a high‑level retriever for broader concepts, which together provide more comprehensive information coverage[C2].  

- LightRAG’s **graph‑based text indexing** segments documents, extracts entities and relationships with LLMs, deduplicates them, and builds a knowledge graph ( \(\hat D = (\hat V,\hat E)\) ) that supports efficient discovery of both specific entities and overarching themes[C2].  

- An **incremental update algorithm** allows the indexed graph to be refreshed quickly as new data arrives, keeping the system responsive in dynamic environments[C1].  

- Experiments on four datasets (Agriculture, CS, Legal, Mix) show that LightRAG achieves **significant improvements in retrieval accuracy and efficiency** compared with prior RAG approaches[C3].  

- The system uses specially designed **prompt templates** for keyword extraction (high‑level vs. low‑level) and for RAG evaluation across the dimensions of comprehensiveness, diversity, and empowerment[C4].  

- A case‑study comparison with a baseline model (NaiveRAG) demonstrates that LightRAG provides **more in‑depth, diverse, and empowering answers**, thanks to its dual‑level retrieval and graph‑enhanced knowledge representation[C5].  

- LightRAG is released as **open‑source software** (GitHub link provided) to facilitate further research and adoption[C1].</pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 3280.05

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 708 | 3000 | 10000 | 3142.44 | stop |

### Finalized answer

<pre>LightRAG generally outperforms GraphRAG across the evaluation dimensions. In the win‑rate tables, LightRAG achieves higher percentages than GraphRAG for comprehensiveness, diversity, empowerment and overall performance on all tested datasets (e.g., 54.4 % vs. 26.0 % in comprehensiveness, 77.2 % vs. 24.0 % in diversity, 74.8 % vs. 25.2 % in empowerment, and 75.2 % vs. 24.8 % overall) [C2]. The authors attribute LightRAG’s advantage to its dual‑level retrieval paradigm, which combines low‑level entity retrieval with high‑level topic retrieval, thereby capturing a fuller context and producing more varied responses, especially in large‑scale corpora such as the Legal dataset [C3]. While GraphRAG also uses a graph‑enhanced RAG approach that extracts entities and relationships and aggregates them into communities for high‑level queries [C1], LightRAG’s hierarchical retrieval and graph‑based indexing give it a clear edge in handling complex, high‑token queries. A case‑study table further highlights LightRAG’s superiority over GraphRAG as a baseline method [C5].</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 1262.26

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2479 | 2254 | 152 | 3000 | 10000 | 1096.88 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Lookup; expected: Synthesis

Standalone Question: How do the experiments support the paper&#x27;s claims?

Sub-queries: []

Total evaluation latency_ms: 4761.77

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2692 | 2467 | 949 | 3000 | 10000 | 4616.09 | stop |

### Finalized answer

<pre>The experimental results directly back the paper’s main claims in three ways:

**1. Quantitative superiority over baselines**  
Table 1 compares LightRAG with three strong baselines (NaiveRAG, RQ‑RAG and HyDE) on four public datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall). In every case LightRAG’s win‑rate is markedly higher—for example, on the Agriculture dataset LightRAG achieves a 67.6 % overall win‑rate versus 32.4 % for NaiveRAG, and on the Legal dataset the overall win‑rate rises from 15.2 % (NaiveRAG) to 84.8 % (LightRAG)[C1]. The same pattern holds for RQ‑RAG and HyDE, confirming that LightRAG consistently outperforms existing RAG methods across domains and metrics.

**2. Robustness through ablation studies**  
Table 2 presents ablated versions of LightRAG (using NaiveRAG as the reference) under “‑High” and “‑Low” settings. Even when components are weakened, LightRAG still maintains higher scores than the NaiveRAG reference across all dimensions (e.g., Overall % = 64.8 % vs 35.2 % in the “‑High” condition)[C2]. This demonstrates that the performance gains are not due to a single fragile component but stem from the overall design.

**3. Qualitative advantages in answer quality**  
The “Winner” analysis in Section 9 shows that LightRAG’s answers are judged superior in Diversity, Empowerment, and Overall quality. Answer 2 (generated by LightRAG) is praised for covering a broader set of metrics, providing nuanced explanations, and empowering readers with deeper insight into metric trade‑offs[C3]. These human‑centric evaluations corroborate the quantitative gains.

**4. Efficiency and cost‑effectiveness**  
Figure 2 (described in the same section) compares token consumption and API calls between GraphRAG and LightRAG on the Legal dataset. LightRAG requires far fewer tokens (≈ 1 400 × 2 vs. 610 × 1 000 for GraphRAG) and fewer API calls, confirming the claim that LightRAG is more economical while delivering higher performance[C3].

**5. Comprehensive experimental setup**  
The paper reports detailed dataset statistics (document counts and token totals) for all four corpora, ensuring that the evaluations cover a range of sizes and domains[C5]. This breadth supports the generality of the reported improvements.

Together, these experiments provide empirical evidence that LightRAG delivers higher accuracy, richer answer content, and lower computational cost than existing retrieval‑augmented generation approaches.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 5287.69

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1367 | 3000 | 10000 | 5110.29 | stop |

### Finalized answer

<pre>**Ablated LightRAG (high‑ablation setting) performance**

| Dataset | Comprehensiveness | Diversity | Empowerment | Overall |
|---------|------------------|----------|-------------|---------|
| Agriculture | 65.2 % | 72.8 % | 64.0 % | 64.8 % |
| CS (Computer Science) | 57.2 % | 63.2 % | 57.6 % | 56.0 % |
| Legal | 76.4 % | 83.2 % | 77.2 % | 78.0 % |
| Mix (mixed domains) | 59.6 % | 64.0 % | 52.4 % | 57.6 % |

These figures are taken from Table 2, which reports the performance of ablated versions of LightRAG (using a “‑High” ablation) compared with NaiveRAG across four benchmark corpora [C3].</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Standalone Question: What datasets were used?

Sub-queries: []

Total evaluation latency_ms: 1050.74

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2641 | 2416 | 126 | 3000 | 10000 | 868.98 | stop |

### Finalized answer

<pre>The experiments used four UltraDomain benchmark datasets: **Agriculture**, **CS** (computer science), **Legal**, and **Mix**[C1][C5].</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Sub-queries: []

Total evaluation latency_ms: 3378.41

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2528 | 2303 | 791 | 3000 | 10000 | 3241.63 | stop |

### Finalized answer

<pre>55.6% [C4]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Total evaluation latency_ms: 1006.70

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2156 | 1931 | 100 | 3000 | 10000 | 836.98 | stop |

### Finalized answer

<pre>LightRAG needs only a single API call for the entire retrieval process[C3]</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Standalone Question: 那 LightRAG 呢？

Sub-queries: []

Total evaluation latency_ms: 4747.20

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2144 | 1919 | 845 | 3000 | 10000 | 4609.34 | stop |

### Finalized answer

<pre>LightRAG 是一种检索增强生成（RAG）系统，它在文本索引和检索过程中引入图结构，使得实体及其关系能够被高效地检索和利用[C1]。该框架采用双层检索范式，既能从低层获取具体信息，又能在高层发现抽象知识，从而满足多样化的用户需求[C5]。系统通过将图结构与向量表示相结合，实现了对相关实体及其关系的快速检索，并配备了增量更新算法，能够在数据快速变化的环境中及时整合新数据，保持高效响应[C1]。  

在实现细节上，LightRAG 使用 nano 向量数据库管理向量数据，所有 LLM 操作默认使用 GPT‑4o‑mini，块大小统一设为 1200，gleaning 参数固定为 1，以保证实验的一致性[C2]。  

实验评估表明，针对大型语料库和复杂查询，LightRAG 在“全面性”“多样性”“赋能”和“整体”四个维度的胜率均显著高于纯块检索的基线方法（如 NaiveRAG、HyDE、RQRAG），在多数数据集上胜率在 50%–75% 之间，尤其在最大数据集（Legal）中优势更为明显[C3]。此外，LightRAG 在机器学习指标覆盖范围更广，能够提供更丰富、多元且具赋能性的答案，体现了其图‑基索引范式在精确实体关系抽取和 LLM 画像方面的优势[C4]。  

综上，LightRAG 通过图‑增强的索引与双层检索机制，在检索准确性、效率以及生成内容的全面性和多样性方面均实现了显著提升[C1][C5]。</pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Lookup; expected: Synthesis

Standalone Question: 那它跟 GraphRAG 比呢？

Sub-queries: []

Total evaluation latency_ms: 3387.96

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2619 | 2394 | 627 | 3000 | 10000 | 3189.92 | stop |

### Finalized answer

<pre>LightRAG 在各项评估维度上均优于 GraphRAG。  
- 在 **Comprehensiveness、Diversity、Empowerment** 以及 **Overall** 四个维度的胜率上，LightRAG 的得分均高于 GraphRAG（例如 Overall 维度 LightRAG 为 54.8% vs 45.2%）[C2]。  
- 在具体的答案质量比较中，LightRAG 被评为在 **Diversity、Empowerment** 以及 **Overall** 三项的获胜答案，评审说明其提供了更丰富的视角、更加深入的解释并能更好地帮助读者做出判断[C3]。  

在 **成本与效率** 方面，LightRAG 也显著优于 GraphRAG：  
- 检索阶段 LightRAG 只使用不到 100 tokens 并只发起一次 API 调用，而 GraphRAG 需要 610 × 1,000 = 610,000 tokens 并产生数百次 API 调用[C4]。  
- 在增量数据更新阶段，LightRAG 直接将新抽取的实体和关系并入现有图结构，无需重新构建社区报告，从而避免了 GraphRAG 需要的约 1,399 × 2 × 5,000 tokens 的巨额开销[C5]。  

综上所述，LightRAG 在答案质量和运行成本两方面均相对于 GraphRAG 表现更佳。</pre>

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
| 1 | judge | low | 673 | 448 | 116 | 1000 | 10000 | 949.40 | stop |

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
| 1 | judge | low | 687 | 462 | 114 | 1000 | 10000 | 1385.94 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
