from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.policy import CONTEXT_BUDGET, QUESTION_TOKEN_LIMIT, SAFETY_MARGIN
from chat_document.tokens import count_tokens


@pytest.mark.asyncio
async def test_upload_document_and_ask_with_real_embedding_and_recorded_llm():
    llm = ScriptedLLM(["not JSON", "Ablation variants are compared with NaiveRAG. [C1]"])
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
    assert any(s.title == "1 INTRODUCTION" for s in document.sections)
    assert all(s.title != "REFERENCES" for s in document.sections)
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
        prompt_tokens = sum(count_tokens(m["content"]) for m in call.messages) + SAFETY_MARGIN
        assert prompt_tokens + call.num_predict <= CONTEXT_BUDGET
        if call.format is not None:
            import json

            prompt_tokens += count_tokens(json.dumps(call.format, ensure_ascii=False))
        assert prompt_tokens == call.estimated_prompt_tokens
        if call is llm.calls[0]:
            assert call.think == "low" and call.num_predict == 600
            continue
        system = call.messages[0]["content"]
        assert "EVERY factual claim" in system
        assert "文件中未提及" in system and "Not mentioned in the document." in system
        assert call.think == "medium" and call.num_predict == 3000
    trace = events[-1].calls[0]
    assert trace.safety_margin == SAFETY_MARGIN
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


async def test_scanned_document_is_rejected_before_embedding_or_llm():
    from .fixtures import text_pdf

    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    result = [event async for event in app.upload_document(text_pdf(""), "scan.pdf")]
    assert result[-1].type == "error"
    assert result[-1].code == "invalid_document"
    assert "text layer" in result[-1].message
    assert app.document is None
    assert llm.calls == []


async def test_questions_over_1000_tokens_never_call_llm():
    from .fixtures import text_pdf

    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("question " * (QUESTION_TOKEN_LIMIT + 1))]
    assert [e.type for e in result] == ["rejected"]
    assert result[0].code == "question_too_long"
    assert llm.calls == []


async def test_truncated_answer_never_becomes_final():
    from chat_document.llm_adapter import LLMFrame

    from .fixtures import text_pdf

    llm = ScriptedLLM(
        [
            "not JSON",
            [LLMFrame(content="Partial [C1]"), LLMFrame(done=True, done_reason="length")],
            [LLMFrame(done=True, done_reason="length")],
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    assert "delta" in [e.type for e in result]
    assert any(e.type == "error" for e in result)
    assert "final" not in [e.type for e in result]
    assert result[-1].type == "error"
    assert result[-2].calls[-1].done_reason == "length"


async def test_citation_markers_split_across_stream_frames_remain_clickable():
    from chat_document.llm_adapter import LLMFrame

    from .fixtures import text_pdf

    llm = ScriptedLLM(
        [
            "not JSON",
            [
                LLMFrame(content="A claim 【"),
                LLMFrame(content="C1"),
                LLMFrame(content="】."),
                LLMFrame(done=True, prompt_eval_count=100, eval_count=10, done_reason="stop"),
            ],
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    final = next(e for e in result if e.type == "final")
    assert final.answer == "A claim [C1]."
    assert "".join(e.text for e in result if e.type == "delta") == final.answer
    assert final.citations[0].id == "C1"
    assert app.source(final.citations[0].source_id).text == "hello Document"


async def test_interrupted_llm_stream_emits_error_and_failed_call_trace():
    from chat_document.llm_adapter import LLMFrame

    from .fixtures import text_pdf

    llm = ScriptedLLM(["not JSON", [LLMFrame(content="Unfinished answer [C1]")]])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in result][-2:] == ["trace", "error"]
    assert "final" not in [e.type for e in result]
    assert "completion record" in result[-1].message
    assert result[-2].calls[-1].done_reason == "error"
