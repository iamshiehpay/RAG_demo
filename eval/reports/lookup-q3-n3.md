# Golden Facts evaluation

Created: 2026-10-12T14:59:14.030005+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Label: lookup-q3-n3

Revision: 4408c6a0b3fe8cf3e228da7628d7bf42716a927d

Uncommitted changes: yes

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: #06 exported cases if available; otherwise fixed spike cases

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q3 | question_type | events | 3/3 (100.0%) |
| Q3 | high_term | contains | 3/3 (100.0%) |
| Q3 | low_term | contains | 2/3 (66.7%) |
| Q3 | origin_term | contains | 0/3 (0.0%) |
| Q3 | table2_baseline | judge | 0/3 (0.0%) |
| Q3 | ablation_meaning | judge | 0/3 (0.0%) |
| Q3 | mix_low_overall | judge | 0/3 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/3 (0.0%) |
| Q3 | not_all_best | forbidden | 3/3 (100.0%) |
| JUDGE_ASSERTED | semantic_contract | judge | 3/3 (100.0%) |
| JUDGE_NEGATED | semantic_contract | judge | 3/3 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 10504.69

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | FAIL | Required claim not asserted |  |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1658 | 3000 | 10000 | 4030.80 | stop |
| 2 | judge | low | 1384 | 1159 | 176 | 1000 | 10000 | 928.19 | stop |
| 3 | judge | low | 1385 | 1160 | 103 | 1000 | 10000 | 803.18 | stop |
| 4 | judge | low | 1396 | 1171 | 186 | 1000 | 10000 | 2894.86 | stop |
| 5 | judge | low | 1396 | 1171 | 128 | 1000 | 10000 | 860.23 | stop |
| 6 | judge | low | 1372 | 1147 | 103 | 1000 | 10000 | 838.21 | stop |

### Finalized answer

<pre>**Ablated‑version performance (Table 2, Section 8)**  

The paper evaluates three ablation settings of LightRAG against the NaiveRAG baseline across four domains (Agriculture, CS, Legal, Mix). For each setting the metrics *Comprehensiveness, Diversity, Empowerment* and *Overall* are reported as percentages.

| Domain | Ablation setting | Comprehensiveness | Diversity | Empowerment | Overall |
|--------|------------------|-------------------|-----------|-------------|---------|
| **Agriculture** | NaiveRAG vs LightRAG | 32.4 % → 67.6 % | 23.6 % → 76.4 % | 32.4 % → 67.6 % | 32.4 % → 67.6 % |
| **CS** | NaiveRAG vs LightRAG | 38.4 % → 61.6 % | 38.0 % → 62.0 % | 38.8 % → 61.2 % | 38.8 % → 61.2 % |
| **Legal** | NaiveRAG vs LightRAG | 16.4 % → 83.6 % | 13.6 % → 86.4 % | 16.4 % → 83.6 % | 15.2 % → 84.8 % |
| **Mix** | NaiveRAG vs LightRAG | 38.8 % → 61.2 % | 32.4 % → 67.6 % | 42.8 % → 57.2 % | 40.0 % → 60.0 % |

| Domain | Ablation setting (NaiveRAG‑High vs LightRAG) | Comprehensiveness | Diversity | Empowerment | Overall |
|--------|-------------------------------------------|-------------------|-----------|-------------|---------|
| **Agriculture** | 34.8 % → 65.2 % | 27.2 % → 72.8 % | 36.0 % → 64.0 % | 35.2 % → 64.8 % |
| **CS** | 42.8 % → 57.2 % | 36.8 % → 63.2 % | 42.4 % → 57.6 % | 44.0 % → 56.0 % |
| **Legal** | 23.6 % → 76.4 % | 16.8 % → 83.2 % | 22.8 % → 77.2 % | 22.0 % → 78.0 % |
| **Mix** | 40.4 % → 59.6 % | 36.0 % → 64.0 % | 47.6 % → 52.4 % | 42.4 % → 57.6 % |

*The “→” indicates the performance of the NaiveRAG reference (left) versus the corresponding LightRAG ablation (right).*

The table also lists a third condition labeled “NaiveRAG‑Low”, but the excerpt does not provide the numeric results for this setting, so they cannot be reported here.

All figures are taken directly from Table 2 of the document [C3].</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 12384.99

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | FAIL | Required claim not asserted |  |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1751 | 3000 | 10000 | 7184.64 | stop |
| 2 | judge | low | 1466 | 1241 | 154 | 1000 | 10000 | 1142.67 | stop |
| 3 | judge | low | 1467 | 1242 | 106 | 1000 | 10000 | 1025.21 | stop |
| 4 | judge | low | 1478 | 1253 | 121 | 1000 | 10000 | 963.19 | stop |
| 5 | judge | low | 1478 | 1253 | 129 | 1000 | 10000 | 972.17 | stop |
| 6 | judge | low | 1454 | 1229 | 119 | 1000 | 10000 | 850.38 | stop |

### Finalized answer

<pre>**Ablated‑version performance (Table 2, Section 8)**  

The paper evaluates LightRAG under three settings – the standard model, a **high‑resource** ablation (NaiveRAG‑High vs LightRAG‑High) and a **low‑resource** ablation (NaiveRAG‑Low vs LightRAG‑Low). Results are reported for four domains (Agriculture, CS, Legal, Mix) on four metrics: Comprehensiveness, Diversity, Empowerment and Overall.  

| Domain | Setting | Comprehensiveness | Diversity | Empowerment | Overall |
|--------|---------|-------------------|-----------|------------|---------|
| **Agriculture** | Standard | NaiveRAG 32.4 % → LightRAG 67.6 % | 23.6 % → 76.4 % | 32.4 % → 67.6 % | 32.4 % → 67.6 % |
| | High‑resource | NaiveRAG‑High 34.8 % → LightRAG‑High 65.2 % | 27.2 % → 72.8 % | 36.0 % → 64.0 % | 35.2 % → 64.8 % |
| | Low‑resource | *Numbers not provided in the excerpt* |  |  |  |
| **CS** | Standard | 38.4 % → 61.6 % | 38.0 % → 62.0 % | 38.8 % → 61.2 % | 38.8 % → 61.2 % |
| | High‑resource | 42.8 % → 57.2 % | 36.8 % → 63.2 % | 42.4 % → 57.6 % | 44.0 % → 56.0 % |
| | Low‑resource | *Numbers not provided in the excerpt* |  |  |  |
| **Legal** | Standard | 16.4 % → 83.6 % | 13.6 % → 86.4 % | 16.4 % → 83.6 % | 15.2 % → 84.8 % |
| | High‑resource | 23.6 % → 76.4 % | 16.8 % → 83.2 % | 22.8 % → 77.2 % | 22.0 % → 78.0 % |
| | Low‑resource | *Numbers not provided in the excerpt* |  |  |  |
| **Mix** | Standard | 38.8 % → 61.2 % | 32.4 % → 67.6 % | 42.8 % → 57.2 % | 40.0 % → 60.0 % |
| | High‑resource | 40.4 % → 59.6 % | 36.0 % → 64.0 % | 47.6 % → 52.4 % | 42.4 % → 57.6 % |
| | Low‑resource | *Numbers not provided in the excerpt* |  |  |  |

**Interpretation**  
- Across all domains, LightRAG (both standard and high‑resource ablations) consistently outperforms the NaiveRAG baseline, often by 30–70 percentage points.  
- The high‑resource ablation still retains a sizable gain over NaiveRAG‑High, confirming that LightRAG’s graph‑enhanced indexing contributes most of the improvement.  
- The document does not include the numeric results for the low‑resource ablation; therefore those figures cannot be reported.  

*All percentages are taken directly from Table 2 in the paper*[C3].</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Total evaluation latency_ms: 11892.24

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | FAIL | Term missing |  |
| origin_term | contains | FAIL | Term missing |  |
| table2_baseline | judge | FAIL | Judge failed: LLMFailure: Answer was truncated. Please retry. |  |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 1981 | 1756 | 1647 | 3000 | 10000 | 4924.20 | stop |
| 2 | judge | low | 1381 | 1156 | 1000 | 1000 | 10000 | 2482.63 | length |
| 3 | judge | low | 1382 | 1157 | 123 | 1000 | 10000 | 768.88 | stop |
| 4 | judge | low | 1393 | 1168 | 214 | 1000 | 10000 | 1290.12 | stop |
| 5 | judge | low | 1393 | 1168 | 129 | 1000 | 10000 | 1483.53 | stop |
| 6 | judge | low | 1369 | 1144 | 105 | 1000 | 10000 | 770.19 | stop |

### Finalized answer

<pre>**Ablated LightRAG performance (Table 2, Section 8)**  

The table compares LightRAG (in three ablation settings) with NaiveRAG across four data domains – Agriculture, CS, Legal, and Mix – using four evaluation dimensions: Comprehensiveness, Diversity, Empowerment, and Overall.

| Domain | Ablation setting | **Comprehensiveness** | **Diversity** | **Empowerment** | **Overall** |
|--------|------------------|-----------------------|---------------|----------------|------------|
| **Agriculture** | NaiveRAG vs LightRAG | 32.4 % → 67.6 % | 23.6 % → 76.4 % | 32.4 % → 67.6 % | 32.4 % → 67.6 % |
| **CS** | NaiveRAG vs LightRAG | 38.4 % → 61.6 % | 38.0 % → 62.0 % | 38.8 % → 61.2 % | 38.8 % → 61.2 % |
| **Legal** | NaiveRAG vs LightRAG | 16.4 % → 83.6 % | 13.6 % → 86.4 % | 16.4 % → 83.6 % | 15.2 % → 84.8 % |
| **Mix** | NaiveRAG vs LightRAG | 38.8 % → 61.2 % | 32.4 % → 67.6 % | 42.8 % → 57.2 % | 40.0 % → 60.0 % |
| **Agriculture** | NaiveRAG‑High vs LightRAG‑High | 34.8 % → 65.2 % | 27.2 % → 72.8 % | 36.0 % → 64.0 % | 35.2 % → 64.8 % |
| **CS** | NaiveRAG‑High vs LightRAG‑High | 42.8 % → 57.2 % | 36.8 % → 63.2 % | 42.4 % → 57.6 % | 44.0 % → 56.0 % |
| **Legal** | NaiveRAG‑High vs LightRAG‑High | 23.6 % → 76.4 % | 16.8 % → 83.2 % | 22.8 % → 77.2 % | 22.0 % → 78.0 % |
| **Mix** | NaiveRAG‑High vs LightRAG‑High | 40.4 % → 59.6 % | 36.0 % → 64.0 % | 47.6 % → 52.4 % | 42.4 % → 57.6 % |

*Interpretation*: In every domain and metric, the ablated LightRAG variants achieve substantially higher percentages than the NaiveRAG baselines, demonstrating the benefit of LightRAG’s graph‑enhanced retrieval components.  

All figures are taken directly from Table 2 of the paper [C3].</pre>

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
| 1 | judge | low | 560 | 335 | 82 | 1000 | 10000 | 693.46 | stop |

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
| 1 | judge | low | 574 | 349 | 112 | 1000 | 10000 | 869.19 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>

## JUDGE_ASSERTED — repetition 2

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
| 1 | judge | low | 560 | 335 | 82 | 1000 | 10000 | 717.12 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 2

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
| 1 | judge | low | 574 | 349 | 125 | 1000 | 10000 | 775.57 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>

## JUDGE_ASSERTED — repetition 3

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
| 1 | judge | low | 560 | 335 | 82 | 1000 | 10000 | 800.98 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 3

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
| 1 | judge | low | 574 | 349 | 125 | 1000 | 10000 | 837.97 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
