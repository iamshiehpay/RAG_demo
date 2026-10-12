import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway

from .fixtures import scanned_pdf, text_pdf


@pytest.mark.parametrize(
    "content", [b"not a PDF", b"", text_pdf("")[:-100]], ids=["non-pdf", "empty", "truncated"]
)
async def test_invalid_document_has_a_distinct_error_from_missing_text_layer(content):
    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(content, "invalid.pdf")]
    assert [e.type for e in events] == ["stage", "error"]
    assert events[-1].code == "invalid_document"
    assert "valid PDF" in events[-1].message
    assert "text layer" not in events[-1].message
    assert app.document is None and llm.calls == []


async def test_image_only_document_reports_missing_text_layer_before_embedding():
    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(scanned_pdf(), "scan.pdf")]
    assert [e.type for e in events] == ["stage", "error"]
    assert events[-1].code == "invalid_document"
    assert "no text layer" in events[-1].message
    assert "scanned PDFs" in events[-1].message
    assert app.document is None and llm.calls == []
