# Golden Facts evaluation

Created: 2026-10-12T15:45:10.432221+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Label: router-integrated

Revision: eada653f02b0dc9bf7033215c3f9a33ef3dc3c9c

Uncommitted changes: no

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: chat_document.router_regression.CASES (#06 canonical 12 cases)

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 0/1 (0.0%) |
| Q1 | motivation | judge | 0/1 (0.0%) |
| Q1 | graph_indexing | judge | 0/1 (0.0%) |
| Q1 | dual_level | judge | 1/1 (100.0%) |
| Q1 | incremental_update | judge | 0/1 (0.0%) |
| Q1 | experiments | judge | 0/1 (0.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 0/1 (0.0%) |
| Q2 | question_type | events | 0/1 (0.0%) |
| Q2 | retrieval_methods | judge | 0/1 (0.0%) |
| Q2 | retrieval_cost | judge | 0/1 (0.0%) |
| Q2 | incremental_update | judge | 0/1 (0.0%) |
| Q2 | table1_agriculture_overall | judge | 0/1 (0.0%) |
| Q2 | table1_cs_overall | judge | 0/1 (0.0%) |
| Q2 | table1_legal_overall | judge | 0/1 (0.0%) |
| Q2 | table1_mix_overall | judge | 0/1 (0.0%) |
| Q2 | table3_case_study | judge | 0/1 (0.0%) |
| Q2 | not_all_datasets | forbidden | 1/1 (100.0%) |
| Q3 | table2_citation | events | 1/1 (100.0%) |
| Q3 | question_type | events | 1/1 (100.0%) |
| Q3 | high_term | contains | 1/1 (100.0%) |
| Q3 | low_term | contains | 1/1 (100.0%) |
| Q3 | origin_term | contains | 0/1 (0.0%) |
| Q3 | table2_baseline | judge | 0/1 (0.0%) |
| Q3 | ablation_meaning | judge | 0/1 (0.0%) |
| Q3 | mix_low_overall | judge | 0/1 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/1 (0.0%) |
| Q3 | not_all_best | forbidden | 0/1 (0.0%) |
| ROUTER_01 | question_type | events | 0/1 (0.0%) |
| ROUTER_02 | question_type | events | 0/1 (0.0%) |
| ROUTER_03 | question_type | events | 0/1 (0.0%) |
| ROUTER_04 | question_type | events | 0/1 (0.0%) |
| ROUTER_05 | question_type | events | 0/1 (0.0%) |
| ROUTER_06 | question_type | events | 1/1 (100.0%) |
| ROUTER_07 | question_type | events | 1/1 (100.0%) |
| ROUTER_08 | question_type | events | 1/1 (100.0%) |
| ROUTER_09 | question_type | events | 1/1 (100.0%) |
| ROUTER_10 | question_type | events | 1/1 (100.0%) |
| ROUTER_11 | question_type | events | 1/1 (100.0%) |
| ROUTER_11 | history_supported | events | 1/1 (100.0%) |
| ROUTER_12 | question_type | events | 0/1 (0.0%) |
| ROUTER_12 | history_supported | events | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q1 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Ask latency_ms: 4621.73

Judge latency_ms: 8384.94

Total evaluation latency_ms: 13015.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The system uses low‑level retrieval for precise entity‑level information and high‑level retrieval for broader topics |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Experimental evaluation on four datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens)—shows that LightRAG substantially outperforms a baseline NaiveRAG across multiple dimensions. ... Similar gains are observed for comprehensiveness, diversity, and empowerment, indicating more comprehensive and diverse retrieval results |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 568 | 223 | 38 | 600 | 10000 | 1328.76 | stop |
| 2 | answer | medium | 2421 | 2196 | 515 | 3000 | 10000 | 3095.88 | stop |
| 3 | judge | low | 991 | 766 | 87 | 1000 | 10000 | 1489.57 | stop |
| 4 | judge | low | 986 | 761 | 112 | 1000 | 10000 | 1005.35 | stop |
| 5 | judge | low | 988 | 763 | 118 | 1000 | 10000 | 974.72 | stop |
| 6 | judge | low | 994 | 769 | 95 | 1000 | 10000 | 922.68 | stop |
| 7 | judge | low | 997 | 772 | 244 | 1000 | 10000 | 2108.91 | stop |
| 8 | judge | low | 994 | 769 | 117 | 1000 | 10000 | 970.89 | stop |
| 9 | judge | low | 987 | 762 | 83 | 1000 | 10000 | 912.83 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism. The system uses low‑level retrieval for precise entity‑level information and high‑level retrieval for broader topics, allowing it to capture complex inter‑dependencies among entities and produce more coherent, context‑rich responses [C1][C2]. By integrating graph structures with vector representations, LightRAG enables efficient retrieval of related entities and their relationships, improves response times, and supports rapid incremental updates for dynamic data environments [C1][C2].

Experimental evaluation on four datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens)—shows that LightRAG substantially outperforms a baseline NaiveRAG across multiple dimensions. In the “Overall” metric, LightRAG achieves scores ranging from 60 % to 84.8 % versus NaiveRAG’s 15.2 %–32.4 % across domains [C3][C4]. Similar gains are observed for comprehensiveness, diversity, and empowerment, indicating more comprehensive and diverse retrieval results [C3][C4].

The authors provide an open‑source implementation of LightRAG at https://github.com/HKUDS/LightRAG [C1]. The paper also details the methodology for extracting entities and relationships using large language models, the prompt templates employed, and the evaluation criteria used to benchmark LightRAG against baselines [C5].</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Ask latency_ms: 5542.87

Judge latency_ms: 10748.82

Total evaluation latency_ms: 16315.72

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | its Overall scores are 54.8 % vs. 45.2 % |
| table1_cs_overall | judge | FAIL | Required claim not asserted |  |
| table1_legal_overall | judge | FAIL | Required claim not asserted |  |
| table1_mix_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | * **Metric‑wise performance** – In the win‑rate tables, LightRAG records higher percentages than GraphRAG for Comprehensiveness, Diversity, Empowerment and Overall on most datasets (e.g., LightRAG’s Diversity win rates are 77 % vs. 24 % for GraphRAG, and its Overall scores are 54.8 % vs. 45.2 %)[C2].<br>* **Case‑study reference** – A dedicated case‑study table (Table 3) directly compares LightRAG with GraphRAG, underscoring the focus on their relative performance[C5]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 573 | 228 | 164 | 600 | 10000 | 1817.84 | stop |
| 2 | answer | medium | 2067 | 1842 | 657 | 3000 | 10000 | 3498.43 | stop |
| 3 | judge | low | 992 | 767 | 111 | 1000 | 10000 | 949.46 | stop |
| 4 | judge | low | 1029 | 804 | 53 | 1000 | 10000 | 811.33 | stop |
| 5 | judge | low | 989 | 764 | 99 | 1000 | 10000 | 940.56 | stop |
| 6 | judge | low | 1005 | 780 | 137 | 1000 | 10000 | 1559.14 | stop |
| 7 | judge | low | 1005 | 780 | 105 | 1000 | 10000 | 881.26 | stop |
| 8 | judge | low | 1005 | 780 | 133 | 1000 | 10000 | 1566.89 | stop |
| 9 | judge | low | 1005 | 780 | 117 | 1000 | 10000 | 1014.03 | stop |
| 10 | judge | low | 997 | 772 | 305 | 1000 | 10000 | 1626.77 | stop |
| 11 | judge | low | 990 | 765 | 101 | 1000 | 10000 | 1399.37 | stop |

### Finalized answer

<pre>LightRAG generally outperforms GraphRAG across the evaluation dimensions.  

* **Metric‑wise performance** – In the win‑rate tables, LightRAG records higher percentages than GraphRAG for Comprehensiveness, Diversity, Empowerment and Overall on most datasets (e.g., LightRAG’s Diversity win rates are 77 % vs. 24 % for GraphRAG, and its Overall scores are 54.8 % vs. 45.2 %)[C2].  

* **Strengths of LightRAG** – The authors attribute LightRAG’s advantage to its dual‑level retrieval paradigm, which combines low‑level entity retrieval with high‑level topic retrieval. This design yields a “significant advantage in the Diversity metric, particularly within the larger Legal dataset” and “a clear advantage” in larger, complex corpora such as Agriculture, CS and Legal[C3].  

* **Qualitative comparison** – While both systems employ graph‑based retrieval, LightRAG “consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts” and delivers more diverse and empowering responses thanks to its hierarchical retrieval mechanism[C3].  

* **Case‑study reference** – A dedicated case‑study table (Table 3) directly compares LightRAG with GraphRAG, underscoring the focus on their relative performance[C5].  

Overall, the document reports that LightRAG surpasses GraphRAG on most quantitative metrics and is especially stronger in handling large‑scale, complex queries due to its dual‑level, graph‑enhanced retrieval approach.</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 8507.88

Judge latency_ms: 6203.57

Total evaluation latency_ms: 14721.86

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required source Chunk (metadata fallback) | C3 |
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | FAIL | Required claim not asserted |  |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | *The table shows that, across all four domains, the full LightRAG model consistently outperforms its high‑resource ablated version (LightRAG‑High) on every metric.* |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 574 | 229 | 188 | 600 | 10000 | 1513.56 | stop |
| 2 | answer | medium | 1981 | 1756 | 1518 | 3000 | 10000 | 6738.47 | stop |
| 3 | judge | low | 1112 | 887 | 126 | 1000 | 10000 | 1214.21 | stop |
| 4 | judge | low | 1113 | 888 | 114 | 1000 | 10000 | 991.19 | stop |
| 5 | judge | low | 1124 | 899 | 125 | 1000 | 10000 | 984.51 | stop |
| 6 | judge | low | 1124 | 899 | 124 | 1000 | 10000 | 1020.20 | stop |
| 7 | judge | low | 1100 | 875 | 325 | 1000 | 10000 | 1993.46 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (Table 2, C3)**  

| Dataset | Metric | LightRAG (standard) | LightRAG‑High (ablation) |
|---------|--------|---------------------|--------------------------|
| **Agriculture** | Comprehensiveness | 67.6 % | 65.2 % |
| | Diversity | 76.4 % | 72.8 % |
| | Empowerment | 67.6 % | 64.0 % |
| | Overall | 67.6 % | 64.8 % |
| **CS** | Comprehensiveness | 61.6 % | 57.2 % |
| | Diversity | 62.0 % | 63.2 % |
| | Empowerment | 61.2 % | 57.6 % |
| | Overall | 61.2 % | 56.0 % |
| **Legal** | Comprehensiveness | 83.6 % | 76.4 % |
| | Diversity | 86.4 % | 83.2 % |
| | Empowerment | 83.6 % | 77.2 % |
| | Overall | 84.8 % | 78.0 % |
| **Mix** | Comprehensiveness | 61.2 % | 59.6 % |
| | Diversity | 67.6 % | 64.0 % |
| | Empowerment | 57.2 % | 52.4 % |
| | Overall | 60.0 % | 57.6 % |

*The table shows that, across all four domains, the full LightRAG model consistently outperforms its high‑resource ablated version (LightRAG‑High) on every metric.*  

*Data for a “Low” ablation (NaiveRAG‑Low) are not included in the provided excerpt.*  

[C3]</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Ask latency_ms: 4913.41

Judge latency_ms: 0.00

Total evaluation latency_ms: 4913.45

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 568 | 223 | 38 | 600 | 10000 | 1287.19 | stop |
| 2 | answer | medium | 2421 | 2196 | 495 | 3000 | 10000 | 3413.52 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism. The system uses low‑level retrieval for precise entity‑level information and high‑level retrieval for broader topics, allowing it to capture complex inter‑dependencies among entities and produce more coherent, context‑rich responses [C1][C2].  

To address common RAG limitations—such as reliance on flat data representations, fragmented answers, and slow adaptation to new data—LightRAG integrates graph structures with vector representations and includes an incremental update algorithm that quickly incorporates fresh information [C2].  

Experimental results show that LightRAG substantially outperforms a baseline NaiveRAG across four domains (Agriculture, Computer Science, Legal, and a mixed set). Compared with NaiveRAG, LightRAG achieves higher scores in comprehensiveness, diversity, empowerment, and overall performance; for example, in the Agriculture domain overall accuracy rises from 32.4 % to 67.6 % [C3][C4].  

The evaluation uses four datasets whose sizes are detailed in Table 4: Agriculture (12 documents, 2,017,886 tokens), CS (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and Mix (61 documents, 619,009 tokens) [C5].  

The authors have released LightRAG as open‑source software, available at https://github.com/HKUDS/LightRAG [C1].</pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Lookup; expected: Global

Standalone Question: 這篇在講什麼？

Sub-queries: []

Ask latency_ms: 6055.12

Judge latency_ms: 0.00

Total evaluation latency_ms: 6055.52

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 571 | 226 | 63 | 600 | 10000 | 1356.97 | stop |
| 2 | answer | medium | 2729 | 2504 | 620 | 3000 | 10000 | 4493.43 | stop |

### Finalized answer

<pre>這篇文件主要介紹 LightRAG 框架——一種結合圖結構與向量表示的檢索增強生成（RAG）系統。  
- 文章先以「Beekeeper」實體為例，說明系統如何從原始文本中抽取實體、屬性與關係，並在圖中建立低階鍵與高階鍵以支援後續檢索 [C1]。  
- 接著闡述 LightRAG 採用的 **雙層檢索範式**：  
  * **低階檢索**聚焦於具體實體及其屬性／關係的精確查找；  
  * **高階檢索**則彙整多個相關實體與關係，提供概念性、摘要性的資訊 [C2]。  
  為了同時利用局部與全域關鍵字，系統先抽取本地關鍵字 k(l) 與全域關鍵字 k(g)，再分別在向量資料庫中匹配實體與關聯 [C2]。  
- 文件還說明了實驗設計：在 Legal、Mixed 等多領域資料集上，將 LightRAG 與 Naive RAG、RQ‑RAG、HyDE 等最新基線進行比較，並以完整語料生成大量測試問題來評估高層次意義建構能力 [C3]。  
- 最後列出相關研究與參考文獻，涵蓋圖‑文本嵌入、查詢精煉、RAG 評估等領域 [C4]。  

總結來說，本文聚焦於 **如何透過圖‑向量混合與雙層檢索機制提升 RAG 系統在具體與抽象查詢上的效能**。</pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Lookup; expected: Global

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Ask latency_ms: 4975.53

Judge latency_ms: 0.00

Total evaluation latency_ms: 4975.84

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 574 | 229 | 38 | 600 | 10000 | 1303.57 | stop |
| 2 | answer | medium | 2345 | 2120 | 609 | 3000 | 10000 | 3420.29 | stop |

### Finalized answer

<pre>**Key takeaways of the LightRAG paper**

- **Graph‑enhanced RAG architecture** – LightRAG augments traditional Retrieval‑Augmented Generation by integrating graph structures into the text indexing and retrieval pipeline, enabling the system to capture entities and their relationships more effectively [C1][C3].

- **Dual‑level retrieval** – The framework employs a dual‑level (low‑level and high‑level) retrieval process that extracts both fine‑grained and broad‑scope keywords, allowing comprehensive information discovery and more contextually relevant generation [C1][C4].

- **Efficient, low‑cost indexing** – The indexed data structure \(\hat D\) is designed to support rapid and cost‑effective retrieval, which is essential for handling high query volumes [C2].

- **Fast adaptation to data changes** – An incremental update algorithm continuously incorporates new information into the graph‑based index, keeping the system up‑to‑date in dynamic environments [C1].

- **Open‑source implementation** – The authors have released LightRAG’s code publicly at https://github.com/HKUDS/LightRAG [C1].

- **Empirical validation** – Experiments on four datasets (Agriculture, CS, Legal, Mix) demonstrate substantial improvements in retrieval accuracy and efficiency compared with existing baselines [C3].

- **Superior performance over NaiveRAG** – A case study (Table 5) shows that LightRAG provides more comprehensive, diverse, and empowering answers than the baseline NaiveRAG, thanks to its dual‑level retrieval and graph‑based knowledge representation [C5].

- **Comprehensive information retrieval goals** – The paper emphasizes three core objectives for an effective RAG system: (1) extracting global information for better query answering, (2) enabling rapid, low‑cost retrieval, and (3) quickly adapting the index to new data [C2].</pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Ask latency_ms: 5462.50

Judge latency_ms: 0.00

Total evaluation latency_ms: 5462.81

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 573 | 228 | 146 | 600 | 10000 | 1747.37 | stop |
| 2 | answer | medium | 2067 | 1842 | 621 | 3000 | 10000 | 3511.04 | stop |

### Finalized answer

<pre>LightRAG consistently outperforms GraphRAG across all evaluation dimensions. In the head‑to‑head win‑rate tables, LightRAG achieves higher percentages than GraphRAG for Comprehensiveness (e.g., 74 % vs 26 %), Diversity (76 % vs 24 %), Empowerment (74.8 % vs 25.2 %) and Overall (75.2 % vs 24.8 %) on the first dataset, and similar advantages on the remaining datasets [C2].  

The authors attribute LightRAG’s superiority to its dual‑level retrieval paradigm, which combines low‑level entity retrieval with high‑level topic retrieval, enabling richer, more diverse responses and better handling of complex, large‑scale queries [C3]. This advantage is especially pronounced on the larger datasets (Agriculture, CS, Legal), where LightRAG “significantly surpasses GraphRAG” and delivers a clearer grasp of comprehensive information [C3].  

Thus, compared with GraphRAG, LightRAG provides higher win rates on comprehensiveness, diversity, empowerment and overall performance, largely because its hierarchical, graph‑based indexing and dual‑level retrieval better capture both detailed and abstract knowledge. [C1][C2][C3]</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 有什麼限制？

Sub-queries: []

Ask latency_ms: 2413.87

Judge latency_ms: 0.00

Total evaluation latency_ms: 2413.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 572 | 227 | 102 | 600 | 10000 | 1023.33 | stop |
| 2 | answer | medium | 2479 | 2254 | 166 | 3000 | 10000 | 1179.78 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Synthesis; expected: Synthesis

Standalone Question: How do the experiments presented throughout the paper support its main claims, including the specific results, quantitative metrics, control comparisons, and statistical validations?

Sub-queries: [&#x27;What specific experimental results are presented in each section of the paper?&#x27;, &quot;How do the quantitative metrics from the experiments align with the paper&#x27;s main hypotheses?&quot;, &#x27;What control experiments or baselines are used, and how do they demonstrate the claimed improvements?&#x27;, &#x27;Are there any statistical analyses or significance tests reported that validate the experimental findings?&#x27;]

Ask latency_ms: 6851.44

Judge latency_ms: 0.00

Total evaluation latency_ms: 6851.75

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 574 | 229 | 161 | 600 | 10000 | 1312.06 | stop |
| 2 | answer | medium | 2248 | 2023 | 907 | 3000 | 10000 | 4833.47 | stop |

### Finalized answer

<pre>The paper validates its main claims through a series of quantitative experiments that compare LightRAG with multiple baselines across several datasets, evaluation dimensions, and ablation settings.

**1. Baseline win‑rate comparisons**  
Table 1 reports the win‑rate percentages of each baseline versus LightRAG on four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall). LightRAG consistently outperforms the baselines: for example, against NaiveRAG it wins 67.6 % vs 32.4 % on Agriculture (Comprehensiveness) and 76.4 % vs 23.6 % on Diversity; against RQ‑RAG it wins 68.4 % vs 31.6 % on Agriculture (Comprehensiveness) and 70.8 % vs 29.2 % on Diversity; and against HyDE it also shows higher win rates (the detailed numbers are omitted in the excerpt but follow the same pattern)[C2]. These results demonstrate that LightRAG achieves superior performance across all measured dimensions.

**2. Ablation study**  
Table 2 evaluates ablated versions of LightRAG using NaiveRAG as the reference. When the “‑High” configuration is applied, LightRAG’s win rates drop (e.g., Comprehensive: 65.2 % vs 34.8 % for NaiveRAG‑High; Diversity: 72.8 % vs 27.2 %; Empowerment: 64.0 % vs 36.0 %). The “‑Low” configuration shows a similar trend with lower win rates (e.g., Comprehensive: 57.2 % vs 34.8 %; Diversity: 63.2 % vs 27.2 %; Empowerment: 57.6 % vs 36.0 %). These ablations confirm that both high‑level and low‑level retrieval components contribute positively to LightRAG’s performance[C3].

**3. Cost and adaptability analysis**  
Figure 2 compares token usage and API call counts between GraphRAG and LightRAG on the Legal dataset. LightRAG requires fewer tokens (1,399 × 2 + Cextract vs. 610 × 1,000 for GraphRAG) and fewer API calls, indicating higher efficiency and lower operational cost[C4].

**4. Dataset statistics**  
The experimental setup uses four heterogeneous corpora (Agriculture, CS, Legal, Mix) with documented sizes: Agriculture (12 documents, 2,017,886 tokens), CS (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and Mix (61 documents, 619,009 tokens)[C5]. This diversity ensures that the reported improvements are not limited to a single domain.

**5. Qualitative evaluation**  
Human‑judged “Winner” labels for Diversity, Empowerment, and Overall categories (e.g., Answer 2 generated by LightRAG is preferred for its broader metric coverage and deeper explanations) further corroborate the quantitative gains[C4].

Together, these experiments provide concrete quantitative metrics (win‑rate percentages, token/API cost reductions), control comparisons against strong baselines (NaiveRAG, RQ‑RAG, HyDE, GraphRAG), and statistical context (dataset sizes) that collectively substantiate the paper’s claims of LightRAG’s superior comprehensiveness, diversity, empowerment, and efficiency.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 5735.87

Judge latency_ms: 0.00

Total evaluation latency_ms: 5736.01

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 574 | 229 | 188 | 600 | 10000 | 1377.76 | stop |
| 2 | answer | medium | 1981 | 1756 | 1046 | 3000 | 10000 | 4118.75 | stop |

### Finalized answer

<pre>**Ablated‑version performance (LightRAG vs. NaiveRAG)**  

| Domain | Metric | NaiveRAG | LightRAG |
|--------|--------|----------|----------|
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

**Ablated versions with “NaiveRAG‑High” as reference**

| Domain | Metric | NaiveRAG‑High | LightRAG |
|--------|--------|--------------|----------|
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

*Across all domains and metrics, LightRAG consistently achieves substantially higher percentages than the NaiveRAG baselines (both standard and “‑High” variants), demonstrating the effectiveness of the graph‑enhanced, ablated configurations.*  

[C3]</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Standalone Question: What datasets were used?

Sub-queries: []

Ask latency_ms: 2042.41

Judge latency_ms: 0.00

Total evaluation latency_ms: 2042.48

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 569 | 224 | 86 | 600 | 10000 | 887.96 | stop |
| 2 | answer | medium | 2641 | 2416 | 128 | 3000 | 10000 | 959.07 | stop |

### Finalized answer

<pre>The experiments used four UltraDomain benchmark datasets: **Agriculture**, **CS**, **Legal**, and **Mix**[C1][C5]</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Sub-queries: []

Ask latency_ms: 2758.38

Judge latency_ms: 0.00

Total evaluation latency_ms: 2758.88

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 578 | 233 | 76 | 600 | 10000 | 790.42 | stop |
| 2 | answer | medium | 2528 | 2303 | 310 | 3000 | 10000 | 1837.35 | stop |

### Finalized answer

<pre>55.6% [C4]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Ask latency_ms: 1774.72

Judge latency_ms: 0.00

Total evaluation latency_ms: 1775.13

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 576 | 231 | 59 | 600 | 10000 | 741.24 | stop |
| 2 | answer | medium | 2156 | 1931 | 107 | 3000 | 10000 | 828.96 | stop |

### Finalized answer

<pre>LightRAG needs just one API call for the retrieval phase[C3].</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Standalone Question: 那 LightRAG 呢？

Sub-queries: []

Ask latency_ms: 5930.38

Judge latency_ms: 0.00

Total evaluation latency_ms: 5930.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| history_supported | events | PASS | Explicit history supported |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 604 | 269 | 63 | 600 | 10000 | 851.02 | stop |
| 2 | answer | medium | 2144 | 1919 | 631 | 3000 | 10000 | 4896.35 | stop |

### Finalized answer

<pre>LightRAG 是一种将图结构引入文本索引和检索的检索增强生成（RAG）框架。它通过 **图‑基索引** 将实体及其关系建模为节点和边，并结合向量表示，实现对相关实体及其关联的高效检索，从而提升检索的上下文相关性和响应速度[C1]。  

该系统采用 **双层检索范式**：低层检索负责快速定位具体文档，高层检索通过图的社区结构发现抽象的全局信息，使得既能获取细粒度答案，又能捕获高层语义依赖[C1]。  

在 **增量更新算法** 的支持下，LightRAG 能够及时将新数据并入知识图谱，保持系统在快速变化的数据环境中的有效性和响应性[C1]。  

实验评估表明，LightRAG 在 **全面性、 多样性、赋能性** 等四个评价维度上均显著优于传统的基于纯块检索的 RAG 方法，并在多数对比中超过了同类的 GraphRAG。例如，在综合性维度的对比表中，LightRAG 的胜率为 **54.8%**（相较于 GraphRAG 的 **45.2%**），在多样性、赋能性和整体评分上也均保持领先[C3]。  

此外，LightRAG 在 **效率** 方面同样表现突出：通过图结构与向量检索的结合，实现了快速且相关的文档检索，显著提升了信息检索与生成的速度和质量，并降低了大模型推理成本[C5]。  

综上，LightRAG 通过图‑增强的索引与双层检索机制，在大规模语料库中实现了更高的检索准确性、上下文完整性和系统响应效率。  </pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Lookup; expected: Synthesis

Standalone Question: 那它跟 GraphRAG 比呢？

Sub-queries: []

Ask latency_ms: 6262.53

Judge latency_ms: 0.00

Total evaluation latency_ms: 6262.86

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| history_supported | events | PASS | Explicit history supported |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 595 | 260 | 154 | 600 | 10000 | 1197.81 | stop |
| 2 | answer | medium | 2619 | 2394 | 759 | 3000 | 10000 | 4894.31 | stop |

### Finalized answer

<pre>LightRAG 在多个维度上均优于 GraphRAG：

1. **回答质量**  
   - 在 **Comprehensiveness（全面性）**、**Diversity（多样性）**、**Empowerment（赋能）** 和 **Overall（整体）** 四个评估维度上，LightRAG 的胜率均高于 GraphRAG。例如，在 Comprehensive 维度上 LightRAG 获得 54.4%（对比 GraphRAG 的 26.0%），在 Diversity 维度上 LightRAG 获得 77.2%（对比 GraphRAG 的 24.0%），在 Empowerment 维度上 LightRAG 获得 74.8%（对比 GraphRAG 的 25.2%），在 Overall 维度上 LightRAG 获得 75.2%（对比 GraphRAG 的 24.8%）[C2]。  
   - 进一步的定性评估也显示 LightRAG 在 **Diversity**、**Empowerment** 以及 **Overall** 三项上均被评为 “Winner”，评审说明 LightRAG 提供了更丰富的指标解释、细致的关联分析以及更有助于读者做出判断的深度信息[C3]。

2. **检索成本**  
   - 在检索阶段，GraphRAG 需要遍历 610 个二级社区，每个社区报告约 1,000 tokens，累计消耗约 610,000 tokens，并产生数百次 API 调用；而 LightRAG 只使用不到 100 tokens 进行关键词生成和检索，并且仅需一次 API 调用[C4]。  
   - 这种差异表明 LightRAG 在 token 使用和 API 调用次数上都显著更低，成本更低。

3. **增量更新效率**  
   - 对于增量数据更新，GraphRAG 必须拆除并重新生成全部社区结构，导致每个社区报告约 5,000 tokens 的开销，整体需要约 1,399 × 2 × 5,000 tokens，成本极高；而 LightRAG 直接将新抽取的实体和关系并入现有图结构，无需完整重建，增量更新的 token 开销和 API 调用都大幅降低[C5]。  

综上所述，LightRAG 在回答质量、检索成本以及增量更新效率等方面均优于 GraphRAG。</pre>


## Judge semantic probes (excluded from Golden Facts result)

## JUDGE_ASSERTED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 852.67

Total evaluation latency_ms: 852.67

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 86 | 1000 | 10000 | 852.67 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 889.23

Total evaluation latency_ms: 889.23

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 889.23 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
