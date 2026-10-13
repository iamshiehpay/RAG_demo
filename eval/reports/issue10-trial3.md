# Golden Facts evaluation

Created: 2026-10-13T04:39:30.979856+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-35445d9cb54a39e36d6bf773a9d35c7e8a4b875d901211c3a305b1ecf9279187

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

Upload failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload.

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
| 1 | section_summary | low | 696 | 471 | 110 | 1200 | 10000 | 1766.03 | stop |
| 2 | section_summary | low | 2679 | 2454 | 512 | 1200 | 10000 | 2297.32 | stop |
| 3 | section_summary | low | 2650 | 2425 | 578 | 1200 | 10000 | 2466.11 | stop |
| 4 | section_summary | low | 1576 | 1351 | 339 | 1200 | 10000 | 2558.16 | stop |
| 5 | section_summary | low | 569 | 344 | 71 | 1200 | 10000 | 759.13 | stop |
| 6 | section_summary | low | 993 | 768 | 153 | 1200 | 10000 | 1094.75 | stop |
| 7 | section_summary | low | 1076 | 851 | 315 | 1200 | 10000 | 1617.13 | stop |
| 8 | section_summary | low | 1938 | 1713 | 329 | 1200 | 10000 | 2486.39 | stop |
| 9 | section_summary | low | 553 | 328 | 72 | 1200 | 10000 | 1422.47 | stop |
| 10 | section_summary | low | 2313 | 2088 | 301 | 1200 | 10000 | 1775.59 | stop |
| 11 | section_summary | low | 1374 | 1149 | 262 | 1200 | 10000 | 1484.71 | stop |
| 12 | section_summary | low | 1244 | 1019 | 220 | 1200 | 10000 | 1383.20 | stop |
| 13 | section_summary | low | 907 | 682 | 107 | 1200 | 10000 | 809.59 | stop |
| 14 | section_summary | low | 1383 | 1158 | 242 | 1200 | 10000 | 1383.39 | stop |
| 15 | section_summary | low | 793 | 568 | 100 | 1200 | 10000 | 799.72 | stop |
| 16 | section_summary | low | 745 | 520 | 102 | 1200 | 10000 | 796.81 | stop |
| 17 | section_summary | low | 1541 | 1316 | 272 | 1200 | 10000 | 1794.04 | stop |
| 18 | section_summary | low | 1166 | 941 | 207 | 1200 | 10000 | 1818.15 | stop |
| 19 | section_summary | low | 1569 | 1344 | 205 | 1200 | 10000 | 1417.68 | stop |
| 20 | section_summary | low | 2770 | 2545 | 518 | 1200 | 10000 | 3344.45 | stop |
| 21 | section_summary | low | 763 | 538 | 121 | 1200 | 10000 | 913.02 | stop |
| 22 | section_summary | low | 2632 | 2407 | 502 | 1200 | 10000 | 2607.09 | stop |
| 23 | section_summary | low | 4958 | 4733 | 761 | 1200 | 10000 | 3483.79 | stop |
| 24 | section_summary | low | 2429 | 2204 | 384 | 1200 | 10000 | 1927.86 | stop |
| 25 | section_summary | low | 1259 | 1034 | 533 | 1200 | 10000 | 2084.75 | stop |
| 26 | section_summary | low | 3651 | 3426 | 691 | 1200 | 10000 | 2817.10 | stop |
| 27 | section_summary | low | 3525 | 3300 | 801 | 1200 | 10000 | 3450.53 | stop |
| 28 | section_summary | low | 2559 | 2334 | 465 | 1200 | 10000 | 2488.82 | stop |
| 29 | section_summary | low | 1033 | 808 | 503 | 1200 | 10000 | 1390.72 | stop |
| 30 | section_summary | low | 1324 | 1099 | 485 | 1200 | 10000 | 1598.76 | stop |
| 31 | section_summary | low | 1210 | 985 | 564 | 1200 | 10000 | 1713.57 | stop |
| 32 | section_summary | low | 1729 | 1504 | 297 | 1200 | 10000 | 1722.13 | stop |
| 33 | section_summary | low | 2073 | 1848 | 406 | 1200 | 10000 | 2350.64 | stop |
| 34 | section_summary | low | 1080 | 855 | 558 | 1200 | 10000 | 1897.23 | stop |

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

Total evaluation latency_ms: 0.11

Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload.

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Lookup; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload. |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload. |  |

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

Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload.

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Global; actual None; plan_source=None; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>
