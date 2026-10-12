# Q3 think=low run1

## thinking
We need to answer using context. Provide summary of performance from Table.

## answer
**Ablated versions of LightRAG (compared to the full LightRAG model)**  

| Ablated Variant | How it differs from full LightRAG | Overall win‑rate vs. NaiveRAG (overall metric) |
|-----------------|-----------------------------------|-----------------------------------------------|
| **‑High** (removes the high‑level retrieval module) | Keeps only low‑level (entity‑centric) retrieval | 35.2 % / 64.8 % (wins / losses) |
| **‑Low** (removes the low‑level retrieval module) | Keeps only high‑level (broader, entity‑wise) retrieval | 34.8 % / 65.2 % |
| **‑Origin** (removes the original‑text source, using only the graph‑based index) | No original text is used in retrieval | 25.6 % / 74.4 % |

**Key observations from the ablation study (p.7‑p.8):**

* Removing **high‑level** retrieval (‑High) causes a noticeable drop in performance across almost all datasets and metrics, because the system then focuses too narrowly on specific entities and their immediate neighbors, limiting its ability to answer complex queries that need broader context.  
* Removing **low‑level** retrieval (‑Low) improves **comprehensiveness** (the system gathers more varied information) but reduces depth on specific entities, which can hurt detailed answers.  
* The **‑Origin** variant, which relies solely on the semantic graph and discards the original text, does **not** suffer major performance losses; in some datasets (e.g., Agriculture and Mix) it even shows slight improvements, suggesting that the graph‑based indexing captures the essential information while filtering out noisy text.  

Overall, the full **LightRAG** hybrid mode (combining both low‑ and high‑level retrieval) achieves the most balanced and highest performance across the four test domains (Agriculture, Computer Science, Legal, Mix).
