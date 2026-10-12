"""Public seams: upload Document and ask. HTTP and tests consume the same events."""

import logging
from collections.abc import AsyncIterator
from uuid import uuid4

import httpx

from .answer_generator import AnswerGenerator
from .chunker import chunk_sections
from .citation import citation_map, cited_sources
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
    RetrievalEvent,
    StageEvent,
    TraceEvent,
)
from .index import Index
from .llm_gateway import BudgetExceeded, LLMFailure, LLMGateway
from .models import Chunk, ConversationTurn, Document, LLMCallTrace
from .pdf_parser import DocumentError, parse_pdf
from .policy import HISTORY_ROUND_LIMIT, QUESTION_TOKEN_LIMIT
from .router import Router
from .settings import RetrievalSettings
from .tokens import count_tokens

logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self, embedder: Embedder, gateway: LLMGateway, *, settings: RetrievalSettings | None = None
    ):
        self.embedder = embedder
        self.answer_generator = AnswerGenerator(gateway)
        self.router = Router(gateway)
        self.context_packer = ContextPacker(gateway, settings or RetrievalSettings())
        self.document: Document | None = None
        self.index: Index | None = None
        self.history: list[ConversationTurn] = []

    async def upload_document(self, content: bytes, name: str) -> AsyncIterator[Event]:
        self.document = None
        self.index = None
        self.history = []
        try:
            yield StageEvent(stage="parsing", completed=0, total=1)
            sections = parse_pdf(content)
            yield StageEvent(stage="chunking", completed=0, total=1)
            document_id = uuid4().hex
            chunks = chunk_sections(sections, document_id)
            yield StageEvent(stage="embedding", completed=0, total=len(chunks))
            index = await Index.build(chunks, self.embedder)
            self.document = Document(id=document_id, name=name, sections=sections, chunks=chunks)
            self.index = index
            yield ReadyEvent(document_id=document_id, name=name, chunk_count=len(chunks))
        except DocumentError as exc:
            yield ErrorEvent(code="invalid_document", message=str(exc))
        except (httpx.HTTPError, ValueError) as exc:
            yield ErrorEvent(code="ingestion_failed", message=f"Document processing failed: {exc}")
        except Exception:
            logger.exception("Unexpected Document processing failure")
            yield ErrorEvent(
                code="ingestion_failed",
                message="Unexpected Document processing failure. Please retry.",
            )

    def source(self, source_id: str) -> Chunk:
        if self.document:
            for chunk in self.document.chunks:
                if chunk.id == source_id:
                    return chunk
        raise KeyError(source_id)

    async def ask(
        self, question: str, *, history: list[ConversationTurn] | None = None
    ) -> AsyncIterator[Event]:
        calls: list[LLMCallTrace] = []
        try:
            index = self.index
            if index is None:
                yield ErrorEvent(
                    code="document_not_ready", message="Upload a Document before asking."
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
            # Until #05, Global uses the Synthesis path while the visible plan stays Global.
            context_plan = (
                plan.model_copy(update={"question_type": "Synthesis"})
                if plan.question_type == "Global"
                else plan
            )
            retrieved = await self.context_packer.retrieve(
                index, context_plan, current_question=question
            )
            yield RetrievalEvent(chunks=retrieved)
            chunks = sorted((item.chunk for item in retrieved), key=lambda chunk: chunk.order)
            citations = citation_map(chunks)
            yield CitationMapEvent(citations=citations)
            context = await self.context_packer.pack(
                context_plan, chunks, citations, calls, current_question=question
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
            if not answer.strip():
                raise LLMFailure("LLM returned an empty answer. Please retry.")
            if history is None:
                self.history = (
                    self.history + [ConversationTurn(question=question, answer=answer)]
                )[-HISTORY_ROUND_LIMIT:]
            yield FinalEvent(answer=answer, citations=cited_sources(answer, citations))
            if calls:
                yield TraceEvent(calls=calls)
        except BudgetExceeded as exc:
            yield ErrorEvent(code="budget_exceeded", message=str(exc))
            if calls:
                yield TraceEvent(calls=calls)
        except (httpx.HTTPError, ValueError) as exc:
            yield ErrorEvent(code="answer_failed", message=f"Answer failed: {exc}")
            if calls:
                yield TraceEvent(calls=calls)
        except Exception:
            logger.exception("Unexpected answer failure")
            yield ErrorEvent(
                code="answer_failed", message="Unexpected answer failure. Please retry."
            )
            if calls:
                yield TraceEvent(calls=calls)
