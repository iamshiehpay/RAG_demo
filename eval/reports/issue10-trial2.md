# Golden Facts evaluation

Created: 2026-10-13T04:34:03.705336+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-de907714e759b41eaddae642f32ac555a895d8e5343b90b15de8e18b3fef52a8

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

Upload failure: ingestion_failed: Document summary failed: Section summary was truncated. Please retry.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | question_type | events | 0/1 (0.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/1 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 0/1 (0.0%) |
| SECOND_SUMMARY | question_type | events | 0/1 (0.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/1 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 695 | 470 | 140 | 1200 | 10000 | 1390.76 | stop |
| 2 | section_summary | low | 1575 | 1350 | 371 | 1200 | 10000 | 2833.81 | stop |
| 3 | section_summary | low | 2678 | 2453 | 586 | 1200 | 10000 | 3169.21 | stop |
| 4 | section_summary | low | 568 | 343 | 81 | 1200 | 10000 | 748.47 | stop |
| 5 | section_summary | low | 2649 | 2424 | 658 | 1200 | 10000 | 4010.69 | stop |
| 6 | section_summary | low | 992 | 767 | 168 | 1200 | 10000 | 1189.01 | stop |
| 7 | section_summary | low | 1937 | 1712 | 383 | 1200 | 10000 | 2712.17 | stop |
| 8 | section_summary | low | 552 | 327 | 67 | 1200 | 10000 | 1492.86 | stop |
| 9 | section_summary | low | 1243 | 1018 | 284 | 1200 | 10000 | 1810.02 | stop |
| 10 | section_summary | low | 2312 | 2087 | 307 | 1200 | 10000 | 2496.55 | stop |
| 11 | section_summary | low | 1373 | 1148 | 292 | 1200 | 10000 | 2521.56 | stop |
| 12 | section_summary | low | 906 | 681 | 156 | 1200 | 10000 | 1222.57 | stop |
| 13 | section_summary | low | 792 | 567 | 108 | 1200 | 10000 | 1122.18 | stop |
| 14 | section_summary | low | 1382 | 1157 | 284 | 1200 | 10000 | 2189.19 | stop |
| 15 | section_summary | low | 1540 | 1315 | 302 | 1200 | 10000 | 1793.09 | stop |
| 16 | section_summary | low | 744 | 519 | 100 | 1200 | 10000 | 944.00 | stop |
| 17 | section_summary | low | 1165 | 940 | 297 | 1200 | 10000 | 2252.80 | stop |
| 18 | section_summary | low | 1568 | 1343 | 212 | 1200 | 10000 | 1458.11 | stop |
| 19 | section_summary | low | 2769 | 2544 | 664 | 1200 | 10000 | 3847.53 | stop |
| 20 | section_summary | low | 762 | 537 | 111 | 1200 | 10000 | 1637.91 | stop |
| 21 | section_summary | low | 4957 | 4732 | 857 | 1200 | 10000 | 4459.27 | stop |
| 22 | section_summary | low | 2631 | 2406 | 703 | 1200 | 10000 | 3777.57 | stop |
| 23 | section_summary | low | 2428 | 2203 | 482 | 1200 | 10000 | 2663.84 | stop |
| 24 | section_summary | low | 3524 | 3299 | 786 | 1200 | 10000 | 3903.34 | stop |
| 25 | section_summary | low | 1728 | 1503 | 328 | 1200 | 10000 | 1934.93 | stop |
| 26 | section_summary | low | 3650 | 3425 | 910 | 1200 | 10000 | 3915.38 | stop |
| 27 | section_summary | low | 2558 | 2333 | 919 | 1200 | 10000 | 4002.73 | stop |
| 28 | section_summary | low | 2072 | 1847 | 459 | 1200 | 10000 | 2553.04 | stop |
| 29 | section_summary | low | 7034 | 6809 | 709 | 1200 | 10000 | 3083.99 | stop |
| 30 | section_summary | low | 8065 | 7840 | 1200 | 1200 | 10000 | 5348.70 | length |

## SECOND_NUMBER — repetition 1

Question: In the expert-validation comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: None; expected: Lookup

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.07

Application failure: ingestion_failed: Document summary failed: Section summary was truncated. Please retry.

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Section summary was truncated. Please retry. |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Section summary was truncated. Please retry. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations, including what the appendices contribute.

Question Type: None; expected: Global

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.02

Application failure: ingestion_failed: Document summary failed: Section summary was truncated. Please retry.

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Section summary was truncated. Please retry. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>
