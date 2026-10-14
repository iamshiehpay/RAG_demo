"""Scripted text provider for deterministic tests and controlled retrieval experiments."""

from collections import deque
from collections.abc import AsyncIterator

from app.llm_adapter import LLMFrame, LLMRequest
from app.tokens import TOKENIZER, count_tokens, encode


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
