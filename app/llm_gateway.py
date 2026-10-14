"""Every LLM call crosses this guard; numeric policies mirror AGENTS.md."""

import json
from collections.abc import AsyncIterator
from contextlib import aclosing
from dataclasses import dataclass
from time import perf_counter
from typing import Literal

from .events import DeltaEvent, ThinkingEvent, TraceEvent
from .llm_adapter import LLMAdapter, LLMRequest
from .models import LLMCallTrace
from .policy import CONTEXT_BUDGET, SAFETY_MARGIN
from .tokens import count_tokens


@dataclass(frozen=True)
class CallPolicy:
    think: Literal["low", "medium"]
    num_predict: int
    prompt_limit: int


BUDGET_TABLE = {
    "router": CallPolicy("low", 600, 9100),
    "section_summary": CallPolicy("low", 1200, 8500),
    "group_summary": CallPolicy("low", 2500, 7200),
    "document_summary": CallPolicy("low", 2500, 7200),
    "fact_extraction": CallPolicy("low", 1000, 8700),
    "answer": CallPolicy("medium", 3000, 6700),
    "judge": CallPolicy("low", 1000, 8700),
}


class BudgetExceeded(ValueError):
    pass


class LLMFailure(ValueError):
    pass


class LLMTruncated(LLMFailure):
    pass


class LLMGateway:
    def __init__(self, adapter: LLMAdapter, context_budget: int = CONTEXT_BUDGET):
        self.adapter = adapter
        self.context_budget = context_budget

    async def generate(
        self,
        call_type: str,
        messages: list[dict[str, str]],
        *,
        format: dict | None = None,
        think: Literal["low", "medium"] | None = None,
    ) -> AsyncIterator[DeltaEvent | ThinkingEvent | TraceEvent]:
        policy = BUDGET_TABLE[call_type]
        raw_tokens = sum(count_tokens(message["content"]) for message in messages)
        if format is not None:
            raw_tokens += count_tokens(json.dumps(format, ensure_ascii=False))
        estimated = raw_tokens + SAFETY_MARGIN
        if raw_tokens > policy.prompt_limit or estimated + policy.num_predict > self.context_budget:
            raise BudgetExceeded(
                f"Context Budget exceeded: {estimated} estimated prompt tokens + "
                f"{policy.num_predict} output reservation > permitted budget "
                f"({self.context_budget}); prompt limit is {policy.prompt_limit}."
            )
        effective_think = think or policy.think
        request = LLMRequest(
            messages, effective_think, policy.num_predict, estimated, format, call_type
        )
        started = perf_counter()
        thinking = ""
        terminal = None

        def trace(done_reason: str) -> TraceEvent:
            return TraceEvent(
                calls=[
                    LLMCallTrace(
                        call_type=call_type,
                        estimated_prompt_tokens=estimated,
                        prompt_eval_count=terminal.prompt_eval_count if terminal else None,
                        eval_count=terminal.eval_count if terminal else None,
                        think=effective_think,
                        num_predict=policy.num_predict,
                        context_budget=self.context_budget,
                        safety_margin=SAFETY_MARGIN,
                        thinking=thinking,
                        latency_ms=(perf_counter() - started) * 1000,
                        done_reason=done_reason,
                    )
                ]
            )

        try:
            async with aclosing(self.adapter.stream(request)) as frames:
                async for frame in frames:
                    thinking += frame.thinking
                    if frame.thinking and call_type == "answer":
                        yield ThinkingEvent(text=frame.thinking)
                    if frame.content:
                        yield DeltaEvent(text=frame.content)
                    if frame.done:
                        terminal = frame
                        break
            if terminal is None:
                raise LLMFailure("LLM stream ended without a completion record. Please retry.")
        except Exception:
            yield trace("error")
            raise
        yield trace(terminal.done_reason)
        if terminal.done_reason == "length":
            label = {"answer": "Answer", "fact_extraction": "Fact extraction"}.get(
                call_type, call_type.replace("_", " ").capitalize()
            )
            raise LLMTruncated(f"{label} was truncated. Please retry.")
