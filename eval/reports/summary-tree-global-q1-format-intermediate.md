# Golden Facts evaluation

Created: 2026-10-12T20:42:34.509580+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: summary-tree-global-format-coverage

Revision: f38ebb3fc80c1bf77eb6fd242f8918769a2a3759

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
| Q1 | experiments | judge | 1/1 (100.0%) |
| Q1 | not_all_best | forbidden | 1/1 (100.0%) |
| Q1 | conclusion | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 645 | 420 | 109 | 1200 | 10000 | 1064.58 | stop |
| 2 | section_summary | low | 906 | 681 | 149 | 1200 | 10000 | 1228.35 | stop |
| 3 | section_summary | low | 481 | 256 | 164 | 1200 | 10000 | 1493.34 | stop |
| 4 | section_summary | low | 1435 | 1210 | 223 | 1200 | 10000 | 1503.10 | stop |
| 5 | section_summary | low | 944 | 719 | 165 | 1200 | 10000 | 1143.67 | stop |
| 6 | section_summary | low | 563 | 338 | 107 | 1200 | 10000 | 989.99 | stop |
| 7 | section_summary | low | 639 | 414 | 120 | 1200 | 10000 | 995.43 | stop |
| 8 | section_summary | low | 517 | 292 | 125 | 1200 | 10000 | 1072.24 | stop |
| 9 | section_summary | low | 1354 | 1129 | 268 | 1200 | 10000 | 2494.29 | stop |
| 10 | section_summary | low | 1504 | 1279 | 268 | 1200 | 10000 | 1605.73 | stop |
| 11 | section_summary | low | 1653 | 1428 | 394 | 1200 | 10000 | 2230.92 | stop |
| 12 | section_summary | low | 1451 | 1226 | 250 | 1200 | 10000 | 1601.06 | stop |
| 13 | section_summary | low | 1018 | 793 | 158 | 1200 | 10000 | 1115.52 | stop |
| 14 | section_summary | low | 1610 | 1385 | 358 | 1200 | 10000 | 2040.10 | stop |
| 15 | section_summary | low | 696 | 471 | 138 | 1200 | 10000 | 1096.03 | stop |
| 16 | section_summary | low | 546 | 321 | 122 | 1200 | 10000 | 1129.16 | stop |
| 17 | section_summary | low | 498 | 273 | 76 | 1200 | 10000 | 821.64 | stop |
| 18 | section_summary | low | 661 | 436 | 185 | 1200 | 10000 | 1335.86 | stop |
| 19 | section_summary | low | 558 | 333 | 73 | 1200 | 10000 | 711.46 | stop |
| 20 | section_summary | low | 539 | 314 | 119 | 1200 | 10000 | 1042.04 | stop |
| 21 | section_summary | low | 529 | 304 | 96 | 1200 | 10000 | 893.19 | stop |
| 22 | section_summary | low | 515 | 290 | 110 | 1200 | 10000 | 1070.27 | stop |
| 23 | section_summary | low | 504 | 279 | 81 | 1200 | 10000 | 1339.76 | stop |
| 24 | section_summary | low | 595 | 370 | 112 | 1200 | 10000 | 911.71 | stop |
| 25 | section_summary | low | 1182 | 957 | 200 | 1200 | 10000 | 1293.24 | stop |
| 26 | document_summary | low | 4654 | 4429 | 1052 | 2500 | 10000 | 4378.89 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the summary of this document?

Sub-queries: []

Ask latency_ms: 4828.63

Judge latency_ms: 6871.64

Total evaluation latency_ms: 11711.89

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is motivated by the need for a simpler, faster Retrieval‑Augmented Generation (RAG) system that overcomes the flat‑representation limits and fragmented answers of existing approaches |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | It builds a knowledge graph from chunked documents by extracting entities and relations with LLM prompts |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | employs a dual‑level retrieval paradigm that generates low‑level (entity/edge) and high‑level (topic) query keys |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | incremental updates are handled by unioning newly‑generated sub‑graphs with the existing graph, avoiding full re‑indexing |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Experiments on four UltraDomain corpora (Agriculture, Computer Science, Legal, Mix) containing 0.6–5 M tokens each compare LightRAG against NaiveRAG, RQ‑RAG, HyDE and GraphRAG using a GPT‑4o‑mini multi‑dimensional ranking; LightRAG achieves consistently higher win‑rates (≈60‑70 % overall) and superior scores on comprehensiveness, diversity and empowerment |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | The authors conclude that the graph‑based index and dual‑level retrieval markedly improve retrieval efficiency, answer quality and adaptability while reducing LLM inference costs, demonstrating LightRAG’s effectiveness, efficiency and scalability for dynamic knowledge‑rich domains [S17][S14]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 114 | 600 | 10000 | 903.87 | stop |
| 2 | answer | medium | 4918 | 4693 | 802 | 3000 | 10000 | 3907.07 | stop |
| 3 | judge | low | 980 | 755 | 201 | 1000 | 10000 | 1068.65 | stop |
| 4 | judge | low | 975 | 750 | 112 | 1000 | 10000 | 852.97 | stop |
| 5 | judge | low | 977 | 752 | 150 | 1000 | 10000 | 960.71 | stop |
| 6 | judge | low | 983 | 758 | 123 | 1000 | 10000 | 812.95 | stop |
| 7 | judge | low | 986 | 761 | 272 | 1000 | 10000 | 1218.37 | stop |
| 8 | judge | low | 983 | 758 | 140 | 1000 | 10000 | 983.34 | stop |
| 9 | judge | low | 976 | 751 | 168 | 1000 | 10000 | 974.64 | stop |

### Finalized answer

<pre>LightRAG is motivated by the need for a simpler, faster Retrieval‑Augmented Generation (RAG) system that overcomes the flat‑representation limits and fragmented answers of existing approaches, proposing to embed graph structures into text indexing to capture inter‑entity dependencies and richer context [S1][S3][S4].  It builds a knowledge graph from chunked documents by extracting entities and relations with LLM prompts, then employs a dual‑level retrieval paradigm that generates low‑level (entity/edge) and high‑level (topic) query keys and augments results with one‑hop neighbors, while incremental updates are handled by unioning newly‑generated sub‑graphs with the existing graph, avoiding full re‑indexing [S5][S6].  Experiments on four UltraDomain corpora (Agriculture, Computer Science, Legal, Mix) containing 0.6–5 M tokens each compare LightRAG against NaiveRAG, RQ‑RAG, HyDE and GraphRAG using a GPT‑4o‑mini multi‑dimensional ranking; LightRAG achieves consistently higher win‑rates (≈60‑70 % overall) and superior scores on comprehensiveness, diversity and empowerment, with ablations confirming the importance of both retrieval levels and the graph index, and cost analysis showing far fewer tokens and API calls than GraphRAG [S10][S11][S12][S14].  The authors conclude that the graph‑based index and dual‑level retrieval markedly improve retrieval efficiency, answer quality and adaptability while reducing LLM inference costs, demonstrating LightRAG’s effectiveness, efficiency and scalability for dynamic knowledge‑rich domains [S17][S14].</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 5217.81

Judge latency_ms: 10962.13

Total evaluation latency_ms: 16196.25

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | 為了解決現有 RAG 系統依賴平面表示、缺乏上下文感知且效率低下的問題，作者提出 LightRAG，透過將實體與關係抽取後構建知識圖譜的方式進行圖形化文本索引，以提升檢索的全面性與效率 |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | 作者提出 LightRAG，透過將實體與關係抽取後構建知識圖譜的方式進行圖形化文本索引 |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG 採用雙層檢索機制：低層檢索聚焦具體實體與關係，高層檢索捕捉抽象主題， |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 新增文件只需經過相同的抽取與合併步驟即可增量更新圖譜，避免重建索引 |
| experiments | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | 為了解決現有 RAG 系統依賴平面表示、缺乏上下文感知且效率低下的問題，作者提出 LightRAG，透過將實體與關係抽取後構建知識圖譜的方式進行圖形化文本索引，以提升檢索的全面性與效率[S3][S5]。  <br>LightRAG 採用雙層檢索機制：低層檢索聚焦具體實體與關係，高層檢索捕捉抽象主題，並在查詢時同時擴展一跳鄰近節點；同時，新增文件只需經過相同的抽取與合併步驟即可增量更新圖譜，避免重建索引[S6][S5]。  <br>在四個 UltraDomain 資料集上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 等四個基線比較，LightRAG 在全面性、多樣性、賦能等指標上平均贏率達 60% 以上，且在檢索代幣使用與增量更新成本上遠低於 GraphRAG，最終結論是其顯著提升了檢索速度、生成品質與成本效益[S10][S11][S14][S17]。 |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | 為了解決現有 RAG 系統依賴平面表示、缺乏上下文感知且效率低下的問題，作者提出 LightRAG，透過將實體與關係抽取後構建知識圖譜的方式進行圖形化文本索引，以提升檢索的全面性與效率[S3][S5]。  <br>LightRAG 採用雙層檢索機制：低層檢索聚焦具體實體與關係，高層檢索捕捉抽象主題，並在查詢時同時擴展一跳鄰近節點；同時，新增文件只需經過相同的抽取與合併步驟即可增量更新圖譜，避免重建索引[S6][S5]。  <br>在四個 UltraDomain 資料集上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 等四個基線比較，LightRAG 在全面性、多樣性、賦能等指標上平均贏率達 60% 以上，且在檢索代幣使用與增量更新成本上遠低於 GraphRAG，最終結論是其顯著提升了檢索速度、生成品質與成本效益[S10][S11][S14][S17]。 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 89 | 600 | 10000 | 815.89 | stop |
| 2 | answer | medium | 4960 | 4735 | 958 | 3000 | 10000 | 4389.78 | stop |
| 3 | judge | low | 942 | 717 | 207 | 1000 | 10000 | 1116.22 | stop |
| 4 | judge | low | 937 | 712 | 153 | 1000 | 10000 | 959.87 | stop |
| 5 | judge | low | 939 | 714 | 168 | 1000 | 10000 | 983.52 | stop |
| 6 | judge | low | 945 | 720 | 143 | 1000 | 10000 | 894.95 | stop |
| 7 | judge | low | 948 | 723 | 119 | 1000 | 10000 | 892.98 | stop |
| 8 | judge | low | 945 | 720 | 91 | 1000 | 10000 | 806.52 | stop |
| 9 | judge | low | 938 | 713 | 101 | 1000 | 10000 | 862.46 | stop |
| 10 | judge | low | 939 | 714 | 437 | 1000 | 10000 | 2255.71 | stop |
| 11 | judge | low | 948 | 723 | 497 | 1000 | 10000 | 2189.88 | stop |

### Finalized answer

<pre>為了解決現有 RAG 系統依賴平面表示、缺乏上下文感知且效率低下的問題，作者提出 LightRAG，透過將實體與關係抽取後構建知識圖譜的方式進行圖形化文本索引，以提升檢索的全面性與效率[S3][S5]。  
LightRAG 採用雙層檢索機制：低層檢索聚焦具體實體與關係，高層檢索捕捉抽象主題，並在查詢時同時擴展一跳鄰近節點；同時，新增文件只需經過相同的抽取與合併步驟即可增量更新圖譜，避免重建索引[S6][S5]。  
在四個 UltraDomain 資料集上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 等四個基線比較，LightRAG 在全面性、多樣性、賦能等指標上平均贏率達 60% 以上，且在檢索代幣使用與增量更新成本上遠低於 GraphRAG，最終結論是其顯著提升了檢索速度、生成品質與成本效益[S10][S11][S14][S17]。</pre>


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

Judge latency_ms: 712.52

Total evaluation latency_ms: 712.52

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 83 | 1000 | 10000 | 712.52 | stop |

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

Judge latency_ms: 851.24

Total evaluation latency_ms: 851.24

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 106 | 1000 | 10000 | 851.24 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
