"""Native Ollama text→text adapter and recorded scripted fake at the same seam."""

import json
from collections import deque
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Literal, Protocol

import httpx

from .tokens import TOKENIZER, count_tokens, encode


@dataclass(frozen=True)
class LLMRequest:
    messages: list[dict[str, str]]
    think: Literal["low", "medium"]
    num_predict: int
    estimated_prompt_tokens: int
    format: dict | None = None


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


class ScriptedLLM:
    """Each script is a text response or an explicit stream, including failure frames."""

    def __init__(self, scripts: list[str | list[LLMFrame] | Exception]):
        self.scripts = deque(scripts)
        self.calls: list[LLMRequest] = []

    async def stream(self, request: LLMRequest) -> AsyncIterator[LLMFrame]:
        self.calls.append(request)
        script = self.scripts.popleft()
        if isinstance(script, Exception):
            raise script
        if isinstance(script, str):
            script = [
                LLMFrame(content=script),
                LLMFrame(
                    done=True,
                    prompt_eval_count=100,
                    eval_count=count_tokens(script),
                    done_reason="stop",
                ),
            ]
        content = thinking = ""
        for frame in script:
            next_tokens = count_tokens(content + frame.content) + count_tokens(
                thinking + frame.thinking
            )
            if next_tokens > request.num_predict:
                remaining = request.num_predict - count_tokens(content) - count_tokens(thinking)

                def prefix(text: str, limit: int) -> str:
                    ids = encode(text)[: max(0, limit)]
                    return TOKENIZER.decode_bytes(ids).decode("utf-8", errors="ignore")

                partial_thinking = prefix(frame.thinking, remaining)
                remaining -= count_tokens(partial_thinking)
                partial_content = prefix(frame.content, remaining)
                yield LLMFrame(content=partial_content, thinking=partial_thinking)
                yield LLMFrame(
                    done=True,
                    prompt_eval_count=100,
                    eval_count=request.num_predict,
                    done_reason="length",
                )
                return
            content += frame.content
            thinking += frame.thinking
            yield frame
