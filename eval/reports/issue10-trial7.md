# Golden Facts evaluation

Created: 2026-10-13T05:01:12.506952+00:00

Document: industrial-robotics.pdf

Document SHA-256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`

Repetitions per question: 1

Result: FAIL

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 448b719a5bda057038e1913a1887567fb294bbd8

Uncommitted changes: yes

Fixed source: https://arxiv.org/pdf/2603.06749v1

Pipeline version: ingest-v2-089e6560bba3d124204992e26e2fd9e08974fd92c6884f46ac33dbb17b965b5a

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: real Application upload/ask and Gateway judges; fresh cache

Training provenance: Public v1 postdates original August 2025 gpt-oss release; exact served cloud weights remain opaque/unproven.

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| SECOND_NUMBER | table2_citation | events | 1/1 (100.0%) |
| SECOND_NUMBER | question_type | events | 1/1 (100.0%) |
| SECOND_NUMBER | expert_agreement | judge | 1/1 (100.0%) |
| SECOND_NUMBER | no_filter_improvement | forbidden | 1/1 (100.0%) |
| SECOND_SUMMARY | question_type | events | 1/1 (100.0%) |
| SECOND_SUMMARY | whole_document_coverage | judge | 0/1 (0.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 785 | 560 | 103 | 1200 | 10000 | 1568.02 | stop |
| 2 | section_summary | low | 1665 | 1440 | 328 | 1200 | 10000 | 1890.06 | stop |
| 3 | section_summary | low | 2739 | 2514 | 387 | 1200 | 10000 | 2053.62 | stop |
| 4 | section_summary | low | 658 | 433 | 96 | 1200 | 10000 | 897.16 | stop |
| 5 | section_summary | low | 1082 | 857 | 145 | 1200 | 10000 | 1242.34 | stop |
| 6 | section_summary | low | 2768 | 2543 | 500 | 1200 | 10000 | 3334.92 | stop |
| 7 | section_summary | low | 2027 | 1802 | 317 | 1200 | 10000 | 2499.32 | stop |
| 8 | section_summary | low | 642 | 417 | 144 | 1200 | 10000 | 1184.49 | stop |
| 9 | section_summary | low | 1463 | 1238 | 184 | 1200 | 10000 | 2104.51 | stop |
| 10 | section_summary | low | 2402 | 2177 | 316 | 1200 | 10000 | 2688.47 | stop |
| 11 | section_summary | low | 1472 | 1247 | 252 | 1200 | 10000 | 1799.09 | stop |
| 12 | section_summary | low | 1333 | 1108 | 232 | 1200 | 10000 | 2265.39 | stop |
| 13 | section_summary | low | 996 | 771 | 130 | 1200 | 10000 | 995.31 | stop |
| 14 | section_summary | low | 882 | 657 | 88 | 1200 | 10000 | 864.20 | stop |
| 15 | section_summary | low | 834 | 609 | 99 | 1200 | 10000 | 925.68 | stop |
| 16 | section_summary | low | 1630 | 1405 | 284 | 1200 | 10000 | 1565.41 | stop |
| 17 | section_summary | low | 1255 | 1030 | 169 | 1200 | 10000 | 1911.10 | stop |
| 18 | section_summary | low | 1658 | 1433 | 199 | 1200 | 10000 | 1341.42 | stop |
| 19 | section_summary | low | 2859 | 2634 | 520 | 1200 | 10000 | 3309.36 | stop |
| 20 | section_summary | low | 852 | 627 | 113 | 1200 | 10000 | 1056.10 | stop |
| 21 | section_summary | low | 2721 | 2496 | 447 | 1200 | 10000 | 2929.58 | stop |
| 22 | section_summary | low | 5047 | 4822 | 841 | 1200 | 10000 | 5017.59 | stop |
| 23 | section_summary | low | 2518 | 2293 | 430 | 1200 | 10000 | 2870.10 | stop |
| 24 | section_summary | low | 1439 | 1214 | 344 | 1200 | 10000 | 1877.30 | stop |
| 25 | section_summary | low | 3614 | 3389 | 723 | 1200 | 10000 | 4368.95 | stop |
| 26 | section_summary | low | 3740 | 3515 | 761 | 1200 | 10000 | 3815.31 | stop |
| 27 | section_summary | low | 2648 | 2423 | 520 | 1200 | 10000 | 3099.23 | stop |
| 28 | section_summary | low | 1380 | 1155 | 266 | 1200 | 10000 | 1599.39 | stop |
| 29 | section_summary | low | 1818 | 1593 | 309 | 1200 | 10000 | 2341.70 | stop |
| 30 | section_summary | low | 1336 | 1111 | 299 | 1200 | 10000 | 2260.00 | stop |
| 31 | section_summary | low | 2162 | 1937 | 467 | 1200 | 10000 | 4204.20 | stop |
| 32 | section_summary | low | 7124 | 6899 | 546 | 1200 | 10000 | 4154.86 | stop |
| 33 | section_summary | low | 7136 | 6911 | 624 | 1200 | 10000 | 4020.96 | stop |
| 34 | section_summary | low | 8155 | 7930 | 1200 | 1200 | 10000 | 8340.39 | length |
| 35 | section_summary | low | 8217 | 7992 | 272 | 1200 | 10000 | 2721.03 | stop |
| 36 | section_summary | low | 2053 | 1828 | 293 | 1200 | 10000 | 2327.25 | stop |
| 37 | section_summary | low | 8643 | 8418 | 1200 | 1200 | 10000 | 7001.35 | length |
| 38 | section_summary | low | 1106 | 881 | 579 | 1200 | 10000 | 3022.04 | stop |
| 39 | section_summary | low | 8705 | 8480 | 323 | 1200 | 10000 | 2395.24 | stop |
| 40 | section_summary | low | 1196 | 971 | 328 | 1200 | 10000 | 1899.55 | stop |
| 41 | section_summary | low | 1445 | 1220 | 341 | 1200 | 10000 | 1790.37 | stop |
| 42 | section_summary | low | 2219 | 1994 | 652 | 1200 | 10000 | 1913.02 | stop |
| 43 | section_summary | low | 1256 | 1031 | 386 | 1200 | 10000 | 1279.86 | stop |
| 44 | group_summary | low | 6310 | 6085 | 1925 | 2500 | 10000 | 5802.72 | stop |
| 45 | group_summary | low | 2991 | 2766 | 1962 | 2500 | 10000 | 5040.03 | stop |
| 46 | document_summary | low | 4723 | 4498 | 962 | 2500 | 10000 | 3150.32 | stop |

## SECOND_NUMBER — repetition 1

Question: Identify the manually annotated expert-validation subset. In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Identify the manually annotated expert-validation subset. In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.

Sub-queries: [&#x27;InfoFound vs All overall accuracy expert-validation subset&#x27;, &#x27;InfoFound vs All positive-class F1 expert-validation subset&#x27;, &#x27;evaluation counts InfoFound and All expert-validation&#x27;]

Ask latency_ms: 3577.49

Judge latency_ms: 1752.46

Total evaluation latency_ms: 5336.66

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| table2_citation | events | PASS | Used Citation resolves to the required Table Chunk | C4 |
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| expert_agreement | judge | PASS | Required claim supported by verbatim evidence | The expert‑validation subset that was manually annotated consists of **447 criterion‑level evaluations** (N = 447) [C1][C4].<br><br>When the analysis is restricted to the “InfoFound” cases (i.e., only those LLM outputs flagged as information‑found), the evaluation set shrinks to **304 evaluations** [C4].  <br><br>\| Setting \| N (evaluations) \| Accuracy \| Positive‑class F1 \|<br>\|--------\|----------------\|----------\|-------------------\|<br>\| **All** \| 447 \| 0.966 \| 0.762 \|<br>\| **InfoFound** \| 304 \| 0.951 \| 0.762 \|<br><br>Thus, using the InfoFound subset **lowers overall accuracy** from 0.966 to 0.951, while the **positive‑class F1 score remains unchanged** at 0.762 [C4]. |
| no_filter_improvement | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 851 | 512 | 205 | 600 | 10000 | 828.01 | stop |
| 2 | answer | medium | 2767 | 2542 | 636 | 3000 | 10000 | 2218.89 | stop |
| 3 | judge | low | 894 | 669 | 337 | 1000 | 10000 | 1062.02 | stop |
| 4 | judge | low | 843 | 618 | 88 | 1000 | 10000 | 690.44 | stop |

### Finalized answer

<pre>The expert‑validation subset that was manually annotated consists of **447 criterion‑level evaluations** (N = 447) [C1][C4].

When the analysis is restricted to the “InfoFound” cases (i.e., only those LLM outputs flagged as information‑found), the evaluation set shrinks to **304 evaluations** [C4].  

| Setting | N (evaluations) | Accuracy | Positive‑class F1 |
|--------|----------------|----------|-------------------|
| **All** | 447 | 0.966 | 0.762 |
| **InfoFound** | 304 | 0.951 | 0.762 |

Thus, using the InfoFound subset **lowers overall accuracy** from 0.966 to 0.951, while the **positive‑class F1 score remains unchanged** at 0.762 [C4].</pre>

## SECOND_SUMMARY — repetition 1

Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations (including validation scope and missing reported evidence), and give the purpose of each appendix.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize the whole document&#x27;s motivation, assessment method, main findings and limitations (including validation scope and missing reported evidence), and give the purpose of each appendix.

Sub-queries: []

Ask latency_ms: 4640.69

Judge latency_ms: 1276.13

Total evaluation latency_ms: 5920.05

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| whole_document_coverage | judge | FAIL | Required claim not asserted |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 848 | 509 | 72 | 600 | 10000 | 624.24 | stop |
| 2 | answer | medium | 4925 | 4700 | 1772 | 3000 | 10000 | 3989.59 | stop |
| 3 | judge | low | 2292 | 2067 | 75 | 1000 | 10000 | 1276.13 | stop |

### Finalized answer

<pre>**Motivation**  
The survey frames the current bottleneck in industrial robotics as a *control* problem rather than an actuation problem and points to collaborative robots (cobots) that must be commissioned quickly, operate safely near humans, and adapt to variable tasks, environments and sensing modalities while meeting industrial constraints such as low latency, reliability and cost [S1]. To satisfy these demands the authors propose **Robotic Foundation Models (RFMs)** – large‑scale, self‑supervised models that ingest heterogeneous multimodal data and exhibit emergent reasoning and programming capabilities [S1]. RFMs are positioned as a way to move from narrow, rule‑based control toward “foundation‑model‑driven” autonomy, but the authors note that true industrial‑grade autonomy still requires robust online adaptation, dependable instruction following and safe operation under uncertainty [S1].

**Assessment method**  
1. **Corpus construction** – Three literature corpora were built with a fully automated Python pipeline that translates Academic Search Query Syntax into native queries for arXiv, Google Scholar, OpenAlex, Scopus and Semantic Scholar, merges results, removes duplicates, enriches missing metadata and applies GPT‑4o‑based semantic relevance filters. The *main corpus* contains 1 025 papers (341 describing control‑or integrated RFMs, 324 manipulation‑focused); an *industrial‑implication corpus* of 125 manually vetted papers supplies the industrial requirements; auxiliary searches add 113 more publications [S1].  
2. **Industrial rubric** – Eleven inter‑dependent industrial implications (I1–I11) are defined, expanded into 47 concrete attributes and a 149‑item criteria catalogue (Appendix C) that cover model capabilities, ecosystem concerns and joint requirements [S1][S2].  
3. **Automated annotation** – An evaluation pipeline uses GPT‑5.1 to extract evidence from each of the 324 manipulation‑capable RFMs and to decide, for every criterion, whether it is fulfilled. Each criterion‑paper pair is isolated in a fresh vector store; the LLM outputs a binary judgment, confidence score, evidence flag, extracted quote and rationale [S2].  
4. **Validation** – The pipeline’s judgments were validated against three blind expert‑rated papers, achieving 96.6 % accuracy at the criterion level, a 1.9 % false‑positive rate and a 22.6 % false‑negative rate, reflecting the deliberately conservative policy [S2].

**Main findings**  
* **Overall maturity** – The average catalogue coverage across all 324 models is only 0.11 ± 0.12, indicating a strong ceiling effect; even the best system reaches at most 0.12 of the total criteria [S2].  
* **Top‑performing models** – Gemini Robotics 1.5 attains the highest total maturity (0.12) mainly because of a strong adaptability score (I1 = 0.44). Four other models (Collab‑VLA, GF‑VLA, OneTwo‑VLA, SC‑VLA) each reach 0.11 total maturity with different strength areas (human‑robot interaction, data‑efficiency, flexibility, robustness/precision) [S2].  
* **Implication coverage** – Only three implications—adaptability/flexibility (I1), benchmarking/evaluation (I10) and data‑requirements/efficiency (I11)—are repeatedly addressed, with breadth‑coverage near 1.0 for these three (≈ 0.75). Safety/compliance (I2), human‑robot interaction (I3), real‑time performance (I6) and cost‑effectiveness (I7) remain consistently low (ACC ≈ 0.02–0.07) [S2].  
* **Score distribution** – Most models score below 0.04; a few reach ≈ 0.2; a single outlier (Gemini [157]) attains 1.5. Per‑criterion maxima are modest (0.31 for I11 – generalisation, 0.29 for I5 – safety/robustness); several criteria (I3, I4, I7, I8) are often zero, indicating near‑absence of human‑robot interaction, cost‑effectiveness and related attributes [S2].  
* **Gap analysis** – Large evidence‑fulfilled gaps (gc ≈ 0.5–0.98) and modest explicitness of fulfilled criteria show that most studies provide only partial, criterion‑incomplete solutions, especially for safety, real‑time performance, integration and human‑robot interaction [S2].

**Limitations (including validation scope and missing reported evidence)**  
* **Table reconstruction** – Many quantitative tables could not be reliably reconstructed by the extraction system (marked 「結構未能可靠重建」); therefore specific numeric rows or column associations are omitted and comparative claims rely solely on narrative aggregates [S2].  
* **Reliance on LLM annotation** – The audit depends on large‑language‑model judgments without external validation beyond the three expert‑rated papers, introducing potential systematic bias despite the high reported accuracy [S2].  
* **Scope of validation** – Validation was performed on only three blind expert‑rated papers (447 assessments), so the reported 96.6 % accuracy reflects a limited validation sample [S2].  
* **Literature search reporting** – The query design and execution are described, but retrieval statistics (e.g., number of papers retrieved per query) are not reported, limiting confidence in the completeness of the underlying corpora [S2].  
* **Coverage metrics** – The average catalogue coverage (0.11) and related statistics are derived from the authors’ own rubric and may not capture unmeasured aspects of model capability [S2].

**Purpose of each appendix**  
* **Appendix A – Related Works** – Situates the study within the broader survey literature, enumerating 55 recent surveys on embodied AI, VLA models and foundation‑model‑driven robotics and summarising their thematic coverage [S2].  
* **Appendix B – Literature Research** – Details the systematic query design (Boolean strings, Python‑compatible syntax, database adaptation) used to assemble the main and industrial‑implication corpora [S2].  
* **Appendix C – Industrial Implications** – Presents the 11 × 47 matrix of concrete attributes and the 149‑item criteria catalogue that operationalise the industrial implications for evaluating RFMs [S1][S2].  
* **Appendix D – RFM Overview** – Provides the audited list of 324 manipulation‑capable RFMs, the evidence extraction procedure and the raw annotation results that underpin the maturity analysis [S2].  
* **(Appendix C4 – mentioned in the main text)** – Contains the full 149‑item criteria catalogue, organised into RFM‑centric, ecosystem‑centric and joint scopes, serving as the reference for the automated evaluation [S1].  

These points together capture the document’s motivation, how the authors assessed RFMs, the principal empirical outcomes, the acknowledged limitations, and the role of each appendix, all supported by the supplied excerpts.</pre>
