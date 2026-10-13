# Golden Facts evaluation

Created: 2026-10-13T04:30:56.099595+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-4ac5310e37a71174a9a056a31b524e19d0b88688b65b1fc604bc1b40f6154a41

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
| 1 | section_summary | low | 645 | 420 | 123 | 1200 | 10000 | 1127.19 | stop |
| 2 | section_summary | low | 1525 | 1300 | 318 | 1200 | 10000 | 2408.01 | stop |
| 3 | section_summary | low | 942 | 717 | 165 | 1200 | 10000 | 2274.18 | stop |
| 4 | section_summary | low | 1887 | 1662 | 390 | 1200 | 10000 | 3652.72 | stop |
| 5 | section_summary | low | 2599 | 2374 | 828 | 1200 | 10000 | 4855.33 | stop |
| 6 | section_summary | low | 2628 | 2403 | 820 | 1200 | 10000 | 5211.61 | stop |
| 7 | section_summary | low | 518 | 293 | 84 | 1200 | 10000 | 847.40 | stop |
| 8 | section_summary | low | 502 | 277 | 70 | 1200 | 10000 | 800.93 | stop |
| 9 | section_summary | low | 1323 | 1098 | 311 | 1200 | 10000 | 2926.22 | stop |
| 10 | section_summary | low | 2262 | 2037 | 466 | 1200 | 10000 | 3482.37 | stop |
| 11 | section_summary | low | 1332 | 1107 | 321 | 1200 | 10000 | 3179.83 | stop |
| 12 | section_summary | low | 1193 | 968 | 338 | 1200 | 10000 | 3425.42 | stop |
| 13 | section_summary | low | 742 | 517 | 123 | 1200 | 10000 | 1767.99 | stop |
| 14 | section_summary | low | 856 | 631 | 163 | 1200 | 10000 | 2044.90 | stop |
| 15 | section_summary | low | 694 | 469 | 161 | 1200 | 10000 | 1709.21 | stop |
| 16 | section_summary | low | 1115 | 890 | 285 | 1200 | 10000 | 3076.08 | stop |
| 17 | section_summary | low | 1490 | 1265 | 321 | 1200 | 10000 | 3305.48 | stop |
| 18 | section_summary | low | 1518 | 1293 | 341 | 1200 | 10000 | 3063.77 | stop |
| 19 | section_summary | low | 2719 | 2494 | 718 | 1200 | 10000 | 5892.25 | stop |
| 20 | section_summary | low | 712 | 487 | 153 | 1200 | 10000 | 1307.51 | stop |
| 21 | section_summary | low | 2581 | 2356 | 609 | 1200 | 10000 | 4720.69 | stop |
| 22 | section_summary | low | 4907 | 4682 | 1200 | 1200 | 10000 | 7527.17 | length |

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

Total evaluation latency_ms: 0.04

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

Total evaluation latency_ms: 0.01

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
