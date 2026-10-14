# Golden Facts evaluation

Created: 2026-10-13T12:16:43.777371+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 3

Result: FAIL

Functional operations: PASS (separate from D05 semantic rates)

Call audit: {&quot;budget_violations&quot;: 0, &quot;calls&quot;: 102, &quot;length_attempts&quot;: [{&quot;call_type&quot;: &quot;section_summary&quot;, &quot;num_predict&quot;: 1200, &quot;think&quot;: &quot;low&quot;}], &quot;maximum_estimated_prompt_plus_reservation&quot;: 9630, &quot;maximum_reported_prompt_plus_reservation&quot;: 9363, &quot;missing_reported_prompt_counts&quot;: 0, &quot;router_answer_length_attempts&quot;: 0}

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 0c320a8c24ae4917a2fe56db55ae2651c5ad76da

Uncommitted changes: yes

Pipeline version: ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Created: 2026-10-13T12:16:43.774735+00:00

Label: issue11-final-second

D05: Report raw rates/causes; semantic defects do not block delivery.

Effective settings: {&quot;answer_think&quot;: &quot;medium&quot;, &quot;bm25_weight&quot;: 0.0, &quot;chunk_token_target&quot;: 500, &quot;lookup_top_k&quot;: 5, &quot;sub_query_top_k&quot;: 2, &quot;summary_concurrency&quot;: 4, &quot;synthesis_top_k&quot;: 3}

Peak guarded calls by type: {&quot;section_summary&quot;: 4, &quot;group_summary&quot;: 1, &quot;document_summary&quot;: 1, &quot;router&quot;: 1, &quot;answer&quot;: 1, &quot;judge&quot;: 1}

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | required_source_citation | events | 3/3 (100.0%) |
| SECOND_NUMBER | question_type | events | 3/3 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 1/3 (33.3%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 3/3 (100.0%) |
| SECOND_SUMMARY | question_type | events | 3/3 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 1/3 (33.3%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 854 | 629 | 128 | 1200 | 10000 | 1037.11 | stop |
| 2 | section_summary | low | 922 | 697 | 166 | 1200 | 10000 | 1275.43 | stop |
| 3 | section_summary | low | 1734 | 1509 | 344 | 1200 | 10000 | 1979.03 | stop |
| 4 | section_summary | low | 2094 | 1869 | 525 | 1200 | 10000 | 2552.52 | stop |
| 5 | section_summary | low | 2804 | 2579 | 924 | 1200 | 10000 | 3939.31 | stop |
| 6 | section_summary | low | 1151 | 926 | 227 | 1200 | 10000 | 1187.22 | stop |
| 7 | section_summary | low | 729 | 504 | 75 | 1200 | 10000 | 815.04 | stop |
| 8 | section_summary | low | 2835 | 2610 | 820 | 1200 | 10000 | 4929.64 | stop |
| 9 | section_summary | low | 2866 | 2641 | 248 | 1200 | 10000 | 1590.92 | stop |
| 10 | section_summary | low | 806 | 581 | 159 | 1200 | 10000 | 1181.87 | stop |
| 11 | section_summary | low | 713 | 488 | 122 | 1200 | 10000 | 1159.54 | stop |
| 12 | section_summary | low | 2897 | 2672 | 225 | 1200 | 10000 | 1775.26 | stop |
| 13 | section_summary | low | 790 | 565 | 104 | 1200 | 10000 | 962.89 | stop |
| 14 | section_summary | low | 2469 | 2244 | 754 | 1200 | 10000 | 3510.50 | stop |
| 15 | section_summary | low | 1532 | 1307 | 395 | 1200 | 10000 | 2222.39 | stop |
| 16 | section_summary | low | 1404 | 1179 | 328 | 1200 | 10000 | 1959.69 | stop |
| 17 | section_summary | low | 2531 | 2306 | 167 | 1200 | 10000 | 1275.25 | stop |
| 18 | section_summary | low | 790 | 565 | 216 | 1200 | 10000 | 1724.25 | stop |
| 19 | section_summary | low | 1541 | 1316 | 254 | 1200 | 10000 | 1618.68 | stop |
| 20 | section_summary | low | 1065 | 840 | 169 | 1200 | 10000 | 1205.39 | stop |
| 21 | section_summary | low | 953 | 728 | 162 | 1200 | 10000 | 1185.31 | stop |
| 22 | section_summary | low | 1324 | 1099 | 266 | 1200 | 10000 | 1476.68 | stop |
| 23 | section_summary | low | 1699 | 1474 | 358 | 1200 | 10000 | 1772.73 | stop |
| 24 | section_summary | low | 905 | 680 | 128 | 1200 | 10000 | 993.01 | stop |
| 25 | section_summary | low | 1727 | 1502 | 401 | 1200 | 10000 | 2759.87 | stop |
| 26 | section_summary | low | 2926 | 2701 | 774 | 1200 | 10000 | 4040.24 | stop |
| 27 | section_summary | low | 921 | 696 | 157 | 1200 | 10000 | 1363.09 | stop |
| 28 | section_summary | low | 2988 | 2763 | 210 | 1200 | 10000 | 1838.51 | stop |
| 29 | section_summary | low | 2788 | 2563 | 895 | 1200 | 10000 | 5222.91 | stop |
| 30 | section_summary | low | 5108 | 4883 | 1200 | 1200 | 10000 | 6568.61 | length |
| 31 | section_summary | low | 2587 | 2362 | 595 | 1200 | 10000 | 3299.08 | stop |
| 32 | section_summary | low | 7200 | 6933 | 419 | 1200 | 10000 | 2798.11 | stop |
| 33 | section_summary | low | 2850 | 2625 | 261 | 1200 | 10000 | 3142.50 | stop |
| 34 | section_summary | low | 5170 | 4945 | 222 | 1200 | 10000 | 2171.17 | stop |
| 35 | section_summary | low | 2649 | 2424 | 246 | 1200 | 10000 | 2178.22 | stop |
| 36 | section_summary | low | 4385 | 4118 | 269 | 1200 | 10000 | 2842.14 | stop |
| 37 | section_summary | low | 6042 | 5775 | 268 | 1200 | 10000 | 2555.12 | stop |
| 38 | section_summary | low | 3803 | 3578 | 899 | 1200 | 10000 | 4440.66 | stop |
| 39 | section_summary | low | 2715 | 2490 | 871 | 1200 | 10000 | 4278.16 | stop |
| 40 | section_summary | low | 3090 | 2823 | 189 | 1200 | 10000 | 3243.65 | stop |
| 41 | section_summary | low | 6670 | 6403 | 227 | 1200 | 10000 | 1741.65 | stop |
| 42 | section_summary | low | 2777 | 2552 | 176 | 1200 | 10000 | 1719.08 | stop |
| 43 | section_summary | low | 3865 | 3640 | 306 | 1200 | 10000 | 1880.54 | stop |
| 44 | section_summary | low | 6398 | 6131 | 500 | 1200 | 10000 | 1663.47 | stop |
| 45 | section_summary | low | 6440 | 6173 | 494 | 1200 | 10000 | 1991.07 | stop |
| 46 | section_summary | low | 6752 | 6485 | 526 | 1200 | 10000 | 1957.17 | stop |
| 47 | section_summary | low | 6794 | 6527 | 462 | 1200 | 10000 | 2461.44 | stop |
| 48 | section_summary | low | 6768 | 6501 | 554 | 1200 | 10000 | 2714.48 | stop |
| 49 | section_summary | low | 4608 | 4341 | 111 | 1200 | 10000 | 11956.75 | stop |
| 50 | section_summary | low | 6523 | 6256 | 166 | 1200 | 10000 | 1302.63 | stop |
| 51 | section_summary | low | 6521 | 6254 | 147 | 1200 | 10000 | 1142.11 | stop |
| 52 | section_summary | low | 6667 | 6400 | 941 | 1200 | 10000 | 4185.01 | stop |
| 53 | section_summary | low | 6561 | 6294 | 115 | 1200 | 10000 | 1193.70 | stop |
| 54 | section_summary | low | 5596 | 5329 | 129 | 1200 | 10000 | 1052.20 | stop |
| 55 | section_summary | low | 6780 | 6513 | 559 | 1200 | 10000 | 3192.69 | stop |
| 56 | section_summary | low | 6871 | 6604 | 128 | 1200 | 10000 | 1128.10 | stop |
| 57 | section_summary | low | 5570 | 5303 | 184 | 1200 | 10000 | 1433.43 | stop |
| 58 | section_summary | low | 4942 | 4675 | 102 | 1200 | 10000 | 1006.71 | stop |
| 59 | section_summary | low | 6743 | 6476 | 627 | 1200 | 10000 | 3395.12 | stop |
| 60 | section_summary | low | 5427 | 5160 | 143 | 1200 | 10000 | 1210.13 | stop |
| 61 | section_summary | low | 5467 | 5200 | 255 | 1200 | 10000 | 1649.16 | stop |
| 62 | section_summary | low | 4166 | 3899 | 355 | 1200 | 10000 | 2105.71 | stop |
| 63 | section_summary | low | 5570 | 5303 | 125 | 1200 | 10000 | 1183.12 | stop |
| 64 | section_summary | low | 6551 | 6284 | 161 | 1200 | 10000 | 1513.79 | stop |
| 65 | section_summary | low | 8352 | 8085 | 473 | 1200 | 10000 | 2770.53 | stop |
| 66 | section_summary | low | 6591 | 6324 | 128 | 1200 | 10000 | 1327.17 | stop |
| 67 | section_summary | low | 5586 | 5319 | 160 | 1200 | 10000 | 1462.09 | stop |
| 68 | section_summary | low | 2623 | 2356 | 558 | 1200 | 10000 | 3219.99 | stop |
| 69 | section_summary | low | 4210 | 3943 | 461 | 1200 | 10000 | 2265.07 | stop |
| 70 | section_summary | low | 7207 | 6940 | 584 | 1200 | 10000 | 2940.82 | stop |
| 71 | section_summary | low | 7247 | 6980 | 391 | 1200 | 10000 | 1785.14 | stop |
| 72 | section_summary | low | 8340 | 8073 | 334 | 1200 | 10000 | 1487.28 | stop |
| 73 | section_summary | low | 7151 | 6884 | 353 | 1200 | 10000 | 2077.37 | stop |
| 74 | section_summary | low | 2201 | 1934 | 381 | 1200 | 10000 | 1986.96 | stop |
| 75 | section_summary | low | 8287 | 8020 | 178 | 1200 | 10000 | 1360.93 | stop |
| 76 | section_summary | low | 8390 | 8123 | 148 | 1200 | 10000 | 1244.08 | stop |
| 77 | section_summary | low | 8430 | 8163 | 228 | 1200 | 10000 | 1592.52 | stop |
| 78 | section_summary | low | 2727 | 2460 | 214 | 1200 | 10000 | 1962.68 | stop |
| 79 | group_summary | low | 6450 | 6225 | 1384 | 2500 | 10000 | 7555.32 | stop |
| 80 | group_summary | low | 3126 | 2901 | 900 | 2500 | 10000 | 4898.60 | stop |
| 81 | document_summary | low | 3243 | 3018 | 1764 | 2500 | 10000 | 5605.28 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation, and how does InfoFound affect overall accuracy and positive-class F1 relative to All, including the evaluation counts for both settings?

Sub-queries: []

Ask latency_ms: 4056.09

Judge latency_ms: 2271.77

Total evaluation latency_ms: 6333.25

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the LLM‑expert agreement table (Table 9), the “All” setting evaluates 447 criterion‑paper pairs and yields an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  <br>When only the cases where the LLM flagged “information found” are considered (“InfoFound”), the evaluation count drops to 304 pairs, the accuracy falls to 0.951 (a decrease of 0.015), while the positive‑class F1 remains unchanged at 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 125 | 600 | 10000 | 978.97 | stop |
| 2 | answer | medium | 5204 | 4979 | 408 | 3000 | 10000 | 2833.42 | stop |
| 3 | judge | low | 1059 | 834 | 230 | 1000 | 10000 | 1272.64 | stop |
| 4 | judge | low | 944 | 719 | 128 | 1000 | 10000 | 999.13 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — two before the automated run and one after — as described in the expert‑agreement comparison [C4].  

In the LLM‑expert agreement table (Table 9), the “All” setting evaluates 447 criterion‑paper pairs and yields an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  
When only the cases where the LLM flagged “information found” are considered (“InfoFound”), the evaluation count drops to 304 pairs, the accuracy falls to 0.951 (a decrease of 0.015), while the positive‑class F1 remains unchanged at 0.762 [C8].</pre>

## SECOND_NUMBER — repetition 2

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation, and in that comparison how does InfoFound affect overall accuracy and positive-class F1 relative to All, including the evaluation counts for both settings?

Sub-queries: [&#x27;model papers manually annotated count expert validation&#x27;, &#x27;InfoFound overall accuracy vs All&#x27;, &#x27;InfoFound positive-class F1 vs All evaluation counts&#x27;]

Ask latency_ms: 3313.16

Judge latency_ms: 2247.64

Total evaluation latency_ms: 5578.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C6 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | Three model papers were manually annotated for expert validation — two before the automated run and one after it [C2].  <br><br>When the “InfoFound” subset is used, the evaluation count drops from 447 to 304 papers [C6].  <br>Overall accuracy falls from 0.966 (All) to 0.951 (InfoFound) [C6], while the positive‑class F1 score remains the same at 0.762 for both settings [C6]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 157 | 600 | 10000 | 1149.42 | stop |
| 2 | answer | medium | 3738 | 3513 | 314 | 3000 | 10000 | 1608.52 | stop |
| 3 | judge | low | 1006 | 781 | 281 | 1000 | 10000 | 1299.46 | stop |
| 4 | judge | low | 891 | 666 | 144 | 1000 | 10000 | 948.19 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — two before the automated run and one after it [C2].  

When the “InfoFound” subset is used, the evaluation count drops from 447 to 304 papers [C6].  
Overall accuracy falls from 0.966 (All) to 0.951 (InfoFound) [C6], while the positive‑class F1 score remains the same at 0.762 for both settings [C6].</pre>

## SECOND_NUMBER — repetition 3

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 3147.28

Judge latency_ms: 2696.62

Total evaluation latency_ms: 5861.91

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | PASS | Required claim supported by verbatim evidence | Three model papers were manually annotated for expert validation — two before the automated run and one after — as described in the expert‑agreement comparison [C4].<br><br>The LLM‑expert agreement results are reported in Table 9.  <br>- **All** settings: 447 criterion‑paper evaluations, overall accuracy 0.966, positive‑class F1 0.762 [C8].  <br>- **InfoFound** settings: 304 evaluations, accuracy 0.951, positive‑class F1 0.762 [C8].<br><br>Thus, using only the “information‑found” subset lowers overall accuracy by 0.015 (from 0.966 to 0.951) while leaving the positive‑class F1 unchanged. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 127 | 600 | 10000 | 917.38 | stop |
| 2 | answer | medium | 5166 | 4941 | 498 | 3000 | 10000 | 1997.92 | stop |
| 3 | judge | low | 1065 | 840 | 478 | 1000 | 10000 | 1830.23 | stop |
| 4 | judge | low | 951 | 726 | 127 | 1000 | 10000 | 866.40 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — two before the automated run and one after — as described in the expert‑agreement comparison [C4].

The LLM‑expert agreement results are reported in Table 9.  
- **All** settings: 447 criterion‑paper evaluations, overall accuracy 0.966, positive‑class F1 0.762 [C8].  
- **InfoFound** settings: 304 evaluations, accuracy 0.951, positive‑class F1 0.762 [C8].

Thus, using only the “information‑found” subset lowers overall accuracy by 0.015 (from 0.966 to 0.951) while leaving the positive‑class F1 unchanged.</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 5172.62

Judge latency_ms: 1141.30

Total evaluation latency_ms: 6323.49

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted: The answer does not provide verbatim excerpts covering all required elements such as the specific number of implications, criteria, model count, detailed limitations, and statements about not claiming universal production readiness; thus the claim is not fully supported. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 94 | 600 | 10000 | 738.95 | stop |
| 2 | answer | medium | 3551 | 3326 | 1180 | 3000 | 10000 | 4392.38 | stop |
| 3 | judge | low | 1675 | 1450 | 123 | 1000 | 10000 | 1141.30 | stop |

### Finalized answer

<pre>The authors motivate the work by pointing out that, although robotic foundation models (RFMs) are defined as highly adaptable, multimodal systems that can generalise across tasks, environments and robot embodiments, only a handful of prior surveys have examined RFMs and virtually none have linked them to industrial use, leaving a gap that this study aims to fill [S1].  They also note the broader industrial shift from traditional high‑speed, high‑payload robots to collaborative cobots that require flexible, safe, and human‑centric automation, which creates a demand for RFMs that can provide intuitive instruction, autonomous decision‑making and real‑time adaptation [S1].

To assess industrial readiness the authors first built three literature corpora (a main RFM‑related corpus of 1 025 highly relevant works, an industrial‑implication corpus and auxiliary searches) and then derived eleven domain‑agnostic requirements that were expanded into 149 concrete criteria covering model‑centric, ecosystem‑centric and joint aspects [S1].  An automated pipeline based on GPT‑5.1 extracted evidence from each of the 324 manipulation‑capable RFMs and produced binary fulfil‑ment judgments for every criterion, yielding 48 276 decisions [S1][S2].  The pipeline’s output was checked by experts on three papers, achieving 96.6 % accuracy, an F1 of 0.762 and Cohen’s κ = 0.744, but with a low false‑positive rate (1.9 %) and a higher false‑negative rate (22.6 %) because of a conservative decision policy [S1].

The main findings are that industrial maturity is limited and uneven: even the highest‑scoring models (e.g., Gemini Robotics 1.5) attain only a total applicability score of 0.12 and show narrow strengths in adaptability/flexibility, benchmarking/evaluation and data usage, while safety/compliance, human‑robot interaction, real‑time performance and cost‑effectiveness receive very little attention (coverage ≈ 0.03‑0.07, accuracy ≈ 0.01‑0.04) [S2].  Across all 324 models the best depth (ACC) reaches only about 0.24 for the three dominant implications, and most papers provide only sparse, non‑explicit evidence for many industrial criteria [S2].  The authors conclude that robust, adaptable intelligence for cobots remains a bottleneck and that future research must address safety, latency, edge‑aware deployment and verifiable architectures [S2].

A key limitation is that the assessment relies on LLM‑based extraction from publication text, so any capability that is not explicitly reported in the paper is likely to be missed and counted as unfulfilled, inflating false‑negative rates and biasing the overall scores [S1][S2].  The expert validation is confined to three papers, which, while showing high agreement, limits the generalisability of the validation results to the full set of 324 RFMs [S1].

The appendices serve distinct supporting roles: Appendix A (Table A1) catalogues the 55 related surveys and reviews on embodied AI, vision‑language‑action models and foundation‑model robotics, situating this work within the broader literature [S2]; Appendix B lists the eleven ASQS queries used to construct the RFM‑related corpus [S2]; Appendix C (Table C4) presents the complete criteria catalogue of 149 industrial‑applicability questions; and Appendix D (Table D5 and related tables) provides the full inventory of the 324 evaluated RFMs with per‑implication ratings and example rows such as Gemini Robotics 1.5, as well as detailed criterion fulfilment for specific implications (e.g., precision &amp; accuracy) [S2].</pre>

## SECOND_SUMMARY — repetition 2

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 12651.64

Judge latency_ms: 1339.34

Total evaluation latency_ms: 13997.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted: The answer does not include a verbatim statement that the work does not claim any model is universally production‑ready, which is required by the claim. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 98 | 600 | 10000 | 8027.44 | stop |
| 2 | answer | medium | 3551 | 3326 | 958 | 3000 | 10000 | 4593.33 | stop |
| 3 | judge | low | 1532 | 1307 | 223 | 1000 | 10000 | 1339.34 | stop |

### Finalized answer

<pre>The authors begin by noting that robotic foundation models (RFMs) are presented as highly adaptable, multimodal systems that could enable flexible, data‑driven automation, yet no prior work has linked RFMs to concrete industrial use‑cases, leaving a clear gap that this survey aims to fill [S1].  

To address this, they construct three literature corpora (a main RFM‑related set, an industrial‑implication set, and auxiliary searches) and extract 324 manipulation‑capable RFMs for evaluation [S1][S2].  From the industrial‑implication corpus they derive eleven domain‑agnostic requirements (safety, robustness, real‑time performance, cost‑effectiveness, etc.) and expand them into a catalogue of 149 concrete criteria [S1].  An automated LLM‑based pipeline (GPT‑5.1) reads each paper, extracts evidence, and makes binary fulfil‑ment judgments for every criterion, producing 48 276 decisions [S2].  Expert validation on three papers shows high agreement (accuracy 0.966, F1 0.762, κ 0.744) but also reveals a low false‑positive rate (1.9 %) and a higher false‑negative rate (22.6 %) due to a conservative decision policy [S2].  

The evaluation finds that industrial maturity is limited and uneven: the highest‑scoring models achieve total applicability scores of only 0.11–0.12, with strengths concentrated in adaptability/flexibility (I1), benchmarking/evaluation (I10) and data usage (I11), while safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness (I7) receive very sparse attention [S2].  Even the best papers reach full coverage (1+‑Coverage = 1.0) for a few implications, but depth remains low (maximum ACC ≈ 0.24) and many criteria are only partially addressed [S2].  

A key limitation is that the assessment relies on LLM‑based extraction from the text of each publication; any capability that is not explicitly reported cannot be captured, leading to under‑estimation of a model’s true abilities and contributing to the observed false‑negative rate [S2].  The expert validation is confined to three papers, so while it confirms the pipeline’s general reliability, the scope of validation does not extend to the full set of 324 models [S2].  

The appendices serve complementary roles: Appendix A lists the 55 related surveys and reviews that contextualise this work within the broader embodied‑AI and foundation‑model literature [S2]; Appendix B details the eleven ASQS queries used to build the RFM‑related corpus [S2]; Appendix C presents the complete criteria catalogue (the 149 questions covering adaptability, safety, explainability, etc.) [S2]; and Appendix D provides the full dataset of 324 RFMs with per‑implication ratings and total scores, including specific tables for individual implications such as precision &amp; accuracy [S2].  </pre>

## SECOND_SUMMARY — repetition 3

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 5237.84

Judge latency_ms: 2511.57

Total evaluation latency_ms: 7756.96

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | PASS | Required claim supported by verbatim evidence | The paper is motivated by the lack of dedicated analysis linking robotic foundation models (RFMs) to industrial use, noting that only a few prior surveys address RFMs and virtually none consider their industrial implications, so this work provides the first systematic examination of how RFMs could support collaborative cobots in real‑world settings[S1].  <br>To assess industrial readiness, the authors built a catalogue of 149 criteria covering model‑centric, ecosystem‑centric and joint requirements, then automatically extracted evidence from each of the 324 manipulation‑capable RFMs using a GPT‑5.1‑based pipeline that produced binary fulfil‑ment judgments for every criterion, yielding 48 276 decisions[S2].  <br>Expert validation was performed on three papers, showing high agreement with the automated extraction (accuracy 0.966, F1 0.762, κ 0.744) but revealing a low false‑positive rate (1.9 %) and a higher false‑negative rate (22.6 %) due to a conservative decision policy, which the authors caution against over‑interpreting individual fine‑grained outcomes[S2].  <br>The main findings show that industrial maturity across all RFMs is limited and uneven: the highest‑scoring models attain total applicability scores of only 0.11–0.12, with strengths concentrated in adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements (I11), while safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness (I7) receive very sparse attention (coverage ≈ 0.03‑0.07, ACC ≈ 0.01‑0.04)[S2].  <br>Because the assessment relies on text‑based extraction, any model capabilities that are not explicitly reported in the publications are missed, leading to lower scores for those models and contributing to the observed gaps in safety, HRI and latency criteria[S2].  <br>The scope of expert validation is limited to three papers, providing a reliable but narrow check on the automated pipeline and indicating that broader validation would be needed to confirm the overall trends[S2].  <br>Appendix A enumerates the 55 related surveys and reviews on embodied AI, vision‑language‑action models and foundation‑model robotics, situating the current work within the broader literature[S2].  <br>Appendix B details the eleven ASQS queries used to construct the RFM‑related corpus, documenting the systematic literature acquisition process[S2].  <br>Appendix C presents the complete industrial‑applicability criteria catalogue (Table C4), defining the 149 questions that guide the evaluation of adaptability, safety, explainability, robustness, and other essential attributes[S2].  <br>Appendix D lists all 324 manipulation‑capable RFMs with their per‑implication ratings and total scores (e.g., Gemini Robotics 1.5: Total 0.12, I1 0.44, I2 0.06, …, I11 0.09), providing the raw data underlying the maturity analysis[S2]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 94 | 600 | 10000 | 1067.00 | stop |
| 2 | answer | medium | 3551 | 3326 | 988 | 3000 | 10000 | 4125.90 | stop |
| 3 | judge | low | 1533 | 1308 | 895 | 1000 | 10000 | 2511.57 | stop |

### Finalized answer

<pre>The paper is motivated by the lack of dedicated analysis linking robotic foundation models (RFMs) to industrial use, noting that only a few prior surveys address RFMs and virtually none consider their industrial implications, so this work provides the first systematic examination of how RFMs could support collaborative cobots in real‑world settings[S1].  
To assess industrial readiness, the authors built a catalogue of 149 criteria covering model‑centric, ecosystem‑centric and joint requirements, then automatically extracted evidence from each of the 324 manipulation‑capable RFMs using a GPT‑5.1‑based pipeline that produced binary fulfil‑ment judgments for every criterion, yielding 48 276 decisions[S2].  
Expert validation was performed on three papers, showing high agreement with the automated extraction (accuracy 0.966, F1 0.762, κ 0.744) but revealing a low false‑positive rate (1.9 %) and a higher false‑negative rate (22.6 %) due to a conservative decision policy, which the authors caution against over‑interpreting individual fine‑grained outcomes[S2].  
The main findings show that industrial maturity across all RFMs is limited and uneven: the highest‑scoring models attain total applicability scores of only 0.11–0.12, with strengths concentrated in adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements (I11), while safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness (I7) receive very sparse attention (coverage ≈ 0.03‑0.07, ACC ≈ 0.01‑0.04)[S2].  
Because the assessment relies on text‑based extraction, any model capabilities that are not explicitly reported in the publications are missed, leading to lower scores for those models and contributing to the observed gaps in safety, HRI and latency criteria[S2].  
The scope of expert validation is limited to three papers, providing a reliable but narrow check on the automated pipeline and indicating that broader validation would be needed to confirm the overall trends[S2].  
Appendix A enumerates the 55 related surveys and reviews on embodied AI, vision‑language‑action models and foundation‑model robotics, situating the current work within the broader literature[S2].  
Appendix B details the eleven ASQS queries used to construct the RFM‑related corpus, documenting the systematic literature acquisition process[S2].  
Appendix C presents the complete industrial‑applicability criteria catalogue (Table C4), defining the 149 questions that guide the evaluation of adaptability, safety, explainability, robustness, and other essential attributes[S2].  
Appendix D lists all 324 manipulation‑capable RFMs with their per‑implication ratings and total scores (e.g., Gemini Robotics 1.5: Total 0.12, I1 0.44, I2 0.06, …, I11 0.09), providing the raw data underlying the maturity analysis[S2].  </pre>
