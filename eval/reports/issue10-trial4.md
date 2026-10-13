# Golden Facts evaluation

Created: 2026-10-13T04:45:46.824582+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-bef898c944a3fae0b72604751901b5ed610644ac3d0bb87e2992438781aa364c

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | table2_citation | events | 1/1 (100.0%) |
| SECOND_NUMBER | question_type | events | 1/1 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/1 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 1/1 (100.0%) |
| SECOND_SUMMARY | question_type | events | 1/1 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/1 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 696 | 471 | 112 | 1200 | 10000 | 1588.12 | stop |
| 2 | section_summary | low | 1576 | 1351 | 328 | 1200 | 10000 | 1724.72 | stop |
| 3 | section_summary | low | 2679 | 2454 | 538 | 1200 | 10000 | 3010.75 | stop |
| 4 | section_summary | low | 2650 | 2425 | 564 | 1200 | 10000 | 3294.88 | stop |
| 5 | section_summary | low | 1938 | 1713 | 317 | 1200 | 10000 | 1836.17 | stop |
| 6 | section_summary | low | 993 | 768 | 152 | 1200 | 10000 | 1751.31 | stop |
| 7 | section_summary | low | 1035 | 810 | 333 | 1200 | 10000 | 1571.54 | stop |
| 8 | section_summary | low | 569 | 344 | 71 | 1200 | 10000 | 1369.42 | stop |
| 9 | section_summary | low | 1058 | 833 | 303 | 1200 | 10000 | 1572.23 | stop |
| 10 | section_summary | low | 553 | 328 | 88 | 1200 | 10000 | 903.81 | stop |
| 11 | section_summary | low | 2313 | 2088 | 306 | 1200 | 10000 | 2017.83 | stop |
| 12 | section_summary | low | 1374 | 1149 | 258 | 1200 | 10000 | 1569.20 | stop |
| 13 | section_summary | low | 907 | 682 | 130 | 1200 | 10000 | 1125.46 | stop |
| 14 | section_summary | low | 1244 | 1019 | 251 | 1200 | 10000 | 2070.95 | stop |
| 15 | section_summary | low | 1383 | 1158 | 221 | 1200 | 10000 | 1517.84 | stop |
| 16 | section_summary | low | 793 | 568 | 95 | 1200 | 10000 | 1531.77 | stop |
| 17 | section_summary | low | 1541 | 1316 | 280 | 1200 | 10000 | 1417.32 | stop |
| 18 | section_summary | low | 1166 | 941 | 238 | 1200 | 10000 | 1498.72 | stop |
| 19 | section_summary | low | 745 | 520 | 92 | 1200 | 10000 | 822.95 | stop |
| 20 | section_summary | low | 2770 | 2545 | 482 | 1200 | 10000 | 2527.80 | stop |
| 21 | section_summary | low | 1569 | 1344 | 208 | 1200 | 10000 | 1424.93 | stop |
| 22 | section_summary | low | 763 | 538 | 127 | 1200 | 10000 | 1037.61 | stop |
| 23 | section_summary | low | 2632 | 2407 | 410 | 1200 | 10000 | 2271.20 | stop |
| 24 | section_summary | low | 4958 | 4733 | 780 | 1200 | 10000 | 3744.51 | stop |
| 25 | section_summary | low | 2429 | 2204 | 555 | 1200 | 10000 | 2840.07 | stop |
| 26 | section_summary | low | 3525 | 3300 | 806 | 1200 | 10000 | 3396.24 | stop |
| 27 | section_summary | low | 3651 | 3426 | 721 | 1200 | 10000 | 2964.70 | stop |
| 28 | section_summary | low | 1053 | 828 | 385 | 1200 | 10000 | 1427.42 | stop |
| 29 | section_summary | low | 1277 | 1052 | 228 | 1200 | 10000 | 3042.98 | stop |
| 30 | section_summary | low | 1239 | 1014 | 380 | 1200 | 10000 | 1477.67 | stop |
| 31 | section_summary | low | 2559 | 2334 | 420 | 1200 | 10000 | 1854.69 | stop |
| 32 | section_summary | low | 1729 | 1504 | 271 | 1200 | 10000 | 1478.24 | stop |
| 33 | section_summary | low | 1308 | 1083 | 327 | 1200 | 10000 | 2875.71 | stop |
| 34 | section_summary | low | 2073 | 1848 | 335 | 1200 | 10000 | 1912.85 | stop |
| 35 | section_summary | low | 7035 | 6810 | 488 | 1200 | 10000 | 3145.94 | stop |
| 36 | section_summary | low | 8066 | 7841 | 754 | 1200 | 10000 | 4366.01 | stop |
| 37 | section_summary | low | 1964 | 1739 | 373 | 1200 | 10000 | 2191.63 | stop |
| 38 | section_summary | low | 7047 | 6822 | 750 | 1200 | 10000 | 3777.66 | stop |
| 39 | section_summary | low | 1591 | 1366 | 940 | 1200 | 10000 | 2848.79 | stop |
| 40 | section_summary | low | 1459 | 1234 | 390 | 1200 | 10000 | 1884.23 | stop |
| 41 | section_summary | low | 8554 | 8329 | 1026 | 1200 | 10000 | 5027.41 | stop |
| 42 | section_summary | low | 1356 | 1131 | 453 | 1200 | 10000 | 2078.57 | stop |
| 43 | section_summary | low | 3135 | 2910 | 1200 | 1200 | 10000 | 2885.66 | length |
| 44 | section_summary | low | 3186 | 2961 | 481 | 1200 | 10000 | 1648.36 | stop |
| 45 | group_summary | low | 6211 | 5986 | 2500 | 2500 | 10000 | 5850.03 | length |
| 46 | group_summary | low | 6262 | 6037 | 848 | 2500 | 10000 | 2881.78 | stop |
| 47 | group_summary | low | 2661 | 2436 | 1389 | 2500 | 10000 | 3851.79 | stop |
| 48 | document_summary | low | 2740 | 2515 | 987 | 2500 | 10000 | 2171.87 | stop |

## SECOND_NUMBER — repetition 1

Question: In the expert-validation comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: In the expert-validation comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 2788.41

Judge latency_ms: 1845.97

Total evaluation latency_ms: 4641.56

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C6 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Required claim not asserted |  |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 845 | 506 | 139 | 600 | 10000 | 783.13 | stop |
| 2 | answer | medium | 4806 | 4581 | 637 | 3000 | 10000 | 1743.45 | stop |
| 3 | judge | low | 832 | 607 | 245 | 1000 | 10000 | 997.07 | stop |
| 4 | judge | low | 781 | 556 | 135 | 1000 | 10000 | 848.90 | stop |

### Finalized answer

<pre>- For the **All** setting the evaluation used **447** criterion‑level judgments, achieving an overall accuracy of **0.966** and a positive‑class F1 score of **0.762**[C6].  
- For the **InfoFound** setting the evaluation used **304** judgments, the overall accuracy dropped to **0.951**, while the positive‑class F1 score remained **0.762**[C6].  

Thus, restricting to cases where the LLM flagged information as found lowers accuracy slightly (0.966 → 0.951) but does not change the positive‑class F1.</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations, including what the appendices contribute.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations, including what the appendices contribute.

Sub-queries: []

Ask latency_ms: 4488.38

Judge latency_ms: 742.98

Total evaluation latency_ms: 5234.26

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 839 | 500 | 108 | 600 | 10000 | 616.01 | stop |
| 2 | answer | medium | 3012 | 2787 | 1569 | 3000 | 10000 | 3822.67 | stop |
| 3 | judge | low | 2062 | 1837 | 75 | 1000 | 10000 | 742.98 | stop |

### Finalized answer

<pre>**Motivation**  
The paper is motivated by the industrial shift from rigid, high‑speed manipulators to collaborative cobots that must be commissioned quickly, redeployed across variable processes, and operate safely alongside humans. This creates a bottleneck in adaptive low‑level control, and the authors note that systematic, industrial‑focused evaluation of robotic foundation models (RFMs) is currently missing, risking fragmentation of the emerging field[S1].  

**Assessment method**  
1. **Corpus construction** – Three literature corpora were built with a modular Python pipeline that queries arXiv, Google Scholar, OpenAlex, Scopus and Semantic Scholar, removes duplicates, enriches metadata, and filters relevance using GPT‑4o scoring. The main RFM corpus contains 1 025 works, of which 324 are manipulation‑oriented RFMs; an industrial‑implication corpus of 125 top‑scored papers supplies eleven domain‑agnostic requirements[S1].  
2. **Requirement‑to‑criterion mapping** – The eleven implications (I1–I11) are expanded into 47 attributes, forming a 11 × 47 matrix (517 cells) that underpins a catalogue of 149 concrete criteria covering model capabilities, ecosystem documentation, and hybrid responsibilities such as hot‑swapping, out‑of‑distribution robustness, calibrated uncertainty, human‑in‑the‑loop clarification, supervisory failure detection, and memory governance[S1].  
3. **Automated evaluation pipeline** – GPT‑5.1 is queried for each of the 324 RFMs against every criterion, returning binary fulfilment judgments, confidence scores, evidence flags and rationales. Validation on three expert‑annotated papers shows 96.6 % accuracy, κ≈0.74, a 1.9 % false‑positive rate and a 22.6 % false‑negative rate, reflecting a conservative policy that marks a criterion unfulfilled unless clearly supported[S1].  
4. **Quantitative analysis** – The authors evaluate 324 RFMs (48 276 individual criterion decisions) and a high‑performing Top‑50 subset, measuring *breadth* (coverage score) and *depth* (average criterion fulfilment, ACC) for each implication[S2].  

**Main findings**  
* **Overall coverage is low** – Across the full corpus only adaptability (I1), benchmarking/evaluation (I10) and data usage (I11) reach a coverage score above 0.7; all depth values are below 0.10[S2].  
* **Ceiling effect in maturity scores** – The five highest‑rated models achieve only 0.11–0.12 of the total criteria (≈10 %); Gemini Robotics 1.5 attains the best overall score (0.12) and a peak implication score of 0.44[S1].  
* **Top‑50 improvements are modest** – The Top‑50 models obtain full coverage (1.0) for several implications (I1, I4, I5, I8, I9, I10, I11) and a modest depth gain for adaptability (I1 = 0.238), yet safety/compliance (I2) and real‑time performance (I6) remain under‑addressed (depth &lt; 0.04)[S2].  
* **Dominant research themes** – Multi‑Task Generalisation (0.494) and Flexible Data Type Acceptance (0.488) are the most frequently cited criteria, but explicit reporting is limited (e.g., Multi‑Task Generalisation appears in only 28 % of papers)[S2].  
* **Safety, real‑time, cost‑effectiveness, and HRI are largely absent** – Fewer than 5 % of models satisfy any sub‑criterion in these areas, and gap analysis shows mismatches &gt; 0.8 for most implications[S2].  
* **Hardware constraints** – Cobots typically have six DOF, median payload ≈5.5 kg, reach ≈0.9 m, positioning accuracy 0.05–0.09 mm, and power ≈0.3 kW, making edge AI platforms essential; among NVIDIA Jetson devices, the Orin Nano offers the lowest price‑per‑TOPS, the Xavier NX the smallest power envelope, and the Orin AGX 32 GB balances throughput and efficiency[S1].  

**Limitations**  
* The tables in the source material are marked “結構未能可靠重建”, so row/column associations cannot be reliably inferred[S1][S2].  
* The automated pipeline uses a conservative binary judgement policy, leading to a 22.6 % false‑negative rate that may under‑report fulfilled criteria[S1].  
* Evaluation is limited to the 149 pre‑defined criteria; many practical aspects of deployable cobot intelligence (e.g., long‑horizon operation, dynamic energy management) remain untested.  

**Appendix contributions**  
* **Appendix C** – Provides the full industrial implication catalogue, detailing the 11 implications, their 47 attributes, and the 149 concrete criteria (e.g., adaptability requirements, safety compliance checks, multimodal interaction specifications, robustness fault‑detection, cost‑efficiency targets, explainability traces, benchmarking protocols, and data‑governance rules)[S2].  
* **Appendix D** – Summarises the applicability scores derived by the LLM‑based pipeline, showing that total scores cluster between 0.01 and 0.12, with the highest‑scoring model (Gemini [157]) achieving only 1.5 % of the theoretical maximum; it also reports the distribution of non‑zero dimensions across implications, highlighting the sparsity of safety/robustness and integration scores[S2].  

Overall, the document argues that while RFMs are rapidly emerging, current research addresses only narrow subsets of industrial needs, and a more balanced, hardware‑aware, and safety‑centric evaluation framework is required to bridge the gap between laboratory advances and deployable cobot intelligence[S1][S2].</pre>
