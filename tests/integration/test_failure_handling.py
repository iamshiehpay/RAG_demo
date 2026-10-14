import httpx
import pytest

from app.application import Application
from app.embedder import OllamaEmbedder
from app.llm_adapter import LLMFrame
from app.llm_gateway import LLMGateway
from tests.support import SummaryScriptedLLM as ScriptedLLM
from tests.support import paragraph_pdf, text_pdf


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
    assert [c.think for c in llm.ask_calls] == ["low", "medium", "low"]
    assert llm.ask_calls[1].messages == llm.ask_calls[2].messages
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.ask_calls)
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
    assert len(llm.ask_calls) == 3


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
    assert len(llm.ask_calls) == 3


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
    from tests.support import paragraph_pdf

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

    from app.settings import RetrievalSettings
    from tests.support import paragraph_pdf

    class RangeExtractionLLM(ScriptedLLM):
        def __init__(self):
            super().__init__([])
            self.extracted_ids = []

        async def ask_stream(self, request):
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
            async for frame in super().ask_stream(request):
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
    prompt = llm.ask_calls[-1].messages[-1]["content"]
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
    assert len(llm.ask_calls) == (2 if failure_stage == "answer" else 1)
    assert len(embedder.calls) == (1 if failure_stage == "router" else 2)
    if failure_stage != "answer":
        assert not any(e.type in {"retrieval", "citation_map", "delta"} for e in events)
    embedder.fail = False
    recovered = [e async for e in app.ask("What does this say?")]
    assert next(e for e in recovered if e.type == "final").answer == "Recovered [C1]."


async def test_comma_and_line_suffixed_citations_normalize_across_frames():
    from app.llm_adapter import LLMFrame

    llm = ScriptedLLM(
        [
            "not JSON",
            [
                LLMFrame(content="Multi [C1, "),
                LLMFrame(content="C3] and 【C3"),
                LLMFrame(content="†L1-"),
                LLMFrame(content="L4】."),
                LLMFrame(done=True, prompt_eval_count=100, eval_count=20, done_reason="stop"),
            ],
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    text = "Win rate 64.8% vs 60.0%, e.g. an ablation. " * 100
    assert [e async for e in app.upload_document(paragraph_pdf(text), "numbers.pdf")][
        -1
    ].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    final = next(e for e in result if e.type == "final")
    assert final.answer == "Multi [C1][C3] and [C3]."
    assert {c.id for c in final.citations} == {"C1", "C3"}
    assert "".join(e.text for e in result if e.type == "delta") == final.answer


@pytest.mark.parametrize("over_budget_second_call", [False, True])
async def test_ask_accumulates_traces_from_every_gateway_call(over_budget_second_call):
    from app.llm_gateway import BUDGET_TABLE
    from tests.support import text_pdf

    class TwoCallGateway(LLMGateway):
        # Simulate a multi-call flow through real budget guards and the scripted adapter.
        async def generate(self, call_type, messages, **kwargs):
            if call_type == "router":
                async for event in super().generate(call_type, messages, **kwargs):
                    yield event
                return
            for i in range(2):
                prompt = messages
                if i == 1 and over_budget_second_call:
                    prompt = [
                        {"role": "user", "content": "x " * BUDGET_TABLE["answer"].prompt_limit}
                    ]
                async for event in super().generate(call_type, prompt):
                    yield event

    llm = ScriptedLLM(["not JSON", "One ", "two [C1]."])
    app = Application(OllamaEmbedder(), TwoCallGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    expected = 2 if over_budget_second_call else 3
    assert len(llm.ask_calls) == expected
    assert len(next(e for e in result if e.type == "trace").calls) == expected
    if over_budget_second_call:
        assert result[-1].type == "error" and result[-1].code == "budget_exceeded"
        assert not any(e.type == "final" for e in result)


async def test_terminal_llm_frame_closes_adapter_before_ask_finishes():
    from tests.support import text_pdf

    class ClosingLLM(ScriptedLLM):
        closed = False

        async def stream(self, request):
            try:
                async for frame in super().stream(request):
                    yield frame
            finally:
                self.closed = True

    llm = ClosingLLM(["not JSON", "An answer [C1]."])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    assert any(e.type == "final" for e in result)
    assert llm.closed


async def test_real_10k_prompt_cap_failure_is_an_application_error_without_final():
    from app.llm_gateway import BUDGET_TABLE
    from app.policy import CONTEXT_BUDGET
    from tests.support import text_pdf

    class OversizedPromptGateway(LLMGateway):
        # Control only upstream prompt text; keep the real Gateway budget policy and guard.
        async def generate(self, call_type, messages, **kwargs):
            if call_type.endswith("summary"):
                guarded_messages = messages
            else:
                guarded_messages = [
                    {"role": "user", "content": "x " * BUDGET_TABLE[call_type].prompt_limit}
                ]
            async for event in super().generate(call_type, guarded_messages, **kwargs):
                yield event

    llm = ScriptedLLM(["Must not run"])
    gateway = OversizedPromptGateway(llm)
    assert gateway.context_budget == CONTEXT_BUDGET
    app = Application(OllamaEmbedder(), gateway)
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    assert result[-1].type == "error" and result[-1].code == "budget_exceeded"
    assert not any(e.type == "final" for e in result)
    assert llm.ask_calls == []


async def test_unexpected_upload_exception_emits_generic_error():
    from tests.support import text_pdf

    class FailingEmbedder(OllamaEmbedder):
        # Inject an unexpected exception only at the replaceable external adapter seam.
        async def embed(self, texts):
            raise RuntimeError("Internal details must not appear to the user")

    llm = ScriptedLLM([])
    app = Application(FailingEmbedder(), LLMGateway(llm))
    result = [e async for e in app.upload_document(text_pdf(), "sample.pdf")]
    assert result[-1].type == "error" and result[-1].code == "ingestion_failed"
    assert "Internal details" not in result[-1].message
    assert not any(e.type == "ready" for e in result)
    assert llm.calls == []


async def test_unexpected_llm_exception_emits_generic_error_and_trace():
    from tests.support import text_pdf

    llm = ScriptedLLM([RuntimeError("Internal details must not appear to the user")])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in result][-2:] == ["trace", "error"]
    assert "Internal details" not in result[-1].message
    assert not any(e.type == "final" for e in result)
    assert result[-2].calls[0].done_reason == "error"
