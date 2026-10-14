# Golden Facts evaluation

Created: 2026-10-13T02:38:09.746097+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: qa05-integrated-0718466

Revision: 0718466a1dae475417f61f622f796ddf77429d27

Uncommitted changes: yes

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: chat_document.router_regression.CASES (#06 canonical 12 cases)

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 1/1 (100.0%) |
| Q1 | motivation | judge | 0/1 (0.0%) |
| Q1 | graph_indexing | judge | 1/1 (100.0%) |
| Q1 | dual_level | judge | 1/1 (100.0%) |
| Q1 | incremental_update | judge | 1/1 (100.0%) |
| Q1 | experiments | judge | 0/1 (0.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 508 | 283 | 103 | 1200 | 10000 | 1059.98 | stop |
| 2 | section_summary | low | 671 | 446 | 135 | 1200 | 10000 | 1172.31 | stop |
| 3 | section_summary | low | 1463 | 1238 | 212 | 1200 | 10000 | 1495.36 | stop |
| 4 | section_summary | low | 934 | 709 | 153 | 1200 | 10000 | 1726.79 | stop |
| 5 | section_summary | low | 972 | 747 | 182 | 1200 | 10000 | 857.33 | stop |
| 6 | section_summary | low | 667 | 442 | 119 | 1200 | 10000 | 794.69 | stop |
| 7 | section_summary | low | 1382 | 1157 | 259 | 1200 | 10000 | 1799.71 | stop |
| 8 | section_summary | low | 591 | 366 | 117 | 1200 | 10000 | 1439.69 | stop |
| 9 | section_summary | low | 545 | 320 | 162 | 1200 | 10000 | 1926.21 | stop |
| 10 | section_summary | low | 1532 | 1307 | 266 | 1200 | 10000 | 1716.74 | stop |
| 11 | section_summary | low | 1047 | 822 | 165 | 1200 | 10000 | 1484.75 | stop |
| 12 | section_summary | low | 1483 | 1258 | 305 | 1200 | 10000 | 2410.99 | stop |
| 13 | section_summary | low | 2303 | 2078 | 499 | 1200 | 10000 | 3538.10 | stop |
| 14 | section_summary | low | 2286 | 2061 | 416 | 1200 | 10000 | 3870.36 | stop |
| 15 | section_summary | low | 724 | 499 | 122 | 1200 | 10000 | 1872.43 | stop |
| 16 | section_summary | low | 689 | 464 | 171 | 1200 | 10000 | 1323.22 | stop |
| 17 | section_summary | low | 526 | 301 | 111 | 1200 | 10000 | 1041.96 | stop |
| 18 | section_summary | low | 574 | 349 | 130 | 1200 | 10000 | 1626.61 | stop |
| 19 | section_summary | low | 565 | 340 | 101 | 1200 | 10000 | 796.42 | stop |
| 20 | section_summary | low | 530 | 305 | 107 | 1200 | 10000 | 1027.17 | stop |
| 21 | section_summary | low | 541 | 316 | 103 | 1200 | 10000 | 1964.31 | stop |
| 22 | section_summary | low | 555 | 330 | 109 | 1200 | 10000 | 1653.25 | stop |
| 23 | section_summary | low | 621 | 396 | 124 | 1200 | 10000 | 1159.92 | stop |
| 24 | section_summary | low | 591 | 366 | 95 | 1200 | 10000 | 3399.09 | stop |
| 25 | section_summary | low | 1210 | 985 | 220 | 1200 | 10000 | 1551.03 | stop |
| 26 | group_summary | low | 5010 | 4785 | 1772 | 2500 | 10000 | 6680.57 | stop |
| 27 | document_summary | low | 2208 | 1983 | 1657 | 2500 | 10000 | 4564.75 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 6113.09

Judge latency_ms: 8379.67

Total evaluation latency_ms: 14504.90

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | It builds a graph‑based index by segmenting documents, prompting a large language model (LLM) to extract entities and their relations, and storing the result as a semantic graph that supports multi‑hop sub‑graph queries and key‑value look‑ups [S5]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The core retrieval mechanism is a dual‑level paradigm: low‑level retrieval generates specific query keywords to fetch precise entity‑relation facts, while high‑level retrieval extracts abstract keywords to retrieve broader thematic content; the two result sets are merged to provide both depth and breadth [S6]. |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | The design includes an incremental‑update algorithm that unions new nodes and edges with the existing graph, avoiding a full index rebuild and keeping the system up‑to‑date with minimal overhead [S5][S8]. |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Experiments were conducted on four “UltraDomain” corpora (Agriculture, Computer‑Science, Legal, and a mixed set) ... LightRAG (using GPT‑4o‑mini for LLM operations) was compared against four baselines—... using LLM‑based multi‑dimensional rankings (Comprehensiveness, Diversity, Empowerment, Overall) [S10][S11]. Across all domains LightRAG achieved majority win rates; for example, against NaiveRAG it obtained 67.6 % overall wins on the Agriculture set ... |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 85 | 600 | 10000 | 741.82 | stop |
| 2 | answer | medium | 5294 | 5069 | 1261 | 3000 | 10000 | 5354.04 | stop |
| 3 | judge | low | 1408 | 1183 | 139 | 1000 | 10000 | 1414.62 | stop |
| 4 | judge | low | 1403 | 1178 | 163 | 1000 | 10000 | 1070.88 | stop |
| 5 | judge | low | 1405 | 1180 | 196 | 1000 | 10000 | 870.64 | stop |
| 6 | judge | low | 1411 | 1186 | 172 | 1000 | 10000 | 1008.67 | stop |
| 7 | judge | low | 1414 | 1189 | 408 | 1000 | 10000 | 2074.82 | stop |
| 8 | judge | low | 1411 | 1186 | 113 | 1000 | 10000 | 940.03 | stop |
| 9 | judge | low | 1404 | 1179 | 154 | 1000 | 10000 | 1000.01 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) system that augments traditional flat‑text indexing with a knowledge‑graph structure, aiming to capture complex entity relationships and improve contextual awareness [S2][S3]. It builds a graph‑based index by segmenting documents, prompting a large language model (LLM) to extract entities and their relations, and storing the result as a semantic graph that supports multi‑hop sub‑graph queries and key‑value look‑ups [S5]. The design includes an incremental‑update algorithm that unions new nodes and edges with the existing graph, avoiding a full index rebuild and keeping the system up‑to‑date with minimal overhead [S5][S8].

The core retrieval mechanism is a dual‑level paradigm: low‑level retrieval generates specific query keywords to fetch precise entity‑relation facts, while high‑level retrieval extracts abstract keywords to retrieve broader thematic content; the two result sets are merged to provide both depth and breadth [S6]. Retrieved graph values (entity names, descriptions, original‑text excerpts) are concatenated with the user query and fed to a general‑purpose LLM for answer generation [S7].

Experiments were conducted on four “UltraDomain” corpora (Agriculture, Computer‑Science, Legal, and a mixed set) derived from 428 college textbooks (600 K–5 M tokens) [S10][S19]. LightRAG (using GPT‑4o‑mini for LLM operations) was compared against four baselines—NaiveRAG (vector‑based), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (graph‑enhanced)—using LLM‑based multi‑dimensional rankings (Comprehensiveness, Diversity, Empowerment, Overall) [S10][S11]. Across all domains LightRAG achieved majority win rates; for example, against NaiveRAG it obtained 67.6 % overall wins on the Agriculture set (versus 32.4 % for the baseline) and modest but consistent advantages over GraphRAG (e.g., 54.8 % vs 45.2 % overall on Agriculture) [S11].

Ablation studies examined the contribution of each component. Removing the high‑level module (‑High) lowered win rates to the low‑60 % range, while removing the low‑level module (‑Low) produced a similar decline, indicating that both levels provide complementary strengths [S12]. Omitting the original text from retrieval (‑Origin) did not degrade performance and even improved some scores (e.g., Agriculture overall 74.4 % vs 67.6 % for the full system), suggesting the semantic graph alone supplies sufficient context [S12].

A case study comparing LightRAG with GraphRAG on a machine‑learning query reported LightRAG winning on every LLM‑judged dimension (comprehensiveness, diversity, empowerment, overall) by offering a broader set of recommendation‑system metrics and richer explanations [S13]. Cost analysis on the Legal dataset showed LightRAG required fewer than 100 tokens and a single API call for retrieval, whereas GraphRAG consumed 610 k tokens and hundreds of calls; incremental updates also incurred far lower overhead for LightRAG because it avoids rebuilding all graph communities [S14].

The authors conclude that LightRAG’s graph‑based indexing and dual‑level retrieval markedly improve retrieval speed, answer quality, and LLM inference cost while supporting rapid incorporation of new data [S17]. Limitations and statistical significance of the reported win rates are not detailed in the excerpts [S3][S11].</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 3686.57

Judge latency_ms: 11600.80

Total evaluation latency_ms: 15311.87

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将文本分块后利用 LLM 提取实体及其关系构建知识图，并在检索阶段同时生成低层（具体实体）和高层（抽象主题）关键词，实现了图‑结构索引和双层检索的结合，以提升检索相关性和速度 |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将文本分块后利用 LLM 提取实体及其关系构建知识图，并在检索阶段同时生成低层（具体实体）和高层（抽象主题）关键词，实现了图‑结构索引和双层检索的结合，以提升检索相关性和速度 |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 该框架支持增量更新，仅需对新增文档进行一次 LLM 调用并直接合并节点和边，显著降低了索引和检索过程中的 token 使用和 API 调用量，相比 GraphRAG 在成本和适应性上更具优势 |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在四个大规模领域数据集（农业、计算机科学、法律、混合）上的实验表明，LightRAG 在全面性、 多样性、赋能和整体评分等四项指标上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型语料上优势更为明显 |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | 在四个大规模领域数据集（农业、计算机科学、法律、混合）上的实验表明，LightRAG 在全面性、 多样性、赋能和整体评分等四项指标上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型语料上优势更为明显[S10][S11]。 |
| conclusion | judge | FAIL | Required claim not asserted |  |
| chinese_summary | judge | FAIL | Required claim not asserted |  |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将文本分块后利用 LLM 提取实体及其关系构建知识图，并在检索阶段同时生成低层（具体实体）和高层（抽象主题）关键词，实现了图‑结构索引和双层检索的结合，以提升检索相关性和速度[S5][S6][S3]。  <br>在四个大规模领域数据集（农业、计算机科学、法律、混合）上的实验表明，LightRAG 在全面性、 多样性、赋能和整体评分等四项指标上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型语料上优势更为明显[S10][S11]。  <br>该框架支持增量更新，仅需对新增文档进行一次 LLM 调用并直接合并节点和边，显著降低了索引和检索过程中的 token 使用和 API 调用量，相比 GraphRAG 在成本和适应性上更具优势[S5][S14]。 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 91 | 600 | 10000 | 803.55 | stop |
| 2 | answer | medium | 5338 | 5113 | 875 | 3000 | 10000 | 2867.17 | stop |
| 3 | judge | low | 874 | 649 | 90 | 1000 | 10000 | 770.30 | stop |
| 4 | judge | low | 869 | 644 | 219 | 1000 | 10000 | 1393.16 | stop |
| 5 | judge | low | 871 | 646 | 213 | 1000 | 10000 | 1648.36 | stop |
| 6 | judge | low | 877 | 652 | 210 | 1000 | 10000 | 1012.54 | stop |
| 7 | judge | low | 880 | 655 | 270 | 1000 | 10000 | 1136.85 | stop |
| 8 | judge | low | 877 | 652 | 244 | 1000 | 10000 | 1277.03 | stop |
| 9 | judge | low | 870 | 645 | 98 | 1000 | 10000 | 710.12 | stop |
| 10 | judge | low | 871 | 646 | 109 | 1000 | 10000 | 1446.29 | stop |
| 11 | judge | low | 880 | 655 | 447 | 1000 | 10000 | 2206.15 | stop |

### Finalized answer

<pre>LightRAG 通过将文本分块后利用 LLM 提取实体及其关系构建知识图，并在检索阶段同时生成低层（具体实体）和高层（抽象主题）关键词，实现了图‑结构索引和双层检索的结合，以提升检索相关性和速度[S5][S6][S3]。  
在四个大规模领域数据集（农业、计算机科学、法律、混合）上的实验表明，LightRAG 在全面性、 多样性、赋能和整体评分等四项指标上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型语料上优势更为明显[S10][S11]。  
该框架支持增量更新，仅需对新增文档进行一次 LLM 调用并直接合并节点和边，显著降低了索引和检索过程中的 token 使用和 API 调用量，相比 GraphRAG 在成本和适应性上更具优势[S5][S14]。</pre>


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

Judge latency_ms: 1011.20

Total evaluation latency_ms: 1011.20

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 117 | 1000 | 10000 | 1011.20 | stop |

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

Judge latency_ms: 1002.35

Total evaluation latency_ms: 1002.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 130 | 1000 | 10000 | 1002.35 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
