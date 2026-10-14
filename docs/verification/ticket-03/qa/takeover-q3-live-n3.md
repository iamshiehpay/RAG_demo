# Golden Facts evaluation

Created: 2026-10-13T01:57:56.269516+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: nova-qa03-integrated

Revision: ca8a02c747086b6aabd2d05e34a5a0b90be59708

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
| Q3 | low_term | contains | 3/3 (100.0%) |
| Q3 | origin_term | contains | 3/3 (100.0%) |
| Q3 | table2_baseline | judge | 1/3 (33.3%) |
| Q3 | ablation_meaning | judge | 0/3 (0.0%) |
| Q3 | mix_low_overall | judge | 0/3 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/3 (0.0%) |
| Q3 | not_all_best | forbidden | 2/3 (66.7%) |

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

Ask latency_ms: 6190.82

Judge latency_ms: 10346.94

Total evaluation latency_ms: 16561.22

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *Each cell shows “NaïveRAG win % / variant win %”. The full LightRAG row (LightRAG vs. NaïveRAG) is the reference for these comparisons*[C9]. |
| ablation_meaning | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | **‑High** (removes high‑level retrieval) \| **‑Low** (removes low‑level retrieval) \| **‑Origin** (removes original‑text retrieval) |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 128 | 600 | 10000 | 1505.18 | stop |
| 2 | answer | medium | 5784 | 5559 | 1299 | 3000 | 10000 | 4448.30 | stop |
| 3 | judge | low | 1747 | 1522 | 220 | 1000 | 10000 | 3214.12 | stop |
| 4 | judge | low | 1748 | 1523 | 257 | 1000 | 10000 | 2311.08 | stop |
| 5 | judge | low | 1759 | 1534 | 196 | 1000 | 10000 | 1338.24 | stop |
| 6 | judge | low | 1759 | 1534 | 179 | 1000 | 10000 | 1194.67 | stop |
| 7 | judge | low | 1735 | 1510 | 182 | 1000 | 10000 | 2288.83 | stop |

### Finalized answer

<pre>**Ablated‑version performance (win‑rate percentages against the NaïveRAG baseline)**  

| Variant | Metric | Agriculture | CS | Legal | Mix |
|---------|--------|-------------|----|-------|-----|
| **‑High** (removes high‑level retrieval) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (removes low‑level retrieval) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (removes original‑text retrieval) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

*Each cell shows “NaïveRAG win % / variant win %”. The full LightRAG row (LightRAG vs. NaïveRAG) is the reference for these comparisons*[C9].

**Key observations from the ablation study**

* The **‑High** variant (low‑level‑only retrieval) suffers a noticeable drop in performance across almost all metrics and datasets compared with the full LightRAG, especially in comprehensiveness and overall scores[C10].  
* The **‑Low** variant (high‑level‑only retrieval) also declines relative to the full system, though it retains relatively strong diversity scores; its loss of depth in specific entity retrieval harms comprehensiveness and overall effectiveness[C10].  
* The **‑Origin** variant (removing original‑text retrieval) does **not** cause major degradations; in some cases (e.g., Agriculture and Mix) it even yields higher win rates for certain metrics, suggesting that the graph‑based indexing alone can provide sufficient context[C10].  

Thus, the ablated versions generally perform worse than the full LightRAG, with the hybrid (full) model achieving the most balanced and highest win rates across the four benchmark domains.</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 8616.11

Judge latency_ms: 8461.29

Total evaluation latency_ms: 17089.91

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | For each variant the table reports the win‑rate of NaiveRAG versus the variant (baseline % / variant %) on four datasets... |
| ablation_meaning | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | **‑High (high‑level‑only retrieval)**  <br>\| Metric \| Agriculture \| CS \| Legal \| Mix \|<br>...**‑Low (low‑level‑only retrieval)**  <br>...**‑Origin (removing original text from retrieval)**  <br>...Across all four datasets, each ablated version attains lower win‑rates than the full LightRAG system (which is the “unmodified system” row in the same table). |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | Across all four datasets, each ablated version attains lower win‑rates than the full LightRAG system (which is the “unmodified system” row in the same table). |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 122 | 600 | 10000 | 1081.35 | stop |
| 2 | answer | medium | 5784 | 5559 | 1369 | 3000 | 10000 | 7305.61 | stop |
| 3 | judge | low | 1836 | 1611 | 210 | 1000 | 10000 | 1198.79 | stop |
| 4 | judge | low | 1837 | 1612 | 227 | 1000 | 10000 | 1362.94 | stop |
| 5 | judge | low | 1848 | 1623 | 335 | 1000 | 10000 | 2342.64 | stop |
| 6 | judge | low | 1848 | 1623 | 240 | 1000 | 10000 | 1982.97 | stop |
| 7 | judge | low | 1824 | 1599 | 211 | 1000 | 10000 | 1573.96 | stop |

### Finalized answer

<pre>The ablation study compares three stripped‑down variants of LightRAG (‑High, ‑Low, and ‑Origin) against the NaiveRAG baseline.  For each variant the table reports the win‑rate of NaiveRAG versus the variant (baseline % / variant %) on four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C9].

**‑High (high‑level‑only retrieval)**  
| Metric | Agriculture | CS | Legal | Mix |
|--------|-------------|----|-------|-----|
| Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |

**‑Low (low‑level‑only retrieval)**  
| Metric | Agriculture | CS | Legal | Mix |
|--------|-------------|----|-------|-----|
| Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |

**‑Origin (removing original text from retrieval)**  
| Metric | Agriculture | CS | Legal | Mix |
|--------|-------------|----|-------|-----|
| Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

Across all four datasets, each ablated version attains lower win‑rates than the full LightRAG system (which is the “unmodified system” row in the same table).  The ‑High variant suffers the greatest drop in comprehensiveness, the ‑Low variant shows the strongest decline in diversity on the Legal dataset, and the ‑Origin variant generally maintains competitive scores but still lags behind the full system on most metrics[C9].

Qualitatively, the authors note that removing high‑order retrieval (‑Low) leads to a “significant performance decline across nearly all datasets and metrics” because it over‑focuses on specific entities, while removing low‑level retrieval (‑High) harms depth of detail.  The ‑Origin variant, which eliminates original text from retrieval, “does not exhibit significant performance declines” and even improves in some cases (e.g., Agriculture and Mix)[C10].</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 4348.23

Judge latency_ms: 7900.88

Total evaluation latency_ms: 12268.60

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The ablation study compares three LightRAG variants (‑High, ‑Low, ‑Origin) against the NaiveRAG baseline on four datasets ... For each cell the table reports “NaiveRAG win % / variant win %”.  The variant win % therefore reflects the performance of the ablated version. |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 129 | 600 | 10000 | 929.12 | stop |
| 2 | answer | medium | 5784 | 5559 | 976 | 3000 | 10000 | 3185.60 | stop |
| 3 | judge | low | 1433 | 1208 | 265 | 1000 | 10000 | 1792.45 | stop |
| 4 | judge | low | 1434 | 1209 | 278 | 1000 | 10000 | 1405.57 | stop |
| 5 | judge | low | 1445 | 1220 | 210 | 1000 | 10000 | 1740.86 | stop |
| 6 | judge | low | 1445 | 1220 | 143 | 1000 | 10000 | 1466.21 | stop |
| 7 | judge | low | 1421 | 1196 | 113 | 1000 | 10000 | 1495.78 | stop |

### Finalized answer

<pre>The ablation study compares three LightRAG variants (‑High, ‑Low, ‑Origin) against the NaiveRAG baseline on four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall).  For each cell the table reports “NaiveRAG win % / variant win %”.  The variant win % therefore reflects the performance of the ablated version.

| Variant | Metric | Agriculture (variant %) | CS (variant %) | Legal (variant %) | Mix (variant %) |
|---------|--------|------------------------|---------------|-------------------|----------------|
| **‑High** (high‑level‑only retrieval) | Comprehensiveness | 65.2 % | 57.2 % | 76.4 % | 59.6 % |
| | Diversity | 72.8 % | 63.2 % | 83.2 % | 64.0 % |
| | Empowerment | 64.0 % | 57.6 % | 77.2 % | 52.4 % |
| | Overall | 64.8 % | 56.0 % | 78.0 % | 57.6 % |
| **‑Low** (low‑level‑only retrieval) | Comprehensiveness | 64.0 % | 56.8 % | 80.8 % | 64.0 % |
| | Diversity | 72.0 % | 60.4 % | 86.4 % | 66.8 % |
| | Empowerment | 65.2 % | 57.2 % | 83.6 % | 64.8 % |
| | Overall | 65.2 % | 56.4 % | 81.2 % | 64.8 % |
| **‑Origin** (original‑text removed) | Comprehensiveness | 75.2 % | 60.8 % | 83.6 % | 55.6 % |
| | Diversity | 73.6 % | 55.2 % | 85.6 % | 74.4 % |
| | Empowerment | 68.0 % | 56.8 % | 82.8 % | 54.8 % |
| | Overall | 74.4 % | 60.8 % | 84.4 % | 55.6 % |

These numbers are taken directly from Table 2 of the paper [C9].

Qualitatively, the authors note that:

* The **‑High** variant (high‑level‑only retrieval) suffers a “significant performance decline across nearly all datasets and metrics” because it focuses too narrowly on specific entities [C10].
* The **‑Low** variant (low‑level‑only retrieval) improves comprehensiveness but loses depth for detailed answers, leading to mixed results [C10].
* The **‑Origin** variant (removing original text) does **not** cause major performance drops and even improves in some cases (e.g., Agriculture and Mix), suggesting that the graph‑based indexing captures enough context [C10].

Thus, the ablated versions achieve the win‑rate percentages shown above, with the full LightRAG (hybrid mode) generally outperforming each single‑level variant.</pre>


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

Judge latency_ms: 909.89

Total evaluation latency_ms: 909.89

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 122 | 1000 | 10000 | 909.89 | stop |

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

Judge latency_ms: 773.29

Total evaluation latency_ms: 773.29

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 111 | 1000 | 10000 | 773.29 | stop |

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

Judge latency_ms: 808.27

Total evaluation latency_ms: 808.27

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 110 | 1000 | 10000 | 808.27 | stop |

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

Judge latency_ms: 1305.38

Total evaluation latency_ms: 1305.38

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 111 | 1000 | 10000 | 1305.38 | stop |

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

Judge latency_ms: 780.40

Total evaluation latency_ms: 780.40

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 114 | 1000 | 10000 | 780.40 | stop |

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

Judge latency_ms: 705.76

Total evaluation latency_ms: 705.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 111 | 1000 | 10000 | 705.76 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
