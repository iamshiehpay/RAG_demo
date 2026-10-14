"""Request-scoped LangGraph orchestration, streaming the existing public events.

Services and the Document remain in the request closure. Graph state contains only
intermediate answer data; there is no persistence, agent loop or second LLM stack.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import aclosing
from typing import TYPE_CHECKING, TypedDict

from anyio import CancelScope
from langgraph.config import get_stream_writer
from langgraph.errors import NodeCancelledError
from langgraph.graph import END, START, StateGraph

from .citation import citation_map, validate_citations
from .events import (
    CitationMapEvent,
    DeltaEvent,
    ErrorEvent,
    Event,
    FinalEvent,
    PlanEvent,
    RejectedEvent,
    RetrievalEvent,
    RetryEvent,
    ThinkingEvent,
    TraceEvent,
)
from .llm_gateway import LLMFailure
from .models import Chunk, Citation, ConversationTurn, LLMCallTrace
from .policy import HISTORY_ROUND_LIMIT, QUESTION_TOKEN_LIMIT
from .summary_context import select_summary_context
from .tokens import count_tokens

if TYPE_CHECKING:
    from .application import Application


class AskState(TypedDict, total=False):
    valid: bool
    plan: PlanEvent
    chunks: list[Chunk]
    citations: list[Citation]
    context: str
    answer: str


class AskWorkflow:
    def __init__(
        self, application: "Application", question: str, history: list[ConversationTurn] | None
    ):
        self.application = application
        self.question = question
        self.history = history
        self.index = application.index
        self.document = application.document
        self.document_ready_at_start = application._active_upload is None and self.index is not None
        self.calls: list[LLMCallTrace] = []
        self.stage = "router"
        self.dropped_chunk_count = 0
        self.summary_level: str | None = None
        graph = StateGraph(AskState)
        graph.add_node("validate", self.validate)
        graph.add_node("plan", self.plan)
        graph.add_node("summary_evidence", self.summary_evidence)
        graph.add_node("retrieved_evidence", self.retrieved_evidence)
        graph.add_node("generate", self.generate)
        graph.add_node("finalize", self.finalize)
        graph.add_edge(START, "validate")
        graph.add_conditional_edges(
            "validate", lambda state: "plan" if state["valid"] else END, ["plan", END]
        )
        graph.add_conditional_edges(
            "plan",
            lambda state: (
                "summary_evidence"
                if state["plan"].question_type == "Global"
                else "retrieved_evidence"
            ),
            ["summary_evidence", "retrieved_evidence"],
        )
        graph.add_edge("summary_evidence", "generate")
        graph.add_edge("retrieved_evidence", "generate")
        graph.add_edge("generate", "finalize")
        graph.add_edge("finalize", END)
        self.graph = graph.compile(checkpointer=False)

    async def emit(self, event: Event) -> None:
        # Acknowledge only when the public consumer resumes. This prevents graph
        # execution from committing history ahead of a paused/disconnected stream.
        consumed = asyncio.get_running_loop().create_future()
        get_stream_writer()((event, consumed))
        await consumed

    async def stream(self) -> AsyncIterator[Event]:
        queue: asyncio.Queue[tuple[Event, asyncio.Future]] = asyncio.Queue(maxsize=1)
        available = asyncio.Event()

        async def produce():
            try:
                async with aclosing(
                    self.graph.astream({}, stream_mode="custom", version="v1")
                ) as stream:
                    async for payload in stream:
                        await queue.put(payload)
                        available.set()
            except NodeCancelledError as exc:
                # LangGraph wraps a node's own CancelledError as a failure.
                # Restore the public seam's original cancellation contract.
                if isinstance(exc.__cause__, asyncio.CancelledError):
                    raise exc.__cause__ from None
                raise

        # Own the graph task so transport cancellation reaches it once, rather
        # than repeatedly interrupting LangGraph cleanup via AnyIO's cancel scope.
        producer = asyncio.create_task(produce(), name="ask-graph")
        producer.add_done_callback(lambda _: available.set())
        try:
            while True:
                if queue.empty() and producer.done():
                    producer.result()
                    return
                await available.wait()
                available.clear()
                if queue.empty():
                    # Includes producer-initiated cancellation: never strand the
                    # public consumer waiting for an event that cannot arrive.
                    producer.result()
                    return
                event, consumed = queue.get_nowait()
                yield event
                if not consumed.done():
                    consumed.set_result(None)
        finally:
            if not producer.done():
                producer.cancel()
            with CancelScope(shield=True):
                while not producer.done():
                    try:
                        await asyncio.shield(producer)
                    except asyncio.CancelledError:
                        # Repeated Task.cancel must also wait for owned cleanup.
                        continue
                if not producer.cancelled():
                    producer.result()

    async def validate(self, state: AskState) -> AskState:
        if not self.document_ready_at_start:
            await self.emit(
                ErrorEvent(
                    code="document_not_ready",
                    message="Wait until Document processing is complete before asking.",
                )
            )
            return {"valid": False}
        if not self.question.strip():
            await self.emit(ErrorEvent(code="invalid_question", message="Please enter a question."))
            return {"valid": False}
        question_tokens = count_tokens(self.question)
        if question_tokens > QUESTION_TOKEN_LIMIT:
            await self.emit(
                RejectedEvent(
                    message=f"Question must not exceed {QUESTION_TOKEN_LIMIT:,} tokens.",
                    question_tokens=question_tokens,
                    token_limit=QUESTION_TOKEN_LIMIT,
                )
            )
            return {"valid": False}
        return {"valid": True}

    async def plan(self, state: AskState) -> AskState:
        plan = await self.application.router.plan(
            self.question,
            self.application.history if self.history is None else self.history,
            self.calls,
        )
        await self.emit(plan)
        return {"plan": plan}

    async def summary_evidence(self, state: AskState) -> AskState:
        self.stage = "answer"
        if self.document is None or self.document.summary_tree is None:
            raise LLMFailure("Document has no Summary Tree. Please upload it again.")
        context, citations, self.summary_level = select_summary_context(
            self.document.summary_tree,
            state["plan"].standalone_question,
            current_question=self.question,
        )
        await self.emit(RetrievalEvent(chunks=[]))
        await self.emit(CitationMapEvent(citations=citations))
        return {"chunks": [], "citations": citations, "context": context}

    async def retrieved_evidence(self, state: AskState) -> AskState:
        self.stage = "embedding"
        retrieved = await self.application.context_packer.retrieve(
            self.index, state["plan"], current_question=self.question
        )
        self.dropped_chunk_count = retrieved.dropped_chunk_count
        await self.emit(retrieved)
        chunks = sorted((item.chunk for item in retrieved.chunks), key=lambda chunk: chunk.order)
        citations = citation_map(chunks)
        await self.emit(CitationMapEvent(citations=citations))
        self.stage = "fact_extraction"
        context = await self.application.context_packer.pack(
            state["plan"], chunks, citations, self.calls, current_question=self.question
        )
        return {"chunks": chunks, "citations": citations, "context": context}

    async def generate(self, state: AskState) -> AskState:
        self.stage = "answer"
        answer = ""
        async with aclosing(
            self.application.answer_generator.generate(
                state["plan"].standalone_question,
                state["chunks"],
                state["citations"],
                context=state["context"],
                current_question=self.question,
                sources="summary" if state["plan"].question_type == "Global" else "chunk",
            )
        ) as events:
            async for event in events:
                if isinstance(event, DeltaEvent):
                    answer += event.text
                    await self.emit(event)
                elif isinstance(event, TraceEvent):
                    self.calls.extend(event.calls)
                elif isinstance(event, RetryEvent):
                    answer = ""
                    await self.emit(event)
                elif isinstance(event, ThinkingEvent):
                    await self.emit(event)
        if not answer.strip():
            raise LLMFailure("LLM returned an empty answer. Please retry.")
        return {"answer": answer}

    async def finalize(self, state: AskState) -> AskState:
        validated = validate_citations(state["answer"], state["citations"])
        if self.history is None:
            self.application.history = (
                self.application.history
                + [ConversationTurn(question=self.question, answer=validated.answer)]
            )[-HISTORY_ROUND_LIMIT:]
        await self.emit(
            FinalEvent(
                answer=validated.answer,
                citations=validated.citations,
                unverified=validated.unverified,
            )
        )
        if self.calls:
            await self.emit(
                TraceEvent(
                    calls=self.calls,
                    invalid_citation_count=validated.invalid_citation_count,
                    dropped_chunk_count=self.dropped_chunk_count,
                    summary_level=self.summary_level,
                )
            )
        return {"answer": validated.answer}
