# Issue11 retrieval experiment

Maximize actual Router evidence coverage, then MRR; ties prefer dense and documented defaults.

| Chunk | Lookup/Synthesis/Sub-query k | BM25 | MRR | Context coverage |
|---|---|---|---|---|
| 256 | 3/3/2 | 0.0 | 0.833 | {'table2': True, 'cost': False, 'update': False} |
| 256 | 5/3/2 | 0.0 | 0.833 | {'table2': True, 'cost': False, 'update': False} |
| 256 | 7/5/3 | 0.0 | 0.833 | {'table2': True, 'cost': False, 'update': True} |
| 256 | 3/3/2 | 0.1 | 0.833 | {'table2': True, 'cost': False, 'update': False} |
| 256 | 5/3/2 | 0.1 | 0.833 | {'table2': True, 'cost': False, 'update': False} |
| 256 | 7/5/3 | 0.1 | 0.833 | {'table2': True, 'cost': False, 'update': True} |
| 256 | 3/3/2 | 0.25 | 0.833 | {'table2': True, 'cost': False, 'update': False} |
| 256 | 5/3/2 | 0.25 | 0.833 | {'table2': True, 'cost': False, 'update': False} |
| 256 | 7/5/3 | 0.25 | 0.833 | {'table2': True, 'cost': False, 'update': True} |
| 256 | 3/3/2 | 0.5 | 0.667 | {'table2': True, 'cost': True, 'update': True} |
| 256 | 5/3/2 | 0.5 | 0.667 | {'table2': True, 'cost': True, 'update': True} |
| 256 | 7/5/3 | 0.5 | 0.667 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 3/3/2 | 0.0 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 5/3/2 | 0.0 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 7/5/3 | 0.0 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 3/3/2 | 0.1 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 5/3/2 | 0.1 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 7/5/3 | 0.1 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 3/3/2 | 0.25 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 5/3/2 | 0.25 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 7/5/3 | 0.25 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 3/3/2 | 0.5 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 5/3/2 | 0.5 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 500 | 7/5/3 | 0.5 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 3/3/2 | 0.0 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 5/3/2 | 0.0 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 7/5/3 | 0.0 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 3/3/2 | 0.1 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 5/3/2 | 0.1 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 7/5/3 | 0.1 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 3/3/2 | 0.25 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 5/3/2 | 0.25 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 7/5/3 | 0.25 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 3/3/2 | 0.5 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 5/3/2 | 0.5 | 1.000 | {'table2': True, 'cost': True, 'update': True} |
| 800 | 7/5/3 | 0.5 | 1.000 | {'table2': True, 'cost': True, 'update': True} |

Selected effective settings: `{"lookup_top_k": 5, "synthesis_top_k": 3, "sub_query_top_k": 2, "chunk_token_target": 500, "answer_think": "medium", "bm25_weight": 0.0, "summary_concurrency": 4}`

These are retrieval measurements, not Golden Facts answer acceptance. Raw controlled plans/settings/provenance are in retrieval-controlled.json. This historical matrix used internal ranking seams; the corrected public-event experiment is recorded separately.

Fixed actual Router plan pair across all configurations; reuse measured original Chunks/vectors because parser/chunker/embedder and explicit Chunk targets are unchanged. Old Summary Trees are not final-cache evidence.
Ingestion version: ingest-v2-d6cc86232977edb2c4cd1a1e6fd3deb5755d2b0e85e3a858d999fd23b1e62058
