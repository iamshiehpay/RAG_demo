# Held-out Table 1 reading measurement

Created: 2026-10-12T20:29:47.087751+00:00

Revision: `d6a075e67a6ae48379aa1db6929518e56ac8c4b7`; uncommitted changes: no

Same Application/Gateway session as the authorized follow-up Q3 N=3 evaluation.
Question selected outside Golden Facts. No reference answer or numeric hints supplied.

Question: In Table 1's Legal dataset, compare HyDE and LightRAG on Diversity and Empowerment. State both win rates for each metric.

## Finalized answer

**Legal dataset – HyDE vs. LightRAG**

- **Diversity** – HyDE wins 20.0 % of the time, while LightRAG wins 80.0 % [C2].
- **Empowerment** – HyDE wins 26.0 % of the time, while LightRAG wins 74.0 % [C2].

## Plan, Trace, Citations and original sources

```json
{
  "question": "In Table 1's Legal dataset, compare HyDE and LightRAG on Diversity and Empowerment. State both win rates for each metric.",
  "answer": "**Legal dataset – HyDE vs. LightRAG**\n\n- **Diversity** – HyDE wins 20.0 % of the time, while LightRAG wins 80.0 % [C2].\n- **Empowerment** – HyDE wins 26.0 % of the time, while LightRAG wins 74.0 % [C2].",
  "plan": {
    "type": "plan",
    "question_type": "Synthesis",
    "standalone_question": "In Table 1's Legal dataset, compare HyDE and LightRAG on Diversity and Empowerment, stating both win rates for each metric.",
    "sub_queries": [
      "HyDE vs LightRAG Diversity win rate",
      "HyDE vs LightRAG Empowerment win rate"
    ],
    "plan_source": "router",
    "fallback_reason": null,
    "rewrite_language_mismatch": false,
    "router_standalone_question": null
  },
  "trace": {
    "type": "trace",
    "calls": [
      {
        "call_type": "router",
        "estimated_prompt_tokens": 844,
        "prompt_eval_count": 505,
        "eval_count": 121,
        "think": "low",
        "num_predict": 600,
        "context_budget": 10000,
        "safety_margin": 300,
        "thinking": "We need to output JSON. It's a Synthesis? Comparing across table, but single table maybe Lookup? It's comparing two systems across two metrics, that's synthesis across sections. Use Synthesis. Provide sub_queries 2-3.",
        "latency_ms": 1483.8015001732856,
        "done_reason": "stop",
        "discarded_fact_lines": 0,
        "plan_source": "router",
        "fallback_reason": null,
        "rewrite_language_mismatch": false,
        "router_standalone_question": null
      },
      {
        "call_type": "answer",
        "estimated_prompt_tokens": 5192,
        "prompt_eval_count": 4967,
        "eval_count": 216,
        "think": "medium",
        "num_predict": 3000,
        "context_budget": 10000,
        "safety_margin": 300,
        "thinking": "We need to answer using only supplied excerpts. Table 1 is in C2. For HyDE / LightRAG rows, we need win rates for Legal dataset for Diversity and Empowerment. In C2, HyDE / LightRAG | Diversity: Legal / Diversity: 20.0% / 80.0% . Empowerment: Legal / Empowerment: 26.0% / 74.0% . So we need to state both win rates for each metric. Provide both baseline (HyDE) win rate and LightRAG win rate. Cite C2. Use proper citation format.",
        "latency_ms": 1152.4681670125574,
        "done_reason": "stop",
        "discarded_fact_lines": 0,
        "plan_source": null,
        "fallback_reason": null,
        "rewrite_language_mismatch": false,
        "router_standalone_question": null
      }
    ],
    "invalid_citation_count": 0,
    "dropped_chunk_count": 0
  },
  "citations": [
    {
      "id": "C2",
      "source_id": "1b89f46975b740668688943c780fd726:chunk-20",
      "section": "4.2 COMPARISON OF LIGHTRAG WITH EXISTING RAG METHODS (RQ1)",
      "page_start": 7,
      "page_end": 7
    }
  ],
  "sources": {
    "C2": {
      "id": "1b89f46975b740668688943c780fd726:chunk-20",
      "section_id": "section-12",
      "section": "4.2 COMPARISON OF LIGHTRAG WITH EXISTING RAG METHODS (RQ1)",
      "page_start": 7,
      "page_end": 7,
      "text": "Table 1: Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.\nEach cell is baseline win rate / candidate win rate (%); the Comparison column names both systems in that order.\nComparison | Metric | Agriculture (baseline / variant win rate %) | CS (baseline / variant win rate %) | Legal (baseline / variant win rate %) | Mix (baseline / variant win rate %)\nNaiveRAG / LightRAG | Comprehensiveness | Agriculture / Comprehensiveness: 32.4% / 67.6% | CS / Comprehensiveness: 38.4% / 61.6% | Legal / Comprehensiveness: 16.4% / 83.6% | Mix / Comprehensiveness: 38.8% / 61.2%\nNaiveRAG / LightRAG | Diversity | Agriculture / Diversity: 23.6% / 76.4% | CS / Diversity: 38.0% / 62.0% | Legal / Diversity: 13.6% / 86.4% | Mix / Diversity: 32.4% / 67.6%\nNaiveRAG / LightRAG | Empowerment | Agriculture / Empowerment: 32.4% / 67.6% | CS / Empowerment: 38.8% / 61.2% | Legal / Empowerment: 16.4% / 83.6% | Mix / Empowerment: 42.8% / 57.2%\nNaiveRAG / LightRAG | Overall | Agriculture / Overall: 32.4% / 67.6% | CS / Overall: 38.8% / 61.2% | Legal / Overall: 15.2% / 84.8% | Mix / Overall: 40.0% / 60.0%\nRQ-RAG / LightRAG | Comprehensiveness | Agriculture / Comprehensiveness: 31.6% / 68.4% | CS / Comprehensiveness: 38.8% / 61.2% | Legal / Comprehensiveness: 15.2% / 84.8% | Mix / Comprehensiveness: 39.2% / 60.8%\nRQ-RAG / LightRAG | Diversity | Agriculture / Diversity: 29.2% / 70.8% | CS / Diversity: 39.2% / 60.8% | Legal / Diversity: 11.6% / 88.4% | Mix / Diversity: 30.8% / 69.2%\nRQ-RAG / LightRAG | Empowerment | Agriculture / Empowerment: 31.6% / 68.4% | CS / Empowerment: 36.4% / 63.6% | Legal / Empowerment: 15.2% / 84.8% | Mix / Empowerment: 42.4% / 57.6%\nRQ-RAG / LightRAG | Overall | Agriculture / Overall: 32.4% / 67.6% | CS / Overall: 38.0% / 62.0% | Legal / Overall: 14.4% / 85.6% | Mix / Overall: 40.0% / 60.0%\nHyDE / LightRAG | Comprehensiveness | Agriculture / Comprehensiveness: 26.0% / 74.0% | CS / Comprehensiveness: 41.6% / 58.4% | Legal / Comprehensiveness: 26.8% / 73.2% | Mix / Comprehensiveness: 40.4% / 59.6%\nHyDE / LightRAG | Diversity | Agriculture / Diversity: 24.0% / 76.0% | CS / Diversity: 38.8% / 61.2% | Legal / Diversity: 20.0% / 80.0% | Mix / Diversity: 32.4% / 67.6%\nHyDE / LightRAG | Empowerment | Agriculture / Empowerment: 25.2% / 74.8% | CS / Empowerment: 40.8% / 59.2% | Legal / Empowerment: 26.0% / 74.0% | Mix / Empowerment: 46.0% / 54.0%\nHyDE / LightRAG | Overall | Agriculture / Overall: 24.8% / 75.2% | CS / Overall: 41.6% / 58.4% | Legal / Overall: 26.4% / 73.6% | Mix / Overall: 42.4% / 57.6%\nGraphRAG / LightRAG | Comprehensiveness | Agriculture / Comprehensiveness: 45.6% / 54.4% | CS / Comprehensiveness: 48.4% / 51.6% | Legal / Comprehensiveness: 48.4% / 51.6% | Mix / Comprehensiveness: 50.4% / 49.6%\nGraphRAG / LightRAG | Diversity | Agriculture / Diversity: 22.8% / 77.2% | CS / Diversity: 40.8% / 59.2% | Legal / Diversity: 26.4% / 73.6% | Mix / Diversity: 36.0% / 64.0%\nGraphRAG / LightRAG | Empowerment | Agriculture / Empowerment: 41.2% / 58.8% | CS / Empowerment: 45.2% / 54.8% | Legal / Empowerment: 43.6% / 56.4% | Mix / Empowerment: 50.8% / 49.2%\nGraphRAG / LightRAG | Overall | Agriculture / Overall: 45.2% / 54.8% | CS / Overall: 48.0% / 52.0% | Legal / Overall: 47.2% / 52.8% | Mix / Overall: 50.4% / 49.6%",
      "order": 19,
      "kind": "table",
      "table_label": "Table 1",
      "table_caption": "Table 1: Win rates (%) of baselines v.s. LightRAG across four datasets and four evaluation dimensions.",
      "table_meaning": "Each cell is baseline win rate / candidate win rate (%); the Comparison column names both systems in that order.",
      "table_headers": [
        "Comparison",
        "Metric",
        "Agriculture (baseline / variant win rate %)",
        "CS (baseline / variant win rate %)",
        "Legal (baseline / variant win rate %)",
        "Mix (baseline / variant win rate %)"
      ],
      "table_rows": [
        [
          "NaiveRAG / LightRAG",
          "Comprehensiveness",
          "32.4% / 67.6%",
          "38.4% / 61.6%",
          "16.4% / 83.6%",
          "38.8% / 61.2%"
        ],
        [
          "NaiveRAG / LightRAG",
          "Diversity",
          "23.6% / 76.4%",
          "38.0% / 62.0%",
          "13.6% / 86.4%",
          "32.4% / 67.6%"
        ],
        [
          "NaiveRAG / LightRAG",
          "Empowerment",
          "32.4% / 67.6%",
          "38.8% / 61.2%",
          "16.4% / 83.6%",
          "42.8% / 57.2%"
        ],
        [
          "NaiveRAG / LightRAG",
          "Overall",
          "32.4% / 67.6%",
          "38.8% / 61.2%",
          "15.2% / 84.8%",
          "40.0% / 60.0%"
        ],
        [
          "RQ-RAG / LightRAG",
          "Comprehensiveness",
          "31.6% / 68.4%",
          "38.8% / 61.2%",
          "15.2% / 84.8%",
          "39.2% / 60.8%"
        ],
        [
          "RQ-RAG / LightRAG",
          "Diversity",
          "29.2% / 70.8%",
          "39.2% / 60.8%",
          "11.6% / 88.4%",
          "30.8% / 69.2%"
        ],
        [
          "RQ-RAG / LightRAG",
          "Empowerment",
          "31.6% / 68.4%",
          "36.4% / 63.6%",
          "15.2% / 84.8%",
          "42.4% / 57.6%"
        ],
        [
          "RQ-RAG / LightRAG",
          "Overall",
          "32.4% / 67.6%",
          "38.0% / 62.0%",
          "14.4% / 85.6%",
          "40.0% / 60.0%"
        ],
        [
          "HyDE / LightRAG",
          "Comprehensiveness",
          "26.0% / 74.0%",
          "41.6% / 58.4%",
          "26.8% / 73.2%",
          "40.4% / 59.6%"
        ],
        [
          "HyDE / LightRAG",
          "Diversity",
          "24.0% / 76.0%",
          "38.8% / 61.2%",
          "20.0% / 80.0%",
          "32.4% / 67.6%"
        ],
        [
          "HyDE / LightRAG",
          "Empowerment",
          "25.2% / 74.8%",
          "40.8% / 59.2%",
          "26.0% / 74.0%",
          "46.0% / 54.0%"
        ],
        [
          "HyDE / LightRAG",
          "Overall",
          "24.8% / 75.2%",
          "41.6% / 58.4%",
          "26.4% / 73.6%",
          "42.4% / 57.6%"
        ],
        [
          "GraphRAG / LightRAG",
          "Comprehensiveness",
          "45.6% / 54.4%",
          "48.4% / 51.6%",
          "48.4% / 51.6%",
          "50.4% / 49.6%"
        ],
        [
          "GraphRAG / LightRAG",
          "Diversity",
          "22.8% / 77.2%",
          "40.8% / 59.2%",
          "26.4% / 73.6%",
          "36.0% / 64.0%"
        ],
        [
          "GraphRAG / LightRAG",
          "Empowerment",
          "41.2% / 58.8%",
          "45.2% / 54.8%",
          "43.6% / 56.4%",
          "50.8% / 49.2%"
        ],
        [
          "GraphRAG / LightRAG",
          "Overall",
          "45.2% / 54.8%",
          "48.0% / 52.0%",
          "47.2% / 52.8%",
          "50.4% / 49.6%"
        ]
      ],
      "table_reconstructed": true,
      "linked_chunk_ids": [
        "1b89f46975b740668688943c780fd726:chunk-19"
      ]
    }
  },
  "errors": []
}
```
