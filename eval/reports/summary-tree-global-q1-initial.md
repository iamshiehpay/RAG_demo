# Golden Facts evaluation

Created: 2026-10-12T20:41:03.542339+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: summary-tree-global

Revision: d56e092138f6d5c87c75e042caf4f79e0db6989c

Uncommitted changes: yes

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: chat_document.router_regression.CASES (#06 canonical 12 cases)

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 1/1 (100.0%) |
| Q1 | motivation | judge | 1/1 (100.0%) |
| Q1 | graph_indexing | judge | 1/1 (100.0%) |
| Q1 | dual_level | judge | 1/1 (100.0%) |
| Q1 | incremental_update | judge | 1/1 (100.0%) |
| Q1 | experiments | judge | 0/1 (0.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 481 | 256 | 159 | 1200 | 10000 | 1173.82 | stop |
| 2 | section_summary | low | 906 | 681 | 162 | 1200 | 10000 | 1158.96 | stop |
| 3 | section_summary | low | 645 | 420 | 111 | 1200 | 10000 | 1530.74 | stop |
| 4 | section_summary | low | 1435 | 1210 | 236 | 1200 | 10000 | 1626.56 | stop |
| 5 | section_summary | low | 944 | 719 | 153 | 1200 | 10000 | 1026.29 | stop |
| 6 | section_summary | low | 1354 | 1129 | 217 | 1200 | 10000 | 1443.18 | stop |
| 7 | section_summary | low | 563 | 338 | 118 | 1200 | 10000 | 1580.25 | stop |
| 8 | section_summary | low | 517 | 292 | 128 | 1200 | 10000 | 1059.44 | stop |
| 9 | section_summary | low | 639 | 414 | 123 | 1200 | 10000 | 1641.74 | stop |
| 10 | section_summary | low | 1504 | 1279 | 260 | 1200 | 10000 | 1630.70 | stop |
| 11 | section_summary | low | 1653 | 1428 | 379 | 1200 | 10000 | 2077.42 | stop |
| 12 | section_summary | low | 1610 | 1385 | 362 | 1200 | 10000 | 2227.35 | stop |
| 13 | section_summary | low | 1451 | 1226 | 276 | 1200 | 10000 | 2412.91 | stop |
| 14 | section_summary | low | 1018 | 793 | 162 | 1200 | 10000 | 1653.01 | stop |
| 15 | section_summary | low | 696 | 471 | 131 | 1200 | 10000 | 1082.83 | stop |
| 16 | section_summary | low | 661 | 436 | 182 | 1200 | 10000 | 1280.53 | stop |
| 17 | section_summary | low | 498 | 273 | 93 | 1200 | 10000 | 902.24 | stop |
| 18 | section_summary | low | 546 | 321 | 119 | 1200 | 10000 | 1111.22 | stop |
| 19 | section_summary | low | 558 | 333 | 92 | 1200 | 10000 | 809.31 | stop |
| 20 | section_summary | low | 515 | 290 | 107 | 1200 | 10000 | 931.61 | stop |
| 21 | section_summary | low | 529 | 304 | 95 | 1200 | 10000 | 1499.32 | stop |
| 22 | section_summary | low | 539 | 314 | 115 | 1200 | 10000 | 1563.06 | stop |
| 23 | section_summary | low | 504 | 279 | 90 | 1200 | 10000 | 1427.18 | stop |
| 24 | section_summary | low | 1182 | 957 | 204 | 1200 | 10000 | 1325.14 | stop |
| 25 | section_summary | low | 595 | 370 | 113 | 1200 | 10000 | 927.15 | stop |
| 26 | document_summary | low | 4659 | 4434 | 1195 | 2500 | 10000 | 5664.13 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summary this document.

Sub-queries: []

Ask latency_ms: 5231.36

Judge latency_ms: 8857.79

Total evaluation latency_ms: 14102.22

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is introduced to overcome the limitations of existing retrieval‑augmented generation (RAG) systems that rely on flat text representations and therefore miss complex entity relationships and struggle with inter‑dependent information synthesis [S3][S2]. |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | Documents are chunked, LLM prompts extract entities, relationships and key‑value pairs, and a deduplication step builds a compact graph [S5]; incremental updates are performed by processing new documents through the same pipeline and union‑ing the resulting nodes and edges with the existing graph, avoiding a full rebuild [S5][S8]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The proposed framework augments RAG with a knowledge‑graph‑based index and a dual‑level retrieval mechanism that handles both precise entity‑relation facts (low‑level) and broader topical concepts (high‑level) [S5][S6]. |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | incremental updates are performed by processing new documents through the same pipeline and union‑ing the resulting nodes and edges with the existing graph, avoiding a full rebuild |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Experiments evaluate LightRAG on four “UltraDomain” corpora (Agriculture, Computer‑Science, Legal, Mixed) ... LightRAG is compared against four baselines—NaiveRAG (vector‑based), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (entity‑relationship graph)… Results show LightRAG winning the majority of LLM‑driven pairwise comparisons… confirming that the hybrid dual‑level design yields balanced gains in comprehensiveness, diversity, empowerment and overall quality |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 83 | 600 | 10000 | 725.15 | stop |
| 2 | answer | medium | 4828 | 4603 | 963 | 3000 | 10000 | 4492.83 | stop |
| 3 | judge | low | 1325 | 1100 | 184 | 1000 | 10000 | 956.36 | stop |
| 4 | judge | low | 1320 | 1095 | 189 | 1000 | 10000 | 1759.86 | stop |
| 5 | judge | low | 1322 | 1097 | 148 | 1000 | 10000 | 1512.49 | stop |
| 6 | judge | low | 1328 | 1103 | 129 | 1000 | 10000 | 855.80 | stop |
| 7 | judge | low | 1331 | 1106 | 272 | 1000 | 10000 | 1314.20 | stop |
| 8 | judge | low | 1328 | 1103 | 106 | 1000 | 10000 | 930.68 | stop |
| 9 | judge | low | 1321 | 1096 | 134 | 1000 | 10000 | 1528.41 | stop |

### Finalized answer

<pre>LightRAG is introduced to overcome the limitations of existing retrieval‑augmented generation (RAG) systems that rely on flat text representations and therefore miss complex entity relationships and struggle with inter‑dependent information synthesis [S3][S2].  The proposed framework augments RAG with a knowledge‑graph‑based index and a dual‑level retrieval mechanism that handles both precise entity‑relation facts (low‑level) and broader topical concepts (high‑level) [S5][S6].  Documents are chunked, LLM prompts extract entities, relationships and key‑value pairs, and a deduplication step builds a compact graph [S5]; incremental updates are performed by processing new documents through the same pipeline and union‑ing the resulting nodes and edges with the existing graph, avoiding a full rebuild [S5][S8].  Retrieval first generates low‑ and high‑level query keywords, matches them in a vector store, and then augments the results with one‑hop neighbours from the graph, enabling multi‑hop subgraph queries while keeping token‑wise LLM calls low [S6][S8].  The retrieved entity and relation values are concatenated and fed to a general‑purpose LLM for answer generation [S7].

Experiments evaluate LightRAG on four “UltraDomain” corpora (Agriculture, Computer‑Science, Legal, Mixed) ranging from 0.6 M to 5 M tokens across 428 college textbooks [S10][S19].  LightRAG is compared against four baselines—NaiveRAG (vector‑based), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (entity‑relationship graph)—using GPT‑4o‑mini for both retrieval and generation, with a consistent nano vector store, 1200‑token chunks and a gleaning parameter of 1 [S10].  Results show LightRAG winning the majority of LLM‑driven pairwise comparisons, achieving overall win rates of roughly 60‑70 % against NaiveRAG, RQ‑RAG and HyDE, and 49‑55 % against GraphRAG, with the strongest advantage on the large Legal corpus [S11].  Ablation studies reveal that removing either the low‑level or high‑level retrieval component degrades performance across all four datasets, confirming that the hybrid dual‑level design yields balanced gains in comprehensiveness, diversity, empowerment and overall quality [S12].  A case study on a machine‑learning normalization query demonstrates that LightRAG outperforms GraphRAG on every judged dimension (comprehensiveness, diversity, empowerment, overall) by providing a wider set of metrics, richer explanations and contextual trade‑offs [S13].  Cost analysis on the Legal dataset indicates that LightRAG uses under 100 tokens and a single API call for retrieval, compared with GraphRAG’s 610 k tokens and hundreds of calls, and that incremental updates incur far lower token overhead because no community‑based reconstruction is needed [S14].

The authors conclude that integrating a graph‑based index with dual‑level retrieval markedly improves retrieval efficiency, answer quality and adaptability while reducing LLM inference costs, and that LightRAG’s incremental update mechanism keeps the system current with minimal overhead [S17].</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 4919.91

Judge latency_ms: 12631.13

Total evaluation latency_ms: 17567.69

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG 提出了一種結合知識圖譜與雙層檢索的檢索增強生成框架，以克服傳統 RAG 的平面表示限制，提升對實體關係的捕捉與快速更新能力。 |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 實驗在四個大規模領域資料集上顯示，LightRAG 在全面性、多樣性、賦能與整體表現上普遍優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且在成本與適應性上亦具顯著優勢。 |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 提出了一種結合知識圖譜與雙層檢索的檢索增強生成框架，以克服傳統 RAG 的平面表示限制，提升對實體關係的捕捉與快速更新能力。[S3][S5][S6]  <br>系統透過圖形化文本索引、低層與高層關鍵字生成的雙層檢索，以及增量更新機制，實現了較低的檢索開銷與更快的回應速度。[S5][S6][S8][S14]  <br>實驗在四個大規模領域資料集上顯示，LightRAG 在全面性、多樣性、賦能與整體表現上普遍優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且在成本與適應性上亦具顯著優勢。[S11][S12][S14][S17] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 提出了一種結合知識圖譜與雙層檢索的檢索增強生成框架，以克服傳統 RAG 的平面表示限制，提升對實體關係的捕捉與快速更新能力。[S3][S5][S6]  <br>系統透過圖形化文本索引、低層與高層關鍵字生成的雙層檢索，以及增量更新機制，實現了較低的檢索開銷與更快的回應速度。[S5][S6][S8][S14]  <br>實驗在四個大規模領域資料集上顯示，LightRAG 在全面性、多樣性、賦能與整體表現上普遍優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且在成本與適應性上亦具顯著優勢。[S11][S12][S14][S17] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 92 | 600 | 10000 | 1454.40 | stop |
| 2 | answer | medium | 4874 | 4649 | 580 | 3000 | 10000 | 3457.42 | stop |
| 3 | judge | low | 860 | 635 | 178 | 1000 | 10000 | 1018.68 | stop |
| 4 | judge | low | 855 | 630 | 104 | 1000 | 10000 | 1345.64 | stop |
| 5 | judge | low | 857 | 632 | 217 | 1000 | 10000 | 1338.35 | stop |
| 6 | judge | low | 863 | 638 | 130 | 1000 | 10000 | 862.01 | stop |
| 7 | judge | low | 866 | 641 | 332 | 1000 | 10000 | 1832.68 | stop |
| 8 | judge | low | 863 | 638 | 142 | 1000 | 10000 | 996.96 | stop |
| 9 | judge | low | 856 | 631 | 109 | 1000 | 10000 | 961.52 | stop |
| 10 | judge | low | 857 | 632 | 393 | 1000 | 10000 | 1663.29 | stop |
| 11 | judge | low | 866 | 641 | 610 | 1000 | 10000 | 2612.01 | stop |

### Finalized answer

<pre>LightRAG 提出了一種結合知識圖譜與雙層檢索的檢索增強生成框架，以克服傳統 RAG 的平面表示限制，提升對實體關係的捕捉與快速更新能力。[S3][S5][S6]  
系統透過圖形化文本索引、低層與高層關鍵字生成的雙層檢索，以及增量更新機制，實現了較低的檢索開銷與更快的回應速度。[S5][S6][S8][S14]  
實驗在四個大規模領域資料集上顯示，LightRAG 在全面性、多樣性、賦能與整體表現上普遍優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且在成本與適應性上亦具顯著優勢。[S11][S12][S14][S17]</pre>


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

Judge latency_ms: 777.00

Total evaluation latency_ms: 777.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 777.00 | stop |

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

Judge latency_ms: 759.01

Total evaluation latency_ms: 759.01

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 111 | 1000 | 10000 | 759.01 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
