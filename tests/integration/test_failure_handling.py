import httpx
import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import LLMFrame, ScriptedLLM
from chat_document.llm_gateway import LLMGateway

from .fixtures import text_pdf


async def uploaded_app(scripts, embedder=None):
    llm = ScriptedLLM(scripts)
    app = Application(embedder or OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    return app, llm


async def test_length_with_content_retries_low_once_and_finalizes_only_replacement():
    app, llm = await uploaded_app(
        [
            "not JSON",
            [LLMFrame(content="Discard me [C1]."), LLMFrame(done=True, done_reason="length")],
            "Replacement [C1].",
        ]
    )
    events = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in events] == [
        "plan",
        "retrieval",
        "citation_map",
        "delta",
        "retry",
        "delta",
        "final",
        "trace",
    ]
    assert events[-2].answer == "Replacement [C1]."
    assert app.history[-1].answer == "Replacement [C1]."
    assert [c.think for c in llm.calls] == ["low", "medium", "low"]
    assert llm.calls[1].messages == llm.calls[2].messages
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)
    assert [c.done_reason for c in events[-1].calls] == ["stop", "length", "stop"]


async def test_two_lengths_end_in_error_without_final_or_successful_history():
    app, llm = await uploaded_app(
        [
            "not JSON",
            [LLMFrame(content="First partial."), LLMFrame(done=True, done_reason="length")],
            [LLMFrame(content="Second partial."), LLMFrame(done=True, done_reason="length")],
        ]
    )
    events = [e async for e in app.ask("What does this say?")]
    assert events[-1].type == "error"
    assert [e.type for e in events].count("retry") == 1
    assert not any(e.type == "final" for e in events)
    assert app.history == []
    trace = next(e for e in events if e.type == "trace")
    assert [c.done_reason for c in trace.calls] == ["stop", "length", "length"]
    assert len(llm.calls) == 3


@pytest.mark.parametrize(
    "second", ["", httpx.ConnectError("Retry disconnected"), [LLMFrame(content="Unfinished")]]
)
async def test_failed_low_retry_never_finalizes_first_or_second_attempt(second):
    app, llm = await uploaded_app(
        [
            "not JSON",
            [LLMFrame(content="First partial"), LLMFrame(done=True, done_reason="length")],
            second,
        ]
    )
    events = [e async for e in app.ask("What does this say?")]
    assert events[-1].type == "error"
    assert [e.type for e in events].count("retry") == 1
    assert not any(e.type == "final" for e in events)
    assert app.history == []
    assert len(llm.calls) == 3


async def test_invalid_citation_flags_only_its_sentence_and_counts_in_trace():
    app, _ = await uploaded_app(
        ["not JSON", "Intro without a Citation. Supported [C1]. Invented [C99]. 文件中未提及。"]
    )
    events = [e async for e in app.ask("What does this say?")]
    final = next(e for e in events if e.type == "final")
    assert final.answer == ("Intro without a Citation. Supported [C1]. Invented. 文件中未提及。")
    assert [final.answer[s.start : s.end] for s in final.unverified] == ["Invented."]
    assert [c.id for c in final.citations] == ["C1"]
    assert events[-1].invalid_citation_count == 1


async def test_thinking_streams_before_answer_and_preserves_split_citation():
    app, _ = await uploaded_app(
        [
            "not JSON",
            [
                LLMFrame(thinking="Check "),
                LLMFrame(thinking="the evidence."),
                LLMFrame(content="Supported [C"),
                LLMFrame(thinking="Still checking."),
                LLMFrame(content="1]."),
                LLMFrame(done=True, done_reason="stop"),
            ],
        ]
    )
    events = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in events][:5] == [
        "plan",
        "retrieval",
        "citation_map",
        "thinking",
        "thinking",
    ]
    assert "".join(e.text for e in events if e.type == "thinking") == (
        "Check the evidence.Still checking."
    )
    final = next(e for e in events if e.type == "final")
    assert final.answer == "Supported [C1]."
    assert "".join(e.text for e in events if e.type == "delta") == final.answer
    assert events[-1].calls[-1].thinking == "Check the evidence.Still checking."
    assert app.history[-1].answer == final.answer


async def test_unverified_prose_stays_plain_and_only_invalid_sentence_has_structured_span():
    app, _ = await uploaded_app(["not JSON", "論文中的假設仍未驗證[C1]。🙂 這句錯誤[C99]。"])
    events = [e async for e in app.ask("What does this say?")]
    final = next(e for e in events if e.type == "final")
    assert final.answer == "論文中的假設仍未驗證[C1]。🙂 這句錯誤。"
    assert [final.answer[s.start : s.end] for s in final.unverified] == ["🙂 這句錯誤。"]
    assert app.history[-1].answer == final.answer
    assert events[-1].invalid_citation_count == 1


@pytest.mark.parametrize("abbreviation", ["vs.", "e.g.", "i.e.", "et al."])
async def test_unverified_span_preserves_abbreviated_sentence_and_collapses_removed_id_spaces(
    abbreviation,
):
    sentence = f"Result {abbreviation} the baseline [C99] remains 64.8%."
    app, _ = await uploaded_app(["not JSON", f"Intro [C1]. {sentence} Next [C1]."])
    events = [e async for e in app.ask("What does this say?")]
    final = next(e for e in events if e.type == "final")
    expected = f"Result {abbreviation} the baseline remains 64.8%."
    assert final.answer == f"Intro [C1]. {expected} Next [C1]."
    assert [final.answer[s.start : s.end] for s in final.unverified] == [expected]


async def test_citations_after_punctuation_flag_the_preceding_sentence_only():
    app, _ = await uploaded_app(
        [
            "not JSON",
            "Known 64.8%. [C1] Unknown 60.0%. [C99][C99] Next uncited.\n無效[C99]。有效[C1]。",
        ]
    )
    events = [e async for e in app.ask("What does this say?")]
    final = next(e for e in events if e.type == "final")
    assert [final.answer[s.start : s.end] for s in final.unverified] == ["Unknown 60.0%.", "無效。"]
    assert final.answer == ("Known 64.8%. [C1] Unknown 60.0%. Next uncited.\n無效。有效[C1]。")
    assert events[-1].invalid_citation_count == 3


@pytest.mark.parametrize("marker", ["[C1 C3]", "[C1–C3]", "【C1-C3】", "[C1—C3]"])
async def test_space_and_range_citations_normalize_across_frames(marker):
    from .fixtures import paragraph_pdf

    llm = ScriptedLLM(
        [
            "not JSON",
            [
                *[LLMFrame(content=c) for c in f"Evidence {marker}."],
                LLMFrame(done=True, done_reason="stop"),
            ],
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [
        e
        async for e in app.upload_document(
            paragraph_pdf("Evidence about the Document. " * 500), "sample.pdf"
        )
    ][-1].type == "ready"
    events = [e async for e in app.ask("What does this say?")]
    final = next(e for e in events if e.type == "final")
    expected = "Evidence [C1][C3]." if marker == "[C1 C3]" else "Evidence [C1][C2][C3]."
    assert final.answer == expected
    assert "".join(e.text for e in events if e.type == "delta") == expected
    assert final.unverified == []
    assert events[-1].invalid_citation_count == 0


@pytest.mark.parametrize("marker", ["[C1–C3]", "[C1–C999999999]", "[C3–C1]", "[C1–S1]"])
async def test_invalid_range_is_not_expanded_into_valid_sources(marker):
    app, _ = await uploaded_app(["not JSON", f"Untrusted {marker}. Supported [C1]."])
    events = [e async for e in app.ask("What does this say?")]
    final = next(e for e in events if e.type == "final")
    assert final.answer == "Untrusted. Supported [C1]."
    assert [final.answer[s.start : s.end] for s in final.unverified] == ["Untrusted."]
    assert [c.id for c in final.citations] == ["C1"]
    assert events[-1].invalid_citation_count == 1


async def test_synthesis_extraction_range_uses_each_batch_citation_map():
    import json
    import re

    from chat_document.settings import RetrievalSettings

    from .fixtures import paragraph_pdf

    class RangeExtractionLLM(ScriptedLLM):
        def __init__(self):
            super().__init__([])
            self.extracted_ids = []

        async def stream(self, request):
            if request.format is not None:
                script = json.dumps(
                    dict(
                        question_type="Synthesis",
                        standalone_question="Compare facts",
                        sub_queries=["facts"],
                    )
                )
            elif request.num_predict == 1000:
                ids = list(dict.fromkeys(re.findall(r"C\d+", request.messages[-1]["content"])))
                selected = ids[:3]
                self.extracted_ids.extend(selected)
                script = f"Range fact [{selected[0]}–{selected[-1]}]."
            else:
                script = "Final [C1]."
            self.scripts.append(script)
            async for frame in super().stream(request):
                yield frame

    llm = RangeExtractionLLM()
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(synthesis_top_k=30)
    )
    assert [
        e
        async for e in app.upload_document(
            paragraph_pdf("Evidence about the Document. " * 1500), "sample.pdf"
        )
    ][-1].type == "ready"
    events = [e async for e in app.ask("Compare facts")]
    assert any(e.type == "final" for e in events), [
        e.model_dump() for e in events if e.type == "error"
    ]
    prompt = llm.calls[-1].messages[-1]["content"]
    assert "Range fact [C1][C2][C3]." in prompt
    assert all(f"[{id}]" in prompt for id in llm.extracted_ids)
    assert all(c.discarded_fact_lines == 0 for c in events[-1].calls)


@pytest.mark.parametrize("failure_stage", ["router", "embedding", "answer"])
@pytest.mark.parametrize("failure_type", [httpx.ConnectError, httpx.ReadTimeout])
async def test_transport_failure_stops_downstream_work_and_same_question_can_retry(
    failure_stage, failure_type
):
    class RecordingEmbedder(OllamaEmbedder):
        def __init__(self):
            super().__init__()
            self.calls = []
            self.fail = False

        async def embed(self, texts):
            self.calls.append(texts)
            if self.fail:
                raise failure_type("Query embedding unavailable")
            return await super().embed(texts)

    failure = failure_type("Service unavailable")
    scripts = [failure] if failure_stage == "router" else ["not JSON"]
    if failure_stage == "answer":
        scripts.append(failure)
    scripts += ["not JSON", "Recovered [C1]."]
    embedder = RecordingEmbedder()
    app, llm = await uploaded_app(scripts, embedder)
    embedder.fail = failure_stage == "embedding"
    events = [e async for e in app.ask("What does this say?")]
    assert events[-1].type == "error"
    assert events[-1].code == f"{failure_stage}_failed"
    assert failure_stage.capitalize() in events[-1].message
    assert "local Ollama daemon" in events[-1].message
    assert not any(e.type in {"retry", "final"} for e in events)
    assert app.history == []
    assert len(llm.calls) == (2 if failure_stage == "answer" else 1)
    assert len(embedder.calls) == (1 if failure_stage == "router" else 2)
    if failure_stage != "answer":
        assert not any(e.type in {"retrieval", "citation_map", "delta"} for e in events)
    embedder.fail = False
    recovered = [e async for e in app.ask("What does this say?")]
    assert next(e for e in recovered if e.type == "final").answer == "Recovered [C1]."
