from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway


@pytest.mark.asyncio
async def test_upload_document_and_ask_with_real_embedding_and_recorded_llm():
    llm = ScriptedLLM(["Ablation variants are compared with NaiveRAG. [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    uploaded = [
        event
        async for event in app.upload_document(
            Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf"
        )
    ]
    assert uploaded[-1].type == "ready"
    document = app.document
    assert document is not None
    assert len(document.sections) == 16
    assert all(chunk.section_id for chunk in document.chunks)
    events = [event async for event in app.ask("Performance of ablated versions of LightRAG")]
    assert [event.type for event in events] == [
        "plan",
        "retrieval",
        "citation_map",
        "delta",
        "final",
        "trace",
    ]
    assert len(events[1].chunks) == 5
    assert events[4].citations[0].id == "C1"
    source = app.source(events[4].citations[0].source_id)
    assert source.text and source.page_start >= 1
    assert llm.calls
    for call in llm.calls:
        assert call.estimated_prompt_tokens + call.num_predict <= 10_000
        assert call.think == "medium" and call.num_predict == 3000
    trace = events[-1].calls[0]
    assert trace.prompt_eval_count == 100
    assert trace.estimated_prompt_tokens == llm.calls[0].estimated_prompt_tokens


async def test_guard_emits_error_without_final_or_llm_call():
    from .fixtures import text_pdf

    llm = ScriptedLLM(["Should never run"])
    app = Application(OllamaEmbedder(), LLMGateway(llm, context_budget=1))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does the Document say?")]
    assert result[-1].type == "error"
    assert result[-1].code == "budget_exceeded"
    assert "final" not in [e.type for e in result]
    assert llm.calls == []
