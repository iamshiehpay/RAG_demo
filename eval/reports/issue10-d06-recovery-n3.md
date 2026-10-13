# Golden Facts evaluation

Created: 2026-10-13T08:57:02.739165+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 588638d67ab0166ddee98c22c2ad4a7a2296b82b

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-d5c6a32bafdaea8eddbbffcea184e34fe08350a767f4690ff0613bc3396eee7c

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

Upload failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | question_type | events | 0/3 (0.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/3 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 0/3 (0.0%) |
| SECOND_SUMMARY | question_type | events | 0/3 (0.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/3 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 922 | 697 | 223 | 1200 | 10000 | 1477.83 | stop |
| 2 | section_summary | low | 854 | 629 | 213 | 1200 | 10000 | 1414.32 | stop |
| 3 | section_summary | low | 2804 | 2579 | 815 | 1200 | 10000 | 3936.57 | stop |
| 4 | section_summary | low | 2835 | 2610 | 930 | 1200 | 10000 | 3944.56 | stop |
| 5 | section_summary | low | 2094 | 1869 | 569 | 1200 | 10000 | 3058.03 | stop |
| 6 | section_summary | low | 1734 | 1509 | 396 | 1200 | 10000 | 3209.61 | stop |
| 7 | section_summary | low | 2897 | 2672 | 153 | 1200 | 10000 | 1043.24 | stop |
| 8 | section_summary | low | 729 | 504 | 67 | 1200 | 10000 | 651.59 | stop |
| 9 | section_summary | low | 1151 | 926 | 201 | 1200 | 10000 | 1120.17 | stop |
| 10 | section_summary | low | 2866 | 2641 | 220 | 1200 | 10000 | 1879.11 | stop |
| 11 | section_summary | low | 806 | 581 | 159 | 1200 | 10000 | 1397.72 | stop |
| 12 | section_summary | low | 713 | 488 | 117 | 1200 | 10000 | 1467.63 | stop |
| 13 | section_summary | low | 2469 | 2244 | 590 | 1200 | 10000 | 2504.55 | stop |
| 14 | section_summary | low | 1532 | 1307 | 380 | 1200 | 10000 | 2691.33 | stop |
| 15 | section_summary | low | 790 | 565 | 158 | 1200 | 10000 | 1526.87 | stop |
| 16 | section_summary | low | 1404 | 1179 | 329 | 1200 | 10000 | 2785.10 | stop |
| 17 | section_summary | low | 2531 | 2306 | 205 | 1200 | 10000 | 2311.06 | stop |
| 18 | section_summary | low | 790 | 565 | 187 | 1200 | 10000 | 2206.53 | stop |
| 19 | section_summary | low | 1065 | 840 | 169 | 1200 | 10000 | 1496.61 | stop |
| 20 | section_summary | low | 1541 | 1316 | 279 | 1200 | 10000 | 2543.78 | stop |
| 21 | section_summary | low | 953 | 728 | 134 | 1200 | 10000 | 1846.13 | stop |
| 22 | section_summary | low | 1324 | 1099 | 261 | 1200 | 10000 | 1411.10 | stop |
| 23 | section_summary | low | 1699 | 1474 | 355 | 1200 | 10000 | 1833.64 | stop |
| 24 | section_summary | low | 905 | 680 | 145 | 1200 | 10000 | 1904.32 | stop |
| 25 | section_summary | low | 2926 | 2701 | 684 | 1200 | 10000 | 4055.60 | stop |
| 26 | section_summary | low | 1727 | 1502 | 261 | 1200 | 10000 | 2617.85 | stop |
| 27 | section_summary | low | 2988 | 2763 | 238 | 1200 | 10000 | 1718.01 | stop |
| 28 | section_summary | low | 5108 | 4883 | 1200 | 1200 | 10000 | 5313.78 | length |
| 29 | section_summary | low | 921 | 696 | 159 | 1200 | 10000 | 2831.80 | stop |
| 30 | section_summary | low | 2788 | 2563 | 999 | 1200 | 10000 | 4969.62 | stop |
| 31 | section_summary | low | 5170 | 4945 | 293 | 1200 | 10000 | 2561.94 | stop |
| 32 | section_summary | low | 2587 | 2362 | 547 | 1200 | 10000 | 3950.97 | stop |
| 33 | section_summary | low | 7214 | 6947 | 432 | 1200 | 10000 | 3039.68 | stop |
| 34 | section_summary | low | 2850 | 2625 | 170 | 1200 | 10000 | 3349.44 | stop |
| 35 | section_summary | low | 2649 | 2424 | 208 | 1200 | 10000 | 2582.87 | stop |
| 36 | section_summary | low | 7248 | 6981 | 239 | 1200 | 10000 | 2967.66 | stop |
| 37 | section_summary | low | 3803 | 3578 | 983 | 1200 | 10000 | 4848.37 | stop |
| 38 | section_summary | low | 6046 | 5779 | 458 | 1200 | 10000 | 2639.95 | stop |
| 39 | section_summary | low | 2715 | 2490 | 955 | 1200 | 10000 | 4729.41 | stop |
| 40 | section_summary | low | 4389 | 4122 | 241 | 1200 | 10000 | 2529.23 | stop |
| 41 | section_summary | low | 3865 | 3640 | 240 | 1200 | 10000 | 2206.83 | stop |
| 42 | section_summary | low | 2777 | 2552 | 201 | 1200 | 10000 | 1485.19 | stop |
| 43 | section_summary | low | 6674 | 6407 | 347 | 1200 | 10000 | 2640.72 | stop |
| 44 | section_summary | low | 2636 | 2369 | 294 | 1200 | 10000 | 2263.29 | stop |
| 45 | section_summary | low | 4610 | 4343 | 150 | 1200 | 10000 | 1650.53 | stop |
| 46 | section_summary | low | 6402 | 6135 | 463 | 1200 | 10000 | 2649.18 | stop |
| 47 | section_summary | low | 6708 | 6441 | 272 | 1200 | 10000 | 1863.36 | stop |
| 48 | section_summary | low | 6527 | 6260 | 142 | 1200 | 10000 | 1290.69 | stop |
| 49 | section_summary | low | 2676 | 2409 | 367 | 1200 | 10000 | 3063.96 | stop |
| 50 | section_summary | low | 6442 | 6175 | 384 | 1200 | 10000 | 2292.88 | stop |
| 51 | section_summary | low | 6525 | 6258 | 144 | 1200 | 10000 | 1611.52 | stop |
| 52 | section_summary | low | 2670 | 2403 | 205 | 1200 | 10000 | 1359.16 | stop |
| 53 | section_summary | low | 5598 | 5331 | 133 | 1200 | 10000 | 1025.94 | stop |
| 54 | section_summary | low | 6756 | 6489 | 566 | 1200 | 10000 | 2473.49 | stop |
| 55 | section_summary | low | 6875 | 6608 | 153 | 1200 | 10000 | 1163.88 | stop |
| 56 | section_summary | low | 6790 | 6523 | 195 | 1200 | 10000 | 1351.07 | stop |
| 57 | section_summary | low | 5572 | 5305 | 214 | 1200 | 10000 | 3514.44 | stop |
| 58 | section_summary | low | 6790 | 6523 | 300 | 1200 | 10000 | 3730.28 | stop |
| 59 | section_summary | low | 4944 | 4677 | 184 | 1200 | 10000 | 1528.04 | stop |
| 60 | section_summary | low | 5429 | 5162 | 183 | 1200 | 10000 | 1596.77 | stop |
| 61 | section_summary | low | 5572 | 5305 | 148 | 1200 | 10000 | 1274.48 | stop |
| 62 | section_summary | low | 6772 | 6505 | 716 | 1200 | 10000 | 3555.53 | stop |
| 63 | section_summary | low | 6555 | 6288 | 143 | 1200 | 10000 | 1262.97 | stop |
| 64 | section_summary | low | 5588 | 5321 | 116 | 1200 | 10000 | 1125.17 | stop |
| 65 | section_summary | low | 6671 | 6404 | 556 | 1200 | 10000 | 2232.50 | stop |
| 66 | section_summary | low | 7211 | 6944 | 303 | 1200 | 10000 | 1657.92 | stop |
| 67 | section_summary | low | 6713 | 6446 | 387 | 1200 | 10000 | 1687.43 | stop |
| 68 | section_summary | low | 7251 | 6984 | 231 | 1200 | 10000 | 1584.16 | stop |
| 69 | section_summary | low | 8350 | 8083 | 287 | 1200 | 10000 | 1350.11 | stop |
| 70 | section_summary | low | 6784 | 6517 | 601 | 1200 | 10000 | 2727.29 | stop |
| 71 | section_summary | low | 7159 | 6892 | 332 | 1200 | 10000 | 1592.08 | stop |
| 72 | section_summary | low | 6747 | 6480 | 682 | 1200 | 10000 | 2340.12 | stop |
| 73 | section_summary | low | 2203 | 1936 | 560 | 1200 | 10000 | 2583.34 | stop |
| 74 | section_summary | low | 6781 | 6514 | 454 | 1200 | 10000 | 2147.16 | stop |
| 75 | section_summary | low | 2237 | 1970 | 278 | 1200 | 10000 | 1659.44 | stop |
| 76 | section_summary | low | 6787 | 6520 | 513 | 1200 | 10000 | 2677.05 | stop |
| 77 | section_summary | low | 2243 | 1976 | 500 | 1200 | 10000 | 2826.20 | stop |
| 78 | section_summary | low | 4170 | 3903 | 308 | 1200 | 10000 | 2252.58 | stop |
| 79 | section_summary | low | 8610 | 8343 | 237 | 1200 | 10000 | 1643.89 | stop |
| 80 | section_summary | low | 4204 | 3937 | 261 | 1200 | 10000 | 1930.95 | stop |
| 81 | section_summary | low | 8650 | 8383 | 131 | 1200 | 10000 | 1193.07 | stop |
| 82 | section_summary | low | 4204 | 3937 | 361 | 1200 | 10000 | 1859.69 | stop |
| 83 | section_summary | low | 6422 | 6155 | 505 | 1200 | 10000 | 2196.13 | stop |
| 84 | section_summary | low | 4210 | 3943 | 278 | 1200 | 10000 | 2004.63 | stop |
| 85 | section_summary | low | 6462 | 6195 | 312 | 1200 | 10000 | 1907.27 | stop |
| 86 | section_summary | low | 8542 | 8275 | 259 | 1200 | 10000 | 1511.85 | stop |
| 87 | section_summary | low | 2960 | 2693 | 270 | 1200 | 10000 | 1593.61 | stop |
| 88 | section_summary | low | 849 | 582 | 83 | 1200 | 10000 | 697.38 | stop |
| 89 | section_summary | low | 883 | 616 | 49 | 1200 | 10000 | 829.15 | stop |
| 90 | section_summary | low | 2994 | 2727 | 221 | 1200 | 10000 | 1503.56 | stop |
| 91 | section_summary | low | 889 | 622 | 112 | 1200 | 10000 | 837.62 | stop |
| 92 | section_summary | low | 2994 | 2727 | 157 | 1200 | 10000 | 1093.48 | stop |
| 93 | section_summary | low | 883 | 616 | 49 | 1200 | 10000 | 648.55 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: None; expected: Lookup / Synthesis

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.05

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup / Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_NUMBER — repetition 2

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: None; expected: Lookup / Synthesis

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.01

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup / Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_NUMBER — repetition 3

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: None; expected: Lookup / Synthesis

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.01

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup / Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: None; expected: Global

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.01

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_SUMMARY — repetition 2

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: None; expected: Global

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.01

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_SUMMARY — repetition 3

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: None; expected: Global

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.00

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Selected source length 74; rendered length 92 |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>
