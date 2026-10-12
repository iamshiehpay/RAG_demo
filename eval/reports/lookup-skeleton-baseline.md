# Golden Facts evaluation

Created: 2026-10-12T15:32:15.955448+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: FAIL

Label: lookup-skeleton

Revision: 7245c1c01b375ac33f5513c1b214da566710ced7

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
| Q1 | experiments | judge | 1/1 (100.0%) |
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
| LIMITATIONS | no_invented_limit | forbidden | 1/1 (100.0%) |
| ABSENT_HOTPOT | question_type | events | 1/1 (100.0%) |
| ABSENT_HOTPOT | fixed_reply | judge | 0/1 (0.0%) |
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

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q1 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Ask latency_ms: 3069.79

Judge latency_ms: 8738.07

Total evaluation latency_ms: 11813.95

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |
| motivation | judge | FAIL | Required claim not asserted |  |
| graph_indexing | judge | FAIL | Required claim not asserted |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | dual‑level retrieval mechanism, which jointly handles precise entity‑level information (low‑level) and broader thematic content (high‑level) |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Experimental evaluation was conducted on four datasets—Agriculture (12 documents, 2,017,886 tokens), CS (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and Mix (61 documents, 619,009 tokens) [C5].<br><br>Compared with a baseline NaiveRAG, LightRAG achieved markedly higher scores across three evaluation dimensions—Comprehensiveness, Diversity, and Empowerment—and consequently higher Overall performance. For example, in the Agriculture domain LightRAG’s Overall score reached 67.6 % versus 32.4 % for NaiveRAG; similar improvements were observed in the other domains (e.g., Legal Overall 84.8 % vs 15.2 %) [C3][C4]. |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 695 | 3000 | 10000 | 2918.64 | stop |
| 2 | judge | low | 1001 | 776 | 80 | 1000 | 10000 | 1323.69 | stop |
| 3 | judge | low | 996 | 771 | 109 | 1000 | 10000 | 1352.04 | stop |
| 4 | judge | low | 998 | 773 | 130 | 1000 | 10000 | 1369.41 | stop |
| 5 | judge | low | 1004 | 779 | 115 | 1000 | 10000 | 1362.65 | stop |
| 6 | judge | low | 1007 | 782 | 280 | 1000 | 10000 | 1109.62 | stop |
| 7 | judge | low | 1004 | 779 | 103 | 1000 | 10000 | 816.24 | stop |
| 8 | judge | low | 997 | 772 | 85 | 1000 | 10000 | 1404.43 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism, which jointly handles precise entity‑level information (low‑level) and broader thematic content (high‑level) to improve contextual awareness and answer coherence [C1][C2].  

The system integrates graph structures with vector representations, enabling fast retrieval of related entities and their relationships while supporting incremental updates that keep the knowledge base current in dynamic environments [C1][C2].  

Experimental evaluation was conducted on four datasets—Agriculture (12 documents, 2,017,886 tokens), CS (10 documents, 2,306,535 tokens), Legal (94 documents, 5,081,069 tokens), and Mix (61 documents, 619,009 tokens) [C5].  

Compared with a baseline NaiveRAG, LightRAG achieved markedly higher scores across three evaluation dimensions—Comprehensiveness, Diversity, and Empowerment—and consequently higher Overall performance. For example, in the Agriculture domain LightRAG’s Overall score reached 67.6 % versus 32.4 % for NaiveRAG; similar improvements were observed in the other domains (e.g., Legal Overall 84.8 % vs 15.2 %) [C3][C4].  

These results demonstrate that the graph‑empowered, dual‑level retrieval approach substantially boosts retrieval accuracy, result diversity, and the richness of generated responses while maintaining efficiency [C3][C4].  

The LightRAG codebase has been released as open‑source software at https://github.com/HKUDS/LightRAG [C1].</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Ask latency_ms: 3270.19

Judge latency_ms: 10010.37

Total evaluation latency_ms: 13306.79

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| retrieval_methods | judge | FAIL | Required claim not asserted |  |
| retrieval_cost | judge | FAIL | Required claim not asserted |  |
| incremental_update | judge | FAIL | Required claim not asserted |  |
| table1_agriculture_overall | judge | FAIL | Required claim not asserted |  |
| table1_cs_overall | judge | FAIL | Required claim not asserted |  |
| table1_legal_overall | judge | FAIL | Required claim not asserted |  |
| table1_mix_overall | judge | FAIL | Required claim not asserted |  |
| table3_case_study | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | LightRAG consistently outperforms GraphRAG across the evaluated dimensions. In the win‑rate tables, LightRAG records higher percentages than GraphRAG for Comprehensiveness, Diversity, Empowerment and Overall on the datasets shown, indicating a clear advantage ... The case‑study table (Table 3) further contrasts the two systems, underscoring LightRAG’s overall stronger results [C5]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 525 | 3000 | 10000 | 2986.57 | stop |
| 2 | judge | low | 871 | 646 | 124 | 1000 | 10000 | 881.46 | stop |
| 3 | judge | low | 908 | 683 | 53 | 1000 | 10000 | 807.05 | stop |
| 4 | judge | low | 868 | 643 | 83 | 1000 | 10000 | 673.42 | stop |
| 5 | judge | low | 884 | 659 | 91 | 1000 | 10000 | 945.06 | stop |
| 6 | judge | low | 884 | 659 | 117 | 1000 | 10000 | 1300.51 | stop |
| 7 | judge | low | 884 | 659 | 120 | 1000 | 10000 | 658.85 | stop |
| 8 | judge | low | 884 | 659 | 92 | 1000 | 10000 | 1416.59 | stop |
| 9 | judge | low | 876 | 651 | 226 | 1000 | 10000 | 1847.12 | stop |
| 10 | judge | low | 869 | 644 | 117 | 1000 | 10000 | 1480.30 | stop |

### Finalized answer

<pre>LightRAG consistently outperforms GraphRAG across the evaluated dimensions. In the win‑rate tables, LightRAG records higher percentages than GraphRAG for Comprehensiveness, Diversity, Empowerment and Overall on the datasets shown, indicating a clear advantage in retrieving more complete and higher‑quality answers [C2]. The authors attribute this superiority to LightRAG’s dual‑level retrieval paradigm, which combines low‑level entity retrieval with high‑level topic retrieval, thereby capturing a broader context and generating more diverse responses, especially in large‑scale corpora such as the Legal dataset [C3]. Moreover, LightRAG’s graph‑based text indexing is highlighted as a key factor that enhances both the breadth (comprehensiveness) and the richness (diversity and empowerment) of the information it retrieves, leading to better performance than GraphRAG on complex, high‑token‑count queries [C4]. The case‑study table (Table 3) further contrasts the two systems, underscoring LightRAG’s overall stronger results [C5].</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 4401.03

Judge latency_ms: 4748.50

Total evaluation latency_ms: 9162.17

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required source Chunk | C3 |
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
| 1 | answer | medium | 1981 | 1756 | 1681 | 3000 | 10000 | 4205.88 | stop |
| 2 | judge | low | 1569 | 1344 | 109 | 1000 | 10000 | 772.55 | stop |
| 3 | judge | low | 1570 | 1345 | 93 | 1000 | 10000 | 768.37 | stop |
| 4 | judge | low | 1581 | 1356 | 233 | 1000 | 10000 | 1065.17 | stop |
| 5 | judge | low | 1581 | 1356 | 148 | 1000 | 10000 | 910.18 | stop |
| 6 | judge | low | 1557 | 1332 | 93 | 1000 | 10000 | 1232.23 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (using NaiveRAG as reference)**  

| Domain / Setting | Metric | NaiveRAG (baseline) | **LightRAG (ablated)** |
|------------------|--------|---------------------|------------------------|
| **Agriculture** | Comprehensiveness | 32.4 % | **67.6 %** |
|                  | Diversity        | 23.6 % | **76.4 %** |
|                  | Empowerment      | 32.4 % | **67.6 %** |
|                  | Overall          | 32.4 % | **67.6 %** |
| **CS**           | Comprehensiveness | 38.4 % | **61.6 %** |
|                  | Diversity        | 38.0 % | **62.0 %** |
|                  | Empowerment      | 38.8 % | **61.2 %** |
|                  | Overall          | 38.8 % | **61.2 %** |
| **Legal**        | Comprehensiveness | 16.4 % | **83.6 %** |
|                  | Diversity        | 13.6 % | **86.4 %** |
|                  | Empowerment      | 16.4 % | **83.6 %** |
|                  | Overall          | 15.2 % | **84.8 %** |
| **Mix**          | Comprehensiveness | 38.8 % | **61.2 %** |
|                  | Diversity        | 32.4 % | **67.6 %** |
|                  | Empowerment      | 42.8 % | **57.2 %** |
|                  | Overall          | 40.0 % | **60.0 %** |

**High‑capacity NaiveRAG vs. LightRAG (ablated)**  

| Domain | Metric | NaiveRAG‑High | **LightRAG (ablated)** |
|--------|--------|---------------|------------------------|
| Agriculture | Comprehensiveness | 34.8 % | **65.2 %** |
|             | Diversity        | 27.2 % | **72.8 %** |
|             | Empowerment      | 36.0 % | **64.0 %** |
|             | Overall          | 35.2 % | **64.8 %** |
| CS          | Comprehensiveness | 42.8 % | **57.2 %** |
|             | Diversity        | 36.8 % | **63.2 %** |
|             | Empowerment      | 42.4 % | **57.6 %** |
|             | Overall          | 44.0 % | **56.0 %** |
| Legal       | Comprehensiveness | 23.6 % | **76.4 %** |
|             | Diversity        | 16.8 % | **83.2 %** |
|             | Empowerment      | 22.8 % | **77.2 %** |
|             | Overall          | 22.0 % | **78.0 %** |
| Mix         | Comprehensiveness | 40.4 % | **59.6 %** |
|             | Diversity        | 36.0 % | **64.0 %** |
|             | Empowerment      | 47.6 % | **52.4 %** |
|             | Overall          | 42.4 % | **57.6 %** |

These figures are taken directly from the ablation study table that compares LightRAG (in its various ablated configurations) against NaiveRAG baselines across four datasets (Agriculture, CS, Legal, Mix) and multiple evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C3].</pre>

## ZH_COST — repetition 1

Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 和 GraphRAG 的檢索成本差異是什麼？

Sub-queries: []

Ask latency_ms: 2945.38

Judge latency_ms: 3295.12

Total evaluation latency_ms: 6246.31

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| chinese_answer | judge | PASS | Required claim supported by verbatim evidence | LightRAG 的檢索成本遠低於 GraphRAG。  <br>在檢索階段，GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索成本極低[C4]。 |
| retrieval_cost | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索成本極低 |
| numbers_unchanged | judge | PASS | Required claim supported by verbatim evidence | GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2625 | 2400 | 411 | 3000 | 10000 | 2744.90 | stop |
| 2 | judge | low | 847 | 622 | 265 | 1000 | 10000 | 998.76 | stop |
| 3 | judge | low | 894 | 669 | 326 | 1000 | 10000 | 1036.32 | stop |
| 4 | judge | low | 879 | 654 | 351 | 1000 | 10000 | 1260.04 | stop |

### Finalized answer

<pre>LightRAG 的檢索成本遠低於 GraphRAG。  
在檢索階段，GraphRAG 必須產生 1,399 個社群，實際使用 610 個二層社群，每個社群報告約 1,000 個 token，總計約 610,000 個 token，且因需逐一遍歷社群而產生數百次 API 呼叫，檢索開銷相當龐大。相較之下，LightRAG 只需使用不到 100 個 token 產生關鍵字並完成檢索，整個過程僅需一次 API 呼叫，檢索成本極低[C4]。  
此外，LightRAG 透過結合圖結構與向量化表示進行資訊檢索，省去大量前置處理的需求，進一步降低了檢索時的資源消耗[C5]。</pre>

## LIMITATIONS — repetition 1

Question: 這篇論文有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: 這篇論文有什麼限制？

Sub-queries: []

Ask latency_ms: 1143.59

Judge latency_ms: 3096.80

Total evaluation latency_ms: 4242.47

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| citation_sections | events | FAIL | 0 distinct cited Sections; requires 2 |  |
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| evaluation_limit | judge | FAIL | Required claim not asserted |  |
| retrieval_tradeoff | judge | FAIL | Required claim not asserted |  |
| not_universally_best | judge | FAIL | Required claim not asserted |  |
| no_invented_limit | forbidden | PASS | Exact fixed refusal contains no asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2565 | 2340 | 181 | 3000 | 10000 | 949.02 | stop |
| 2 | judge | low | 653 | 428 | 60 | 1000 | 10000 | 601.84 | stop |
| 3 | judge | low | 670 | 445 | 59 | 1000 | 10000 | 1140.63 | stop |
| 4 | judge | low | 653 | 428 | 60 | 1000 | 10000 | 1354.34 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 913.55

Judge latency_ms: 0.00

Total evaluation latency_ms: 913.86

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | FAIL | Answer differs from the fixed reply or adds unsupported content |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2312 | 2087 | 91 | 3000 | 10000 | 705.09 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 980.38

Judge latency_ms: 0.00

Total evaluation latency_ms: 980.45

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2356 | 2131 | 95 | 3000 | 10000 | 771.49 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 1048.43

Judge latency_ms: 0.00

Total evaluation latency_ms: 1048.47

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2176 | 1951 | 158 | 3000 | 10000 | 910.59 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ROUTER_01 — repetition 1

Question: Summary this document.

Question Type: Lookup; expected: Global

Standalone Question: Summary this document.

Sub-queries: []

Ask latency_ms: 2371.97

Judge latency_ms: 0.00

Total evaluation latency_ms: 2372.12

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2421 | 2196 | 412 | 3000 | 10000 | 2240.48 | stop |

### Finalized answer

<pre>LightRAG is a retrieval‑augmented generation (RAG) framework that enhances large language models by incorporating graph‑based text indexing and a dual‑level retrieval mechanism (low‑level entity‑centric and high‑level topic‑centric) to capture complex inter‑dependencies among entities and produce more coherent, context‑rich responses [C1][C2].  
The system integrates graph structures with vector representations, enabling efficient retrieval of related entities and their relationships while supporting rapid incremental updates for dynamic data environments [C1][C2].  
Experimental evaluation on four datasets (Agriculture, CS, Legal, Mix) shows that LightRAG markedly outperforms the NaiveRAG baseline across three quality dimensions—Comprehensiveness, Diversity, and Empowerment—and overall scores. For example, in the Agriculture domain LightRAG achieves 67.6 % overall versus 32.4 % for NaiveRAG; similar gains are observed in the other domains [C3][C4].  
The datasets comprise 12–94 documents with token counts ranging from 619 k to over 5 M [C5].  
The authors have released LightRAG as open‑source software (https://github.com/HKUDS/LightRAG) [C1].</pre>

## ROUTER_02 — repetition 1

Question: 這篇在講什麼？

Question Type: Lookup; expected: Global

Standalone Question: 這篇在講什麼？

Sub-queries: []

Ask latency_ms: 3021.29

Judge latency_ms: 0.00

Total evaluation latency_ms: 3021.55

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2729 | 2504 | 544 | 3000 | 10000 | 2827.94 | stop |

### Finalized answer

<pre>這篇文件主要介紹 **LightRAG** 這個結合圖結構與向量表示的檢索增強生成（RAG）框架。  
- 透過 **雙層檢索（dual‑level retrieval）**，系統同時支援 **低階檢索**（針對具體實體及其屬性／關係）與 **高階檢索**（聚合多個實體以回應抽象、概念性的問題）[C2]。  
- 框架的核心是 **圖‑向量整合**：先從查詢中抽取本地關鍵字與全域關鍵字，再分別以向量資料庫匹配實體與關聯，提升本地與全域資訊的檢索效率 [C2]。  
- 文件以 **“Beekeeper（養蜂人）”** 為示例，展示實體抽取、關係建模與文本索引的過程，說明如何將實體（PERSON）與其描述、關係（如與 Bees 的互動）映射到圖中 [C1]。  
- 為驗證 LightRAG 的效能，作者在多個資料集上與 **Naive RAG、RQ‑RAG、HyDE** 等現有方法進行比較，並以大量自動生成的問題測試高階語意理解能力 [C3]。  
- 最後列出相關的學術參考文獻，涵蓋圖‑文本嵌入、RAG 方法與評估等領域的最新研究 [C4][C5]。  

總結來說，本文說明了 LightRAG 的設計理念、檢索機制、實體與關係抽取示例，以及在不同查詢類型下的效能評估。</pre>

## ROUTER_03 — repetition 1

Question: Give me the key takeaways of this paper.

Question Type: Lookup; expected: Global

Standalone Question: Give me the key takeaways of this paper.

Sub-queries: []

Ask latency_ms: 2758.47

Judge latency_ms: 0.00

Total evaluation latency_ms: 2758.52

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2345 | 2120 | 659 | 3000 | 10000 | 2550.85 | stop |

### Finalized answer

<pre>- LightRAG is a Retrieval‑Augmented Generation (RAG) framework that integrates **graph structures** into text indexing and retrieval, enabling the system to capture entities and their relationships while maintaining fast response times[C1].  

- The architecture consists of two core components: a **Data Indexer φ(·)** that builds a graph‑based indexed structure ˆD, and a **Data Retriever ψ(·)** that retrieves relevant documents by comparing queries against this structure, after which a generative model G(·) produces context‑aware answers[C2].  

- LightRAG’s **graph‑enhanced entity and relationship extraction** segments documents, extracts entities (e.g., names, dates, locations, events) and their interconnections using LLMs, and constructs a knowledge graph ˆD = (ˆV, ˆE) to support comprehensive retrieval[C2].  

- The system is designed around three efficiency goals:  
  1. **Comprehensive information retrieval** – the indexer extracts global information to improve answer quality[C2].  
  2. **Efficient, low‑cost retrieval** – the graph‑based index enables rapid, scalable query handling[C2].  
  3. **Fast adaptation to data changes** – an incremental update algorithm allows the index to incorporate new data quickly, keeping the system up‑to‑date[C1].  

- Experiments on four datasets (Agriculture, CS, Legal, Mix) show that LightRAG achieves **considerable improvements in retrieval accuracy and efficiency** compared with prior approaches; the datasets contain 12–94 documents and between ~0.6 M and 5 M tokens[C3].  

- The framework includes **prompt templates** for extracting high‑level and low‑level keywords from user queries (returned in JSON format) and for evaluating RAG outputs across three criteria—Comprehensiveness, Diversity, and Empowerment[C4].  

- In a **case study** comparing LightRAG with a baseline NaiveRAG, LightRAG delivers more in‑depth, diverse, and empowering answers (e.g., richer discussion of indigenous perspectives, legal frameworks, and collaboration), leading to it being selected as the overall winner in the evaluation JSON[C5].  

- LightRAG is **open‑source**, with the code publicly available on GitHub[C1].</pre>

## ROUTER_04 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Lookup; expected: Synthesis

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: []

Ask latency_ms: 3609.23

Judge latency_ms: 0.00

Total evaluation latency_ms: 3609.59

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2067 | 1842 | 676 | 3000 | 10000 | 3434.36 | stop |

### Finalized answer

<pre>LightRAG and GraphRAG are both graph‑enhanced retrieval‑augmented generation systems, but LightRAG consistently achieves higher performance across the evaluated dimensions.  

**Performance metrics** – The comparative tables show that, for each dataset, LightRAG attains larger win‑rate percentages than GraphRAG on all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall). For example, on the Legal dataset LightRAG’s win rates are 54.4 % (Comprehensiveness), 77.2 % (Diversity), 74.8 % (Empowerment) and 54.8 % (Overall), whereas GraphRAG’s corresponding rates are 26.0 %, 24.0 %, 25.2 % and 24.8 % respectively. Similar advantages for LightRAG are observed on the other datasets (Agriculture, CS, etc.)[C2].  

**Qualitative advantages** – LightRAG’s “dual‑level retrieval paradigm” (low‑level entity retrieval combined with high‑level topic retrieval) is credited with delivering a broader range of responses, especially in large‑scale corpora where diverse content is essential. This mechanism enables LightRAG to capture both detailed and abstract information, leading to superior Diversity and overall comprehension compared with GraphRAG[C3].  

**Overall comparison** – While both systems employ graph‑based indexing, LightRAG’s hierarchical retrieval and integration of low‑ and high‑level cues give it a clear edge in handling complex, high‑token queries and in producing more comprehensive, diverse, and empowering answers than GraphRAG[C1][C3]. A case‑study table further contrasts the two methods, underscoring LightRAG’s stronger performance[C5].</pre>

## ROUTER_05 — repetition 1

Question: LightRAG 有什麼限制？

Question Type: Lookup; expected: Synthesis

Standalone Question: LightRAG 有什麼限制？

Sub-queries: []

Ask latency_ms: 1394.53

Judge latency_ms: 0.00

Total evaluation latency_ms: 1394.60

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2479 | 2254 | 155 | 3000 | 10000 | 1174.71 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ROUTER_06 — repetition 1

Question: How do the experiments support the paper&#x27;s claims?

Question Type: Lookup; expected: Synthesis

Standalone Question: How do the experiments support the paper&#x27;s claims?

Sub-queries: []

Ask latency_ms: 3447.20

Judge latency_ms: 0.00

Total evaluation latency_ms: 3447.47

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2692 | 2467 | 757 | 3000 | 10000 | 3280.91 | stop |

### Finalized answer

<pre>The experimental results consistently show that LightRAG outperforms the baseline methods, confirming the paper’s claims about its superior performance, robustness, and efficiency.

* **Quantitative superiority:** Across the four benchmark datasets (Agriculture, CS, Legal, Mix) LightRAG achieves markedly higher win‑rate percentages than NaiveRAG, RQ‑RAG and HyDE on all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall). For example, on the Legal dataset LightRAG’s Overall win rate is 84.8 % versus 15.2 % for NaiveRAG, and on the Mix dataset it reaches 60.0 % versus 40.0 % for NaiveRAG[C1]. This pattern holds for every baseline and every dimension, demonstrating that LightRAG delivers consistently better results.

* **Ablation validation:** When key components of LightRAG are removed (high‑level or low‑level retrieval), the win rates drop substantially. The “‑High” and “‑Low” ablated versions show lower percentages across all dimensions compared with the full LightRAG model (e.g., Overall drops from 64.8 % to 57.6 % in the “‑High” ablation for the Agriculture dataset)[C2]. These ablations confirm that both high‑level and low‑level retrieval contribute to the observed performance gains.

* **Qualitative advantage:** Human‑rated evaluations of answer quality label LightRAG’s responses as the “Winner” for Diversity, Empowerment, and the Overall category. The explanations highlight that LightRAG provides richer, more nuanced coverage of metrics, deeper contextual insight, and better guidance for users, thereby supporting the claim that LightRAG delivers more empowering and diverse answers[C3].

* **Efficiency gains:** Cost analysis shows that LightRAG requires far fewer tokens and API calls than GraphRAG on the Legal dataset (e.g., 610 × 1,000 tokens vs. 1,399 × 2 × 5,000 tokens, and a single API call vs. multiple calls)[C4]. This demonstrates the model’s lower computational overhead, aligning with the claim of improved adaptability and cost‑effectiveness.

* **Experimental scope:** The experiments are conducted on four diverse corpora (Agriculture, CS, Legal, Mix) with substantial document and token counts, ensuring that the reported improvements are not limited to a narrow domain[C5].

Together, these quantitative, ablation, qualitative, and efficiency experiments provide comprehensive empirical evidence that LightRAG fulfills the paper’s assertions of higher performance, greater answer diversity and empowerment, and reduced resource consumption.</pre>

## ROUTER_07 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 4295.97

Judge latency_ms: 0.00

Total evaluation latency_ms: 4296.21

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1667 | 3000 | 10000 | 4085.95 | stop |

### Finalized answer

<pre>**Ablated‑version results (LightRAG vs. NaiveRAG)**  

| Domain / Setting | Metric | NaiveRAG | LightRAG |
|-------------------|--------|----------|----------|
| **Agriculture** (baseline) | Comprehensiveness | 32.4 % | 67.6 % |
| | Diversity | 23.6 % | 76.4 % |
| | Empowerment | 32.4 % | 67.6 % |
| | Overall | 32.4 % | 67.6 % |
| **Computer Science** (baseline) | Comprehensiveness | 38.4 % | 61.6 % |
| | Diversity | 38.0 % | 62.0 % |
| | Empowerment | 38.8 % | 61.2 % |
| | Overall | 38.8 % | 61.2 % |
| **Legal** (baseline) | Comprehensiveness | 16.4 % | 83.6 % |
| | Diversity | 13.6 % | 86.4 % |
| | Empowerment | 16.4 % | 83.6 % |
| | Overall | 15.2 % | 84.8 % |
| **Mixed** (baseline) | Comprehensiveness | 38.8 % | 61.2 % |
| | Diversity | 32.4 % | 67.6 % |
| | Empowerment | 42.8 % | 57.2 % |
| | Overall | 40.0 % | 60.0 % |
| **High‑resource** (NaiveRAG‑High) | Comprehensiveness | 34.8 % | 65.2 % |
| | Diversity | 27.2 % | 72.8 % |
| | Empowerment | 36.0 % | 64.0 % |
| | Overall | 35.2 % | 64.8 % |
| **High‑resource** (second column) | Comprehensiveness | 42.8 % | 57.2 % |
| | Diversity | 36.8 % | 63.2 % |
| | Empowerment | 42.4 % | 57.6 % |
| | Overall | 44.0 % | 56.0 % |
| **High‑resource** (third column) | Comprehensiveness | 23.6 % | 76.4 % |
| | Diversity | 16.8 % | 83.2 % |
| | Empowerment | 22.8 % | 77.2 % |
| | Overall | 22.0 % | 78.0 % |
| **High‑resource** (fourth column) | Comprehensiveness | 40.4 % | 59.6 % |
| | Diversity | 36.0 % | 64.0 % |
| | Empowerment | 47.6 % | 52.4 % |
| | Overall | 42.4 % | 57.6 % |

**Key observations**

* Across all four test domains (Agriculture, CS, Legal, Mix), LightRAG’s ablated versions achieve substantially higher scores than NaiveRAG on every metric, with overall improvements ranging from ~20 % (e.g., CS overall: 38.8 % → 61.2 %) to over 60 % (e.g., Legal overall: 15.2 % → 84.8 %)[C3].  
* In the “high‑resource” ablation settings, LightRAG also consistently outperforms NaiveRAG, delivering gains of roughly 20–30 % absolute across comprehensiveness, diversity, empowerment, and overall measures[C3].  

These results demonstrate that even when components of LightRAG are removed (ablated), the system retains a strong advantage over the NaiveRAG baseline.</pre>

## ROUTER_08 — repetition 1

Question: What datasets were used?

Question Type: Lookup; expected: Lookup

Standalone Question: What datasets were used?

Sub-queries: []

Ask latency_ms: 1682.25

Judge latency_ms: 0.00

Total evaluation latency_ms: 1682.29

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2641 | 2416 | 125 | 3000 | 10000 | 1500.84 | stop |

### Finalized answer

<pre>The experiments used four UltraDomain benchmark datasets: **Agriculture**, **CS**, **Legal**, and **Mix**[C1][C5]</pre>

## ROUTER_09 — repetition 1

Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: Table 2 裡 -Origin 在 Mix 的 Overall 是多少？

Sub-queries: []

Ask latency_ms: 4159.86

Judge latency_ms: 0.00

Total evaluation latency_ms: 4159.95

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2528 | 2303 | 1086 | 3000 | 10000 | 3994.55 | stop |

### Finalized answer

<pre>在 Table 2 中，‑Origin 条件下 Mix 数据集的 Overall 为 **64.8 %**[C4]</pre>

## ROUTER_10 — repetition 1

Question: How many API calls does LightRAG need for retrieval?

Question Type: Lookup; expected: Lookup

Standalone Question: How many API calls does LightRAG need for retrieval?

Sub-queries: []

Ask latency_ms: 938.76

Judge latency_ms: 0.00

Total evaluation latency_ms: 938.81

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2156 | 1931 | 100 | 3000 | 10000 | 754.01 | stop |

### Finalized answer

<pre>LightRAG needs just a single API call for the retrieval phase[C3].</pre>

## ROUTER_11 — repetition 1

Question: 那 LightRAG 呢？

Question Type: Lookup; expected: Lookup

Standalone Question: 那 LightRAG 呢？

Sub-queries: []

Ask latency_ms: 3471.98

Judge latency_ms: 0.00

Total evaluation latency_ms: 3472.25

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2144 | 1919 | 745 | 3000 | 10000 | 3261.40 | stop |

### Finalized answer

<pre>LightRAG 是一种图结构增强的检索‑生成（RAG）系统，核心特点包括：

1. **图结构索引与检索**：将实体及其关系建模为节点和边，结合向量表示实现高效的相关实体与关系检索[C1]。  
2. **双层检索范式**：同时进行低层次（具体片段）和高层次（抽象概念）检索，以捕获更全面的知识信息[C1]。  
3. **增量更新算法**：能够及时将新数据并入知识图谱，保持系统在快速变化环境中的时效性[C1]。  
4. **提升检索准确性与效率**：实验验证显示 LightRAG 在检索准确率和响应速度上均显著优于传统 RAG 方法[C1]。  
5. **在多维评估中的优势**：在“全面性、 多样性、赋能”和“整体”四个维度的对比实验中，LightRAG 的胜率均高于 GraphRAG，体现了其在复杂查询下的更强表现[C3]。  
6. **综合性与多样性**：通过层次化检索，LightRAG 能覆盖更广的机器学习指标，提供更丰富、多元且具启发性的答案[C4]。  
7. **效率与成本优势**：图‑基索引加上双层检索使文档检索更快速、相关性更高，同时显著降低了大模型推理的计算成本[C5]。

综上，LightRAG 通过图‑增强的索引与双层检索机制，实现了在大规模语料和复杂查询场景下的高效、全面且具赋能性的检索‑生成能力。</pre>

## ROUTER_12 — repetition 1

Question: 那它跟 GraphRAG 比呢？

Question Type: Lookup; expected: Synthesis

Standalone Question: 那它跟 GraphRAG 比呢？

Sub-queries: []

Ask latency_ms: 2457.72

Judge latency_ms: 0.00

Total evaluation latency_ms: 2458.05

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual Lookup |  |
| history_supported | events | FAIL | Lookup-only baseline has no history input |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2619 | 2394 | 593 | 3000 | 10000 | 2311.41 | stop |

### Finalized answer

<pre>LightRAG 在多个维度上均优于 GraphRAG：

1. **回答质量**  
   - 在 **Comprehensiveness、Diversity、Empowerment** 以及 **Overall** 四个评估维度上，LightRAG 的胜率均高于 GraphRAG。例如，在第一组实验中 LightRAG 的 Overall 胜率为 **54.8%**，而 GraphRAG 为 **45.2%**；在第二组实验中 LightRAG 的 Overall 胜率为 **52.0%**，而 GraphRAG 为 **48.0%**[C2]。  
   - 进一步的案例分析也表明 LightRAG 的答案在多样性、赋能和整体表现上均被评为 “Winner”，其解释强调了 LightRAG 提供了更丰富的指标解释和更深入的洞察[C3]。

2. **检索成本**  
   - **检索阶段**：GraphRAG 需要遍历 610 个社区，每个社区报告约 1,000 tokens，累计约 **610,000 tokens**，且产生数百次 API 调用；而 LightRAG 只使用 **&lt;100 tokens** 进行关键词生成和检索，并仅需一次 API 调用[C4]。  
   - **增量更新阶段**：当加入与 Legal 数据集等量的新数据时，GraphRAG 必须拆除并重新生成全部社区报告，代价约 **1,399 × 2 × 5,000 tokens**，成本极高；LightRAG 则直接将新抽取的实体和关系并入现有图结构，无需完整重建，成本显著更低[C5]。

综上所述，LightRAG 在答案的全面性、丰富性和实用性上均领先于 GraphRAG，同时在 token 消耗、API 调用次数以及增量更新的效率上也更具优势。</pre>


## Judge semantic probes (excluded from Golden Facts result)

## JUDGE_ASSERTED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 768.78

Total evaluation latency_ms: 768.78

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 85 | 1000 | 10000 | 768.78 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 821.91

Total evaluation latency_ms: 821.91

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 821.91 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
