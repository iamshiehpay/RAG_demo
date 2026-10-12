"""HTTP transport only; processing remains in the two application operations."""

import os
from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .application import Application
from .embedder import OllamaEmbedder
from .events import Event
from .llm_adapter import OllamaLLM
from .llm_gateway import LLMGateway

DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


class AskRequest(BaseModel):
    question: str


def sse(events: AsyncIterator[Event]) -> StreamingResponse:
    async def stream():
        try:
            async for event in events:
                yield f"event: {event.type}\ndata: {event.model_dump_json()}\n\n"
        finally:
            await events.aclose()

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


def create_app(application: Application | None = None) -> FastAPI:
    if application is None:
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        application = Application(OllamaEmbedder(base_url), LLMGateway(OllamaLLM(base_url)))
    app = FastAPI(title="Chat with Document")

    @app.post("/api/documents")
    async def upload_document(document: UploadFile):
        content = await document.read()
        return sse(application.upload_document(content, document.filename or "Document.pdf"))

    @app.post("/api/ask")
    async def ask(request: AskRequest):
        return sse(application.ask(request.question))

    @app.get("/api/sources/{source_id}")
    async def source(source_id: str):
        try:
            return application.source(source_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Source not found.") from exc

    if DIST.exists():
        app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")
    return app
