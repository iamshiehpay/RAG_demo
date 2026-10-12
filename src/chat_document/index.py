import numpy as np

from .embedder import Embedder
from .models import Chunk, RetrievedChunk


class Index:
    def __init__(self, chunks: list[Chunk], vectors: np.ndarray, embedder: Embedder):
        self.chunks = chunks
        self.vectors = vectors
        self.embedder = embedder

    @classmethod
    async def build(cls, chunks: list[Chunk], embedder: Embedder) -> "Index":
        return cls(chunks, await embedder.embed([chunk.context for chunk in chunks]), embedder)

    async def retrieve(self, standalone_question: str, top_k: int = 5) -> list[RetrievedChunk]:
        query = (await self.embedder.embed([standalone_question]))[0]
        scores = self.vectors @ query
        ranks = np.argsort(-scores, kind="stable")[:top_k]
        return [RetrievedChunk(chunk=self.chunks[int(i)], score=float(scores[i])) for i in ranks]
