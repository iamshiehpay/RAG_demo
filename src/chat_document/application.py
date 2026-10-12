"""Public seams: upload Document and ask. HTTP and tests consume the same events."""

from collections.abc import AsyncIterator
from uuid import uuid4

import httpx

from .answer_generator import AnswerGenerator
from .chunker import chunk_sections
from .citation import citation_map, cited_sources
from .embedder import Embedder
from .events import (
    CitationMapEvent,
    DeltaEvent,
    ErrorEvent,
    Event,
    FinalEvent,
    PlanEvent,
    ReadyEvent,
    RetrievalEvent,
    StageEvent,
    TraceEvent,
)
from .index import Index
from .llm_gateway import BudgetExceeded, LLMFailure, LLMGateway
from .models import Chunk, Document
from .pdf_parser import DocumentError, parse_pdf
from .tokens import count_tokens


class Application:
    def __init__(self, embedder: Embedder, gateway: LLMGateway):
        self.embedder = embedder
        self.answer_generator = AnswerGenerator(gateway)
        self.document: Document | None = None
        self.index: Index | None = None

    async def upload_document(self, content: bytes, name: str) -> AsyncIterator[Event]:
        self.document = None
        self.index = None
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

    def source(self, source_id: str) -> Chunk:
        if self.document:
            for chunk in self.document.chunks:
                if chunk.id == source_id:
                    return chunk
        raise KeyError(source_id)

    async def ask(self, question: str) -> AsyncIterator[Event]:
        index = self.index
        if index is None:
            yield ErrorEvent(code="document_not_ready", message="Upload a Document before asking.")
            return
        if not question.strip():
            yield ErrorEvent(code="invalid_question", message="Please enter a question.")
            return
        if count_tokens(question) > 1000:
            yield ErrorEvent(
                code="question_too_long", message="Question must not exceed 1,000 tokens."
            )
            return
        trace = None
        try:
            yield PlanEvent(question_type="Lookup", standalone_question=question, sub_queries=[])
            retrieved = await index.retrieve(question)
            yield RetrievalEvent(chunks=retrieved)
            chunks = sorted((item.chunk for item in retrieved), key=lambda chunk: chunk.order)
            citations = citation_map(chunks)
            yield CitationMapEvent(citations=citations)
            answer = ""
            async for event in self.answer_generator.generate(question, chunks, citations):
                if isinstance(event, DeltaEvent):
                    answer += event.text
                    yield event
                elif isinstance(event, TraceEvent):
                    trace = event
            if not answer.strip():
                raise LLMFailure("LLM returned an empty answer. Please retry.")
            yield FinalEvent(answer=answer, citations=cited_sources(answer, citations))
            if trace:
                yield trace
        except BudgetExceeded as exc:
            yield ErrorEvent(code="budget_exceeded", message=str(exc))
        except (httpx.HTTPError, ValueError) as exc:
            yield ErrorEvent(code="answer_failed", message=f"Answer failed: {exc}")
            if trace:
                yield trace
