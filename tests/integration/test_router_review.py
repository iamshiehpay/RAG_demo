import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway

from .fixtures import text_pdf
from .test_router_synthesis import router_script


@pytest.mark.parametrize(
    "question_type,queries,expected",
    [
        ("Synthesis", [], []),
        ("Synthesis", ["cost"], ["cost"]),
        ("Synthesis", [f"query {i}" for i in range(8)], [f"query {i}" for i in range(5)]),
        ("Lookup", ["cost"], []),
        ("Global", ["cost"], []),
    ],
)
async def test_schema_valid_router_plan_preserves_follow_up_rewrite(
    question_type, queries, expected
):
    standalone = "比較 LightRAG 與 GraphRAG。"
    llm = ScriptedLLM([router_script(question_type, standalone, queries), "Evidence [C1]."])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("那它跟 GraphRAG 比呢？")]
    plan = events[0]
    assert plan.question_type == question_type
    assert plan.standalone_question == standalone
    assert plan.sub_queries == expected
    assert standalone in llm.calls[-1].messages[-1]["content"]
    assert any(e.type == "final" for e in events)


async def test_extraction_normalizes_citations_discards_headings_and_filters_sentinel():
    from pathlib import Path

    from chat_document.settings import RetrievalSettings

    class NormalizationScript(ScriptedLLM):
        batches = 0

        async def stream(self, request):
            if request.format is not None:
                script = router_script("Synthesis", "Compare costs.", ["cost", "update"])
            elif request.call_type == "fact_extraction":
                self.batches += 1
                script = (
                    "Facts\nBoth [C1, C3]\nOther 【C3†L1-L4】\n"
                    "No supported relevant fact found [C1]\nUncited sentence."
                    if self.batches == 1
                    else "No supported relevant fact found"
                )
            else:
                script = "Combined [C1][C3]."
            self.scripts.append(script)
            async for frame in super().stream(request):
                yield frame

    llm = NormalizationScript([])
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(synthesis_top_k=30)
    )
    assert [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ][-1].type == "ready"
    events = [e async for e in app.ask("Compare costs.")]
    assert any(e.type == "final" for e in events)
    prompt = llm.calls[-1].messages[-1]["content"]
    assert "Both [C1][C3]" in prompt and "Other [C3]" in prompt
    assert "No supported relevant fact found" not in prompt
    assert "Uncited sentence" not in prompt
    traces = [c for c in events[-1].calls if c.call_type == "fact_extraction"]
    assert len(traces) >= 2
    assert traces[0].discarded_fact_lines == 3
    assert all(c.discarded_fact_lines == 1 for c in traces[1:])
    final = next(e for e in events if e.type == "final")
    assert {c.id for c in final.citations} == {"C1", "C3"}


async def test_lookup_with_large_top_k_fits_without_extraction():
    from pathlib import Path

    from chat_document.settings import RetrievalSettings

    llm = ScriptedLLM([router_script("Lookup", "retrieval cost"), "Supported [C1]."])
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(lookup_top_k=30)
    )
    assert [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ][-1].type == "ready"
    events = [e async for e in app.ask("What is the retrieval cost?")]
    assert any(e.type == "final" for e in events)
    assert [c.call_type for c in events[-1].calls] == ["router", "answer"]
    assert len(events[1].chunks) < 30
    assert llm.calls[-1].estimated_prompt_tokens + llm.calls[-1].num_predict <= 10000


async def test_truncated_router_falls_back_but_retains_its_failed_trace():
    from chat_document.llm_adapter import LLMFrame

    llm = ScriptedLLM(
        [
            [LLMFrame(content="{partial"), LLMFrame(done=True, done_reason="length")],
            "Supported [C1].",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("Original question")]
    assert events[0].question_type == "Lookup"
    assert events[0].standalone_question == "Original question"
    assert events[0].plan_source == "fallback" and events[0].fallback_reason == "length"
    assert any(e.type == "final" for e in events)
    assert [c.done_reason for c in events[-1].calls] == ["length", "stop"]
    assert events[-1].calls[0].plan_source == "fallback"
    assert events[-1].calls[0].fallback_reason == "length"


async def test_explicit_history_does_not_modify_session_history():
    from chat_document.models import ConversationTurn

    llm = ScriptedLLM([router_script(), "Session [C1].", router_script(), "Evaluation [C1]."])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    assert any(e.type == "final" for e in [e async for e in app.ask("Session question")])
    before = app.history.copy()
    events = [
        e
        async for e in app.ask(
            "Eval question",
            history=[ConversationTurn(question="Fixture question", answer="Fixture answer")],
        )
    ]
    assert any(e.type == "final" for e in events)
    assert app.history == before
    assert llm.calls[2].messages[1]["content"] == "Fixture question"


async def test_scripted_llm_honors_output_reservation_including_thinking():
    from chat_document.llm_adapter import LLMFrame
    from chat_document.tokens import count_tokens

    llm = ScriptedLLM(
        [
            "{" + "broken " * 700,
            "Supported [C1].",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("Original question")]
    assert any(e.type == "final" for e in events)
    assert events[-1].calls[0].done_reason == "length"
    assert events[-1].calls[0].eval_count == 600
    # Explicit frames also count thinking, which shares the same output reservation.
    request = llm.calls[0]
    framed = ScriptedLLM(
        [
            [
                LLMFrame(thinking="thinking " * 500),
                LLMFrame(content="answer " * 500),
                LLMFrame(done=True, done_reason="stop"),
            ]
        ]
    )
    frames = [f async for f in framed.stream(request)]
    assert frames[-1].done_reason == "length" and frames[-1].eval_count == 600
    assert (
        count_tokens("".join(f.thinking for f in frames))
        + count_tokens("".join(f.content for f in frames))
        <= 600
    )
