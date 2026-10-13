# Golden Facts evaluation

Created: 2026-10-13T06:03:02.291417+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 1286357f2bed9d4d39d4ffda91a05b3f9bbb5c2d

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-05cc5da8e95893e7c25dcac663c7aa098220e11695f560d234e74010a392459a

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
| 1 | section_summary | low | 865 | 640 | 98 | 1200 | 10000 | 1068.26 | stop |
| 2 | section_summary | low | 1745 | 1520 | 331 | 1200 | 10000 | 2097.65 | stop |
| 3 | section_summary | low | 2848 | 2623 | 398 | 1200 | 10000 | 2178.18 | stop |
| 4 | section_summary | low | 2819 | 2594 | 468 | 1200 | 10000 | 2647.00 | stop |
| 5 | section_summary | low | 738 | 513 | 113 | 1200 | 10000 | 1478.55 | stop |
| 6 | section_summary | low | 2107 | 1882 | 344 | 1200 | 10000 | 2672.90 | stop |
| 7 | section_summary | low | 1162 | 937 | 137 | 1200 | 10000 | 1708.20 | stop |
| 8 | section_summary | low | 2482 | 2257 | 319 | 1200 | 10000 | 1935.49 | stop |
| 9 | section_summary | low | 722 | 497 | 124 | 1200 | 10000 | 1015.00 | stop |
| 10 | section_summary | low | 1076 | 851 | 134 | 1200 | 10000 | 994.63 | stop |
| 11 | section_summary | low | 1543 | 1318 | 238 | 1200 | 10000 | 2151.97 | stop |
| 12 | section_summary | low | 1552 | 1327 | 241 | 1200 | 10000 | 1435.97 | stop |
| 13 | section_summary | low | 1413 | 1188 | 253 | 1200 | 10000 | 2274.81 | stop |
| 14 | section_summary | low | 962 | 737 | 111 | 1200 | 10000 | 976.12 | stop |
| 15 | section_summary | low | 1335 | 1110 | 254 | 1200 | 10000 | 1481.44 | stop |
| 16 | section_summary | low | 914 | 689 | 85 | 1200 | 10000 | 904.53 | stop |
| 17 | section_summary | low | 1710 | 1485 | 309 | 1200 | 10000 | 1677.38 | stop |
| 18 | section_summary | low | 1738 | 1513 | 216 | 1200 | 10000 | 1541.01 | stop |
| 19 | section_summary | low | 2939 | 2714 | 508 | 1200 | 10000 | 3562.20 | stop |
| 20 | section_summary | low | 932 | 707 | 128 | 1200 | 10000 | 1023.30 | stop |
| 21 | section_summary | low | 2801 | 2576 | 480 | 1200 | 10000 | 2894.11 | stop |
| 22 | section_summary | low | 5127 | 4902 | 767 | 1200 | 10000 | 4151.04 | stop |
| 23 | section_summary | low | 2598 | 2373 | 444 | 1200 | 10000 | 2511.87 | stop |
| 24 | section_summary | low | 5189 | 4964 | 188 | 1200 | 10000 | 1528.46 | stop |
| 25 | section_summary | low | 3694 | 3469 | 690 | 1200 | 10000 | 3375.57 | stop |
| 26 | section_summary | low | 3820 | 3595 | 792 | 1200 | 10000 | 4305.92 | stop |
| 27 | section_summary | low | 2728 | 2503 | 508 | 1200 | 10000 | 2889.29 | stop |
| 28 | section_summary | low | 3756 | 3531 | 241 | 1200 | 10000 | 1805.88 | stop |
| 29 | section_summary | low | 1898 | 1673 | 272 | 1200 | 10000 | 2465.49 | stop |
| 30 | section_summary | low | 3882 | 3657 | 274 | 1200 | 10000 | 2097.53 | stop |
| 31 | section_summary | low | 2245 | 2020 | 421 | 1200 | 10000 | 2897.21 | stop |
| 32 | section_summary | low | 6916 | 6691 | 870 | 1200 | 10000 | 4779.49 | stop |
| 33 | section_summary | low | 8235 | 8010 | 987 | 1200 | 10000 | 5575.54 | stop |
| 34 | section_summary | low | 2133 | 1908 | 387 | 1200 | 10000 | 2432.74 | stop |
| 35 | section_summary | low | 7111 | 6886 | 826 | 1200 | 10000 | 4063.84 | stop |
| 36 | section_summary | low | 2010 | 1785 | 1200 | 1200 | 10000 | 4568.72 | length |
| 37 | section_summary | low | 8648 | 8423 | 622 | 1200 | 10000 | 3881.14 | stop |
| 38 | section_summary | low | 2072 | 1847 | 415 | 1200 | 10000 | 2710.98 | stop |
| 39 | section_summary | low | 6823 | 6598 | 1200 | 1200 | 10000 | 6192.29 | length |
| 40 | section_summary | low | 6885 | 6660 | 350 | 1200 | 10000 | 2502.61 | stop |
| 41 | section_summary | low | 3098 | 2873 | 894 | 1200 | 10000 | 4045.49 | stop |
| 42 | section_summary | low | 3160 | 2935 | 250 | 1200 | 10000 | 1469.83 | stop |
| 43 | group_summary | low | 6529 | 6304 | 2500 | 2500 | 10000 | 9179.26 | length |
| 44 | group_summary | low | 6591 | 6366 | 511 | 2500 | 10000 | 2904.81 | stop |
| 45 | group_summary | low | 2984 | 2759 | 2027 | 2500 | 10000 | 8433.10 | stop |
| 46 | document_summary | low | 3435 | 3210 | 878 | 2500 | 10000 | 3488.73 | stop |

## SECOND_NUMBER — repetition 1

Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Lookup; expected: Lookup / Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: []

Ask latency_ms: 3627.27

Judge latency_ms: 2372.91

Total evaluation latency_ms: 6022.48

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup / Synthesis; actual Lookup; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | Three model papers were manually annotated for expert validation — two were annotated before the automated run and one after it [C4].<br><br>In the agreement comparison (Table 9), the “All” setting evaluated 447 criterion‑paper pairs and achieved an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].<br>When restricting to cases where the LLM reported that information was found (“InfoFound”), the evaluation count dropped to 304 pairs; accuracy decreased to 0.951 (‑0.015) while the positive‑class F1 remained unchanged at 0.762 [C8]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 854 | 515 | 196 | 600 | 10000 | 1109.60 | stop |
| 2 | answer | medium | 5165 | 4940 | 426 | 3000 | 10000 | 2241.69 | stop |
| 3 | judge | low | 989 | 764 | 388 | 1000 | 10000 | 1565.88 | stop |
| 4 | judge | low | 874 | 649 | 99 | 1000 | 10000 | 807.02 | stop |

### Finalized answer

<pre>Three model papers were manually annotated for expert validation — two were annotated before the automated run and one after it [C4].  

In the agreement comparison (Table 9), the “All” setting evaluated 447 criterion‑paper pairs and achieved an overall accuracy of 0.966 and a positive‑class F1 of 0.762 [C8].  
When restricting to cases where the LLM reported that information was found (“InfoFound”), the evaluation count dropped to 304 pairs; accuracy decreased to 0.951 (‑0.015) while the positive‑class F1 remained unchanged at 0.762 [C8].</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations. Explain how unreported model capabilities affect the assessment and the scope of expert validation, and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 7305.96

Judge latency_ms: 862.81

Total evaluation latency_ms: 8172.43

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 856 | 517 | 101 | 600 | 10000 | 793.47 | stop |
| 2 | answer | medium | 3614 | 3389 | 1542 | 3000 | 10000 | 6469.64 | stop |
| 3 | judge | low | 2156 | 1931 | 70 | 1000 | 10000 | 862.81 | stop |

### Finalized answer

<pre>**Motivation**  
The paper is driven by the emerging shift in manufacturing from tightly programmed, single‑task robots to collaborative cobots that must operate safely with humans, adapt quickly to new tasks, and run on low‑power edge hardware.  To determine whether today’s robot‑foundation models (RFMs) can satisfy these industrial demands, the authors built a systematic catalogue of deployment criteria and audited the literature against it[S2].  The broader context is that RFMs are defined as large‑scale, multimodal systems that generate low‑level actions and can be rapidly adapted across tasks, environments, and hardware, positioning them as potential general‑purpose, zero‑/few‑shot agents for industry[S1].

**Assessment method**  
1. **Criteria catalogue** – Eleven inter‑dependent industrial implications (I1‑I11) were expanded into 47 concrete attributes, yielding 149 items that cover model capabilities, ecosystem requirements, safety, HRI, real‑time performance, cost‑efficiency, explainability, and data usage[S2].  
2. **Literature corpus** – 324 manipulation‑capable RFM papers (48 276 individual criterion decisions) were collected using transparent Boolean search strings (Appendix B) that combined robot‑centric terms with “foundation model”, “multimodal”, etc.[S2].  
3. **Automated evaluation** – An LLM‑based pipeline (Section 8.1) extracted from each paper whether each of the 149 items was satisfied, producing a total industrial‑applicability proportion and eleven implication‑specific scores for every RFM[S2].  
4. **Expert validation** – A separate expert‑LLM review compared the automated decisions to human judgments, achieving 96.6 % accuracy and a Cohen’s κ of 0.744, indicating high but not perfect agreement[S1].

**Main findings**  
* **Overall maturity is low** – All total scores are ≤ 0.12; the best models satisfy only about one‑tenth of the catalogue, with the top five reaching 0.11–0.12[S2].  
* **Adaptability leads** – The strongest single‑implication score (0.44) is for adaptability/flexibility (I1) by Gemini Robotics 1.5; most high‑scoring models also do relatively well on robustness (I4), sensor fusion (I9) or data usage (I11)[S2].  
* **Critical gaps** – Safety/compliance (I2), human‑robot interaction (I3), real‑time operation (I6) and cost‑effectiveness/integration (I7) receive near‑zero scores across the board[S2].  
* **Breadth vs. depth** – Papers frequently mention adaptability, benchmarking (I10) and data usage (I11) (≈ 75 % of papers) but the average criteria coverage (ACC) stays below 0.10, showing shallow treatment of the detailed items[S2]. Even the most cited 50 papers only raise ACC to ≈ 0.23 for those three implications, while the under‑addressed implications remain below 0.05 ACC[S2].  
* **Trade‑off context** – The study notes hardware constraints (e.g., Jetson Orin‑Nano ≈148 TOPS/$ vs. RTX 5090 &gt;120 W) and typical cobot limits (≈6‑axis, 8.5 kg payload, 0.1 mm accuracy, 0.3 kW power) that exacerbate the need for low‑latency, safety‑critical inference[S1].  

**Limitations**  
* **Reliance on text extraction** – All scores are derived from an automated LLM‑based extraction of publication text; they are context‑dependent estimates without confidence intervals, external validation, or direct performance measurements[S2].  
* **Missing fine‑grained data** – Several tables could not be reliably reconstructed (“結構未能可靠重建”), so only the reported aggregate numbers (total scores, breadth‑depth metrics) are available[S2][S1].  
* **Unreported capabilities** – When a model’s capability (e.g., safety gating, deterministic latency) is not explicitly described in the paper, the pipeline records it as absent, which depresses the model’s score even if the capability exists in practice.  This systematic under‑counting inflates the apparent gap between research and industrial readiness.  
* **Scope of expert validation** – The high expert‑LLM agreement (96.6 % accuracy, κ = 0.744) validates the extraction logic but only for the textual evidence present; it does not confirm actual system behaviour or hardware integration[S1].

**Purpose of each appendix**  
* **Appendix A – Related Works** – Lists 55 recent surveys (2023‑2025) on embodied AI, vision‑language‑action, and foundation models for robotics, showing the broader research landscape that informs the criteria catalogue[S2].  
* **Appendix B – Literature Research** – Provides the exact Boolean search strings used to build the RFM‑related and industrial‑implication corpora, ensuring transparency and reproducibility of the literature acquisition[S2].  
* **Appendix C – Industrial Implications** – Enumerates the full set of 149 criteria (I1‑I11 and sub‑items), defining the attributes against which each RFM is evaluated[S2].  
* **Appendix D – RFM Overview** – Supplies a concise description of the surveyed RFMs (e.g., Gemini Robotics 1.5) and their reported capabilities, supporting the quantitative audit presented in Section 8[S2].  

In sum, the document motivates a criteria‑driven audit of RFMs for cobot deployment, uses an LLM‑based extraction pipeline validated by expert review, finds that current models excel only in isolated areas such as adaptability while falling short on safety, real‑time, and cost dimensions, and acknowledges that unreported capabilities and incomplete tables limit the precision of the assessment. The appendices document the survey background, search methodology, criteria definition, and model overview that together make the audit reproducible.</pre>
