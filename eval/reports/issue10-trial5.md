# Golden Facts evaluation

Created: 2026-10-13T04:50:52.967270+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-74dad9dc8f8dd147418e6f8ead6070306fb616c2171c117719882208e2e53e0a

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | table2_citation | events | 1/1 (100.0%) |
| SECOND_NUMBER | question_type | events | 0/1 (0.0%) |
| SECOND_NUMBER | expert_agreement | judge | 1/1 (100.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 1/1 (100.0%) |
| SECOND_SUMMARY | question_type | events | 1/1 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/1 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 767 | 542 | 110 | 1200 | 10000 | 1654.00 | stop |
| 2 | section_summary | low | 1647 | 1422 | 332 | 1200 | 10000 | 2473.00 | stop |
| 3 | section_summary | low | 2750 | 2525 | 423 | 1200 | 10000 | 2741.60 | stop |
| 4 | section_summary | low | 2721 | 2496 | 602 | 1200 | 10000 | 3203.29 | stop |
| 5 | section_summary | low | 2009 | 1784 | 394 | 1200 | 10000 | 1771.15 | stop |
| 6 | section_summary | low | 1064 | 839 | 148 | 1200 | 10000 | 1004.70 | stop |
| 7 | section_summary | low | 640 | 415 | 83 | 1200 | 10000 | 777.42 | stop |
| 8 | section_summary | low | 624 | 399 | 113 | 1200 | 10000 | 1218.74 | stop |
| 9 | section_summary | low | 1445 | 1220 | 236 | 1200 | 10000 | 1260.54 | stop |
| 10 | section_summary | low | 1168 | 943 | 359 | 1200 | 10000 | 1894.78 | stop |
| 11 | section_summary | low | 2384 | 2159 | 298 | 1200 | 10000 | 2085.40 | stop |
| 12 | section_summary | low | 978 | 753 | 130 | 1200 | 10000 | 1263.22 | stop |
| 13 | section_summary | low | 1315 | 1090 | 212 | 1200 | 10000 | 1794.63 | stop |
| 14 | section_summary | low | 1454 | 1229 | 220 | 1200 | 10000 | 1924.98 | stop |
| 15 | section_summary | low | 864 | 639 | 98 | 1200 | 10000 | 1502.09 | stop |
| 16 | section_summary | low | 816 | 591 | 98 | 1200 | 10000 | 825.29 | stop |
| 17 | section_summary | low | 1237 | 1012 | 264 | 1200 | 10000 | 1418.56 | stop |
| 18 | section_summary | low | 1612 | 1387 | 288 | 1200 | 10000 | 2070.99 | stop |
| 19 | section_summary | low | 1640 | 1415 | 193 | 1200 | 10000 | 1867.71 | stop |
| 20 | section_summary | low | 2841 | 2616 | 501 | 1200 | 10000 | 3354.18 | stop |
| 21 | section_summary | low | 834 | 609 | 105 | 1200 | 10000 | 1093.82 | stop |
| 22 | section_summary | low | 2703 | 2478 | 466 | 1200 | 10000 | 2591.84 | stop |
| 23 | section_summary | low | 2500 | 2275 | 400 | 1200 | 10000 | 2270.83 | stop |
| 24 | section_summary | low | 5029 | 4804 | 927 | 1200 | 10000 | 4617.82 | stop |
| 25 | section_summary | low | 3596 | 3371 | 715 | 1200 | 10000 | 3362.87 | stop |
| 26 | section_summary | low | 1500 | 1275 | 330 | 1200 | 10000 | 1950.24 | stop |
| 27 | section_summary | low | 3722 | 3497 | 828 | 1200 | 10000 | 3543.05 | stop |
| 28 | section_summary | low | 2630 | 2405 | 576 | 1200 | 10000 | 2786.45 | stop |
| 29 | section_summary | low | 1300 | 1075 | 516 | 1200 | 10000 | 2171.96 | stop |
| 30 | section_summary | low | 1800 | 1575 | 335 | 1200 | 10000 | 2042.54 | stop |
| 31 | section_summary | low | 1414 | 1189 | 524 | 1200 | 10000 | 2177.59 | stop |
| 32 | section_summary | low | 1141 | 916 | 279 | 1200 | 10000 | 1634.58 | stop |
| 33 | section_summary | low | 1105 | 880 | 422 | 1200 | 10000 | 1926.01 | stop |
| 34 | section_summary | low | 1101 | 876 | 370 | 1200 | 10000 | 1876.97 | stop |
| 35 | section_summary | low | 2144 | 1919 | 361 | 1200 | 10000 | 2787.62 | stop |
| 36 | section_summary | low | 7106 | 6881 | 633 | 1200 | 10000 | 3700.68 | stop |
| 37 | section_summary | low | 8137 | 7912 | 1200 | 1200 | 10000 | 6834.47 | length |
| 38 | section_summary | low | 7118 | 6893 | 596 | 1200 | 10000 | 3055.92 | stop |
| 39 | section_summary | low | 8188 | 7963 | 540 | 1200 | 10000 | 3276.46 | stop |
| 40 | section_summary | low | 2035 | 1810 | 545 | 1200 | 10000 | 2854.35 | stop |
| 41 | section_summary | low | 8625 | 8400 | 1200 | 1200 | 10000 | 5647.81 | length |
| 42 | section_summary | low | 1607 | 1382 | 881 | 1200 | 10000 | 3145.78 | stop |
| 43 | section_summary | low | 8676 | 8451 | 473 | 1200 | 10000 | 2683.27 | stop |
| 44 | section_summary | low | 1465 | 1240 | 514 | 1200 | 10000 | 2397.54 | stop |
| 45 | section_summary | low | 1427 | 1202 | 469 | 1200 | 10000 | 2208.98 | stop |
| 46 | section_summary | low | 1105 | 880 | 365 | 1200 | 10000 | 1444.35 | stop |
| 47 | section_summary | low | 2590 | 2365 | 932 | 1200 | 10000 | 3410.32 | stop |
| 48 | section_summary | low | 1502 | 1277 | 356 | 1200 | 10000 | 1385.23 | stop |
| 49 | group_summary | low | 6269 | 6044 | 2009 | 2500 | 10000 | 8319.91 | stop |
| 50 | group_summary | low | 2943 | 2718 | 1873 | 2500 | 10000 | 8247.92 | stop |
| 51 | document_summary | low | 4444 | 4219 | 1056 | 2500 | 10000 | 4194.04 | stop |

## SECOND_NUMBER — repetition 1

Question: Identify the manually annotated expert-validation subset. In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Identify the manually annotated expert-validation subset. In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: [&#x27;expert-validation subset definition&#x27;, &#x27;InfoFound vs All overall accuracy and positive-class F1&#x27;, &#x27;evaluation counts InfoFound All&#x27;]

Ask latency_ms: 4026.62

Judge latency_ms: 1900.86

Total evaluation latency_ms: 5930.50

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C5 |
| question_type | events | FAIL | Expected Lookup; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | PASS | Required claim supported by verbatim evidence | Comparing the two settings:<br><br>\| Setting \| N (evaluations) \| Overall Accuracy \| Positive‑class F1 \|<br>\|---------\|----------------\|------------------\|-------------------\|<br>\| All     \| 447            \| 0.966            \| 0.762 \|<br>\| InfoFound\| 304           \| 0.951            \| 0.762 \|<br><br>Thus, restricting to InfoFound **reduces overall accuracy** from 0.966 to 0.951 (a drop of 0.015) while **leaving the positive‑class F1 unchanged** at 0.762 |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 851 | 512 | 190 | 600 | 10000 | 967.59 | stop |
| 2 | answer | medium | 3238 | 3013 | 848 | 3000 | 10000 | 2410.60 | stop |
| 3 | judge | low | 929 | 704 | 285 | 1000 | 10000 | 1109.65 | stop |
| 4 | judge | low | 878 | 653 | 116 | 1000 | 10000 | 791.21 | stop |

### Finalized answer

<pre>The expert‑validation subset that was manually annotated consists of the 447 criterion‑level evaluations used for the “All” condition in Table 9 — these are the cases where both the expert and the LLM made a judgment[C5].  

When the analysis is limited to the subset in which the LLM marked the information as found (the “InfoFound” condition), the number of evaluated instances drops to 304[C5].  

Comparing the two settings:

| Setting | N (evaluations) | Overall Accuracy | Positive‑class F1 |
|---------|----------------|------------------|-------------------|
| All     | 447            | 0.966            | 0.762 |
| InfoFound| 304           | 0.951            | 0.762 |

Thus, restricting to InfoFound **reduces overall accuracy** from 0.966 to 0.951 (a drop of 0.015) while **leaving the positive‑class F1 unchanged** at 0.762[C5][C1].</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations (including validation scope and missing reported evidence), and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations (including validation scope and missing reported evidence), and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 6096.60

Judge latency_ms: 725.45

Total evaluation latency_ms: 6824.85

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 848 | 509 | 120 | 600 | 10000 | 636.86 | stop |
| 2 | answer | medium | 4663 | 4438 | 1781 | 3000 | 10000 | 5446.67 | stop |
| 3 | judge | low | 2026 | 1801 | 73 | 1000 | 10000 | 725.45 | stop |

### Finalized answer

<pre>**Motivation**  
The paper is motivated by the transition from tightly‑tuned, single‑purpose industrial automation to flexible, collaborative cobots that must operate in high‑mix, low‑volume and SME settings.  Existing control pipelines and specialised learning systems are said to lack the multi‑task competence, cross‑domain generalisation, and low‑effort re‑configuration required for such environments, so the authors propose robotic foundation models (RFMs) as a unifying solution [S1][S2].

**Assessment method**  
1. **Literature collection** – Eleven Boolean queries (plus seven industrial‑focus queries) were run on multiple scholarly databases, yielding a primary corpus of 324 RFM‑related papers (2020‑2025) and a “Top‑50” subset selected by citation/venue metrics [S2].  
2. **Scoring pipeline** – An LLM‑based text‑cue pipeline (GPT‑5.1) automatically extracts evidence for each of the 149 criteria (derived from 11 industrial implications) and assigns a binary fulfil‑ment label with confidence.  Scores for the eleven implication dimensions (I1–I11) are rounded to two decimals; the total proportional applicability of a model is the sum of its implication scores (range 0.02–0.12) [S2].  
3. **Scale of evaluation** – The automated process produced 48 276 binary decisions (324 × 149) [S1].  
4. **Validation** – The pipeline was compared with expert judgements on three papers, achieving overall accuracy ≈ 96.6 % (Cohen’s κ ≈ 0.74) but a false‑negative rate of about 22 % due to a conservative “unfulfilled unless clearly supported” policy [S1][S2].

**Main findings**  
* **Limited industrial maturity** – Even the five highest‑rated models satisfy only roughly one‑tenth of the catalogue criteria (total proportional applicability ≈ 0.11–0.12) [S2].  
* **Narrow strength profiles** – Top models excel on only a few implications:  
  * Gemini Robotics 1.5 scores highest on adaptability/flexibility (I1 = 0.44) [S2];  
  * Collab‑VLA leads on human‑robot interaction (I11 = 0.09) and perception (I9 = 0.21) [S2];  
  * GF‑VLA is strongest on data‑requirements (I11 = 0.27) [S2];  
  * OneTwo‑VLA shows flexibility (I1 = 0.33) [S2];  
  * SC‑VLA peaks on robustness (I4 = 0.21) and precision (I5 = 0.23) [S2].  
  No model attains high scores on more than three implications, and safety, real‑time performance, cost‑effectiveness, and comprehensive HRI remain largely untouched [S2].  
* **Breadth and depth** – Across the full 324‑paper set, the most addressed implications (adaptability, benchmarking, data usage) reach only modest breadth (≈0.75) and low average criteria coverage (ACC &lt; 0.10).  All other implications stay well below these values; safety (I2) and real‑time performance (I6) are especially under‑represented [S2].  
* **Evidence‑fulfilment gap** – Gap analyses (Evidence – Fulfil) often exceed 0.8, indicating that discussion of many criteria far outpaces actual demonstrated capability, particularly for integration, safety, real‑time operation, and HRI/HRC [S2].  

**Limitations**  
* **Table reconstruction** – The authors note that the tabular presentation of implication scores could not be reliably rebuilt, so numeric patterns are treated as indicative rather than definitive [S2].  
* **Automated extraction bias** – The LLM‑based scoring adopts a conservative stance, leading to a notable false‑negative rate (~22 %) and occasional missed nuanced evidence when documentation is sparse [S1][S2].  
* **Validation scope** – Expert validation was performed on only three papers, limiting confidence in the pipeline’s generalisation beyond the sampled set [S1][S2].  
* **Missing reported evidence** – Systematic under‑representation is observed for safety/compliance, real‑time performance, cost‑effectiveness, and full‑stack human‑robot collaboration; many papers discuss these criteria without providing concrete fulfilment evidence [S2].

**Purpose of each appendix**  
* **Appendix A** – Positions the current work within the broader literature, listing 55 recent surveys on embodied AI, vision‑language‑action systems, and foundation‑model integration, and highlighting the consensus that the field still faces validation, multimodal fusion, scalability, and safety challenges [S2].  
* **Appendix B** – Details the systematic literature‑search methodology: the eleven Boolean queries for RFM‑related work, the seven industrial‑focus queries, corpus construction (324 papers + Top‑50), and data‑cleaning steps [S2].  
* **Appendix C** – Expands the industrial‑applicability rubric, specifying required safety compliance, explainability, multimodal HRI, fault‑detection, and a comprehensive set of evaluation criteria (benchmark diversity, data efficiency, privacy/ethics, confidence scoring, etc.) to guide future hardware‑aware, robust, and reproducible assessments [S2].  

Overall, the document argues that while RFMs hold promise for flexible cobot automation, current models meet only a small fraction of the industrial‑grade requirements, and substantial work remains to close the safety, real‑time, and integration gaps identified. [S1][S2]</pre>
