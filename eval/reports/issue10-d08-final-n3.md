# Golden Facts evaluation

Created: 2026-10-13T09:24:53.197858+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 3

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 79d0f55321874806091ce08668c7ec991562dd90

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-02fd2cb4e73f4747cb9137caa5187680561716d41d3edc4ce4fd5a83a5cd7fc7

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | required_source_citation | events | 3/3 (100.0%) |
| SECOND_NUMBER | question_type | events | 3/3 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 1/3 (33.3%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 3/3 (100.0%) |
| SECOND_SUMMARY | question_type | events | 3/3 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/3 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 854 | 629 | 136 | 1200 | 10000 | 1027.43 | stop |
| 2 | section_summary | low | 922 | 697 | 210 | 1200 | 10000 | 2085.19 | stop |
| 3 | section_summary | low | 1734 | 1509 | 408 | 1200 | 10000 | 2001.40 | stop |
| 4 | section_summary | low | 2835 | 2610 | 708 | 1200 | 10000 | 3786.40 | stop |
| 5 | section_summary | low | 2804 | 2579 | 896 | 1200 | 10000 | 4262.50 | stop |
| 6 | section_summary | low | 2094 | 1869 | 366 | 1200 | 10000 | 2453.63 | stop |
| 7 | section_summary | low | 1151 | 926 | 218 | 1200 | 10000 | 1712.66 | stop |
| 8 | section_summary | low | 729 | 504 | 67 | 1200 | 10000 | 681.61 | stop |
| 9 | section_summary | low | 2897 | 2672 | 155 | 1200 | 10000 | 1235.64 | stop |
| 10 | section_summary | low | 2866 | 2641 | 163 | 1200 | 10000 | 1262.89 | stop |
| 11 | section_summary | low | 713 | 488 | 121 | 1200 | 10000 | 1000.84 | stop |
| 12 | section_summary | low | 2469 | 2244 | 353 | 1200 | 10000 | 1972.56 | stop |
| 13 | section_summary | low | 806 | 581 | 149 | 1200 | 10000 | 1769.32 | stop |
| 14 | section_summary | low | 790 | 565 | 106 | 1200 | 10000 | 884.92 | stop |
| 15 | section_summary | low | 1532 | 1307 | 391 | 1200 | 10000 | 2007.08 | stop |
| 16 | section_summary | low | 806 | 581 | 179 | 1200 | 10000 | 1018.92 | stop |
| 17 | section_summary | low | 1065 | 840 | 174 | 1200 | 10000 | 1140.45 | stop |
| 18 | section_summary | low | 1404 | 1179 | 414 | 1200 | 10000 | 1963.81 | stop |
| 19 | section_summary | low | 1541 | 1316 | 288 | 1200 | 10000 | 1628.36 | stop |
| 20 | section_summary | low | 953 | 728 | 152 | 1200 | 10000 | 964.23 | stop |
| 21 | section_summary | low | 905 | 680 | 117 | 1200 | 10000 | 926.54 | stop |
| 22 | section_summary | low | 1324 | 1099 | 280 | 1200 | 10000 | 1517.97 | stop |
| 23 | section_summary | low | 1699 | 1474 | 336 | 1200 | 10000 | 1764.80 | stop |
| 24 | section_summary | low | 1727 | 1502 | 302 | 1200 | 10000 | 1598.85 | stop |
| 25 | section_summary | low | 2926 | 2701 | 793 | 1200 | 10000 | 3160.53 | stop |
| 26 | section_summary | low | 921 | 696 | 159 | 1200 | 10000 | 1123.31 | stop |
| 27 | section_summary | low | 2988 | 2763 | 237 | 1200 | 10000 | 1618.90 | stop |
| 28 | section_summary | low | 2788 | 2563 | 892 | 1200 | 10000 | 3486.91 | stop |
| 29 | section_summary | low | 5108 | 4883 | 1200 | 1200 | 10000 | 4291.81 | length |
| 30 | section_summary | low | 2587 | 2362 | 532 | 1200 | 10000 | 2506.15 | stop |
| 31 | section_summary | low | 7200 | 6933 | 112 | 1200 | 10000 | 1753.04 | stop |
| 32 | section_summary | low | 2850 | 2625 | 154 | 1200 | 10000 | 1787.42 | stop |
| 33 | section_summary | low | 5170 | 4945 | 398 | 1200 | 10000 | 2673.21 | stop |
| 34 | section_summary | low | 2649 | 2424 | 205 | 1200 | 10000 | 1542.90 | stop |
| 35 | section_summary | low | 7240 | 6973 | 290 | 1200 | 10000 | 1756.60 | stop |
| 36 | section_summary | low | 7240 | 6973 | 187 | 1200 | 10000 | 1535.75 | stop |
| 37 | section_summary | low | 6042 | 5775 | 276 | 1200 | 10000 | 1918.20 | stop |
| 38 | section_summary | low | 7240 | 6973 | 224 | 1200 | 10000 | 1746.91 | stop |
| 39 | section_summary | low | 3803 | 3578 | 1200 | 1200 | 10000 | 5066.46 | length |
| 40 | section_summary | low | 6670 | 6403 | 262 | 1200 | 10000 | 1942.04 | stop |
| 41 | section_summary | low | 2715 | 2490 | 889 | 1200 | 10000 | 4138.59 | stop |
| 42 | section_summary | low | 4385 | 4118 | 212 | 1200 | 10000 | 1533.33 | stop |
| 43 | section_summary | low | 2777 | 2552 | 154 | 1200 | 10000 | 1311.11 | stop |
| 44 | section_summary | low | 3865 | 3640 | 346 | 1200 | 10000 | 2230.59 | stop |
| 45 | section_summary | low | 6398 | 6131 | 475 | 1200 | 10000 | 2063.14 | stop |
| 46 | section_summary | low | 4608 | 4341 | 155 | 1200 | 10000 | 1317.32 | stop |
| 47 | section_summary | low | 6523 | 6256 | 132 | 1200 | 10000 | 1131.63 | stop |
| 48 | section_summary | low | 6438 | 6171 | 557 | 1200 | 10000 | 2477.73 | stop |
| 49 | section_summary | low | 2289 | 2022 | 367 | 1200 | 10000 | 3385.82 | stop |
| 50 | section_summary | low | 6521 | 6254 | 167 | 1200 | 10000 | 1398.79 | stop |
| 51 | section_summary | low | 6752 | 6485 | 580 | 1200 | 10000 | 2363.71 | stop |
| 52 | section_summary | low | 5596 | 5329 | 146 | 1200 | 10000 | 1093.50 | stop |
| 53 | section_summary | low | 6871 | 6604 | 125 | 1200 | 10000 | 984.14 | stop |
| 54 | section_summary | low | 6768 | 6501 | 413 | 1200 | 10000 | 1980.60 | stop |
| 55 | section_summary | low | 6911 | 6644 | 122 | 1200 | 10000 | 1056.46 | stop |
| 56 | section_summary | low | 5570 | 5303 | 118 | 1200 | 10000 | 922.93 | stop |
| 57 | section_summary | low | 6667 | 6400 | 417 | 1200 | 10000 | 1423.71 | stop |
| 58 | section_summary | low | 5610 | 5343 | 223 | 1200 | 10000 | 1277.49 | stop |
| 59 | section_summary | low | 6707 | 6440 | 539 | 1200 | 10000 | 1925.35 | stop |
| 60 | section_summary | low | 4942 | 4675 | 206 | 1200 | 10000 | 1233.71 | stop |
| 61 | section_summary | low | 5427 | 5160 | 155 | 1200 | 10000 | 1139.08 | stop |
| 62 | section_summary | low | 6780 | 6513 | 321 | 1200 | 10000 | 1541.75 | stop |
| 63 | section_summary | low | 5570 | 5303 | 160 | 1200 | 10000 | 1242.49 | stop |
| 64 | section_summary | low | 6743 | 6476 | 621 | 1200 | 10000 | 2231.05 | stop |
| 65 | section_summary | low | 6551 | 6284 | 214 | 1200 | 10000 | 1234.70 | stop |
| 66 | section_summary | low | 6591 | 6324 | 142 | 1200 | 10000 | 1078.62 | stop |
| 67 | section_summary | low | 6783 | 6516 | 294 | 1200 | 10000 | 1570.26 | stop |
| 68 | section_summary | low | 5586 | 5319 | 163 | 1200 | 10000 | 1190.64 | stop |
| 69 | section_summary | low | 7207 | 6940 | 294 | 1200 | 10000 | 1691.16 | stop |
| 70 | section_summary | low | 4166 | 3899 | 523 | 1200 | 10000 | 2501.67 | stop |
| 71 | section_summary | low | 8340 | 8073 | 774 | 1200 | 10000 | 2631.77 | stop |
| 72 | section_summary | low | 7868 | 7601 | 758 | 1200 | 10000 | 3220.64 | stop |
| 73 | section_summary | low | 1982 | 1715 | 216 | 1200 | 10000 | 1296.63 | stop |
| 74 | section_summary | low | 8380 | 8113 | 494 | 1200 | 10000 | 2129.43 | stop |
| 75 | section_summary | low | 7151 | 6884 | 387 | 1200 | 10000 | 1788.86 | stop |
| 76 | section_summary | low | 2985 | 2718 | 656 | 1200 | 10000 | 2816.69 | stop |
| 77 | section_summary | low | 2201 | 1934 | 593 | 1200 | 10000 | 2319.48 | stop |
| 78 | section_summary | low | 8489 | 8222 | 199 | 1200 | 10000 | 1449.96 | stop |
| 79 | section_summary | low | 8529 | 8262 | 288 | 1200 | 10000 | 2127.98 | stop |
| 80 | section_summary | low | 7393 | 7126 | 264 | 1200 | 10000 | 1289.65 | stop |
| 81 | section_summary | low | 7433 | 7166 | 212 | 1200 | 10000 | 1321.85 | stop |
| 82 | section_summary | low | 3311 | 3044 | 196 | 1200 | 10000 | 1257.85 | stop |
| 83 | section_summary | low | 3351 | 3084 | 146 | 1200 | 10000 | 1099.85 | stop |
| 84 | group_summary | low | 6429 | 6204 | 1053 | 2500 | 10000 | 3270.23 | stop |
| 85 | group_summary | low | 3162 | 2937 | 684 | 2500 | 10000 | 2330.47 | stop |
| 86 | document_summary | low | 2692 | 2467 | 1534 | 2500 | 10000 | 2873.25 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation, and in that comparison how does InfoFound affect overall accuracy and positive-class F1 relative to All, including the evaluation counts for both settings?

Sub-queries: [&#x27;model papers manually annotated count&#x27;, &#x27;InfoFound vs All overall accuracy and positive-class F1&#x27;, &#x27;evaluation counts for InfoFound and All settings&#x27;]

Ask latency_ms: 3632.79

Judge latency_ms: 1769.22

Total evaluation latency_ms: 5423.21

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the expert‑LLM agreement analysis (Table 9), the “All” setting evaluated 447 criterion‑level decisions, achieving an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  <br>When restricting to the “InfoFound” subset (only cases where the LLM flagged the information as found), the evaluation count drops to 304 decisions; accuracy decreases to 0.951 while the positive‑class F1 remains unchanged at 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 173 | 600 | 10000 | 946.83 | stop |
| 2 | answer | medium | 4369 | 4144 | 525 | 3000 | 10000 | 2039.21 | stop |
| 3 | judge | low | 1001 | 776 | 336 | 1000 | 10000 | 985.07 | stop |
| 4 | judge | low | 886 | 661 | 104 | 1000 | 10000 | 784.16 | stop |

### Finalized answer

<pre>Three model papers were manually annotated by experts for validation — the three representative RFMs (Gemini Robotics 1.5, OpenVLA, and π0) [C4].  

In the expert‑LLM agreement analysis (Table 9), the “All” setting evaluated 447 criterion‑level decisions, achieving an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  
When restricting to the “InfoFound” subset (only cases where the LLM flagged the information as found), the evaluation count drops to 304 decisions; accuracy decreases to 0.951 while the positive‑class F1 remains unchanged at 0.762 [C8].  </pre>

## SECOND_NUMBER — repetition 2

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: [&#x27;model papers manually annotated expert validation count&#x27;, &#x27;InfoFound overall accuracy vs All evaluation counts&#x27;, &#x27;InfoFound positive-class F1 vs All evaluation counts&#x27;]

Ask latency_ms: 5695.91

Judge latency_ms: 1790.02

Total evaluation latency_ms: 7503.34

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C5 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | PASS | Required claim supported by verbatim evidence | Three model papers were manually annotated for expert validation — the “expert‑annotated papers” referenced in the evaluation [C2].  <br><br>Table 9 compares two settings for the LLM‑expert agreement:<br><br>\| Setting \| Evaluation count (N) \| Overall accuracy \| Positive‑class F1 \|<br>\|---------\|----------------------\|------------------\|-------------------\|<br>\| All \| 447 \| 0.966 \| 0.762 \|<br>\| InfoFound \| 304 \| 0.951 \| 0.762 \|<br><br>Thus, using the InfoFound filter reduces the overall accuracy from 0.966 to 0.951 (a drop of 0.015) while the positive‑class F1 score remains the same at 0.762. The evaluation counts are 447 for the All setting and 304 for the InfoFound setting [C5]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 261 | 600 | 10000 | 1308.37 | stop |
| 2 | answer | medium | 3190 | 2965 | 533 | 3000 | 10000 | 2139.72 | stop |
| 3 | judge | low | 1029 | 804 | 356 | 1000 | 10000 | 1114.21 | stop |
| 4 | judge | low | 914 | 689 | 86 | 1000 | 10000 | 675.81 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — the “expert‑annotated papers” referenced in the evaluation [C2].  

Table 9 compares two settings for the LLM‑expert agreement:

| Setting | Evaluation count (N) | Overall accuracy | Positive‑class F1 |
|---------|----------------------|------------------|-------------------|
| All | 447 | 0.966 | 0.762 |
| InfoFound | 304 | 0.951 | 0.762 |

Thus, using the InfoFound filter reduces the overall accuracy from 0.966 to 0.951 (a drop of 0.015) while the positive‑class F1 score remains the same at 0.762. The evaluation counts are 447 for the All setting and 304 for the InfoFound setting [C5].</pre>

## SECOND_NUMBER — repetition 3

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: [&#x27;model papers manually annotated expert validation count&#x27;, &#x27;InfoFound vs All overall accuracy and positive-class F1 evaluation counts&#x27;, &#x27;InfoFound impact on accuracy and F1 compared to All&#x27;]

Ask latency_ms: 4548.87

Judge latency_ms: 1827.84

Total evaluation latency_ms: 6392.49

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C5 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | Three model papers were manually annotated for expert validation — the three “expert‑annotated papers” referenced in the study [C2].<br><br>In the comparison of the two evaluation settings reported in Table 9, the “InfoFound” condition uses fewer evaluations (N = 304) than the “All” condition (N = 447) [C5].<br>- Overall accuracy drops from 0.966 (All) to 0.951 (InfoFound), a decrease of 0.015.<br>- The positive‑class F1 score remains the same at 0.762 for both settings. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 263 | 600 | 10000 | 1251.86 | stop |
| 2 | answer | medium | 3190 | 2965 | 588 | 3000 | 10000 | 2090.94 | stop |
| 3 | judge | low | 1017 | 792 | 337 | 1000 | 10000 | 1200.46 | stop |
| 4 | judge | low | 902 | 677 | 86 | 1000 | 10000 | 627.37 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — the three “expert‑annotated papers” referenced in the study [C2].  

In the comparison of the two evaluation settings reported in Table 9, the “InfoFound” condition uses fewer evaluations (N = 304) than the “All” condition (N = 447) [C5].  
- Overall accuracy drops from 0.966 (All) to 0.951 (InfoFound), a decrease of 0.015.  
- The positive‑class F1 score remains the same at 0.762 for both settings.  

Thus, InfoFound slightly lowers overall accuracy while leaving the positive‑class F1 unchanged, with evaluation counts of 447 (All) and 304 (InfoFound).</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 4798.26

Judge latency_ms: 752.07

Total evaluation latency_ms: 5553.74

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 121 | 600 | 10000 | 740.81 | stop |
| 2 | answer | medium | 2993 | 2768 | 1340 | 3000 | 10000 | 4018.79 | stop |
| 3 | judge | low | 1570 | 1345 | 75 | 1000 | 10000 | 752.07 | stop |

### Finalized answer

<pre>The paper is motivated by the need to understand how far current robotic foundation models (RFMs) are from meeting the requirements of real‑world industry, especially for collaborative robots that must operate safely, flexibly and under edge‑computing constraints[S1].  

To assess this, the authors first built three literature corpora (a main set of 1 025 RFMs, an “implications” set of 125 articles and a supplementary set of 113 papers) using a modular Python pipeline that merges database results, removes duplicates and applies GPT‑4o relevance filtering, followed by manual refinement[S1].  They then evaluated the 324 manipulation‑capable RFMs against a catalogue of 149 industrial criteria (derived from 11 high‑level implications) with an automated LLM‑based pipeline (GPT‑5.1) that produces binary fulfilment judgments, confidence scores, evidence flags and rationales[S1].  Proportional applicability ratings for each implication (I1–I11) were computed for the full corpus and for a Top‑50 subset[S2].  Expert validation was performed on three blind‑rated papers, yielding high agreement with the automated labels (accuracy 0.966, κ 0.744) but revealing a low false‑positive rate (1.9 %) and a higher false‑negative rate (22.6%) caused by a conservative marking policy when model capabilities were not reported[S1].  

The main findings are that industrial maturity of RFMs is limited and uneven: even the best models satisfy only about 10 % of the 149 criteria and show narrow, implication‑specific strengths[S1].  Coverage is concentrated on adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements (I11), which together account for roughly three‑quarters of “1+‑Coverage” in the full set and reach full coverage in the Top‑50[S2].  Safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7) remain consistently under‑addressed, with breadth and depth ≤0.10 even for the Top‑50[S2].  The highest proportional fulfilment observed is 0.44 for I1 (Gemini Robotics 1.5), and the best per‑implication scores are modest (e.g., 0.11 for I6)[S2].  Gap analysis shows large discrepancies between evidence presence and actual fulfilment, often exceeding 0.8[S2].  

Limitations are explicitly acknowledged: the automated evaluation provides a reliable lower‑bound estimate for corpus‑level analysis but individual criterion judgments should be interpreted cautiously because of interpretive latitude, occasional disagreement and the impact of unreported model capabilities, which the conservative policy treats as non‑fulfilment and thus inflates false‑negatives[S1].  The expert validation scope is restricted to only three blind‑rated papers, so broader confidence in the automated labels is not established[S1].  

The appendices serve complementary roles: Appendix A supplies a survey of related works that situates the study within existing literature[S2]; Appendix B details the literature‑search procedures and corpus construction that underpin the systematic review[S2]; Appendix C enumerates the industrial implications and the 149 criteria used for the maturity assessment[S2]; and Appendix D provides an overview of the evaluated RFMs together with the detailed tables (e.g., Tables 11, 12, D5) that report the highest‑rated models and per‑implication scores[S2].</pre>

## SECOND_SUMMARY — repetition 2

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 4716.04

Judge latency_ms: 824.94

Total evaluation latency_ms: 5543.61

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 160 | 600 | 10000 | 789.70 | stop |
| 2 | answer | medium | 2993 | 2768 | 1211 | 3000 | 10000 | 3891.60 | stop |
| 3 | judge | low | 1528 | 1303 | 75 | 1000 | 10000 | 824.94 | stop |

### Finalized answer

<pre>The paper is motivated by the need to understand how far current robotic foundation models (RFMs) are from meeting the concrete requirements of industrial automation, especially for collaborative robots (cobots) that must operate safely, flexibly and under edge‑computing constraints[S1].  

To assess this, the authors built three literature corpora (a main corpus of 1 025 RFMs, an “implications” corpus of 125 articles and a supplementary set of 113 works) using a modular Python pipeline that merges database results, removes duplicates and applies LLM‑based relevance filtering (GPT‑4o) followed by manual refinement[S1].  They then evaluated 324 manipulation‑capable RFMs against a catalogue of 149 industrial‑grade criteria (derived from 11 high‑level implications) with an automated LLM‑based pipeline (GPT‑5.1) that produced binary fulfilment judgments, confidence scores, evidence flags and rationales[S1].  The evaluation was cross‑checked on three blind‑rated papers, yielding high expert agreement (accuracy 0.966, κ 0.744) but a relatively high false‑negative rate (22.6 %) because the marking policy was conservative when model capabilities were not reported[S1].  

The main findings are that industrial maturity is limited and uneven: even the best RFMs satisfy only about 10 % of the 149 criteria and show narrow, implication‑specific strengths rather than broad coverage[S2].  Coverage is concentrated on adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements (I11), with breadth values around 0.75–0.76 in the full set and reaching 1.0 in the Top‑50, but depth remains low (≤0.10 in the full set, ≤0.24 in the Top‑50)[S2].  The highest proportional fulfilment observed is 0.44 for I1 (Gemini Robotics 1.5), and the best per‑implication scores are modest (e.g., 0.11 for I6)[S2].  Persistent gaps are safety/compliance (I2), human‑robot interaction/co‑robotics (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7), which remain under‑addressed across both the full corpus and the Top‑50[S2].  

Limitations acknowledged by the authors include that the automated evaluation provides only a reliable lower‑bound estimate of maturity and that individual criterion judgments should be interpreted cautiously because of interpretive latitude and occasional disagreement among annotators[S1].  The high false‑negative rate reflects the impact of unreported model capabilities: when a paper does not explicitly describe a capability, the conservative policy marks it as unfulfilled, thereby understating a model’s true potential[S1].  Expert validation was limited to three blind‑rated papers, so while agreement was strong, the scope of human verification is narrow[S1].  

The appendices serve complementary roles: Appendix A supplies a survey of related works to situate the study within existing literature[S2]; Appendix B details the literature‑search methodology and corpus construction; Appendix C enumerates the industrial implications and the 149 criteria used for evaluation; and Appendix D presents the RFM overview, including tables of the highest‑rated models and their detailed implication scores[S2].</pre>

## SECOND_SUMMARY — repetition 3

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 4978.94

Judge latency_ms: 741.34

Total evaluation latency_ms: 5728.06

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 160 | 600 | 10000 | 938.68 | stop |
| 2 | answer | medium | 2993 | 2768 | 1126 | 3000 | 10000 | 4003.68 | stop |
| 3 | judge | low | 1558 | 1333 | 75 | 1000 | 10000 | 741.34 | stop |

### Finalized answer

<pre>The paper is motivated by the need to understand whether today’s robotic foundation models (RFMs) are ready for industrial use, especially for collaborative‑robot (cobot) scenarios that demand safety, flexibility, multimodal perception and real‑time operation[S1].  

To answer this, the authors built three literature corpora (a main set of 1 025 RFM‑related works, an “implications” set of 125 papers and a supplementary set of 113 items) using a modular Python pipeline with LLM‑based relevance filtering, and then derived a catalogue of 149 industrial‑grade criteria covering 11 high‑level implications (adaptability, safety, HRI, robustness, precision, real‑time performance, cost, explainability, sensor fusion, benchmarking, data efficiency)[S1]. An automated GPT‑5.1 pipeline generated binary fulfil‑ment judgments, confidence scores and rationales for each of the 324 manipulation‑capable RFMs against all criteria; a blind expert check on three papers was used to validate the pipeline, showing 96.6 % accuracy, κ = 0.744, a low false‑positive rate (1.9 %) but a higher false‑negative rate (22.6 %) that stems from a conservative marking policy[S1].  

The assessment reveals that industrial maturity is limited and uneven: even the best models satisfy only about 10 % of the 149 criteria and show narrow, implication‑specific strengths rather than broad coverage[S2]. Coverage is concentrated on adaptability/flexibility (I1), benchmarking/evaluation (I10) and data requirements (I11), which reach full “1+‑Coverage” in the Top‑50 subset, while safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness/integration (I7) remain consistently under‑addressed with breadth and depth ≤0.10[S2]. The highest proportional fulfil‑ment for any implication is 0.44 for I1 (Gemini Robotics 1.5), and the best per‑implication scores are modest (e.g., 0.11 for I6)[S2]. Gap analysis shows large discrepancies between evidence presence and actual fulfil‑ment (gap scores often &gt;0.8)[S2].  

A key limitation is that many RFMs do not explicitly report capabilities relevant to the industrial criteria; because the evaluation relies on documented evidence, unreported features are treated as absent, inflating false‑negative rates and producing conservative maturity estimates[S1][S2]. The expert validation is therefore scoped to a small sample of three blind‑rated papers, providing high‑level confidence in the pipeline but not guaranteeing correctness for every individual criterion judgment[S1].  

The appendices support the main study: Appendix A compiles related works that contextualise the RFM literature; Appendix B details the literature‑search methodology and corpus construction; Appendix C lists the full set of industrial implications and their 149 criteria; Appendix D presents the RFM overview, including the tables of highest‑rated models and detailed per‑implication scores referenced in the results[S2].  

Overall, the authors conclude that advancing industry‑grade RFMs will require systematic integration of safety, real‑time feasibility, robust perception, interaction and cost‑effective, auditable system design, rather than isolated benchmark gains, while cautioning that the reported maturity figures are lower‑bound estimates due to the conservative handling of unreported capabilities[S1].</pre>
