"""Domain values shared by processing modules and the event contract."""

from pydantic import BaseModel


class ConversationTurn(BaseModel):
    question: str
    answer: str


class Section(BaseModel):
    id: str
    title: str
    page_start: int
    page_end: int
    paragraphs: list[str]


class Chunk(BaseModel):
    id: str
    section_id: str
    section: str
    page_start: int
    page_end: int
    text: str
    order: int

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
