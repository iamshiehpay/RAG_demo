# Golden Facts evaluation

Created: 2026-10-12T17:00:11.266506+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: router-provenance

Revision: a27409acdbfaca7408fb868f1e783134c1a13cdc

Uncommitted changes: no

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: chat_document.router_regression.CASES (#06 canonical 12 cases)

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 1/1 (100.0%) |
| Q1 | motivation | judge | 0/1 (0.0%) |
| Q1 | graph_indexing | judge | 0/1 (0.0%) |
| Q1 | dual_level | judge | 1/1 (100.0%) |
| Q1 | incremental_update | judge | 0/1 (0.0%) |
| Q1 | experiments | judge | 0/1 (0.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 0/1 (0.0%) |
| Q2 | question_type | events | 1/1 (100.0%) |
| Q2 | retrieval_methods | judge | 0/1 (0.0%) |
| Q2 | retrieval_cost | judge | 1/1 (100.0%) |
| Q2 | incremental_update | judge | 0/1 (0.0%) |
| Q2 | table1_agriculture_overall | judge | 0/1 (0.0%) |
| Q2 | table1_cs_overall | judge | 0/1 (0.0%) |
| Q2 | table1_legal_overall | judge | 0/1 (0.0%) |
| Q2 | table1_mix_overall | judge | 0/1 (0.0%) |
| Q2 | table3_case_study | judge | 1/1 (100.0%) |
| Q2 | not_all_datasets | forbidden | 1/1 (100.0%) |
| Q3 | table2_citation | events | 1/1 (100.0%) |
| Q3 | question_type | events | 1/1 (100.0%) |
| Q3 | high_term | contains | 1/1 (100.0%) |
| Q3 | low_term | contains | 0/1 (0.0%) |
| Q3 | origin_term | contains | 0/1 (0.0%) |
| Q3 | table2_baseline | judge | 0/1 (0.0%) |
| Q3 | ablation_meaning | judge | 0/1 (0.0%) |
| Q3 | mix_low_overall | judge | 0/1 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/1 (0.0%) |
| Q3 | not_all_best | forbidden | 1/1 (100.0%) |
| ROUTER_01 | question_type | events | 1/1 (100.0%) |
| ROUTER_02 | question_type | events | 1/1 (100.0%) |
| ROUTER_03 | question_type | events | 1/1 (100.0%) |
| ROUTER_04 | question_type | events | 1/1 (100.0%) |
| ROUTER_05 | question_type | events | 1/1 (100.0%) |
| ROUTER_06 | question_type | events | 1/1 (100.0%) |
| ROUTER_07 | question_type | events | 1/1 (100.0%) |
| ROUTER_08 | question_type | events | 1/1 (100.0%) |
| ROUTER_09 | question_type | events | 1/1 (100.0%) |
| ROUTER_10 | question_type | events | 1/1 (100.0%) |
| ROUTER_11 | question_type | events | 1/1 (100.0%) |
| ROUTER_11 | standalone_rewrite | events | 1/1 (100.0%) |
| ROUTER_12 | question_type | events | 1/1 (100.0%) |
| ROUTER_12 | standalone_rewrite | events | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the summary of this document?

Sub-queries: []

Ask latency_ms: 10167.93

Judge latency_ms: 10174.22

Total evaluation latency_ms: 20353.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Data Indexer φ(·), which builds a graph‑structured index \(\hat D\) from an external database \(D\) by extracting entities and their relationships and deduplicating them into a knowledge graph[C2]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG’s dual‑level retrieval operates at:<br><br>* **Low‑level** – precise extraction of specific entities and their relations.<br>* **High‑level** – broader thematic retrieval of related topics. |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 118 | 600 | 10000 | 1005.67 | stop |
| 2 | answer | medium | 1761 | 1536 | 495 | 3000 | 10000 | 3084.17 | stop |
| 3 | judge | low | 1044 | 819 | 89 | 1000 | 10000 | 1362.21 | stop |
| 4 | judge | low | 1039 | 814 | 151 | 1000 | 10000 | 2264.34 | stop |
| 5 | judge | low | 1041 | 816 | 147 | 1000 | 10000 | 1630.18 | stop |
| 6 | judge | low | 1047 | 822 | 122 | 1000 | 10000 | 1002.32 | stop |
| 7 | judge | low | 1050 | 825 | 93 | 1000 | 10000 | 884.90 | stop |
| 8 | judge | low | 1047 | 822 | 73 | 1000 | 10000 | 780.37 | stop |
| 9 | judge | low | 1040 | 815 | 95 | 1000 | 10000 | 2249.88 | stop |

### Finalized answer

<pre>The paper introduces **LightRAG**, a Retrieval‑Augmented Generation (RAG) system that combines graph‑based text indexing with a dual‑level retrieval framework to better capture complex inter‑dependencies among entities and produce more coherent, context‑rich responses[C1].  

Key components of the architecture are:  

* **Data Indexer φ(·)**, which builds a graph‑structured index \(\hat D\) from an external database \(D\) by extracting entities and their relationships and deduplicating them into a knowledge graph[C2].  
* **Data Retriever ψ(·)**, which retrieves “relevant documents” by comparing a query against the indexed graph, feeding the results together with the original query into a generative model \(G(·)\) for answer generation[C2].  

LightRAG’s dual‑level retrieval operates at:  

* **Low‑level** – precise extraction of specific entities and their relations.  
* **High‑level** – broader thematic retrieval of related topics.  

The system is designed to achieve three main goals:  

1. **Comprehensive information retrieval** by leveraging the global graph structure to capture all relevant context[C2].  
2. **Efficient, low‑cost retrieval** through the graph‑based index, enabling rapid response even under high query volumes[C2].  
3. **Fast adaptation to new data** by quickly updating the graph when external knowledge changes[C2].  

Experimental evaluation uses four datasets (Agriculture, CS, Legal, Mix) with a total of 177 documents and over 10 million tokens, demonstrating LightRAG’s ability to handle diverse domains[C3].  

Overall, LightRAG advances RAG by integrating graph‑enhanced entity/relationship extraction with dual‑level retrieval, delivering more comprehensive and adaptable generation performance.</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG architecture&#x27;, &#x27;LightRAG performance compared to GraphRAG&#x27;, &#x27;LightRAG and GraphRAG cost and maintenance&#x27;]

Ask latency_ms: 13983.73

Judge latency_ms: 13974.05

Total evaluation latency_ms: 27977.54

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | PASS | Required claim supported by verbatim evidence | GraphRAG’s retrieval process is far more token‑ and API‑intensive. It creates 1,399 communities, actively uses 610 level‑2 communities, and generates community reports that total about 610,000 tokens (610 × 1,000) [C4]. Traversing each community also requires hundreds of API calls. By contrast, LightRAG generates fewer than 100 tokens for keyword generation and retrieval and completes the entire retrieval with a single API call [C4]. |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | Overall 54.8 % vs 45.2 % |
| table1_cs_overall | judge | FAIL | Required claim not asserted |  |
| table1_legal_overall | judge | FAIL | Required claim not asserted |  |
| table1_mix_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | When evaluated on the four LLM‑based dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG consistently attains higher win‑rate percentages than GraphRAG. For example, in the first experimental setting LightRAG wins 74.0 % of the Comprehensiveness judgments versus GraphRAG’s 26.0 % [C2]; in Diversity it wins 76.0 % versus 24.0 %; in Empowerment 74.8 % versus 25.2 %; and overall 75.2 % versus 24.8 %. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 141 | 600 | 10000 | 1611.19 | stop |
| 2 | answer | medium | 1820 | 1595 | 1013 | 3000 | 10000 | 7872.88 | stop |
| 3 | judge | low | 1156 | 931 | 159 | 1000 | 10000 | 4956.70 | stop |
| 4 | judge | low | 1193 | 968 | 263 | 1000 | 10000 | 1759.53 | stop |
| 5 | judge | low | 1153 | 928 | 81 | 1000 | 10000 | 800.23 | stop |
| 6 | judge | low | 1169 | 944 | 170 | 1000 | 10000 | 1127.73 | stop |
| 7 | judge | low | 1169 | 944 | 123 | 1000 | 10000 | 899.48 | stop |
| 8 | judge | low | 1169 | 944 | 134 | 1000 | 10000 | 862.63 | stop |
| 9 | judge | low | 1169 | 944 | 98 | 1000 | 10000 | 1363.79 | stop |
| 10 | judge | low | 1161 | 936 | 222 | 1000 | 10000 | 1107.35 | stop |
| 11 | judge | low | 1154 | 929 | 125 | 1000 | 10000 | 1096.62 | stop |

### Finalized answer

<pre>LightRAG and GraphRAG are both graph‑enhanced retrieval‑augmented generation (RAG) systems that share several implementation choices: they both use a chunk size of 1200, a gleaning parameter of 1, and rely on the same LLM (GPT‑4o‑mini) for all LLM‑based operations [C1].

**Performance comparison**  
When evaluated on the four LLM‑based dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG consistently attains higher win‑rate percentages than GraphRAG. For example, in the first experimental setting LightRAG wins 74.0 % of the Comprehensiveness judgments versus GraphRAG’s 26.0 % [C2]; in Diversity it wins 76.0 % versus 24.0 %; in Empowerment 74.8 % versus 25.2 %; and overall 75.2 % versus 24.8 %. Even in later settings where the gap narrows, LightRAG still leads (e.g., Overall 54.8 % vs 45.2 %) [C2]. These figures indicate that LightRAG provides more comprehensive, diverse, and empowering answers across the tested queries.

**Cost and efficiency comparison**  
GraphRAG’s retrieval process is far more token‑ and API‑intensive. It creates 1,399 communities, actively uses 610 level‑2 communities, and generates community reports that total about 610,000 tokens (610 × 1,000) [C4]. Traversing each community also requires hundreds of API calls. By contrast, LightRAG generates fewer than 100 tokens for keyword generation and retrieval and completes the entire retrieval with a single API call [C4]. This makes LightRAG dramatically more efficient in both token consumption and API usage.

**Summary**  
- Both systems use the same chunk size, gleaning parameter, and LLM (GPT‑4o‑mini) [C1].  
- LightRAG outperforms GraphRAG on win‑rate metrics for all four evaluation dimensions, indicating superior answer quality [C2].  
- LightRAG is far more cost‑effective, needing &lt;100 tokens and one API call, whereas GraphRAG consumes ~610 k tokens and hundreds of API calls during retrieval [C4].</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 31702.73

Judge latency_ms: 8113.17

Total evaluation latency_ms: 39833.15

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required source Chunk (metadata fallback) | C3 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | FAIL | Term missing |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The ablation study (Table 2) reports LightRAG’s performance—compared with the NaïveRAG baseline—on four benchmark collections ... \| Collection \| Metric \| NaïveRAG \| **LightRAG (ablated)** \|<br>\|------------\|--------\|---------\|------------------------\| |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 116 | 600 | 10000 | 1003.47 | stop |
| 2 | answer | medium | 2113 | 1888 | 1510 | 3000 | 10000 | 7312.99 | stop |
| 3 | judge | low | 1355 | 1130 | 353 | 1000 | 10000 | 1550.51 | stop |
| 4 | judge | low | 1356 | 1131 | 95 | 1000 | 10000 | 759.96 | stop |
| 5 | judge | low | 1367 | 1142 | 248 | 1000 | 10000 | 1259.59 | stop |
| 6 | judge | low | 1367 | 1142 | 143 | 1000 | 10000 | 1924.55 | stop |
| 7 | judge | low | 1343 | 1118 | 143 | 1000 | 10000 | 2618.55 | stop |

### Finalized answer

<pre>The ablation study (Table 2) reports LightRAG’s performance—compared with the NaïveRAG baseline—on four benchmark collections (Agriculture, CS, Legal, Mix) for four evaluation dimensions:

| Collection | Metric | NaïveRAG | **LightRAG (ablated)** |
|------------|--------|---------|------------------------|
| **Agriculture** | Comprehensiveness | 32.4 % | **67.6 %** |
| | Diversity | 23.6 % | **76.4 %** |
| | Empowerment | 32.4 % | **67.6 %** |
| | Overall | 32.4 % | **67.6 %** |
| **CS** | Comprehensiveness | 38.4 % | **61.6 %** |
| | Diversity | 38.0 % | **62.0 %** |
| | Empowerment | 38.8 % | **61.2 %** |
| | Overall | 38.8 % | **61.2 %** |
| **Legal** | Comprehensiveness | 16.4 % | **83.6 %** |
| | Diversity | 13.6 % | **86.4 %** |
| | Empowerment | 16.4 % | **83.6 %** |
| | Overall | 15.2 % | **84.8 %** |
| **Mix** | Comprehensiveness | 38.8 % | **61.2 %** |
| | Diversity | 32.4 % | **67.6 %** |
| | Empowerment | 42.8 % | **57.2 %** |
| | Overall | 40.0 % | **60.0 %** |

The table also includes a “high‑resource” ablation (NaïveRAG‑High vs. LightRAG‑High). In this setting LightRAG again outperforms the baseline:

| Collection | Metric | NaïveRAG‑High | **LightRAG‑High** |
|------------|--------|---------------|-------------------|
| Agriculture | Comprehensiveness | 34.8 % | **65.2 %** |
| | Diversity | 27.2 % | **72.8 %** |
| | Empowerment | 36.0 % | **64.0 %** |
| | Overall | 35.2 % | **64.8 %** |
| CS | Comprehensiveness | 42.8 % | **57.2 %** |
| | Diversity | 23.6 % | **76.4 %** |
| | Empowerment | 40.4 % | **59.6 %** |
| | Overall | — | — |

These results demonstrate that even when components of LightRAG are removed (ablated), the system retains a large advantage over the NaïveRAG baseline across all datasets and evaluation dimensions [C3].</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summary this document.

Sub-queries: []

Ask latency_ms: 3550.99

Judge latency_ms: 0.00

Total evaluation latency_ms: 3551.11

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 116 | 600 | 10000 | 1562.97 | stop |
| 2 | answer | medium | 1582 | 1357 | 369 | 3000 | 10000 | 1785.43 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that improves large language models (LLMs) by incorporating graph‑structured representations of text. By indexing documents as entities and relationships, LightRAG enables a dual‑level retrieval system that captures both low‑level keywords and high‑level semantic connections, leading to more comprehensive and context‑aware answers. The system also combines graph structures with vector embeddings for fast entity‑relationship retrieval and includes an incremental update algorithm to keep the knowledge base current. Experiments on four benchmark datasets—Agriculture (12 documents, 2,017,886 tokens), CS (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and Mix (61 documents, 619,009 tokens)—show that LightRAG achieves higher scores across multiple evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall) compared with a NaiveRAG baseline; for example, overall performance improves from 44.4 %/55.6 % (NaiveRAG) to 35.2 %/64.8 % (LightRAG) on the reported splits[C2]. The paper details the entity‑extraction pipeline, prompt templates, and evaluation criteria in its appendix, and the code has been released as open‑source[C1][C3].</pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 這篇文章在講什麼？

Sub-queries: []

Ask latency_ms: 4377.09

Judge latency_ms: 0.00

Total evaluation latency_ms: 4377.13

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 836 | 497 | 98 | 600 | 10000 | 770.33 | stop |
| 2 | answer | medium | 1883 | 1658 | 587 | 3000 | 10000 | 3457.67 | stop |

### Finalized answer

<pre>本文介紹了一種名為 LightRAG 的檢索增強生成框架，該框架採用圖式文本索引與雙層檢索範式，並結合實體與關係抽取，以處理如「Beekeeper」等實體的描述與關聯（C1）。文章在多個資料集上進行了實驗，包括法律領域、混合領域以及與蜜蜂相關的實體資料，並將 LightRAG 與 Naive RAG、RQ‑RAG、HyDE 等最新基線方法進行了全面比較（C2）。最後，文中列出了多篇相關研究，涵蓋檢索增強生成、圖模型及其在各類任務中的應用（C3）。</pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Ask latency_ms: 5341.53

Judge latency_ms: 0.00

Total evaluation latency_ms: 5341.69

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 59 | 600 | 10000 | 1242.72 | stop |
| 2 | answer | medium | 1497 | 1272 | 404 | 3000 | 10000 | 3932.97 | stop |

### Finalized answer

<pre>- LightRAG is a Retrieval‑Augmented Generation (RAG) framework that enhances large language models by **integrating graph structures into text indexing and retrieval**, enabling more accurate and context‑aware responses [C1].

- It employs a **dual‑level retrieval system** that extracts both low‑level (specific entities) and high‑level (broad concepts) keywords from a query and uses them to retrieve information from two complementary knowledge layers [C1][C3].

- The combination of **graph structures with vector representations** allows efficient retrieval of related entities and their relationships, improving both **retrieval accuracy and response time** [C1].

- An **incremental update algorithm** continuously incorporates new data, keeping the system effective in rapidly changing environments [C1].

- Extensive experiments on four datasets (Agriculture, CS, Legal, Mix) show **considerable improvements in retrieval accuracy and efficiency** compared with existing approaches [C2].

- The paper also provides **prompt templates** for keyword extraction (producing JSON with “high_level_keywords” and “low_level_keywords”) and for RAG evaluation (assessing answers on Comprehensiveness, Diversity, and Empowerment) [C3].

- LightRAG is **open‑source** and publicly available at https://github.com/HKUDS/LightRAG [C1].</pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG architecture vs GraphRAG architecture&#x27;, &#x27;LightRAG performance metrics compared to GraphRAG&#x27;, &#x27;LightRAG cost and maintenance compared to GraphRAG&#x27;]

Ask latency_ms: 16663.69

Judge latency_ms: 0.00

Total evaluation latency_ms: 16663.82

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 107 | 600 | 10000 | 1028.45 | stop |
| 2 | answer | medium | 1665 | 1440 | 980 | 3000 | 10000 | 13776.19 | stop |

### Finalized answer

<pre>**System architecture**

- **GraphRAG** builds a graph from the text by extracting entities and relationships, representing them as nodes and edges, generating descriptions for each element, and aggregating nodes into communities that are used to answer high‑level queries [C1].
- **LightRAG** also uses a graph‑based index, but its retrieval is hierarchical: it first performs a coarse‑grained search and then refines results through deeper graph traversal, which the authors say enables precise entity‑relation extraction and LLM profiling [C1][C3].

**Empirical performance**

Across the evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG consistently achieves higher win‑rates than GraphRAG:

| Dimension        | GraphRAG win‑rate | LightRAG win‑rate |
|-------------------|-------------------|-------------------|
| Comprehensiveness | 26.0 % / 45.6 % / 48.4 % / 48.4 % | 74.0 % / 54.4 % / 51.6 % / 51.6 % |
| Diversity         | 24.0 % / 22.8 % / 38.8 % / 40.8 % | 76.0 % / 77.2 % / 61.2 % / 59.2 % |
| Empowerment       | 25.2 % / 41.2 % / 40.8 % / 43.6 % | 74.8 % / 58.8 % / 59.2 % / 56.4 % |
| Overall           | 24.8 % / 45.2 % / 41.6 % / 47.2 % | 75.2 % / 54.8 % / 58.4 % / 52.8 % |

These results show LightRAG outperforming GraphRAG on every metric in each dataset examined [C2].

**Qualitative strengths**

- LightRAG covers a broader range of machine‑learning metrics, indicating higher **comprehensiveness** [C3].
- Its hierarchical retrieval yields a **more diverse** set of information and delivers **more empowering** content to users [C3].

**Summary**

While both systems rely on graph‑enhanced retrieval, LightRAG’s hierarchical approach leads to superior quantitative performance (higher win‑rates across all evaluation dimensions) and qualitative advantages (broader metric coverage, greater diversity, and more empowering answers) compared with GraphRAG [C1][C2][C3].</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 有什麼限制？

Sub-queries: [&#x27;LightRAG 限制因素&#x27;, &#x27;LightRAG 可擴展性與效能限制&#x27;, &#x27;LightRAG 資料更新與維護限制&#x27;]

Ask latency_ms: 9292.20

Judge latency_ms: 0.00

Total evaluation latency_ms: 9292.22

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 836 | 497 | 104 | 600 | 10000 | 1419.97 | stop |
| 2 | answer | medium | 2942 | 2717 | 164 | 3000 | 10000 | 4319.71 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How do the experiments support the paper&#x27;s claims?

Sub-queries: [&#x27;experimental results validation of claims&#x27;, &#x27;methodology evidence linking experiments to hypotheses&#x27;, &#x27;limitations of experimental support&#x27;]

Ask latency_ms: 36878.39

Judge latency_ms: 0.00

Total evaluation latency_ms: 36878.55

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 85 | 600 | 10000 | 1052.34 | stop |
| 2 | answer | medium | 3099 | 2874 | 590 | 3000 | 10000 | 8792.19 | stop |

### Finalized answer

<pre>The experimental results demonstrate that LightRAG consistently outperforms existing RAG baselines, confirming the paper’s claims of superior comprehensiveness, diversity, empowerment and overall quality.  

* **Higher win rates across all datasets and evaluation dimensions.**  
  In the four benchmark datasets (Agriculture, CS, Legal, Mix), LightRAG achieves win‑rate improvements of roughly 30–50 percentage points over NaiveRAG, RQ‑RAG and HyDE on metrics such as Comprehensiveness, Diversity, Empowerment and Overall performance (e.g., LightRAG’s Overall win rate is 67.6 % vs. 32.4 % for NaiveRAG on Agriculture)[C3].  

* **Ablation studies validate the contribution of key components.**  
  When the “High‑order relatedness” module is removed (NaiveRAG‑High), win rates drop noticeably (e.g., Overall falls from 67.6 % to 64.8 % on Agriculture), showing that incorporating neighboring graph nodes substantially boosts results[C4].  

* **Complexity analysis shows efficiency.**  
  The LightRAG framework requires only a single LLM call per text chunk, with no extra overhead for indexing, confirming that the proposed graph‑based indexing and retrieval are computationally lightweight while still delivering performance gains[C2].  

Together, these experiments substantiate the paper’s assertions that LightRAG’s dual‑level retrieval, high‑order relatedness, and efficient indexing lead to more accurate, diverse and empowering generation compared with prior RAG systems.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 7787.55

Judge latency_ms: 0.00

Total evaluation latency_ms: 7787.66

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 92 | 600 | 10000 | 2814.02 | stop |
| 2 | answer | medium | 2014 | 1789 | 762 | 3000 | 10000 | 4820.71 | stop |

### Finalized answer

<pre>The ablation study (Table 2) compares LightRAG with the NaiveRAG baseline across four data domains and reports four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall).

**Full‑domain results**

| Domain | Metric | LightRAG | NaiveRAG |
|--------|--------|----------|----------|
| **Agriculture** | Overall | 67.6 % | 32.4 % |
| **CS** | Overall | 61.2 % | 38.8 % |
| **Legal** | Overall | 84.8 % | 15.2 % |
| **Mix** | Overall | 60.0 % | 40.0 % |

In every domain LightRAG outperforms NaiveRAG on all four metrics, with gains ranging from ~20 % (Mix) to &gt;70 % (Legal) in overall performance [C3].

**High‑ablation results** (NaiveRAG‑High vs. LightRAG‑High)

| Domain | Metric | LightRAG‑High | NaiveRAG‑High |
|--------|--------|--------------|--------------|
| Agriculture | Overall | 64.8 % | 35.2 % |
| CS | Overall | 56.0 % | 44.0 % |
| Legal | Overall | 78.0 % | 22.0 % |
| Mix | Overall | 57.6 % | 42.4 % |

Again, LightRAG‑High consistently exceeds the NaiveRAG‑High baseline across all metrics [C3].

**Low‑ablation results** (NaiveRAG‑Low vs. LightRAG‑Low) are listed in the same table but the specific numbers are not shown in the excerpt; only the headings appear. Therefore, the documented performance details are limited to the full‑domain and high‑ablation comparisons above.</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What datasets were used?

Sub-queries: []

Ask latency_ms: 2458.28

Judge latency_ms: 0.00

Total evaluation latency_ms: 2458.32

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 820 | 481 | 87 | 600 | 10000 | 1089.80 | stop |
| 2 | answer | medium | 2669 | 2444 | 100 | 3000 | 10000 | 1220.49 | stop |

### Finalized answer

<pre>The experiments employed four datasets: Agriculture, CS (computer science), Legal, and Mix [C1][C5]</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Table 2 中 -Origin 在 Mix 的 Overall 數值是多少？

Sub-queries: []

Ask latency_ms: 13364.72

Judge latency_ms: 0.00

Total evaluation latency_ms: 13364.87

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 142 | 600 | 10000 | 1281.04 | stop |
| 2 | answer | medium | 2569 | 2344 | 1834 | 3000 | 10000 | 11867.74 | stop |

### Finalized answer

<pre>60.8% [C3]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Ask latency_ms: 2417.04

Judge latency_ms: 0.00

Total evaluation latency_ms: 2417.06

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 827 | 488 | 70 | 600 | 10000 | 893.39 | stop |
| 2 | answer | medium | 2191 | 1966 | 123 | 3000 | 10000 | 1036.15 | stop |

### Finalized answer

<pre>LightRAG requires only a single API call for the entire retrieval process[C3]</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 的檢索成本在論文中是多少？

Sub-queries: []

Ask latency_ms: 2605.11

Judge latency_ms: 0.00

Total evaluation latency_ms: 2607.13

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| standalone_rewrite | events | PASS | Changed question=True; missing referents/context=[]; criteria supplied=True; plan_source=router; rewrite_language_mismatch=False | LightRAG 的檢索成本在論文中是多少？ |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 868 | 539 | 94 | 600 | 10000 | 1046.05 | stop |
| 2 | answer | medium | 2415 | 2190 | 162 | 3000 | 10000 | 1456.17 | stop |

### Finalized answer

<pre>在检索阶段，LightRAG 只使用不到 100 个 token 来完成关键词生成和检索，并且整个过程只需一次 API 调用[C3].</pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 跟 GraphRAG 比較如何？

Sub-queries: [&#x27;LightRAG 與 GraphRAG 的檢索機制差異&#x27;, &#x27;LightRAG 與 GraphRAG 的效能與成本比較&#x27;, &#x27;LightRAG 與 GraphRAG 的增量更新與維護方式&#x27;]

Ask latency_ms: 10141.35

Judge latency_ms: 0.00

Total evaluation latency_ms: 10143.43

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| standalone_rewrite | events | PASS | Changed question=True; missing referents/context=[]; criteria supplied=True; plan_source=router; rewrite_language_mismatch=False | LightRAG 跟 GraphRAG 比較如何？ |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 859 | 530 | 131 | 600 | 10000 | 1299.63 | stop |
| 2 | answer | medium | 2527 | 2302 | 698 | 3000 | 10000 | 7014.69 | stop |

### Finalized answer

<pre>LightRAG 在多项评估指标上均优于 GraphRAG，尤其在大规模、语义复杂的数据集上表现更为突出。

1. **整体表现**  
   - 在 **Comprehensiveness、Diversity、Empowerment** 以及 **Overall** 四个维度的胜率上，LightRAG 的得分均高于 GraphRAG。例如，在 Legal 数据集的 Overall 维度，LightRAG 获得 54.8% 的胜率，而 GraphRAG 仅为 45.2%[C2]。  
   - 这一趋势在 Agriculture、CS 等包含数百万 token 的数据集上同样显著，LightRAG 明显领先于 GraphRAG[C3]。

2. **响应多样性**  
   - LightRAG 在 Diversity 指标上持续领先，尤其在 Legal 数据集上表现出显著优势，说明其能够生成更丰富、视角更广的答案[C3]。这得益于其 **双层检索范式**：低层检索具体实体，高层检索更广泛主题，从而捕获完整上下文[C3]。

3. **增量更新效率**  
   - 在处理新增数据时，GraphRAG 需要拆除并重新生成所有社区报告，代价约为 5,000 token/社区，若有 1,399 个社区则需约 14 M token，成本极高[C5]。  
   - 相比之下，LightRAG 能直接将新抽取的实体和关系并入现有图结构，无需完整重建，显著降低了增量更新的开销[C5]。

4. **系统设计差异**  
   - GraphRAG 通过 LLM 提取实体与关系并构建图结构，随后在高层查询时遍历社区以获取更全面信息[C1]。  
   - LightRAG 同样采用图增强检索，但在实现上加入了双层检索机制和高效的图索引，使其在大规模语料和复杂查询下更具优势[C1][C6]。

综上所述，LightRAG 在答案完整性、响应多样性、整体性能以及增量更新成本方面均优于 GraphRAG，特别是在处理大规模、复杂语义的任务时表现更为突出。</pre>


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

Judge latency_ms: 814.06

Total evaluation latency_ms: 814.06

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 83 | 1000 | 10000 | 814.06 | stop |

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

Judge latency_ms: 3305.66

Total evaluation latency_ms: 3305.66

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 3305.66 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
