# Golden Facts evaluation

Created: 2026-10-12T20:44:08.289166+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: summary-tree-global-complete-coverage

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
| Q1 | motivation | judge | 0/1 (0.0%) |
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
| Q1_ZH_THREE_SENTENCES | experiments | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/1 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 1/1 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 906 | 681 | 161 | 1200 | 10000 | 1305.44 | stop |
| 2 | section_summary | low | 1435 | 1210 | 189 | 1200 | 10000 | 1613.44 | stop |
| 3 | section_summary | low | 645 | 420 | 106 | 1200 | 10000 | 1883.50 | stop |
| 4 | section_summary | low | 481 | 256 | 145 | 1200 | 10000 | 2387.37 | stop |
| 5 | section_summary | low | 944 | 719 | 157 | 1200 | 10000 | 1618.94 | stop |
| 6 | section_summary | low | 563 | 338 | 116 | 1200 | 10000 | 1523.09 | stop |
| 7 | section_summary | low | 1354 | 1129 | 245 | 1200 | 10000 | 2251.40 | stop |
| 8 | section_summary | low | 639 | 414 | 128 | 1200 | 10000 | 1226.49 | stop |
| 9 | section_summary | low | 517 | 292 | 116 | 1200 | 10000 | 1005.50 | stop |
| 10 | section_summary | low | 1504 | 1279 | 290 | 1200 | 10000 | 1845.00 | stop |
| 11 | section_summary | low | 1451 | 1226 | 283 | 1200 | 10000 | 2024.53 | stop |
| 12 | section_summary | low | 1610 | 1385 | 306 | 1200 | 10000 | 2938.39 | stop |
| 13 | section_summary | low | 1653 | 1428 | 367 | 1200 | 10000 | 3045.10 | stop |
| 14 | section_summary | low | 1018 | 793 | 162 | 1200 | 10000 | 1532.51 | stop |
| 15 | section_summary | low | 696 | 471 | 124 | 1200 | 10000 | 1076.26 | stop |
| 16 | section_summary | low | 498 | 273 | 78 | 1200 | 10000 | 961.76 | stop |
| 17 | section_summary | low | 546 | 321 | 122 | 1200 | 10000 | 1221.21 | stop |
| 18 | section_summary | low | 661 | 436 | 204 | 1200 | 10000 | 1535.44 | stop |
| 19 | section_summary | low | 558 | 333 | 77 | 1200 | 10000 | 744.34 | stop |
| 20 | section_summary | low | 539 | 314 | 119 | 1200 | 10000 | 1025.50 | stop |
| 21 | section_summary | low | 515 | 290 | 107 | 1200 | 10000 | 999.12 | stop |
| 22 | section_summary | low | 504 | 279 | 76 | 1200 | 10000 | 852.44 | stop |
| 23 | section_summary | low | 529 | 304 | 97 | 1200 | 10000 | 958.96 | stop |
| 24 | section_summary | low | 595 | 370 | 112 | 1200 | 10000 | 1003.83 | stop |
| 25 | section_summary | low | 1182 | 957 | 190 | 1200 | 10000 | 1344.77 | stop |
| 26 | document_summary | low | 4571 | 4346 | 1138 | 2500 | 10000 | 5116.30 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the summary of this document?

Sub-queries: []

Ask latency_ms: 4963.69

Judge latency_ms: 9124.09

Total evaluation latency_ms: 14122.86

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | LightRAG tackles the key limits of existing Retrieval‑Augmented Generation systems—flat data representations and weak contextual awareness—by embedding graph structures into the indexing process... |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | by embedding graph structures into the indexing process, segmenting documents, extracting entities and relationships, and constructing a knowledge graph |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | It introduces a dual‑level retrieval paradigm that generates low‑level entity/edge keywords and high‑level abstract keywords, combining graph matches with vector search to capture both precise facts and broader topics |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | while an incremental update algorithm unions new document graphs with the existing index, avoiding full re‑indexing and reducing computational overhead |
| experiments | judge | PASS | Required claim supported by verbatim evidence | In experiments on four UltraDomain corpora (Agriculture, Computer Science, Legal, Mix) against NaiveRAG, RQ‑RAG, HyDE and GraphRAG, LightRAG attained 60‑70 % win rates across comprehensiveness, diversity, empowerment and overall metrics—improving baseline scores by 5‑30 % points |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | leading the authors to conclude that the graph‑based index and dual‑level retrieval substantially boost retrieval efficiency, answer quality, and adaptability to dynamic data |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 114 | 600 | 10000 | 902.49 | stop |
| 2 | answer | medium | 4887 | 4662 | 910 | 3000 | 10000 | 4053.15 | stop |
| 3 | judge | low | 917 | 692 | 188 | 1000 | 10000 | 1180.06 | stop |
| 4 | judge | low | 912 | 687 | 120 | 1000 | 10000 | 813.12 | stop |
| 5 | judge | low | 914 | 689 | 155 | 1000 | 10000 | 969.60 | stop |
| 6 | judge | low | 920 | 695 | 126 | 1000 | 10000 | 924.33 | stop |
| 7 | judge | low | 923 | 698 | 218 | 1000 | 10000 | 1555.93 | stop |
| 8 | judge | low | 920 | 695 | 111 | 1000 | 10000 | 896.76 | stop |
| 9 | judge | low | 913 | 688 | 236 | 1000 | 10000 | 2784.30 | stop |

### Finalized answer

<pre>LightRAG tackles the key limits of existing Retrieval‑Augmented Generation systems—flat data representations and weak contextual awareness—by embedding graph structures into the indexing process, segmenting documents, extracting entities and relationships, and constructing a knowledge graph that enables richer, multi‑hop queries than pure vector matching [S3][S5]. It introduces a dual‑level retrieval paradigm that generates low‑level entity/edge keywords and high‑level abstract keywords, combining graph matches with vector search to capture both precise facts and broader topics, while an incremental update algorithm unions new document graphs with the existing index, avoiding full re‑indexing and reducing computational overhead [S6][S5][S8]. In experiments on four UltraDomain corpora (Agriculture, Computer Science, Legal, Mix) against NaiveRAG, RQ‑RAG, HyDE and GraphRAG, LightRAG attained 60‑70 % win rates across comprehensiveness, diversity, empowerment and overall metrics—improving baseline scores by 5‑30 % points—and used under 100 tokens and a single API call versus 610 k tokens and hundreds of calls for GraphRAG, leading the authors to conclude that the graph‑based index and dual‑level retrieval substantially boost retrieval efficiency, answer quality, and adaptability to dynamic data [S10][S11][S14][S17].</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 5182.83

Judge latency_ms: 11657.20

Total evaluation latency_ms: 16850.36

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有 RAG 系統的平面資料表示與缺乏上下文感知的問題，提出將文本以實體與關係抽取後構建知識圖，利用圖‑向量結合的方式進行索引，以提升檢索效率與全局理解 |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有 RAG 系統的平面資料表示與缺乏上下文感知的問題，提出將文本以實體與關係抽取後構建知識圖，利用圖‑向量結合的方式進行索引，以提升檢索效率與全局理解 |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | 系統採用雙層檢索架構，分別產生低層次的實體/關係關鍵字與高層次的概念關鍵字，結合圖結構與向量搜索 |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 系統採用雙層檢索架構，分別產生低層次的實體/關係關鍵字與高層次的概念關鍵字，結合圖結構與向量搜索，同時透過增量更新演算法在加入新文件時僅合併圖節點而避免完整重建索引 [S6][S5] |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 四個基線比較，LightRAG 在綜合性、多樣性、賦能與整體指標上平均贏率達 60‑70% |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有 RAG 系統的平面資料表示與缺乏上下文感知的問題，提出將文本以實體與關係抽取後構建知識圖，利用圖‑向量結合的方式進行索引，以提升檢索效率與全局理解 [S3][S5]。  <br>系統採用雙層檢索架構，分別產生低層次的實體/關係關鍵字與高層次的概念關鍵字，結合圖結構與向量搜索，同時透過增量更新演算法在加入新文件時僅合併圖節點而避免完整重建索引 [S6][S5]。  <br>在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 四個基線比較，LightRAG 在綜合性、多樣性、賦能與整體指標上平均贏率達 60‑70% 並在大型法律語料上仍保持優勢，且因增量更新僅使用少量 token 與單次 API 呼叫顯示出更高的效率與適應性，作者因此認為 LightRAG 在速度、品質與成本上均顯著優於現有方法 [S10][S11][S12][S14][S17]。 |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 針對現有 RAG 系統的平面資料表示與缺乏上下文感知的問題，提出將文本以實體與關係抽取後構建知識圖，利用圖‑向量結合的方式進行索引，以提升檢索效率與全局理解 [S3][S5]。  <br>系統採用雙層檢索架構，分別產生低層次的實體/關係關鍵字與高層次的概念關鍵字，結合圖結構與向量搜索，同時透過增量更新演算法在加入新文件時僅合併圖節點而避免完整重建索引 [S6][S5]。  <br>在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 四個基線比較，LightRAG 在綜合性、多樣性、賦能與整體指標上平均贏率達 60‑70% 並在大型法律語料上仍保持優勢，且因增量更新僅使用少量 token 與單次 API 呼叫顯示出更高的效率與適應性，作者因此認為 LightRAG 在速度、品質與成本上均顯著優於現有方法 [S10][S11][S12][S14][S17]。 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 88 | 600 | 10000 | 859.13 | stop |
| 2 | answer | medium | 4929 | 4704 | 1040 | 3000 | 10000 | 4304.87 | stop |
| 3 | judge | low | 968 | 743 | 204 | 1000 | 10000 | 1035.15 | stop |
| 4 | judge | low | 963 | 738 | 214 | 1000 | 10000 | 1019.23 | stop |
| 5 | judge | low | 965 | 740 | 201 | 1000 | 10000 | 1172.07 | stop |
| 6 | judge | low | 971 | 746 | 198 | 1000 | 10000 | 1120.94 | stop |
| 7 | judge | low | 974 | 749 | 258 | 1000 | 10000 | 1176.86 | stop |
| 8 | judge | low | 971 | 746 | 100 | 1000 | 10000 | 807.84 | stop |
| 9 | judge | low | 964 | 739 | 89 | 1000 | 10000 | 1407.54 | stop |
| 10 | judge | low | 965 | 740 | 535 | 1000 | 10000 | 2032.77 | stop |
| 11 | judge | low | 974 | 749 | 534 | 1000 | 10000 | 1884.80 | stop |

### Finalized answer

<pre>LightRAG 針對現有 RAG 系統的平面資料表示與缺乏上下文感知的問題，提出將文本以實體與關係抽取後構建知識圖，利用圖‑向量結合的方式進行索引，以提升檢索效率與全局理解 [S3][S5]。  
系統採用雙層檢索架構，分別產生低層次的實體/關係關鍵字與高層次的概念關鍵字，結合圖結構與向量搜索，同時透過增量更新演算法在加入新文件時僅合併圖節點而避免完整重建索引 [S6][S5]。  
在四個 UltraDomain 資料集（農業、計算機科學、法律、混合）上與 NaiveRAG、RQ‑RAG、HyDE、GraphRAG 四個基線比較，LightRAG 在綜合性、多樣性、賦能與整體指標上平均贏率達 60‑70% 並在大型法律語料上仍保持優勢，且因增量更新僅使用少量 token 與單次 API 呼叫顯示出更高的效率與適應性，作者因此認為 LightRAG 在速度、品質與成本上均顯著優於現有方法 [S10][S11][S12][S14][S17]。</pre>


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

Judge latency_ms: 765.91

Total evaluation latency_ms: 765.91

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 86 | 1000 | 10000 | 765.91 | stop |

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

Judge latency_ms: 828.96

Total evaluation latency_ms: 828.96

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 106 | 1000 | 10000 | 828.96 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
