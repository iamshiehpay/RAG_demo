# Golden Facts evaluation

Created: 2026-10-12T17:35:51.846062+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: qa-08

Revision: f38cf47ae990dc6a57d7d807bbd0ef2eb64f9c3f

Uncommitted changes: yes

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: chat_document.router_regression.CASES (#06 canonical 12 cases)

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q3 | table2_citation | events | 3/3 (100.0%) |
| Q3 | question_type | events | 3/3 (100.0%) |
| Q3 | high_term | contains | 3/3 (100.0%) |
| Q3 | low_term | contains | 0/3 (0.0%) |
| Q3 | origin_term | contains | 0/3 (0.0%) |
| Q3 | table2_baseline | judge | 0/3 (0.0%) |
| Q3 | ablation_meaning | judge | 0/3 (0.0%) |
| Q3 | mix_low_overall | judge | 0/3 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/3 (0.0%) |
| Q3 | not_all_best | forbidden | 3/3 (100.0%) |
| ABSENT_HOTPOT | question_type | events | 3/3 (100.0%) |
| ABSENT_HOTPOT | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_LICENSE | question_type | events | 3/3 (100.0%) |
| ABSENT_LICENSE | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_GPU | question_type | events | 3/3 (100.0%) |
| ABSENT_GPU | fixed_reply | judge | 3/3 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 4840.16

Judge latency_ms: 6178.76

Total evaluation latency_ms: 11033.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required source Chunk (metadata fallback) | C3 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
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
| 1 | router | low | 825 | 486 | 124 | 600 | 10000 | 1385.55 | stop |
| 2 | answer | medium | 2113 | 1888 | 1240 | 3000 | 10000 | 3285.87 | stop |
| 3 | judge | low | 1202 | 977 | 131 | 1000 | 10000 | 775.28 | stop |
| 4 | judge | low | 1203 | 978 | 117 | 1000 | 10000 | 1162.66 | stop |
| 5 | judge | low | 1214 | 989 | 231 | 1000 | 10000 | 1874.96 | stop |
| 6 | judge | low | 1214 | 989 | 142 | 1000 | 10000 | 999.82 | stop |
| 7 | judge | low | 1190 | 965 | 82 | 1000 | 10000 | 1366.04 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (using NaiveRAG as reference)**  

| Dataset | Metric | LightRAG (ablated) |
|--------|--------|--------------------|
| **Agriculture** | Comprehensiveness | 67.6 % |
| | Diversity | 76.4 % |
| | Empowerment | 67.6 % |
| | Overall | 67.6 % |
| **Computer Science (CS)** | Comprehensiveness | 61.6 % |
| | Diversity | 62.0 % |
| | Empowerment | 61.2 % |
| | Overall | 61.2 % |
| **Legal** | Comprehensiveness | 83.6 % |
| | Diversity | 86.4 % |
| | Empowerment | 83.6 % |
| | Overall | 84.8 % |
| **Mix** | Comprehensiveness | 61.2 % |
| | Diversity | 67.6 % |
| | Empowerment | 57.2 % |
| | Overall | 60.0 % |

*High‑ablation variant (NaiveRAG‑High)*  

| Dataset | Metric | LightRAG (high‑ablation) |
|--------|--------|--------------------------|
| Agriculture | Comprehensiveness | 65.2 % |
| | Diversity | 72.8 % |
| | Empowerment | 64.0 % |
| | Overall | 64.8 % |
| CS | Comprehensiveness | 57.2 % |
| | Diversity | 63.2 % |
| | Empowerment | 57.6 % |
| | Overall | 56.0 % |
| Legal | Comprehensiveness | 76.4 % |
| | Diversity | 83.2 % |
| | Empowerment | 77.2 % |
| | Overall | 78.0 % |
| Mix | Comprehensiveness | 59.6 % |
| | Diversity | 64.0 % |
| | Empowerment | 52.4 % |
| | Overall | 57.6 % |

These figures are taken directly from Table 2, which reports the performance of the ablated versions of LightRAG across four benchmark domains[C3].</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 6986.20

Judge latency_ms: 5351.03

Total evaluation latency_ms: 12344.87

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required source Chunk (metadata fallback) | C3 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
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
| 1 | router | low | 825 | 486 | 121 | 600 | 10000 | 1615.25 | stop |
| 2 | answer | medium | 2113 | 1888 | 1370 | 3000 | 10000 | 5199.70 | stop |
| 3 | judge | low | 1102 | 877 | 105 | 1000 | 10000 | 804.56 | stop |
| 4 | judge | low | 1103 | 878 | 97 | 1000 | 10000 | 765.29 | stop |
| 5 | judge | low | 1114 | 889 | 152 | 1000 | 10000 | 1456.51 | stop |
| 6 | judge | low | 1114 | 889 | 135 | 1000 | 10000 | 1501.85 | stop |
| 7 | judge | low | 1090 | 865 | 95 | 1000 | 10000 | 822.82 | stop |

### Finalized answer

<pre>The ablated LightRAG models were evaluated on four benchmark domains (Agriculture, CS, Legal, Mix) using four metrics. The percentages reported for the LightRAG column in Table 2 are:

**Baseline ablation (LightRAG vs. NaiveRAG)**  
- **Agriculture:** Comprehensiveness 67.6 %, Diversity 76.4 %, Empowerment 67.6 %, Overall 67.6 %[C3]  
- **CS:** Comprehensiveness 61.6 %, Diversity 62.0 %, Empowerment 61.2 %, Overall 61.2 %[C3]  
- **Legal:** Comprehensiveness 83.6 %, Diversity 86.4 %, Empowerment 83.6 %, Overall 84.8 %[C3]  
- **Mix:** Comprehensiveness 61.2 %, Diversity 67.6 %, Empowerment 57.2 %, Overall 60.0 %[C3]

**“‑High” ablation (LightRAG‑High vs. NaiveRAG‑High)**  
- **Agriculture:** Comprehensiveness 65.2 %, Diversity 72.8 %, Empowerment 64.0 %, Overall 64.8 %[C3]  
- **CS:** Comprehensiveness 57.2 %, Diversity 63.2 %, Empowerment 57.6 %, Overall 56.0 %[C3]  
- **Legal:** Comprehensiveness 76.4 %, Diversity 83.2 %, Empowerment 77.2 %, Overall 78.0 %[C3]  
- **Mix:** Comprehensiveness 59.6 %, Diversity 64.0 %, Empowerment 52.4 %, Overall 57.6 %[C3]

These figures represent the performance of the ablated versions of LightRAG across the four datasets and four evaluation dimensions.</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 6160.10

Judge latency_ms: 7087.50

Total evaluation latency_ms: 13257.06

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required source Chunk (metadata fallback) | C3 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
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
| 1 | router | low | 825 | 486 | 121 | 600 | 10000 | 999.62 | stop |
| 2 | answer | medium | 2113 | 1888 | 1621 | 3000 | 10000 | 4930.55 | stop |
| 3 | judge | low | 1485 | 1260 | 192 | 1000 | 10000 | 1667.21 | stop |
| 4 | judge | low | 1486 | 1261 | 99 | 1000 | 10000 | 767.75 | stop |
| 5 | judge | low | 1497 | 1272 | 313 | 1000 | 10000 | 2385.10 | stop |
| 6 | judge | low | 1497 | 1272 | 145 | 1000 | 10000 | 884.99 | stop |
| 7 | judge | low | 1473 | 1248 | 96 | 1000 | 10000 | 1382.45 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (NaiveRAG shown for reference)**  

| Dataset | Metric | NaiveRAG (baseline) | LightRAG (ablated) |
|---------|--------|---------------------|--------------------|
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

**High‑ablation variant (NaiveRAG‑High vs. LightRAG‑High)**  

| Dataset | Metric | NaiveRAG‑High | LightRAG‑High |
|---------|--------|--------------|---------------|
| Agriculture | Comprehensiveness | 34.8 % | **65.2 %** |
| | Diversity | 27.2 % | **72.8 %** |
| | Empowerment | 36.0 % | **64.0 %** |
| | Overall | 35.2 % | **64.8 %** |
| CS | Comprehensiveness | 42.8 % | **57.2 %** |
| | Diversity | 36.8 % | **63.2 %** |
| | Empowerment | 42.4 % | **57.6 %** |
| | Overall | 44.0 % | **56.0 %** |
| Legal | Comprehensiveness | 23.6 % | **76.4 %** |
| | Diversity | 16.8 % | **83.2 %** |
| | Empowerment | 22.8 % | **77.2 %** |
| | Overall | 22.0 % | **78.0 %** |
| Mix | Comprehensiveness | 40.4 % | **59.6 %** |
| | Diversity | 36.0 % | **64.0 %** |
| | Empowerment | 47.6 % | **52.4 %** |
| | Overall | 42.4 % | **57.6 %** |

*All numbers are taken from Table 2 in the paper, which reports the performance of ablated LightRAG versions compared with NaiveRAG as the reference.* [C3]</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 2414.12

Judge latency_ms: 0.00

Total evaluation latency_ms: 2414.24

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 106 | 600 | 10000 | 696.88 | stop |
| 2 | answer | medium | 2378 | 2153 | 116 | 3000 | 10000 | 1374.45 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_HOTPOT — repetition 2

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 1849.36

Judge latency_ms: 0.00

Total evaluation latency_ms: 1849.41

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 92 | 600 | 10000 | 787.51 | stop |
| 2 | answer | medium | 2378 | 2153 | 119 | 3000 | 10000 | 849.12 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_HOTPOT — repetition 3

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 2068.02

Judge latency_ms: 0.00

Total evaluation latency_ms: 2068.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 106 | 600 | 10000 | 864.85 | stop |
| 2 | answer | medium | 2378 | 2153 | 178 | 3000 | 10000 | 1066.79 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 1743.41

Judge latency_ms: 0.00

Total evaluation latency_ms: 1743.49

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 78 | 600 | 10000 | 755.74 | stop |
| 2 | answer | medium | 2388 | 2163 | 103 | 3000 | 10000 | 801.29 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_LICENSE — repetition 2

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 1786.24

Judge latency_ms: 0.00

Total evaluation latency_ms: 1786.32

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 78 | 600 | 10000 | 739.16 | stop |
| 2 | answer | medium | 2388 | 2163 | 104 | 3000 | 10000 | 846.17 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_LICENSE — repetition 3

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 1708.63

Judge latency_ms: 0.00

Total evaluation latency_ms: 1708.71

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 78 | 600 | 10000 | 769.71 | stop |
| 2 | answer | medium | 2388 | 2163 | 94 | 3000 | 10000 | 751.55 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 1969.70

Judge latency_ms: 0.00

Total evaluation latency_ms: 1969.78

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 123 | 600 | 10000 | 815.79 | stop |
| 2 | answer | medium | 2243 | 2018 | 150 | 3000 | 10000 | 930.69 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_GPU — repetition 2

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 2459.03

Judge latency_ms: 0.00

Total evaluation latency_ms: 2459.14

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 123 | 600 | 10000 | 1385.13 | stop |
| 2 | answer | medium | 2243 | 2018 | 150 | 3000 | 10000 | 885.53 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_GPU — repetition 3

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 1900.60

Judge latency_ms: 0.00

Total evaluation latency_ms: 1900.74

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 113 | 600 | 10000 | 796.86 | stop |
| 2 | answer | medium | 2243 | 2018 | 166 | 3000 | 10000 | 882.54 | stop |

### Finalized answer

<pre>文件中未提及</pre>


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

Judge latency_ms: 690.76

Total evaluation latency_ms: 690.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 85 | 1000 | 10000 | 690.76 | stop |

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

Judge latency_ms: 742.10

Total evaluation latency_ms: 742.10

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 742.10 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>

## JUDGE_ASSERTED — repetition 2

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 725.76

Total evaluation latency_ms: 725.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 725.76 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 2

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 860.67

Total evaluation latency_ms: 860.67

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 860.67 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>

## JUDGE_ASSERTED — repetition 3

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 706.64

Total evaluation latency_ms: 706.64

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 114 | 1000 | 10000 | 706.64 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 3

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 677.61

Total evaluation latency_ms: 677.61

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 677.61 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
