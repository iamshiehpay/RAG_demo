"""Native Ollama text→text adapter."""

import json
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Literal, Protocol

import httpx


@dataclass(frozen=True)
class LLMRequest:
    messages: list[dict[str, str]]
    think: Literal["low", "medium"]
    num_predict: int
    estimated_prompt_tokens: int
    format: dict | None = None
    call_type: str = ""


@dataclass(frozen=True)
class LLMFrame:
    content: str = ""
    thinking: str = ""
    done: bool = False
    prompt_eval_count: int | None = None
    eval_count: int | None = None
    done_reason: str = ""


class LLMAdapter(Protocol):
    def stream(self, request: LLMRequest) -> AsyncIterator[LLMFrame]: ...


class OllamaLLM:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gpt-oss:120b-cloud"):
        self.base_url = base_url
        self.model = model

    async def stream(self, request: LLMRequest) -> AsyncIterator[LLMFrame]:
        async with httpx.AsyncClient(timeout=180) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": request.messages,
                    "think": request.think,
                    "stream": True,
                    **({"format": request.format} if request.format is not None else {}),
                    "options": {"num_predict": request.num_predict, "temperature": 0},
                },
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    if data.get("error"):
                        raise ValueError(f"Ollama: {data['error']}")
                    message = data.get("message", {})
                    yield LLMFrame(
                        content=message.get("content", ""),
                        thinking=message.get("thinking", ""),
                        done=data.get("done", False),
                        prompt_eval_count=data.get("prompt_eval_count"),
                        eval_count=data.get("eval_count"),
                        done_reason=data.get("done_reason", ""),
                    )
