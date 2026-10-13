# Golden Facts evaluation

Created: 2026-10-13T02:02:27.825885+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: summary-tree-global-integrated

Revision: aa5085918a8ff24fab22fc4c0ec845e6f83128da

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
| Q1 | dual_level | judge | 0/1 (0.0%) |
| Q1 | incremental_update | judge | 1/1 (100.0%) |
| Q1 | experiments | judge | 0/1 (0.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 508 | 283 | 111 | 1200 | 10000 | 859.71 | stop |
| 2 | section_summary | low | 934 | 709 | 164 | 1200 | 10000 | 967.03 | stop |
| 3 | section_summary | low | 671 | 446 | 108 | 1200 | 10000 | 1525.52 | stop |
| 4 | section_summary | low | 1463 | 1238 | 239 | 1200 | 10000 | 1772.22 | stop |
| 5 | section_summary | low | 972 | 747 | 167 | 1200 | 10000 | 935.37 | stop |
| 6 | section_summary | low | 1382 | 1157 | 257 | 1200 | 10000 | 1187.25 | stop |
| 7 | section_summary | low | 591 | 366 | 117 | 1200 | 10000 | 697.15 | stop |
| 8 | section_summary | low | 545 | 320 | 106 | 1200 | 10000 | 734.61 | stop |
| 9 | section_summary | low | 667 | 442 | 121 | 1200 | 10000 | 1455.66 | stop |
| 10 | section_summary | low | 1532 | 1307 | 272 | 1200 | 10000 | 1255.91 | stop |
| 11 | section_summary | low | 2286 | 2061 | 467 | 1200 | 10000 | 1832.88 | stop |
| 12 | section_summary | low | 1047 | 822 | 172 | 1200 | 10000 | 978.56 | stop |
| 13 | section_summary | low | 1483 | 1258 | 289 | 1200 | 10000 | 1371.56 | stop |
| 14 | section_summary | low | 724 | 499 | 123 | 1200 | 10000 | 846.56 | stop |
| 15 | section_summary | low | 689 | 464 | 191 | 1200 | 10000 | 910.17 | stop |
| 16 | section_summary | low | 2303 | 2078 | 487 | 1200 | 10000 | 2568.07 | stop |
| 17 | section_summary | low | 574 | 349 | 113 | 1200 | 10000 | 710.97 | stop |
| 18 | section_summary | low | 526 | 301 | 99 | 1200 | 10000 | 700.66 | stop |
| 19 | section_summary | low | 591 | 366 | 97 | 1200 | 10000 | 655.81 | stop |
| 20 | section_summary | low | 565 | 340 | 123 | 1200 | 10000 | 801.12 | stop |
| 21 | section_summary | low | 541 | 316 | 110 | 1200 | 10000 | 749.95 | stop |
| 22 | section_summary | low | 555 | 330 | 112 | 1200 | 10000 | 730.42 | stop |
| 23 | section_summary | low | 530 | 305 | 83 | 1200 | 10000 | 667.19 | stop |
| 24 | section_summary | low | 621 | 396 | 135 | 1200 | 10000 | 1095.70 | stop |
| 25 | section_summary | low | 1210 | 985 | 265 | 1200 | 10000 | 1352.70 | stop |
| 26 | group_summary | low | 5066 | 4841 | 2013 | 2500 | 10000 | 5243.79 | stop |
| 27 | document_summary | low | 2449 | 2224 | 1872 | 2500 | 10000 | 2884.42 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 4121.12

Judge latency_ms: 7155.00

Total evaluation latency_ms: 11306.20

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The design addresses three limitations of existing RAG methods: (i) flat vector representations that miss inter‑dependent entity relations, ... |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | Documents are first chunked, then an LLM extracts entities (nodes) and their relationships (edges) to build a compact knowledge graph ˆD; each node/edge is stored as a key‑value pair linking a short phrase to a summarising paragraph [S5]. |
| dual_level | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | the dual‑level retrieval generates both **specific (low‑level) keywords** that target individual graph nodes/edges and **abstract (high‑level) keywords** that capture broader topics |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | supports **incremental updates** that union new nodes/edges without rebuilding the whole index, keeping computational overhead low [S5][S8][S14]. |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Evaluation was performed on four “UltraDomain” corpora (Agriculture, CS, Legal, Mix) ... LightRAG was compared against four baselines—NaiveRAG (pure vector retrieval), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG ... LightRAG achieved a clear majority of pairwise wins. ... and showed especially strong gains in Diversity and Empowerment [S11]. |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | The authors conclude that LightRAG **significantly improves retrieval speed, answer quality, and adaptability**, while reducing LLM inference costs and maintaining effectiveness over time [S17]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 92 | 600 | 10000 | 668.47 | stop |
| 2 | answer | medium | 5350 | 5125 | 1238 | 3000 | 10000 | 3432.22 | stop |
| 3 | judge | low | 1461 | 1236 | 145 | 1000 | 10000 | 704.79 | stop |
| 4 | judge | low | 1456 | 1231 | 179 | 1000 | 10000 | 2099.75 | stop |
| 5 | judge | low | 1458 | 1233 | 133 | 1000 | 10000 | 732.71 | stop |
| 6 | judge | low | 1464 | 1239 | 161 | 1000 | 10000 | 772.41 | stop |
| 7 | judge | low | 1467 | 1242 | 205 | 1000 | 10000 | 939.03 | stop |
| 8 | judge | low | 1464 | 1239 | 126 | 1000 | 10000 | 764.51 | stop |
| 9 | judge | low | 1457 | 1232 | 185 | 1000 | 10000 | 1141.80 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments the standard RAG pipeline with a **graph‑based text index** and a **dual‑level retrieval paradigm**.  Documents are first chunked, then an LLM extracts entities (nodes) and their relationships (edges) to build a compact knowledge graph ˆD; each node/edge is stored as a key‑value pair linking a short phrase to a summarising paragraph [S5].  The dual‑level retrieval generates both **specific (low‑level) keywords** that target individual graph nodes/edges and **abstract (high‑level) keywords** that capture broader topics; these are matched in a vector store and expanded with one‑hop neighbours to retrieve precise as well as comprehensive information [S6][S7].

The design addresses three limitations of existing RAG methods: (i) flat vector representations that miss inter‑dependent entity relations, (ii) high retrieval latency and poor scalability, and (iii) difficulty updating the index when new data arrive [S2][S3][S15].  By combining graph structure with vector similarity, LightRAG achieves **faster, relationship‑aware retrieval** and supports **incremental updates** that union new nodes/edges without rebuilding the whole index, keeping computational overhead low [S5][S8][S14].

**Evaluation** was performed on four “UltraDomain” corpora (Agriculture, CS, Legal, Mix) ranging from 600 K to 5 M tokens [S10][S19].  LightRAG was compared against four baselines—NaiveRAG (pure vector retrieval), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (entity‑graph traversal).  Using a multi‑dimensional LLM‑based assessment (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieved a clear majority of pairwise wins.  For example, against NaiveRAG its overall win‑rates ranged from 68 % (Agriculture) to 84 % (Legal); against GraphRAG it still led on most settings (e.g., 55 % vs 45 % overall on Agriculture) and showed especially strong gains in Diversity and Empowerment [S11].

**Ablation studies** confirmed that both retrieval levels are complementary.  Removing the high‑level component reduced overall win‑rates (e.g., from 67.6 % to 64.8 % on Agriculture), while removing the low‑level component lowered overall performance despite higher Comprehensiveness in some cases.  A variant that omitted the original text and relied solely on the semantic graph performed almost on par with the full system, indicating that the graph index captures most useful information [S12].

Qualitative **case studies** further demonstrated LightRAG’s advantage.  In a comparison with GraphRAG on a recommendation‑system metrics query, LightRAG was judged superior on Comprehensiveness, Diversity, Empowerment, and Overall because it listed a broader set of metrics, explained their relationships, and provided richer contextual insight.  A similar qualitative comparison with NaiveRAG highlighted LightRAG’s deeper coverage of cultural and legal dimensions in a query about indigenous perspectives, again attributed to its dual‑level retrieval and graph indexing [S13][S25].

In terms of **computational cost**, LightRAG required fewer than 100 tokens and a single API call for retrieval on the legal dataset, whereas GraphRAG consumed 610 k tokens and hundreds of calls.  Incremental updates for LightRAG avoided the costly reconstruction of all graph communities needed by GraphRAG, leading to substantially lower token usage [S14].

The authors conclude that LightRAG **significantly improves retrieval speed, answer quality, and adaptability**, while reducing LLM inference costs and maintaining effectiveness over time [S17].</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 3195.35

Judge latency_ms: 8661.87

Total evaluation latency_ms: 11868.67

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将图结构嵌入文本索引并采用低层‑高层双层检索范式，克服了传统 RAG 系统的平面表示和上下文感知不足的问题。 |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 该框架的图‑基索引支持增量更新，仅需少量 token 和一次 API 调用即可完成检索，显著降低了模型成本并实现快速适应新数据。 |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在农业、计算机、法律和混合四个领域的实验中，LightRAG 在全面性、 多样性、赋能和整体四个维度上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型数据集上表现出显著优势。 |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将图结构嵌入文本索引并采用低层‑高层双层检索范式，克服了传统 RAG 系统的平面表示和上下文感知不足的问题。[S2][S3]  <br><br>在农业、计算机、法律和混合四个领域的实验中，LightRAG 在全面性、 多样性、赋能和整体四个维度上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型数据集上表现出显著优势。[S11][S12]  <br><br>该框架的图‑基索引支持增量更新，仅需少量 token 和一次 API 调用即可完成检索，显著降低了模型成本并实现快速适应新数据。[S5][S14] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将图结构嵌入文本索引并采用低层‑高层双层检索范式，克服了传统 RAG 系统的平面表示和上下文感知不足的问题。[S2][S3]<br><br>在农业、计算机、法律和混合四个领域的实验中，LightRAG 在全面性、 多样性、赋能和整体四个维度上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型数据集上表现出显著优势。[S11][S12]<br><br>该框架的图‑基索引支持增量更新，仅需少量 token 和一次 API 调用即可完成检索，显著降低了模型成本并实现快速适应新数据。[S5][S14] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 116 | 600 | 10000 | 738.96 | stop |
| 2 | answer | medium | 5394 | 5169 | 694 | 3000 | 10000 | 2445.96 | stop |
| 3 | judge | low | 827 | 602 | 208 | 1000 | 10000 | 1025.57 | stop |
| 4 | judge | low | 822 | 597 | 92 | 1000 | 10000 | 675.76 | stop |
| 5 | judge | low | 824 | 599 | 129 | 1000 | 10000 | 800.16 | stop |
| 6 | judge | low | 830 | 605 | 232 | 1000 | 10000 | 1030.79 | stop |
| 7 | judge | low | 833 | 608 | 220 | 1000 | 10000 | 985.70 | stop |
| 8 | judge | low | 830 | 605 | 117 | 1000 | 10000 | 775.29 | stop |
| 9 | judge | low | 823 | 598 | 109 | 1000 | 10000 | 812.42 | stop |
| 10 | judge | low | 824 | 599 | 331 | 1000 | 10000 | 1173.83 | stop |
| 11 | judge | low | 833 | 608 | 560 | 1000 | 10000 | 1382.35 | stop |

### Finalized answer

<pre>LightRAG 通过将图结构嵌入文本索引并采用低层‑高层双层检索范式，克服了传统 RAG 系统的平面表示和上下文感知不足的问题。[S2][S3]  

在农业、计算机、法律和混合四个领域的实验中，LightRAG 在全面性、 多样性、赋能和整体四个维度上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型数据集上表现出显著优势。[S11][S12]  

该框架的图‑基索引支持增量更新，仅需少量 token 和一次 API 调用即可完成检索，显著降低了模型成本并实现快速适应新数据。[S5][S14]</pre>


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

Judge latency_ms: 670.52

Total evaluation latency_ms: 670.52

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 116 | 1000 | 10000 | 670.52 | stop |

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

Judge latency_ms: 723.49

Total evaluation latency_ms: 723.49

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 111 | 1000 | 10000 | 723.49 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
