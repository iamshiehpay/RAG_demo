"""Public seams: upload Document and ask. HTTP and tests consume the same events."""

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import aclosing, suppress
from uuid import uuid4

import httpx
import numpy as np

from .answer_generator import AnswerGenerator
from .ask_graph import AskWorkflow
from .cache import ProcessingCache
from .chunker import chunk_sections
from .context_packer import ContextPacker
from .embedder import Embedder
from .events import (
    ErrorEvent,
    Event,
    ReadyEvent,
    StageEvent,
    TraceEvent,
)
from .index import Index
from .ingestion import IngestionJob, UploadBusy
from .llm_gateway import BudgetExceeded, LLMGateway
from .models import Chunk, ConversationTurn, Document, Summary
from .pdf_parser import DocumentError, parse_pdf
from .policy import EMBEDDING_BATCH_CHUNKS
from .router import Router
from .settings import RetrievalSettings
from .summary_tree import SummaryTreeBuilder

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


class Application:
    def __init__(
        self,
        embedder: Embedder,
        gateway: LLMGateway,
        *,
        settings: RetrievalSettings | None = None,
        chunk_token_target: int | None = None,
        cache: ProcessingCache | None = None,
        summary_concurrency: int | None = None,
    ):
        settings = settings or RetrievalSettings.from_env()
        if chunk_token_target is not None:
            settings = RetrievalSettings(
                **(settings.model_dump() | {"chunk_token_target": chunk_token_target})
            )
        if summary_concurrency is not None:
            settings = settings.model_copy(update={"summary_concurrency": summary_concurrency})
        self.settings = settings
        self.chunk_token_target = settings.chunk_token_target
        self.embedder = embedder
        self.cache = cache
        self.answer_generator = AnswerGenerator(gateway, think=settings.answer_think)
        self.router = Router(gateway)
        self.context_packer = ContextPacker(gateway, settings)
        self.summary_builder = SummaryTreeBuilder(
            gateway,
            concurrency=settings.summary_concurrency,
        )
        self.document: Document | None = None
        self.index: Index | None = None
        self.history: list[ConversationTurn] = []
        self._jobs: dict[str, IngestionJob] = {}
        self._active_upload: str | None = None
        self._upload_task: asyncio.Task | None = None
        self._asking = 0

    def start_upload(self, content: bytes, name: str) -> str:
        if self._active_upload is not None or self._asking:
            raise UploadBusy("A Document operation is in progress. Please wait and retry.")
        job_id = uuid4().hex
        job = IngestionJob()
        self._jobs[job_id] = job
        self._active_upload = job_id
        self._upload_task = asyncio.create_task(self._run_upload(job_id, job, content, name))
        return job_id

    def upload_events(self, job_id: str) -> AsyncIterator[Event]:
        return self._jobs[job_id].subscribe()

    def _publish_document(self, document: Document, index: Index) -> ReadyEvent:
        self.document = document
        self.index = index
        self.history = []
        return ReadyEvent(
            document_id=document.id,
            name=document.name,
            chunk_count=len(document.chunks),
            document_summary=document.summary_tree.document_summary.text
            if document.summary_tree
            else None,
        )

    async def close(self):
        job_id = self._active_upload
        if self._upload_task and not self._upload_task.done():
            self._upload_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._upload_task
        # A Task cancelled before its first execution cannot run the worker's cleanup.
        if job_id is not None and not self._jobs[job_id].finished:
            await self._jobs[job_id].publish(
                ErrorEvent(
                    code="ingestion_cancelled", message="Document processing stopped. Retry."
                )
            )
        if self._active_upload == job_id:
            self._active_upload = None

    async def upload_document(self, content: bytes, name: str) -> AsyncIterator[Event]:
        """Application seam for callers that want to await a complete upload."""
        try:
            job_id = self.start_upload(content, name)
        except UploadBusy as exc:
            yield ErrorEvent(code="document_busy", message=str(exc))
            return
        async for event in self.upload_events(job_id):
            yield event

    async def _run_upload(self, job_id: str, job: IngestionJob, content: bytes, name: str):
        try:
            async for event in self._process_document(content, name):
                if event.type in {"ready", "error"}:
                    self._active_upload = None
                await job.publish(event)
        except asyncio.CancelledError:
            await job.publish(
                ErrorEvent(
                    code="ingestion_cancelled", message="Document processing stopped. Retry."
                )
            )
        finally:
            if self._active_upload == job_id:
                self._active_upload = None

    async def _process_document(self, content: bytes, name: str) -> AsyncIterator[Event]:
        stage = "parsing"
        try:
            config = {
                "embedding_model": getattr(self.embedder, "model", "bge-m3"),
                "chunk_token_target": self.chunk_token_target,
                "summary_model": getattr(self.summary_builder.gateway.adapter, "model", "scripted"),
            }
            cached = (
                await asyncio.to_thread(self.cache.load, content, config) if self.cache else None
            )
            if cached:
                document = cached.document.model_copy(update={"name": name})
                index = Index(
                    document.chunks,
                    np.asarray(cached.embeddings, dtype=np.float32),
                    self.embedder,
                    bm25_weight=self.settings.bm25_weight,
                )
                yield self._publish_document(document, index)
                return
            yield StageEvent(stage="parsing", completed=0, total=1)
            sections = await asyncio.to_thread(
                parse_pdf, content, chunk_token_target=self.chunk_token_target
            )
            stage = "chunking"
            yield StageEvent(stage="chunking", completed=0, total=1)
            document_id = uuid4().hex
            chunks = await asyncio.to_thread(
                chunk_sections, sections, document_id, target=self.chunk_token_target
            )
            stage = "embedding"
            yield StageEvent(stage="embedding", completed=0, total=len(chunks))
            vectors = []
            completed = 0
            for start in range(0, len(chunks), EMBEDDING_BATCH_CHUNKS):
                batch = chunks[start : start + EMBEDDING_BATCH_CHUNKS]
                vectors.append(await self.embedder.embed([chunk.context for chunk in batch]))
                completed += len(batch)
                yield StageEvent(stage="embedding", completed=completed, total=len(chunks))
            index = Index(
                chunks,
                np.concatenate(vectors),
                self.embedder,
                bm25_weight=self.settings.bm25_weight,
            )
            document = Document(id=document_id, name=name, sections=sections, chunks=chunks)
            stage = "summary"
            async for item in self.summary_builder.build(document):
                if isinstance(item, StageEvent):
                    yield item
                else:
                    document.summary_tree = item
            if self.cache:
                try:
                    await asyncio.to_thread(
                        self.cache.store, content, config, document, index.vectors
                    )
                except Exception:
                    logger.warning(
                        "Ingestion cache write failed; Document remains ready.", exc_info=True
                    )
            ready = self._publish_document(document, index)
            yield StageEvent(stage="complete", completed=1, total=1)
            yield ready
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

    def source(self, source_id: str) -> Chunk | Summary:
        if self.document:
            for chunk in self.document.chunks:
                if chunk.id == source_id:
                    return chunk
            tree = self.document.summary_tree
            if tree:
                for summary in (
                    tree.section_summaries
                    + [s for level in tree.group_levels for s in level]
                    + [tree.document_summary]
                ):
                    if summary.id == source_id:
                        return summary
        raise KeyError(source_id)

    async def ask(
        self, question: str, *, history: list[ConversationTurn] | None = None
    ) -> AsyncIterator[Event]:
        workflow = AskWorkflow(self, question, history)
        self._asking += 1
        try:
            async with aclosing(workflow.stream()) as events:
                async for event in events:
                    yield event
        except BudgetExceeded as exc:
            if workflow.calls:
                yield TraceEvent(
                    calls=workflow.calls, dropped_chunk_count=workflow.dropped_chunk_count
                )
            yield ErrorEvent(code="budget_exceeded", message=str(exc))
        except httpx.HTTPError as exc:
            if workflow.calls:
                yield TraceEvent(
                    calls=workflow.calls, dropped_chunk_count=workflow.dropped_chunk_count
                )
            yield ErrorEvent(
                code=f"{workflow.stage}_failed",
                message=http_failure_message(workflow.stage, exc),
            )
        except ValueError as exc:
            if workflow.calls:
                yield TraceEvent(
                    calls=workflow.calls, dropped_chunk_count=workflow.dropped_chunk_count
                )
            yield ErrorEvent(
                code=f"{workflow.stage}_failed",
                message=f"{workflow.stage.replace('_', ' ').capitalize()} failed: {exc}",
            )
        except Exception:
            logger.exception("Unexpected answer failure")
            if workflow.calls:
                yield TraceEvent(
                    calls=workflow.calls, dropped_chunk_count=workflow.dropped_chunk_count
                )
            yield ErrorEvent(
                code="answer_failed", message="Unexpected answer failure. Please retry."
            )
        finally:
            self._asking -= 1
