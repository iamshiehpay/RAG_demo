"""How much does gpt-oss think when generating a real answer, per think level?

Builds Q2/Q3-sized contexts from the paper, gives each call the largest
num_predict the 10K Context Budget allows, and records thinking vs answer
tokens, latency, and whether Golden Facts appear in the answer.

Run: uv run --python 3.12 --with pymupdf --with tiktoken python spikes/answer_think_probe.py
"""

import json
import re
import time
import urllib.request

import pymupdf
import tiktoken

MODEL = "gpt-oss:120b-cloud"
BUDGET = 10_000
TEMPLATE_OVERHEAD = 300
LEVELS = ["low", "medium", "high"]
RUNS = 2
enc = tiktoken.get_encoding("o200k_harmony")
doc = pymupdf.open("data/lightrag.pdf")

SYSTEM = """You answer questions about a document using ONLY the context below.
Cite pages like [p.8]. If the context does not contain the answer, say so.
Be precise with numbers and do not add facts from outside the context."""


def table2_markdown():
    """Rebuild Table 2 from its one-cell-per-line text (spike-only, table-specific)."""
    lines = [l.strip() for l in doc[7].get_text().split("Table 2:")[1].splitlines()[1:]]
    datasets, i = lines[:4], 4
    rows = []
    while i < len(lines) and lines[i] == "NaiveRAG":
        variant = lines[i + 1]
        i += 8
        for _ in range(4):
            metric, vals = lines[i], lines[i + 1:i + 9]
            i += 9
            cells = [f"{vals[k*2]} / {vals[k*2+1]}" for k in range(4)]
            rows.append(f"| {variant} | {metric} | " + " | ".join(cells) + " |")
    head = ("Table 2: Performance of ablated versions of LightRAG, using NaiveRAG as reference. "
            "Each cell is win rate NaiveRAG / variant.\n"
            "| Variant | Metric | " + " | ".join(datasets) + " |\n|---|---|" + "---|" * 4)
    rest = doc[7].get_text()[doc[7].get_text().find("• Low-level-only"):]
    return head + "\n" + "\n".join(rows) + "\n\n" + rest


def page(n):
    return f"[p.{n}]\n" + doc[n - 1].get_text()


p7 = doc[6].get_text()
CASES = {
    "Q3": {
        "question": "Performance of ablated versions of LightRAG.",
        "context": "[p.7]\n" + p7[p7.find("4.3"):] + "\n[p.8]\n" + table2_markdown(),
        "facts": {"-High": r"-High", "-Low": r"-Low", "-Origin": r"-Origin",
                  "Mix -Low 64.8 > 60.0": r"64\.8", "Agri -Origin 74.4": r"74\.4"},
    },
    "Q2": {
        "question": "Compare LightRAG with GraphRAG.",
        "context": "\n".join(page(n) for n in (1, 5, 6, 7, 9)),
        "facts": {"cost 610": r"610", "incremental": r"(?i)incremental", "community": r"(?i)communit",
                  "API calls": r"(?i)API call", "win rate %": r"\d\d\.\d%"},
    },
}


def chat(question, context, think):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}]
    prompt_est = sum(len(enc.encode(m["content"])) for m in messages) + TEMPLATE_OVERHEAD
    num_predict = BUDGET - prompt_est
    payload = {"model": MODEL, "messages": messages, "stream": False, "think": think,
               "options": {"num_predict": num_predict, "temperature": 0}}
    req = urllib.request.Request("http://localhost:11434/api/chat", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=600))
    return r, time.time() - t0, prompt_est, num_predict


def main():
    for name, case in CASES.items():
        print(f"\n=== {name}: {case['question']}")
        for think in LEVELS:
            for run in range(RUNS):
                r, dt, est, cap = chat(case["question"], case["context"], think)
                answer = r["message"]["content"]
                thinking = r["message"].get("thinking") or ""
                t_tok, a_tok = len(enc.encode(thinking)), len(enc.encode(answer))
                hits = [f for f, pat in case["facts"].items() if re.search(pat, answer)]
                print(f"think={think:<6} run{run+1} {dt:5.1f}s prompt est={est} reported={r.get('prompt_eval_count')} "
                      f"cap={cap} | thinking≈{t_tok} answer≈{a_tok} eval={r.get('eval_count')} "
                      f"done={r.get('done_reason')} | facts {len(hits)}/{len(case['facts'])} "
                      f"missing={[f for f in case['facts'] if f not in hits]}")
                with open(f"spikes/out/{name}_{think}_{run+1}.md", "w") as fh:
                    fh.write(f"# {name} think={think} run{run+1}\n\n## thinking\n{thinking}\n\n## answer\n{answer}\n")


if __name__ == "__main__":
    main()
