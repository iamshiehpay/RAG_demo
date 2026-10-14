import re
from collections import Counter

import numpy as np

from .embedder import Embedder
from .models import Chunk, RetrievedChunk
from .policy import BM25_B, BM25_K1, RRF_K


class Index:
    def __init__(
        self,
        chunks: list[Chunk],
        vectors: np.ndarray,
        embedder: Embedder,
        *,
        bm25_weight: float = 0,
    ):
        self.chunks = chunks
        self.vectors = vectors
        self.embedder = embedder
        self.bm25_weight = bm25_weight
        self.terms = [Counter(re.findall(r"\w+", c.context.casefold())) for c in chunks]
        self.lengths = np.array([sum(t.values()) for t in self.terms])
        self.document_frequency = Counter(term for t in self.terms for term in t)

    def lexical_scores(self, question: str) -> np.ndarray:
        scores = np.zeros(len(self.chunks))
        if not self.chunks:
            return scores
        average = max(float(self.lengths.mean()), 1)
        normalizer = BM25_K1 * (1 - BM25_B + BM25_B * self.lengths / average)
        for term in set(re.findall(r"\w+", question.casefold())):
            frequency = self.document_frequency[term]
            if not frequency:
                continue
            idf = np.log(1 + (len(self.chunks) - frequency + 0.5) / (frequency + 0.5))
            counts = np.array([t[term] for t in self.terms])
            scores += idf * counts * (BM25_K1 + 1) / (counts + normalizer)
        return scores

    async def retrieve(self, standalone_question: str, top_k: int = 5) -> list[RetrievedChunk]:
        query = (await self.embedder.embed([standalone_question]))[0]
        scores = self.vectors @ query
        ranks = np.argsort(-scores, kind="stable")
        ranking = None
        if self.bm25_weight:
            lexical = self.lexical_scores(standalone_question)
            ranking = np.zeros(len(scores))
            ranking[ranks] = 1 / (RRF_K + np.arange(1, len(scores) + 1))
            # Queries without lexical overlap keep dense ranking (e.g. Chinese→English).
            if np.any(lexical > 0):
                lexical_ranks = np.argsort(-lexical, kind="stable")
                ranking *= 1 - self.bm25_weight
                ranking[lexical_ranks] += self.bm25_weight / (RRF_K + np.arange(1, len(scores) + 1))
                ranks = np.argsort(-ranking, kind="stable")
        return [
            RetrievedChunk(
                chunk=self.chunks[int(i)],
                score=float(scores[i]),
                ranking_score=float(ranking[i]) if ranking is not None else None,
            )
            for i in ranks[:top_k]
        ]
