"""HTTP transport only; processing remains in the two application operations."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .application import Application
from .cache import ProcessingCache
from .embedder import OllamaEmbedder
from .events import Event
from .ingestion import UploadBusy
from .llm_adapter import OllamaLLM
from .llm_gateway import LLMGateway
from .settings import RetrievalSettings

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "frontend" / "dist"
CACHE_DIRECTORY = ROOT / ".cache"


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
        application = Application(
            OllamaEmbedder(base_url),
            LLMGateway(OllamaLLM(base_url)),
            settings=RetrievalSettings.from_env(),
            cache=ProcessingCache(CACHE_DIRECTORY),
        )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            yield
        finally:
            await application.close()

    app = FastAPI(title="Chat with Document", lifespan=lifespan)

    @app.post("/api/documents", status_code=202)
    async def upload_document(document: UploadFile):
        content = await document.read()
        try:
            job_id = application.start_upload(content, document.filename or "Document.pdf")
        except UploadBusy as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {"job_id": job_id, "events_url": f"/api/documents/{job_id}/events"}

    @app.get("/api/documents/{job_id}/events")
    async def upload_events(job_id: str):
        try:
            return sse(application.upload_events(job_id))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Upload job not found.") from exc

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
