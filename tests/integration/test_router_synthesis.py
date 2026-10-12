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
    assert (
        "Current user question (language reference): What about it?"
        in (llm.calls[-1].messages[-1]["content"])
    )


async def test_malformed_router_json_falls_back_to_lookup_with_original_question():
    llm = ScriptedLLM(["{broken json", "hello [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("Original question")]
    assert events[0].question_type == "Lookup"
    assert events[0].standalone_question == "Original question"
    assert events[0].sub_queries == []
    assert any(e.type == "final" for e in events)
    assert events[0].plan_source == "fallback" and events[0].fallback_reason == "invalid_json"
    assert events[-1].calls[0].fallback_reason == "invalid_json"


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


async def test_q2_sub_queries_cover_cost_and_incremental_update_in_document_order():
    from pathlib import Path

    from chat_document.settings import RetrievalSettings

    llm = ScriptedLLM(
        [
            router_script("Lookup", "Compare LightRAG with GraphRAG."),
            "Baseline [C1].",
            router_script(
                "Synthesis",
                "Compare LightRAG with GraphRAG.",
                [
                    "LightRAG GraphRAG retrieval cost token consumption 610 1000 API calls",
                    "LightRAG GraphRAG incremental updates new data community reconstruction",
                ],
            ),
            "Cost and incremental updates [C1].",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(lookup_top_k=3))
    assert [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ][-1].type == "ready"
    baseline = [e async for e in app.ask("Compare LightRAG with GraphRAG.", history=[])]
    assert len(baseline[1].chunks) == 3
    assert not any("610" in item.chunk.text for item in baseline[1].chunks)
    events = [e async for e in app.ask("Compare LightRAG with GraphRAG.", history=[])]
    plan, retrieval = events[:2]
    assert plan.question_type == "Synthesis" and len(plan.sub_queries) == 2
    chunks = [item.chunk for item in retrieval.chunks]
    text = "\n".join(c.text for c in chunks).lower()
    assert "610" in text and "incremental" in text
    assert any("community" in c.text.lower() and "update" in c.text.lower() for c in chunks)
    assert len(chunks) <= 7
    assert len({c.id for c in chunks}) == len(chunks)
    assert [c.order for c in chunks] == sorted(c.order for c in chunks)
    answer_prompt = llm.calls[-1].messages[-1]["content"]
    for number, chunk in enumerate(chunks, 1):
        assert f"[C{number}] {chunk.context}" in answer_prompt


async def test_oversized_synthesis_extracts_facts_and_keeps_original_citation_sources():
    from pathlib import Path

    from chat_document.settings import RetrievalSettings
    from chat_document.tokens import count_tokens

    llm = ScriptedLLM(
        [
            router_script(
                "Synthesis",
                "Compare costs and incremental updates.",
                [
                    "retrieval costs",
                    "incremental updates",
                ],
            ),
            "Retrieval fact [C1].",
            "Incremental update fact [C20].",
            "Combined answer [C1][C20].",
        ]
    )
    app = Application(
        OllamaEmbedder(),
        LLMGateway(llm),
        settings=RetrievalSettings(synthesis_top_k=30, sub_query_top_k=2),
    )
    assert [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ][-1].type == "ready"
    events = [e async for e in app.ask("Compare costs and incremental updates.")]
    assert any(e.type == "final" for e in events), [
        e.model_dump() for e in events if e.type == "error"
    ]
    assert [c.call_type for c in events[-1].calls] == [
        "router",
        "fact_extraction",
        "fact_extraction",
        "answer",
    ]
    citation_map = next(e.citations for e in events if e.type == "citation_map")
    final = next(e for e in events if e.type == "final")
    assert {c.id for c in final.citations} == {"C1", "C20"}
    for citation in final.citations:
        assert citation == next(c for c in citation_map if c.id == citation.id)
        assert app.source(citation.source_id).text
    answer_prompt = llm.calls[-1].messages[-1]["content"]
    assert "Retrieval fact [C1]." in answer_prompt
    assert "Incremental update fact [C20]." in answer_prompt
    assert count_tokens(answer_prompt) < 6700
    for call in llm.calls:
        assert call.estimated_prompt_tokens + call.num_predict <= 10000


async def test_extracted_facts_are_reduced_again_when_they_still_do_not_fit():
    import re

    import pymupdf

    from chat_document.settings import RetrievalSettings
    from chat_document.tokens import count_tokens

    from .fixtures import paragraph_pdf

    class ExtractionScript(ScriptedLLM):
        def __init__(self):
            super().__init__([])
            self.first_pass_facts = []

        async def stream(self, request):
            if request.format is not None:
                script = router_script("Synthesis", "Compare costs and incremental updates.", [])
            elif request.num_predict == 1000:
                evidence = request.messages[-1]["content"].split("Evidence:\n", 1)[1]
                ids = list(dict.fromkeys(re.findall(r"\[C\d+\]", evidence)))
                if "retrieval cost incremental updates." in evidence:
                    script = "cost " * 900 + ids[0]
                    self.first_pass_facts.append(script)
                else:
                    script = "Compressed cost " + "".join(ids)
            else:
                script = "Combined answer [C1]."
            assert count_tokens(script) <= request.num_predict
            self.scripts.append(script)
            async for frame in super().stream(request):
                yield frame

    # Enough raw evidence for >6 first-pass batches. Each result stays below 1,000 tokens,
    # yet their total exceeds 6,000 and requires a real second reduction pass.
    with (
        pymupdf.open(
            stream=paragraph_pdf("retrieval cost incremental updates. " * 1800), filetype="pdf"
        ) as source,
        pymupdf.open() as document,
    ):
        for _ in range(7):
            document.insert_pdf(source)
        content = document.tobytes()
    llm = ExtractionScript()
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(synthesis_top_k=1000)
    )
    assert [e async for e in app.upload_document(content, "long.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("Compare costs and incremental updates.")]
    assert any(e.type == "final" for e in events), [
        e.model_dump() for e in events if e.type == "error"
    ]
    assert count_tokens("\n\n".join(llm.first_pass_facts)) > 6000
    extraction = [c for c in events[-1].calls if c.call_type == "fact_extraction"]
    assert len(extraction) > len(llm.first_pass_facts)
    assert all(c.eval_count <= 1000 and c.done_reason == "stop" for c in extraction)
    final = next(e for e in events if e.type == "final")
    assert final.citations[0].id == "C1"
    assert app.source(final.citations[0].source_id).text
    assert "Compressed cost [C1]" in llm.calls[-1].messages[-1]["content"]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


async def test_configurable_top_k_counts_and_global_temporarily_uses_synthesis():
    from pathlib import Path

    from chat_document.settings import RetrievalSettings

    question = "LightRAG retrieval costs"
    llm = ScriptedLLM(
        [
            router_script("Lookup", question),
            "Lookup [C1].",
            router_script("Synthesis", question, [question, question]),
            "Synthesis [C1].",
            router_script("Global", question),
            "Global [C1].",
        ]
    )
    app = Application(
        OllamaEmbedder(),
        LLMGateway(llm),
        settings=RetrievalSettings(lookup_top_k=2, synthesis_top_k=1, sub_query_top_k=4),
    )
    assert [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ][-1].type == "ready"
    for expected_type, expected_count in [("Lookup", 2), ("Synthesis", 4), ("Global", 1)]:
        events = [e async for e in app.ask(question, history=[])]
        assert events[0].question_type == expected_type
        assert len(events[1].chunks) == expected_count
        assert any(e.type == "final" for e in events)
    assert RetrievalSettings().model_dump() == dict(
        lookup_top_k=5, synthesis_top_k=3, sub_query_top_k=2
    )


async def test_router_transport_failure_stops_before_query_embedding():
    import httpx

    class RecordingEmbedder(OllamaEmbedder):
        def __init__(self):
            super().__init__()
            self.calls = []

        async def embed(self, texts):
            self.calls.append(texts)
            return await super().embed(texts)

    embedder = RecordingEmbedder()
    llm = ScriptedLLM([httpx.ReadTimeout("Router timeout")])
    app = Application(embedder, LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in events] == ["trace", "error"]
    assert events[-2].calls[0].call_type == "router"
    assert len(llm.calls) == 1 and len(embedder.calls) == 1


async def test_successful_turns_supply_history_to_later_follow_up():
    llm = ScriptedLLM(
        [
            router_script(question="LightRAG incremental updates"),
            "Incremental updates [C1].",
            router_script(question="GraphRAG 如何進行增量更新？"),
            "GraphRAG updates [C1].",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    assert any(e.type == "final" for e in [e async for e in app.ask("How does LightRAG update?")])
    events = [e async for e in app.ask("那 GraphRAG 呢？")]
    assert events[0].standalone_question == "GraphRAG 如何進行增量更新？"
    assert llm.calls[2].messages[1:3] == [
        dict(role="user", content="How does LightRAG update?"),
        dict(role="assistant", content="Incremental updates [C1]."),
    ]


async def test_query_embedding_failure_does_not_start_answer_generation():
    import httpx

    class FailingQueryEmbedder(OllamaEmbedder):
        async def embed(self, texts):
            if texts == ["Standalone question"]:
                raise httpx.ConnectError("Embedding unavailable")
            return await super().embed(texts)

    llm = ScriptedLLM([router_script(), "Must not run"])
    app = Application(FailingQueryEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in events] == ["plan", "trace", "error"]
    assert len(llm.calls) == 1
    assert [c.call_type for c in events[-2].calls] == ["router"]


async def test_extraction_losing_citation_ids_fails_without_final_answer():
    from pathlib import Path

    from chat_document.settings import RetrievalSettings

    llm = ScriptedLLM(
        [
            router_script("Synthesis", "Compare costs.", ["cost", "update"]),
            "An uncited extracted fact.",
            "No supported relevant fact found",
        ]
    )
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(synthesis_top_k=30)
    )
    assert [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ][-1].type == "ready"
    events = [e async for e in app.ask("Compare costs.")]
    assert not any(e.type == "final" for e in events)
    assert not any(e.type == "delta" for e in events)  # Extraction text is not answer text.
    assert "Citation IDs" in next(e.message for e in events if e.type == "error")
    assert [c.call_type for c in events[-2].calls] == [
        "router",
        "fact_extraction",
        "fact_extraction",
    ]
    assert len(llm.calls) == 3
    assert all(c.discarded_fact_lines == 1 for c in events[-2].calls[1:])
