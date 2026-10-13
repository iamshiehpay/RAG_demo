# Golden Facts evaluation

Created: 2026-10-13T08:52:56.472042+00:00

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

Upload failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

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
| 1 | section_summary | low | 922 | 697 | 168 | 1200 | 10000 | 1095.02 | stop |
| 2 | section_summary | low | 854 | 629 | 198 | 1200 | 10000 | 1091.20 | stop |
| 3 | section_summary | low | 1734 | 1509 | 470 | 1200 | 10000 | 2040.24 | stop |
| 4 | section_summary | low | 2835 | 2610 | 886 | 1200 | 10000 | 3107.41 | stop |
| 5 | section_summary | low | 2804 | 2579 | 797 | 1200 | 10000 | 3407.55 | stop |
| 6 | section_summary | low | 2094 | 1869 | 415 | 1200 | 10000 | 2337.95 | stop |
| 7 | section_summary | low | 729 | 504 | 67 | 1200 | 10000 | 604.08 | stop |
| 8 | section_summary | low | 1151 | 926 | 205 | 1200 | 10000 | 991.96 | stop |
| 9 | section_summary | low | 2866 | 2641 | 160 | 1200 | 10000 | 1046.02 | stop |
| 10 | section_summary | low | 2897 | 2672 | 179 | 1200 | 10000 | 1641.34 | stop |
| 11 | section_summary | low | 713 | 488 | 112 | 1200 | 10000 | 918.87 | stop |
| 12 | section_summary | low | 806 | 581 | 237 | 1200 | 10000 | 1874.25 | stop |
| 13 | section_summary | low | 2469 | 2244 | 650 | 1200 | 10000 | 2427.85 | stop |
| 14 | section_summary | low | 790 | 565 | 215 | 1200 | 10000 | 1175.39 | stop |
| 15 | section_summary | low | 1532 | 1307 | 422 | 1200 | 10000 | 1795.48 | stop |
| 16 | section_summary | low | 1404 | 1179 | 330 | 1200 | 10000 | 1416.85 | stop |
| 17 | section_summary | low | 1065 | 840 | 170 | 1200 | 10000 | 1042.75 | stop |
| 18 | section_summary | low | 2531 | 2306 | 196 | 1200 | 10000 | 1188.29 | stop |
| 19 | section_summary | low | 1541 | 1316 | 289 | 1200 | 10000 | 1260.95 | stop |
| 20 | section_summary | low | 953 | 728 | 134 | 1200 | 10000 | 734.64 | stop |
| 21 | section_summary | low | 1324 | 1099 | 279 | 1200 | 10000 | 1307.69 | stop |
| 22 | section_summary | low | 905 | 680 | 146 | 1200 | 10000 | 1145.02 | stop |
| 23 | section_summary | low | 1699 | 1474 | 310 | 1200 | 10000 | 2059.90 | stop |
| 24 | section_summary | low | 2926 | 2701 | 780 | 1200 | 10000 | 2740.92 | stop |
| 25 | section_summary | low | 1727 | 1502 | 306 | 1200 | 10000 | 1386.46 | stop |
| 26 | section_summary | low | 921 | 696 | 160 | 1200 | 10000 | 1041.40 | stop |
| 27 | section_summary | low | 2988 | 2763 | 217 | 1200 | 10000 | 1470.75 | stop |
| 28 | section_summary | low | 2788 | 2563 | 1122 | 1200 | 10000 | 4105.97 | stop |
| 29 | section_summary | low | 7200 | 6933 | 274 | 1200 | 10000 | 1734.93 | stop |
| 30 | section_summary | low | 5108 | 4883 | 1200 | 1200 | 10000 | 4891.94 | length |
| 31 | section_summary | low | 2587 | 2362 | 702 | 1200 | 10000 | 3114.21 | stop |
| 32 | section_summary | low | 2850 | 2625 | 137 | 1200 | 10000 | 1250.35 | stop |
| 33 | section_summary | low | 4385 | 4118 | 261 | 1200 | 10000 | 1582.37 | stop |
| 34 | section_summary | low | 5170 | 4945 | 328 | 1200 | 10000 | 2073.69 | stop |
| 35 | section_summary | low | 2649 | 2424 | 247 | 1200 | 10000 | 1517.22 | stop |
| 36 | section_summary | low | 2583 | 2316 | 314 | 1200 | 10000 | 1592.49 | stop |
| 37 | section_summary | low | 6042 | 5775 | 242 | 1200 | 10000 | 1524.20 | stop |
| 38 | section_summary | low | 3803 | 3578 | 1062 | 1200 | 10000 | 4078.78 | stop |
| 39 | section_summary | low | 2715 | 2490 | 959 | 1200 | 10000 | 3444.14 | stop |
| 40 | section_summary | low | 6670 | 6403 | 524 | 1200 | 10000 | 2839.78 | stop |
| 41 | section_summary | low | 6398 | 6131 | 496 | 1200 | 10000 | 2134.20 | stop |
| 42 | section_summary | low | 3865 | 3640 | 266 | 1200 | 10000 | 1344.18 | stop |
| 43 | section_summary | low | 2777 | 2552 | 203 | 1200 | 10000 | 1272.66 | stop |
| 44 | section_summary | low | 4608 | 4341 | 155 | 1200 | 10000 | 1046.60 | stop |
| 45 | section_summary | low | 6432 | 6165 | 461 | 1200 | 10000 | 1794.76 | stop |
| 46 | section_summary | low | 6523 | 6256 | 221 | 1200 | 10000 | 1397.60 | stop |
| 47 | section_summary | low | 6563 | 6296 | 149 | 1200 | 10000 | 1193.45 | stop |
| 48 | section_summary | low | 6432 | 6165 | 515 | 1200 | 10000 | 2198.14 | stop |
| 49 | section_summary | low | 6521 | 6254 | 163 | 1200 | 10000 | 1275.72 | stop |
| 50 | section_summary | low | 6555 | 6288 | 185 | 1200 | 10000 | 1333.72 | stop |
| 51 | section_summary | low | 6432 | 6165 | 516 | 1200 | 10000 | 2231.34 | stop |

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

Total evaluation latency_ms: 0.03

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup / Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |

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

Total evaluation latency_ms: 0.00

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup / Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |

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

Total evaluation latency_ms: 0.00

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup / Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |

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

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |

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

Total evaluation latency_ms: 0.00

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |

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

Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary selection failed after bounded correction: Expected only span_ids |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>
