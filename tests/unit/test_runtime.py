"""Focused regressions grouped by feature; helpers remain outside test modules."""

import subprocess
import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from app.api import CACHE_DIRECTORY, DIST, create_app


async def test_checkout_serves_committed_frontend_and_rejects_ask_before_upload():
    root = Path(__file__).resolve().parents[2]
    assert DIST == root / "frontend" / "dist"
    assert CACHE_DIRECTORY == root / ".cache"
    async with AsyncClient(
        transport=ASGITransport(app=create_app()), base_url="http://test"
    ) as client:
        page = await client.get("/")
        assert page.status_code == 200
        assert page.content == (DIST / "index.html").read_bytes()
        response = await client.post("/api/ask", json={"question": "文件內容是什麼？"})
        assert "document_not_ready" in response.text
        assert "event: final" not in response.text


async def test_processing_prepares_a_document_without_publishing_application_state():
    import numpy as np

    from app.ingestion import PreparedDocument, process_document
    from app.llm_gateway import LLMGateway
    from app.settings import RetrievalSettings
    from app.summary_tree import SummaryTreeBuilder
    from tests.support import SummaryScriptedLLM, text_pdf

    class Embedder:
        model = "fake"

        async def embed(self, texts):
            return np.ones((len(texts), 3), dtype=np.float32)

    events = [
        event
        async for event in process_document(
            text_pdf(),
            "sample.pdf",
            embedder=Embedder(),
            summary_builder=SummaryTreeBuilder(LLMGateway(SummaryScriptedLLM([]))),
            settings=RetrievalSettings(),
            cache=None,
        )
    ]
    prepared = events[-1]
    assert isinstance(prepared, PreparedDocument)
    assert prepared.document.name == "sample.pdf"
    assert prepared.document.chunks
    assert prepared.document.summary_tree is not None
    assert prepared.index.chunks == prepared.document.chunks
    assert not prepared.cached
    assert events[0].stage == "parsing"


@pytest.mark.parametrize(
    "module",
    ["pdf_layout.py", "pdf_sections.py", "table_layout.py", "table_grid.py", "ingestion.py"],
)
def test_processing_changes_in_new_modules_invalidate_cache(module, monkeypatch):
    from app.cache import _pipeline_version

    before = _pipeline_version()
    original = Path.read_bytes

    def changed_source(path):
        content = original(path)
        if path.name == module and path.parent.name == "app":
            content += b"\n# changed processing semantics\n"
        return content

    monkeypatch.setattr(Path, "read_bytes", changed_source)
    assert _pipeline_version() != before


def test_frontend_types_match_backend_event_models():
    result = subprocess.run(
        [sys.executable, "scripts/generate_event_types.py", "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
