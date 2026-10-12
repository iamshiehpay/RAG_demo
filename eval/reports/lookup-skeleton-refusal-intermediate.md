# Golden Facts evaluation

Created: 2026-10-12T15:04:53.670915+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Label: lookup-skeleton

Revision: 4b2c7b4db7b464f4086e6fa43b3c2da27a2c37d4

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
| LIMITATIONS | no_invented_limit | forbidden | 0/1 (0.0%) |
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

Total evaluation latency_ms: 9596.04

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism, which together capture complex inter‑dependencies among entities and provide both detailed (low‑level) and conceptual (high‑level) information to generate more coherent, context‑rich responses[C1][C2]. |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Experimental evaluation on four datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens)—demonstrates that LightRAG substantially outperforms a baseline NaiveRAG across three evaluation dimensions (Comprehensiveness, Diversity, Empowerment) and overall scores[C5].<br><br>For example, in the Agriculture domain LightRAG achieves 67.6 % comprehensiveness versus 32.4 % for NaiveRAG, 76.4 % diversity versus 23.6 %, and 67.6 % empowerment versus 32.4 %, yielding an overall improvement from 32.4 % to 67.6 %[C3]. Similar gains are observed in the CS, Legal, and Mix domains, with LightRAG’s overall scores ranging from 60 % to 84.8 % compared to NaiveRAG’s 15.2 %–40.0 %[C3][C4]. |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 602 | 3000 | 10000 | 2751.68 | stop |
| 2 | judge | low | 1121 | 896 | 96 | 1000 | 10000 | 803.98 | stop |
| 3 | judge | low | 1116 | 891 | 114 | 1000 | 10000 | 935.14 | stop |
| 4 | judge | low | 1118 | 893 | 187 | 1000 | 10000 | 1037.33 | stop |
| 5 | judge | low | 1124 | 899 | 145 | 1000 | 10000 | 1364.40 | stop |
| 6 | judge | low | 1133 | 908 | 406 | 1000 | 10000 | 1755.70 | stop |
| 7 | judge | low | 1117 | 892 | 84 | 1000 | 10000 | 823.16 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism, which together capture complex inter‑dependencies among entities and provide both detailed (low‑level) and conceptual (high‑level) information to generate more coherent, context‑rich responses[C1][C2].  

The system integrates graph structures with vector representations to enable efficient retrieval of related entities and their relationships, and includes an incremental update algorithm that quickly incorporates new data, keeping the model responsive in dynamic environments[C1][C2].  

Experimental evaluation on four datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens)—demonstrates that LightRAG substantially outperforms a baseline NaiveRAG across three evaluation dimensions (Comprehensiveness, Diversity, Empowerment) and overall scores[C5].  

For example, in the Agriculture domain LightRAG achieves 67.6 % comprehensiveness versus 32.4 % for NaiveRAG, 76.4 % diversity versus 23.6 %, and 67.6 % empowerment versus 32.4 %, yielding an overall improvement from 32.4 % to 67.6 %[C3]. Similar gains are observed in the CS, Legal, and Mix domains, with LightRAG’s overall scores ranging from 60 % to 84.8 % compared to NaiveRAG’s 15.2 %–40.0 %[C3][C4].  

These results confirm that LightRAG’s graph‑empowered indexing and dual‑level retrieval significantly boost retrieval accuracy, diversity of retrieved information, and the empowerment of generated answers, while also reducing response times and supporting rapid adaptation to new data[C1][C2].  

The LightRAG codebase is released as open‑source software at https://github.com/HKUDS/LightRAG[C1].</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 11119.33

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| retrieval_methods | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | GraphRAG is described as a graph‑enhanced RAG system that extracts entities and relationships, builds a graph of nodes and edges, aggregates nodes into communities, and traverses these communities for high‑level queries [C1]. ... LightRAG employs a dual‑level retrieval paradigm (low‑level entity + high‑level topic) that enhances context capture and response variety |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | FAIL | Required claim not asserted |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | - **Performance metrics**: LightRAG achieves higher win‑rates than GraphRAG on Comprehensiveness, Diversity, Empowerment, and Overall across all evaluated datasets [C2]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 782 | 3000 | 10000 | 3935.40 | stop |
| 2 | judge | low | 1235 | 1010 | 221 | 1000 | 10000 | 1096.73 | stop |
| 3 | judge | low | 1272 | 1047 | 54 | 1000 | 10000 | 716.89 | stop |
| 4 | judge | low | 1232 | 1007 | 91 | 1000 | 10000 | 783.75 | stop |
| 5 | judge | low | 1271 | 1046 | 141 | 1000 | 10000 | 1028.35 | stop |
| 6 | judge | low | 1253 | 1028 | 130 | 1000 | 10000 | 988.21 | stop |
| 7 | judge | low | 1233 | 1008 | 199 | 1000 | 10000 | 1082.00 | stop |

### Finalized answer

<pre>**Overall performance**

The quantitative results in Section 7 (Table shown in [C2]) compare GraphRAG and LightRAG on four evaluation dimensions—Comprehensiveness, Diversity, Empowerment, and Overall—across several datasets. For each dimension the percentages represent win‑rates (higher % = better). Across almost all dataset‑metric pairs LightRAG attains a higher win‑rate than GraphRAG (e.g., Comprehensiveness 54.4 % vs 45.6 % for GraphRAG; Diversity 77.2 % vs 22.8 %; Empowerment 58.8 % vs 41.2 %; Overall 54.8 % vs 45.2 %). This pattern repeats for the other datasets, indicating that LightRAG consistently outperforms GraphRAG on these metrics [C2].

**Why LightRAG is stronger**

Section 7 further explains that LightRAG’s advantage stems from its *dual‑level retrieval paradigm*, which combines low‑level entity retrieval with high‑level topic retrieval. This design enables LightRAG to capture the full context of queries, especially in large‑scale corpora, and to generate a wider variety of responses [C3]. The authors attribute LightRAG’s superior Diversity scores—particularly on the large Legal dataset—to this mechanism [C3].

**GraphRAG’s characteristics**

GraphRAG is described as a graph‑enhanced RAG system that extracts entities and relationships, builds a graph of nodes and edges, aggregates nodes into communities, and traverses these communities for high‑level queries [C1]. It uses the same LLM (GPT‑4o‑mini) and the same gleaning parameter as LightRAG, but relies on a single‑level graph retrieval without the explicit dual‑level hierarchy employed by LightRAG [C1].

**Summary of the comparison**

- **Performance metrics**: LightRAG achieves higher win‑rates than GraphRAG on Comprehensiveness, Diversity, Empowerment, and Overall across all evaluated datasets [C2].
- **Mechanistic difference**: LightRAG employs a dual‑level retrieval paradigm (low‑level entity + high‑level topic) that enhances context capture and response variety, whereas GraphRAG uses a community‑based graph traversal without this hierarchical retrieval [C1][C3].
- **Impact on large, complex corpora**: LightRAG’s design yields a clear advantage in large‑scale, high‑token datasets (e.g., Legal, Agriculture, CS), leading to more comprehensive and diverse answers [C3].</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 11235.12

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
| 1 | answer | medium | 1981 | 1756 | 1633 | 3000 | 10000 | 5572.35 | stop |
| 2 | judge | low | 906 | 681 | 182 | 1000 | 10000 | 1135.73 | stop |
| 3 | judge | low | 907 | 682 | 108 | 1000 | 10000 | 1296.87 | stop |
| 4 | judge | low | 918 | 693 | 140 | 1000 | 10000 | 1034.29 | stop |
| 5 | judge | low | 918 | 693 | 133 | 1000 | 10000 | 1125.89 | stop |
| 6 | judge | low | 894 | 669 | 92 | 1000 | 10000 | 857.61 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (using the “‑High” ablation setting)**  

| Domain | Comprehensiveness | Diversity | Empowerment | Overall |
|--------|-------------------|-----------|-------------|---------|
| **Agriculture** | 65.2 % | 72.8 % | 64.0 % | 64.8 % |
| **Computer Science (CS)** | 57.2 % | 63.2 % | 57.6 % | 56.0 % |
| **Legal** | 76.4 % | 83.2 % | 77.2 % | 78.0 % |
| **Mix** | 59.6 % | 64.0 % | 52.4 % | 57.6 % |

These figures are taken from Table 2, which reports the results of the ablated versions of LightRAG (the “‑High” configuration) compared with NaiveRAG as a reference [C3].</pre>

## ZH_COST — repetition 1

Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Sub-queries: []

Total evaluation latency_ms: 8165.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| chinese_answer | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。  <br>在檢索階段，GraphRAG 必須先產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000），且因為需要逐一遍歷社群，會產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，幾乎不產生額外的 token 或呼叫成本[C4]。 |
| retrieval_cost | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。  <br>在檢索階段，GraphRAG 必須先產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000），且因為需要逐一遍歷社群，會產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，幾乎不產生額外的 token 或呼叫成本[C4]。 |
| numbers_unchanged | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 必須先產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000），且因為需要逐一遍歷社群，會產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2625 | 2400 | 425 | 3000 | 10000 | 2657.09 | stop |
| 2 | judge | low | 876 | 651 | 276 | 1000 | 10000 | 1415.91 | stop |
| 3 | judge | low | 923 | 698 | 519 | 1000 | 10000 | 2117.84 | stop |
| 4 | judge | low | 908 | 683 | 362 | 1000 | 10000 | 1698.15 | stop |

### Finalized answer

<pre>LightRAG 的檢索成本遠低於 GraphRAG。  
在檢索階段，GraphRAG 必須先產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token（610 × 1,000），且因為需要逐一遍歷社群，會產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，幾乎不產生額外的 token 或呼叫成本[C4]。  

因此，LightRAG 在檢索時的 token 用量與 API 呼叫次數皆遠低於 GraphRAG，顯著降低了檢索成本。</pre>

## LIMITATIONS — repetition 1

Question: 這篇論文有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: 這篇論文有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 5123.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| citation_sections | events | FAIL | 0 distinct cited Sections; requires 2 |  |
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| evaluation_limit | judge | FAIL | Required claim not asserted |  |
| retrieval_tradeoff | judge | FAIL | Required claim not asserted |  |
| not_universally_best | judge | FAIL | Required claim not asserted |  |
| no_invented_limit | forbidden | FAIL | Forbidden claim asserted | Not mentioned in the document. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2565 | 2340 | 213 | 3000 | 10000 | 1477.54 | stop |
| 2 | judge | low | 676 | 451 | 65 | 1000 | 10000 | 729.78 | stop |
| 3 | judge | low | 693 | 468 | 66 | 1000 | 10000 | 688.76 | stop |
| 4 | judge | low | 676 | 451 | 63 | 1000 | 10000 | 678.68 | stop |
| 5 | judge | low | 673 | 448 | 250 | 1000 | 10000 | 1370.89 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Total evaluation latency_ms: 2133.16

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2312 | 2087 | 131 | 3000 | 10000 | 960.07 | stop |
| 2 | judge | low | 659 | 434 | 109 | 1000 | 10000 | 857.13 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Total evaluation latency_ms: 1700.47

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | Not mentioned in the document. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2356 | 2131 | 67 | 3000 | 10000 | 749.18 | stop |
| 2 | judge | low | 660 | 435 | 78 | 1000 | 10000 | 747.42 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Total evaluation latency_ms: 2772.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2176 | 1951 | 227 | 3000 | 10000 | 1736.57 | stop |
| 2 | judge | low | 659 | 434 | 109 | 1000 | 10000 | 856.81 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Total evaluation latency_ms: 2935.45

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 576 | 3000 | 10000 | 2758.45 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism. The system combines low‑level retrieval (focused on precise entity information) with high‑level retrieval (covering broader topics), allowing it to capture complex inter‑dependencies among entities and produce more coherent, context‑rich responses [C1][C2].  

The authors evaluate LightRAG on four heterogeneous datasets—Agriculture (12 documents, 2,017,886 tokens), Computer Science (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and a mixed set (61 documents, 619,009 tokens) [C5]. Experimental results (Table 2) compare LightRAG with a baseline NaïveRAG across three quality dimensions—Comprehensiveness, Diversity, and Empowerment—and an overall score. Using the “High” configuration as baseline, LightRAG improves overall performance from 32.4 % to 67.6 % on the Agriculture domain, from 38.8 % to 61.2 % on CS, from 15.2 % to 84.8 % on Legal, and from 40.0 % to 60.0 % on the Mix domain [C3]. Similar gains are observed under “Low” and “Origin” configurations, with LightRAG consistently achieving higher percentages across all metrics [C4].  

An illustrative case shows LightRAG processing a query about movie‑recommendation evaluation metrics: the LLM extracts low‑ and high‑level keywords, which guide the dual‑level retrieval to fetch relevant entities and relationships before generating the final answer [C5].  

Overall, LightRAG’s integration of graph structures with vector representations, its incremental update algorithm, and its dual‑level retrieval strategy lead to notable improvements in retrieval accuracy, efficiency, and adaptability compared with existing RAG approaches. [C1][C2][C3][C4][C5]</pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Lookup; expected: Global

Standalone Question: 這篇在講什麼？

Sub-queries: []

Total evaluation latency_ms: 3186.67

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2729 | 2504 | 519 | 3000 | 10000 | 2940.23 | stop |

### Finalized answer

<pre>這篇文件介紹了 **LightRAG** 框架——一種結合圖結構與向量表示的檢索增強生成（RAG）系統。  
- 透過實體與關係抽取（如「Beekeeper」的描述與其與蜜蜂的關聯）建立圖形化知識庫，並以雙層檢索範式同時支援 **低階檢索**（針對具體實體與屬性）與 **高階檢索**（聚合多個實體以提供概念性摘要）[C1][C2]。  
- 系統在查詢時先抽取本地與全域關鍵詞，分別在向量資料庫中匹配實體與關係，從而提升檢索的相關性與效率[C2]。  
- 為評估 LightRAG 的高層次意義建構（sensemaking）能力，作者將多個資料集的全文作為上下文，使用 LLM 產生使用者與任務，並生成大量需要全局理解的問題，最後與 Naive RAG、RQ‑RAG、HyDE 等先進基線進行比較[C3]。  
- 文件最後列出相關的研究參考文獻，涵蓋圖‑文本嵌入、RAG 方法與評估等領域[C4]。  </pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Lookup; expected: Global

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Total evaluation latency_ms: 2616.44

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2345 | 2120 | 510 | 3000 | 10000 | 2446.71 | stop |

### Finalized answer

<pre>**Key takeaways of the LightRAG paper**

1. **Motivation and Problem** – Existing Retrieval‑Augmented Generation (RAG) systems rely on flat data representations and lack sufficient contextual awareness, often producing fragmented answers that miss complex inter‑dependencies[C1].  

2. **Graph‑based text indexing** – LightRAG introduces a graph‑enhanced indexing module that extracts entities and their relationships from documents, builds a knowledge graph \( \hat D = (\hat V,\hat E) \) and stores it as a deduplicated structure for retrieval[C2].  

3. **Dual‑level retrieval** – The system employs a two‑stage retrieval process (low‑level and high‑level keyword extraction) that enables both fine‑grained and high‑level information discovery, improving the relevance of retrieved passages[C2][C4].  

4. **Fast adaptation to data changes** – An incremental update algorithm continuously integrates new data into the graph‑based index, keeping the system up‑to‑date in dynamic environments[C1].  

5. **Efficiency and accuracy gains** – Experiments on four datasets (Agriculture, CS, Legal, Mix) show that LightRAG achieves considerably higher retrieval accuracy and faster response times compared with baseline approaches such as NaiveRAG[C3][C5].  

6. **Comprehensive evaluation** – The authors assess LightRAG on dimensions of **comprehensiveness**, **diversity**, and **empowerment**, using specially designed prompts for keyword extraction and RAG evaluation; LightRAG consistently outperforms baselines in these criteria[C4][C5].  

7. **Open‑source release** – The full LightRAG framework, including code and data, is publicly available on GitHub, encouraging reproducibility and further research[C1].</pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Total evaluation latency_ms: 3730.23

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 755 | 3000 | 10000 | 3558.47 | stop |

### Finalized answer

<pre>**Overall performance**

The experimental tables compare LightRAG and GraphRAG on four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall). For each dimension the percentages represent the win‑rate of the method against the other baseline. Across all reported datasets LightRAG consistently achieves higher win‑rates than GraphRAG (e.g., 54.4 % vs 45.6 % in Comprehensiveness, 77.2 % vs 22.8 % in Diversity, 58.8 % vs 41.2 % in Empowerment, and 54.8 % vs 45.2 % overall)[C2]. This indicates that LightRAG more frequently produces superior answers than GraphRAG on the measured criteria.

**Specific advantages of LightRAG**

- **Diversity:** LightRAG shows a marked lead in the Diversity metric, especially on the large Legal dataset, reflecting its ability to generate a wider range of responses. The authors attribute this to LightRAG’s dual‑level retrieval paradigm that combines low‑level entity retrieval with high‑level topic retrieval[C3].  
- **Complex query handling:** By accessing both specific details and broader themes, LightRAG better addresses complex queries that involve interconnected topics, providing more contextually relevant answers[C3].  
- **Comprehensiveness and empowerment:** The dual‑level, graph‑based indexing of LightRAG enables broader coverage of machine‑learning metrics and more empowering content, outperforming GraphRAG in these aspects[C4].

**Conclusion**

Across quantitative win‑rate tables and qualitative analysis, LightRAG outperforms GraphRAG on all evaluated dimensions, particularly in larger, more complex corpora where its dual‑level, graph‑enhanced retrieval strategy yields more comprehensive, diverse, and empowering responses[C2][C3][C4].</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 有什麼限制？

Sub-queries: []

Total evaluation latency_ms: 1623.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2479 | 2254 | 205 | 3000 | 10000 | 1469.48 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Lookup; expected: Synthesis

Standalone Question: How do the experiments support the paper&#x27;s claims?

Sub-queries: []

Total evaluation latency_ms: 7132.25

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2692 | 2467 | 882 | 3000 | 10000 | 4410.23 | stop |

### Finalized answer

<pre>The experimental results directly back the paper’s main claims:

* **Superior effectiveness across domains and metrics** – On the four benchmark datasets (Agriculture, CS, Legal, Mix), LightRAG consistently achieves higher win‑rates than the three baselines (NaiveRAG, RQ‑RAG, HyDE) for every evaluation dimension (Comprehensiveness, Diversity, Empowerment) and for the overall score. For example, LightRAG’s win‑rate on the Legal set is 84.8 % overall versus 15.2 % for NaiveRAG, and similar gaps appear for the other baselines and datasets[C1].  

* **Ablation studies confirm the contribution of the dual‑level retrieval design** – When the high‑level retrieval component is removed (NaiveRAG‑High) or the low‑level component is removed (NaiveRAG‑Low), the win‑rates drop noticeably across all datasets and dimensions. The full LightRAG model outperforms these ablated versions, demonstrating that both low‑level and high‑level retrieval are essential for the observed gains[C2].  

* **Qualitative evaluation shows better diversity, empowerment, and overall answer quality** – Human judges selected LightRAG’s answers as the “Winner” for Diversity, Empowerment, and the Overall category, citing richer coverage of metrics, nuanced explanations, and more informative context that helps readers make informed judgments[C3].  

* **Cost‑efficiency advantage** – Compared with GraphRAG on the Legal dataset, LightRAG requires far fewer tokens (≈1 400 × 2 vs. 610 × 1 000) and fewer API calls, indicating a lower computational and monetary cost while delivering higher performance[C3].  

* **Robust experimental setup** – The experiments are conducted on four diverse corpora (Agriculture, CS, Legal, Mix) with substantial token counts (ranging from ~0.6 M to &gt;5 M tokens), ensuring that the reported improvements are not limited to a single domain[C5].  

Together, these quantitative win‑rate tables, ablation results, human‑rated answer quality, and cost analysis provide concrete empirical evidence that LightRAG outperforms existing RAG baselines, validates the design choices, and fulfills the paper’s claims of higher effectiveness and efficiency.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 4021.33

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1130 | 3000 | 10000 | 3923.94 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (using NaiveRAG as the reference baseline)**  

| Dataset | Metric | NaiveRAG (baseline) | LightRAG (ablated) |
|---------|--------|---------------------|--------------------|
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

*High‑knowledge‑density (NaiveRAG‑High) ablation*  

| Dataset | Metric | NaiveRAG‑High | LightRAG |
|---------|--------|--------------|----------|
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

*Low‑knowledge‑density (NaiveRAG‑Low) ablation* – the document lists only the NaiveRAG‑Low rows without accompanying LightRAG numbers, so no comparative LightRAG values are provided for this condition.

All figures are taken directly from Table 2, which reports the performance of ablated versions of LightRAG versus NaiveRAG across four domains and three knowledge‑density settings [C3].</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Standalone Question: What datasets were used?

Sub-queries: []

Total evaluation latency_ms: 1003.25

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2641 | 2416 | 118 | 3000 | 10000 | 880.84 | stop |

### Finalized answer

<pre>The experiments used four datasets from the UltraDomain benchmark: **Agriculture**, **CS** (computer science), **Legal**, and **Mix**[C1][C5]</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Sub-queries: []

Total evaluation latency_ms: 10886.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2528 | 2303 | 1745 | 3000 | 10000 | 7921.54 | stop |

### Finalized answer

<pre>60.8% [C4]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Total evaluation latency_ms: 1091.55

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2156 | 1931 | 110 | 3000 | 10000 | 893.66 | stop |

### Finalized answer

<pre>LightRAG needs only one API call for the entire retrieval process[C3].</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Standalone Question: 那 LightRAG 呢？

Sub-queries: []

Total evaluation latency_ms: 5410.57

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2144 | 1919 | 1081 | 3000 | 10000 | 5303.53 | stop |

### Finalized answer

<pre>LightRAG 是一种检索增强生成（RAG）系统，采用图结构进行文本索引和检索，实现了对实体及其关系的高效检索[C1]。它使用双层检索范式，能够从低层次和高层次两方面发现信息，支持对具体和抽象信息的提取，并通过增量更新算法及时将新数据加入知识图谱，保持在快速变化环境中的有效性[C1][C5]。在实现细节上，LightRAG 使用 nano 向量数据库管理向量数据，所有 LLM 操作默认使用 GPT‑4o‑mini，块大小设为 1200，gleaning 参数固定为 1，适用于 GraphRAG 与 LightRAG[C2]。  

实验结果显示，在综合性、 多样性、赋能和整体四个评估维度上，LightRAG 的胜率均显著高于 GraphRAG 等基线，例如在综合性维度上 LightRAG 获得 54.4%‑59.6% 的胜率，而 GraphRAG 仅为 26.0%‑45.6%[C3]。与纯块式检索方法（如 NaiveRAG、HyDE、RQRAG）相比，LightRAG 在大规模语料（如 Legal 数据集）上表现出更高的胜率，基线方法仅约 20% 而 LightRAG 占优势[C3]。通过图结构与向量表示的结合，LightRAG 能够快速检索相关实体及其关系，提升检索速度并保持上下文相关性[C1][C5]。该系统已开源，代码托管在 GitHub（https://github.com/HKUDS/LightRAG）[C1]。</pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Lookup; expected: Synthesis

Standalone Question: 那它跟 GraphRAG 比呢？

Sub-queries: []

Total evaluation latency_ms: 4236.12

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2619 | 2394 | 672 | 3000 | 10000 | 4075.55 | stop |

### Finalized answer

<pre>LightRAG 在各项评估指标上均优于 GraphRAG。  
- 在 **Comprehensiveness**、**Diversity**、**Empowerment** 以及 **Overall** 四个维度的胜率中，LightRAG 的得分均高于 GraphRAG（例如在第一组实验中，LightRAG 的 Overall 胜率为 54.8% 而 GraphRAG 为 45.2%）[C2]。  
- 在 **成本** 上，检索阶段 GraphRAG 需要遍历 610 个社区，每个社区报告约 1 000 tokens，累计约 610 000 tokens，并产生数百次 API 调用；而 LightRAG 只使用不足 100 tokens 生成关键词并完成检索，仅需一次 API 调用[C4]。  
- 在 **增量更新** 场景，GraphRAG 必须拆除并重新生成全部社区结构，导致约 1 399 × 2 × 5 000 tokens 的巨额开销；LightRAG 则直接将新抽取的实体和关系并入现有图中，无需完整重建，成本显著更低[C5]。  

综上，LightRAG 在回答质量、检索效率以及动态更新成本方面均相较于 GraphRAG 有明显优势。</pre>

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
| 1 | judge | low | 672 | 447 | 119 | 1000 | 10000 | 989.92 | stop |

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
| 1 | judge | low | 686 | 461 | 114 | 1000 | 10000 | 1380.30 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
