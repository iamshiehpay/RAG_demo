"""Public seams: upload Document and ask. HTTP and tests consume the same events."""

import asyncio
import logging
import os
from collections.abc import AsyncIterator
from contextlib import suppress
from uuid import uuid4

import httpx
import numpy as np

from .answer_generator import AnswerGenerator
from .cache import ProcessingCache
from .chunker import chunk_sections
from .citation import citation_map, validate_citations
from .context_packer import ContextPacker
from .embedder import Embedder
from .events import (
    CitationMapEvent,
    DeltaEvent,
    ErrorEvent,
    Event,
    FinalEvent,
    ReadyEvent,
    RejectedEvent,
    RetryEvent,
    StageEvent,
    ThinkingEvent,
    TraceEvent,
)
from .index import Index
from .ingestion import IngestionJob, UploadBusy
from .llm_gateway import BudgetExceeded, LLMFailure, LLMGateway
from .models import Chunk, ConversationTurn, Document, LLMCallTrace, Summary
from .pdf_parser import DocumentError, parse_pdf
from .policy import (
    EMBEDDING_BATCH_CHUNKS,
    HISTORY_ROUND_LIMIT,
    QUESTION_TOKEN_LIMIT,
    SUMMARY_CONCURRENCY,
)
from .router import Router
from .settings import RetrievalSettings
from .summary_context import select_summary_context
from .summary_tree import SummaryTreeBuilder
from .tokens import count_tokens

logger = logging.getLogger(__name__)


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
        settings = settings or RetrievalSettings()
        if chunk_token_target is not None:
            settings = RetrievalSettings(
                **(settings.model_dump() | {"chunk_token_target": chunk_token_target})
            )
        self.chunk_token_target = settings.chunk_token_target
        self.embedder = embedder
        self.cache = cache
        self.answer_generator = AnswerGenerator(gateway)
        self.router = Router(gateway)
        self.context_packer = ContextPacker(gateway, settings)
        self.summary_builder = SummaryTreeBuilder(
            gateway,
            concurrency=summary_concurrency
            if summary_concurrency is not None
            else int(os.environ.get("SUMMARY_CONCURRENCY", SUMMARY_CONCURRENCY)),
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
            index = Index(chunks, np.concatenate(vectors), self.embedder)
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
            message = (
                "Embedding failed. Check that the local Ollama daemon is running and "
                f"bge-m3 is installed, then retry. Details: {exc}"
                if stage == "embedding"
                else f"Document {stage} failed: {exc}"
            )
            yield ErrorEvent(
                code=f"{stage}_failed",
                message=message,
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
        calls: list[LLMCallTrace] = []
        summary_level: str | None = None
        stage = "router"
        self._asking += 1
        dropped_chunk_count = 0
        try:
            index = self.index
            if self._active_upload is not None or index is None:
                yield ErrorEvent(
                    code="document_not_ready",
                    message="Wait until Document processing is complete before asking.",
                )
                return
            if not question.strip():
                yield ErrorEvent(code="invalid_question", message="Please enter a question.")
                return
            question_tokens = count_tokens(question)
            if question_tokens > QUESTION_TOKEN_LIMIT:
                yield RejectedEvent(
                    message=f"Question must not exceed {QUESTION_TOKEN_LIMIT:,} tokens.",
                    question_tokens=question_tokens,
                    token_limit=QUESTION_TOKEN_LIMIT,
                )
                return
            plan = await self.router.plan(
                question, self.history if history is None else history, calls
            )
            yield plan
            if plan.question_type == "Global":
                stage = "answer"
                if self.document is None or self.document.summary_tree is None:
                    raise LLMFailure("Document has no Summary Tree. Please upload it again.")
                context, citations, summary_level = select_summary_context(
                    self.document.summary_tree,
                    plan.standalone_question,
                    current_question=question,
                )
                chunks = []
                yield RetrievalEvent(chunks=[])
                yield CitationMapEvent(citations=citations)
            else:
                stage = "embedding"
                retrieved = await self.context_packer.retrieve(
                    index, plan, current_question=question
                )
                dropped_chunk_count = retrieved.dropped_chunk_count
                yield retrieved
                chunks = sorted((item.chunk for item in retrieved.chunks), key=lambda chunk: chunk.order)
                citations = citation_map(chunks)
                yield CitationMapEvent(citations=citations)
                stage = "answer"
                context = await self.context_packer.pack(
                    plan, chunks, citations, calls, current_question=question
                )
            answer = ""
            async for event in self.answer_generator.generate(
                plan.standalone_question,
                chunks,
                citations,
                context=context,
                current_question=question,
            ):
                if isinstance(event, DeltaEvent):
                    answer += event.text
                    yield event
                elif isinstance(event, TraceEvent):
                    calls.extend(event.calls)
                elif isinstance(event, RetryEvent):
                    answer = ""
                    yield event
                elif isinstance(event, ThinkingEvent):
                    yield event
            if not answer.strip():
                raise LLMFailure("LLM returned an empty answer. Please retry.")
            validated = validate_citations(answer, citations)
            answer = validated.answer
            if history is None:
                self.history = (
                    self.history + [ConversationTurn(question=question, answer=answer)]
                )[-HISTORY_ROUND_LIMIT:]
            yield FinalEvent(
                answer=answer, citations=validated.citations, unverified=validated.unverified
            )
            if calls:
                yield TraceEvent(
                    calls=calls,
                    invalid_citation_count=validated.invalid_citation_count,
                    dropped_chunk_count=dropped_chunk_count,
                    summary_level=summary_level,
                )
        except BudgetExceeded as exc:
            if calls:
                yield TraceEvent(calls=calls, dropped_chunk_count=dropped_chunk_count)
            yield ErrorEvent(code="budget_exceeded", message=str(exc))
        except httpx.HTTPError as exc:
            if calls:
                yield TraceEvent(calls=calls, dropped_chunk_count=dropped_chunk_count)
            reason = "timed out" if isinstance(exc, httpx.TimeoutException) else "connection failed"
            yield ErrorEvent(
                code=f"{stage}_failed",
                message=f"{stage.capitalize()} {reason}. Check that the local Ollama daemon "
                f"is running, then retry. Details: {exc}",
            )
        except ValueError as exc:
            if calls:
                yield TraceEvent(calls=calls, dropped_chunk_count=dropped_chunk_count)
            yield ErrorEvent(code="answer_failed", message=f"Answer failed: {exc}")
        except Exception:
            logger.exception("Unexpected answer failure")
            if calls:
                yield TraceEvent(calls=calls, dropped_chunk_count=dropped_chunk_count)
            yield ErrorEvent(
                code="answer_failed", message="Unexpected answer failure. Please retry."
            )
        finally:
            self._asking -= 1
