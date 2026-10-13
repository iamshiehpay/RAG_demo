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
| 500 | 3/3/2 | 0.0 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 5/3/2 | 0.0 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 7/5/3 | 0.0 | 1.000 | {'table2': True, 'cost': False, 'update': True} |
| 500 | 3/3/2 | 0.1 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 5/3/2 | 0.1 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 7/5/3 | 0.1 | 1.000 | {'table2': True, 'cost': False, 'update': True} |
| 500 | 3/3/2 | 0.25 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 5/3/2 | 0.25 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 7/5/3 | 0.25 | 1.000 | {'table2': True, 'cost': False, 'update': True} |
| 500 | 3/3/2 | 0.5 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
| 500 | 5/3/2 | 0.5 | 1.000 | {'table2': True, 'cost': False, 'update': False} |
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

Selected effective settings: `{"lookup_top_k": 5, "synthesis_top_k": 3, "sub_query_top_k": 2, "chunk_token_target": 800, "answer_think": "medium", "bm25_weight": 0.0, "summary_concurrency": 4}`

These are retrieval measurements, not Golden Facts answer acceptance. Raw plans/settings/provenance are in retrieval.json.
