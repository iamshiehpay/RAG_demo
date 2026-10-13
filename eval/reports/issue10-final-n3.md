# Golden Facts evaluation

Created: 2026-10-13T08:10:35.588433+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 597db375a5b3aa59cfa5ac0ab57891198134385e

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-e059ebb4d45dea7be844478cf38173ef74ad27c39e91240c47f961ed19c481dd

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | required_source_citation | events | 3/3 (100.0%) |
| SECOND_NUMBER | question_type | events | 3/3 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/3 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 3/3 (100.0%) |
| SECOND_SUMMARY | question_type | events | 3/3 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/3 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 856 | 631 | 119 | 1200 | 10000 | 1846.15 | stop |
| 2 | section_summary | low | 922 | 697 | 166 | 1200 | 10000 | 1949.09 | stop |
| 3 | section_summary | low | 2098 | 1873 | 380 | 1200 | 10000 | 2208.38 | stop |
| 4 | section_summary | low | 2810 | 2585 | 785 | 1200 | 10000 | 4241.53 | stop |
| 5 | section_summary | low | 2839 | 2614 | 1012 | 1200 | 10000 | 4571.04 | stop |
| 6 | section_summary | low | 1736 | 1511 | 439 | 1200 | 10000 | 2767.13 | stop |
| 7 | section_summary | low | 2872 | 2647 | 147 | 1200 | 10000 | 1140.66 | stop |
| 8 | section_summary | low | 729 | 504 | 77 | 1200 | 10000 | 837.24 | stop |
| 9 | section_summary | low | 1153 | 928 | 239 | 1200 | 10000 | 1751.84 | stop |
| 10 | section_summary | low | 2901 | 2676 | 218 | 1200 | 10000 | 1361.76 | stop |
| 11 | section_summary | low | 806 | 581 | 189 | 1200 | 10000 | 1081.29 | stop |
| 12 | section_summary | low | 713 | 488 | 126 | 1200 | 10000 | 876.94 | stop |
| 13 | section_summary | low | 1534 | 1309 | 322 | 1200 | 10000 | 1761.84 | stop |
| 14 | section_summary | low | 2473 | 2248 | 543 | 1200 | 10000 | 2381.36 | stop |
| 15 | section_summary | low | 1404 | 1179 | 301 | 1200 | 10000 | 2001.73 | stop |
| 16 | section_summary | low | 790 | 565 | 186 | 1200 | 10000 | 1964.27 | stop |
| 17 | section_summary | low | 2535 | 2310 | 194 | 1200 | 10000 | 1390.10 | stop |
| 18 | section_summary | low | 1543 | 1318 | 295 | 1200 | 10000 | 1684.15 | stop |
| 19 | section_summary | low | 1067 | 842 | 161 | 1200 | 10000 | 1039.02 | stop |
| 20 | section_summary | low | 790 | 565 | 200 | 1200 | 10000 | 1118.77 | stop |
| 21 | section_summary | low | 953 | 728 | 143 | 1200 | 10000 | 995.03 | stop |
| 22 | section_summary | low | 905 | 680 | 145 | 1200 | 10000 | 989.99 | stop |
| 23 | section_summary | low | 1326 | 1101 | 307 | 1200 | 10000 | 1594.21 | stop |
| 24 | section_summary | low | 1701 | 1476 | 354 | 1200 | 10000 | 1822.88 | stop |
| 25 | section_summary | low | 2930 | 2705 | 595 | 1200 | 10000 | 3329.47 | stop |
| 26 | section_summary | low | 1729 | 1504 | 267 | 1200 | 10000 | 2054.16 | stop |
| 27 | section_summary | low | 923 | 698 | 164 | 1200 | 10000 | 1165.61 | stop |
| 28 | section_summary | low | 2992 | 2767 | 230 | 1200 | 10000 | 1571.65 | stop |
| 29 | section_summary | low | 2792 | 2567 | 1052 | 1200 | 10000 | 4963.36 | stop |
| 30 | section_summary | low | 5118 | 4893 | 1200 | 1200 | 10000 | 6129.61 | length |
| 31 | section_summary | low | 7314 | 7047 | 447 | 1200 | 10000 | 2757.99 | stop |
| 32 | section_summary | low | 2854 | 2629 | 227 | 1200 | 10000 | 1651.60 | stop |
| 33 | section_summary | low | 2589 | 2364 | 718 | 1200 | 10000 | 4134.23 | stop |
| 34 | section_summary | low | 5180 | 4955 | 413 | 1200 | 10000 | 2921.66 | stop |
| 35 | section_summary | low | 4385 | 4118 | 332 | 1200 | 10000 | 2753.46 | stop |
| 36 | section_summary | low | 2651 | 2426 | 229 | 1200 | 10000 | 1844.95 | stop |
| 37 | section_summary | low | 4425 | 4158 | 185 | 1200 | 10000 | 1616.23 | stop |
| 38 | section_summary | low | 6217 | 5950 | 247 | 1200 | 10000 | 1666.71 | stop |
| 39 | section_summary | low | 6979 | 6712 | 177 | 1200 | 10000 | 1220.19 | stop |
| 40 | section_summary | low | 3811 | 3586 | 1180 | 1200 | 10000 | 6033.50 | stop |
| 41 | section_summary | low | 2719 | 2494 | 922 | 1200 | 10000 | 4251.59 | stop |
| 42 | section_summary | low | 2407 | 2140 | 537 | 1200 | 10000 | 3356.86 | stop |
| 43 | section_summary | low | 7019 | 6752 | 269 | 1200 | 10000 | 1998.54 | stop |
| 44 | section_summary | low | 3873 | 3648 | 290 | 1200 | 10000 | 1754.56 | stop |
| 45 | section_summary | low | 2781 | 2556 | 211 | 1200 | 10000 | 1665.09 | stop |
| 46 | section_summary | low | 4711 | 4444 | 149 | 1200 | 10000 | 1063.59 | stop |
| 47 | section_summary | low | 2447 | 2180 | 266 | 1200 | 10000 | 1816.61 | stop |
| 48 | section_summary | low | 6523 | 6256 | 116 | 1200 | 10000 | 1113.49 | stop |
| 49 | section_summary | low | 6574 | 6307 | 604 | 1200 | 10000 | 2763.46 | stop |
| 50 | section_summary | low | 2444 | 2177 | 243 | 1200 | 10000 | 1388.65 | stop |
| 51 | section_summary | low | 6521 | 6254 | 127 | 1200 | 10000 | 1127.33 | stop |
| 52 | section_summary | low | 5596 | 5329 | 203 | 1200 | 10000 | 1412.19 | stop |
| 53 | section_summary | low | 6614 | 6347 | 566 | 1200 | 10000 | 2832.00 | stop |
| 54 | section_summary | low | 6871 | 6604 | 307 | 1200 | 10000 | 1783.45 | stop |
| 55 | section_summary | low | 6825 | 6558 | 370 | 1200 | 10000 | 1592.20 | stop |
| 56 | section_summary | low | 6911 | 6644 | 183 | 1200 | 10000 | 1430.98 | stop |
| 57 | section_summary | low | 5570 | 5303 | 151 | 1200 | 10000 | 1231.29 | stop |
| 58 | section_summary | low | 6865 | 6598 | 553 | 1200 | 10000 | 2448.70 | stop |
| 59 | section_summary | low | 4942 | 4675 | 143 | 1200 | 10000 | 1239.73 | stop |
| 60 | section_summary | low | 6841 | 6574 | 426 | 1200 | 10000 | 1658.23 | stop |
| 61 | section_summary | low | 5427 | 5160 | 169 | 1200 | 10000 | 1103.61 | stop |
| 62 | section_summary | low | 5570 | 5303 | 122 | 1200 | 10000 | 1134.79 | stop |
| 63 | section_summary | low | 6881 | 6614 | 480 | 1200 | 10000 | 2479.90 | stop |
| 64 | section_summary | low | 6551 | 6284 | 183 | 1200 | 10000 | 1344.39 | stop |
| 65 | section_summary | low | 6875 | 6608 | 339 | 1200 | 10000 | 1742.13 | stop |
| 66 | section_summary | low | 6591 | 6324 | 221 | 1200 | 10000 | 1443.33 | stop |
| 67 | section_summary | low | 5586 | 5319 | 160 | 1200 | 10000 | 1260.88 | stop |
| 68 | section_summary | low | 6741 | 6474 | 675 | 1200 | 10000 | 3051.41 | stop |
| 69 | section_summary | low | 7207 | 6940 | 245 | 1200 | 10000 | 1548.88 | stop |
| 70 | section_summary | low | 6854 | 6587 | 452 | 1200 | 10000 | 2563.87 | stop |
| 71 | section_summary | low | 8546 | 8279 | 768 | 1200 | 10000 | 3499.07 | stop |
| 72 | section_summary | low | 7357 | 7090 | 467 | 1200 | 10000 | 2102.64 | stop |
| 73 | section_summary | low | 6817 | 6550 | 764 | 1200 | 10000 | 3279.45 | stop |
| 74 | section_summary | low | 2304 | 2037 | 630 | 1200 | 10000 | 2303.60 | stop |
| 75 | section_summary | low | 4240 | 3973 | 823 | 1200 | 10000 | 3656.09 | stop |
| 76 | section_summary | low | 8091 | 7824 | 266 | 1200 | 10000 | 1701.17 | stop |
| 77 | section_summary | low | 8125 | 7858 | 140 | 1200 | 10000 | 1102.23 | stop |
| 78 | section_summary | low | 8207 | 7940 | 298 | 1200 | 10000 | 1637.05 | stop |
| 79 | section_summary | low | 2355 | 2088 | 292 | 1200 | 10000 | 1284.58 | stop |
| 80 | section_summary | low | 7459 | 7192 | 476 | 1200 | 10000 | 2352.47 | stop |
| 81 | section_summary | low | 7493 | 7226 | 204 | 1200 | 10000 | 1365.06 | stop |
| 82 | section_summary | low | 4416 | 4149 | 647 | 1200 | 10000 | 2643.51 | stop |
| 83 | section_summary | low | 2141 | 1874 | 129 | 1200 | 10000 | 921.34 | stop |
| 84 | section_summary | low | 4456 | 4189 | 506 | 1200 | 10000 | 2490.54 | stop |
| 85 | section_summary | low | 4450 | 4183 | 334 | 1200 | 10000 | 1592.68 | stop |
| 86 | group_summary | low | 6253 | 6028 | 2500 | 2500 | 10000 | 6969.77 | length |
| 87 | group_summary | low | 6315 | 6090 | 310 | 2500 | 10000 | 1675.45 | stop |
| 88 | group_summary | low | 2895 | 2670 | 950 | 2500 | 10000 | 3813.66 | stop |
| 89 | document_summary | low | 2204 | 1979 | 959 | 2500 | 10000 | 2926.14 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 3516.89

Judge latency_ms: 1724.73

Total evaluation latency_ms: 5248.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the agreement comparison (Table 9), the “All” setting evaluated 447 criterion‑paper pairs and achieved an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  <br>When restricting to cases where the LLM reported that information was found (“InfoFound”), the evaluation count dropped to 304 pairs, the accuracy decreased to 0.951 (‑0.015), while the positive‑class F1 remained unchanged at 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 197 | 600 | 10000 | 1073.41 | stop |
| 2 | answer | medium | 5165 | 4940 | 408 | 3000 | 10000 | 2234.13 | stop |
| 3 | judge | low | 973 | 748 | 165 | 1000 | 10000 | 896.18 | stop |
| 4 | judge | low | 858 | 633 | 96 | 1000 | 10000 | 828.55 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation [C4].  

In the agreement comparison (Table 9), the “All” setting evaluated 447 criterion‑paper pairs and achieved an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  
When restricting to cases where the LLM reported that information was found (“InfoFound”), the evaluation count dropped to 304 pairs, the accuracy decreased to 0.951 (‑0.015), while the positive‑class F1 remained unchanged at 0.762 [C8].</pre>

## SECOND_NUMBER — repetition 2

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: [&#x27;model papers manually annotated expert validation count&#x27;, &#x27;InfoFound vs All overall accuracy and positive-class F1&#x27;, &#x27;evaluation counts InfoFound All&#x27;]

Ask latency_ms: 5238.46

Judge latency_ms: 2160.09

Total evaluation latency_ms: 7407.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C5 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | Three model papers were manually annotated for expert validation — the three “expert‑annotated papers” referenced in the study [C2].  <br><br>When the “InfoFound” filter is applied, the overall accuracy drops from 0.966 (All) to 0.951 (InfoFound), while the positive‑class F1 score remains unchanged at 0.762 [C5].  <br><br>Evaluation counts:  <br>* **All** — N = 447 [C5]  <br>* **InfoFound** — N = 304 [C5] |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 248 | 600 | 10000 | 1449.37 | stop |
| 2 | answer | medium | 3192 | 2967 | 545 | 3000 | 10000 | 2455.37 | stop |
| 3 | judge | low | 972 | 747 | 358 | 1000 | 10000 | 1344.46 | stop |
| 4 | judge | low | 858 | 633 | 105 | 1000 | 10000 | 815.63 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — the three “expert‑annotated papers” referenced in the study [C2].  

When the “InfoFound” filter is applied, the overall accuracy drops from 0.966 (All) to 0.951 (InfoFound), while the positive‑class F1 score remains unchanged at 0.762 [C5].  

Evaluation counts:  
* **All** — N = 447 [C5]  
* **InfoFound** — N = 304 [C5]</pre>

## SECOND_NUMBER — repetition 3

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 3231.20

Judge latency_ms: 1483.84

Total evaluation latency_ms: 4718.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the agreement comparison (Table 9), the “All” setting uses 447 criterion‑paper evaluations and yields an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  When restricting to cases where the LLM reported that information was found (“InfoFound”), the evaluation count drops to 304, the accuracy falls to 0.951 (a decrease of 0.015), while the positive‑class F1 remains unchanged at 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 127 | 600 | 10000 | 821.99 | stop |
| 2 | answer | medium | 5165 | 4940 | 385 | 3000 | 10000 | 1759.29 | stop |
| 3 | judge | low | 984 | 759 | 161 | 1000 | 10000 | 781.78 | stop |
| 4 | judge | low | 869 | 644 | 92 | 1000 | 10000 | 702.07 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation – two were annotated before the automated run and one after it [C4].  

In the agreement comparison (Table 9), the “All” setting uses 447 criterion‑paper evaluations and yields an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  
When restricting to cases where the LLM reported that information was found (“InfoFound”), the evaluation count drops to 304, the accuracy falls to 0.951 (a decrease of 0.015), while the positive‑class F1 remains unchanged at 0.762 [C8].  </pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 6215.56

Judge latency_ms: 682.69

Total evaluation latency_ms: 6905.40

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 155 | 600 | 10000 | 924.02 | stop |
| 2 | answer | medium | 2505 | 2280 | 1470 | 3000 | 10000 | 5265.07 | stop |
| 3 | judge | low | 1882 | 1657 | 72 | 1000 | 10000 | 682.69 | stop |

### Finalized answer

<pre>The paper is motivated by the rapid emergence of **robotic foundation models (RFMs)**—highly adaptable, data‑driven systems that combine multimodal proprioceptive, exteroceptive and natural‑language inputs to generate low‑level actions, plans or trajectories for many robot platforms, with Vision‑Language‑Action models highlighted as a key sub‑category[S1].  Because industry requires concrete guarantees of **adaptability, safety, robustness, precision, real‑time performance, cost‑effectiveness, explainability, sensor‑fusion, benchmarking and data efficiency**, the authors built a systematic review (1 025 works plus 125 industrial‑implication articles) and distilled eleven domain‑agnostic expectations into a **149‑criterion catalogue** for assessing industrial readiness[S1].

**Assessment method** – The authors applied the catalogue to **324 manipulation‑capable RFMs** by generating binary decisions with a GPT‑5.1 pipeline (48 276 decisions) and then converting them into proportional scores per criterion (rounded to two decimals)[S2].  The pipeline’s outputs were validated against **28 expert judgments**, achieving **96.6 % accuracy**, which defines the scope of expert validation for the study[S1].  Scores were aggregated into total ratings and per‑implication (I1–I11) values, and breadth (1+‑Coverage) versus depth (ACC) metrics were computed for the whole set and the Top‑50 subset[S2].

**Main findings** –  
* The **top‑rated model** is “Gemini Robotics 1.5” (total 0.12), excelling in multi‑hardware and configuration adaptability (I1 = 0.44) and showing modest data‑efficiency (I11 = 0.09)[S2].  
* “HAMSTER” attains the highest benchmarking/evaluation score (I10 = 0.23) among the top‑five[S2].  
* Across all 324 RFMs, **adaptability/flexibility (I1), benchmarking/evaluation (I10) and data efficiency (I11)** receive the highest breadth (≈0.75) but **depth remains below 0.10 for every implication**, indicating shallow fulfillment of criteria[S2].  
* In the Top‑50, depth improves only modestly (≈0.23)[S2].  
* The ten most frequently fulfilled criteria cluster in I1, I10 and I11, while **explicitness is low** (e.g., Multi‑Task Generalisation = 0.2812)[S2].  
* **Evidence‑fulfilment gaps are large** (gc &gt; 0.8), especially for safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7)[S2].  
* Overall, the field shows rapid **breadth expansion** but **early industrial maturity**, with top models covering only about **0.11–0.12 of the 149 criteria** and strong performance limited to isolated implications such as adaptability[S2].

**Limitations** – The assessment reveals that **most criteria are discussed but rarely satisfied**, leading to low depth scores and large gaps, which the authors cite as evidence of limited and uneven maturity[S2].  The structural reconstruction of tables could not be reliably recovered, so some detailed row/column associations are missing from the extracted summary[S1].  Moreover, because the scoring relies on **reported model capabilities**, any **unreported features** (e.g., safety mechanisms, real‑time guarantees) cannot be captured and therefore depress the model’s scores, inflating the apparent gaps[S2].  The expert validation is confined to the **28 expert judgments** used to benchmark the LLM‑based pipeline, so the accuracy claim (96.6 %) applies only within that limited expert sample[S1].

**Purpose of each appendix** –  
* **Appendix A** (Table A1) lists the **55 surveyed publications** on vision‑language‑action models, foundation models for robot learning, autonomous driving, robotic language grounding and related topics, providing the literature background for the review[S2].  
* **Appendix B** (Table B2) presents the **eleven ASQS queries** employed to retrieve the RFM‑related corpus, documenting the systematic search strategy[S2].  
* **Appendix C** (Table C4) defines the **industrial implication criteria** (e.g., I1 – Multi‑Hardware and Configuration Adaptability, I11 – Data Efficiency &amp; Finetuning), establishing the detailed rubric used for scoring[S2].  
* **Appendix D** (Table D5) supplies the **proportional industrial applicability ratings** for all 324 RFMs with manipulation capabilities, including example entries such as Gemini Robotics 1.5 and Collab VLA, enabling transparent inspection of the raw evaluation data[S2].</pre>

## SECOND_SUMMARY — repetition 2

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 17569.46

Judge latency_ms: 795.13

Total evaluation latency_ms: 18365.60

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 153 | 600 | 10000 | 1194.45 | stop |
| 2 | answer | medium | 2505 | 2280 | 1132 | 3000 | 10000 | 16359.78 | stop |
| 3 | judge | low | 1428 | 1203 | 72 | 1000 | 10000 | 795.13 | stop |

### Finalized answer

<pre>The document is motivated by the need to clarify what robotic foundation models (RFMs) are—a class of highly adaptable, data‑driven systems that ingest multimodal proprioceptive, exteroceptive and natural‑language inputs and output low‑level actions, plans or trajectories—and to evaluate how ready these models are for industrial use, given that current expectations (e.g., adaptability, safety, real‑time performance, cost‑effectiveness) are only partially met by existing work[S1].  

To assess industrial readiness, the authors built three corpora (Main, Implications, Further) containing 1 025 relevant works plus 125 core industrial‑implication articles, distilled eleven domain‑agnostic expectations into 517 attribute‑level concerns and a 149‑criterion catalogue, then applied this framework to 324 manipulation‑capable RFMs using 48 276 GPT‑5.1‑generated binary decisions that were validated against 28 expert judgments with 96.6 % accuracy[S1].  

The main findings show that even the highest‑rated models (e.g., Gemini Robotics 1.5 with a total score of 0.12, strong I1 = 0.44, modest I11 = 0.09) satisfy only a small fraction of the catalogue (≈0.11–0.12 of 149 criteria) and excel mainly in adaptability, benchmarking/evaluation and data efficiency, while lagging sharply in safety/compliance, human‑robot interaction, real‑time performance and cost‑effectiveness[S2].  Across all 324 RFMs the breadth of coverage for I1, I10 and I11 is high (≈0.75) but depth remains below 0.10 for every implication, and evidence‑fulfilment gaps are large (gc &gt; 0.8), indicating that criteria are widely discussed but rarely satisfied, especially for deployment‑related implications[S2].  

A key limitation is that the assessment relies on reported capabilities; unreported model features cannot be captured by the LLM‑generated binary decisions and therefore lead to under‑estimation of a model’s true industrial applicability[S2].  Moreover, expert validation is confined to 28 judgments, so the reported 96.6 % accuracy reflects a limited validation scope rather than exhaustive expert coverage[S1].  

Appendix A lists the 55 surveyed publications on vision‑language‑action models, foundation models for robot learning and related topics, providing the literature background[S2].  Appendix B details the eleven ASQS queries used to retrieve the RFM‑related corpus, documenting the systematic search strategy[S2].  Appendix C presents the full industrial implication criteria catalogue (e.g., definitions of I1 and I11), establishing the measurement framework[S2].  Appendix D supplies the proportional industrial applicability ratings for all 324 RFMs, enabling detailed per‑model analysis[S2].  </pre>

## SECOND_SUMMARY — repetition 3

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 7767.77

Judge latency_ms: 834.71

Total evaluation latency_ms: 8605.56

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 112 | 600 | 10000 | 1416.33 | stop |
| 2 | answer | medium | 2505 | 2280 | 1146 | 3000 | 10000 | 6312.60 | stop |
| 3 | judge | low | 1554 | 1329 | 72 | 1000 | 10000 | 834.71 | stop |

### Finalized answer

<pre>The document is motivated by the rapid emergence of **robotic foundation models (RFMs)**—highly adaptable, multimodal systems that can generate low‑level actions, plans or trajectories for many robot types—and by the need to determine whether these models are ready for industrial deployment, given eleven domain‑agnostic expectations such as adaptability, safety, real‑time performance and cost‑effectiveness that were distilled into a 149‑criterion catalogue for assessing industrial readiness[S1].  

To assess the models, the authors applied a **systematic, LLM‑based evaluation pipeline**: 324 manipulation‑capable RFMs were scored against each of the 149 criteria, producing proportional scores (rounded to two decimals) for every implication (e.g., I1, I10, I11)[S2]. The binary decisions underlying these scores were generated by GPT‑5.1 and **validated against 28 expert judgments**, achieving 96.6 % accuracy[S1]. Results were aggregated as total ratings (e.g., Gemini Robotics 1.5 = 0.12) and as per‑implication breadth (coverage) and depth (ACC) metrics[S2].  

**Main findings** show that even the highest‑rated models satisfy only a small fraction of the catalogue (≈0.11–0.12 of the criteria) and excel mainly in adaptability (I1) and data‑efficiency / benchmarking (I10, I11), while **safety, human‑robot interaction, real‑time performance and cost‑effectiveness remain poorly addressed** (depth &lt; 0.10 for all implications)[S2]. Breadth is relatively high for I1, I10 and I11 (≈0.75), but evidence‑fulfilment gaps are large (gc &gt; 0.8), indicating that many criteria are discussed but rarely met[S2]. The authors conclude that the field is expanding in breadth but remains early in industrial maturity, and that closing the identified gaps through layered architectures, edge‑ready inference and structured evaluation is essential for achieving reliable, industry‑grade RFMs[S2].  

A key **limitation** is that the assessment can only incorporate capabilities that are **explicitly reported** in the source literature; unreported or undocumented model features are therefore omitted from the scoring, potentially under‑representing a model’s true industrial suitability[S1]. Consequently, the **scope of expert validation** is confined to the 28 expert judgments used to verify the LLM‑generated binary decisions, which, while highly accurate, cannot compensate for missing information in the original reports[S1].  

The document’s appendices serve distinct supporting roles:  

* **Appendix A (Table A1)** enumerates 55 surveyed publications on vision‑language‑action and related foundation models, providing the **related‑works background**[S2].  
* **Appendix B (Table B2)** lists the eleven ASQS queries employed to retrieve the RFM‑related corpus, documenting the **literature‑search methodology**[S2].  
* **Appendix C (Table C4)** defines each industrial implication (e.g., I1, I11) and its sub‑criteria, forming the **criteria catalogue** used for evaluation[S2].  
* **Appendix D (Table D5)** presents the full proportional applicability ratings for all 324 RFMs, supplying the **comprehensive data set** underlying the analysis[S2].  </pre>
