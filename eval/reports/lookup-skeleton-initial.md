# Golden Facts evaluation

Created: 2026-10-12T14:57:19.148067+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Label: lookup-skeleton

Revision: 4408c6a0b3fe8cf3e228da7628d7bf42716a927d

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
| Q2 | not_all_datasets | forbidden | 1/1 (100.0%) |
| Q3 | question_type | events | 1/1 (100.0%) |
| Q3 | high_term | contains | 0/1 (0.0%) |
| Q3 | low_term | contains | 0/1 (0.0%) |
| Q3 | origin_term | contains | 0/1 (0.0%) |
| Q3 | table2_baseline | judge | 0/1 (0.0%) |
| Q3 | ablation_meaning | judge | 0/1 (0.0%) |
| Q3 | mix_low_overall | judge | 0/1 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/1 (0.0%) |
| Q3 | not_all_best | forbidden | 1/1 (100.0%) |
| ZH_COST | question_type | events | 0/1 (0.0%) |
| ZH_COST | chinese_answer | judge | 0/1 (0.0%) |
| ZH_COST | retrieval_cost | judge | 0/1 (0.0%) |
| ZH_COST | numbers_unchanged | judge | 0/1 (0.0%) |
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

Total evaluation latency_ms: 13237.32

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | addressing the flat‑data and contextual‑awareness limitations of existing RAG systems |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The system combines **low‑level retrieval** (precise entity and relationship extraction) and **high‑level retrieval** (broader topics and themes) to capture complex inter‑dependencies among entities |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Experimental results on four benchmark datasets—**Agriculture** (12 documents, 2,017,886 tokens), **CS** (10 documents, 2,306,535 tokens), **Legal** (94 documents, 5,081,069 tokens), and **Mix** (61 documents, 619,009 tokens)—show that LightRAG consistently outperforms the NaiveRAG baseline across multiple evaluation dimensions. For example, in the Agriculture domain LightRAG achieves 67.6 % comprehensiveness versus 32.4 % for NaiveRAG, and 76.4 % diversity versus 23.6 % for NaiveRAG; similar gains are observed for empowerment and overall scores across all domains |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 873 | 3000 | 10000 | 3403.86 | stop |
| 2 | judge | low | 1054 | 829 | 132 | 1000 | 10000 | 1405.43 | stop |
| 3 | judge | low | 1049 | 824 | 136 | 1000 | 10000 | 1563.16 | stop |
| 4 | judge | low | 1051 | 826 | 135 | 1000 | 10000 | 1601.37 | stop |
| 5 | judge | low | 1057 | 832 | 136 | 1000 | 10000 | 969.54 | stop |
| 6 | judge | low | 1066 | 841 | 307 | 1000 | 10000 | 1950.50 | stop |
| 7 | judge | low | 1050 | 825 | 102 | 1000 | 10000 | 2185.77 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) framework that enhances large language models by integrating graph‑structured text indexing with a dual‑level retrieval mechanism, addressing the flat‑data and contextual‑awareness limitations of existing RAG systems and reducing fragmented answers [C1][C2].  

The system combines **low‑level retrieval** (precise entity and relationship extraction) and **high‑level retrieval** (broader topics and themes) to capture complex inter‑dependencies among entities, and it incorporates an incremental update algorithm that enables rapid adaptation to new data [C2].  

LightRAG’s key contributions are:  
1. A graph‑based text indexing paradigm that represents inter‑entity relationships. [C2]  
2. A dual‑level retrieval framework (low‑ and high‑level) for comprehensive and efficient information access. [C2]  
3. An incremental update mechanism for fast integration of fresh data. [C2]  

The authors released the implementation as open‑source software (https://github.com/HKUDS/LightRAG) [C1].  

Experimental results on four benchmark datasets—**Agriculture** (12 documents, 2,017,886 tokens), **CS** (10 documents, 2,306,535 tokens), **Legal** (94 documents, 5,081,069 tokens), and **Mix** (61 documents, 619,009 tokens)—show that LightRAG consistently outperforms the NaiveRAG baseline across multiple evaluation dimensions. For example, in the Agriculture domain LightRAG achieves 67.6 % comprehensiveness versus 32.4 % for NaiveRAG, and 76.4 % diversity versus 23.6 % for NaiveRAG; similar gains are observed for empowerment and overall scores across all domains [C3][C4].  

The methodology section details how entities and relationships are extracted from documents using large language models, the prompt templates employed, and the evaluation criteria used to compare LightRAG against baselines [C5].  

A concrete retrieval‑augmented generation example (Figure 3) demonstrates the process: given the query “What metrics are most informative for evaluating movie recommendation systems?”, the LLM extracts low‑ and high‑level keywords that drive the dual‑level retrieval and subsequent generation [C5].  </pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 9869.23

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | FAIL | Required claim not asserted |  |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 736 | 3000 | 10000 | 3405.12 | stop |
| 2 | judge | low | 943 | 718 | 114 | 1000 | 10000 | 769.83 | stop |
| 3 | judge | low | 980 | 755 | 55 | 1000 | 10000 | 644.61 | stop |
| 4 | judge | low | 940 | 715 | 90 | 1000 | 10000 | 773.71 | stop |
| 5 | judge | low | 979 | 754 | 133 | 1000 | 10000 | 807.60 | stop |
| 6 | judge | low | 961 | 736 | 149 | 1000 | 10000 | 2011.35 | stop |
| 7 | judge | low | 941 | 716 | 156 | 1000 | 10000 | 1137.39 | stop |

### Finalized answer

<pre>LightRAG generally surpasses GraphRAG on the evaluated dimensions. In the win‑rate tables, LightRAG achieves markedly higher percentages than GraphRAG for **Comprehensiveness** (e.g., 74 % vs. 26 % in one setting and 54.4 % vs. 45.6 % in another) [C2]; for **Diversity** (74 % vs. 24 % and 77.2 % vs. 22.8 %) [C2]; for **Empowerment** (74.8 % vs. 25.2 % and 58.8 % vs. 41.2 %) [C2]; and for the **Overall** score (75.2 % vs. 24.8 % and 54.8 % vs. 45.2 %) [C2].  

The authors attribute LightRAG’s advantage to its **dual‑level retrieval paradigm**, which combines low‑level entity retrieval with high‑level topic retrieval, and to its **hierarchical graph‑based indexing** that captures both detailed and broader context [C3][C4]. This mechanism yields a broader range of information (higher Diversity) and more empowering content (higher Empowerment) [C4].  

While both systems employ graph‑enhanced retrieval, LightRAG’s architecture consistently yields better performance, especially on larger, more complex datasets such as Agriculture, CS, and Legal, where it “significantly surpasses GraphRAG” [C3].  

Thus, compared with GraphRAG, LightRAG demonstrates superior comprehensiveness, diversity, empowerment, and overall answer quality, largely due to its dual‑level, hierarchical graph‑based retrieval design. [C1][C3][C4]</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 9840.17

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | FAIL | Term missing |  |
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
| 1 | answer | medium | 1981 | 1756 | 698 | 3000 | 10000 | 2967.07 | stop |
| 2 | judge | low | 1014 | 789 | 146 | 1000 | 10000 | 1502.26 | stop |
| 3 | judge | low | 1015 | 790 | 106 | 1000 | 10000 | 1350.05 | stop |
| 4 | judge | low | 1026 | 801 | 137 | 1000 | 10000 | 781.46 | stop |
| 5 | judge | low | 1026 | 801 | 133 | 1000 | 10000 | 1393.74 | stop |
| 6 | judge | low | 1002 | 777 | 99 | 1000 | 10000 | 1432.87 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (NaiveRAG used as reference)**  

| Domain | Metric | NaiveRAG (baseline) | LightRAG (ablated) |
|--------|--------|--------------------|--------------------|
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

*The table reports the percentages for each evaluation dimension (Comprehensiveness, Diversity, Empowerment, Overall) when comparing the original NaiveRAG baseline to the ablated LightRAG variants across four datasets (Agriculture, CS, Legal, Mix) as presented in the paper’s Table 2 [C3].*</pre>

## ZH_COST — repetition 1

Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Sub-queries: []

Total evaluation latency_ms: 6762.77

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| chinese_answer | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | 在檢索階段，GraphRAG 必須產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索開銷極為輕量。 |
| numbers_unchanged | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | GraphRAG 必須產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫... LightRAG 只需使用不到 100 個 token... 整個過程僅需一次 API 呼叫 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2625 | 2400 | 420 | 3000 | 10000 | 2854.54 | stop |
| 2 | judge | low | 796 | 571 | 194 | 1000 | 10000 | 1209.71 | stop |
| 3 | judge | low | 844 | 619 | 346 | 1000 | 10000 | 1288.57 | stop |
| 4 | judge | low | 829 | 604 | 314 | 1000 | 10000 | 1176.01 | stop |

### Finalized answer

<pre>LightRAG 的檢索成本遠低於 GraphRAG。  
在檢索階段，GraphRAG 必須產生 1,399 個社群，實驗中使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大[C4]。  
相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索開銷極為輕量[C4]。  

此外，在增量資料更新時，LightRAG 只需將新抽取的實體與關係直接加入現有圖中，無需重新建構社群，進一步降低了檢索相關的 token 與 API 開銷，而 GraphRAG 則需重新生成所有社群報告，代價高昂[C5]。</pre>

## LIMITATIONS — repetition 1

Question: 這篇論文有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: 這篇論文有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 5392.30

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
| 1 | answer | medium | 2565 | 2340 | 205 | 3000 | 10000 | 1655.96 | stop |
| 2 | judge | low | 564 | 339 | 61 | 1000 | 10000 | 692.49 | stop |
| 3 | judge | low | 581 | 356 | 62 | 1000 | 10000 | 644.05 | stop |
| 4 | judge | low | 564 | 339 | 63 | 1000 | 10000 | 707.92 | stop |
| 5 | judge | low | 561 | 336 | 126 | 1000 | 10000 | 1529.05 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Total evaluation latency_ms: 1878.59

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2312 | 2087 | 134 | 3000 | 10000 | 795.80 | stop |
| 2 | judge | low | 541 | 316 | 92 | 1000 | 10000 | 698.24 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Total evaluation latency_ms: 1746.27

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2356 | 2131 | 79 | 3000 | 10000 | 807.70 | stop |
| 2 | judge | low | 542 | 317 | 73 | 1000 | 10000 | 664.16 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Total evaluation latency_ms: 2058.97

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2176 | 1951 | 250 | 3000 | 10000 | 1140.25 | stop |
| 2 | judge | low | 541 | 316 | 106 | 1000 | 10000 | 760.50 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Total evaluation latency_ms: 3254.70

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 925 | 3000 | 10000 | 3083.83 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) framework that enhances large language models by integrating graph‑structured text indexing with a dual‑level retrieval system, addressing the flat‑data and contextual‑awareness limitations of existing RAG approaches[C1][C2].  
The system performs **low‑level retrieval** (precise entity and relationship information) and **high‑level retrieval** (broader topics and themes), enabling it to capture complex inter‑dependencies among entities and to produce more coherent, context‑rich responses[C2].  
Key technical contributions include:  

* a graph‑based knowledge representation that couples with vector embeddings for efficient entity‑relation retrieval;  
* an incremental update algorithm that quickly incorporates new data, keeping the system responsive in dynamic environments[C2];  
* an open‑source implementation released at https://github.com/HKUDS/LightRAG[C1].  

Experimental evaluation on four datasets—Agriculture (12 documents, 2,017,886 tokens), CS (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and Mix (61 documents, 619,009 tokens)[C5]—shows that LightRAG consistently outperforms the NaiveRAG baseline across multiple metrics. For example, in the “Mix” domain LightRAG achieves 61.2 % comprehensiveness versus 38.8 % for NaiveRAG, 67.6 % diversity versus 32.4 %, and 57.2 % empowerment versus 42.8 % (overall 60.0 % vs. 40.0 %)[C3]; similar gains are observed in the other domains, with LightRAG’s overall scores ranging from 56.0 % to 84.8 % compared to NaiveRAG’s 32.4 %–44.4 %[C3][C4].  

The appendix details the methodology for extracting entities and relationships using LLMs, the prompt templates employed, and the evaluation dimensions used to assess LightRAG’s performance[C5]. A concrete retrieval‑augmented generation example (query: “What metrics are most informative for evaluating movie recommendation systems?”) illustrates how low‑ and high‑level keywords guide the dual‑level retrieval process[C5].  

Overall, LightRAG demonstrates that graph‑empowered indexing and dual‑level retrieval can markedly improve the accuracy, diversity, and empowerment of RAG systems while maintaining fast response times.</pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Lookup; expected: Global

Standalone Question: 這篇在講什麼？

Sub-queries: []

Total evaluation latency_ms: 5673.27

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2729 | 2504 | 883 | 3000 | 10000 | 5476.71 | stop |

### Finalized answer

<pre>本文介紹 LightRAG 框架，一種結合圖結構與向量表示的檢索增強生成（RAG）系統。[C2]  
該框架採用雙層檢索範式，分為低層檢索（針對具體實體及其屬性）與高層檢索（聚合多實體以提供概念性摘要）。[C2]  
透過圖與向量的整合，系統能同時利用局部關鍵詞與全局關鍵詞進行匹配，提高檢索相關性。[C2]  
文中以「Beekeeper（養蜂人）」為例，展示實體抽取、關係抽取與去重等過程，說明如何從文本中構建實體圖譜。[C1]  
為評估高層次意義建構任務，作者將多個資料集的全文作為上下文，使用 LLM 生成使用者與任務，產生 125 條問題作為測試集。[C3]  
LightRAG 的效能與 Naive RAG、RQ‑RAG、HyDE 等最新 RAG 方法進行比較。[C3]  
文章最後列出相關工作與參考文獻，涵蓋圖文嵌入、RAG 評估與自監督學習等領域。[C4][C5]</pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Lookup; expected: Global

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Total evaluation latency_ms: 3044.90

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2345 | 2120 | 593 | 3000 | 10000 | 2872.77 | stop |

### Finalized answer

<pre>**Key Takeaways of the LightRAG paper**

- **Motivation &amp; Goal** – Retrieval‑Augmented Generation (RAG) systems improve large language models by pulling in external knowledge, but current approaches rely on flat data representations and lack deep contextual awareness, often producing fragmented answers. LightRAG aims to overcome these limitations by integrating graph structures into the indexing and retrieval pipeline[C1].  

- **Graph‑Based Text Indexing** – Documents are segmented and processed with LLMs to extract entities (names, dates, locations, events) and their relationships, which are then organized into a knowledge graph \( \hat{D} = (\hat{V},\hat{E}) \) that captures global inter‑dependencies across the corpus[C2].  

- **Dual‑Level Retrieval** – LightRAG employs a two‑stage retrieval mechanism: low‑level (entity‑level) and high‑level (concept‑level) keyword extraction guides separate retrieval paths, enabling both fine‑grained and broad‑scope information discovery[C2][C4].  

- **Efficient, Low‑Cost Retrieval &amp; Fast Adaptation** – The graph‑enhanced index \( \hat{D} \) is designed for rapid, cost‑effective lookup and supports an incremental update algorithm that quickly incorporates new data, keeping the system current in dynamic environments[C2].  

- **Empirical Validation** – Experiments on four datasets (Agriculture, CS, Legal, Mix) show that LightRAG achieves substantial gains in retrieval accuracy and efficiency compared with baseline methods, as reflected in the statistical overview of the datasets and the reported performance improvements[C3].  

- **Evaluation Framework** – The authors define a comprehensive RAG evaluation protocol that judges answers on **Comprehensiveness**, **Diversity**, and **Empowerment**, using JSON‑formatted prompts and detailed rationales to select the better response[C4][C5].  

- **Superiority Over Baselines** – A case study comparing LightRAG with a naive RAG baseline (NaiveRAG) demonstrates that LightRAG provides deeper, more nuanced explorations of complex topics (e.g., indigenous perspectives in corporate mergers) thanks to its dual‑level retrieval and graph‑based knowledge representation[C5].  

- **Open‑Source Release** – The LightRAG codebase is publicly available, encouraging further research and adoption[C1].  </pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 3441.21

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 660 | 3000 | 10000 | 3263.04 | stop |

### Finalized answer

<pre>LightRAG generally surpasses GraphRAG on all evaluated dimensions.  In the win‑rate tables LightRAG achieves higher percentages than GraphRAG for comprehensiveness, diversity, empowerment and overall performance across the four test corpora, indicating more thorough and varied answers and a stronger overall advantage [C2].  The authors explicitly state that LightRAG “consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts,” and that its dual‑level retrieval paradigm and hierarchical graph‑based indexing give it a clear edge in capturing comprehensive information and generating more diverse responses [C3].  A dedicated case‑study (Table 3) further contrasts the two systems, treating GraphRAG as the baseline method against which LightRAG’s improvements are highlighted [C5].  While both systems employ graph‑enhanced retrieval, LightRAG’s combination of low‑level entity retrieval and high‑level topic retrieval yields superior performance, especially on large‑scale corpora. [C1]</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 1210.66

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2479 | 2254 | 194 | 3000 | 10000 | 1050.28 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Lookup; expected: Synthesis

Standalone Question: How do the experiments support the paper&#x27;s claims?

Sub-queries: []

Total evaluation latency_ms: 3818.95

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2692 | 2467 | 991 | 3000 | 10000 | 3650.74 | stop |

### Finalized answer

<pre>The experimental results directly substantiate the paper’s main claims in several ways:

1. **Superior performance across domains and evaluation dimensions** – Table 1 (Virtual Section 7) reports win‑rate percentages for LightRAG versus three baselines (NaiveRAG, RQ‑RAG, HyDE) on the four benchmark datasets (Agriculture, CS, Legal, Mix). In every case LightRAG achieves a markedly higher win rate (e.g., 67.6 % vs 32.4 % on Agriculture for Comprehensiveness, 61.2 % vs 38.8 % on Legal for Overall) across all three dimensions (Comprehensiveness, Diversity, Empowerment) and the aggregated Overall score, confirming the claim that LightRAG consistently outperforms existing RAG methods [C1].

2. **Effectiveness of the dual‑level retrieval design** – The ablation study in Table 2 (Virtual Section 8) uses NaiveRAG as a reference and compares the full LightRAG model with versions that omit the high‑level or low‑level retrieval components. Removing either component leads to noticeable drops in all metrics (e.g., Overall falls from 64.8 % to 56.0 % when the high‑level component is removed on the Agriculture set), demonstrating that both low‑level and high‑level retrieval are essential for the observed gains [C2].

3. **Qualitative superiority in answer quality** – The “Winner” analysis in Virtual Section 9 shows that LightRAG’s answers are judged the best for Diversity, Empowerment, and the Overall category. The explanations highlight LightRAG’s richer coverage of metrics, nuanced inter‑relations, and deeper contextual insight, supporting the claim that LightRAG delivers more comprehensive, diverse, and empowering responses [C3].

4. **Lower computational cost** – Figure 2 (Virtual Section 9) compares token consumption and API‑call counts between GraphRAG and LightRAG on the Legal dataset. LightRAG requires far fewer tokens (e.g., &lt; 100 × 1,000 vs. 1,399 × 2 × 5,000) and fewer API calls, confirming the claim that LightRAG is more cost‑effective while maintaining performance [C4].

5. **Broad applicability across varied corpora** – Table 4 (Virtual Section 13) lists the statistical properties of the four datasets (ranging from 12 to 94 documents and from ~0.6 M to &gt;5 M tokens). The diversity of domains (Agriculture, Computer Science, Legal, mixed) and document sizes demonstrates that the experiments evaluate LightRAG under heterogeneous conditions, supporting the claim of generalizability [C5].

Together, these quantitative and qualitative experiments provide concrete evidence that LightRAG achieves higher accuracy, richer answer quality, and lower resource usage than existing retrieval‑augmented generation approaches.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 4073.13

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1600 | 3000 | 10000 | 3861.10 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (using NaiveRAG as reference)**  

| Domain | Metric | NaiveRAG (baseline) | LightRAG (ablated) |
|--------|--------|--------------------|--------------------|
| **Agriculture** | Comprehensiveness | 32.4 % | 67.6 % |
| | Diversity | 23.6 % | 76.4 % |
| | Empowerment | 32.4 % | 67.6 % |
| | Overall | 32.4 % | 67.6 % |
| **Computer Science (CS)** | Comprehensiveness | 38.4 % | 61.6 % |
| | Diversity | 38.0 % | 62.0 % |
| | Empowerment | 38.8 % | 61.2 % |
| | Overall | 38.8 % | 61.2 % |
| **Legal** | Comprehensiveness | 16.4 % | 83.6 % |
| | Diversity | 13.6 % | 86.4 % |
| | Empowerment | 16.4 % | 83.6 % |
| | Overall | 15.2 % | 84.8 % |
| **Mix** (heterogeneous corpus) | Comprehensiveness | 38.8 % | 61.2 % |
| | Diversity | 32.4 % | 67.6 % |
| | Empowerment | 42.8 % | 57.2 % |
| | Overall | 40.0 % | 60.0 % |

**Ablated LightRAG with “NaiveRAG‑High” baseline**  

| Domain | Metric | NaiveRAG‑High | LightRAG |
|--------|--------|--------------|----------|
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

*All percentages are taken directly from Table 2, which reports the performance of ablated LightRAG versions across four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) and four dataset categories (Agriculture, CS, Legal, Mix) using NaiveRAG and NaiveRAG‑High as baselines*[C3].  

(The document does not provide the numeric results for the “NaiveRAG‑Low” ablation.)</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Standalone Question: What datasets were used?

Sub-queries: []

Total evaluation latency_ms: 1378.77

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2641 | 2416 | 102 | 3000 | 10000 | 839.48 | stop |

### Finalized answer

<pre>The experiments used four datasets from the UltraDomain benchmark: **Agriculture, CS (computer science), Legal, and Mix**[C1][C5]</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Sub-queries: []

Total evaluation latency_ms: 2942.27

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2528 | 2303 | 839 | 3000 | 10000 | 2777.00 | stop |

### Finalized answer

<pre>在 Table 2 中，‑Origin 设定下 Mix 数据集的 Overall 为 **55.6%**[C4]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Total evaluation latency_ms: 1033.82

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2156 | 1931 | 108 | 3000 | 10000 | 778.05 | stop |

### Finalized answer

<pre>LightRAG needs only one API call for the retrieval phase[C3]</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Standalone Question: 那 LightRAG 呢？

Sub-queries: []

Total evaluation latency_ms: 4269.03

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2144 | 1919 | 1095 | 3000 | 10000 | 4101.51 | stop |

### Finalized answer

<pre>LightRAG 是一种将图结构引入检索增强生成（RAG）体系的系统。它在文本索引和检索阶段使用知识图，将实体和关系建模为节点和边，从而实现 **低层‑高层双层检索**，既能获取具体信息，又能抽取抽象概念[C1]。系统配备 **增量更新算法**，能够及时将新数据整合进图中，保持在快速变化数据环境中的有效性和响应性[C1]。

在实现细节上，LightRAG 采用 **nano 向量数据库** 管理向量数据，所有基于 LLM 的操作默认使用 **GPT‑4o‑mini**，块大小统一设为 **1200**，gleaning 参数固定为 **1**，与 GraphRAG 保持一致[C2]。

实验评估表明，LightRAG 在四个评价维度上均显著优于传统的纯块检索方法。具体胜率如下（相对于基线）：

- **全面性（Comprehensiveness）**：约 **54.4%‑59.6%**  
- **多样性（Diversity）**：约 **77.2%‑67.6%**  
- **赋能性（Empowerment）**：约 **58.8%‑54.0%**  
- **整体（Overall）**：约 **54.8%‑57.6%**  

这些数值均高于基线的 20% 左右的胜率，显示出图‑增强 RAG 在大规模语料库和复杂查询下的优势[C3]。

此外，LightRAG 在 **全面性、 多样性和赋能性** 方面也表现突出。它能够覆盖更广泛的机器学习指标，提供更丰富、多元且有助于用户理解的内容，这归功于其 **层次化检索范式**，能够深入挖掘实体、关系以及 LLM 的画像信息[C4]。

总体而言，LightRAG 通过 **图‑结构索引** 提升检索效率和语义理解深度，实现 **快速、相关的文档检索**，并通过双层检索满足多样化的用户需求，同时显著降低 LLM 推理成本[C5]。</pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Lookup; expected: Synthesis

Standalone Question: 那它跟 GraphRAG 比呢？

Sub-queries: []

Total evaluation latency_ms: 5747.20

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2619 | 2394 | 939 | 3000 | 10000 | 5549.61 | stop |

### Finalized answer

<pre>相较于 GraphRAG，LightRAG 在答案质量和系统效率上均表现更佳。

**答案质量**  
在四项评估维度（Comprehensiveness、Diversity、Empowerment、Overall）上，LightRAG 的胜率均高于 GraphRAG。例如，在 Comprehensiveness 维度 LightRAG 获得 54.4% 的胜率，而 GraphRAG 仅为 45.6%；在 Diversity 维度 LightRAG 为 77.2% 对比 GraphRAG 的 22.8%；在 Empowerment 维度 LightRAG 为 58.8% 对比 GraphRAG 的 41.2%；在 Overall 维度 LightRAG 为 54.8% 对比 GraphRAG 的 45.2%[C2]。  
此外，针对具体答案的比较，LightRAG 在 Diversity、Empowerment 以及 Overall 三个维度均被评为“Winner”，说明其在提供多样化、赋能读者以及整体信息丰富度方面优于 GraphRAG[C3]。

**检索阶段成本**  
LightRAG 只需不到 100 个 token 生成关键词并完成检索，且整个过程只调用一次 API；而 GraphRAG 需要遍历 610 个二级社区，每个社区报告约 1,000 token，累计消耗约 610,000 token，并产生数百次 API 调用[C4]。这表明 LightRAG 在检索阶段的 token 使用和 API 调用量都远低于 GraphRAG。

**增量更新成本**  
在处理新增数据时，GraphRAG 必须拆除并重新生成全部社区结构，导致约 1,399 × 2 × 5,000 ≈ 14 百万 token 的巨额开销；而 LightRAG 直接将新抽取的实体和关系并入已有图中，无需完整重建，成本显著更低[C5]。

综上所述，LightRAG 在答案的全面性、多样性、赋能能力以及整体表现上均优于 GraphRAG，同时在检索和增量更新阶段的 token 消耗与 API 调用量也更为高效。</pre>

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
| 1 | judge | low | 560 | 335 | 113 | 1000 | 10000 | 708.07 | stop |

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
| 1 | judge | low | 574 | 349 | 122 | 1000 | 10000 | 884.61 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
