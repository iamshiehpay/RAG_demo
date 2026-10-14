# Golden Facts evaluation

Created: 2026-10-13T12:12:10.480804+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 3

Result: FAIL

Functional operations: PASS (separate from D05 semantic rates)

Call audit: {&quot;budget_violations&quot;: 0, &quot;calls&quot;: 170, &quot;length_attempts&quot;: [], &quot;maximum_estimated_prompt_plus_reservation&quot;: 9667, &quot;maximum_reported_prompt_plus_reservation&quot;: 9442, &quot;missing_reported_prompt_counts&quot;: 0, &quot;router_answer_length_attempts&quot;: 0}

Router classification requires plan_source=router. Fallback plans fail with status FALLBACK, even when their Question Type matches. Follow-up checks require a changed Standalone Question resolving the case referents; language-mismatch rewrites fail. Accepting a history argument is not a pass condition.

Revision: 0c320a8c24ae4917a2fe56db55ae2651c5ad76da

Uncommitted changes: yes

Pipeline version: ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Created: 2026-10-13T12:12:10.479665+00:00

Label: issue11-final-lightrag

D05: Report raw rates/causes; semantic defects do not block delivery.

Effective settings: {&quot;answer_think&quot;: &quot;medium&quot;, &quot;bm25_weight&quot;: 0.0, &quot;chunk_token_target&quot;: 500, &quot;lookup_top_k&quot;: 5, &quot;sub_query_top_k&quot;: 2, &quot;summary_concurrency&quot;: 4, &quot;synthesis_top_k&quot;: 3}

Peak guarded calls by type: {&quot;section_summary&quot;: 4, &quot;group_summary&quot;: 1, &quot;document_summary&quot;: 1, &quot;router&quot;: 1, &quot;answer&quot;: 1, &quot;judge&quot;: 1}

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| Q1 | question_type | events | 3/3 (100.0%) |
| Q1 | motivation | judge | 3/3 (100.0%) |
| Q1 | graph_indexing | judge | 3/3 (100.0%) |
| Q1 | dual_level | judge | 3/3 (100.0%) |
| Q1 | incremental_update | judge | 0/3 (0.0%) |
| Q1 | experiments | judge | 3/3 (100.0%) |
| Q1 | not_all_best | forbidden | 0/3 (0.0%) |
| Q1 | not_all_datasets | forbidden | 2/3 (66.7%) |
| Q1 | conclusion | judge | 2/3 (66.7%) |
| Q2 | question_type | events | 3/3 (100.0%) |
| Q2 | retrieval_methods | judge | 0/3 (0.0%) |
| Q2 | retrieval_cost | judge | 0/3 (0.0%) |
| Q2 | incremental_update | judge | 0/3 (0.0%) |
| Q2 | table1_agriculture_overall | judge | 0/3 (0.0%) |
| Q2 | table1_cs_overall | judge | 0/3 (0.0%) |
| Q2 | table1_legal_overall | judge | 0/3 (0.0%) |
| Q2 | table1_mix_overall | judge | 0/3 (0.0%) |
| Q2 | table3_case_study | judge | 1/3 (33.3%) |
| Q2 | not_all_datasets | forbidden | 3/3 (100.0%) |
| Q3 | required_source_citation | events | 3/3 (100.0%) |
| Q3 | question_type | events | 2/3 (66.7%) |
| Q3 | high_term | contains | 3/3 (100.0%) |
| Q3 | low_term | contains | 3/3 (100.0%) |
| Q3 | origin_term | contains | 3/3 (100.0%) |
| Q3 | table2_baseline | judge | 2/3 (66.7%) |
| Q3 | ablation_meaning | judge | 0/3 (0.0%) |
| Q3 | mix_low_overall | judge | 0/3 (0.0%) |
| Q3 | agriculture_origin_overall | judge | 0/3 (0.0%) |
| Q3 | not_all_best | forbidden | 1/3 (33.3%) |
| ABSENT_HOTPOT | question_type | events | 3/3 (100.0%) |
| ABSENT_HOTPOT | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_HOTPOT | answer_script | property | 3/3 (100.0%) |
| ABSENT_LICENSE | question_type | events | 3/3 (100.0%) |
| ABSENT_LICENSE | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_GPU | question_type | events | 3/3 (100.0%) |
| ABSENT_GPU | fixed_reply | judge | 3/3 (100.0%) |
| ABSENT_GPU | answer_script | property | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | question_type | events | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | motivation | judge | 0/3 (0.0%) |
| Q1_ZH_THREE_SENTENCES | graph_indexing | judge | 1/3 (33.3%) |
| Q1_ZH_THREE_SENTENCES | dual_level | judge | 2/3 (66.7%) |
| Q1_ZH_THREE_SENTENCES | incremental_update | judge | 2/3 (66.7%) |
| Q1_ZH_THREE_SENTENCES | experiments | judge | 2/3 (66.7%) |
| Q1_ZH_THREE_SENTENCES | not_all_best | forbidden | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | not_all_datasets | forbidden | 0/3 (0.0%) |
| Q1_ZH_THREE_SENTENCES | conclusion | judge | 0/3 (0.0%) |
| Q1_ZH_THREE_SENTENCES | chinese_summary | judge | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | three_sentences | judge | 3/3 (100.0%) |
| Q1_ZH_THREE_SENTENCES | answer_script | property | 3/3 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | section_summary | low | 882 | 657 | 106 | 1200 | 10000 | 1211.58 | stop |
| 2 | section_summary | low | 1674 | 1449 | 202 | 1200 | 10000 | 1476.39 | stop |
| 3 | section_summary | low | 1145 | 920 | 258 | 1200 | 10000 | 1741.47 | stop |
| 4 | section_summary | low | 1593 | 1368 | 231 | 1200 | 10000 | 1898.40 | stop |
| 5 | section_summary | low | 1183 | 958 | 161 | 1200 | 10000 | 955.23 | stop |
| 6 | section_summary | low | 802 | 577 | 111 | 1200 | 10000 | 758.72 | stop |
| 7 | section_summary | low | 878 | 653 | 125 | 1200 | 10000 | 802.51 | stop |
| 8 | section_summary | low | 756 | 531 | 123 | 1200 | 10000 | 1490.34 | stop |
| 9 | section_summary | low | 1743 | 1518 | 270 | 1200 | 10000 | 1991.56 | stop |
| 10 | section_summary | low | 4419 | 4152 | 197 | 1200 | 10000 | 1458.70 | stop |
| 11 | section_summary | low | 3433 | 3166 | 302 | 1200 | 10000 | 2607.62 | stop |
| 12 | section_summary | low | 3457 | 3190 | 451 | 1200 | 10000 | 2977.04 | stop |
| 13 | section_summary | low | 1258 | 1033 | 191 | 1200 | 10000 | 1206.91 | stop |
| 14 | section_summary | low | 785 | 560 | 155 | 1200 | 10000 | 1166.02 | stop |
| 15 | section_summary | low | 935 | 710 | 116 | 1200 | 10000 | 1562.54 | stop |
| 16 | section_summary | low | 737 | 512 | 159 | 1200 | 10000 | 1245.64 | stop |
| 17 | section_summary | low | 900 | 675 | 265 | 1200 | 10000 | 1898.46 | stop |
| 18 | section_summary | low | 802 | 577 | 107 | 1200 | 10000 | 808.30 | stop |
| 19 | section_summary | low | 814 | 589 | 199 | 1200 | 10000 | 1234.93 | stop |
| 20 | section_summary | low | 776 | 551 | 205 | 1200 | 10000 | 1910.18 | stop |
| 21 | section_summary | low | 752 | 527 | 90 | 1200 | 10000 | 1470.82 | stop |
| 22 | section_summary | low | 879 | 654 | 138 | 1200 | 10000 | 1597.81 | stop |
| 23 | section_summary | low | 766 | 541 | 156 | 1200 | 10000 | 1122.08 | stop |
| 24 | section_summary | low | 741 | 516 | 96 | 1200 | 10000 | 816.25 | stop |
| 25 | section_summary | low | 829 | 604 | 211 | 1200 | 10000 | 1309.01 | stop |
| 26 | section_summary | low | 818 | 593 | 161 | 1200 | 10000 | 1143.43 | stop |
| 27 | section_summary | low | 843 | 618 | 221 | 1200 | 10000 | 1383.40 | stop |
| 28 | section_summary | low | 832 | 607 | 130 | 1200 | 10000 | 1553.20 | stop |
| 29 | section_summary | low | 3934 | 3667 | 682 | 1200 | 10000 | 2969.82 | stop |
| 30 | section_summary | low | 3974 | 3707 | 333 | 1200 | 10000 | 2199.69 | stop |
| 31 | group_summary | low | 5313 | 5088 | 1534 | 2500 | 10000 | 5803.90 | stop |
| 32 | document_summary | low | 2516 | 2291 | 1507 | 2500 | 10000 | 3457.20 | stop |

## Q1 — repetition 1

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 5686.83

Judge latency_ms: 10591.39

Total evaluation latency_ms: 16356.41

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | The authors observe that many RAG systems rely on flat, chunk‑based indexes, which leads to fragmented answers for queries that involve inter‑dependent entities, and they propose using graph structures to capture entity relationships and support coherent synthesis; LightRAG therefore combines graph‑enhanced indexing with low‑level (entity‑specific) and high‑level (topic‑wide) retrieval to provide comprehensive, cost‑effective access to knowledge and to enable rapid incremental updates[S2]. |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | In the indexing stage, documents are split into chunks, LLM prompts extract entities (names, dates, locations, events) and their relations, and these are stored as a knowledge graph where each entity node holds a key‑value pair (entity name → summarizing paragraph) and edges carry thematic keys; new documents are processed similarly and merged with the existing graph without rebuilding the whole index[S4]. |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | The dual‑level retrieval paradigm generates both detailed and abstract query keys: specific keys drive low‑level retrieval of precise entities or edges, while abstract keys drive high‑level retrieval of broader topics; |
| incremental_update | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | new documents are processed similarly and merged with the existing graph without rebuilding the whole index[S4].<br>...for incremental updates, LightRAG integrates new entities without rebuilding the graph, incurring far lower overhead than GraphRAG’s costly community reconstruction[S13]. |
| experiments | judge | PASS | Required claim supported by verbatim evidence | The evaluation uses four “UltraDomain” corpora (Agriculture, CS, Legal, Mixed) ranging from 2 M to over 5 M tokens per dataset[S9][S18], and compares LightRAG against NaiveRAG, RQ‑RAG, HyDE and GraphRAG.  Across all datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates; the advantage grows with dataset size, e.g., on the largest Legal set baseline methods win only about 20 % versus LightRAG’s dominance, and LightRAG shows a particularly strong lead on the Diversity metric[S10]. |
| not_all_best | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | Across all datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates; the advantage grows with dataset size, e.g., on the largest Legal set baseline methods win only about 20 % versus LightRAG’s dominance, and LightRAG shows a particularly strong lead on the Diversity metric. |
| not_all_datasets | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | Across all datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates; the advantage grows with dataset size, e.g., on the largest Legal set baseline methods win only about 20 % versus LightRAG’s dominance, and LightRAG shows a particularly strong lead on the Diversity metric[S10].<br>Case‑study comparisons (e.g., a machine‑learning metric normalization query) show LightRAG outperforming GraphRAG on all judged dimensions, |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | Overall, the authors conclude that LightRAG’s graph‑based indexing, dual‑level retrieval and incremental update mechanism substantially boost retrieval speed and generation quality while lowering LLM inference costs, thereby improving efficiency and comprehension in RAG systems[S16]. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 86 | 600 | 10000 | 790.80 | stop |
| 2 | answer | medium | 5590 | 5365 | 1128 | 3000 | 10000 | 4884.79 | stop |
| 3 | judge | low | 1631 | 1406 | 252 | 1000 | 10000 | 1213.88 | stop |
| 4 | judge | low | 1626 | 1401 | 318 | 1000 | 10000 | 1574.85 | stop |
| 5 | judge | low | 1628 | 1403 | 196 | 1000 | 10000 | 931.90 | stop |
| 6 | judge | low | 1634 | 1409 | 216 | 1000 | 10000 | 883.79 | stop |
| 7 | judge | low | 1637 | 1412 | 352 | 1000 | 10000 | 1224.85 | stop |
| 8 | judge | low | 1634 | 1409 | 330 | 1000 | 10000 | 1968.20 | stop |
| 9 | judge | low | 1641 | 1416 | 340 | 1000 | 10000 | 1387.72 | stop |
| 10 | judge | low | 1627 | 1402 | 340 | 1000 | 10000 | 1406.20 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) system that extends large language models with a graph‑based text index and a dual‑level retrieval framework to address the flat‑representation and contextual‑awareness limits of existing RAG approaches, reporting notable improvements in accuracy, efficiency and response time while being open‑source[S1].  
The authors observe that many RAG systems rely on flat, chunk‑based indexes, which leads to fragmented answers for queries that involve inter‑dependent entities, and they propose using graph structures to capture entity relationships and support coherent synthesis; LightRAG therefore combines graph‑enhanced indexing with low‑level (entity‑specific) and high‑level (topic‑wide) retrieval to provide comprehensive, cost‑effective access to knowledge and to enable rapid incremental updates[S2].  
In the indexing stage, documents are split into chunks, LLM prompts extract entities (names, dates, locations, events) and their relations, and these are stored as a knowledge graph where each entity node holds a key‑value pair (entity name → summarizing paragraph) and edges carry thematic keys; new documents are processed similarly and merged with the existing graph without rebuilding the whole index[S4].  
The dual‑level retrieval paradigm generates both detailed and abstract query keys: specific keys drive low‑level retrieval of precise entities or edges, while abstract keys drive high‑level retrieval of broader topics; query keywords are matched in a vector database and the results are enriched with one‑hop neighboring nodes and edges to capture higher‑order relatedness[S5].  
For answer generation, the retrieved values (entity names, descriptions and text excerpts) are concatenated and fed to a general‑purpose LLM, which produces answers that are informative, aligned with the query intent and streamlined by the integrated context[S6].  
Complexity analysis shows that indexing requires one LLM call per token in each chunk with no extra overhead, and retrieval replaces whole‑chunk vector search with entity‑level vector matching, thereby markedly reducing retrieval overhead compared with community‑based traversal in GraphRAG[S7].  
The evaluation uses four “UltraDomain” corpora (Agriculture, CS, Legal, Mixed) ranging from 2 M to over 5 M tokens per dataset[S9][S18], and compares LightRAG against NaiveRAG, RQ‑RAG, HyDE and GraphRAG.  Across all datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates; the advantage grows with dataset size, e.g., on the largest Legal set baseline methods win only about 20 % versus LightRAG’s dominance, and LightRAG shows a particularly strong lead on the Diversity metric[S10].  
Ablation studies confirm that removing either the low‑level or high‑level retrieval component degrades performance on most metrics, while the full hybrid mode balances breadth and depth; additionally, eliminating the original text from retrieval (‑Origin) does not significantly hurt performance and can even improve results on some datasets, indicating the effectiveness of the graph‑based index alone[S11].  
Case‑study comparisons (e.g., a machine‑learning metric normalization query) show LightRAG outperforming GraphRAG on all judged dimensions, and a separate indigenous‑perspectives query demonstrates LightRAG’s more in‑depth, diverse answers relative to NaiveRAG, which the authors attribute to the dual‑level retrieval process[S12][S24].  
Cost and adaptability analysis on the Legal dataset reveals that LightRAG requires fewer than 100 tokens and a single API call for retrieval, whereas GraphRAG consumes hundreds of thousands of tokens and many API calls; for incremental updates, LightRAG integrates new entities without rebuilding the graph, incurring far lower overhead than GraphRAG’s costly community reconstruction[S13].  
Overall, the authors conclude that LightRAG’s graph‑based indexing, dual‑level retrieval and incremental update mechanism substantially boost retrieval speed and generation quality while lowering LLM inference costs, thereby improving efficiency and comprehension in RAG systems[S16].</pre>

## Q1 — repetition 2

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 5966.58

Judge latency_ms: 10638.37

Total evaluation latency_ms: 16644.87

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments large language models with graph‑based text indexing and a dual‑level retrieval framework to overcome the flat‑representation limits and poor contextual awareness of existing RAG approaches [S1][S2]. |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | The system first segments documents into chunks, uses LLM prompts to extract entities (names, dates, locations, events) and their relationships, and builds a knowledge graph \(\hat D=(\hat V,\hat E)\) where each entity node stores a key‑value pair (entity name → summarizing paragraph) and edges capture multi‑hop relations; |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | Retrieval operates on two levels: low‑level queries target precise entities or edges, while high‑level queries address broader topics; both generate query keywords, perform vector‑based search, and then augment results with one‑hop neighboring nodes and edges to capture higher‑order relatedness, improving relevance and comprehensiveness [S5][S6]. |
| incremental_update | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | new documents are processed in the same way and their graph components are unioned with the existing graph, avoiding full re‑indexing [S4][S5].<br><br>Cost and adaptability analysis demonstrates that LightRAG’s retrieval consumes fewer than 100 tokens and a single API call, versus GraphRAG’s 610 000 tokens and hundreds of calls; incremental updates for LightRAG merely add new entities to the existing graph, incurring far lower token and API overhead than GraphRAG’s full community reconstruction (≈5 000 tokens per report) [S13]. |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Evaluation uses four UltraDomain datasets—Agriculture, Computer‑Science, Legal, and Mixed—derived from 428 college textbooks (token counts ranging from 2 M to 5 M) and generates 125 questions per dataset via LLM‑driven prompting; LightRAG is compared against four baselines: NaiveRAG (vector‑based), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (graph‑enhanced) [S9][S18].<br><br>Across the four datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates than all baselines, with the gap widening on the largest Legal dataset where baselines win only about 20 % of the time; LightRAG also shows a pronounced advantage on the Diversity metric, attributed to its dual‑level retrieval paradigm [S10]. |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | Across the four datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates than all baselines, with the gap widening on the largest Legal dataset where baselines win only about 20 % of the time; LightRAG also shows a pronounced advantage on the Diversity metric, attributed to its dual‑level retrieval paradigm [S10]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | PASS | Required claim supported by verbatim evidence | The authors conclude that LightRAG markedly boosts retrieval speed, generation quality, and lowers LLM inference costs while supporting rapid adaptation to new information, thanks to its comprehensive knowledge graph, dual‑level retrieval, and incremental update mechanism |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 135 | 600 | 10000 | 871.58 | stop |
| 2 | answer | medium | 5590 | 5365 | 1434 | 3000 | 10000 | 5065.38 | stop |
| 3 | judge | low | 1607 | 1382 | 260 | 1000 | 10000 | 1155.46 | stop |
| 4 | judge | low | 1602 | 1377 | 230 | 1000 | 10000 | 1184.59 | stop |
| 5 | judge | low | 1604 | 1379 | 231 | 1000 | 10000 | 1729.23 | stop |
| 6 | judge | low | 1610 | 1385 | 382 | 1000 | 10000 | 1435.56 | stop |
| 7 | judge | low | 1613 | 1388 | 435 | 1000 | 10000 | 1372.45 | stop |
| 8 | judge | low | 1610 | 1385 | 352 | 1000 | 10000 | 1438.72 | stop |
| 9 | judge | low | 1617 | 1392 | 278 | 1000 | 10000 | 1157.98 | stop |
| 10 | judge | low | 1603 | 1378 | 328 | 1000 | 10000 | 1164.39 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments large language models with graph‑based text indexing and a dual‑level retrieval framework to overcome the flat‑representation limits and poor contextual awareness of existing RAG approaches [S1][S2].  

The system first segments documents into chunks, uses LLM prompts to extract entities (names, dates, locations, events) and their relationships, and builds a knowledge graph \(\hat D=(\hat V,\hat E)\) where each entity node stores a key‑value pair (entity name → summarizing paragraph) and edges capture multi‑hop relations; new documents are processed in the same way and their graph components are unioned with the existing graph, avoiding full re‑indexing [S4][S5].  

Retrieval operates on two levels: low‑level queries target precise entities or edges, while high‑level queries address broader topics; both generate query keywords, perform vector‑based search, and then augment results with one‑hop neighboring nodes and edges to capture higher‑order relatedness, improving relevance and comprehensiveness [S5][S6].  

Complexity analysis notes that indexing requires one LLM call per token in a chunk with no extra overhead, and that retrieving vector‑matched entities rather than whole chunks markedly reduces retrieval overhead compared with GraphRAG’s community‑based traversal [S7].  

Evaluation uses four UltraDomain datasets—Agriculture, Computer‑Science, Legal, and Mixed—derived from 428 college textbooks (token counts ranging from 2 M to 5 M) and generates 125 questions per dataset via LLM‑driven prompting; LightRAG is compared against four baselines: NaiveRAG (vector‑based), RQ‑RAG (query decomposition), HyDE (hypothetical document generation), and GraphRAG (graph‑enhanced) [S9][S18].  

Across the four datasets and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall), LightRAG achieves substantially higher win rates than all baselines, with the gap widening on the largest Legal dataset where baselines win only about 20 % of the time; LightRAG also shows a pronounced advantage on the Diversity metric, attributed to its dual‑level retrieval paradigm [S10].  

Ablation studies (Table 2) reveal that removing the high‑level module (‑High) leads to significant performance drops, especially on metrics requiring broad context, while removing the low‑level module (‑Low) harms comprehensiveness; omitting the original text (‑Origin) does not cause major declines and can even improve results on some datasets, suggesting the graph‑based index captures sufficient information [S11].  

A case study comparing LightRAG with GraphRAG on a machine‑learning normalization query shows LightRAG winning in all evaluated dimensions (comprehensiveness, diversity, empowerment, overall) [S12].  

Cost and adaptability analysis demonstrates that LightRAG’s retrieval consumes fewer than 100 tokens and a single API call, versus GraphRAG’s 610 000 tokens and hundreds of calls; incremental updates for LightRAG merely add new entities to the existing graph, incurring far lower token and API overhead than GraphRAG’s full community reconstruction (≈5 000 tokens per report) [S13].  

The authors conclude that LightRAG markedly boosts retrieval speed, generation quality, and lowers LLM inference costs while supporting rapid adaptation to new information, thanks to its comprehensive knowledge graph, dual‑level retrieval, and incremental update mechanism [S16][S14].  

Appendices provide detailed dataset statistics, the exact prompts used for graph construction, query generation, and keyword extraction, and additional case examples illustrating LightRAG’s retrieval‑augmented generation process [S18][S20][S21][S22][S19][S24].</pre>

## Q1 — repetition 3

Question: Summary this document.

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Summarize this document.

Sub-queries: []

Ask latency_ms: 6555.36

Judge latency_ms: 10484.96

Total evaluation latency_ms: 17064.31

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | PASS | Required claim supported by verbatim evidence | LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments large language models with graph‑based text indexing and a dual‑level retrieval framework to overcome the flat‑representation limits and poor contextual awareness of existing RAG approaches [S1][S2]. |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | The system first segments documents into chunks, uses LLM prompts to extract entities (e.g., names, dates, locations, events) and their relationships, and constructs a knowledge graph ˆD = (ˆV,ˆE) where each entity node stores a key‑value pair (entity name → summarizing paragraph) and edges capture multi‑hop relations; |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | Retrieval operates on two levels: low‑level (specific) queries target precise entities or edges, while high‑level (abstract) queries address broader topics; query keywords are generated, matched in a vector database, and then augmented with one‑hop neighboring nodes and edges to capture higher‑order relatedness, improving relevance and comprehensiveness [S5][S6]. |
| incremental_update | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | incremental updates are performed by processing new documents into a graph ˆD′ and unioning its nodes and edges with the existing graph, avoiding full re‑indexing [S4][S5].<br><br>...for incremental updates LightRAG integrates new entities with minimal overhead, while GraphRAG must dismantle and fully regenerate its community structure, incurring ≈5 000 tokens per report [S13]. |
| experiments | judge | PASS | Required claim supported by verbatim evidence | Evaluation is conducted on four UltraDomain datasets—Agriculture, Computer‑Science, Legal, and Mixed—derived from 428 college textbooks (600 k–5 M tokens per set) with 125 generated questions per dataset; LightRAG is compared against four baselines (NaiveRAG, RQ‑RAG, HyDE, GraphRAG) using a nano vector database, GPT‑4o‑mini for all LLM operations, a uniform chunk size of 1200, and a gleaning parameter of 1 [S9][S18].<br><br>Win‑rate results (Table 1) show LightRAG consistently outperforms the baselines across all evaluation dimensions, especially on the largest Legal dataset where baselines achieve only about 20 % win rates; LightRAG also shows a pronounced advantage on the Diversity metric, attributed to its dual‑level retrieval paradigm [S10]. |
| not_all_best | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | Win‑rate results (Table 1) show LightRAG consistently outperforms the baselines across all evaluation dimensions, especially on the largest Legal dataset where baselines achieve only about 20 % win rates; LightRAG also shows a pronounced advantage on the Diversity metric, attributed to its dual‑level retrieval paradigm [S10].<br><br>A case study comparing LightRAG with GraphRAG on a machine‑learning query reports that LightRAG wins on all judged dimensions—comprehensiveness, diversity, empowerment, and overall quality [S12]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |
| conclusion | judge | FAIL | Required claim not asserted: The answer does not explicitly state that Section 6’s conclusion combines effective, efficient graph‑based retrieval with adaptability; it mentions conclusions about speed, quality, and adaptation but does not reference Section 6 or explicitly tie effectiveness and efficiency to graph‑based retrieval. |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 819 | 480 | 135 | 600 | 10000 | 864.51 | stop |
| 2 | answer | medium | 5590 | 5365 | 1429 | 3000 | 10000 | 5674.10 | stop |
| 3 | judge | low | 1613 | 1388 | 278 | 1000 | 10000 | 1277.96 | stop |
| 4 | judge | low | 1608 | 1383 | 227 | 1000 | 10000 | 1124.43 | stop |
| 5 | judge | low | 1610 | 1385 | 230 | 1000 | 10000 | 994.63 | stop |
| 6 | judge | low | 1616 | 1391 | 277 | 1000 | 10000 | 1267.23 | stop |
| 7 | judge | low | 1619 | 1394 | 436 | 1000 | 10000 | 1714.15 | stop |
| 8 | judge | low | 1616 | 1391 | 318 | 1000 | 10000 | 1407.29 | stop |
| 9 | judge | low | 1623 | 1398 | 249 | 1000 | 10000 | 1225.73 | stop |
| 10 | judge | low | 1609 | 1384 | 316 | 1000 | 10000 | 1473.53 | stop |

### Finalized answer

<pre>LightRAG is a Retrieval‑Augmented Generation (RAG) system that augments large language models with graph‑based text indexing and a dual‑level retrieval framework to overcome the flat‑representation limits and poor contextual awareness of existing RAG approaches [S1][S2].  

The system first segments documents into chunks, uses LLM prompts to extract entities (e.g., names, dates, locations, events) and their relationships, and constructs a knowledge graph ˆD = (ˆV,ˆE) where each entity node stores a key‑value pair (entity name → summarizing paragraph) and edges capture multi‑hop relations; incremental updates are performed by processing new documents into a graph ˆD′ and unioning its nodes and edges with the existing graph, avoiding full re‑indexing [S4][S5].  

Retrieval operates on two levels: low‑level (specific) queries target precise entities or edges, while high‑level (abstract) queries address broader topics; query keywords are generated, matched in a vector database, and then augmented with one‑hop neighboring nodes and edges to capture higher‑order relatedness, improving relevance and comprehensiveness [S5][S6].  

Complexity analysis notes that indexing requires one LLM call per token in a chunk with no extra overhead, and that vector‑based retrieval of entities/relationships markedly reduces retrieval overhead compared with GraphRAG’s community‑based traversal [S7].  

Evaluation is conducted on four UltraDomain datasets—Agriculture, Computer‑Science, Legal, and Mixed—derived from 428 college textbooks (600 k–5 M tokens per set) with 125 generated questions per dataset; LightRAG is compared against four baselines (NaiveRAG, RQ‑RAG, HyDE, GraphRAG) using a nano vector database, GPT‑4o‑mini for all LLM operations, a uniform chunk size of 1200, and a gleaning parameter of 1 [S9][S18].  

Win‑rate results (Table 1) show LightRAG consistently outperforms the baselines across all evaluation dimensions, especially on the largest Legal dataset where baselines achieve only about 20 % win rates; LightRAG also shows a pronounced advantage on the Diversity metric, attributed to its dual‑level retrieval paradigm [S10].  

Ablation studies (Table 2) reveal that removing the high‑level module (‑High) leads to significant performance drops due to over‑focus on specific entities, while removing the low‑level module (‑Low) harms comprehensiveness because broader context is missed; the full hybrid mode balances breadth and depth, and omitting original text (‑Origin) does not cause major degradation, sometimes even improving results in Agriculture and Mix, indicating the graph‑based index captures sufficient context [S11].  

A case study comparing LightRAG with GraphRAG on a machine‑learning query reports that LightRAG wins on all judged dimensions—comprehensiveness, diversity, empowerment, and overall quality [S12].  

Cost and adaptability analysis shows that during retrieval LightRAG uses fewer than 100 tokens for keyword generation and requires only one API call, whereas GraphRAG consumes 610 000 tokens and hundreds of calls; for incremental updates LightRAG integrates new entities with minimal overhead, while GraphRAG must dismantle and fully regenerate its community structure, incurring ≈5 000 tokens per report [S13].  

The authors conclude that LightRAG markedly boosts retrieval speed, generation quality, and lowers LLM inference costs while supporting rapid adaptation to new information [S14][S16].  

Appendix sections provide detailed dataset statistics, prompt templates for graph construction, query generation, keyword extraction, and additional case examples that illustrate the system’s workflow and evaluation criteria [S18][S19][S20][S21][S22][S23][S24].</pre>

## Q2 — repetition 1

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG vs GraphRAG performance and scalability&#x27;, &#x27;LightRAG vs GraphRAG limitations and maintenance&#x27;]

Ask latency_ms: 8218.05

Judge latency_ms: 10301.90

Total evaluation latency_ms: 18551.06

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer discusses performance metrics and comparisons between LightRAG and GraphRAG, but does not mention GraphRAG traversing communities or LightRAG retrieving with dual‑level keywords (entities and topics). |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer never mentions Section 4.5, token counts (610 × 1,000), or API call details for GraphRAG or LightRAG, so it does not assert the required claim. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer discusses performance metrics and comparisons between LightRAG and GraphRAG but does not mention Section 4.5 or any details about GraphRAG rebuilding communities or LightRAG incrementally updating its graph. |  |
| table1_agriculture_overall | judge | FAIL | Required claim not asserted: The answer lists Agriculture Overall as 49.6% for LightRAG and 45.2% for GraphRAG, not the claimed 54.8% vs 45.2%, so the required values and comparison are incorrect. |  |
| table1_cs_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| 49.6 % / 45.2 % \| 52.0 % / 48.0 % \| 52.8 % / 47.2 % \| 49.6 % / 50.4 % \| |
| table1_legal_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| 49.6 % / 45.2 % \| 52.0 % / 48.0 % \| 52.8 % / 47.2 % \| 49.6 % / 50.4 % \| |
| table1_mix_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| 49.6 % / 45.2 % \| 52.0 % / 48.0 % \| 52.8 % / 47.2 % \| 49.6 % / 50.4 % \|<br> |
| table3_case_study | judge | PASS | Required claim supported by verbatim evidence | In a qualitative case study, LightRAG is reported to beat GraphRAG in **all** evaluation dimensions (comprehensiveness, diversity, empowerment, overall quality). [C4] |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 113 | 600 | 10000 | 820.64 | stop |
| 2 | answer | medium | 3644 | 3419 | 1348 | 3000 | 10000 | 6811.24 | stop |
| 3 | judge | low | 1507 | 1282 | 159 | 1000 | 10000 | 993.37 | stop |
| 4 | judge | low | 1569 | 1344 | 117 | 1000 | 10000 | 934.10 | stop |
| 5 | judge | low | 1504 | 1279 | 142 | 1000 | 10000 | 1012.84 | stop |
| 6 | judge | low | 1567 | 1342 | 176 | 1000 | 10000 | 1082.30 | stop |
| 7 | judge | low | 1572 | 1347 | 352 | 1000 | 10000 | 1364.42 | stop |
| 8 | judge | low | 1565 | 1340 | 305 | 1000 | 10000 | 1474.24 | stop |
| 9 | judge | low | 1566 | 1341 | 289 | 1000 | 10000 | 1462.91 | stop |
| 10 | judge | low | 1512 | 1287 | 176 | 1000 | 10000 | 1033.29 | stop |
| 11 | judge | low | 1505 | 1280 | 151 | 1000 | 10000 | 944.43 | stop |

### Finalized answer

<pre>**Overall performance**

- Across the three large‑scale datasets (Agriculture, CS, Legal) LightRAG achieves higher win rates than GraphRAG on most metrics, while on the smaller “Mix” dataset GraphRAG is slightly ahead on a few cells.  

**Metric‑by‑metric comparison (Table 1)**  

| Metric | Agriculture (LightRAG / GraphRAG) | CS (LightRAG / GraphRAG) | Legal (LightRAG / GraphRAG) | Mix (LightRAG / GraphRAG) |
|--------|-----------------------------------|--------------------------|-----------------------------|---------------------------|
| **Comprehensiveness** | 54.4 % / 45.6 % | 51.6 % / 48.4 % | 51.6 % / 48.4 % | 49.6 % / 50.4 % |
| **Diversity** | 77.2 % / 22.8 % | 59.2 % / 40.8 % | 73.6 % / 26.4 % | 64.0 % / 36.0 % |
| **Empowerment** | 58.8 % / 41.2 % | 54.8 % / 45.2 % | 56.4 % / 43.6 % | 49.2 % / 50.8 % |
| **Overall** | 49.6 % / 45.2 % | 52.0 % / 48.0 % | 52.8 % / 47.2 % | 49.6 % / 50.4 % |

These figures show that LightRAG wins a larger share of evaluations on **Comprehensiveness, Diversity, Empowerment, and Overall** for the three large corpora, whereas GraphRAG has a modest edge only on the Mix dataset’s Overall and Empowerment scores. [C2]

**Narrative findings**

- The authors state that “LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts” (Agriculture, CS, Legal). [C3]  
- In a qualitative case study, LightRAG is reported to beat GraphRAG in **all** evaluation dimensions (comprehensiveness, diversity, empowerment, overall quality). [C4]

**Summary**

- **Strengths of LightRAG vs. GraphRAG:** Higher win rates on most metrics for the three large‑scale datasets, especially in Diversity where LightRAG’s advantage is most pronounced (e.g., 77.2 % vs. 22.8 % on Agriculture).  
- **Exception:** On the smaller Mix dataset, GraphRAG slightly surpasses LightRAG in Overall (50.4 % vs. 49.6 %) and Empowerment (50.8 % vs. 49.2 %).  

Overall, the evidence indicates that LightRAG generally provides better performance than GraphRAG, particularly when handling large, complex corpora.</pre>

## Q2 — repetition 2

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG GraphRAG performance comparison&#x27;, &#x27;LightRAG GraphRAG maintenance and update requirements&#x27;]

Ask latency_ms: 9235.06

Judge latency_ms: 9826.03

Total evaluation latency_ms: 19093.18

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer provides performance tables and qualitative observations but does not state anything about GraphRAG traversing communities or LightRAG retrieving with dual-level keywords, so the claim is neither mentioned nor affirmed. |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer does not mention the token counts (610 × 1,000 tokens), the &lt;100 token claim, or the single API call for LightRAG, nor does it address retrieval cost as described in the claim. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer provides performance tables and qualitative observations but does not mention Section 4.5, nor any claim about GraphRAG rebuilding communities or LightRAG incrementally updating its graph. |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | **Overall** \| Agriculture \| 45.2 % \| 54.8 % \| LightRAG |
| table1_cs_overall | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | \| Overall \| CS \| 48.0 % \| 52.0 % \| LightRAG \| |
| table1_legal_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| Legal \| 47.2 % \| 52.8 % \| LightRAG \| |
| table1_mix_overall | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | \| Overall \| Mix \| 50.4 % \| 49.6 % \| **GraphRAG** \| |
| table3_case_study | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | In a detailed case‑study (Table 3), LightRAG was judged superior to GraphRAG on **all** evaluation dimensions—comprehensiveness, diversity, empowerment, and overall quality for a specific machine‑learning query[C6]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 103 | 600 | 10000 | 828.51 | stop |
| 2 | answer | medium | 4210 | 3985 | 1442 | 3000 | 10000 | 5209.76 | stop |
| 3 | judge | low | 1568 | 1343 | 125 | 1000 | 10000 | 809.80 | stop |
| 4 | judge | low | 1630 | 1405 | 118 | 1000 | 10000 | 969.48 | stop |
| 5 | judge | low | 1565 | 1340 | 128 | 1000 | 10000 | 805.81 | stop |
| 6 | judge | low | 1628 | 1403 | 275 | 1000 | 10000 | 1406.98 | stop |
| 7 | judge | low | 1633 | 1408 | 242 | 1000 | 10000 | 1143.87 | stop |
| 8 | judge | low | 1626 | 1401 | 200 | 1000 | 10000 | 1040.52 | stop |
| 9 | judge | low | 1627 | 1402 | 281 | 1000 | 10000 | 1327.56 | stop |
| 10 | judge | low | 1573 | 1348 | 223 | 1000 | 10000 | 1216.70 | stop |
| 11 | judge | low | 1566 | 1341 | 167 | 1000 | 10000 | 1105.31 | stop |

### Finalized answer

<pre>**Performance on quantitative benchmarks**

| Metric | Dataset | GraphRAG win % | LightRAG win % | Which system wins? |
|--------|---------|---------------|----------------|-------------------|
| **Comprehensiveness** | Agriculture | 45.6 % | 54.4 % | LightRAG |
| | CS | 48.4 % | 51.6 % | LightRAG |
| | Legal | 48.4 % | 51.6 % | LightRAG |
| | Mix | 50.4 % | 49.6 % | **GraphRAG** |
| **Diversity** | Agriculture | 22.8 % | 77.2 % | LightRAG |
| | CS | 40.8 % | 59.2 % | LightRAG |
| | Legal | 26.4 % | 73.6 % | LightRAG |
| | Mix | 36.0 % | 64.0 % | LightRAG |
| **Empowerment** | Agriculture | 41.2 % | 58.8 % | LightRAG |
| | CS | 45.2 % | 54.8 % | LightRAG |
| | Legal | 43.6 % | 56.4 % | LightRAG |
| | Mix | 50.8 % | 49.2 % | **GraphRAG** |
| **Overall** | Agriculture | 45.2 % | 54.8 % | LightRAG |
| | CS | 48.0 % | 52.0 % | LightRAG |
| | Legal | 47.2 % | 52.8 % | LightRAG |
| | Mix | 50.4 % | 49.6 % | **GraphRAG** |

These win‑rate figures come directly from Table 1, which lists baseline (GraphRAG) versus candidate (LightRAG) win percentages across four datasets and four evaluation dimensions[C4]. LightRAG achieves higher win rates than GraphRAG on the Agriculture, CS, and Legal datasets for every metric, while GraphRAG is slightly ahead only on the mixed‑domain (Mix) dataset for Comprehensiveness, Empowerment, and Overall.

**Qualitative observations**

* The authors state that “LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts… Agriculture, CS, and Legal… LightRAG shows a clear advantage”[C5]. This aligns with the numeric results above, where LightRAG dominates on those three large‑scale corpora.

* In a detailed case‑study (Table 3), LightRAG was judged superior to GraphRAG on **all** evaluation dimensions—comprehensiveness, diversity, empowerment, and overall quality—for a specific machine‑learning query[C6].

**Summary**

- **Strengths of LightRAG vs. GraphRAG**: Higher win rates on the three large, domain‑specific datasets (Agriculture, CS, Legal) across every metric; better performance on a concrete case study; textual claims emphasize its advantage in handling complex, large‑scale corpora.

- **Where GraphRAG still leads**: On the mixed‑domain dataset (Mix), GraphRAG edges out LightRAG in Comprehensiveness, Empowerment, and Overall, though LightRAG remains ahead on Diversity for that dataset.</pre>

## Q2 — repetition 3

Question: Compare LightRAG with GraphRAG.

Question Type: Synthesis; expected: Synthesis

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: Compare LightRAG with GraphRAG.

Sub-queries: [&#x27;LightRAG vs GraphRAG mechanisms&#x27;, &#x27;LightRAG GraphRAG performance comparison&#x27;, &#x27;LightRAG GraphRAG maintenance and update requirements&#x27;]

Ask latency_ms: 7240.98

Judge latency_ms: 11400.39

Total evaluation latency_ms: 18718.50

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Synthesis; actual Synthesis; plan_source=router; fallback_reason=None |  |
| retrieval_methods | judge | FAIL | Required claim not asserted: The answer discusses benchmark win rates and observations, but does not mention GraphRAG traversing communities or LightRAG retrieving with dual-level keywords, so the claim is neither stated nor affirmed. |  |
| retrieval_cost | judge | FAIL | Required claim not asserted: The answer provides benchmark win‑rate tables and observations but does not state the claim about GraphRAG using about 610 × 1,000 tokens and LightRAG using fewer than 100 tokens with only one API call. Hence the required claim is missing. |  |
| incremental_update | judge | FAIL | Required claim not asserted: The answer discusses benchmark win rates and observations, but does not mention Section 4.5 or any claim about GraphRAG rebuilding communities or LightRAG incrementally updating its graph. |  |
| table1_agriculture_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| **Overall** \| Agriculture \| 45.2 % \| 54.8 % \| LightRAG \| |
| table1_cs_overall | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | \| Overall \| CS \| 48.0 % \| 52.0 % \| LightRAG \| |
| table1_legal_overall | judge | FAIL | Numeric evidence lacks the required variant/dataset/metric/value context | \| Legal \| 47.2 % \| 52.8 % \| LightRAG \| |
| table1_mix_overall | judge | FAIL | Numeric variant/value do not co-occur in the same clause or row | \| **Overall** \| Agriculture \| 45.2 % \| 54.8 % \| LightRAG \|<br>\| \| CS \| 48.0 % \| 52.0 % \| LightRAG \|<br>\| \| Legal \| 47.2 % \| 52.8 % \| LightRAG \|<br>\| \| Mix \| 50.4 % \| 49.6 % \| **GraphRAG** \| |
| table3_case_study | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | Case‑study confirmation — In a concrete example (machine‑learning question), LightRAG was judged to be better than GraphRAG on all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C6]. |
| not_all_datasets | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 100 | 600 | 10000 | 790.77 | stop |
| 2 | answer | medium | 4210 | 3985 | 1429 | 3000 | 10000 | 5705.04 | stop |
| 3 | judge | low | 1557 | 1332 | 136 | 1000 | 10000 | 1015.50 | stop |
| 4 | judge | low | 1619 | 1394 | 127 | 1000 | 10000 | 1232.06 | stop |
| 5 | judge | low | 1554 | 1329 | 132 | 1000 | 10000 | 930.93 | stop |
| 6 | judge | low | 1617 | 1392 | 261 | 1000 | 10000 | 1454.54 | stop |
| 7 | judge | low | 1622 | 1397 | 236 | 1000 | 10000 | 1488.44 | stop |
| 8 | judge | low | 1615 | 1390 | 226 | 1000 | 10000 | 1340.84 | stop |
| 9 | judge | low | 1616 | 1391 | 314 | 1000 | 10000 | 1653.68 | stop |
| 10 | judge | low | 1562 | 1337 | 237 | 1000 | 10000 | 1166.67 | stop |
| 11 | judge | low | 1555 | 1330 | 137 | 1000 | 10000 | 1117.73 | stop |

### Finalized answer

<pre>**Performance on benchmark datasets**

| Metric | Dataset | GraphRAG win % | LightRAG win % | Which system wins? |
|-------|---------|---------------|----------------|--------------------|
| **Comprehensiveness** | Agriculture | 45.6 % | 54.4 % | LightRAG |
| | CS | 48.4 % | 51.6 % | LightRAG |
| | Legal | 48.4 % | 51.6 % | LightRAG |
| | Mix | 50.4 % | 49.6 % | **GraphRAG** |
| **Diversity** | Agriculture | 22.8 % | 77.2 % | LightRAG |
| | CS | 40.8 % | 59.2 % | LightRAG |
| | Legal | 26.4 % | 73.6 % | LightRAG |
| | Mix | 36.0 % | 64.0 % | LightRAG |
| **Empowerment** | Agriculture | 41.2 % | 58.8 % | LightRAG |
| | CS | 45.2 % | 54.8 % | LightRAG |
| | Legal | 43.6 % | 56.4 % | LightRAG |
| | Mix | 50.8 % | 49.2 % | **GraphRAG** |
| **Overall** | Agriculture | 45.2 % | 54.8 % | LightRAG |
| | CS | 48.0 % | 52.0 % | LightRAG |
| | Legal | 47.2 % | 52.8 % | LightRAG |
| | Mix | 50.4 % | 49.6 % | **GraphRAG** |

These win‑rate figures come directly from Table 1, which lists baseline (GraphRAG) versus candidate (LightRAG) win percentages across four datasets and four evaluation dimensions[C4].

**Key observations**

1. **Consistent advantage on larger, domain‑specific corpora** – LightRAG beats GraphRAG on the Agriculture, CS, and Legal datasets for every metric (Comprehensiveness, Diversity, Empowerment, Overall). This aligns with the authors’ qualitative claim that LightRAG “consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts”[C5].

2. **Mixed dataset exception** – On the “Mix” dataset, GraphRAG has a slight edge for Comprehensiveness, Empowerment, and Overall, while LightRAG still leads on Diversity. Thus LightRAG’s superiority is not universal across all data mixes.

3. **Case‑study confirmation** – In a concrete example (machine‑learning question), LightRAG was judged to be better than GraphRAG on all four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C6].

**Summary**

Overall, LightRAG demonstrates higher win rates than GraphRAG on the three larger, domain‑focused datasets (Agriculture, CS, Legal) across all measured dimensions, confirming its stronger performance in handling extensive token counts and complex queries. The only notable deviation is on the mixed‑domain dataset, where GraphRAG marginally outperforms LightRAG on three of the four dimensions.</pre>

## Q3 — repetition 1

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 7390.49

Judge latency_ms: 7778.32

Total evaluation latency_ms: 15215.01

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | For each variant the table reports the win‑rate of the NaiveRAG baseline versus the win‑rate of the variant (percentage of queries where the variant beats NaiveRAG) on four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall)[C8]. |
| ablation_meaning | judge | FAIL | Required claim not asserted: The answer states that -High is a high-level‑only retrieval variant, whereas the claim says -High removes high-level retrieval. This contradicts the required claim, so it is not asserted. |  |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer provides the -Low Overall win rate of 64.8% for Mix, but does not give the full LightRAG Overall win rate of 60.0% on Mix, so it does not assert the complete claim. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer provides the -Origin Overall win rate of 74.4% for Agriculture but does not explicitly state the full LightRAG&#x27;s Agriculture Overall win rate as 67.6% nor explicitly claim that 74.4% is higher, so the required claim is not fully asserted. |  |
| not_all_best | forbidden | FAIL | Forbidden claim asserted | Thus, the ablated versions achieve lower win‑rates than the full LightRAG system (which attains 67.6 %–86.4 % depending on metric and dataset) but still outperform the NaiveRAG baseline, with the hybrid (full) model providing the most balanced and highest performance across all dimensions. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 118 | 600 | 10000 | 942.76 | stop |
| 2 | answer | medium | 5738 | 5513 | 1625 | 3000 | 10000 | 5767.05 | stop |
| 3 | judge | low | 2078 | 1853 | 254 | 1000 | 10000 | 1280.73 | stop |
| 4 | judge | low | 2079 | 1854 | 277 | 1000 | 10000 | 1600.38 | stop |
| 5 | judge | low | 2138 | 1913 | 259 | 1000 | 10000 | 1379.57 | stop |
| 6 | judge | low | 2139 | 1914 | 362 | 1000 | 10000 | 1960.31 | stop |
| 7 | judge | low | 2066 | 1841 | 319 | 1000 | 10000 | 1557.33 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (compared to NaiveRAG)**  

The paper evaluates three ablated variants of LightRAG – **‑High** (high‑level‑only retrieval), **‑Low** (low‑level‑only retrieval) and **‑Origin** (removing the original‑text component).  
For each variant the table reports the win‑rate of the NaiveRAG baseline versus the win‑rate of the variant (percentage of queries where the variant beats NaiveRAG) on four datasets (Agriculture, CS, Legal, Mix) and four evaluation metrics (Comprehensiveness, Diversity, Empowerment, Overall)[C8].

| Variant | Metric | Agriculture (NaiveRAG / Variant) | CS (NaiveRAG / Variant) | Legal (NaiveRAG / Variant) | Mix (NaiveRAG / Variant) |
|---------|--------|-----------------------------------|--------------------------|-----------------------------|--------------------------|
| **‑High** | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
|  | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
|  | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
|  | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
|  | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
|  | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
|  | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
|  | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
|  | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
|  | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

*All percentages are “NaiveRAG win rate / variant win rate” as defined in the table caption[C8].*

**Qualitative observations**

* The **‑Low** (low‑level‑only) variant “leads to a significant performance decline across nearly all datasets and metrics” because it focuses too narrowly on specific entities, limiting its ability to answer complex queries[C9].  
* The **‑High** (high‑level‑only) variant also shows a “significant performance decline” due to its emphasis on broader content at the expense of depth[C9].  
* The **‑Origin** variant, which removes the original text from retrieval, “does not exhibit significant performance declines” and even improves in some cases (e.g., Agriculture and Mix) because the graph‑based indexing extracts sufficient key information while discarding noisy text[C9].  

Thus, the ablated versions achieve lower win‑rates than the full LightRAG system (which attains 67.6 %–86.4 % depending on metric and dataset) but still outperform the NaiveRAG baseline, with the hybrid (full) model providing the most balanced and highest performance across all dimensions.</pre>

## Q3 — repetition 2

Question: Performance of ablated versions of LightRAG.

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: []

Ask latency_ms: 6501.42

Judge latency_ms: 9243.97

Total evaluation latency_ms: 17579.71

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C8 |
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | PASS | Required claim supported by verbatim evidence | *Each cell shows “NaiveRAG win % / variant win %”.*  <br>These figures are taken directly from Table 2, which reports the win‑rate comparisons of the ablated LightRAG variants against the NaiveRAG baseline across four datasets and four evaluation metrics[C8]. |
| ablation_meaning | judge | FAIL | Required claim not asserted: The answer describes the ablated variants and their meanings but does not state that the full LightRAG combines both high‑level and low‑level retrieval, so the claim is not fully satisfied. |  |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer provides the -Low Overall win rate for Mix (64.8%) but does not state the full LightRAG overall win rate (60.0%) nor explicitly claim that 64.8% is higher than 60.0%. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer provides the -Origin Overall win rate for Agriculture (74.4%) but does not give the full LightRAG overall win rate (67.6%) needed to confirm the comparison, so the claim is not fully supported. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 127 | 600 | 10000 | 1522.01 | stop |
| 2 | answer | medium | 5738 | 5513 | 1400 | 3000 | 10000 | 4825.61 | stop |
| 3 | judge | low | 1965 | 1740 | 313 | 1000 | 10000 | 1475.36 | stop |
| 4 | judge | low | 1966 | 1741 | 219 | 1000 | 10000 | 1154.43 | stop |
| 5 | judge | low | 2025 | 1800 | 267 | 1000 | 10000 | 1776.97 | stop |
| 6 | judge | low | 2026 | 1801 | 252 | 1000 | 10000 | 3694.95 | stop |
| 7 | judge | low | 1953 | 1728 | 173 | 1000 | 10000 | 1142.26 | stop |

### Finalized answer

<pre>**Ablated versions of LightRAG (compared against the NaiveRAG baseline)**  

| Variant | Metric | Agriculture | CS | Legal | Mix |
|--------|--------|--------------|----|-------|-----|
| **‑High** (high‑level‑only retrieval) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (low‑level‑only retrieval) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (no original text) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

*Each cell shows “NaiveRAG win % / variant win %”.*  
These figures are taken directly from Table 2, which reports the win‑rate comparisons of the ablated LightRAG variants against the NaiveRAG baseline across four datasets and four evaluation metrics[C8].

**Key observations (from the same table and accompanying notes):**  

* The **‑High** variant (high‑level‑only retrieval) generally loses to NaiveRAG on the “Comprehensiveness” metric for Agriculture and CS, but outperforms NaiveRAG on Diversity, Empowerment and Overall in most datasets.  
* The **‑Low** variant (low‑level‑only retrieval) shows a similar pattern: lower win rates on Diversity for the Legal dataset (13.6 % / 86.4 %) but higher win rates on Overall across all datasets.  
* The **‑Origin** variant (removing original text) still achieves strong win rates, often exceeding 70 % for the variant side, and in some cases (e.g., Agriculture Diversity 73.6 % vs NaiveRAG 26.4 %) even improves over the full system.  

These results demonstrate that removing either the high‑level or low‑level retrieval component degrades performance on certain metrics, while eliminating the original text has a comparatively modest impact.</pre>

## Q3 — repetition 3

Question: Performance of ablated versions of LightRAG.

Question Type: Synthesis; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: What is the performance of the ablated versions of LightRAG?

Sub-queries: [&#x27;LightRAG ablation performance metrics&#x27;, &#x27;effect of removing retriever on LightRAG&#x27;, &#x27;impact of disabling generator in LightRAG&#x27;]

Ask latency_ms: 13769.57

Judge latency_ms: 8883.19

Total evaluation latency_ms: 22706.48

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| required_source_citation | events | PASS | Used Citation resolves to the required Table Chunk | C4 |
| question_type | events | FAIL | Expected Lookup; actual Synthesis; plan_source=router; fallback_reason=None |  |
| high_term | contains | PASS | Term found |  |
| low_term | contains | PASS | Term found |  |
| origin_term | contains | PASS | Term found |  |
| table2_baseline | judge | FAIL | Judge evidence is not a nonempty verbatim excerpt | For each variant the table reports the win‑rate of NaiveRAG versus the win‑rate of the variant (percentage) on four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C4].<br><br>These percentages represent “NaiveRAG win rate / variant win rate” for each dataset‑metric pair, indicating that all three ablated versions achieve lower win rates than the full LightRAG system (which attains the higher win‑rate side of each pair)[C4]. |
| ablation_meaning | judge | FAIL | Required claim not asserted: The answer states that -High removes low-level retrieval and -Low removes high-level retrieval, which contradicts the claim that -High removes high-level retrieval and -Low removes low-level retrieval; thus the claim is not matched or asserted. |  |
| mix_low_overall | judge | FAIL | Required claim not asserted: The answer provides the -Low Overall win rate for Mix (64.8%) but does not state the full LightRAG overall win rate (60.0%) nor the comparison that 64.8% is higher, so the required claim is not fully asserted. |  |
| agriculture_origin_overall | judge | FAIL | Required claim not asserted: The answer provides the -Origin Overall win rate of 74.4% for Agriculture but does not state the full LightRAG overall win rate of 67.6% nor explicitly claim that 74.4% is higher, so the required claim is not fully present. |  |
| not_all_best | forbidden | FAIL | Judge evidence is not a nonempty verbatim excerpt | These percentages represent “NaiveRAG win rate / variant win rate” for each dataset‑metric pair, indicating that all three ablated versions achieve lower win rates than the full LightRAG system (which attains the higher win‑rate side of each pair). |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 825 | 486 | 245 | 600 | 10000 | 1441.87 | stop |
| 2 | answer | medium | 3531 | 3306 | 1281 | 3000 | 10000 | 5410.95 | stop |
| 3 | judge | low | 1790 | 1565 | 436 | 1000 | 10000 | 1844.99 | stop |
| 4 | judge | low | 1791 | 1566 | 178 | 1000 | 10000 | 1435.01 | stop |
| 5 | judge | low | 1851 | 1626 | 287 | 1000 | 10000 | 1611.36 | stop |
| 6 | judge | low | 1852 | 1627 | 302 | 1000 | 10000 | 1702.04 | stop |
| 7 | judge | low | 1778 | 1553 | 475 | 1000 | 10000 | 2289.79 | stop |

### Finalized answer

<pre>The ablation study compares three stripped‑down variants of LightRAG (‑High, ‑Low, and ‑Origin) against the NaiveRAG baseline.  For each variant the table reports the win‑rate of NaiveRAG versus the win‑rate of the variant (percentage) on four datasets (Agriculture, CS, Legal, Mix) and four evaluation dimensions (Comprehensiveness, Diversity, Empowerment, Overall)[C4].

**‑High (removes low‑level retrieval)**  
| Metric | Agriculture | CS | Legal | Mix |
|--------|--------------|----|-------|-----|
| Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
| Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
| Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
| Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |

**‑Low (removes high‑level retrieval)**  
| Metric | Agriculture | CS | Legal | Mix |
|--------|--------------|----|-------|-----|
| Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
| Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
| Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
| Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |

**‑Origin (removes original text from retrieval)**  
| Metric | Agriculture | CS | Legal | Mix |
|--------|--------------|----|-------|-----|
| Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
| Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
| Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
| Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

These percentages represent “NaiveRAG win rate / variant win rate” for each dataset‑metric pair, indicating that all three ablated versions achieve lower win rates than the full LightRAG system (which attains the higher win‑rate side of each pair)[C4].</pre>

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Ask latency_ms: 2289.43

Judge latency_ms: 0.00

Total evaluation latency_ms: 2350.76

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 117 | 600 | 10000 | 948.66 | stop |
| 2 | answer | medium | 6646 | 6421 | 110 | 3000 | 10000 | 941.72 | stop |

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

Ask latency_ms: 1926.00

Judge latency_ms: 0.00

Total evaluation latency_ms: 1937.23

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 124 | 600 | 10000 | 786.76 | stop |
| 2 | answer | medium | 6646 | 6421 | 110 | 3000 | 10000 | 954.32 | stop |

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

Ask latency_ms: 2439.25

Judge latency_ms: 0.00

Total evaluation latency_ms: 2450.18

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 841 | 502 | 119 | 600 | 10000 | 899.74 | stop |
| 2 | answer | medium | 6646 | 6421 | 111 | 3000 | 10000 | 917.02 | stop |

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

Ask latency_ms: 1981.47

Judge latency_ms: 0.00

Total evaluation latency_ms: 1981.92

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 90 | 600 | 10000 | 809.45 | stop |
| 2 | answer | medium | 6667 | 6442 | 120 | 3000 | 10000 | 996.22 | stop |

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

Ask latency_ms: 1988.91

Judge latency_ms: 0.00

Total evaluation latency_ms: 1989.91

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 87 | 600 | 10000 | 805.23 | stop |
| 2 | answer | medium | 6667 | 6442 | 120 | 3000 | 10000 | 1032.76 | stop |

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

Ask latency_ms: 2122.19

Judge latency_ms: 0.00

Total evaluation latency_ms: 2122.99

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 824 | 485 | 67 | 600 | 10000 | 727.97 | stop |
| 2 | answer | medium | 6667 | 6442 | 120 | 3000 | 10000 | 1006.29 | stop |

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

Ask latency_ms: 2518.57

Judge latency_ms: 0.00

Total evaluation latency_ms: 2523.33

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 108 | 600 | 10000 | 907.86 | stop |
| 2 | answer | medium | 5867 | 5642 | 133 | 3000 | 10000 | 1254.06 | stop |

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

Ask latency_ms: 2129.72

Judge latency_ms: 0.00

Total evaluation latency_ms: 2140.26

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 108 | 600 | 10000 | 938.39 | stop |
| 2 | answer | medium | 5867 | 5642 | 133 | 3000 | 10000 | 1072.08 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_GPU — repetition 3

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Ask latency_ms: 2106.31

Judge latency_ms: 0.00

Total evaluation latency_ms: 2118.56

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup; plan_source=router; fallback_reason=None |  |
| fixed_reply | judge | PASS | Fixed reply matched |  |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 842 | 503 | 108 | 600 | 10000 | 888.34 | stop |
| 2 | answer | medium | 5867 | 5642 | 140 | 3000 | 10000 | 1015.00 | stop |

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

Ask latency_ms: 5671.14

Judge latency_ms: 15119.11

Total evaluation latency_ms: 20822.83

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted: The answer does not explicitly state that flat RAG loses contextual interdependencies; it only mentions overcoming limitations of flat representation, which does not directly assert the specific claim. |  |
| graph_indexing | judge | FAIL | Required claim not asserted: The answer does not mention Section 3.1 or explicitly state that graph-based indexing extracts entities and relationships; it only describes LightRAG&#x27;s graph-based indexing in general. |  |
| dual_level | judge | FAIL | Required claim not asserted: The answer describes a dual-layer retrieval framework but does not state that it combines specific entities and broader topics as required by the claim. |  |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | 與 GraphRAG 相比，LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，且在增量更新時不需重建社群結構，顯著降低了 token 消耗與推論成本，同時提升檢索速度與生成品質。 |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在四個大規模領域資料集（農業、計算機科學、法律、混合）上，LightRAG 的勝率在全面性與多樣性等評估維度上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，尤其在資料量最大的法律資料集上差距顯著，且消除任一層級的檢索皆會導致效能下降，證實雙層檢索的平衡效益。 |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | 在四個大規模領域資料集（農業、計算機科學、法律、混合）上，LightRAG 的勝率在全面性與多樣性等評估維度上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，尤其在資料量最大的法律資料集上差距顯著，且消除任一層級的檢索皆會導致效能下降，證實雙層檢索的平衡效益。 |
| conclusion | judge | FAIL | Required claim not asserted: The answer does not mention Section 6 or a conclusion that combines effective, efficient graph-based retrieval with adaptability; it describes LightRAG features without referencing the claimed statement. |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過圖形化的文本索引與雙層檢索框架，結合圖結構與向量嵌入，以有效的實體‑關係檢索克服傳統平面表示的限制，並提供增量更新演算法以快速整合新資料。[S1][S4][S5]  <br><br>在四個大規模領域資料集（農業、計算機科學、法律、混合）上，LightRAG 的勝率在全面性與多樣性等評估維度上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，尤其在資料量最大的法律資料集上差距顯著，且消除任一層級的檢索皆會導致效能下降，證實雙層檢索的平衡效益。[S9][S10][S11]  <br><br>與 GraphRAG 相比，LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，且在增量更新時不需重建社群結構，顯著降低了 token 消耗與推論成本，同時提升檢索速度與生成品質。[S13][S16] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過圖形化的文本索引與雙層檢索框架，結合圖結構與向量嵌入，以有效的實體‑關係檢索克服傳統平面表示的限制，並提供增量更新演算法以快速整合新資料。[S1][S4][S5]<br><br>在四個大規模領域資料集（農業、計算機科學、法律、混合）上，LightRAG 的勝率在全面性與多樣性等評估維度上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，尤其在資料量最大的法律資料集上差距顯著，且消除任一層級的檢索皆會導致效能下降，證實雙層檢索的平衡效益。[S9][S10][S11]<br><br>與 GraphRAG 相比，LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，且在增量更新時不需重建社群結構，顯著降低了 token 消耗與推論成本，同時提升檢索速度與生成品質。[S13][S16] |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | LightRAG 透過圖形化的文本索引與雙層檢索框架，結合圖結構與向量嵌入，以有效的實體‑關係檢索克服傳統平面表示的限制，並提供增量更新演算法以快速整合新資料。[S1][S4][S5]  <br><br>在四個大規模領域資料集（農業、計算機科學、法律、混合）上，LightRAG 的勝率在全面性與多樣性等評估維度上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，尤其在資料量最大的法律資料集上差距顯著，且消除任一層級的檢索皆會導致效能下降，證實雙層檢索的平衡效益。[S9][S10][S11]  <br><br>與 GraphRAG 相比，LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，且在增量更新時不需重建社群結構，顯著降低了 token 消耗與推論成本，同時提升檢索速度與生成品質。[S13][S16] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 104 | 600 | 10000 | 775.72 | stop |
| 2 | answer | medium | 5620 | 5395 | 1097 | 3000 | 10000 | 4867.40 | stop |
| 3 | judge | low | 1060 | 835 | 285 | 1000 | 10000 | 1782.88 | stop |
| 4 | judge | low | 1055 | 830 | 229 | 1000 | 10000 | 1354.85 | stop |
| 5 | judge | low | 1057 | 832 | 131 | 1000 | 10000 | 1031.03 | stop |
| 6 | judge | low | 1063 | 838 | 234 | 1000 | 10000 | 1171.24 | stop |
| 7 | judge | low | 1066 | 841 | 305 | 1000 | 10000 | 1405.38 | stop |
| 8 | judge | low | 1063 | 838 | 247 | 1000 | 10000 | 1468.83 | stop |
| 9 | judge | low | 1070 | 845 | 321 | 1000 | 10000 | 1433.55 | stop |
| 10 | judge | low | 1056 | 831 | 119 | 1000 | 10000 | 842.60 | stop |
| 11 | judge | low | 1057 | 832 | 476 | 1000 | 10000 | 2010.21 | stop |
| 12 | judge | low | 1066 | 841 | 763 | 1000 | 10000 | 2618.55 | stop |

### Finalized answer

<pre>LightRAG 透過圖形化的文本索引與雙層檢索框架，結合圖結構與向量嵌入，以有效的實體‑關係檢索克服傳統平面表示的限制，並提供增量更新演算法以快速整合新資料。[S1][S4][S5]  

在四個大規模領域資料集（農業、計算機科學、法律、混合）上，LightRAG 的勝率在全面性與多樣性等評估維度上均優於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG，尤其在資料量最大的法律資料集上差距顯著，且消除任一層級的檢索皆會導致效能下降，證實雙層檢索的平衡效益。[S9][S10][S11]  

與 GraphRAG 相比，LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，且在增量更新時不需重建社群結構，顯著降低了 token 消耗與推論成本，同時提升檢索速度與生成品質。[S13][S16]</pre>

## Q1_ZH_THREE_SENTENCES — repetition 2

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 6020.04

Judge latency_ms: 14709.86

Total evaluation latency_ms: 20758.18

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted: The answer never mentions flat RAG or that it loses contextual interdependencies, so it does not state the required claim. |  |
| graph_indexing | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。 |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。 |
| incremental_update | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。 |
| experiments | judge | PASS | Required claim supported by verbatim evidence | 在四個大規模領域資料集（Agriculture、CS、Legal、Mix）上，LightRAG 相較於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 在全面性、多樣性等評估維度皆取得更高的勝率，尤其在資料量最大的 Legal 資料集上表現顯著提升。 |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | 在四個大規模領域資料集（Agriculture、CS、Legal、Mix）上，LightRAG 相較於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 在全面性、多樣性等評估維度皆取得更高的勝率，尤其在資料量最大的 Legal 資料集上表現顯著提升。 |
| conclusion | judge | FAIL | Required claim not asserted: The answer does not mention Section 6, nor state that the conclusion combines effective, efficient graph-based retrieval with adaptability. |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。[S4][S5]  <br>在四個大規模領域資料集（Agriculture、CS、Legal、Mix）上，LightRAG 相較於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 在全面性、多樣性等評估維度皆取得更高的勝率，尤其在資料量最大的 Legal 資料集上表現顯著提升。[S9][S10]  <br>作者指出 LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，較 GraphRAG 大幅降低 token 消耗與成本，同時提升檢索速度與生成品質。[S13][S16] |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。[S4][S5]  <br>在四個大規模領域資料集（Agriculture、CS、Legal、Mix）上，LightRAG 相較於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 在全面性、多樣性等評估維度皆取得更高的勝率，尤其在資料量最大的 Legal 資料集上表現顯著提升。[S9][S10]  <br>作者指出 LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，較 GraphRAG 大幅降低 token 消耗與成本，同時提升檢索速度與生成品質。[S13][S16] |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。[S4][S5]  <br>在四個大規模領域資料集（Agriculture、CS、Legal、Mix）上，LightRAG 相較於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 在全面性、多樣性等評估維度皆取得更高的勝率，尤其在資料量最大的 Legal 資料集上表現顯著提升。[S9][S10]  <br>作者指出 LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，較 GraphRAG 大幅降低 token 消耗與成本，同時提升檢索速度與生成品質。[S13][S16] |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 94 | 600 | 10000 | 792.10 | stop |
| 2 | answer | medium | 5620 | 5395 | 972 | 3000 | 10000 | 5220.49 | stop |
| 3 | judge | low | 1011 | 786 | 108 | 1000 | 10000 | 921.53 | stop |
| 4 | judge | low | 1006 | 781 | 304 | 1000 | 10000 | 1433.34 | stop |
| 5 | judge | low | 1008 | 783 | 345 | 1000 | 10000 | 1524.54 | stop |
| 6 | judge | low | 1014 | 789 | 218 | 1000 | 10000 | 1461.18 | stop |
| 7 | judge | low | 1017 | 792 | 357 | 1000 | 10000 | 1633.84 | stop |
| 8 | judge | low | 1014 | 789 | 276 | 1000 | 10000 | 1593.54 | stop |
| 9 | judge | low | 1021 | 796 | 262 | 1000 | 10000 | 1444.10 | stop |
| 10 | judge | low | 1007 | 782 | 134 | 1000 | 10000 | 1033.44 | stop |
| 11 | judge | low | 1008 | 783 | 421 | 1000 | 10000 | 1710.25 | stop |
| 12 | judge | low | 1017 | 792 | 434 | 1000 | 10000 | 1954.11 | stop |

### Finalized answer

<pre>LightRAG 透過將文件切分成片段、以 LLM 提取實體與關係建立知識圖 (ˆD) 並以圖形結構結合向量表示，實現雙層檢索（低層精確實體、高層概括主題）與增量更新機制，避免完整重建索引。[S4][S5]  
在四個大規模領域資料集（Agriculture、CS、Legal、Mix）上，LightRAG 相較於 NaiveRAG、RQ‑RAG、HyDE 與 GraphRAG 在全面性、多樣性等評估維度皆取得更高的勝率，尤其在資料量最大的 Legal 資料集上表現顯著提升。[S9][S10]  
作者指出 LightRAG 在檢索階段僅使用不到 100 個 token 並只需一次 API 呼叫，較 GraphRAG 大幅降低 token 消耗與成本，同時提升檢索速度與生成品質。[S13][S16]</pre>

## Q1_ZH_THREE_SENTENCES — repetition 3

Question: 用三句話、中文總結這份文件

Question Type: Global; expected: Global

Plan source: router

Fallback reason: None

Rewrite language mismatch: False

Raw Router Standalone Question: None

Standalone Question: 用三句話、中文總結這份文件

Sub-queries: []

Ask latency_ms: 4926.40

Judge latency_ms: 15572.10

Total evaluation latency_ms: 20534.84

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Global; actual Global; plan_source=router; fallback_reason=None |  |
| motivation | judge | FAIL | Required claim not asserted: The answer never mentions flat RAG losing contextual interdependencies or that this motivates LightRAG, so the claim is not present. |  |
| graph_indexing | judge | FAIL | Required claim not asserted: The answer describes LightRAG&#x27;s graph-based text indexing handling entities and relationships, but does not explicitly state that graph-based indexing extracts entities and relationships as claimed in Section 3.1. |  |
| dual_level | judge | PASS | Required claim supported by verbatim evidence | LightRAG 結合圖形化文字索引與雙層檢索框架，能同時處理具體實體關係與抽象主題，並透過增量更新演算法快速整合新資料[S1][S4][S5]。 |
| incremental_update | judge | FAIL | Required claim not asserted: The answer mentions an incremental update algorithm that quickly integrates new data, but it does not explicitly state that this integration occurs without rebuilding the entire index, so the required claim is not fully satisfied. |  |
| experiments | judge | FAIL | Required claim not asserted: The answer mentions superiority on four large domains and highlights Legal, but does not explicitly reference Agriculture, CS, or Mix as required by the claim. |  |
| not_all_best | forbidden | PASS | No asserted forbidden claim |  |
| not_all_datasets | forbidden | FAIL | Forbidden claim asserted | 在四個大規模領域資料集上的實驗顯示，LightRAG 在勝率與多樣性指標上均優於 NaiveRAG、HyDE、RQ‑RAG 與 GraphRAG，尤其在規模最大的 Legal 資料集上表現最為突出[S10]。 |
| conclusion | judge | FAIL | Required claim not asserted: The answer describes LightRAG&#x27;s graph-based retrieval and adaptability but does not reference Section 6 or state that this is the conclusion combining those aspects. |  |
| chinese_summary | judge | PASS | Required claim supported by verbatim evidence | LightRAG 結合圖形化文字索引與雙層檢索框架，能同時處理具體實體關係與抽象主題，並透過增量更新演算法快速整合新資料[S1][S4][S5]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在勝率與多樣性指標上均優於 NaiveRAG、HyDE、RQ‑RAG 與 GraphRAG，尤其在規模最大的 Legal 資料集上表現最為突出[S10]。  <br>相較於 GraphRAG，LightRAG 在檢索階段的 token 使用量與 API 呼叫次數皆顯著降低，證明其在計算成本與資料變更適應性上具備明顯優勢[S13][S16]。 |
| three_sentences | judge | PASS | Required claim supported by verbatim evidence | LightRAG 結合圖形化文字索引與雙層檢索框架，能同時處理具體實體關係與抽象主題，並透過增量更新演算法快速整合新資料[S1][S4][S5]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在勝率與多樣性指標上均優於 NaiveRAG、HyDE、RQ‑RAG 與 GraphRAG，尤其在規模最大的 Legal 資料集上表現最為突出[S10]。  <br>相較於 GraphRAG，LightRAG 在檢索階段的 token 使用量與 API 呼叫次數皆顯著降低，證明其在計算成本與資料變更適應性上具備明顯優勢[S13][S16]。 |
| answer_script | property | PASS | Question script=Traditional; no opposing forms found (shared forms inconclusive) | LightRAG 結合圖形化文字索引與雙層檢索框架，能同時處理具體實體關係與抽象主題，並透過增量更新演算法快速整合新資料[S1][S4][S5]。  <br>在四個大規模領域資料集上的實驗顯示，LightRAG 在勝率與多樣性指標上均優於 NaiveRAG、HyDE、RQ‑RAG 與 GraphRAG，尤其在規模最大的 Legal 資料集上表現最為突出[S10]。  <br>相較於 GraphRAG，LightRAG 在檢索階段的 token 使用量與 API 呼叫次數皆顯著降低，證明其在計算成本與資料變更適應性上具備明顯優勢[S13][S16]。 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | router | low | 840 | 501 | 93 | 600 | 10000 | 758.84 | stop |
| 2 | answer | medium | 5620 | 5395 | 529 | 3000 | 10000 | 4152.93 | stop |
| 3 | judge | low | 971 | 746 | 127 | 1000 | 10000 | 998.45 | stop |
| 4 | judge | low | 966 | 741 | 233 | 1000 | 10000 | 1979.32 | stop |
| 5 | judge | low | 968 | 743 | 226 | 1000 | 10000 | 1126.67 | stop |
| 6 | judge | low | 974 | 749 | 287 | 1000 | 10000 | 1617.02 | stop |
| 7 | judge | low | 977 | 752 | 245 | 1000 | 10000 | 1513.71 | stop |
| 8 | judge | low | 974 | 749 | 252 | 1000 | 10000 | 1407.39 | stop |
| 9 | judge | low | 981 | 756 | 293 | 1000 | 10000 | 1456.27 | stop |
| 10 | judge | low | 967 | 742 | 306 | 1000 | 10000 | 1903.12 | stop |
| 11 | judge | low | 968 | 743 | 346 | 1000 | 10000 | 1424.53 | stop |
| 12 | judge | low | 977 | 752 | 375 | 1000 | 10000 | 2145.62 | stop |

### Finalized answer

<pre>LightRAG 結合圖形化文字索引與雙層檢索框架，能同時處理具體實體關係與抽象主題，並透過增量更新演算法快速整合新資料[S1][S4][S5]。  
在四個大規模領域資料集上的實驗顯示，LightRAG 在勝率與多樣性指標上均優於 NaiveRAG、HyDE、RQ‑RAG 與 GraphRAG，尤其在規模最大的 Legal 資料集上表現最為突出[S10]。  
相較於 GraphRAG，LightRAG 在檢索階段的 token 使用量與 API 呼叫次數皆顯著降低，證明其在計算成本與資料變更適應性上具備明顯優勢[S13][S16]。</pre>
