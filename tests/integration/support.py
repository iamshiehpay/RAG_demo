"""Helpers that deliberately call the local embedding service."""

import asyncio

from app.embedder import OllamaEmbedder


class RecordingEmbedder(OllamaEmbedder):
    """Record calls and optionally hold real bge-m3 at the external dependency seam."""

    def __init__(self, *, hold=False):
        super().__init__()
        self.calls = []
        self.entered = asyncio.Event()
        self.release = asyncio.Event()
        if not hold:
            self.release.set()

    async def embed(self, texts):
        self.calls.append(texts)
        self.entered.set()
        await self.release.wait()
        return await super().embed(texts)
