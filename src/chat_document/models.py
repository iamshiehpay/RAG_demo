"""Domain values shared by processing modules and the event contract."""

from typing import Literal

from pydantic import BaseModel, Field

FallbackReason = Literal["length", "invalid_json", "invalid_plan", "missing_rewrite"]


class ConversationTurn(BaseModel):
    question: str
    answer: str


class Table(BaseModel):
    label: str
    caption: str
    page_start: int
    page_end: int
    paragraph_index: int = 0
    headers: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)
    meaning: str = ""
    raw_text: str
    reconstructed: bool = False


class Section(BaseModel):
    """A heading and its direct text, including heading-only parent metadata.

    Sections with zero Chunks are excluded from Summary Tree input; builders
    must skip them and summarize only Sections containing source Chunks.
    """

    id: str
    title: str
    page_start: int
    page_end: int
    paragraphs: list[str]
    # Parallel to paragraphs; optional so callers constructing #01 Sections remain compatible.
    paragraph_pages: list[tuple[int, int]] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    is_appendix: bool = False
    is_virtual: bool = False


class Chunk(BaseModel):
    id: str
    section_id: str
    section: str
    page_start: int
    page_end: int
    text: str
    order: int
    kind: Literal["text", "table"] = "text"
    table_label: str | None = None
    table_caption: str | None = None
    table_headers: list[str] = Field(default_factory=list)
    table_rows: list[list[str]] = Field(default_factory=list)
    table_reconstructed: bool = True
    linked_chunk_ids: list[str] = Field(default_factory=list)

    @property
    def context(self) -> str:
        return f"{self.section} (p.{self.page_start})\n{self.text}"


class Document(BaseModel):
    id: str
    name: str
    sections: list[Section]
    chunks: list[Chunk]


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float


class Citation(BaseModel):
    id: str
    source_id: str
    section: str
    page_start: int
    page_end: int


class UnverifiedSpan(BaseModel):
    """Sentence in final answer; Unicode code-point offsets, end exclusive."""

    start: int
    end: int


class LLMCallTrace(BaseModel):
    call_type: str
    estimated_prompt_tokens: int
    prompt_eval_count: int | None
    eval_count: int | None
    think: str
    num_predict: int
    context_budget: int
    safety_margin: int
    thinking: str
    latency_ms: float
    done_reason: str
    discarded_fact_lines: int = 0
    plan_source: Literal["router", "fallback"] | None = None
    fallback_reason: FallbackReason | None = None
    rewrite_language_mismatch: bool = False
    router_standalone_question: str | None = None
