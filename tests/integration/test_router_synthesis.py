import json

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway

from .fixtures import text_pdf


def router_script(question_type="Lookup", question="Standalone question", sub_queries=None):
    return json.dumps(
        dict(
            question_type=question_type, standalone_question=question, sub_queries=sub_queries or []
        )
    )


async def test_router_plan_drives_answer_and_is_recorded_with_json_schema():
    llm = ScriptedLLM([router_script(question="What does this Document say?"), "hello [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("What about it?")]
    assert events[0].type == "plan"
    assert events[0].standalone_question == "What does this Document say?"
    assert events[0].question_type == "Lookup"
    assert events[0].sub_queries == []
    assert [c.call_type for c in events[-1].calls] == ["router", "answer"]
    assert llm.calls[0].think == "low" and llm.calls[0].num_predict == 600
    assert llm.calls[0].format["required"] == [
        "question_type",
        "standalone_question",
        "sub_queries",
    ]
    assert "What does this Document say?" in llm.calls[-1].messages[-1]["content"]
    assert "What about it?" not in llm.calls[-1].messages[-1]["content"]


async def test_malformed_router_json_falls_back_to_lookup_with_original_question():
    llm = ScriptedLLM(["{broken json", "hello [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("Original question")]
    assert events[0].question_type == "Lookup"
    assert events[0].standalone_question == "Original question"
    assert events[0].sub_queries == []
    assert any(e.type == "final" for e in events)


async def test_too_long_question_has_explicit_rejection_event_and_zero_calls():
    from chat_document.events import EVENT_ADAPTER

    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("question " * 1001)]
    assert len(events) == 1
    event = events[0]
    assert event.type == "rejected"
    assert event.code == "question_too_long"
    assert event.token_limit == 1000 and event.question_tokens > 1000
    assert "1,000" in event.message
    assert EVENT_ADAPTER.validate_json(event.model_dump_json()) == event
    assert llm.calls == []


async def test_router_history_keeps_only_two_rounds_each_at_most_500_tokens():
    from chat_document.models import ConversationTurn
    from chat_document.tokens import count_tokens

    history = [
        ConversationTurn(question=f"Round {i} " + "q " * 280, answer=f"Answer {i} " + "a " * 800)
        for i in range(4)
    ]
    llm = ScriptedLLM([router_script(question="GraphRAG incremental updates"), "hello [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("那 GraphRAG 呢？", history=history)]
    assert any(e.type == "final" for e in events)
    messages = llm.calls[0].messages[1:-1]
    assert [m["role"] for m in messages] == ["user", "assistant", "user", "assistant"]
    for user, assistant in zip(messages[::2], messages[1::2], strict=True):
        assert count_tokens(user["content"]) + count_tokens(assistant["content"]) <= 500
    assert "Round 2" in messages[0]["content"] and "Round 3" in messages[2]["content"]
    answer_prompt = "\n".join(m["content"] for m in llm.calls[-1].messages)
    assert "Round 2" not in answer_prompt and "Answer 3" not in answer_prompt
