# Golden Facts evaluation

Created: 2026-10-12T20:21:45.522643+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: table-reconstruction-q3-n3

Revision: fef26f5dc5315a5f19441e388c15e8845324e284

Uncommitted changes: no

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
| Q3 | table2_baseline | judge | 3/3 (100.0%) |
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

Ask latency_ms: 7329.28

Judge latency_ms: 8594.29

Total evaluation latency_ms: 15934.54

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | For each dataset the table reports the win‑rate of NaiveRAG versus the win‑rate of the variant (percentage). The numbers are **not** direct wins against the full LightRAG model but separate comparisons against NaiveRAG[C9]. |
| ablation_meaning | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | **‑High** (high‑level‑only) ... **‑Low** (low‑level‑only) ... **‑Origin** (no original text) ... Overall, the ablation study shows that the **dual‑level retrieval** (both low‑ and high‑level) is essential for achieving the best comprehensive, diverse, and empowering responses |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | The full LightRAG model (not shown in the table) consistently outperforms NaiveRAG, and each ablated variant achieves lower win‑rates than the full model. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 121 | 600 | 10000 | 1692.70 | stop |
| 2 | answer | medium | 5387 | 5162 | 1494 | 3000 | 10000 | 5437.06 | stop |
| 3 | judge | low | 1909 | 1684 | 241 | 1000 | 10000 | 1146.25 | stop |
| 4 | judge | low | 1910 | 1685 | 241 | 1000 | 10000 | 1819.40 | stop |
| 5 | judge | low | 1921 | 1696 | 270 | 1000 | 10000 | 2512.62 | stop |
| 6 | judge | low | 1921 | 1696 | 223 | 1000 | 10000 | 1949.77 | stop |
| 7 | judge | low | 1897 | 1672 | 194 | 1000 | 10000 | 1166.24 | stop |

### Finalized answer

<pre>The ablation study compares three reduced versions of LightRAG (‑High, ‑Low, and ‑Origin) with the NaiveRAG baseline. For each dataset the table reports the win‑rate of NaiveRAG versus the win‑rate of the variant (percentage). The numbers are **not** direct wins against the full LightRAG model but separate comparisons against NaiveRAG[C9].

| Variant | Metric | Agriculture (NaiveRAG / variant %) | CS (NaiveRAG / variant %) | Legal (NaiveRAG / variant %) | Mix (NaiveRAG / variant %) |
|---------|--------|-----------------------------------|---------------------------|------------------------------|----------------------------|
| **‑High** (high‑level‑only) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (low‑level‑only) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (no original text) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

**Interpretation of the results**

* The full LightRAG model (not shown in the table) consistently outperforms NaiveRAG, and each ablated variant achieves lower win‑rates than the full model.  
* Removing the high‑level retrieval component (‑High) leads to a noticeable drop in performance across most metrics, especially in the Legal dataset where the overall win‑rate falls to 22.0 % / 78.0 %[C10].  
* Removing the low‑level retrieval component (‑Low) also degrades performance, with the most severe drops in Diversity on the Legal dataset (13.6 % / 86.4 %)[C10].  
* The ‑Origin variant, which omits the original text and relies solely on the graph representation, does **not** suffer large declines; in some cases it even improves (e.g., Agriculture Overall 24.8 % / 75.2 %)[C10].  

Overall, the ablation study shows that the **dual‑level retrieval** (both low‑ and high‑level) is essential for achieving the best comprehensive, diverse, and empowering responses, while the graph‑based indexing alone (‑Origin) remains surprisingly robust.</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 7089.73

Judge latency_ms: 8651.72

Total evaluation latency_ms: 15754.59

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | In every cell the first percentage is the NaiveRAG win rate and the second is the variant’s win rate (both %). The comparisons are **not** direct wins against the full LightRAG model [C9]. |
| ablation_meaning | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | -High (low‑level‑only) – Removing the high‑order retrieval causes a **significant performance decline** ...<br><br>* **‑Low (high‑level‑only)** – Keeping only the high‑level retrieval **improves comprehensiveness** ...<br><br>* **‑Origin (no original text)** – Excluding the original text **does not cause major drops** ...<br><br>Overall, the full LightRAG (hybrid of low‑ and high‑level retrieval with original text) achieves the **most balanced** performance... |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 108 | 600 | 10000 | 1514.72 | stop |
| 2 | answer | medium | 5843 | 5618 | 1499 | 3000 | 10000 | 5399.37 | stop |
| 3 | judge | low | 1951 | 1726 | 217 | 1000 | 10000 | 1141.09 | stop |
| 4 | judge | low | 1952 | 1727 | 292 | 1000 | 10000 | 2230.42 | stop |
| 5 | judge | low | 1963 | 1738 | 313 | 1000 | 10000 | 2093.65 | stop |
| 6 | judge | low | 1963 | 1738 | 225 | 1000 | 10000 | 1774.49 | stop |
| 7 | judge | low | 1939 | 1714 | 87 | 1000 | 10000 | 1412.07 | stop |

### Finalized answer

<pre>The ablation study evaluates three stripped‑down versions of LightRAG – **‑High** (low‑level‑only retrieval), **‑Low** (high‑level‑only retrieval) and **‑Origin** (graph‑based indexing without the original text) – by comparing each variant against the NaiveRAG baseline.  In every cell the first percentage is the NaiveRAG win rate and the second is the variant’s win rate (both %). The comparisons are **not** direct wins against the full LightRAG model [C9].

| Variant | Metric | Agriculture (Naive / Variant) | CS (Naive / Variant) | Legal (Naive / Variant) | Mix (Naive / Variant) |
|---------|--------|------------------------------|----------------------|--------------------------|-----------------------|
| **‑High** (low‑level‑only) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (high‑level‑only) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (no original text) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

**Interpretation of the results**

* **‑High (low‑level‑only)** – Removing the high‑order retrieval causes a **significant performance decline** across almost all datasets and metrics, especially on metrics that require broader context (e.g., Legal overall win rate drops to 22 % for NaiveRAG vs 78 % for the variant) [C10].

* **‑Low (high‑level‑only)** – Keeping only the high‑level retrieval **improves comprehensiveness** (e.g., Legal comprehensiveness 19.2 % / 80.8 %) but **reduces depth**, leading to lower scores on empowerment and overall compared with the full model [C10].

* **‑Origin (graph‑only, no original text)** – Excluding the original text **does not cause major drops**; in several cases it even **outperforms** the baseline (e.g., Agriculture overall 24.8 % / 75.2 %). The authors attribute this to the graph‑based index extracting key information while discarding noisy text [C10].

Overall, the full LightRAG (hybrid of low‑ and high‑level retrieval with original text) achieves the **most balanced** performance, while the ablated variants each exhibit distinct trade‑offs as reflected in the win‑rate tables [C9].</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 7152.73

Judge latency_ms: 6874.47

Total evaluation latency_ms: 14037.47

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | **Ablated versions of LightRAG were evaluated by comparing each variant against the NaiveRAG baseline (the win‑rate columns are “NaiveRAG win % / variant win %”).** The results are shown in Table 2 [C9]. |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 112 | 600 | 10000 | 1661.33 | stop |
| 2 | answer | medium | 5843 | 5618 | 1508 | 3000 | 10000 | 5267.71 | stop |
| 3 | judge | low | 1863 | 1638 | 240 | 1000 | 10000 | 1204.45 | stop |
| 4 | judge | low | 1864 | 1639 | 217 | 1000 | 10000 | 1293.24 | stop |
| 5 | judge | low | 1875 | 1650 | 251 | 1000 | 10000 | 1360.87 | stop |
| 6 | judge | low | 1875 | 1650 | 264 | 1000 | 10000 | 2076.12 | stop |
| 7 | judge | low | 1851 | 1626 | 131 | 1000 | 10000 | 939.80 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG were evaluated by comparing each variant against the NaiveRAG baseline (the win‑rate columns are “NaiveRAG win % / variant win %”).** The results are shown in Table 2 [C9].

| Variant | Metric | Agriculture (NaiveRAG / variant) | CS (NaiveRAG / variant) | Legal (NaiveRAG / variant) | Mix (NaiveRAG / variant) |
|---------|--------|----------------------------------|------------------------|---------------------------|--------------------------|
| **‑High** (high‑level‑only) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
|  | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
|  | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
|  | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (low‑level‑only) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
|  | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
|  | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
|  | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (no original text) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
|  | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
|  | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
|  | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

**Key observations (qualitative description):**  

* The **‑High** (low‑level‑only) variant “removes high‑order retrieval, leading to a significant performance decline across nearly all datasets and metrics” because it focuses excessively on specific entities and lacks breadth [C10].  

* The **‑Low** (high‑level‑only) variant “prioritizes capturing a broader range of content… offering a significant advantage in comprehensiveness… but the trade‑off is reduced depth for detailed answers” [C10].  

* The **‑Origin** variant, which “eliminated the use of original text,” “does not exhibit significant performance declines… and in some cases even shows improvements (e.g., Agriculture and Mix)” [C10].

Overall, all ablated versions still outperform the NaiveRAG baseline (their win‑rate percentages are higher than the NaiveRAG column), but each suffers relative to the full LightRAG model, with the high‑level‑only version showing the greatest drop, the low‑level‑only version excelling in comprehensiveness, and the no‑original‑text version maintaining comparable performance.</pre>


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

Judge latency_ms: 1454.32

Total evaluation latency_ms: 1454.32

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 1454.32 | stop |

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

Judge latency_ms: 865.08

Total evaluation latency_ms: 865.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 865.08 | stop |

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

Judge latency_ms: 836.64

Total evaluation latency_ms: 836.64

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 836.64 | stop |

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

Judge latency_ms: 852.49

Total evaluation latency_ms: 852.49

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 852.49 | stop |

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

Judge latency_ms: 1362.05

Total evaluation latency_ms: 1362.05

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 649 | 424 | 88 | 1000 | 10000 | 1362.05 | stop |

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

Judge latency_ms: 812.82

Total evaluation latency_ms: 812.82

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 663 | 438 | 108 | 1000 | 10000 | 812.82 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
