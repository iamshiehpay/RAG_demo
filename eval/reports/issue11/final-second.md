# Golden Facts evaluation

Created: 2026-10-13T11:44:37.952319+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 3

Result: FAIL

Functional operations: PASS (separate from D05 semantic rates)

Call audit: {&quot;budget_violations&quot;: 0, &quot;calls&quot;: 107, &quot;length_attempts&quot;: [{&quot;call_type&quot;: &quot;section_summary&quot;, &quot;num_predict&quot;: 1200, &quot;think&quot;: &quot;low&quot;}, {&quot;call_type&quot;: &quot;section_summary&quot;, &quot;num_predict&quot;: 1200, &quot;think&quot;: &quot;low&quot;}, {&quot;call_type&quot;: &quot;judge&quot;, &quot;num_predict&quot;: 1000, &quot;think&quot;: &quot;low&quot;}], &quot;maximum_estimated_prompt_plus_reservation&quot;: 9847, &quot;maximum_reported_prompt_plus_reservation&quot;: 9580, &quot;missing_reported_prompt_counts&quot;: 0, &quot;router_answer_length_attempts&quot;: 0}

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 7cf91851f9f86527d69c95910f9eadd58cf7b357

Uncommitted changes: yes

Pipeline version: ingest-v2-06fcd637e034ab2a889dbe6ec9bdadac23d3d44977aca74f1e9890287d31876b

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Created: 2026-10-13T11:44:37.950131+00:00

Label: issue11-final-second

D05: Report raw rates/causes; semantic defects do not block delivery.

Effective settings: {&quot;answer_think&quot;: &quot;medium&quot;, &quot;bm25_weight&quot;: 0.0, &quot;chunk_token_target&quot;: 500, &quot;lookup_top_k&quot;: 5, &quot;sub_query_top_k&quot;: 2, &quot;summary_concurrency&quot;: 4, &quot;synthesis_top_k&quot;: 3}

Peak guarded calls by type: {&quot;section_summary&quot;: 4, &quot;group_summary&quot;: 1, &quot;document_summary&quot;: 1, &quot;router&quot;: 1, &quot;answer&quot;: 1, &quot;judge&quot;: 1}

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | required_source_citation | events | 2/3 (66.7%) |
| SECOND_NUMBER | question_type | events | 3/3 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/3 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 3/3 (100.0%) |
| SECOND_SUMMARY | question_type | events | 3/3 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 1/3 (33.3%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 854 | 629 | 127 | 1200 | 10000 | 1272.62 | stop |
| 2 | section_summary | low | 922 | 697 | 201 | 1200 | 10000 | 1535.78 | stop |
| 3 | section_summary | low | 1734 | 1509 | 390 | 1200 | 10000 | 2115.75 | stop |
| 4 | section_summary | low | 2835 | 2610 | 697 | 1200 | 10000 | 3504.77 | stop |
| 5 | section_summary | low | 2094 | 1869 | 419 | 1200 | 10000 | 2299.08 | stop |
| 6 | section_summary | low | 2804 | 2579 | 893 | 1200 | 10000 | 4119.25 | stop |
| 7 | section_summary | low | 729 | 504 | 67 | 1200 | 10000 | 710.61 | stop |
| 8 | section_summary | low | 2897 | 2672 | 164 | 1200 | 10000 | 1169.00 | stop |
| 9 | section_summary | low | 1151 | 926 | 247 | 1200 | 10000 | 1302.04 | stop |
| 10 | section_summary | low | 806 | 581 | 86 | 1200 | 10000 | 759.56 | stop |
| 11 | section_summary | low | 2866 | 2641 | 215 | 1200 | 10000 | 1368.66 | stop |
| 12 | section_summary | low | 713 | 488 | 134 | 1200 | 10000 | 891.03 | stop |
| 13 | section_summary | low | 790 | 565 | 102 | 1200 | 10000 | 872.47 | stop |
| 14 | section_summary | low | 806 | 581 | 119 | 1200 | 10000 | 1266.72 | stop |
| 15 | section_summary | low | 2469 | 2244 | 536 | 1200 | 10000 | 2815.95 | stop |
| 16 | section_summary | low | 1532 | 1307 | 405 | 1200 | 10000 | 2338.11 | stop |
| 17 | section_summary | low | 790 | 565 | 179 | 1200 | 10000 | 1402.44 | stop |
| 18 | section_summary | low | 1404 | 1179 | 404 | 1200 | 10000 | 2086.37 | stop |
| 19 | section_summary | low | 1065 | 840 | 198 | 1200 | 10000 | 1282.07 | stop |
| 20 | section_summary | low | 2531 | 2306 | 237 | 1200 | 10000 | 1709.81 | stop |
| 21 | section_summary | low | 1541 | 1316 | 292 | 1200 | 10000 | 1728.53 | stop |
| 22 | section_summary | low | 953 | 728 | 153 | 1200 | 10000 | 1154.85 | stop |
| 23 | section_summary | low | 905 | 680 | 151 | 1200 | 10000 | 1028.27 | stop |
| 24 | section_summary | low | 1699 | 1474 | 321 | 1200 | 10000 | 1750.41 | stop |
| 25 | section_summary | low | 1324 | 1099 | 382 | 1200 | 10000 | 2150.37 | stop |
| 26 | section_summary | low | 2926 | 2701 | 715 | 1200 | 10000 | 3164.98 | stop |
| 27 | section_summary | low | 1727 | 1502 | 341 | 1200 | 10000 | 1943.90 | stop |
| 28 | section_summary | low | 921 | 696 | 166 | 1200 | 10000 | 1379.53 | stop |
| 29 | section_summary | low | 2988 | 2763 | 195 | 1200 | 10000 | 1759.97 | stop |
| 30 | section_summary | low | 2788 | 2563 | 615 | 1200 | 10000 | 3488.95 | stop |
| 31 | section_summary | low | 7214 | 6947 | 210 | 1200 | 10000 | 1517.45 | stop |
| 32 | section_summary | low | 5108 | 4883 | 1200 | 1200 | 10000 | 5381.81 | length |
| 33 | section_summary | low | 2850 | 2625 | 238 | 1200 | 10000 | 1571.66 | stop |
| 34 | section_summary | low | 4389 | 4122 | 153 | 1200 | 10000 | 1131.44 | stop |
| 35 | section_summary | low | 2587 | 2362 | 615 | 1200 | 10000 | 2986.08 | stop |
| 36 | section_summary | low | 5170 | 4945 | 353 | 1200 | 10000 | 1785.21 | stop |
| 37 | section_summary | low | 2182 | 1915 | 148 | 1200 | 10000 | 944.81 | stop |
| 38 | section_summary | low | 2649 | 2424 | 182 | 1200 | 10000 | 1067.83 | stop |
| 39 | section_summary | low | 6046 | 5779 | 208 | 1200 | 10000 | 1281.43 | stop |
| 40 | section_summary | low | 2222 | 1955 | 257 | 1200 | 10000 | 1506.01 | stop |
| 41 | section_summary | low | 3803 | 3578 | 1200 | 1200 | 10000 | 3514.87 | length |
| 42 | section_summary | low | 2715 | 2490 | 838 | 1200 | 10000 | 3454.39 | stop |
| 43 | section_summary | low | 6674 | 6407 | 275 | 1200 | 10000 | 2318.87 | stop |
| 44 | section_summary | low | 3865 | 3640 | 384 | 1200 | 10000 | 2412.15 | stop |
| 45 | section_summary | low | 2777 | 2552 | 181 | 1200 | 10000 | 1360.83 | stop |
| 46 | section_summary | low | 4610 | 4343 | 143 | 1200 | 10000 | 1201.56 | stop |
| 47 | section_summary | low | 6402 | 6135 | 772 | 1200 | 10000 | 3779.32 | stop |
| 48 | section_summary | low | 4650 | 4383 | 212 | 1200 | 10000 | 1757.31 | stop |
| 49 | section_summary | low | 6527 | 6260 | 158 | 1200 | 10000 | 1271.57 | stop |
| 50 | section_summary | low | 6756 | 6489 | 831 | 1200 | 10000 | 3996.33 | stop |
| 51 | section_summary | low | 6525 | 6258 | 134 | 1200 | 10000 | 1146.27 | stop |
| 52 | section_summary | low | 5598 | 5331 | 122 | 1200 | 10000 | 1098.40 | stop |
| 53 | section_summary | low | 6875 | 6608 | 180 | 1200 | 10000 | 1442.66 | stop |
| 54 | section_summary | low | 6796 | 6529 | 669 | 1200 | 10000 | 3500.66 | stop |
| 55 | section_summary | low | 6915 | 6648 | 129 | 1200 | 10000 | 1111.87 | stop |
| 56 | section_summary | low | 5572 | 5305 | 152 | 1200 | 10000 | 1139.58 | stop |
| 57 | section_summary | low | 6796 | 6529 | 326 | 1200 | 10000 | 2007.29 | stop |
| 58 | section_summary | low | 4944 | 4677 | 179 | 1200 | 10000 | 1268.04 | stop |
| 59 | section_summary | low | 6772 | 6505 | 385 | 1200 | 10000 | 1794.06 | stop |
| 60 | section_summary | low | 5429 | 5162 | 236 | 1200 | 10000 | 1483.34 | stop |
| 61 | section_summary | low | 5572 | 5305 | 165 | 1200 | 10000 | 1224.45 | stop |
| 62 | section_summary | low | 6812 | 6545 | 381 | 1200 | 10000 | 1889.50 | stop |
| 63 | section_summary | low | 6555 | 6288 | 125 | 1200 | 10000 | 1055.51 | stop |
| 64 | section_summary | low | 6671 | 6404 | 503 | 1200 | 10000 | 1480.31 | stop |
| 65 | section_summary | low | 5588 | 5321 | 121 | 1200 | 10000 | 925.30 | stop |
| 66 | section_summary | low | 6713 | 6446 | 285 | 1200 | 10000 | 1672.57 | stop |
| 67 | section_summary | low | 7211 | 6944 | 295 | 1200 | 10000 | 1637.00 | stop |
| 68 | section_summary | low | 7251 | 6984 | 163 | 1200 | 10000 | 1350.80 | stop |
| 69 | section_summary | low | 6784 | 6517 | 368 | 1200 | 10000 | 1752.44 | stop |
| 70 | section_summary | low | 8350 | 8083 | 350 | 1200 | 10000 | 2190.89 | stop |
| 71 | section_summary | low | 6824 | 6557 | 290 | 1200 | 10000 | 2365.32 | stop |
| 72 | section_summary | low | 7159 | 6892 | 258 | 1200 | 10000 | 1741.61 | stop |
| 73 | section_summary | low | 6747 | 6480 | 538 | 1200 | 10000 | 2095.51 | stop |
| 74 | section_summary | low | 2203 | 1936 | 307 | 1200 | 10000 | 1768.43 | stop |
| 75 | section_summary | low | 6789 | 6522 | 298 | 1200 | 10000 | 1729.62 | stop |
| 76 | section_summary | low | 8607 | 8340 | 353 | 1200 | 10000 | 2080.98 | stop |
| 77 | section_summary | low | 4170 | 3903 | 388 | 1200 | 10000 | 1690.38 | stop |
| 78 | section_summary | low | 8647 | 8380 | 128 | 1200 | 10000 | 1228.74 | stop |
| 79 | section_summary | low | 4210 | 3943 | 373 | 1200 | 10000 | 2266.76 | stop |
| 80 | section_summary | low | 6888 | 6621 | 326 | 1200 | 10000 | 2303.39 | stop |
| 81 | section_summary | low | 2580 | 2313 | 196 | 1200 | 10000 | 1344.11 | stop |
| 82 | section_summary | low | 8576 | 8309 | 662 | 1200 | 10000 | 3093.72 | stop |
| 83 | section_summary | low | 8616 | 8349 | 335 | 1200 | 10000 | 2012.79 | stop |
| 84 | group_summary | low | 6612 | 6387 | 1624 | 2500 | 10000 | 4955.33 | stop |
| 85 | group_summary | low | 2906 | 2681 | 1128 | 2500 | 10000 | 3806.26 | stop |
| 86 | document_summary | low | 3703 | 3478 | 1833 | 2500 | 10000 | 4718.86 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation, and in that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All, including the evaluation counts for both settings?

Sub-queries: [&#x27;model papers manually annotated count&#x27;, &#x27;InfoFound vs All overall accuracy and positive-class F1&#x27;, &#x27;evaluation counts for InfoFound and All settings&#x27;]

Ask latency_ms: 5039.60

Judge latency_ms: 2509.35

Total evaluation latency_ms: 7557.14

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | Three model papers (Gemini Robotics 1.5, OpenVLA, and π0) were manually annotated for expert validation[C4].  <br><br>When the “InfoFound” subset is used instead of all evaluated cases, the overall accuracy drops from 0.966 to 0.951, a decrease of 0.015, while the positive‑class F1 score remains unchanged at 0.762[C8].  <br><br>The evaluation counts are 447 criterion‑level decisions for the “All” setting and 304 decisions for the “InfoFound” setting[C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 235 | 600 | 10000 | 1421.68 | stop |
| 2 | answer | medium | 4370 | 4145 | 766 | 3000 | 10000 | 3018.51 | stop |
| 3 | judge | low | 1027 | 802 | 398 | 1000 | 10000 | 1443.59 | stop |
| 4 | judge | low | 912 | 687 | 179 | 1000 | 10000 | 1065.76 | stop |

### Finalized answer

<pre>Three model papers (Gemini Robotics 1.5, OpenVLA, and π0) were manually annotated for expert validation[C4].  

When the “InfoFound” subset is used instead of all evaluated cases, the overall accuracy drops from 0.966 to 0.951, a decrease of 0.015, while the positive‑class F1 score remains unchanged at 0.762[C8].  

The evaluation counts are 447 criterion‑level decisions for the “All” setting and 304 decisions for the “InfoFound” setting[C8].</pre>

## SECOND_NUMBER — repetition 2

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 3202.99

Judge latency_ms: 2665.67

Total evaluation latency_ms: 5871.79

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | FAIL | No used Citation resolves to a Chunk on the required page or containing the required table label |  |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | Three model papers were manually annotated for expert validation [C4].  <br><br>When the “InfoFound” subset is used instead of all evaluations, the overall accuracy drops from 0.966 to 0.951, while the positive‑class F1 score remains the same at 0.762 [C9].  <br><br>Evaluation counts:  <br>* **All** – 447 criterion‑paper‑implication decisions (N = 447) [C9]  <br>* **InfoFound** – 304 decisions (N = 304) [C9] |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 129 | 600 | 10000 | 906.21 | stop |
| 2 | answer | medium | 5116 | 4891 | 582 | 3000 | 10000 | 1963.68 | stop |
| 3 | judge | low | 1024 | 799 | 402 | 1000 | 10000 | 1793.66 | stop |
| 4 | judge | low | 910 | 685 | 135 | 1000 | 10000 | 872.01 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation [C4].  

When the “InfoFound” subset is used instead of all evaluations, the overall accuracy drops from 0.966 to 0.951, while the positive‑class F1 score remains the same at 0.762 [C9].  

Evaluation counts:  
* **All** – 447 criterion‑paper‑implication decisions (N = 447) [C9]  
* **InfoFound** – 304 decisions (N = 304) [C9]</pre>

## SECOND_NUMBER — repetition 3

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 3147.37

Judge latency_ms: 2048.24

Total evaluation latency_ms: 5199.10

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the expert‑LLM agreement comparison (Table 9), the “All” setting evaluated 447 criterion‑paper pairs with an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8]. When restricting to cases where the LLM flagged that information was found (“InfoFound”), the evaluation covered 304 pairs, the accuracy dropped to 0.951 while the positive‑class F1 remained 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 129 | 600 | 10000 | 870.77 | stop |
| 2 | answer | medium | 5116 | 4891 | 525 | 3000 | 10000 | 2036.97 | stop |
| 3 | judge | low | 1020 | 795 | 162 | 1000 | 10000 | 1075.35 | stop |
| 4 | judge | low | 905 | 680 | 143 | 1000 | 10000 | 972.89 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation [C4].  

In the expert‑LLM agreement comparison (Table 9), the “All” setting evaluated 447 criterion‑paper pairs with an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8]. When restricting to cases where the LLM flagged that information was found (“InfoFound”), the evaluation covered 304 pairs, the accuracy dropped to 0.951 while the positive‑class F1 remained 0.762 [C8].</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 5164.67

Judge latency_ms: 2232.99

Total evaluation latency_ms: 7400.24

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | PASS | Required claim supported by verbatim evidence | The authors are motivated by the industrial shift from highly‑optimized, isolated robots to flexible, collaborative cobots, which makes robust, adaptive control methods the new bottleneck rather than actuation performance[S1].  <br><br>To assess the readiness of robot‑foundation models (RFMs) they built a reproducible DB‑Search pipeline that harvested literature from five databases, created three corpora (RFM‑related, industrial‑implication, and auxiliary), and then automatically scored every manipulation‑capable RFM (324 in total) against a catalogue of 149 industrial‑readiness criteria using a GPT‑5.1‑based extraction method; binary “supported/unsupported” decisions were validated on three expert‑rated papers (0.966 accuracy, 0.762 F1, κ = 0.744)[S1][S2].  <br><br>The main findings are that current RFMs show limited and uneven industrial maturity: even the top‑scoring models satisfy only about 0.11–0.12 of the 149 criteria, with the highest proportional fulfilment for any single implication being 0.44 (adaptability, implication I1) and only one model exceeding 0.4 on any implication[S2].  Dominant implications are adaptability/flexibility (I1), benchmarking/evaluation (I10) and data usage (I11), which achieve the highest coverage values (≈0.75 overall, 1.0 in the top‑50), whereas safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7) remain under‑represented with breadth metrics below 0.1[S2].  The most frequently fulfilled criteria are Multi‑Task Generalisation, Flexible Data Type Acceptance, Repeatability &amp; Reproducibility and Low‑Data Adaptation, yet their explicitness scores stay modest (e.g., 0.28 for Multi‑Task Generalisation)[S2].  <br><br>Limitations reported by the authors include the reliance on an LLM‑based extraction pipeline that may affect the precision of proportional scores, the focus solely on manipulation‑capable models and on the predefined 149 criteria (leaving other robot functions uncovered), the small size of the highest‑rated subset (five models) which limits generalisability, and the observation that coverage has not monotonically increased over time[S2].  <br><br>Because the assessment depends on published evidence, any model capability that is not reported in the literature is treated as unsupported and therefore counted as a gap, leading to conservative maturity estimates[S1].  The expert validation scope is confined to three papers that were manually rated by domain experts; their high agreement metrics provide confidence in the pipeline’s reliability but do not extend validation to the full corpus[S1].  <br><br>Appendix A compiles related‑work references to situate this survey within the broader literature[S2]; Appendix B documents the detailed literature‑search and corpus‑construction procedures that underpin the DB‑Search pipeline[S2]; Appendix C enumerates and describes the twelve industrial implications and their associated attributes, forming the basis of the 149‑criterion catalogue[S2]; and Appendix D presents an overview of the evaluated RFMs, including tables of scores and model‑level details[S2]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 159 | 600 | 10000 | 861.17 | stop |
| 2 | answer | medium | 3961 | 3736 | 1268 | 3000 | 10000 | 4271.10 | stop |
| 3 | judge | low | 1562 | 1337 | 840 | 1000 | 10000 | 2232.99 | stop |

### Finalized answer

<pre>The authors are motivated by the industrial shift from highly‑optimized, isolated robots to flexible, collaborative cobots, which makes robust, adaptive control methods the new bottleneck rather than actuation performance[S1].  

To assess the readiness of robot‑foundation models (RFMs) they built a reproducible DB‑Search pipeline that harvested literature from five databases, created three corpora (RFM‑related, industrial‑implication, and auxiliary), and then automatically scored every manipulation‑capable RFM (324 in total) against a catalogue of 149 industrial‑readiness criteria using a GPT‑5.1‑based extraction method; binary “supported/unsupported” decisions were validated on three expert‑rated papers (0.966 accuracy, 0.762 F1, κ = 0.744)[S1][S2].  

The main findings are that current RFMs show limited and uneven industrial maturity: even the top‑scoring models satisfy only about 0.11–0.12 of the 149 criteria, with the highest proportional fulfilment for any single implication being 0.44 (adaptability, implication I1) and only one model exceeding 0.4 on any implication[S2].  Dominant implications are adaptability/flexibility (I1), benchmarking/evaluation (I10) and data usage (I11), which achieve the highest coverage values (≈0.75 overall, 1.0 in the top‑50), whereas safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7) remain under‑represented with breadth metrics below 0.1[S2].  The most frequently fulfilled criteria are Multi‑Task Generalisation, Flexible Data Type Acceptance, Repeatability &amp; Reproducibility and Low‑Data Adaptation, yet their explicitness scores stay modest (e.g., 0.28 for Multi‑Task Generalisation)[S2].  

Limitations reported by the authors include the reliance on an LLM‑based extraction pipeline that may affect the precision of proportional scores, the focus solely on manipulation‑capable models and on the predefined 149 criteria (leaving other robot functions uncovered), the small size of the highest‑rated subset (five models) which limits generalisability, and the observation that coverage has not monotonically increased over time[S2].  

Because the assessment depends on published evidence, any model capability that is not reported in the literature is treated as unsupported and therefore counted as a gap, leading to conservative maturity estimates[S1].  The expert validation scope is confined to three papers that were manually rated by domain experts; their high agreement metrics provide confidence in the pipeline’s reliability but do not extend validation to the full corpus[S1].  

Appendix A compiles related‑work references to situate this survey within the broader literature[S2]; Appendix B documents the detailed literature‑search and corpus‑construction procedures that underpin the DB‑Search pipeline[S2]; Appendix C enumerates and describes the twelve industrial implications and their associated attributes, forming the basis of the 149‑criterion catalogue[S2]; and Appendix D presents an overview of the evaluated RFMs, including tables of scores and model‑level details[S2].</pre>

## SECOND_SUMMARY — repetition 2

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 4703.85

Judge latency_ms: 963.61

Total evaluation latency_ms: 5676.84

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted: The answer does not contain a verbatim statement that the work does not claim any model is universally production‑ready, so the required claim is not fully supported. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 159 | 600 | 10000 | 813.45 | stop |
| 2 | answer | medium | 3961 | 3736 | 1863 | 3000 | 10000 | 3865.60 | stop |
| 3 | judge | low | 1653 | 1428 | 284 | 1000 | 10000 | 963.61 | stop |

### Finalized answer

<pre>The authors are motivated by the shift from isolated, highly optimized industrial robots to flexible, collaborative cobots and the need for adaptive, learning‑based robot intelligence, noting that current robotic foundation models (RFMs) lack industry‑grade autonomy such as reliable online adaptation, safety under uncertainty, and integrated deployment requirements [S1].  
To address the lack of a dedicated survey of industrial RFM use cases, they define RFMs as multimodal, highly adaptable systems that retain cross‑task and cross‑embodiment adaptability, and they aim to fill this gap by providing a taxonomy, criteria catalogue, and empirical baseline [S1].  
Their assessment method consists of a systematic literature acquisition pipeline (DB‑Search) that gathers three corpora—including 1 025 RFM‑related works, 125 industrial‑implication papers, and 113 auxiliary publications—and then evaluates 324 manipulation‑capable RFMs against a catalogue of 149 industrial‑readiness criteria derived from twelve implications using an automated GPT‑5.1 extraction pipeline with binary support decisions [S1][S2].  
The pipeline’s accuracy was validated against three expert‑rated papers, achieving 0.966 accuracy, 0.762 F1 for the positive class, κ = 0.744, a 1.9 % false‑positive rate and a 22.6 % false‑negative rate, indicating reliable but cautious maturity estimates [S1].  
Results show that even the top‑performing models satisfy only about 0.11‑0.12 of the 149 criteria, with the highest proportional fulfilment for any single implication being 0.44 (Gemini Robotics 1.5 on adaptability) and only one model exceeding 0.4 on any implication, revealing limited and uneven industrial maturity focused mainly on adaptability, benchmarking, and data usage while safety, HRI/HRC, real‑time performance and cost‑effectiveness remain under‑represented [S2].  
Per‑implication coverage metrics confirm that adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements (I11) have the highest 1+‑Coverage values (≈0.75‑0.76 overall, 1.0 in the top‑50), whereas safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7) have very low breadth (e.g., I2: 0.034 overall) and near‑zero scores for most models [S2].  
The authors note that because the assessment relies on published evidence, any capabilities that are not reported in the literature are treated as unsupported, which can depress the measured applicability of models and bias the results toward documented features [S2].  
Expert validation is limited to the three papers used for pipeline verification, so the scope of expert confirmation does not extend to the full set of 324 models, constraining the generalisability of the validation to the extraction method rather than to all model evaluations [S1][S2].  
The study’s limitations include the dependence on an LLM‑based extraction that may affect precision of proportional scores, the focus solely on manipulation‑capable RFMs and the predefined 149 criteria, and the small size of the highest‑rated subset (five models), which may limit the broader applicability of the top‑model observations [S2].  
Appendix A provides related‑work references, Appendix B details the literature‑research procedures and corpus construction, Appendix C enumerates the industrial implications and associated attributes, and Appendix D presents the overview of the evaluated RFMs, supporting the main analysis [S2].</pre>

## SECOND_SUMMARY — repetition 3

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 4970.27

Judge latency_ms: 2515.05

Total evaluation latency_ms: 7520.18

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Judge failed: LLMTruncated: Judge was truncated. Please retry. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 88 | 600 | 10000 | 680.68 | stop |
| 2 | answer | medium | 3961 | 3736 | 1363 | 3000 | 10000 | 4261.01 | stop |
| 3 | judge | low | 2008 | 1783 | 1000 | 1000 | 10000 | 2515.05 | length |

### Finalized answer

<pre>**Motivation**  
The authors observe that industrial robotics is shifting from isolated, highly‑optimized automation toward flexible, collaborative cobot deployment, and that progress is now limited more by the availability of robust, adaptive control methods than by actuation performance [S1]. They therefore survey robotic foundation models (RFMs) to assess whether current data‑driven, multimodal systems can meet the industrial‑grade requirements of safety, online adaptation, and integrated deployment [S1].

**Assessment method**  
A systematic literature‑acquisition pipeline (DB‑Search) collected three corpora, the main one containing 1 025 works of which 324 manipulation‑capable RFMs were identified [S1]. Each RFM was evaluated against a catalogue of 149 industrial‑readiness criteria derived from twelve industrial implications (Section 7) [S1][S2]. The evaluation used an LLM‑based extraction pipeline (GPT‑5.1) that isolates paper‑criterion pairs, extracts evidence, and assigns a proportional applicability rating for every implication [S2]. Validation of the pipeline against three expert‑rated papers reported 0.966 accuracy, 0.762 F1 for the positive class, κ = 0.744, a 1.9 % false‑positive rate and a 22.6 % false‑negative rate [S1].

**Main findings**  

* Overall coverage is low: even the top‑scoring RFMs satisfy only about 0.11–0.12 of the 149 criteria, with the highest proportional fulfilment for any single implication being 0.44 (Gemini Robotics 1.5 on I1) [S2].  
* Adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements/usage (I11) are the only implications with relatively high coverage (e.g., I1 0.756 overall, 1.0 in the top‑50) [S2].  
* Safety/compliance (I2), human‑robot interaction/collaboration (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7) remain under‑represented, showing very low breadth metrics (e.g., I2 0.034 overall, 0.22 in the top‑50) [S2].  
* The most frequently fulfilled criteria are Multi‑Task Generalisation, Flexible Data Type Acceptance, Repeatability &amp; Reproducibility and Low‑Data Adaptation, yet their explicitness scores are modest (e.g., Multi‑Task Generalisation 0.28) [S2].  
* Gap analysis reveals large discrepancies (gc ≈ 0.5–0.98) between literature evidence and actual criterion fulfilment, indicating that industrial constraints are discussed but rarely implemented [S2].

**Limitations**  

* The applicability ratings rely on an automated LLM‑based extraction that may affect the precision of proportional scores [S2].  
* The analysis is limited to models that include manipulation capabilities and to the predefined set of 149 criteria; other robot functionalities are not examined [S2].  
* Only a small “highest‑rated” subset (five models) was inspected in depth, which may limit the generalisability of observations about top‑performing RFMs [S2].  
* No monotonic increase in criteria coverage over time was observed, suggesting that the current literature does not yet reflect rapid progress in the under‑represented implications [S2].

**Effect of unreported model capabilities**  
Because the pipeline extracts evidence only from what is reported in publications, any capability that authors do not disclose (e.g., safety modules, real‑time guarantees, integration features) cannot be captured and is therefore treated as unfulfilled [S2]. This leads to systematic under‑estimation of a model’s true industrial readiness and contributes to the high false‑negative rate observed in the expert validation (22.6 %) [S1].

**Scope of expert validation**  
Expert validation was performed on three papers that had been manually rated by domain experts; the validation metrics (accuracy, F1, κ) reflect how well the automated pipeline reproduces those expert judgments [S1]. Since only three expert‑rated papers were used, the validation scope is narrow and may not capture the full variability of reporting styles across the entire corpus.

**Purpose of each appendix**  

* **Appendix A – Related Works**: documents the existing survey and review literature, highlighting the gap that few works address RFMs with an industrial focus [S1].  
* **Appendix B – Literature Research**: details the DB‑Search pipeline, query syntax, duplicate removal, and relevance‑filtering procedures that produced the three corpora [S1].  
* **Appendix C – Industrial Implications**: enumerates the twelve industrial implications, the 47 detailed attributes, and the 149 criteria used for the maturity assessment [S1].  
* **Appendix D – RFM‑Overview**: provides the full list of the 324 manipulation‑capable RFMs, their classification, and the tabulated evaluation results (e.g., Table D5, Table 11, Table 12) [S2].</pre>
