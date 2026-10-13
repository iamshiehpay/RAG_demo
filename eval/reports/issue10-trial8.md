# Golden Facts evaluation

Created: 2026-10-13T05:34:11.392282+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 1286357f2bed9d4d39d4ffda91a05b3f9bbb5c2d

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-8f8d1852337d45c29d4d31aef5525a6bdf6612cb0b0a9394b2168b80b125c81d

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | required_source_citation | events | 1/1 (100.0%) |
| SECOND_NUMBER | question_type | events | 0/1 (0.0%) |
| SECOND_NUMBER | expert_agreement | judge | 0/1 (0.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 1/1 (100.0%) |
| SECOND_SUMMARY | question_type | events | 1/1 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/1 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 815 | 590 | 112 | 1200 | 10000 | 1542.80 | stop |
| 2 | section_summary | low | 1695 | 1470 | 299 | 1200 | 10000 | 2233.82 | stop |
| 3 | section_summary | low | 2798 | 2573 | 420 | 1200 | 10000 | 2435.30 | stop |
| 4 | section_summary | low | 2769 | 2544 | 427 | 1200 | 10000 | 3649.68 | stop |
| 5 | section_summary | low | 688 | 463 | 91 | 1200 | 10000 | 1514.59 | stop |
| 6 | section_summary | low | 1112 | 887 | 137 | 1200 | 10000 | 1907.62 | stop |
| 7 | section_summary | low | 672 | 447 | 96 | 1200 | 10000 | 979.72 | stop |
| 8 | section_summary | low | 2057 | 1832 | 357 | 1200 | 10000 | 3568.15 | stop |
| 9 | section_summary | low | 2432 | 2207 | 323 | 1200 | 10000 | 2128.75 | stop |
| 10 | section_summary | low | 1493 | 1268 | 243 | 1200 | 10000 | 1636.04 | stop |
| 11 | section_summary | low | 1363 | 1138 | 182 | 1200 | 10000 | 1301.58 | stop |
| 12 | section_summary | low | 912 | 687 | 107 | 1200 | 10000 | 917.31 | stop |
| 13 | section_summary | low | 1026 | 801 | 129 | 1200 | 10000 | 1041.67 | stop |
| 14 | section_summary | low | 1502 | 1277 | 210 | 1200 | 10000 | 2033.92 | stop |
| 15 | section_summary | low | 1660 | 1435 | 315 | 1200 | 10000 | 1616.05 | stop |
| 16 | section_summary | low | 1285 | 1060 | 175 | 1200 | 10000 | 1198.36 | stop |
| 17 | section_summary | low | 864 | 639 | 80 | 1200 | 10000 | 805.71 | stop |
| 18 | section_summary | low | 1688 | 1463 | 186 | 1200 | 10000 | 1389.14 | stop |
| 19 | section_summary | low | 2889 | 2664 | 507 | 1200 | 10000 | 2824.22 | stop |
| 20 | section_summary | low | 882 | 657 | 125 | 1200 | 10000 | 887.05 | stop |
| 21 | section_summary | low | 2751 | 2526 | 486 | 1200 | 10000 | 2694.35 | stop |
| 22 | section_summary | low | 2548 | 2323 | 393 | 1200 | 10000 | 2092.53 | stop |
| 23 | section_summary | low | 5077 | 4852 | 815 | 1200 | 10000 | 4138.72 | stop |
| 24 | section_summary | low | 1426 | 1201 | 207 | 1200 | 10000 | 1384.49 | stop |
| 25 | section_summary | low | 3644 | 3419 | 733 | 1200 | 10000 | 3398.83 | stop |
| 26 | section_summary | low | 3770 | 3545 | 805 | 1200 | 10000 | 3587.48 | stop |
| 27 | section_summary | low | 1382 | 1157 | 288 | 1200 | 10000 | 1478.72 | stop |
| 28 | section_summary | low | 2678 | 2453 | 494 | 1200 | 10000 | 3523.43 | stop |
| 29 | section_summary | low | 1848 | 1623 | 337 | 1200 | 10000 | 2028.08 | stop |
| 30 | section_summary | low | 1443 | 1218 | 418 | 1200 | 10000 | 2025.43 | stop |
| 31 | section_summary | low | 2195 | 1970 | 375 | 1200 | 10000 | 2393.79 | stop |
| 32 | section_summary | low | 6916 | 6691 | 851 | 1200 | 10000 | 6000.45 | stop |
| 33 | section_summary | low | 8185 | 7960 | 1192 | 1200 | 10000 | 7824.23 | stop |
| 34 | section_summary | low | 2083 | 1858 | 475 | 1200 | 10000 | 2773.95 | stop |
| 35 | section_summary | low | 7262 | 7037 | 945 | 1200 | 10000 | 4598.86 | stop |
| 36 | section_summary | low | 8648 | 8423 | 738 | 1200 | 10000 | 3541.25 | stop |
| 37 | section_summary | low | 2243 | 2018 | 1200 | 1200 | 10000 | 3861.07 | length |
| 38 | section_summary | low | 2305 | 2080 | 285 | 1200 | 10000 | 2276.86 | stop |
| 39 | section_summary | low | 6954 | 6729 | 1200 | 1200 | 10000 | 5020.32 | length |
| 40 | section_summary | low | 7016 | 6791 | 516 | 1200 | 10000 | 2390.03 | stop |
| 41 | section_summary | low | 3390 | 3165 | 874 | 1200 | 10000 | 2694.19 | stop |
| 42 | section_summary | low | 1503 | 1278 | 325 | 1200 | 10000 | 1500.14 | stop |
| 43 | group_summary | low | 6481 | 6256 | 1645 | 2500 | 10000 | 5947.87 | stop |
| 44 | group_summary | low | 2726 | 2501 | 1466 | 2500 | 10000 | 5173.31 | stop |
| 45 | document_summary | low | 3999 | 3774 | 922 | 2500 | 10000 | 3497.94 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 2574.02

Judge latency_ms: 1927.53

Total evaluation latency_ms: 4509.67

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | FAIL | Expected Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | In the LLM‑expert agreement table, the “All” setting (447 criterion‑paper evaluations) yields an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8]. When restricting to the “InfoFound” subset (304 evaluations), accuracy drops to 0.951 (a decrease of 0.015) while the positive‑class F1 remains unchanged at 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 127 | 600 | 10000 | 827.88 | stop |
| 2 | answer | medium | 5165 | 4940 | 390 | 3000 | 10000 | 1486.31 | stop |
| 3 | judge | low | 834 | 609 | 335 | 1000 | 10000 | 1189.60 | stop |
| 4 | judge | low | 783 | 558 | 89 | 1000 | 10000 | 737.93 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — two before the automated run and one after — as described in the expert‑agreement comparison [C4].  

In the LLM‑expert agreement table, the “All” setting (447 criterion‑paper evaluations) yields an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8]. When restricting to the “InfoFound” subset (304 evaluations), accuracy drops to 0.951 (a decrease of 0.015) while the positive‑class F1 remains unchanged at 0.762 [C8].  </pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 7723.69

Judge latency_ms: 796.29

Total evaluation latency_ms: 8521.72

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 111 | 600 | 10000 | 786.98 | stop |
| 2 | answer | medium | 4187 | 3962 | 1786 | 3000 | 10000 | 6914.68 | stop |
| 3 | judge | low | 2144 | 1919 | 65 | 1000 | 10000 | 796.29 | stop |

### Finalized answer

<pre>**Motivation**  
The paper is motivated by the industrial shift from static, high‑precision automation to flexible, collaborative robots (cobots) that require control that is robust, adaptive, safe, low‑latency and cost‑effective.  Robotic foundation models (RFMs) are presented as a possible way to meet these constraints, yet the authors note that current foundation models still lack online adaptation, dependable instruction‑following and safe operation needed for true general‑purpose deployment in dynamic factories [S1][S2].

**Assessment method**  
1. **Rubric construction** – The authors first build a detailed industrial‑readiness rubric comprising 149 concrete criteria derived from 47 attributes and organised into eleven implication groups (I1‑I11) that cover adaptability, safety, multimodal HRI, fault detection, precision, real‑time performance, cost‑effective integration, explainability, benchmarking, data‑efficiency and governance [S2].  
2. **Corpus creation** – Three literature corpora are assembled with an automated Python pipeline that translates ASQS queries into the native syntaxes of arXiv, Google Scholar, OpenAlex, Scopus and Semantic Scholar, merges results, removes duplicates, enriches metadata and applies a GPT‑4o relevance filter.  The primary RFM‑related corpus contains 1 025 papers (324 manipulation‑capable RFMs) plus an industrial‑implication corpus (≈300 papers) and a “further” set (113 papers) [S1].  
3. **Automated annotation** – For every paper‑criterion pair a single LLM (GPT‑5.1) is queried to produce a binary fulfil‑ment judgment, confidence score, evidence flag and rationale.  The pipeline is validated on three expert‑rated papers, achieving 96.6 % criterion‑level accuracy, F1 = 0.762, Cohen’s κ = 0.744, with a conservative bias toward false negatives (22.6 % false‑negative rate, 1.9 % false‑positive rate) [S1].  

**Main findings**  
* **Overall coverage** – Even the five highest‑scoring models satisfy only about 11–12 % of the 149 criteria (proportional scores 0.11–0.12) [S1].  
* **Implication‑level results** – Across the full corpus the three most‑covered implication groups are adaptability/flexibility (I1), benchmarking/evaluation (I10) and data‑requirements/usage (I11), with breadth scores ≈0.75 but shallow depth (average criterion coverage ≈0.09).  The “Top‑50” subset reaches universal breadth (1.0) for seven implications, yet the best depth values only reach ≈0.238 for I1, I10 and I11 [S2].  
* **Weak areas** – Safety/compliance (I2) and real‑time performance (I6) are especially poor (ACC ≈ 0.019 and 0.036 respectively).  Only ≤4 % of models meet safety, interaction or real‑time criteria, and ≤14 % meet robustness criteria [S2].  
* **Best individual scores** – Gemini Robotics 1.5 attains the highest single‑implication score (I1 = 0.44) and the highest total applicability (0.12).  Other spikes are modest (e.g., DexGrasp VLA I10 ≈ 0.31, HAMMER I11 ≈ 0.36) [S1][S2].  
* **Gap analysis** – Gap coefficients range from 0.5 to 0.98, indicating large mismatches between what the literature discusses and what is actually satisfied, with the largest gaps in safety, interaction, real‑time performance and cost‑effectiveness [S2].

**Limitations**  
* The tabular data (Tables 14‑15, Appendix D) could not be reliably reconstructed, so the analysis relies on narrative descriptions [S2].  
* The “Total” applicability column in Appendix D is ambiguous because the aggregation rule is hidden and scores were extracted automatically by the LLM pipeline [S2].  
* The overall methodology is opaque: the rubric itself is not experimentally validated, and the quantitative analysis is based solely on literature‑level annotation rather than empirical robot tests [S2].  
* Because many papers do not report all relevant model capabilities, the automated pipeline tends to produce false‑negative judgments, leading to an under‑estimation of actual capability coverage [S1].

**Effect of unreported model capabilities**  
When a model’s capability (e.g., safety‑gating, real‑time latency, hot‑swappable components) is not explicitly described in the source paper, the LLM‑based annotator cannot infer it and therefore marks the criterion as unfulfilled.  This systematic under‑reporting contributes to the conservative bias observed in validation (higher false‑negative rate) and inflates the apparent gaps in the industrial‑readiness assessment [S1].

**Scope of expert validation**  
Expert validation was performed on only three papers that had been manually rated by domain experts.  While this small sample yielded high agreement metrics (96.6 % accuracy, κ = 0.744), the limited number of expert‑rated cases means the validation does not fully capture the diversity of models or the full spectrum of industrial criteria [S1].

**Purpose of each appendix**  
* **Appendix A – Related Works** – Summarises existing embodied‑AI surveys and highlights the paucity of RFM‑focused, industry‑oriented reviews [S2].  
* **Appendix B – Literature Research** – Provides the Boolean search strings (ASQS queries) and detailed protocol used to retrieve the primary RFM corpus and the industrial‑implication corpus [S2].  
* **Appendix C – Industrial Implications** – Defines the nine primary and two additional implication groups (I1‑I11) and enumerates the 149 concrete criteria that constitute the industrial‑readiness rubric [S2].  
* **Appendix D – RFM‑Overview** – Presents model‑level scores (including the “Total” applicability column) and the breakdown of each model’s performance across the implication groups [S2].  

These components together support the systematic mapping of a large body of RFM literature onto a multi‑dimensional industrial readiness framework.</pre>
