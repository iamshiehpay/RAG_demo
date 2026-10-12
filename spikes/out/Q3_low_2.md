# Q3 think=low run2

## thinking
We need to summarize performance from Table. Provide win rates.

## answer
**Ablated versions of LightRAG (win‑rate of NaiveRAG / variant)**  

| Variant | Metric | Agriculture | Computer‑Science (CS) | Legal | Mix |
|---|---|---|---|---|---|
| **LightRAG (full)** | Comprehensiveness | 32.4 % / 67.6 % | 38.4 % / 61.6 % | 16.4 % / 83.6 % | 38.8 % / 61.2 % |
|  | Diversity | 23.6 % / 76.4 % | 38.0 % / 62.0 % | 13.6 % / 86.4 % | 32.4 % / 67.6 % |
|  | Empowerment | 32.4 % / 67.6 % | 38.8 % / 61.2 % | 16.4 % / 83.6 % | 42.8 % / 57.2 % |
|  | Overall | 32.4 % / 67.6 % | 38.8 % / 61.2 % | 15.2 % / 84.8 % | 40.0 % / 60.0 % |
| **‑High** (no high‑level retrieval) | Comprehensiveness | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 23.6 % / 76.4 % | 40.4 % / 59.6 % |
|  | Diversity | 27.2 % / 72.8 % | 36.8 % / 63.2 % | 16.8 % / 83.2 % | 36.0 % / 64.0 % |
|  | Empowerment | 36.0 % / 64.0 % | 42.4 % / 57.6 % | 22.8 % / 77.2 % | 47.6 % / 52.4 % |
|  | Overall | 35.2 % / 64.8 % | 44.0 % / 56.0 % | 22.0 % / 78.0 % | 42.4 % / 57.6 % |
| **‑Low** (no low‑level retrieval) | Comprehensiveness | 36.0 % / 64.0 % | 43.2 % / 56.8 % | 19.2 % / 80.8 % | 36.0 % / 64.0 % |
|  | Diversity | 28.0 % / 72.0 % | 39.6 % / 60.4 % | 13.6 % / 86.4 % | 33.2 % / 66.8 % |
|  | Empowerment | 34.8 % / 65.2 % | 42.8 % / 57.2 % | 16.4 % / 83.6 % | 35.2 % / 64.8 % |
|  | Overall | 34.8 % / 65.2 % | 43.6 % / 56.4 % | 18.8 % / 81.2 % | 35.2 % / 64.8 % |
| **‑Origin** (no original‑text retrieval) | Comprehensiveness | 24.8 % / 75.2 % | 39.2 % / 60.8 % | 16.4 % / 83.6 % | 44.4 % / 55.6 % |
|  | Diversity | 26.4 % / 73.6 % | 44.8 % / 55.2 % | 14.4 % / 85.6 % | 25.6 % / 74.4 % |
|  | Empowerment | 32.0 % / 68.0 % | 43.2 % / 56.8 % | 17.2 % / 82.8 % | 45.2 % / 54.8 % |
|  | Overall | 25.6 % / 74.4 % | 39.2 % / 60.8 % | 15.6 % / 84.4 % | 44.4 % / 55.6 % |

**Key observations (from the text):**  

* Removing the high‑level module (‑High) causes a noticeable drop in performance across most datasets and metrics, especially in comprehensiveness and overall quality.  
* Removing the low‑level module (‑Low) improves comprehensiveness but reduces depth, leading to lower overall scores.  
* The hybrid (full) LightRAG balances breadth and depth, achieving the most balanced performance.  
* Excluding the original text (‑Origin) does **not** cause major degradation; in some cases (Agriculture, Mix) it even improves results, indicating the graph‑based indexing supplies sufficient context while avoiding noisy text.  

All figures are taken directly from Table 2 in the provided context【p.8】.
