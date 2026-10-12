# Golden Facts evaluation

Created: 2026-10-12T20:50:37.010723+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: summary-tree-global-final

Revision: 8ec7093f619554fd98428e407c2d70a0e146baf9

Uncommitted changes: no

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
| Q1 | dual_level | judge | 0/1 (0.0%) |
| Q1 | incremental_update | judge | 1/1 (100.0%) |
| Q1 | experiments | judge | 1/1 (100.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 481 | 256 | 145 | 1200 | 10000 | 1715.63 | stop |
| 2 | section_summary | low | 645 | 420 | 132 | 1200 | 10000 | 1711.33 | stop |
| 3 | section_summary | low | 906 | 681 | 149 | 1200 | 10000 | 1778.31 | stop |
| 4 | section_summary | low | 1435 | 1210 | 218 | 1200 | 10000 | 2208.09 | stop |
| 5 | section_summary | low | 563 | 338 | 107 | 1200 | 10000 | 984.83 | stop |
| 6 | section_summary | low | 944 | 719 | 136 | 1200 | 10000 | 1588.91 | stop |
| 7 | section_summary | low | 639 | 414 | 120 | 1200 | 10000 | 1534.81 | stop |
| 8 | section_summary | low | 517 | 292 | 116 | 1200 | 10000 | 982.28 | stop |
| 9 | section_summary | low | 1354 | 1129 | 340 | 1200 | 10000 | 2373.01 | stop |
| 10 | section_summary | low | 1504 | 1279 | 246 | 1200 | 10000 | 2187.19 | stop |
| 11 | section_summary | low | 1610 | 1385 | 299 | 1200 | 10000 | 2902.08 | stop |
| 12 | section_summary | low | 1653 | 1428 | 318 | 1200 | 10000 | 2942.06 | stop |
| 13 | section_summary | low | 1451 | 1226 | 295 | 1200 | 10000 | 2690.88 | stop |
| 14 | section_summary | low | 1018 | 793 | 170 | 1200 | 10000 | 1302.61 | stop |
| 15 | section_summary | low | 546 | 321 | 117 | 1200 | 10000 | 1012.38 | stop |
| 16 | section_summary | low | 661 | 436 | 187 | 1200 | 10000 | 1356.26 | stop |
| 17 | section_summary | low | 498 | 273 | 77 | 1200 | 10000 | 1422.92 | stop |
| 18 | section_summary | low | 696 | 471 | 130 | 1200 | 10000 | 1797.98 | stop |
| 19 | section_summary | low | 539 | 314 | 115 | 1200 | 10000 | 1094.29 | stop |
| 20 | section_summary | low | 558 | 333 | 96 | 1200 | 10000 | 1521.50 | stop |
| 21 | section_summary | low | 515 | 290 | 110 | 1200 | 10000 | 1662.93 | stop |
| 22 | section_summary | low | 529 | 304 | 96 | 1200 | 10000 | 1635.30 | stop |
| 23 | section_summary | low | 504 | 279 | 102 | 1200 | 10000 | 1685.43 | stop |
| 24 | section_summary | low | 595 | 370 | 120 | 1200 | 10000 | 1153.83 | stop |
| 25 | section_summary | low | 1182 | 957 | 217 | 1200 | 10000 | 2344.63 | stop |
| 26 | document_summary | low | 4661 | 4436 | 1235 | 2500 | 10000 | 5756.14 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the summary of this document?

Sub-queries: []

Ask latency_ms: 6694.75

Judge latency_ms: 8622.26

Total evaluation latency_ms: 15333.53

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is motivated by the flat data representations, poor contextual awareness and slow adaptation of existing retrieval‑augmented generation (RAG) systems |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | LightRAG is motivated by the flat data representations, poor contextual awareness and slow adaptation of existing retrieval‑augmented generation (RAG) systems, and addresses these limits by embedding graph structures into the text indexing process, where documents are chunked, entities and relations are extracted via LLM prompts, deduplicated, and stored as a knowledge graph that enables multi‑hop subgraph queries |
| dual_level | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The framework then employs a dual‑level retrieval paradigm that generates both low‑level specific entity/relationship keys and high‑level abstract topic keys, matches them in a vector store, and augments results with neighboring graph nodes... |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | while an incremental update algorithm processes new documents through the same extraction pipeline and unions the resulting nodes and edges with the existing graph, avoiding full re‑indexing |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Evaluated on four UltraDomain corpora (Agriculture, Computer Science, Legal, Mix) against NaiveRAG, RQ‑RAG, HyDE and GraphRAG, LightRAG achieved 60‑70 % win rates across comprehensiveness, diversity, empowerment and overall metrics—substantially higher than baselines (e.g., 61‑85 % vs 30‑40 % for NaiveRAG) |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 114 | 600 | 10000 | 1407.06 | stop |
| 2 | answer | medium | 5003 | 4778 | 1361 | 3000 | 10000 | 5270.20 | stop |
| 3 | judge | low | 993 | 768 | 157 | 1000 | 10000 | 1542.30 | stop |
| 4 | judge | low | 988 | 763 | 180 | 1000 | 10000 | 1569.38 | stop |
| 5 | judge | low | 990 | 765 | 152 | 1000 | 10000 | 906.04 | stop |
| 6 | judge | low | 996 | 771 | 132 | 1000 | 10000 | 1378.06 | stop |
| 7 | judge | low | 999 | 774 | 232 | 1000 | 10000 | 1061.90 | stop |
| 8 | judge | low | 996 | 771 | 101 | 1000 | 10000 | 776.24 | stop |
| 9 | judge | low | 989 | 764 | 95 | 1000 | 10000 | 1388.34 | stop |

### Finalized answer

<pre>LightRAG is motivated by the flat data representations, poor contextual awareness and slow adaptation of existing retrieval‑augmented generation (RAG) systems, and addresses these limits by embedding graph structures into the text indexing process, where documents are chunked, entities and relations are extracted via LLM prompts, deduplicated, and stored as a knowledge graph that enables multi‑hop subgraph queries and outperforms traditional embedding‑matching and chunk‑traversal methods [S3][S4][S5].  
The framework then employs a dual‑level retrieval paradigm that generates both low‑level specific entity/relationship keys and high‑level abstract topic keys, matches them in a vector store, and augments results with neighboring graph nodes, while an incremental update algorithm processes new documents through the same extraction pipeline and unions the resulting nodes and edges with the existing graph, avoiding full re‑indexing and reducing computational overhead [S6][S5][S8].  
Evaluated on four UltraDomain corpora (Agriculture, Computer Science, Legal, Mix) against NaiveRAG, RQ‑RAG, HyDE and GraphRAG, LightRAG achieved 60‑70 % win rates across comprehensiveness, diversity, empowerment and overall metrics—substantially higher than baselines (e.g., 61‑85 % vs 30‑40 % for NaiveRAG)—and demonstrated lower retrieval cost (&lt;100 tokens, single API call) and far cheaper incremental updates compared with GraphRAG’s token‑intensive community reconstruction, leading the authors to conclude that LightRAG markedly improves both efficiency and effectiveness while supporting rapid adaptation to new data [S10][S11][S12][S14][S17].</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 5924.47

Judge latency_ms: 11395.04

Total evaluation latency_ms: 17329.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有檢索增強生成系統的平面資料表示、上下文感知不足與更新緩慢等問題，提出將圖結構嵌入文本索引的方式，以圖‑基礎的索引保留實體與關係的結構資訊。 |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | 提出將圖結構嵌入文本索引的方式，以圖‑基礎的索引保留實體與關係的結構資訊。 |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | 系統採用雙層檢索機制，低層檢索精確實體與關係，高層檢索抽象主題， |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 透過增量更新演算法在加入新文件時僅合併圖節點與邊，避免完整重建索引。 |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 比較，LightRAG 在全面性、多樣性、賦能與整體指標上取得約 60‑70% 的勝率，顯示檢索準確度與效率均顯著提升，且因圖‑向與向量檢索合併而降低 LLM 推理成本，作者認為其在效能與適應性上均優於現有方法。 |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有檢索增強生成系統的平面資料表示、上下文感知不足與更新緩慢等問題，提出將圖結構嵌入文本索引的方式，以圖‑基礎的索引保留實體與關係的結構資訊。[S3][S5]  <br>系統採用雙層檢索機制，低層檢索精確實體與關係，高層檢索抽象主題，同時透過增量更新演算法在加入新文件時僅合併圖節點與邊，避免完整重建索引。[S6][S5]  <br>在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 比較，LightRAG 在全面性、多樣性、賦能與整體指標上取得約 60‑70% 的勝率，顯示檢索準確度與效率均顯著提升，且因圖‑向與向量檢索合併而降低 LLM 推理成本，作者認為其在效能與適應性上均優於現有方法。[S10][S11][S14][S17] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有檢索增強生成系統的平面資料表示、上下文感知不足與更新緩慢等問題，提出將圖結構嵌入文本索引的方式，以圖‑基礎的索引保留實體與關係的結構資訊。[S3][S5]  <br>系統採用雙層檢索機制，低層檢索精確實體與關係，高層檢索抽象主題，同時透過增量更新演算法在加入新文件時僅合併圖節點與邊，避免完整重建索引。[S6][S5]  <br>在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 比較，LightRAG 在全面性、多樣性、賦能與整體指標上取得約 60‑70% 的勝率，顯示檢索準確度與效率均顯著提升，且因圖‑向與向量檢索合併而降低 LLM 推理成本，作者認為其在效能與適應性上均優於現有方法。[S10][S11][S14][S17] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 89 | 600 | 10000 | 773.27 | stop |
| 2 | answer | medium | 5045 | 4820 | 1085 | 3000 | 10000 | 5144.22 | stop |
| 3 | judge | low | 936 | 711 | 204 | 1000 | 10000 | 986.33 | stop |
| 4 | judge | low | 931 | 706 | 149 | 1000 | 10000 | 1635.39 | stop |
| 5 | judge | low | 933 | 708 | 152 | 1000 | 10000 | 989.87 | stop |
| 6 | judge | low | 939 | 714 | 133 | 1000 | 10000 | 828.32 | stop |
| 7 | judge | low | 942 | 717 | 302 | 1000 | 10000 | 1493.67 | stop |
| 8 | judge | low | 939 | 714 | 104 | 1000 | 10000 | 739.97 | stop |
| 9 | judge | low | 932 | 707 | 150 | 1000 | 10000 | 1083.33 | stop |
| 10 | judge | low | 933 | 708 | 447 | 1000 | 10000 | 1700.05 | stop |
| 11 | judge | low | 942 | 717 | 491 | 1000 | 10000 | 1938.10 | stop |

### Finalized answer

<pre>LightRAG 針對現有檢索增強生成系統的平面資料表示、上下文感知不足與更新緩慢等問題，提出將圖結構嵌入文本索引的方式，以圖‑基礎的索引保留實體與關係的結構資訊。[S3][S5]  
系統採用雙層檢索機制，低層檢索精確實體與關係，高層檢索抽象主題，同時透過增量更新演算法在加入新文件時僅合併圖節點與邊，避免完整重建索引。[S6][S5]  
在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 比較，LightRAG 在全面性、多樣性、賦能與整體指標上取得約 60‑70% 的勝率，顯示檢索準確度與效率均顯著提升，且因圖‑向與向量檢索合併而降低 LLM 推理成本，作者認為其在效能與適應性上均優於現有方法。[S10][S11][S14][S17]</pre>


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

Judge latency_ms: 763.89

Total evaluation latency_ms: 763.89

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 763.89 | stop |

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

Judge latency_ms: 757.02

Total evaluation latency_ms: 757.02

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 106 | 1000 | 10000 | 757.02 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
