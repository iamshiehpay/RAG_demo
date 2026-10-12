"""Does the router (Question Type + standalone question + sub-queries) need more thinking?

Runs the same router prompt over labelled questions at each `think` level and
reports accuracy, latency, and generated tokens (thinking + answer).

Run: python3 spikes/think_level_probe.py
"""

import json
import time
import urllib.request

MODEL = "gpt-oss:120b-cloud"
LEVELS = [False, "low", "medium", "high"]
NUM_PREDICT = 2000

SYSTEM = """You plan how to answer a question about ONE uploaded document.
Classify the question into exactly one question_type:
- Global: needs the whole document at once (summary, main idea, key takeaways).
- Synthesis: needs facts gathered from several sections (comparisons, pros/cons, limitations, how evidence supports claims).
- Lookup: answerable from one place (a specific fact, number, table, definition).
Rewrite the question into a standalone_question that is understandable without the chat history.
For Synthesis, give 2-5 sub_queries that together cover the question; otherwise sub_queries is [].
Reply with JSON only: {"question_type": ..., "standalone_question": ..., "sub_queries": [...]}"""

SCHEMA = {
    "type": "object",
    "properties": {
        "question_type": {"type": "string", "enum": ["Global", "Synthesis", "Lookup"]},
        "standalone_question": {"type": "string"},
        "sub_queries": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["question_type", "standalone_question", "sub_queries"],
}

CASES = [
    ([], "Summary this document.", "Global"),
    ([], "這篇在講什麼？", "Global"),
    ([], "Give me the key takeaways of this paper.", "Global"),
    ([], "Compare LightRAG with GraphRAG.", "Synthesis"),
    ([], "LightRAG 有什麼限制？", "Synthesis"),
    ([], "How do the experiments support the paper's claims?", "Synthesis"),
    ([], "Performance of ablated versions of LightRAG.", "Lookup"),
    ([], "What datasets were used?", "Lookup"),
    ([], "Table 2 裡 -Origin 在 Mix 的 Overall 是多少？", "Lookup"),
    ([], "How many API calls does LightRAG need for retrieval?", "Lookup"),
    (
        [("user", "What is GraphRAG's retrieval cost in the paper?"),
         ("assistant", "GraphRAG needs about 610 x 1,000 tokens per retrieval because it traverses communities.")],
        "那 LightRAG 呢？",
        "Lookup",
    ),
    (
        [("user", "Summary this document."),
         ("assistant", "LightRAG is a graph-based RAG system with dual-level retrieval and incremental updates...")],
        "那它跟 GraphRAG 比呢？",
        "Synthesis",
    ),
]


def chat(history, question, think):
    messages = [{"role": "system", "content": SYSTEM}]
    messages += [{"role": r, "content": c} for r, c in history]
    messages.append({"role": "user", "content": question})
    payload = {"model": MODEL, "messages": messages, "stream": False, "think": think,
               "format": SCHEMA, "options": {"num_predict": NUM_PREDICT, "temperature": 0}}
    req = urllib.request.Request("http://localhost:11434/api/chat", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r, time.time() - t0


def main():
    for think in LEVELS:
        correct = parsed = 0
        lat, gen, think_chars = [], [], []
        misses = []
        for history, q, expected in CASES:
            r, dt = chat(history, q, think)
            lat.append(dt)
            gen.append(r.get("eval_count", 0))
            think_chars.append(len(r["message"].get("thinking") or ""))
            try:
                plan = json.loads(r["message"]["content"])
                parsed += 1
            except json.JSONDecodeError:
                misses.append(f"{q} -> unparseable ({r.get('done_reason')})")
                continue
            if plan["question_type"] == expected:
                correct += 1
            else:
                misses.append(f"{q} -> {plan['question_type']} (expected {expected})")
            if history:
                misses.append(f"  rewrite[{q}] = {plan['standalone_question']}")
        n = len(CASES)
        print(f"\nthink={think!s:<7} accuracy={correct}/{n} parsed={parsed}/{n} "
              f"latency avg={sum(lat)/n:.1f}s max={max(lat):.1f}s  "
              f"generated tokens avg={sum(gen)/n:.0f} max={max(gen)}  thinking chars avg={sum(think_chars)/n:.0f}")
        for m in misses:
            print("   ", m)


if __name__ == "__main__":
    main()
