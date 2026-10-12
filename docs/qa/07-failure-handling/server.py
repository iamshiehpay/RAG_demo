"""Controlled #07 browser fixture: real Application/Gateway/bge-m3, scripted LLM only."""

import asyncio

import httpx
from fastapi import FastAPI

from chat_document.api import create_app
from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import LLMFrame, ScriptedLLM
from chat_document.llm_gateway import LLMGateway


class ControlledLLM(ScriptedLLM):
    def __init__(self):
        super().__init__(
            [
                "not JSON",
                [
                    LLMFrame(thinking="First attempt thinking."),
                    LLMFrame(content="Discarded provisional [C1]."),
                    LLMFrame(done=True, done_reason="length"),
                ],
                [
                    LLMFrame(thinking="Retry thinking."),
                    LLMFrame(content="Verified [C1]. Invented [C99]."),
                    LLMFrame(done=True, done_reason="stop"),
                ],
                "not JSON",
                [
                    LLMFrame(content="First truncated answer."),
                    LLMFrame(done=True, done_reason="length"),
                ],
                [
                    LLMFrame(content="Second truncated answer."),
                    LLMFrame(done=True, done_reason="length"),
                ],
                "not JSON",
                "Recovered same question [C1].",
                httpx.ReadTimeout("Router timeout"),
                "not JSON",
                "Recovered Router question [C1].",
            ]
        )
        self.answer_count = 0
        self.gates = {"first": asyncio.Event(), "retry": asyncio.Event()}

    async def stream(self, request):
        if request.format is not None:
            async for frame in super().stream(request):
                yield frame
            return
        self.answer_count += 1
        async for frame in super().stream(request):
            if self.answer_count == 1 and frame.done:
                await self.gates["first"].wait()
            if self.answer_count == 2 and frame.content:
                await self.gates["retry"].wait()
            yield frame


llm = ControlledLLM()
application = Application(OllamaEmbedder(), LLMGateway(llm))
app = FastAPI()


@app.post("/qa/release/{gate}")
async def release(gate: str):
    llm.gates[gate].set()
    return {"released": gate}


app.mount("/", create_app(application))
