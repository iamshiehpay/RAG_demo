# Golden Facts evaluation

Created: 2026-10-13T11:41:00.046593+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Functional operations: PASS (separate from D05 semantic rates)

Call audit: {&quot;budget_violations&quot;: 0, &quot;calls&quot;: 170, &quot;length_attempts&quot;: [], &quot;maximum_estimated_prompt_plus_reservation&quot;: 9617, &quot;maximum_reported_prompt_plus_reservation&quot;: 9392, &quot;missing_reported_prompt_counts&quot;: 0, &quot;router_answer_length_attempts&quot;: 0}

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 7cf91851f9f86527d69c95910f9eadd58cf7b357

Uncommitted changes: yes

Pipeline version: ingest-v2-06fcd637e034ab2a889dbe6ec9bdadac23d3d44977aca74f1e9890287d31876b

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Created: 2026-10-13T11:41:00.045547+00:00

Label: issue11-final-lightrag

D05: Report raw rates/causes; semantic defects do not block delivery.

Effective settings: {&quot;answer_think&quot;: &quot;medium&quot;, &quot;bm25_weight&quot;: 0.0, &quot;chunk_token_target&quot;: 500, &quot;lookup_top_k&quot;: 5, &quot;sub_query_top_k&quot;: 2, &quot;summary_concurrency&quot;: 4, &quot;synthesis_top_k&quot;: 3}

Peak guarded calls by type: {&quot;section_summary&quot;: 4, &quot;group_summary&quot;: 1, &quot;document_summary&quot;: 1, &quot;router&quot;: 1, &quot;answer&quot;: 1, &quot;judge&quot;: 1}

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 3/3 (100.0%) |
| Q1 | motivation | judge | 2/3 (66.7%) |
| Q1 | graph_indexing | judge | 3/3 (100.0%) |
| Q1 | dual_level | judge | 3/3 (100.0%) |
| Q1 | incremental_update | judge | 0/3 (0.0%) |
| Q1 | experiments | judge | 1/3 (33.3%) |
| Q1 | not_all_best | forbidden | 1/3 (33.3%) |
| Q1 | not_all_datasets | forbidden | 2/3 (66.7%) |
| Q1 | conclusion | judge | 3/3 (100.0%) |
| Q2 | question_type | events | 3/3 (100.0%) |
| Q2 | retrieval_methods | judge | 0/3 (0.0%) |
| Q2 | retrieval_cost | judge | 0/3 (0.0%) |
| Q2 | incremental_update | judge | 0/3 (0.0%) |
| Q2 | table1_agriculture_overall | judge | 0/3 (0.0%) |
| Q2 | table1_cs_overall | judge | 0/3 (0.0%) |
| Q2 | table1_legal_overall | judge | 0/3 (0.0%) |
| Q2 | table1_mix_overall | judge | 0/3 (0.0%) |
| Q2 | table3_case_study | judge | 3/3 (100.0%) |
| Q2 | not_all_datasets | forbidden | 3/3 (100.0%) |
| Q3 | required_source_citation | events | 3/3 (100.0%) |
| Q3 | question_type | events | 2/3 (66.7%) |
| Q3 | high_term | contains | 3/3 (100.0%) |
| Q3 | low_term | contains | 3/3 (100.0%) |
| Q3 | origin_term | contains | 3/3 (100.0%) |
| Q3 | table2_baseline | judge | 2/3 (66.7%) |
| Q3 | ablation_meaning | judge | 1/3 (33.3%) |
| Q3 | mix_low_overall | judge | 0/3 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/3 (0.0%) |
| Q3 | not_all_best | forbidden | 3/3 (100.0%) |
| ABSENT_HOTPOT | question_type | events | 3/3 (100.0%) |
| ABSENT_HOTPOT | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_HOTPOT | answer_script | property | 3/3 (100.0%) |
| ABSENT_LICENSE | question_type | events | 3/3 (100.0%) |
| ABSENT_LICENSE | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_GPU | question_type | events | 3/3 (100.0%) |
| ABSENT_GPU | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_GPU | answer_script | property | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 2/3 (66.7%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 0/3 (0.0%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 2/3 (66.7%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 2/3 (66.7%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 1/3 (33.3%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_datasets | forbidden | 1/3 (33.3%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/3 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | answer_script | property | 1/3 (33.3%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 1145 | 920 | 155 | 1200 | 10000 | 1333.66 | stop |
| 2 | section_summary | low | 882 | 657 | 102 | 1200 | 10000 | 1699.76 | stop |
| 3 | section_summary | low | 1674 | 1449 | 214 | 1200 | 10000 | 2044.85 | stop |
| 4 | section_summary | low | 1593 | 1368 | 217 | 1200 | 10000 | 2084.07 | stop |
| 5 | section_summary | low | 1183 | 958 | 167 | 1200 | 10000 | 1016.08 | stop |
| 6 | section_summary | low | 802 | 577 | 107 | 1200 | 10000 | 1027.85 | stop |
| 7 | section_summary | low | 756 | 531 | 124 | 1200 | 10000 | 786.48 | stop |
| 8 | section_summary | low | 878 | 653 | 125 | 1200 | 10000 | 1455.66 | stop |
| 9 | section_summary | low | 1743 | 1518 | 281 | 1200 | 10000 | 2132.91 | stop |
| 10 | section_summary | low | 3418 | 3151 | 275 | 1200 | 10000 | 1755.31 | stop |
| 11 | section_summary | low | 4404 | 4137 | 192 | 1200 | 10000 | 1183.31 | stop |
| 12 | section_summary | low | 3442 | 3175 | 274 | 1200 | 10000 | 2323.77 | stop |
| 13 | section_summary | low | 1258 | 1033 | 179 | 1200 | 10000 | 1101.90 | stop |
| 14 | section_summary | low | 935 | 710 | 131 | 1200 | 10000 | 1034.04 | stop |
| 15 | section_summary | low | 900 | 675 | 200 | 1200 | 10000 | 1258.26 | stop |
| 16 | section_summary | low | 785 | 560 | 111 | 1200 | 10000 | 983.26 | stop |
| 17 | section_summary | low | 737 | 512 | 83 | 1200 | 10000 | 798.15 | stop |
| 18 | section_summary | low | 802 | 577 | 74 | 1200 | 10000 | 737.15 | stop |
| 19 | section_summary | low | 776 | 551 | 110 | 1200 | 10000 | 919.94 | stop |
| 20 | section_summary | low | 862 | 637 | 166 | 1200 | 10000 | 1074.54 | stop |
| 21 | section_summary | low | 814 | 589 | 191 | 1200 | 10000 | 1137.19 | stop |
| 22 | section_summary | low | 766 | 541 | 91 | 1200 | 10000 | 779.30 | stop |
| 23 | section_summary | low | 879 | 654 | 123 | 1200 | 10000 | 1590.88 | stop |
| 24 | section_summary | low | 752 | 527 | 93 | 1200 | 10000 | 1403.18 | stop |
| 25 | section_summary | low | 741 | 516 | 84 | 1200 | 10000 | 777.30 | stop |
| 26 | section_summary | low | 843 | 618 | 172 | 1200 | 10000 | 1144.62 | stop |
| 27 | section_summary | low | 3919 | 3652 | 216 | 1200 | 10000 | 1287.86 | stop |
| 28 | section_summary | low | 818 | 593 | 170 | 1200 | 10000 | 1104.37 | stop |
| 29 | section_summary | low | 832 | 607 | 188 | 1200 | 10000 | 1078.97 | stop |
| 30 | section_summary | low | 829 | 604 | 221 | 1200 | 10000 | 1846.63 | stop |
| 31 | group_summary | low | 5561 | 5336 | 999 | 2500 | 10000 | 3225.98 | stop |
| 32 | document_summary | low | 1985 | 1760 | 975 | 2500 | 10000 | 2934.09 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 5765.37

Judge latency_ms: 11291.03

Total evaluation latency_ms: 17081.39

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments large language models (LLMs) with a graph‑based text‑indexing pipeline and a dual‑level retrieval framework to address the flat‑representation and limited contextual awareness of existing RAG approaches[S1][S2]. |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | The indexing stage first splits each document into chunks, uses LLM prompts to extract entities and relationships, creates key‑value pairs for graph nodes and edges, and deduplicates them into a compact knowledge graph Ď; this graph supports multi‑hop subgraph queries and enables rapid, precise retrieval of entity‑relationship facts[S4]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | Retrieval is performed at two levels: low‑level queries target specific nodes or edges (e.g., “Who wrote ‘Pride and Prejudice’?”) while high‑level queries address broader topics (e.g., “How does AI influence modern education?”). |
| incremental_update | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | An incremental update module processes new documents with the same steps and unions their nodes and edges with the existing graph, avoiding full re‑indexing and reducing computational overhead[S4].<br><br>For incremental updates, GraphRAG must dismantle and fully rebuild a 1 399‑community structure (≈ 1 399 × 2 × 5 000 tokens), while LightRAG simply integrates new entities into the existing graph, incurring far lower token and API‑call overhead[S13]. |
| experiments | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The system is evaluated on four large‑scale “UltraDomain” datasets (Agriculture, CS, Legal, Mixed) ... **Overall performance (RQ1).**  Table 1 reports win‑rate percentages of four baselines ... LightRAG consistently outperforms the baselines, with especially large gaps on the biggest Legal dataset where baselines achieve only about 20 % win rates while LightRAG dominates; the advantage is most pronounced for the Diversity metric, which LightRAG leads on the Legal set thanks to its dual‑level retrieval[S10]. |
| not_all_best | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | LightRAG consistently outperforms the baselines, with especially large gaps on the biggest Legal dataset where baselines achieve only about 20 % win rates while LightRAG dominates; the advantage is most pronounced for the Diversity metric, which LightRAG leads on the Legal set thanks to its dual‑level retrieval. |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | LightRAG consistently outperforms the baselines, with especially large gaps on the biggest Legal dataset where baselines achieve only about 20 % win rates while LightRAG dominates; the advantage is most pronounced for the Diversity metric, which LightRAG leads on the Legal set thanks to its dual‑level retrieval[S10]. |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | In conclusion, LightRAG advances RAG by (1) introducing a graph‑based indexing method that improves retrieval efficiency and comprehension, (2) employing a dual‑level retrieval paradigm that extracts both specific and abstract information, and (3) supporting seamless incremental updates that keep the knowledge base current with minimal overhead. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 83 | 600 | 10000 | 1370.09 | stop |
| 2 | answer | medium | 5788 | 5563 | 1392 | 3000 | 10000 | 4380.30 | stop |
| 3 | judge | low | 1879 | 1654 | 256 | 1000 | 10000 | 943.96 | stop |
| 4 | judge | low | 1874 | 1649 | 311 | 1000 | 10000 | 3067.70 | stop |
| 5 | judge | low | 1876 | 1651 | 268 | 1000 | 10000 | 1261.72 | stop |
| 6 | judge | low | 1882 | 1657 | 309 | 1000 | 10000 | 1106.13 | stop |
| 7 | judge | low | 1885 | 1660 | 296 | 1000 | 10000 | 1126.54 | stop |
| 8 | judge | low | 1882 | 1657 | 341 | 1000 | 10000 | 1219.90 | stop |
| 9 | judge | low | 1889 | 1664 | 247 | 1000 | 10000 | 1016.86 | stop |
| 10 | judge | low | 1875 | 1650 | 456 | 1000 | 10000 | 1548.21 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments large language models (LLMs) with a graph‑based text‑indexing pipeline and a dual‑level retrieval framework to address the flat‑representation and limited contextual awareness of existing RAG approaches[S1][S2].  

The indexing stage first splits each document into chunks, uses LLM prompts to extract entities and relationships, creates key‑value pairs for graph nodes and edges, and deduplicates them into a compact knowledge graph Ď; this graph supports multi‑hop subgraph queries and enables rapid, precise retrieval of entity‑relationship facts[S4].  An incremental update module processes new documents with the same steps and unions their nodes and edges with the existing graph, avoiding full re‑indexing and reducing computational overhead[S4].  

Retrieval is performed at two levels: low‑level queries target specific nodes or edges (e.g., “Who wrote ‘Pride and Prejudice’?”) while high‑level queries address broader topics (e.g., “How does AI influence modern education?”).  Both levels generate keywords that are matched in a vector database; retrieved items are augmented with one‑hop neighboring nodes and edges to capture higher‑order relatedness, improving relevance and comprehensiveness[S5].  

During answer generation, the retrieved information (names, entity/relationship descriptions, and original‑text excerpts) is concatenated into a unified value set and fed to a general‑purpose LLM, which produces responses aligned with the query intent[S6].  

Complexity analysis shows that the indexing phase requires one LLM call per token in each chunk, while the retrieval phase replaces whole‑chunk vector matches with entity‑level vector searches, markedly lowering retrieval overhead compared with prior graph‑based RAG systems such as GraphRAG[S7].  

The system is evaluated on four large‑scale “UltraDomain” datasets (Agriculture, CS, Legal, Mixed) containing 0.6–5 M tokens each, using GPT‑4o‑mini for both indexing and generation and an LLM‑based multi‑dimensional evaluation (comprehensiveness, diversity, empowerment, overall) because a definitive ground truth is hard to define[S9][S18].  

**Overall performance (RQ1).**  Table 1 reports win‑rate percentages of four baselines (NaiveRAG, RQ‑RAG, HyDE, GraphRAG) against LightRAG across the four datasets and four evaluation dimensions.  LightRAG consistently outperforms the baselines, with especially large gaps on the biggest Legal dataset where baselines achieve only about 20 % win rates while LightRAG dominates; the advantage is most pronounced for the Diversity metric, which LightRAG leads on the Legal set thanks to its dual‑level retrieval[S10].  

**Ablation studies (RQ2).**  Using NaiveRAG as the reference, three ablated variants are examined: “‑High” (low‑level‑only), “‑Low” (high‑level‑only), and “‑Origin” (removing original text from retrieval).  Removing the high‑level component causes a significant drop in most metrics, indicating loss of breadth for complex queries; removing the low‑level component harms comprehensiveness but improves breadth; the full hybrid version achieves balanced performance.  Surprisingly, omitting original text (‑Origin) does not degrade performance and sometimes improves it, suggesting the graph‑extracted information is sufficient and that raw text can introduce noise[S11].  

**Cost and adaptability (RQ4).**  On the Legal dataset, GraphRAG’s retrieval consumes 610 × 1,000 = 610 000 tokens across 610 active level‑2 communities and requires hundreds of API calls, whereas LightRAG generates fewer than 100 tokens for keyword generation and needs only a single API call.  For incremental updates, GraphRAG must dismantle and fully rebuild a 1 399‑community structure (≈ 1 399 × 2 × 5 000 tokens), while LightRAG simply integrates new entities into the existing graph, incurring far lower token and API‑call overhead[S13].  

The authors position LightRAG as addressing two gaps in prior work: the lack of dynamic, scalable graph‑empowered RAG and the inefficiency of brute‑force searches for large queries[S14].  They also situate their approach within broader efforts to combine LLMs and graphs, noting related categories such as “GNNs as Prefix,” “LLMs as Prefix,” and “LLMs‑Graphs Integration”[S15].  

In conclusion, LightRAG advances RAG by (1) introducing a graph‑based indexing method that improves retrieval efficiency and comprehension, (2) employing a dual‑level retrieval paradigm that extracts both specific and abstract information, and (3) supporting seamless incremental updates that keep the knowledge base current with minimal overhead.  The authors claim that these contributions markedly increase the speed and quality of retrieval‑augmented generation while reducing inference costs for large language models[S16].  

No additional limitations beyond the acknowledged difficulty of defining ground truth for high‑level queries are reported[S9].</pre>

## Q1 — repetition 2

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 5350.72

Judge latency_ms: 8526.60

Total evaluation latency_ms: 13900.64

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | LightRAG is a Retrieval‑Augmented Generation system that enhances large language models by adding a graph‑based text‑indexing stage and a dual‑level retrieval framework, aiming to overcome the flat‑representation and limited contextual awareness of prior RAG approaches... |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | In the indexing phase, documents are split into chunks, LLM prompts extract entities and relationships, and key‑value pairs are generated for each node or edge; a deduplication step merges duplicates to form a compact knowledge graph that supports multi‑hop subgraph queries and enables precise, vector‑based retrieval [S4]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The dual‑level retrieval paradigm creates both detailed (low‑level) and abstract (high‑level) query keys.  Low‑level queries retrieve specific entity‑attribute facts, while high‑level queries retrieve broader thematic information; results are combined with one‑hop neighboring nodes and vector similarity matching to improve relevance and coverage [S5]. |
| incremental_update | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | An incremental module processes new documents with the same pipeline and unions their nodes and edges with the existing graph, avoiding full re‑indexing [S4].<br>...<br>for incremental updates, LightRAG integrated new entities without rebuilding the graph, while GraphRAG had to dismantle and regenerate a 1 399‑community structure, incurring far higher token and API‑call overhead [S13]. |
| experiments | judge | FAIL | Required claim not asserted: The answer describes experiments on Agriculture, Computer‑Science, Legal and Mixed datasets and reports stronger answer quality and a pronounced diversity advantage, but it never references &quot;Section 4&quot; as the location of this evaluation, so the full claim is not explicitly stated. |  |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | Across the four datasets and four evaluation dimensions (comprehensiveness, diversity, empowerment, overall), LightRAG achieved higher win rates than all baselines, with the gap widening on the largest Legal dataset where baselines attained only about 20 % win rates [S10]. LightRAG also showed a pronounced advantage in the Diversity metric, especially on the Legal set, which the authors attribute to the dual‑level retrieval paradigm [S10]. Compared with GraphRAG, LightRAG consistently outperformed it on the larger datasets (Agriculture, CS, Legal), demonstrating stronger handling of complex language contexts [S10]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | The authors conclude that LightRAG advances RAG by using graph‑based indexing to improve retrieval efficiency and comprehension, employing a dual‑level retrieval paradigm to address both specific and abstract information needs, and supporting seamless incremental updates that keep the knowledge base current while reducing inference costs for large language models [S16]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 83 | 600 | 10000 | 762.20 | stop |
| 2 | answer | medium | 5788 | 5563 | 1428 | 3000 | 10000 | 4575.37 | stop |
| 3 | judge | low | 1751 | 1526 | 286 | 1000 | 10000 | 1193.54 | stop |
| 4 | judge | low | 1746 | 1521 | 220 | 1000 | 10000 | 949.56 | stop |
| 5 | judge | low | 1748 | 1523 | 243 | 1000 | 10000 | 1074.28 | stop |
| 6 | judge | low | 1754 | 1529 | 260 | 1000 | 10000 | 1044.12 | stop |
| 7 | judge | low | 1757 | 1532 | 246 | 1000 | 10000 | 1158.72 | stop |
| 8 | judge | low | 1754 | 1529 | 331 | 1000 | 10000 | 1153.27 | stop |
| 9 | judge | low | 1761 | 1536 | 157 | 1000 | 10000 | 890.82 | stop |
| 10 | judge | low | 1747 | 1522 | 244 | 1000 | 10000 | 1062.31 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation system that enhances large language models by adding a graph‑based text‑indexing stage and a dual‑level retrieval framework, aiming to overcome the flat‑representation and limited contextual awareness of prior RAG approaches and to provide faster, more scalable updates [S1][S2].  
The design targets three objectives: (1) comprehensive retrieval that captures global information, (2) low‑cost, rapid retrieval through a scalable indexed structure, and (3) quick adaptation of the index to new knowledge [S3].  

In the indexing phase, documents are split into chunks, LLM prompts extract entities and relationships, and key‑value pairs are generated for each node or edge; a deduplication step merges duplicates to form a compact knowledge graph that supports multi‑hop subgraph queries and enables precise, vector‑based retrieval [S4].  An incremental module processes new documents with the same pipeline and unions their nodes and edges with the existing graph, avoiding full re‑indexing [S4].  

The dual‑level retrieval paradigm creates both detailed (low‑level) and abstract (high‑level) query keys.  Low‑level queries retrieve specific entity‑attribute facts, while high‑level queries retrieve broader thematic information; results are combined with one‑hop neighboring nodes and vector similarity matching to improve relevance and coverage [S5].  

During answer generation, the retrieved information (names, entity/relationship descriptions, and original‑text excerpts) is concatenated into a unified value set that is fed to a general‑purpose LLM, which produces responses aligned with the query intent [S6].  

Complexity analysis shows that indexing requires one LLM call per token in a chunk with no extra overhead, and retrieval replaces whole‑chunk vector matches with entity‑level vector searches, markedly reducing retrieval cost compared with GraphRAG’s community‑based traversal [S7].  

Experiments were conducted on four UltraDomain datasets—Agriculture (≈2 M tokens), Computer‑Science (≈2.3 M tokens), Legal (≈5 M tokens), and Mixed (≈0.6 M tokens)—derived from 428 college textbooks [S9][S18].  LightRAG was compared against four baselines: NaiveRAG (vector‑based), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (graph‑enhanced) [S9].  

Across the four datasets and four evaluation dimensions (comprehensiveness, diversity, empowerment, overall), LightRAG achieved higher win rates than all baselines, with the gap widening on the largest Legal dataset where baselines attained only about 20 % win rates [S10].  LightRAG also showed a pronounced advantage in the Diversity metric, especially on the Legal set, which the authors attribute to the dual‑level retrieval paradigm [S10].  Compared with GraphRAG, LightRAG consistently outperformed it on the larger datasets (Agriculture, CS, Legal), demonstrating stronger handling of complex language contexts [S10].  

Ablation studies revealed that removing the high‑level component (‑High) caused significant performance drops due to over‑focus on immediate entities, while removing the low‑level component (‑Low) reduced depth for detailed answers; the full hybrid version achieved balanced performance across dimensions [S11].  Eliminating original text from retrieval (‑Origin) did not markedly degrade performance and sometimes improved results, suggesting the graph‑based index captures sufficient context [S11].  

Case‑study comparisons showed LightRAG winning over GraphRAG and over NaiveRAG in both overall answer quality and specific criteria such as comprehensiveness, diversity, and empowerment [S12][S23][S24].  

Cost analysis on the Legal dataset indicated that LightRAG required fewer than 100 tokens for keyword generation and only a single API call during retrieval, whereas GraphRAG consumed 610 000 tokens and hundreds of API calls; for incremental updates, LightRAG integrated new entities without rebuilding the graph, while GraphRAG had to dismantle and regenerate a 1 399‑community structure, incurring far higher token and API‑call overhead [S13].  

The authors conclude that LightRAG advances RAG by using graph‑based indexing to improve retrieval efficiency and comprehension, employing a dual‑level retrieval paradigm to address both specific and abstract information needs, and supporting seamless incremental updates that keep the knowledge base current while reducing inference costs for large language models [S16].  The implementation is released as open‑source code [S1].</pre>

## Q1 — repetition 3

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 6461.00

Judge latency_ms: 9137.05

Total evaluation latency_ms: 15615.56

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | Existing RAG systems often rely on flat representations and lack contextual awareness, leading to fragmented answers for inter‑dependent entities, so LightRAG incorporates graph structures to capture entity interdependencies and adopts a dual‑level retrieval framework—low‑level retrieval for precise entity‑relation facts and high‑level retrieval for broader topics—to achieve comprehensive information retrieval, higher efficiency, and rapid adaptation without rebuilding the entire index [S2][S5]. |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | The system builds an indexed knowledge graph ˆD by segmenting documents, extracting entities and relationships via LLM prompts, generating key‑value pairs for each node or edge, and deduplicating identical items; this enables multi‑hop subgraph queries and key‑value retrieval, improving on embedding‑matching and chunk‑traversal methods, and supports incremental updates by unioning new nodes/edges with the existing graph [S4]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | adopts a dual‑level retrieval framework—low‑level retrieval for precise entity‑relation facts and high‑level retrieval for broader topics—to achieve comprehensive information retrieval, higher efficiency, and rapid adaptation without rebuilding the entire index [S2][S5]. |
| incremental_update | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | supports incremental updates by unioning new nodes/edges with the existing graph [S4]. ... for incremental updates, LightRAG integrates new entities without full graph reconstruction, resulting in far lower token and API‑call overhead [S13]. |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Evaluation uses four UltraDomain datasets (Agriculture, CS, Legal, Mixed) ranging from 0.6–5 M tokens, generates 125 high‑level questions per dataset, and compares LightRAG against NaiveRAG, RQ‑RAG, HyDE, and GraphRAG using GPT‑4o‑mini for LLM‑based multi‑dimensional evaluation (comprehensiveness, diversity, empowerment, overall) [S9][S18].<br>Across these datasets, LightRAG achieves higher win rates than the baselines, especially on the large Legal dataset where baselines obtain only about 20 % win rates; LightRAG also shows a notable advantage in the Diversity metric, which the authors attribute to the dual‑level retrieval paradigm [S10]. |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | The authors conclude that LightRAG advances Retrieval‑Augmented Generation by providing graph‑based indexing that improves efficiency and comprehension, a dual‑level retrieval paradigm that extracts both specific and abstract information, and seamless incremental updates that keep the knowledge base current while markedly reducing inference costs [S16]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 83 | 600 | 10000 | 726.64 | stop |
| 2 | answer | medium | 5788 | 5563 | 1889 | 3000 | 10000 | 5719.24 | stop |
| 3 | judge | low | 1676 | 1451 | 238 | 1000 | 10000 | 1061.83 | stop |
| 4 | judge | low | 1671 | 1446 | 232 | 1000 | 10000 | 1118.63 | stop |
| 5 | judge | low | 1673 | 1448 | 214 | 1000 | 10000 | 1759.67 | stop |
| 6 | judge | low | 1679 | 1454 | 216 | 1000 | 10000 | 990.16 | stop |
| 7 | judge | low | 1682 | 1457 | 392 | 1000 | 10000 | 1480.29 | stop |
| 8 | judge | low | 1679 | 1454 | 139 | 1000 | 10000 | 888.48 | stop |
| 9 | judge | low | 1686 | 1461 | 144 | 1000 | 10000 | 835.40 | stop |
| 10 | judge | low | 1672 | 1447 | 288 | 1000 | 10000 | 1002.58 | stop |

### Finalized answer

<pre>LightRAG augments large language models with graph‑based text indexing and a dual‑level retrieval system to overcome the flat‑representation limits and weak contextual awareness of existing RAG approaches; it combines graph structures and vector embeddings, includes an incremental update algorithm for rapid data integration, and reports substantial gains in retrieval accuracy, efficiency, and response time, with open‑source code [S1].  
Existing RAG systems often rely on flat representations and lack contextual awareness, leading to fragmented answers for inter‑dependent entities, so LightRAG incorporates graph structures to capture entity interdependencies and adopts a dual‑level retrieval framework—low‑level retrieval for precise entity‑relation facts and high‑level retrieval for broader topics—to achieve comprehensive information retrieval, higher efficiency, and rapid adaptation without rebuilding the entire index [S2][S5].  
The system builds an indexed knowledge graph ˆD by segmenting documents, extracting entities and relationships via LLM prompts, generating key‑value pairs for each node or edge, and deduplicating identical items; this enables multi‑hop subgraph queries and key‑value retrieval, improving on embedding‑matching and chunk‑traversal methods, and supports incremental updates by unioning new nodes/edges with the existing graph [S4].  
Retrieval combines the graph structure with vector embeddings: local and global keywords are extracted, matched in a vector database, and results are augmented with one‑hop neighboring nodes and edges to capture higher‑order relatedness, thereby improving relevance and comprehensiveness [S5].  
Answer generation concatenates the retrieved information (names, entity/relationship descriptions, original‑text excerpts) into values V via a profiling function, which a general‑purpose LLM then consumes to produce answers aligned with the query intent [S6].  
Complexity analysis notes that indexing requires one LLM call per token in each chunk with no extra overhead, while retrieval uses LLM‑generated keywords and vector search over entities/relationships, markedly lowering retrieval overhead compared with GraphRAG’s community‑based traversal [S7].  
Evaluation uses four UltraDomain datasets (Agriculture, CS, Legal, Mixed) ranging from 0.6–5 M tokens, generates 125 high‑level questions per dataset, and compares LightRAG against NaiveRAG, RQ‑RAG, HyDE, and GraphRAG using GPT‑4o‑mini for LLM‑based multi‑dimensional evaluation (comprehensiveness, diversity, empowerment, overall) [S9][S18].  
Across these datasets, LightRAG achieves higher win rates than the baselines, especially on the large Legal dataset where baselines obtain only about 20 % win rates; LightRAG also shows a notable advantage in the Diversity metric, which the authors attribute to the dual‑level retrieval paradigm [S10].  
Compared with GraphRAG, LightRAG consistently outperforms on Agriculture, CS, and Legal datasets, demonstrating stronger handling of complex language contexts and better response variety [S10].  
Ablation studies reveal that removing high‑level retrieval (low‑level‑only) degrades performance on most metrics, while removing low‑level retrieval (high‑level‑only) improves comprehensiveness but reduces depth; the full hybrid mode balances breadth and depth, achieving balanced performance. Moreover, omitting original text (‑Origin) does not significantly hurt performance and can improve results on some datasets, indicating effective graph‑based extraction [S11].  
A case study comparing LightRAG to GraphRAG on a feature‑normalization query selects LightRAG as the overall winner, demonstrating superior answer quality [S12].  
Cost and adaptability analysis on the Legal dataset shows LightRAG uses fewer than 100 tokens for keyword generation and only one API call during retrieval, versus GraphRAG’s 610 000 tokens and hundreds of calls; for incremental updates, LightRAG integrates new entities without full graph reconstruction, resulting in far lower token and API‑call overhead [S13].  
The authors conclude that LightRAG advances Retrieval‑Augmented Generation by providing graph‑based indexing that improves efficiency and comprehension, a dual‑level retrieval paradigm that extracts both specific and abstract information, and seamless incremental updates that keep the knowledge base current while markedly reducing inference costs [S16].</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG vs GraphRAG performance metrics&#x27;, &#x27;LightRAG vs GraphRAG implementation complexity&#x27;]

Ask latency_ms: 5891.35

Judge latency_ms: 10627.13

Total evaluation latency_ms: 16542.80

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer discusses benchmark performance and mentions LightRAG’s dual‑level retrieval, but it does not state that GraphRAG traverses communities nor that LightRAG retrieves with dual‑level keywords as described in Section 3.2/4.1. Therefore the required claim is neither present nor asserted. |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer provides performance win‑rate tables and narrative findings but never states the token count (610 × 1,000) for GraphRAG nor that LightRAG uses fewer than 100 tokens and only one API call. Therefore the required claim is not asserted. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer provides performance tables and narrative findings but does not mention Section 4.5, nor any claim about GraphRAG rebuilding communities or LightRAG incrementally updating its graph. |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | Overall \| Agriculture \| 45.2 % \| 54.8 % \| LightRAG |
| table1_cs_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | \| Overall \| Agriculture \| 45.2 % \| 54.8 % \| LightRAG \|<br>\|  \| CS \| 48.0 % \| 52.0 % \| LightRAG \|<br>\|  \| Legal \| 47.2 % \| 52.8 % \| LightRAG \|<br>\|  \| Mix \| 50.4 % \| 49.6 % \| **GraphRAG** \| |
| table1_legal_overall | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | \| Overall \| Legal \| 47.2 % \| 52.8 % \| LightRAG \| |
| table1_mix_overall | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | \| Overall \| Mix \| 50.4 % \| 49.6 % \| **GraphRAG** \| |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | A qualitative case study (Table 3) also reports LightRAG as the winner over GraphRAG in every evaluated dimension—comprehensiveness, diversity, empowerment, and overall quality[C5]. The detailed LLM‑judge decisions in the same table confirm LightRAG’s superiority across all metrics[C6] |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 113 | 600 | 10000 | 716.12 | stop |
| 2 | answer | medium | 3726 | 3501 | 1566 | 3000 | 10000 | 4652.69 | stop |
| 3 | judge | low | 1641 | 1416 | 209 | 1000 | 10000 | 958.38 | stop |
| 4 | judge | low | 1703 | 1478 | 122 | 1000 | 10000 | 833.43 | stop |
| 5 | judge | low | 1638 | 1413 | 131 | 1000 | 10000 | 797.97 | stop |
| 6 | judge | low | 1701 | 1476 | 208 | 1000 | 10000 | 1111.58 | stop |
| 7 | judge | low | 1706 | 1481 | 272 | 1000 | 10000 | 1914.47 | stop |
| 8 | judge | low | 1699 | 1474 | 200 | 1000 | 10000 | 1118.73 | stop |
| 9 | judge | low | 1700 | 1475 | 240 | 1000 | 10000 | 1605.62 | stop |
| 10 | judge | low | 1646 | 1421 | 266 | 1000 | 10000 | 1268.89 | stop |
| 11 | judge | low | 1639 | 1414 | 143 | 1000 | 10000 | 1018.06 | stop |

### Finalized answer

<pre>**Performance on benchmark datasets**

| Metric | Dataset | GraphRAG win % | LightRAG win % | Which system wins? |
|--------|---------|----------------|----------------|-------------------|
| Comprehensiveness | Agriculture | 45.6 % | 54.4 % | LightRAG |
|  | CS | 48.4 % | 51.6 % | LightRAG |
|  | Legal | 48.4 % | 51.6 % | LightRAG |
|  | Mix | 50.4 % | 49.6 % | **GraphRAG** (LightRAG is slightly lower) |
| Diversity | Agriculture | 22.8 % | 77.2 % | LightRAG |
|  | CS | 40.8 % | 59.2 % | LightRAG |
|  | Legal | 26.4 % | 73.6 % | LightRAG |
|  | Mix | 36.0 % | 64.0 % | LightRAG |
| Empowerment | Agriculture | 41.2 % | 58.8 % | LightRAG |
|  | CS | 45.2 % | 54.8 % | LightRAG |
|  | Legal | 43.6 % | 56.4 % | LightRAG |
|  | Mix | 50.8 % | 49.2 % | **GraphRAG** |
| Overall | Agriculture | 45.2 % | 54.8 % | LightRAG |
|  | CS | 48.0 % | 52.0 % | LightRAG |
|  | Legal | 47.2 % | 52.8 % | LightRAG |
|  | Mix | 50.4 % | 49.6 % | **GraphRAG** |

These win‑rate figures come from Table 1, which lists baseline (GraphRAG) versus candidate (LightRAG) percentages across four datasets and four evaluation dimensions[C3]. LightRAG beats GraphRAG on most metrics and on the three larger corpora (Agriculture, CS, Legal). The only consistent exception is the “Mix” dataset, where GraphRAG’s win rates are marginally higher for Comprehensiveness, Empowerment, and Overall.

**Narrative findings**

The authors explicitly state that LightRAG “consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts” such as Agriculture, CS, and Legal[C4]. They attribute this advantage to LightRAG’s dual‑level retrieval and graph‑based indexing, which capture both low‑level entities and high‑level topics.

**Case‑study evidence**

A qualitative case study (Table 3) also reports LightRAG as the winner over GraphRAG in every evaluated dimension—comprehensiveness, diversity, empowerment, and overall quality[C5]. The detailed LLM‑judge decisions in the same table confirm LightRAG’s superiority across all metrics[C6], but the table is marked “結構未能可靠重建”, indicating that the reconstruction of its structure is not fully reliable; therefore the quantitative details of that table should be treated with caution[C6]. 

**Summary**

- **Quantitative:** LightRAG achieves higher win rates than GraphRAG on most metrics and on the three large‑scale datasets (Agriculture, CS, Legal). The only dataset where GraphRAG retains a slight edge is the mixed‑size “Mix” dataset.
- **Qualitative:** The paper’s narrative and case‑study analysis both claim that LightRAG’s graph‑enhanced, dual‑level retrieval gives it a clear advantage over GraphRAG, especially for complex, large‑scale corpora.</pre>

## Q2 — repetition 2

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG vs GraphRAG performance&#x27;, &#x27;LightRAG vs GraphRAG limitations&#x27;]

Ask latency_ms: 6258.39

Judge latency_ms: 9730.70

Total evaluation latency_ms: 16018.49

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer discusses win‑rate comparisons and overall performance, but does not mention GraphRAG traversing communities or LightRAG retrieving with dual‑level keywords (entities and topics), so the claim is neither stated nor affirmed. |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer discusses win rates and performance metrics but does not mention the token counts (610 × 1,000) or API call details for GraphRAG or LightRAG, so it does not assert the required claim. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer discusses win‑rate comparisons and overall performance, but does not mention Section 4.5 or any behavior about GraphRAG rebuilding communities or LightRAG incrementally updating its graph. Therefore the required claim is neither stated nor affirmed. |  |
| table1_agriculture_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | \| **Overall** \| Agriculture 45.2 % / 54.8 % \| CS 48.0 % / 52.0 % \| Legal 47.2 % / 52.8 % \| Mix 50.4 % / 49.6 % \| LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset[C3] \| |
| table1_cs_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | \| **Overall** \| Agriculture 45.2 % / 54.8 % \| CS 48.0 % / 52.0 % \| Legal 47.2 % / 52.8 % \| Mix 50.4 % / 49.6 % \| LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset[C3] \| |
| table1_legal_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | \| **Overall** \| Agriculture 45.2 % / 54.8 % \| CS 48.0 % / 52.0 % \| Legal 47.2 % / 52.8 % \| Mix 50.4 % / 49.6 % \| LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset[C3] \| |
| table1_mix_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | \| **Overall** \| Agriculture 45.2 % / 54.8 % \| CS 48.0 % / 52.0 % \| Legal 47.2 % / 52.8 % \| Mix 50.4 % / 49.6 % \| LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset[C3] \| |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | In a concrete example (machine‑learning query), LightRAG was judged by an LLM to be superior to GraphRAG in every evaluated dimension—Comprehensiveness, Diversity, Empowerment, and Overall—demonstrating that the quantitative advantage can translate to real‑world answer quality[C5][C6]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 131 | 600 | 10000 | 911.82 | stop |
| 2 | answer | medium | 3852 | 3627 | 1474 | 3000 | 10000 | 4866.58 | stop |
| 3 | judge | low | 1634 | 1409 | 144 | 1000 | 10000 | 866.86 | stop |
| 4 | judge | low | 1696 | 1471 | 112 | 1000 | 10000 | 791.70 | stop |
| 5 | judge | low | 1631 | 1406 | 144 | 1000 | 10000 | 918.43 | stop |
| 6 | judge | low | 1694 | 1469 | 335 | 1000 | 10000 | 1321.16 | stop |
| 7 | judge | low | 1699 | 1474 | 372 | 1000 | 10000 | 1339.46 | stop |
| 8 | judge | low | 1692 | 1467 | 328 | 1000 | 10000 | 1351.11 | stop |
| 9 | judge | low | 1693 | 1468 | 329 | 1000 | 10000 | 1290.83 | stop |
| 10 | judge | low | 1639 | 1414 | 236 | 1000 | 10000 | 957.41 | stop |
| 11 | judge | low | 1632 | 1407 | 146 | 1000 | 10000 | 893.74 | stop |

### Finalized answer

<pre>**Overall performance**

Across the four benchmark datasets (Agriculture, CS, Legal, Mix) and the four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG generally achieves higher win rates than GraphRAG. In the three larger, domain‑specific corpora (Agriculture, CS, Legal) LightRAG’s win rates exceed GraphRAG’s for every metric, confirming the authors’ claim that “LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts”[C4].

**Detailed win‑rate comparison (Table 1)**  

| Metric / Dataset | GraphRAG win % | LightRAG win % | Which system wins? |
|-------------------|----------------|----------------|--------------------|
| **Comprehensiveness** | Agriculture 45.6 % / LightRAG 54.4 % | CS 48.4 % / 51.6 % | Legal 48.4 % / 51.6 % | LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset (50.4 % / 49.6 %)[C3] |
| **Diversity** | Agriculture 22.8 % / 77.2 % | CS 40.8 % / 59.2 % | Legal 26.4 % / 73.6 % | Mix 36.0 % / 64.0 % | LightRAG wins on all four datasets[C3] |
| **Empowerment** | Agriculture 41.2 % / 58.8 % | CS 45.2 % / 54.8 % | Legal 43.6 % / 56.4 % | Mix 50.8 % / 49.2 % | LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset[C3] |
| **Overall** | Agriculture 45.2 % / 54.8 % | CS 48.0 % / 52.0 % | Legal 47.2 % / 52.8 % | Mix 50.4 % / 49.6 % | LightRAG wins on Agriculture, CS and Legal; GraphRAG wins on the mixed dataset[C3] |

**Key observations**

1. **Larger corpora advantage** – LightRAG’s superiority is most pronounced on the three large, domain‑specific datasets (Agriculture, CS, Legal), where its win rates are 6–9 percentage points higher than GraphRAG for Comprehensiveness, 18–27 pp higher for Diversity, and 12–13 pp higher for Empowerment[C4].

2. **Mixed dataset nuance** – On the “Mix” dataset, GraphRAG slightly outperforms LightRAG for Comprehensiveness, Empowerment, and Overall (the baseline win rates are higher than LightRAG’s), while LightRAG still leads on Diversity[C3].

3. **Qualitative case study** – In a concrete example (machine‑learning query), LightRAG was judged by an LLM to be superior to GraphRAG in every evaluated dimension—Comprehensiveness, Diversity, Empowerment, and Overall—demonstrating that the quantitative advantage can translate to real‑world answer quality[C5][C6].

**Conclusion**

LightRAG generally outperforms GraphRAG, especially on large, complex datasets and across most evaluation dimensions. The only consistent exception is the mixed dataset, where GraphRAG retains a slight edge on three of the four metrics. This pattern aligns with the authors’ narrative that graph‑enhanced retrieval (as embodied by LightRAG) yields better performance on large‑scale corpora while still being competitive on more heterogeneous data.</pre>

## Q2 — repetition 3

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG vs GraphRAG performance&#x27;, &#x27;LightRAG vs GraphRAG limitations&#x27;]

Ask latency_ms: 6876.58

Judge latency_ms: 9167.52

Total evaluation latency_ms: 16073.24

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer does not mention GraphRAG traversing communities nor describe LightRAG retrieving with dual-level keywords as stated in the claim; it only discusses performance results. |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer discusses win‑rate tables and performance metrics but never mentions Section 4.5, token counts (610 × 1,000), or API call details for GraphRAG or LightRAG, so it does not assert the claimed retrieval cost comparison. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer discusses win‑rate tables and performance comparisons, but does not mention Section 4.5 or any claim about GraphRAG rebuilding communities or LightRAG incrementally updating its graph. |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | * Overall 45.2 % / **54.8 %** |
| table1_cs_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | * Overall 48.0 % / **52.0 %**[C3] |
| table1_legal_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | * Overall 47.2 % / **52.8 %**[C3] |
| table1_mix_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | * **Mix dataset** – GraphRAG is superior for three of the four metrics:  <br>  * Comprehensiveness **50.4 %** / 49.6 % (GraphRAG higher)  <br>  * Diversity 36.0 % / **64.0 %** (LightRAG higher)  <br>  * Empowerment **50.8 %** / 49.2 % (GraphRAG higher)  <br>  * Overall **50.4 %** / 49.6 % (GraphRAG higher)[C3] |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | A qualitative case study (Table 3) reports that LightRAG was judged superior to GraphRAG in comprehensiveness, diversity, empowerment, and overall quality for a machine‑learning query[C5]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 131 | 600 | 10000 | 817.27 | stop |
| 2 | answer | medium | 3852 | 3627 | 1687 | 3000 | 10000 | 5373.03 | stop |
| 3 | judge | low | 1672 | 1447 | 180 | 1000 | 10000 | 1069.73 | stop |
| 4 | judge | low | 1734 | 1509 | 113 | 1000 | 10000 | 866.95 | stop |
| 5 | judge | low | 1669 | 1444 | 135 | 1000 | 10000 | 918.20 | stop |
| 6 | judge | low | 1732 | 1507 | 243 | 1000 | 10000 | 1156.85 | stop |
| 7 | judge | low | 1737 | 1512 | 172 | 1000 | 10000 | 952.39 | stop |
| 8 | judge | low | 1730 | 1505 | 216 | 1000 | 10000 | 1214.07 | stop |
| 9 | judge | low | 1731 | 1506 | 330 | 1000 | 10000 | 1221.28 | stop |
| 10 | judge | low | 1677 | 1452 | 224 | 1000 | 10000 | 902.71 | stop |
| 11 | judge | low | 1670 | 1445 | 153 | 1000 | 10000 | 865.34 | stop |

### Finalized answer

<pre>**Overall performance (win‑rate tables)**  
The paper reports direct win‑rate comparisons between GraphRAG (baseline) and LightRAG (candidate) in Table 1. For each metric the cell shows “baseline / candidate” percentages.

* **Agriculture dataset** – LightRAG wins on all four metrics:  
  * Comprehensiveness 45.6 % / **54.4 %**  
  * Diversity 22.8 % / **77.2 %**  
  * Empowerment 41.2 % / **58.8 %**  
  * Overall 45.2 % / **54.8 %**[C3]  

* **Computer‑Science (CS) dataset** – LightRAG also leads on every metric:  
  * Comprehensiveness 48.4 % / **51.6 %**  
  * Diversity 40.8 % / **59.2 %**  
  * Empowerment 45.2 % / **54.8 %**  
  * Overall 48.0 % / **52.0 %**[C3]  

* **Legal dataset** (the largest and most complex) – LightRAG again outperforms GraphRAG across the board:  
  * Comprehensiveness 48.4 % / **51.6 %**  
  * Diversity 26.4 % / **73.6 %**  
  * Empowerment 43.6 % / **56.4 %**  
  * Overall 47.2 % / **52.8 %**[C3]  

* **Mix dataset** – GraphRAG is superior for three of the four metrics:  
  * Comprehensiveness **50.4 %** / 49.6 % (GraphRAG higher)  
  * Diversity 36.0 % / **64.0 %** (LightRAG higher)  
  * Empowerment **50.8 %** / 49.2 % (GraphRAG higher)  
  * Overall **50.4 %** / 49.6 % (GraphRAG higher)[C3]

**Narrative findings**  
The authors explicitly state that “LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts (Agriculture, CS, Legal)”[C4]. They attribute this advantage to LightRAG’s dual‑level retrieval that better captures both low‑level entities and high‑level topics.

**Case‑study illustration**  
A qualitative case study (Table 3) reports that LightRAG was judged superior to GraphRAG in comprehensiveness, diversity, empowerment, and overall quality for a machine‑learning query[C5]. However, the table is marked 「結構未能可靠重建」, meaning its structure could not be reliably reconstructed; therefore the quantitative details of that case should be treated with caution[C6].

**Summary of the comparison**  
- On the three large, domain‑specific corpora (Agriculture, CS, Legal), LightRAG achieves higher win rates than GraphRAG across all evaluated dimensions.  
- On the mixed‑domain corpus, GraphRAG wins on comprehensiveness, empowerment, and overall score, while LightRAG only leads on diversity.  
- The authors’ qualitative analysis and the case‑study narrative further emphasize LightRAG’s edge in handling complex queries and delivering more diverse, empowering responses, especially in large‑scale settings.  

Thus, LightRAG generally surpasses GraphRAG, especially on larger, more complex datasets, but the advantage is not universal—GraphRAG remains stronger on certain metrics within the mixed dataset.</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 4417.85

Judge latency_ms: 5470.55

Total evaluation latency_ms: 9913.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | The study evaluates three ablated versions of LightRAG – **‑High** (high‑level retrieval removed), **‑Low** (low‑level retrieval removed) and **‑Origin** (original text removed) – by comparing each variant with the full LightRAG system (using NaiveRAG as the baseline for the win‑rate calculations).<br><br>*All win‑rate numbers are taken from Table 2 of the paper*[C8]. |
| ablation_meaning | judge | PASS | Required claim supported by verbatim evidence | **Ablation results for LightRAG**<br><br>The study evaluates three ablated versions of LightRAG – **‑High** (high‑level retrieval removed), **‑Low** (low‑level retrieval removed) and **‑Origin** (original text removed) – by comparing each variant with the full LightRAG system (using NaiveRAG as the baseline for the win‑rate calculations). |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer gives the -Low Overall win rate for Mix as 64.8% but does not provide the full LightRAG overall win rate of 60.0% nor explicitly compare them, so the required claim is not fully stated. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer provides the -Origin Overall win rate for Agriculture (74.4%) but does not give the full LightRAG Overall win rate (67.6%) nor state that 74.4% is higher, so the required comparison is missing. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 92 | 600 | 10000 | 701.42 | stop |
| 2 | answer | medium | 6453 | 6228 | 1221 | 3000 | 10000 | 3450.81 | stop |
| 3 | judge | low | 1793 | 1568 | 360 | 1000 | 10000 | 1495.67 | stop |
| 4 | judge | low | 1794 | 1569 | 261 | 1000 | 10000 | 876.77 | stop |
| 5 | judge | low | 1853 | 1628 | 253 | 1000 | 10000 | 986.25 | stop |
| 6 | judge | low | 1854 | 1629 | 249 | 1000 | 10000 | 1044.22 | stop |
| 7 | judge | low | 1781 | 1556 | 157 | 1000 | 10000 | 1067.64 | stop |

### Finalized answer

<pre>**Ablation results for LightRAG**

The study evaluates three ablated versions of LightRAG – **‑High** (high‑level retrieval removed), **‑Low** (low‑level retrieval removed) and **‑Origin** (original text removed) – by comparing each variant with the full LightRAG system (using NaiveRAG as the baseline for the win‑rate calculations).

| Variant | Metric | Agriculture (baseline / variant %) | CS (baseline / variant %) | Legal (baseline / variant %) | Mix (baseline / variant %) |
|---------|--------|-----------------------------------|--------------------------|------------------------------|----------------------------|
| **‑High** | Comprehensiveness | 34.8 / 65.2 | 42.8 / 57.2 | 23.6 / 76.4 | 40.4 / 59.6 |
|  | Diversity | 27.2 / 72.8 | 36.8 / 63.2 | 16.8 / 83.2 | 36.0 / 64.0 |
|  | Empowerment | 36.0 / 64.0 | 42.4 / 57.6 | 22.8 / 77.2 | 47.6 / 52.4 |
|  | Overall | 35.2 / 64.8 | 44.0 / 56.0 | 22.0 / 78.0 | 42.4 / 57.6 |
| **‑Low** | Comprehensiveness | 36.0 / 64.0 | 43.2 / 56.8 | 19.2 / 80.8 | 36.0 / 64.0 |
|  | Diversity | 28.0 / 72.0 | 39.6 / 60.4 | 13.6 / 86.4 | 33.2 / 66.8 |
|  | Empowerment | 34.8 / 65.2 | 42.8 / 57.2 | 16.4 / 83.6 | 35.2 / 64.8 |
|  | Overall | 34.8 / 65.2 | 43.6 / 56.4 | 18.8 / 81.2 | 35.2 / 64.8 |
| **‑Origin** | Comprehensiveness | 24.8 / 75.2 | 39.2 / 60.8 | 16.4 / 83.6 | 44.4 / 55.6 |
|  | Diversity | 26.4 / 73.6 | 44.8 / 55.2 | 14.4 / 85.6 | 25.6 / 74.4 |
|  | Empowerment | 32.0 / 68.0 | 43.2 / 56.8 | 17.2 / 82.8 | 45.2 / 54.8 |
|  | Overall | 25.6 / 74.4 | 39.2 / 60.8 | 15.6 / 84.4 | 44.4 / 55.6 |

*All win‑rate numbers are taken from Table 2 of the paper*[C8].

**Key observations**

* **‑High (high‑level retrieval removed)** – performance drops noticeably across almost all datasets and metrics compared with the full system, confirming that high‑order retrieval contributes substantially to LightRAG’s strength[C9].  
* **‑Low (low‑level retrieval removed)** – also leads to a significant decline, especially in diversity and empowerment, indicating that low‑level, entity‑focused retrieval is essential for detailed answers[C9].  
* **‑Origin (original text removed)** – does **not** cause a major degradation; in several cases (e.g., Agriculture and Mix) the variant even outperforms the full system, suggesting that the graph‑based index alone provides sufficient context and that raw text can introduce noise[C9].  

Overall, the ablation study demonstrates that the **dual‑level retrieval paradigm** (both low‑ and high‑level components) is crucial for achieving balanced, high‑quality performance, while the reliance on original text is comparatively less critical.</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Performance of ablated versions of LightRAG.

Sub-queries: []

Ask latency_ms: 6138.27

Judge latency_ms: 5946.20

Total evaluation latency_ms: 12105.69

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *All cells are “NaiveRAG win % / variant win %” as reported in Table 2 [C8].* |
| ablation_meaning | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | **‑High** (removes high‑level retrieval) ... **‑Low** (removes low‑level retrieval) ... **‑Origin** (removes original text from retrieval) ... Full LightRAG outperforms the ablated variants in most cases. |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer provides the -Low Overall win rate (64.8%) but does not state the full LightRAG overall win rate (60.0%) nor explicitly claim that 64.8% is higher than 60.0%. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer does not explicitly state that the -Origin Overall win rate on Agriculture is 74.4% and that this is higher than the full LightRAG&#x27;s 67.6%; it only provides the numbers separately and mentions higher win rates for other metrics, not the specific overall comparison. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 111 | 600 | 10000 | 822.20 | stop |
| 2 | answer | medium | 6453 | 6228 | 2034 | 3000 | 10000 | 5099.05 | stop |
| 3 | judge | low | 2373 | 2148 | 218 | 1000 | 10000 | 1148.56 | stop |
| 4 | judge | low | 2374 | 2149 | 232 | 1000 | 10000 | 941.62 | stop |
| 5 | judge | low | 2433 | 2208 | 276 | 1000 | 10000 | 1223.12 | stop |
| 6 | judge | low | 2434 | 2209 | 412 | 1000 | 10000 | 1636.25 | stop |
| 7 | judge | low | 2361 | 2136 | 154 | 1000 | 10000 | 996.67 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (Table 2)**  

| Variant | Metric | Agriculture | CS | Legal | Mix |
|--------|--------|-------------|----|-------|-----|
| **‑High** (removes high‑level retrieval) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (removes low‑level retrieval) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (removes original text from retrieval) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

*All cells are “NaiveRAG win % / variant win %” as reported in Table 2 [C8].*

### Observations

1. **Full LightRAG outperforms the ablated variants in most cases.**  
   - For the **‑High** and **‑Low** variants, the candidate win rates are consistently lower than those of the full LightRAG row (e.g., Agriculture Overall 64.8 % vs. LightRAG 67.6 %) [C8].  
   - This confirms the authors’ claim that removing either high‑level or low‑level retrieval “leads to a significant performance decline across nearly all datasets and metrics” [C9].

2. **‑High vs. ‑Low trade‑offs.**  
   - **‑High** (high‑level removed) shows relatively higher win rates on **Comprehensiveness** for Agriculture (65.2 %) but lower on **Diversity** and **Empowerment** compared with **‑Low** (e.g., Agriculture Diversity 72.8 % vs. 72.0 %).  
   - The qualitative description notes that **‑High** “focuses excessively on entities and their immediate neighbors, struggling with complex queries” [C9], while **‑Low** “captures a broader range of content but may lack depth for detailed answers” [C9].

3. **‑Origin (no original text) is competitive and sometimes superior.**  
   - In **Agriculture**, **‑Origin** achieves higher win rates than full LightRAG for **Comprehensiveness** (75.2 % vs 67.6 %) and **Diversity** (73.6 % vs 76.4 % – slightly lower) [C8].  
   - For **Mix**, **‑Origin** is lower (Overall 55.6 % vs 60.0 %).  
   - The paper remarks that “the variant even shows improvements (e.g., in Agriculture and Mix)” and that “the original text often contains irrelevant information that can introduce noise” [C9].

4. **Overall trend across datasets.**  
   - Across **Legal** and **CS**, the full LightRAG consistently has the highest candidate win rates (e.g., Legal Overall 84.8 % vs. ‑High 78.0 % and ‑Low 81.2 %) [C8].  
   - This aligns with the authors’ statement that “LightRAG shows a clear advantage, significantly surpassing GraphRAG and highlighting its strength in comprehensive information understanding” [C6], implying that the full dual‑level design is most effective on larger, complex corpora.

### Summary

Ablation studies demonstrate that **both low‑level and high‑level retrieval components are essential** for LightRAG’s best performance; removing either leads to noticeable drops in win rates across most metrics and datasets. The **‑Origin** ablation, which eliminates the use of raw text, retains most of the system’s strength and can even improve results on certain datasets, suggesting that the graph‑based indexing captures sufficient context while reducing noise. [C9][C8]</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Synthesis; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: [&#x27;LightRAG ablation study results&#x27;, &#x27;performance metrics of LightRAG variants&#x27;, &#x27;comparison of LightRAG ablated models&#x27;]

Ask latency_ms: 5466.02

Judge latency_ms: 7424.90

Total evaluation latency_ms: 12899.21

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C6 |
| question_type | events | FAIL | Expected Lookup; actual Synthesis; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *All numbers are the **variant win rates** (the second value in each “baseline / variant” pair) reported in Table 2 of the paper*[C6]. |
| ablation_meaning | judge | FAIL | Required claim not asserted: The answer describes -High and -Low as removing high‑level and low‑level retrieval respectively, matching part of the claim, but states -Origin removes graph‑based indexing, not original text as the claim asserts. It also does not explicitly state that the full LightRAG combines both retrieval levels. Therefore the claim is not fully asserted. |  |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer lists the -Low Overall win rate for Mix as 64.8% and mentions the full LightRAG overall win rate as 60.0%, but it does not explicitly state that the -Low value is higher than the full LightRAG value, so the claim is not asserted. |  |
| agriculture_origin_overall | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Overall \| 74.4 \| 60.8 \| 84.4 \| 55.6<br><br>Across all four datasets, the full LightRAG system (baseline / LightRAG) achieves higher win rates than any ablated version (e.g., Agriculture Overall: 67.6 % vs. 64.8 % for ‑High, 65.2 % for ‑Low, 74.4 % for ‑Origin)[C6]. |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 128 | 600 | 10000 | 837.36 | stop |
| 2 | answer | medium | 4509 | 4284 | 1189 | 3000 | 10000 | 4113.72 | stop |
| 3 | judge | low | 1601 | 1376 | 327 | 1000 | 10000 | 1310.47 | stop |
| 4 | judge | low | 1602 | 1377 | 254 | 1000 | 10000 | 1183.98 | stop |
| 5 | judge | low | 1661 | 1436 | 417 | 1000 | 10000 | 1892.11 | stop |
| 6 | judge | low | 1662 | 1437 | 482 | 1000 | 10000 | 1733.58 | stop |
| 7 | judge | low | 1589 | 1364 | 226 | 1000 | 10000 | 1304.77 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (performance measured as “baseline (NaiveRAG) win % / variant win %”)**

| Variant (removed component) | Metric | Agriculture % | CS % | Legal % | Mix % |
|---|---|---|---|---|---|
| **‑High** (no high‑level retrieval) | Comprehensiveness | 65.2 | 57.2 | 76.4 | 59.6 |
|  | Diversity | 72.8 | 63.2 | 83.2 | 64.0 |
|  | Empowerment | 64.0 | 57.6 | 77.2 | 52.4 |
|  | Overall | 64.8 | 56.0 | 78.0 | 57.6 |
| **‑Low** (no low‑level retrieval) | Comprehensiveness | 64.0 | 56.8 | 80.8 | 64.0 |
|  | Diversity | 72.0 | 60.4 | 86.4 | 66.8 |
|  | Empowerment | 65.2 | 57.2 | 83.6 | 64.8 |
|  | Overall | 65.2 | 56.4 | 81.2 | 64.8 |
| **‑Origin** (no graph‑based indexing) | Comprehensiveness | 75.2 | 60.8 | 83.6 | 55.6 |
|  | Diversity | 73.6 | 55.2 | 85.6 | 74.4 |
|  | Empowerment | 68.0 | 56.8 | 82.8 | 54.8 |
|  | Overall | 74.4 | 60.8 | 84.4 | 55.6 |

*All numbers are the **variant win rates** (the second value in each “baseline / variant” pair) reported in Table 2 of the paper*[C6].

**Key observations**

- Across all four datasets, the full LightRAG system (baseline / LightRAG) achieves higher win rates than any ablated version (e.g., Agriculture Overall: 67.6 % vs. 64.8 % for ‑High, 65.2 % for ‑Low, 74.4 % for ‑Origin)[C6].  
- Removing the high‑level retrieval module (‑High) reduces performance relative to the full system, especially on Diversity (72.8 % vs. 76.4 % on Agriculture) and Overall (64.8 % vs. 67.6 % on Agriculture)[C6].  
- Removing the low‑level retrieval module (‑Low) shows a similar drop, with the largest gap on Diversity for the Legal dataset (86.4 % vs. 86.4 % for full LightRAG, i.e., no drop) but lower scores on other metrics and datasets[C6].  
- The most drastic degradation occurs when the graph‑based indexing component is omitted (‑Origin); win rates fall markedly on the Mix dataset (e.g., Overall 55.6 % vs. 60.0 % for full LightRAG) and on Diversity for the CS dataset (73.6 % vs. 67.6 % for full LightRAG)[C6].  

These results demonstrate that each component—high‑level retrieval, low‑level retrieval, and graph‑based indexing—contributes positively to LightRAG’s overall performance.</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 1778.77

Judge latency_ms: 0.00

Total evaluation latency_ms: 1814.46

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 92 | 600 | 10000 | 749.80 | stop |
| 2 | answer | medium | 6596 | 6371 | 106 | 3000 | 10000 | 825.22 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_HOTPOT — repetition 2

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 1919.48

Judge latency_ms: 0.00

Total evaluation latency_ms: 1924.58

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 108 | 600 | 10000 | 796.32 | stop |
| 2 | answer | medium | 6596 | 6371 | 111 | 3000 | 10000 | 766.49 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_HOTPOT — repetition 3

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 1805.40

Judge latency_ms: 0.00

Total evaluation latency_ms: 1819.17

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 108 | 600 | 10000 | 731.49 | stop |
| 2 | answer | medium | 6596 | 6371 | 110 | 3000 | 10000 | 779.89 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 1794.48

Judge latency_ms: 0.00

Total evaluation latency_ms: 1794.70

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 75 | 600 | 10000 | 663.42 | stop |
| 2 | answer | medium | 6617 | 6392 | 120 | 3000 | 10000 | 894.44 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_LICENSE — repetition 2

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 1695.39

Judge latency_ms: 0.00

Total evaluation latency_ms: 1695.52

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 83 | 600 | 10000 | 673.21 | stop |
| 2 | answer | medium | 6617 | 6392 | 129 | 3000 | 10000 | 810.63 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_LICENSE — repetition 3

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Ask latency_ms: 1710.36

Judge latency_ms: 0.00

Total evaluation latency_ms: 1710.61

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 75 | 600 | 10000 | 668.56 | stop |
| 2 | answer | medium | 6617 | 6392 | 120 | 3000 | 10000 | 818.22 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 1738.27

Judge latency_ms: 0.00

Total evaluation latency_ms: 1749.22

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 96 | 600 | 10000 | 654.00 | stop |
| 2 | answer | medium | 5817 | 5592 | 135 | 3000 | 10000 | 886.03 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_GPU — repetition 2

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 1952.38

Judge latency_ms: 0.00

Total evaluation latency_ms: 1966.36

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 113 | 600 | 10000 | 943.33 | stop |
| 2 | answer | medium | 5817 | 5592 | 124 | 3000 | 10000 | 764.25 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_GPU — repetition 3

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 的訓練使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 1691.81

Judge latency_ms: 0.00

Total evaluation latency_ms: 1701.94

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 111 | 600 | 10000 | 695.65 | stop |
| 2 | answer | medium | 5834 | 5609 | 123 | 3000 | 10000 | 822.32 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## Q1_ZH_THREE_SENTENCES — repetition 1

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 3076.33

Judge latency_ms: 12593.57

Total evaluation latency_ms: 15715.64

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，並採用低階與高階兩層檢索機制，同時支援精確的實體‑屬性查詢與廣義主題檢索，以克服傳統 RAG 系統的平面表示與上下文碎片化問題 [S1][S5]。 |
| graph_indexing | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，... |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，並採用低階與高階兩層檢索機制，同時支援精確的實體‑屬性查詢與廣義主題檢索，以克服傳統 RAG 系統的平面表示與上下文碎片化問題 [S1][S5]。 |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 此系統具備增量更新模組，能在不重新建構整體圖的情況下將新文件的實體與關係合併至既有圖中，顯著降低索引與檢索階段的 token 數量與 API 呼叫次數，較 GraphRAG 有明顯效能優勢 [S4][S13]。 |
| experiments | judge | FAIL | Required claim not asserted: The answer does not mention Section 4, nor specify the Agriculture, CS, Legal, and Mix domains, nor explicitly claim a comparison showing stronger answer quality and diversity, so the claim is not satisfied. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | 較 GraphRAG 有明顯效能優勢 [S4][S13]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在檢索準確度、回應多樣性以及成本效益上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 等基線方法，並提升了生成品質與效率 [S10][S13][S16]。 |
| conclusion | judge | FAIL | Required claim not asserted: The answer does not explicitly state the claim about Section 6 concluding that it combines effective, efficient graph-based retrieval with adaptability; it only describes LightRAG features without referencing a conclusion section. |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，並採用低階與高階兩層檢索機制，同時支援精確的實體‑屬性查詢與廣義主題檢索，以克服傳統 RAG 系統的平面表示與上下文碎片化問題 [S1][S5]。  <br>此系統具備增量更新模組，能在不重新建構整體圖的情況下將新文件的實體與關係合併至既有圖中，顯著降低索引與檢索階段的 token 數量與 API 呼叫次數，較 GraphRAG 有明顯效能優勢 [S4][S13]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在檢索準確度、回應多樣性以及成本效益上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 等基線方法，並提升了生成品質與效率 [S10][S13][S16] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，並採用低階與高階兩層檢索機制，同時支援精確的實體‑屬性查詢與廣義主題檢索，以克服傳統 RAG 系統的平面表示與上下文碎片化問題 [S1][S5]。  <br>此系統具備增量更新模組，能在不重新建構整體圖的情況下將新文件的實體與關係合併至既有圖中，顯著降低索引與檢索階段的 token 數量與 API 呼叫次數，較 GraphRAG 有明顯效能優勢 [S4][S13]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在檢索準確度、回應多樣性以及成本效益上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 等基線方法，並提升了生成品質與效率 [S10][S13][S16]。 |
| answer_script | property | FAIL | Question script=Traditional; opposing script forms found | LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，並採用低階與高階兩層檢索機制，同時支援精確的實體‑屬性查詢與廣義主題檢索，以克服傳統 RAG 系統的平面表示與上下文碎片化問題 [S1][S5]。  <br>此系統具備增量更新模組，能在不重新建構整體圖的情況下將新文件的實體與關係合併至既有圖中，顯著降低索引與檢索階段的 token 數量與 API 呼叫次數，較 GraphRAG 有明顯效能優勢 [S4][S13]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在檢索準確度、回應多樣性以及成本效益上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 等基線方法，並提升了生成品質與效率 [S10][S13][S16]。 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 91 | 600 | 10000 | 753.05 | stop |
| 2 | answer | medium | 5818 | 5593 | 579 | 3000 | 10000 | 2312.66 | stop |
| 3 | judge | low | 1045 | 820 | 269 | 1000 | 10000 | 1043.47 | stop |
| 4 | judge | low | 1040 | 815 | 176 | 1000 | 10000 | 916.85 | stop |
| 5 | judge | low | 1042 | 817 | 309 | 1000 | 10000 | 1326.44 | stop |
| 6 | judge | low | 1048 | 823 | 219 | 1000 | 10000 | 1031.35 | stop |
| 7 | judge | low | 1051 | 826 | 189 | 1000 | 10000 | 1206.99 | stop |
| 8 | judge | low | 1048 | 823 | 185 | 1000 | 10000 | 1017.93 | stop |
| 9 | judge | low | 1055 | 830 | 313 | 1000 | 10000 | 1454.93 | stop |
| 10 | judge | low | 1041 | 816 | 160 | 1000 | 10000 | 968.32 | stop |
| 11 | judge | low | 1042 | 817 | 507 | 1000 | 10000 | 1732.39 | stop |
| 12 | judge | low | 1051 | 826 | 523 | 1000 | 10000 | 1894.89 | stop |

### Finalized answer

<pre>LightRAG 透過將文件切塊後以 LLM 提取實體與關係，建構圖形化的知識索引，並採用低階與高階兩層檢索機制，同時支援精確的實體‑屬性查詢與廣義主題檢索，以克服傳統 RAG 系統的平面表示與上下文碎片化問題 [S1][S5]。  
此系統具備增量更新模組，能在不重新建構整體圖的情況下將新文件的實體與關係合併至既有圖中，顯著降低索引與檢索階段的 token 數量與 API 呼叫次數，較 GraphRAG 有明顯效能優勢 [S4][S13]。  
在四個大規模領域資料集上的實驗顯示，LightRAG 在檢索準確度、回應多樣性以及成本效益上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 等基線方法，並提升了生成品質與效率 [S10][S13][S16]。</pre>

## Q1_ZH_THREE_SENTENCES — repetition 2

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 3638.71

Judge latency_ms: 13867.37

Total evaluation latency_ms: 17552.23

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted: The answer never states that flat RAG loses contextual interdependencies; it only describes LightRAG&#x27;s mechanisms and performance, so the required claim is missing. |  |
| graph_indexing | judge | FAIL | Required claim not asserted: The answer describes graph-based indexing capturing entity dependencies, but does not explicitly state that it extracts entities and relationships as required by the claim. |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過圖形化文字索引結合低階（具體）與高階（抽象）雙層檢索機制，能捕捉實體間的相依關係並提供更完整的資訊檢索。 |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 其增量更新模組可在不重新建構索引的情況下整合新資料，顯著降低 token 與 API 呼叫成本。 |
| experiments | judge | FAIL | Required claim not asserted: The answer does not mention evaluation on Agriculture, CS, or Mix domains nor reference Section 4; it only refers to four large-scale domains including Legal, so the required claim is not stated. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted: The answer describes LightRAG&#x27;s effective, efficient graph-based retrieval and adaptability, but does not state that Section 6&#x27;s conclusion combines these aspects, nor does it reference Section 6. |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過圖形化文字索引結合低階（具體）與高階（抽象）雙層檢索機制，能捕捉實體間的相依關係並提供更完整的資訊檢索。[S1][S5]  <br>在四個大規模領域資料集（含 Legal）上，LightRAG 的勝率在準確度、回應多樣性與效率上皆優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且其增量更新模組可在不重新建構索引的情況下整合新資料，顯著降低 token 與 API 呼叫成本。[S10][S13]  <br>作者因此宣稱 LightRAG 在提升檢索效率與生成品質的同時，顯著降低大型語言模型的推論成本，成為處理複雜查詢的可擴展且具適應性的解決方案。[S16] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過圖形化文字索引結合低階（具體）與高階（抽象）雙層檢索機制，能捕捉實體間的相依關係並提供更完整的資訊檢索。[S1][S5]  <br>在四個大規模領域資料集（含 Legal）上，LightRAG 的勝率在準確度、回應多樣性與效率上皆優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且其增量更新模組可在不重新建構索引的情況下整合新資料，顯著降低 token 與 API 呼叫成本。[S10][S13]  <br>作者因此宣稱 LightRAG 在提升檢索效率與生成品質的同時，顯著降低大型語言模型的推論成本，成為處理複雜查詢的可擴展且具適應性的解決方案。[S16] |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | LightRAG 透過圖形化文字索引結合低階（具體）與高階（抽象）雙層檢索機制，能捕捉實體間的相依關係並提供更完整的資訊檢索。[S1][S5]  <br>在四個大規模領域資料集（含 Legal）上，LightRAG 的勝率在準確度、回應多樣性與效率上皆優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且其增量更新模組可在不重新建構索引的情況下整合新資料，顯著降低 token 與 API 呼叫成本。[S10][S13]  <br>作者因此宣稱 LightRAG 在提升檢索效率與生成品質的同時，顯著降低大型語言模型的推論成本，成為處理複雜查詢的可擴展且具適應性的解決方案。[S16] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 93 | 600 | 10000 | 726.59 | stop |
| 2 | answer | medium | 5818 | 5593 | 519 | 3000 | 10000 | 2889.37 | stop |
| 3 | judge | low | 999 | 774 | 121 | 1000 | 10000 | 1139.54 | stop |
| 4 | judge | low | 994 | 769 | 211 | 1000 | 10000 | 1283.45 | stop |
| 5 | judge | low | 996 | 771 | 238 | 1000 | 10000 | 1165.45 | stop |
| 6 | judge | low | 1002 | 777 | 185 | 1000 | 10000 | 979.33 | stop |
| 7 | judge | low | 1005 | 780 | 189 | 1000 | 10000 | 1161.36 | stop |
| 8 | judge | low | 1002 | 777 | 159 | 1000 | 10000 | 1080.86 | stop |
| 9 | judge | low | 1009 | 784 | 263 | 1000 | 10000 | 1448.26 | stop |
| 10 | judge | low | 995 | 770 | 198 | 1000 | 10000 | 1331.95 | stop |
| 11 | judge | low | 996 | 771 | 491 | 1000 | 10000 | 2150.87 | stop |
| 12 | judge | low | 1005 | 780 | 422 | 1000 | 10000 | 2126.30 | stop |

### Finalized answer

<pre>LightRAG 透過圖形化文字索引結合低階（具體）與高階（抽象）雙層檢索機制，能捕捉實體間的相依關係並提供更完整的資訊檢索。[S1][S5]  
在四個大規模領域資料集（含 Legal）上，LightRAG 的勝率在準確度、回應多樣性與效率上皆優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，且其增量更新模組可在不重新建構索引的情況下整合新資料，顯著降低 token 與 API 呼叫成本。[S10][S13]  
作者因此宣稱 LightRAG 在提升檢索效率與生成品質的同時，顯著降低大型語言模型的推論成本，成為處理複雜查詢的可擴展且具適應性的解決方案。[S16]</pre>

## Q1_ZH_THREE_SENTENCES — repetition 3

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 4964.29

Judge latency_ms: 11503.95

Total evaluation latency_ms: 16513.08

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将图结构与向量嵌入相结合的图‑基文本索引和双层检索框架，克服了传统 RAG 的平面表示限制并提升了上下文感知能力，同时支持增量更新以快速整合新数据。 |
| graph_indexing | judge | FAIL | Required claim not asserted: The answer does not state that Section 3.1&#x27;s graph-based indexing extracts entities and relationships; it discusses LightRAG&#x27;s graph‑based text indexing but does not mention Section 3.1 or extraction of entities and relationships. |  |
| dual_level | judge | FAIL | Required claim not asserted: The answer mentions a dual-layer retrieval framework but does not state that it combines specific entities and broader topics as required by the claim. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer states that LightRAG supports incremental updates to quickly integrate new data, but it does not explicitly claim that these updates occur without rebuilding the entire index, which is required by the claim. |  |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在农业、计算机科学、法律和混合四个大规模领域数据集上的实验表明，LightRAG 在检索准确率、响应多样性和整体生成质量上均优于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG，尤其在规模最大的法律数据集上胜率约为 80%，且在检索和增量更新阶段显著降低了使用的 token 数和 API 调用次数。 |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | 在农业、计算机科学、法律和混合四个大规模领域数据集上的实验表明，LightRAG 在检索准确率、响应多样性和整体生成质量上均优于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG，尤其在规模最大的法律数据集上胜率约为 80%，且在检索和增量更新阶段显著降低了使用的 token 数和 API 调用次数。 |
| conclusion | judge | FAIL | Required claim not asserted: The answer does not reference Section 6 or state that the conclusion combines effective, efficient graph-based retrieval with adaptability; it merely summarizes findings without mentioning the specific section. |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将图结构与向量嵌入相结合的图‑基文本索引和双层检索框架，克服了传统 RAG 的平面表示限制并提升了上下文感知能力，同时支持增量更新以快速整合新数据。[S1][S4][S5]  <br><br>在农业、计算机科学、法律和混合四个大规模领域数据集上的实验表明，LightRAG 在检索准确率、响应多样性和整体生成质量上均优于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG，尤其在规模最大的法律数据集上胜率约为 80%，且在检索和增量更新阶段显著降低了使用的 token 数和 API 调用次数。[S10][S13][S9]  <br><br>作者因此认为，图‑增强的索引、双层检索以及无缝的增量更新使 LightRAG 在检索‑增强生成的效率和效果上都有显著提升，并显著降低了大模型的推理成本。[S16][S7][S13] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 通过将图结构与向量嵌入相结合的图‑基文本索引和双层检索框架，克服了传统 RAG 的平面表示限制并提升了上下文感知能力，同时支持增量更新以快速整合新数据。[S1][S4][S5]  <br><br>在农业、计算机科学、法律和混合四个大规模领域数据集上的实验表明，LightRAG 在检索准确率、响应多样性和整体生成质量上均优于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG，尤其在规模最大的法律数据集上胜率约为 80%，且在检索和增量更新阶段显著降低了使用的 token 数和 API 调用次数。[S10][S13][S9]  <br><br>作者因此认为，图‑增强的索引、双层检索以及无缝的增量更新使 LightRAG 在检索‑增强生成的效率和效果上都有显著提升，并显著降低了大模型的推理成本。[S16][S7][S13] |
| answer_script | property | FAIL | Question script=Traditional; opposing script forms found | LightRAG 通过将图结构与向量嵌入相结合的图‑基文本索引和双层检索框架，克服了传统 RAG 的平面表示限制并提升了上下文感知能力，同时支持增量更新以快速整合新数据。[S1][S4][S5]  <br><br>在农业、计算机科学、法律和混合四个大规模领域数据集上的实验表明，LightRAG 在检索准确率、响应多样性和整体生成质量上均优于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG，尤其在规模最大的法律数据集上胜率约为 80%，且在检索和增量更新阶段显著降低了使用的 token 数和 API 调用次数。[S10][S13][S9]  <br><br>作者因此认为，图‑增强的索引、双层检索以及无缝的增量更新使 LightRAG 在检索‑增强生成的效率和效果上都有显著提升，并显著降低了大模型的推理成本。[S16][S7][S13] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 92 | 600 | 10000 | 692.16 | stop |
| 2 | answer | medium | 5818 | 5593 | 1142 | 3000 | 10000 | 4258.09 | stop |
| 3 | judge | low | 1022 | 797 | 268 | 1000 | 10000 | 1209.16 | stop |
| 4 | judge | low | 1017 | 792 | 125 | 1000 | 10000 | 803.28 | stop |
| 5 | judge | low | 1019 | 794 | 128 | 1000 | 10000 | 761.02 | stop |
| 6 | judge | low | 1025 | 800 | 250 | 1000 | 10000 | 1168.45 | stop |
| 7 | judge | low | 1028 | 803 | 254 | 1000 | 10000 | 1094.01 | stop |
| 8 | judge | low | 1025 | 800 | 165 | 1000 | 10000 | 1005.99 | stop |
| 9 | judge | low | 1032 | 807 | 288 | 1000 | 10000 | 1237.74 | stop |
| 10 | judge | low | 1018 | 793 | 141 | 1000 | 10000 | 875.47 | stop |
| 11 | judge | low | 1019 | 794 | 441 | 1000 | 10000 | 1446.07 | stop |
| 12 | judge | low | 1028 | 803 | 469 | 1000 | 10000 | 1902.74 | stop |

### Finalized answer

<pre>LightRAG 通过将图结构与向量嵌入相结合的图‑基文本索引和双层检索框架，克服了传统 RAG 的平面表示限制并提升了上下文感知能力，同时支持增量更新以快速整合新数据。[S1][S4][S5]  

在农业、计算机科学、法律和混合四个大规模领域数据集上的实验表明，LightRAG 在检索准确率、响应多样性和整体生成质量上均优于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG，尤其在规模最大的法律数据集上胜率约为 80%，且在检索和增量更新阶段显著降低了使用的 token 数和 API 调用次数。[S10][S13][S9]  

作者因此认为，图‑增强的索引、双层检索以及无缝的增量更新使 LightRAG 在检索‑增强生成的效率和效果上都有显著提升，并显著降低了大模型的推理成本。[S16][S7][S13]</pre>
