"""Every LLM call crosses this guard; numeric policies mirror AGENTS.md."""

from collections.abc import AsyncIterator
from dataclasses import dataclass
from time import perf_counter
from typing import Literal

from .events import DeltaEvent, TraceEvent
from .llm_adapter import LLMAdapter, LLMRequest
from .models import LLMCallTrace
from .tokens import count_tokens

CONTEXT_BUDGET = 10_000
SAFETY_MARGIN = 300


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


class LLMGateway:
    def __init__(self, adapter: LLMAdapter, context_budget: int = CONTEXT_BUDGET):
        self.adapter = adapter
        self.context_budget = context_budget

    async def generate(
        self, call_type: str, messages: list[dict[str, str]]
    ) -> AsyncIterator[DeltaEvent | TraceEvent]:
        policy = BUDGET_TABLE[call_type]
        raw_tokens = sum(count_tokens(message["content"]) for message in messages)
        estimated = raw_tokens + SAFETY_MARGIN
        if raw_tokens > policy.prompt_limit or estimated + policy.num_predict > self.context_budget:
            raise BudgetExceeded(
                f"Context Budget exceeded: {estimated} estimated prompt tokens + "
                f"{policy.num_predict} output reservation > permitted budget "
                f"({self.context_budget}); prompt limit is {policy.prompt_limit}."
            )
        request = LLMRequest(messages, policy.think, policy.num_predict, estimated)
        started = perf_counter()
        thinking = ""
        async for frame in self.adapter.stream(request):
            thinking += frame.thinking
            if frame.content:
                yield DeltaEvent(text=frame.content)
            if frame.done:
                if frame.done_reason == "length":
                    raise LLMFailure("Answer was truncated. Please retry.")
                yield TraceEvent(
                    calls=[
                        LLMCallTrace(
                            call_type=call_type,
                            estimated_prompt_tokens=estimated,
                            prompt_eval_count=frame.prompt_eval_count,
                            eval_count=frame.eval_count,
                            think=policy.think,
                            num_predict=policy.num_predict,
                            context_budget=self.context_budget,
                            thinking=thinking,
                            latency_ms=(perf_counter() - started) * 1000,
                            done_reason=frame.done_reason,
                        )
                    ]
                )
                return
        raise LLMFailure("LLM stream ended without a completion record. Please retry.")
