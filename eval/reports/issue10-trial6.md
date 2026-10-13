# Golden Facts evaluation

Created: 2026-10-13T04:57:42.931104+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-ea3d883315915fcb0f2566399058c677c5a21244ca40f87725c9d3cd1a06eabf

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
| 1 | section_summary | low | 785 | 560 | 121 | 1200 | 10000 | 1621.72 | stop |
| 2 | section_summary | low | 1665 | 1440 | 333 | 1200 | 10000 | 2530.51 | stop |
| 3 | section_summary | low | 2768 | 2543 | 473 | 1200 | 10000 | 2978.37 | stop |
| 4 | section_summary | low | 2739 | 2514 | 437 | 1200 | 10000 | 3061.43 | stop |
| 5 | section_summary | low | 658 | 433 | 83 | 1200 | 10000 | 719.51 | stop |
| 6 | section_summary | low | 2027 | 1802 | 327 | 1200 | 10000 | 2274.71 | stop |
| 7 | section_summary | low | 1082 | 857 | 146 | 1200 | 10000 | 1643.70 | stop |
| 8 | section_summary | low | 642 | 417 | 133 | 1200 | 10000 | 954.95 | stop |
| 9 | section_summary | low | 2402 | 2177 | 311 | 1200 | 10000 | 2221.71 | stop |
| 10 | section_summary | low | 1463 | 1238 | 228 | 1200 | 10000 | 1410.87 | stop |
| 11 | section_summary | low | 1333 | 1108 | 236 | 1200 | 10000 | 1406.08 | stop |
| 12 | section_summary | low | 1472 | 1247 | 255 | 1200 | 10000 | 1210.32 | stop |
| 13 | section_summary | low | 996 | 771 | 121 | 1200 | 10000 | 795.81 | stop |
| 14 | section_summary | low | 882 | 657 | 86 | 1200 | 10000 | 1329.73 | stop |
| 15 | section_summary | low | 1255 | 1030 | 170 | 1200 | 10000 | 1014.18 | stop |
| 16 | section_summary | low | 1630 | 1405 | 297 | 1200 | 10000 | 1314.31 | stop |
| 17 | section_summary | low | 834 | 609 | 96 | 1200 | 10000 | 1081.49 | stop |
| 18 | section_summary | low | 1658 | 1433 | 228 | 1200 | 10000 | 1391.81 | stop |
| 19 | section_summary | low | 2859 | 2634 | 549 | 1200 | 10000 | 2603.81 | stop |
| 20 | section_summary | low | 852 | 627 | 123 | 1200 | 10000 | 959.65 | stop |
| 21 | section_summary | low | 5047 | 4822 | 735 | 1200 | 10000 | 3198.98 | stop |
| 22 | section_summary | low | 1136 | 911 | 370 | 1200 | 10000 | 1560.65 | stop |
| 23 | section_summary | low | 2721 | 2496 | 402 | 1200 | 10000 | 2693.03 | stop |
| 24 | section_summary | low | 2518 | 2293 | 377 | 1200 | 10000 | 1761.64 | stop |
| 25 | section_summary | low | 1322 | 1097 | 383 | 1200 | 10000 | 1404.75 | stop |
| 26 | section_summary | low | 2648 | 2423 | 466 | 1200 | 10000 | 2232.05 | stop |
| 27 | section_summary | low | 1818 | 1593 | 342 | 1200 | 10000 | 2007.44 | stop |
| 28 | section_summary | low | 3740 | 3515 | 809 | 1200 | 10000 | 4110.32 | stop |
| 29 | section_summary | low | 3614 | 3389 | 929 | 1200 | 10000 | 4842.75 | stop |
| 30 | section_summary | low | 2162 | 1937 | 412 | 1200 | 10000 | 2372.63 | stop |
| 31 | section_summary | low | 1417 | 1192 | 355 | 1200 | 10000 | 1447.50 | stop |
| 32 | section_summary | low | 1541 | 1316 | 399 | 1200 | 10000 | 1572.41 | stop |
| 33 | section_summary | low | 7124 | 6899 | 693 | 1200 | 10000 | 3121.77 | stop |
| 34 | section_summary | low | 8155 | 7930 | 1200 | 1200 | 10000 | 5373.24 | length |
| 35 | section_summary | low | 7136 | 6911 | 569 | 1200 | 10000 | 2974.04 | stop |
| 36 | section_summary | low | 8206 | 7981 | 562 | 1200 | 10000 | 3036.29 | stop |
| 37 | section_summary | low | 2053 | 1828 | 388 | 1200 | 10000 | 2084.46 | stop |
| 38 | section_summary | low | 8643 | 8418 | 1179 | 1200 | 10000 | 4746.17 | stop |
| 39 | section_summary | low | 1495 | 1270 | 866 | 1200 | 10000 | 2790.00 | stop |
| 40 | section_summary | low | 1445 | 1220 | 518 | 1200 | 10000 | 1818.81 | stop |
| 41 | section_summary | low | 1474 | 1249 | 555 | 1200 | 10000 | 1834.80 | stop |
| 42 | section_summary | low | 1163 | 938 | 553 | 1200 | 10000 | 1674.33 | stop |

## SECOND_NUMBER — repetition 1

Question: Identify the manually annotated expert-validation subset. In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: None; expected: Synthesis

Plan source: None

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 

Sub-queries: []

Ask latency_ms: 0.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 0.41

Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload.

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | FAIL | Expected Synthesis; actual None; plan_source=None; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload. |  |
| no_filter_improvement | forbidden | FAIL | Application failure: ingestion_failed: Document summary failed: Summary length could not be met. Please retry upload. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

### Finalized answer

<pre></pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations (including validation scope and missing reported evidence), and give the purpose of each appendix.

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
