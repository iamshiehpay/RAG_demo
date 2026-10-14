"""In-memory background upload jobs; subscribers can disconnect and replay progress."""

import asyncio
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass
from uuid import uuid4

import httpx
import numpy as np

from .cache import ProcessingCache
from .chunker import chunk_sections
from .embedder import Embedder
from .events import ErrorEvent, Event, StageEvent
from .index import Index
from .models import Document
from .pdf_parser import DocumentError, parse_pdf
from .policy import EMBEDDING_BATCH_CHUNKS
from .settings import RetrievalSettings
from .summary_tree import SummaryTreeBuilder


class UploadBusy(Exception):
    """Only one Document operation can replace the active Document at a time."""


class IngestionJob:
    def __init__(self):
        self.events: list[Event] = []
        self.finished = False
        self.changed = asyncio.Condition()

    async def publish(self, event: Event):
        async with self.changed:
            self.events.append(event)
            self.finished = event.type in {"ready", "error"}
            self.changed.notify_all()

    async def subscribe(self) -> AsyncIterator[Event]:
        position = 0
        while True:
            async with self.changed:
                await self.changed.wait_for(
                    lambda position=position: position < len(self.events) or self.finished
                )
                pending = self.events[position:]
                position = len(self.events)
                finished = self.finished
            for event in pending:
                yield event
            if finished:
                return


logger = logging.getLogger(__name__)


def http_failure_message(stage: str, exc: httpx.HTTPError) -> str:
    label = stage.replace("_", " ").capitalize()
    if isinstance(exc, httpx.HTTPStatusError):
        return (
            f"{label} failed: Ollama HTTP {exc.response.status_code}. "
            f"Check model availability. Details: {exc}"
        )
    reason = "timed out" if isinstance(exc, httpx.TimeoutException) else "connection failed"
    return (
        f"{label} {reason}. Check that the local Ollama daemon is running, "
        f"then retry. Details: {exc}"
    )


@dataclass(frozen=True)
class PreparedDocument:
    document: Document
    index: Index
    cached: bool = False


async def process_document(
    content: bytes,
    name: str,
    *,
    embedder: Embedder,
    summary_builder: SummaryTreeBuilder,
    settings: RetrievalSettings,
    cache: ProcessingCache | None,
) -> AsyncIterator[Event | PreparedDocument]:
    """Prepare all source data before the caller publishes a replacement Document."""
    stage = "parsing"
    try:
        config = {
            "embedding_model": getattr(embedder, "model", "bge-m3"),
            "chunk_token_target": settings.chunk_token_target,
            "summary_model": getattr(summary_builder.gateway.adapter, "model", "scripted"),
        }
        cached = await asyncio.to_thread(cache.load, content, config) if cache else None
        if cached:
            document = cached.document.model_copy(update={"name": name})
            index = Index(
                document.chunks,
                np.asarray(cached.embeddings, dtype=np.float32),
                embedder,
                bm25_weight=settings.bm25_weight,
            )
            yield PreparedDocument(document, index, cached=True)
            return
        yield StageEvent(stage="parsing", completed=0, total=1)
        sections = await asyncio.to_thread(
            parse_pdf, content, chunk_token_target=settings.chunk_token_target
        )
        stage = "chunking"
        yield StageEvent(stage="chunking", completed=0, total=1)
        document_id = uuid4().hex
        chunks = await asyncio.to_thread(
            chunk_sections, sections, document_id, target=settings.chunk_token_target
        )
        stage = "embedding"
        yield StageEvent(stage="embedding", completed=0, total=len(chunks))
        vectors = []
        completed = 0
        for start in range(0, len(chunks), EMBEDDING_BATCH_CHUNKS):
            batch = chunks[start : start + EMBEDDING_BATCH_CHUNKS]
            vectors.append(await embedder.embed([chunk.context for chunk in batch]))
            completed += len(batch)
            yield StageEvent(stage="embedding", completed=completed, total=len(chunks))
        index = Index(
            chunks,
            np.concatenate(vectors),
            embedder,
            bm25_weight=settings.bm25_weight,
        )
        document = Document(id=document_id, name=name, sections=sections, chunks=chunks)
        stage = "summary"
        async for item in summary_builder.build(document):
            if isinstance(item, StageEvent):
                yield item
            else:
                document.summary_tree = item
        if cache:
            try:
                await asyncio.to_thread(cache.store, content, config, document, index.vectors)
            except Exception:
                logger.warning(
                    "Ingestion cache write failed; Document remains ready.", exc_info=True
                )
        yield PreparedDocument(document, index)
    except DocumentError as exc:
        yield ErrorEvent(code="invalid_document", message=str(exc))
    except httpx.HTTPError as exc:
        yield ErrorEvent(
            code=f"{stage}_failed",
            message=http_failure_message(stage, exc),
        )
    except ValueError as exc:
        yield ErrorEvent(
            code="embedding_failed" if stage == "embedding" else "ingestion_failed",
            message=f"Document {stage} failed: {exc}",
        )
    except Exception:
        logger.exception("Unexpected Document processing failure")
        yield ErrorEvent(
            code="ingestion_failed",
            message="Unexpected Document processing failure. Please retry.",
        )
