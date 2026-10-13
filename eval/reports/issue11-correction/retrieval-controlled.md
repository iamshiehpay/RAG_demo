# Public-event retrieval experiment

Public upload/ask PlanEvent and RetrievalEvent. Controlled replay uses saved native Router plans and scripted non-evaluated answers/extraction at the external adapter. Real cached PDF Chunks/vectors and local embeddings; zero native replay calls. Original source-order hits are separate from score-sorted returned-hit diagnostics; returned-hit RR is NOT full-index MRR or end-to-end answer quality. Old Summary Trees are not final-cache evidence.

| Chunk | Lookup/Synthesis/Sub k | BM25 | Returned-hit RR mean | Coverage |
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

Selected settings: `{"lookup_top_k": 5, "synthesis_top_k": 3, "sub_query_top_k": 2, "chunk_token_target": 500, "answer_think": "medium", "bm25_weight": 0.0, "summary_concurrency": 4}`

Raw public events/ordering/plans/provenance: `retrieval-controlled.json`.

This scripted retrieval-only replay does not establish native answer quality, global full-index MRR, final cache identity or universal grounding.
