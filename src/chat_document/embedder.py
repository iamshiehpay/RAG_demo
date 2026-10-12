from typing import Protocol

import httpx
import numpy as np


class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> np.ndarray: ...


class OllamaEmbedder:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "bge-m3"):
        self.base_url = base_url
        self.model = model

    async def embed(self, texts: list[str]) -> np.ndarray:
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                f"{self.base_url}/api/embed",
                json={
                    "model": self.model,
                    "input": texts,
                    "truncate": False,
                },
            )
            response.raise_for_status()
            vectors = np.asarray(response.json()["embeddings"], dtype=np.float32)
        if vectors.ndim != 2 or vectors.shape[0] != len(texts) or not np.isfinite(vectors).all():
            raise ValueError("Embedder returned invalid vectors.")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        if np.any(norms == 0):
            raise ValueError("Embedder returned a zero vector.")
        return vectors / norms
