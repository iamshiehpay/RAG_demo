# Golden Facts evaluation

Created: 2026-10-12T20:28:53.635558+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Label: table-reconstruction-generic-followup

Revision: d6a075e67a6ae48379aa1db6929518e56ac8c4b7

Uncommitted changes: no

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application operations; generic table-reading rules; Levi #4532

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

Ask latency_ms: 5259.49

Judge latency_ms: 7089.22

Total evaluation latency_ms: 12360.50

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *Each cell shows “NaiveRAG win % / variant win %”.*  <br><br>These figures are taken directly from Table 2 in the paper, which reports the performance of the three ablated LightRAG variants (‑High, ‑Low, ‑Origin) against the NaiveRAG baseline across four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall)[C9]. |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 121 | 600 | 10000 | 966.31 | stop |
| 2 | answer | medium | 5784 | 5559 | 963 | 3000 | 10000 | 3835.51 | stop |
| 3 | judge | low | 1491 | 1266 | 281 | 1000 | 10000 | 1818.73 | stop |
| 4 | judge | low | 1492 | 1267 | 191 | 1000 | 10000 | 1685.31 | stop |
| 5 | judge | low | 1503 | 1278 | 193 | 1000 | 10000 | 1072.87 | stop |
| 6 | judge | low | 1503 | 1278 | 186 | 1000 | 10000 | 1081.82 | stop |
| 7 | judge | low | 1479 | 1254 | 100 | 1000 | 10000 | 1430.48 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (compared against NaiveRAG)**  

| Ablated variant | Metric | Agriculture % (NaiveRAG / variant) | CS % (NaiveRAG / variant) | Legal % (NaiveRAG / variant) | Mix % (NaiveRAG / variant) |
|-----------------|--------|-----------------------------------|--------------------------|-----------------------------|---------------------------|
| **‑High** (removes high‑order retrieval) | Comprehensiveness | 34.8 / 65.2 | 42.8 / 57.2 | 23.6 / 76.4 | 40.4 / 59.6 |
| | Diversity | 27.2 / 72.8 | 36.8 / 63.2 | 16.8 / 83.2 | 36.0 / 64.0 |
| | Empowerment | 36.0 / 64.0 | 42.4 / 57.6 | 22.8 / 77.2 | 47.6 / 52.4 |
| | Overall | 35.2 / 64.8 | 44.0 / 56.0 | 22.0 / 78.0 | 42.4 / 57.6 |
| **‑Low** (removes low‑level retrieval) | Comprehensiveness | 36.0 / 64.0 | 43.2 / 56.8 | 19.2 / 80.8 | 36.0 / 64.0 |
| | Diversity | 28.0 / 72.0 | 39.6 / 60.4 | 13.6 / 86.4 | 33.2 / 66.8 |
| | Empowerment | 34.8 / 65.2 | 42.8 / 57.2 | 16.4 / 83.6 | 35.2 / 64.8 |
| | Overall | 34.8 / 65.2 | 43.6 / 56.4 | 18.8 / 81.2 | 35.2 / 64.8 |
| **‑Origin** (removes original‑text retrieval) | Comprehensiveness | 24.8 / 75.2 | 39.2 / 60.8 | 16.4 / 83.6 | 44.4 / 55.6 |
| | Diversity | 26.4 / 73.6 | 44.8 / 55.2 | 14.4 / 85.6 | 25.6 / 74.4 |
| | Empowerment | 32.0 / 68.0 | 43.2 / 56.8 | 17.2 / 82.8 | 45.2 / 54.8 |
| | Overall | 25.6 / 74.4 | 39.2 / 60.8 | 15.6 / 84.4 | 44.4 / 55.6 |

*Each cell shows “NaiveRAG win % / variant win %”.*  

These figures are taken directly from Table 2 in the paper, which reports the performance of the three ablated LightRAG variants (‑High, ‑Low, ‑Origin) against the NaiveRAG baseline across four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall)[C9].</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 6727.07

Judge latency_ms: 7963.78

Total evaluation latency_ms: 14698.66

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *All percentages are “NaiveRAG win rate / variant win rate” as reported in Table 2 of the paper*[C9]. |
| ablation_meaning | judge | FAIL | Required claim not asserted |  |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 121 | 600 | 10000 | 1498.79 | stop |
| 2 | answer | medium | 5784 | 5559 | 1346 | 3000 | 10000 | 5039.27 | stop |
| 3 | judge | low | 1783 | 1558 | 190 | 1000 | 10000 | 1554.73 | stop |
| 4 | judge | low | 1784 | 1559 | 208 | 1000 | 10000 | 1190.72 | stop |
| 5 | judge | low | 1795 | 1570 | 454 | 1000 | 10000 | 2298.65 | stop |
| 6 | judge | low | 1795 | 1570 | 288 | 1000 | 10000 | 1521.43 | stop |
| 7 | judge | low | 1771 | 1546 | 95 | 1000 | 10000 | 1398.25 | stop |

### Finalized answer

<pre>**Ablation results (compared with NaiveRAG as the baseline)**  

| Variant (compared to NaiveRAG) | Metric | Agriculture % (baseline / variant) | CS % (baseline / variant) | Legal % (baseline / variant) | Mix % (baseline / variant) |
|---|---|---|---|---|---|
| **Full LightRAG** (NaiveRAG / LightRAG) | Comprehensiveness | 32.4 / 67.6 | 38.4 / 61.6 | 16.4 / 83.6 | 38.8 / 61.2 |
|  | Diversity | 23.6 / 76.4 | 38.0 / 62.0 | 13.6 / 86.4 | 32.4 / 67.6 |
|  | Empowerment | 32.4 / 67.6 | 38.8 / 61.2 | 16.4 / 83.6 | 42.8 / 57.2 |
|  | Overall | 32.4 / 67.6 | 38.8 / 61.2 | 15.2 / 84.8 | 40.0 / 60.0 |
| **‑High** (removes high‑level retrieval) | Comprehensiveness | 34.8 / 65.2 | 42.8 / 57.2 | 23.6 / 76.4 | 40.4 / 59.6 |
|  | Diversity | 27.2 / 72.8 | 36.8 / 63.2 | 16.8 / 83.2 | 36.0 / 64.0 |
|  | Empowerment | 36.0 / 64.0 | 42.4 / 57.6 | 22.8 / 77.2 | 47.6 / 52.4 |
|  | Overall | 35.2 / 64.8 | 44.0 / 56.0 | 22.0 / 78.0 | 42.4 / 57.6 |
| **‑Low** (removes low‑level retrieval) | Comprehensiveness | 36.0 / 64.0 | 43.2 / 56.8 | 19.2 / 80.8 | 36.0 / 64.0 |
|  | Diversity | 28.0 / 72.0 | 39.6 / 60.4 | 13.6 / 86.4 | 33.2 / 66.8 |
|  | Empowerment | 34.8 / 65.2 | 42.8 / 57.2 | 16.4 / 83.6 | 35.2 / 64.8 |
|  | Overall | 34.8 / 65.2 | 43.6 / 56.4 | 18.8 / 81.2 | 35.2 / 64.8 |
| **‑Origin** (removes original text) | Comprehensiveness | 24.8 / 75.2 | 39.2 / 60.8 | 16.4 / 83.6 | 44.4 / 55.6 |
|  | Diversity | 26.4 / 73.6 | 44.8 / 55.2 | 14.4 / 85.6 | 25.6 / 74.4 |
|  | Empowerment | 32.0 / 68.0 | 43.2 / 56.8 | 17.2 / 82.8 | 45.2 / 54.8 |
|  | Overall | 25.6 / 74.4 | 39.2 / 60.8 | 15.6 / 84.4 | 44.4 / 55.6 |

*All percentages are “NaiveRAG win rate / variant win rate” as reported in Table 2 of the paper*[C9].  

**Key observations (from the same source):**  
- The full LightRAG model consistently outperforms NaiveRAG across all metrics and datasets.  
- Removing the high‑level component (‑High) hurts performance, especially on the Legal dataset.  
- Removing the low‑level component (‑Low) also degrades results, though the drop is less severe for comprehensiveness.  
- Excluding the original text (‑Origin) does not cause major declines; in some cases (e.g., Agriculture and Mix) it even improves certain metrics.  

These figures constitute the reported performance of the ablated LightRAG variants.</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 6026.25

Judge latency_ms: 7818.34

Total evaluation latency_ms: 13859.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C9 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *All percentages are “NaiveRAG win rate / variant win rate” as reported in Table 2 of the paper*[C9]. |
| ablation_meaning | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | **‑High** (high‑level‑only retrieval) ... **‑Low** (low‑level‑only retrieval) ... **‑Origin** (no original‑text retrieval) ... *The full LightRAG system (un‑abated) achieves the highest win rates across all metrics and datasets* |
| mix_low_overall | judge | FAIL | Required claim not asserted |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted |  |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | * The full LightRAG system (un‑abated) achieves the highest win rates across all metrics and datasets (e.g., Overall = 67.6 % on Agriculture, 61.6 % on CS, 84.8 % on Legal, 60.0 % on Mix)[C9]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 121 | 600 | 10000 | 927.31 | stop |
| 2 | answer | medium | 5784 | 5559 | 1384 | 3000 | 10000 | 4793.57 | stop |
| 3 | judge | low | 1868 | 1643 | 186 | 1000 | 10000 | 1588.45 | stop |
| 4 | judge | low | 1869 | 1644 | 219 | 1000 | 10000 | 1003.15 | stop |
| 5 | judge | low | 1880 | 1655 | 351 | 1000 | 10000 | 1710.19 | stop |
| 6 | judge | low | 1880 | 1655 | 353 | 1000 | 10000 | 2466.26 | stop |
| 7 | judge | low | 1856 | 1631 | 222 | 1000 | 10000 | 1050.29 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (compared against NaiveRAG)**  

| Variant | Metric | Agriculture (NaiveRAG % / Variant %) | CS (NaiveRAG % / Variant %) | Legal (NaiveRAG % / Variant %) | Mix (NaiveRAG % / Variant %) |
|---------|--------|--------------------------------------|----------------------------|--------------------------------|------------------------------|
| **‑High** (high‑level‑only retrieval) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
|  | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
|  | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
|  | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (low‑level‑only retrieval) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
|  | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
|  | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
|  | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (no original‑text retrieval) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
|  | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
|  | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
|  | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

*All percentages are “NaiveRAG win rate / variant win rate” as reported in Table 2 of the paper*[C9].  

**Key observations from the ablation study**  

* The full LightRAG system (un‑abated) achieves the highest win rates across all metrics and datasets (e.g., Overall = 67.6 % on Agriculture, 61.6 % on CS, 84.8 % on Legal, 60.0 % on Mix)[C9].  
* Removing the high‑level retrieval component (‑High) leads to a noticeable drop in performance, especially on the Legal dataset where Overall falls to 78.0 % from 84.8 % (full)[C9].  
* Removing the low‑level retrieval component (‑Low) also degrades performance, with the most pronounced loss on Legal Overall (81.2 % vs. 84.8 % full)[C9].  
* The ‑Origin variant, which omits original‑text retrieval, still retains strong performance (e.g., Legal Overall = 84.4 % vs. 84.8 % full), indicating that the graph‑based index alone provides sufficient context[C9][C10].  </pre>
