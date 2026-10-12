"""Compare local Ollama embedding models on the LightRAG paper.

For each query we know which chunks answer it (by marker substrings) and
report the rank of the first relevant chunk. Chunking is a crude
page/paragraph packer, not the real chunker.

Run: uv run --python 3.12 --with pymupdf --with tiktoken --with numpy --with rank-bm25 python spikes/embedding_bakeoff.py
"""

import json
import re
import time
import urllib.request

import numpy as np
import pymupdf
import tiktoken
from rank_bm25 import BM25Okapi

PDF = "data/lightrag.pdf"
CHUNK_TOKENS = 350
enc = tiktoken.get_encoding("o200k_harmony")

QUERIES = [
    # (query, any-of markers that make a chunk relevant)
    ("Performance of ablated versions of LightRAG", ["ablated versions", "-Origin"]),
    ("LightRAG 消融實驗的表現如何？", ["ablated versions", "-Origin"]),
    ("移除高層檢索或原始文本後，LightRAG 效果有什麼變化？", ["ablated versions", "-Origin", "Low-level-only Retrieval"]),
    ("How much cheaper is LightRAG than GraphRAG at retrieval time?", ["610"]),
    ("LightRAG 和 GraphRAG 的檢索成本差多少？", ["610"]),
    ("How does LightRAG handle incremental updates to the knowledge base?", ["Incremental Knowledge Base"]),
    ("新資料加入時，LightRAG 需要重建整個索引嗎？", ["Incremental Knowledge Base"]),
    ("Which datasets were used in the evaluation?", ["UltraDomain"]),
    ("評估用了哪些資料集？", ["UltraDomain"]),
    ("What is dual-level retrieval?", ["Dual-level Retrieval Paradigm", "low-level retrieval"]),
    ("LightRAG 的雙層檢索是什麼？", ["Dual-level Retrieval Paradigm", "low-level retrieval"]),
    ("Why does LightRAG beat GraphRAG?", ["Superiority over GraphRAG"]),
]

MODELS = {
    "bge-m3": (lambda q: q, lambda d: d),
    "qwen3-embedding:0.6b": (
        lambda q: f"Instruct: Given a question, retrieve passages from a research paper that answer it\nQuery: {q}",
        lambda d: d,
    ),
    "qwen3-embedding:0.6b (no instruct)": (lambda q: q, lambda d: d),
    "embeddinggemma:300m": (lambda q: f"task: search result | query: {q}", lambda d: f"title: none | text: {d}"),
}


def chunks_from_pdf(path):
    out = []
    for pno, page in enumerate(pymupdf.open(path), start=1):
        buf, n = [], 0
        for block in page.get_text("blocks"):
            text = block[4].strip()
            if not text:
                continue
            t = len(enc.encode(text))
            if buf and n + t > CHUNK_TOKENS:
                out.append((pno, "\n".join(buf)))
                buf, n = [], 0
            buf.append(text)
            n += t
        if buf:
            out.append((pno, "\n".join(buf)))
    return out


def embed(model, texts):
    req = urllib.request.Request(
        "http://localhost:11434/api/embed",
        data=json.dumps({"model": model, "input": texts}).encode(),
        headers={"Content-Type": "application/json"},
    )
    vecs = np.array(json.load(urllib.request.urlopen(req, timeout=600))["embeddings"], dtype=np.float32)
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)


def first_relevant_rank(order, relevant):
    for rank, idx in enumerate(order, start=1):
        if idx in relevant:
            return rank
    return None


def rrf(*orders, k=60):
    scores = {}
    for order in orders:
        for rank, idx in enumerate(order, start=1):
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)


def main():
    chunks = chunks_from_pdf(PDF)
    texts = [t for _, t in chunks]
    relevant = [{i for i, t in enumerate(texts) if any(m in t for m in markers)} for _, markers in QUERIES]
    print(f"{len(chunks)} chunks; relevant per query: {[len(r) for r in relevant]}")
    assert all(relevant), "a marker matched no chunk — fix the marker"

    results = {}

    tokenized = [re.findall(r"\w+", t.lower()) for t in texts]
    bm25 = BM25Okapi(tokenized)
    results["BM25 (baseline)"] = [
        first_relevant_rank(np.argsort(-bm25.get_scores(re.findall(r"\w+", q.lower()))), rel)
        for (q, _), rel in zip(QUERIES, relevant)
    ]

    for name, (qfmt, dfmt) in MODELS.items():
        model = name.split(" ")[0]
        t0 = time.time()
        dvec = embed(model, [dfmt(t) for t in texts])
        t_docs = time.time() - t0
        qvec = embed(model, [qfmt(q) for q, _ in QUERIES])
        ranks = [first_relevant_rank(np.argsort(-(dvec @ qv)), rel) for qv, rel in zip(qvec, relevant)]
        results[name] = ranks
        if model == "bge-m3":
            bm25_orders = [np.argsort(-bm25.get_scores(re.findall(r"\w+", q.lower()))) for q, _ in QUERIES]
            dense_orders = [np.argsort(-(dvec @ qv)) for qv in qvec]
            results["bge-m3 + BM25 (RRF)"] = [
                first_relevant_rank(rrf(d, b), rel) for d, b, rel in zip(dense_orders, bm25_orders, relevant)
            ]
        print(f"{name}: embedded {len(texts)} chunks in {t_docs:.1f}s")

    print()
    header = f"{'query':<52}" + "".join(f"{n[:22]:>24}" for n in results)
    print(header)
    for qi, (q, _) in enumerate(QUERIES):
        print(f"{q[:50]:<52}" + "".join(f"{str(r[qi]):>24}" for r in results.values()))
    print()
    for name, ranks in results.items():
        mrr = np.mean([1 / r if r else 0 for r in ranks])
        hit3 = np.mean([1 if r and r <= 3 else 0 for r in ranks])
        print(f"{name:<36} MRR={mrr:.3f}  hit@3={hit3:.2f}")


if __name__ == "__main__":
    main()
