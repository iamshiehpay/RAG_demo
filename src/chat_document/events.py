"""Single source of truth for upload/ask events (generate frontend types from this)."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter

from .models import Citation, FallbackReason, LLMCallTrace, RetrievedChunk, UnverifiedSpan


class StageEvent(BaseModel):
    type: Literal["stage"] = "stage"
    stage: Literal["parsing", "chunking", "embedding", "summary", "complete"]
    completed: int
    total: int


class ReadyEvent(BaseModel):
    type: Literal["ready"] = "ready"
    document_id: str
    name: str
    chunk_count: int
    document_summary: str | None = None


class PlanEvent(BaseModel):
    type: Literal["plan"] = "plan"
    question_type: Literal["Global", "Synthesis", "Lookup"]
    standalone_question: str
    sub_queries: list[str]
    plan_source: Literal["router", "fallback"] = "router"
    fallback_reason: FallbackReason | None = None
    rewrite_language_mismatch: bool = False
    router_standalone_question: str | None = None


class RejectedEvent(BaseModel):
    type: Literal["rejected"] = "rejected"
    code: Literal["question_too_long"] = "question_too_long"
    message: str
    question_tokens: int
    token_limit: int


class RetrievalEvent(BaseModel):
    type: Literal["retrieval"] = "retrieval"
    chunks: list[RetrievedChunk]
    dropped_chunk_count: int = 0


class CitationMapEvent(BaseModel):
    type: Literal["citation_map"] = "citation_map"
    citations: list[Citation]


class ThinkingEvent(BaseModel):
    type: Literal["thinking"] = "thinking"
    text: str


class DeltaEvent(BaseModel):
    type: Literal["delta"] = "delta"
    text: str


class RetryEvent(BaseModel):
    type: Literal["retry"] = "retry"
    reason: str


class FinalEvent(BaseModel):
    type: Literal["final"] = "final"
    answer: str
    citations: list[Citation]
    unverified: list[UnverifiedSpan] = Field(default_factory=list)


class TraceEvent(BaseModel):
    type: Literal["trace"] = "trace"
    calls: list[LLMCallTrace]
    invalid_citation_count: int = 0
    dropped_chunk_count: int = 0
    summary_level: str | None = None


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    code: str
    message: str


Event = Annotated[
    StageEvent
    | ReadyEvent
    | PlanEvent
    | RejectedEvent
    | RetrievalEvent
    | CitationMapEvent
    | ThinkingEvent
    | DeltaEvent
    | RetryEvent
    | FinalEvent
    | TraceEvent
    | ErrorEvent,
    Field(discriminator="type"),
]
EVENT_ADAPTER = TypeAdapter(Event)
