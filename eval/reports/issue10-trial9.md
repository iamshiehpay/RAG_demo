# Golden Facts evaluation

Created: 2026-10-13T05:48:47.599046+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 1286357f2bed9d4d39d4ffda91a05b3f9bbb5c2d

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-2de7bb9d9f24566876ee1060cc56f178164bb3f0d46454c232ef4b62664afeee

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | required_source_citation | events | 1/1 (100.0%) |
| SECOND_NUMBER | question_type | events | 1/1 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/1 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 1/1 (100.0%) |
| SECOND_SUMMARY | question_type | events | 1/1 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/1 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 815 | 590 | 122 | 1200 | 10000 | 1425.72 | stop |
| 2 | section_summary | low | 1695 | 1470 | 331 | 1200 | 10000 | 2398.75 | stop |
| 3 | section_summary | low | 2798 | 2573 | 392 | 1200 | 10000 | 2695.21 | stop |
| 4 | section_summary | low | 688 | 463 | 94 | 1200 | 10000 | 894.98 | stop |
| 5 | section_summary | low | 2769 | 2544 | 579 | 1200 | 10000 | 5550.80 | stop |
| 6 | section_summary | low | 1112 | 887 | 135 | 1200 | 10000 | 5093.98 | stop |
| 7 | section_summary | low | 2057 | 1832 | 325 | 1200 | 10000 | 6200.52 | stop |
| 8 | section_summary | low | 672 | 447 | 83 | 1200 | 10000 | 1159.35 | stop |
| 9 | section_summary | low | 1207 | 982 | 233 | 1200 | 10000 | 3189.73 | stop |
| 10 | section_summary | low | 2432 | 2207 | 398 | 1200 | 10000 | 8307.95 | stop |
| 11 | section_summary | low | 1502 | 1277 | 205 | 1200 | 10000 | 4744.98 | stop |
| 12 | section_summary | low | 1493 | 1268 | 271 | 1200 | 10000 | 5948.53 | stop |
| 13 | section_summary | low | 1363 | 1138 | 236 | 1200 | 10000 | 5066.93 | stop |
| 14 | section_summary | low | 1026 | 801 | 132 | 1200 | 10000 | 2308.24 | stop |
| 15 | section_summary | low | 912 | 687 | 84 | 1200 | 10000 | 1082.68 | stop |
| 16 | section_summary | low | 1660 | 1435 | 298 | 1200 | 10000 | 1737.63 | stop |
| 17 | section_summary | low | 1285 | 1060 | 214 | 1200 | 10000 | 2008.76 | stop |
| 18 | section_summary | low | 864 | 639 | 127 | 1200 | 10000 | 1747.11 | stop |
| 19 | section_summary | low | 1688 | 1463 | 216 | 1200 | 10000 | 1787.16 | stop |
| 20 | section_summary | low | 882 | 657 | 121 | 1200 | 10000 | 3436.38 | stop |
| 21 | section_summary | low | 2889 | 2664 | 565 | 1200 | 10000 | 6912.56 | stop |
| 22 | section_summary | low | 2751 | 2526 | 546 | 1200 | 10000 | 6335.93 | stop |
| 23 | section_summary | low | 1189 | 964 | 272 | 1200 | 10000 | 1873.52 | stop |
| 24 | section_summary | low | 5077 | 4852 | 838 | 1200 | 10000 | 7955.07 | stop |
| 25 | section_summary | low | 2548 | 2323 | 397 | 1200 | 10000 | 2608.75 | stop |
| 26 | section_summary | low | 1167 | 942 | 241 | 1200 | 10000 | 1538.00 | stop |
| 27 | section_summary | low | 1449 | 1224 | 274 | 1200 | 10000 | 1791.78 | stop |
| 28 | section_summary | low | 2678 | 2453 | 517 | 1200 | 10000 | 2578.06 | stop |
| 29 | section_summary | low | 3644 | 3419 | 709 | 1200 | 10000 | 3830.36 | stop |
| 30 | section_summary | low | 1848 | 1623 | 309 | 1200 | 10000 | 1896.58 | stop |
| 31 | section_summary | low | 1364 | 1139 | 247 | 1200 | 10000 | 1902.79 | stop |
| 32 | section_summary | low | 3770 | 3545 | 912 | 1200 | 10000 | 5259.41 | stop |
| 33 | section_summary | low | 2195 | 1970 | 299 | 1200 | 10000 | 2769.35 | stop |
| 34 | section_summary | low | 1563 | 1338 | 272 | 1200 | 10000 | 2281.22 | stop |
| 35 | section_summary | low | 6836 | 6611 | 656 | 1200 | 10000 | 5489.33 | stop |
| 36 | section_summary | low | 8185 | 7960 | 1131 | 1200 | 10000 | 8349.61 | stop |
| 37 | section_summary | low | 2083 | 1858 | 521 | 1200 | 10000 | 2965.06 | stop |
| 38 | section_summary | low | 7037 | 6812 | 787 | 1200 | 10000 | 4291.48 | stop |
| 39 | section_summary | low | 8568 | 8343 | 549 | 1200 | 10000 | 3878.45 | stop |
| 40 | section_summary | low | 2242 | 2017 | 1200 | 1200 | 10000 | 5888.53 | length |
| 41 | section_summary | low | 2304 | 2079 | 439 | 1200 | 10000 | 3136.03 | stop |
| 42 | section_summary | low | 6761 | 6536 | 1200 | 1200 | 10000 | 5076.92 | length |
| 43 | section_summary | low | 6823 | 6598 | 359 | 1200 | 10000 | 2812.57 | stop |
| 44 | section_summary | low | 2699 | 2474 | 777 | 1200 | 10000 | 3692.39 | stop |
| 45 | section_summary | low | 1433 | 1208 | 316 | 1200 | 10000 | 6066.72 | stop |
| 46 | group_summary | low | 6378 | 6153 | 2500 | 2500 | 10000 | 19924.93 | length |
| 47 | group_summary | low | 6440 | 6215 | 379 | 2500 | 10000 | 2380.22 | stop |
| 48 | group_summary | low | 2460 | 2235 | 1301 | 2500 | 10000 | 5802.29 | stop |
| 49 | document_summary | low | 2577 | 2352 | 795 | 2500 | 10000 | 3540.78 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation, and in that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All, including the evaluation counts for both settings?

Sub-queries: []

Ask latency_ms: 3333.51

Judge latency_ms: 1637.97

Total evaluation latency_ms: 4985.35

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C6 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the agreement analysis (Table 9), the “All” setting evaluated 447 criterion‑fulfillment judgments, achieving an overall accuracy of 0.966 and a positive‑class F1 score of 0.762. When restricting to cases where the LLM flagged the information as found (“InfoFound”), the evaluation count drops to 304, the accuracy decreases to 0.951, while the positive‑class F1 score remains unchanged at 0.762 [C6]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 132 | 600 | 10000 | 981.12 | stop |
| 2 | answer | medium | 6093 | 5868 | 430 | 3000 | 10000 | 1970.59 | stop |
| 3 | judge | low | 901 | 676 | 162 | 1000 | 10000 | 881.34 | stop |
| 4 | judge | low | 786 | 561 | 94 | 1000 | 10000 | 756.63 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — two before the automated run and one after — as described in the expert‑rated catalogue evaluations [C1].

In the agreement analysis (Table 9), the “All” setting evaluated 447 criterion‑fulfillment judgments, achieving an overall accuracy of 0.966 and a positive‑class F1 score of 0.762. When restricting to cases where the LLM flagged the information as found (“InfoFound”), the evaluation count drops to 304, the accuracy decreases to 0.951, while the positive‑class F1 score remains unchanged at 0.762 [C6].</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 8507.50

Judge latency_ms: 919.85

Total evaluation latency_ms: 9430.71

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 94 | 600 | 10000 | 745.44 | stop |
| 2 | answer | medium | 2806 | 2581 | 1914 | 3000 | 10000 | 7729.79 | stop |
| 3 | judge | low | 1927 | 1702 | 74 | 1000 | 10000 | 919.85 | stop |

### Finalized answer

<pre>**Motivation**  
The paper argues that collaborative cobots need a “generalist core” that can be adapted to many tasks, environments and robot embodiments with only minimal engineering.  Current cobot hardware already meets safety and payload constraints, but the main obstacle is the absence of robust, deployment‑ready models that can handle new tasks, sensor configurations and multimodal commands without extensive hand‑crafting [S1][S2].

**Assessment method**  
1. **Corpus construction** – Three reproducible literature corpora were built (a primary set of 1 025 highly relevant RFM papers, an industrial‑implication set of 125 manually vetted papers, and 113 auxiliary sources) using an automated Python pipeline that combines ASQS queries, duplicate removal, LLM‑based relevance filtering and manual enrichment [S1].  
2. **Industrial‑implication rubric** – Eleven inter‑dependent industrial requirements (adaptability, safety certification, human‑centric interaction, robustness, precision, real‑time edge inference, cost‑effectiveness, explainability, multimodal perception, standardized benchmarking, data‑efficient learning) were mapped to 47 concrete deployment attributes, yielding a 149‑item criteria catalogue [S1][S2].  
3. **Automated scoring** – The catalogue was applied by a GPT‑5.1 pipeline to 324 manipulation‑capable RFMs, producing 48 276 binary decisions.  Scores were normalised to two‑decimal values (overall range 0.01–0.12, peak I1 0.44) and reported as proportional “industrial‑applicability” scores [S1][S2].  
4. **Interpretation** – Scores are purely algorithmic estimates; no empirical performance data, confidence intervals or external expert validation were incorporated [S2].

**Main findings**  
* **Overall maturity is low** – Even the top‑rated model (Gemini Robotics 1.5) satisfies only about one‑tenth of the criteria (overall 0.12, I1 0.44) [S1][S2].  
* **Breadth vs. depth** – The corpus shows high breadth (many models address adaptability, benchmarking and data usage) but shallow depth on safety, human‑robot interaction, real‑time latency and cost‑effectiveness, which remain consistently low [S1][S2].  
* **Distribution of strengths** – Research concentrates on adaptability/flexibility (I1), benchmarking (I10) and data usage (I11); safety/compliance (I2), HRI (I3), real‑time robustness (I6) and cost‑effectiveness (I7) are markedly under‑represented [S2].  
* **No model is comprehensive** – No RFM attains non‑zero values on all eleven criteria; most obtain any score only on I1, ≤5 % address safety or cost, ≤20 % show explainability, and 45–49 % satisfy repeatability or flexible data‑type acceptance [S2].  
* **Implications** – The authors call for layered architectures separating planning, verification and safety, and for evaluation protocols that capture edge‑level latency, dynamic sensor/tool changes, distribution‑shift robustness and long‑horizon operation [S2].

**Limitations**  
* The extraction process could not reliably reconstruct tables or row/column associations, so detailed quantitative comparisons are unavailable [S1][S2].  
* Scores are generated automatically without external validation; they represent indirect estimates rather than measured capabilities [S2].  
* Because many model capabilities (e.g., safety mechanisms, real‑time performance) are not reported in the literature, the pipeline records them as zero or near‑zero, which depresses the overall assessment and highlights the need for expert‑level verification [S2].

**Effect of unreported model capabilities &amp; scope of expert validation**  
The assessment relies exclusively on documented attributes.  When a model’s safety, latency or cost‑effectiveness features are absent from the source papers, the automated rubric assigns a zero/near‑zero value, causing the model to appear less mature than it might actually be.  Consequently, the reported maturity scores are limited to what is publicly described, and the authors acknowledge that the ratings are “context‑dependent, automatically generated, and lack external validation,” indicating that expert review is currently narrow and cannot fully compensate for missing information [S2].

**Purpose of each appendix**  
* **Appendix A** – Provides a curated bibliography of 55 recent surveys (2023‑2025) on vision‑language‑action models, large language models, multimodal foundations and their robot applications; it serves as a reference map without quantitative data [S2].  
* **Appendix B** – Lists the raw systematic query strings (ASQS) used to assemble the three literature corpora; the accompanying tables could not be reliably reconstructed, so only the query texts are reported [S2].  
* **Appendix C** – Defines the industrial‑implication rubric in detail, describing the eight primary categories (adaptability, safety, multimodal interaction, fault robustness, specification compliance, real‑time robustness, cost‑efficiency, explainability) and the associated benchmark themes [S2].  
* **Appendix D** – Presents the RFM‑overview, showing the automatically generated proportional industrial‑applicability scores for each of the 324 manipulation‑enabled RFMs across the eleven implication dimensions, confirming the fragmented applicability of current models [S2].</pre>
