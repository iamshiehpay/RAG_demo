import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

from .fixtures import SummaryScriptedLLM as ScriptedLLM
from .fixtures import paragraph_pdf


async def test_uploaded_oversized_paragraph_keeps_decimals_and_abbreviations():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    text = "Win rate 64.8% vs 60.0%, e.g. an ablation. " * 100
    result = [e async for e in app.upload_document(paragraph_pdf(text), "numbers.pdf")]
    assert result[-1].type == "ready"
    assert any(count_tokens(p) > 500 for s in app.document.sections for p in s.paragraphs)
    chunks = app.document.chunks
    assert len(chunks) > 1
    combined = "\n".join(c.text for c in chunks)
    assert "64.8" in combined and "60.0" in combined and "e.g." in combined
    assert "64.\n8" not in combined and "60.\n0" not in combined


async def test_uploaded_cjk_paragraph_splits_on_characters_with_overlap():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    text = "".join(f"龜測試{i:04d}" for i in range(600))
    result = [e async for e in app.upload_document(paragraph_pdf(text, cjk=True), "cjk.pdf")]
    assert result[-1].type == "ready"
    chunks = app.document.chunks
    assert len(chunks) > 1
    assert all("\ufffd" not in c.text and count_tokens(c.text) <= 500 for c in chunks)
    for left, right in zip(chunks, chunks[1:], strict=False):
        shared = max(
            (
                size
                for size in range(1, min(len(left.text), len(right.text)) + 1)
                if left.text[-size:] == right.text[:size]
            ),
            default=0,
        )
        assert 40 <= count_tokens(left.text[-shared:]) <= 50


async def test_real_10k_budget_rejects_prompt_one_token_over_answer_cap():
    import pytest

    from chat_document.llm_gateway import BUDGET_TABLE, BudgetExceeded

    llm = ScriptedLLM(["Must not run"])
    gateway = LLMGateway(llm)
    cap = BUDGET_TABLE["answer"].prompt_limit
    prompt = "x " * cap
    assert count_tokens(prompt) == cap + 1
    observed = []
    with pytest.raises(BudgetExceeded):
        async for event in gateway.generate("answer", [{"role": "user", "content": prompt}]):
            observed.append(event)
    assert observed == []  # No delta, final or Trace: the adapter was never called.
    assert llm.ask_calls == []
    # The exact cap remains legal: reserved usage reaches, but never exceeds, 10K.
    accepted = [
        e async for e in gateway.generate("answer", [{"role": "user", "content": prompt.rstrip()}])
    ]
    assert count_tokens(prompt.rstrip()) == cap
    trace = accepted[-1].calls[0]
    assert trace.estimated_prompt_tokens + trace.num_predict == trace.context_budget


async def test_comma_and_line_suffixed_citations_normalize_across_frames():
    from chat_document.llm_adapter import LLMFrame

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
    from chat_document.llm_gateway import BUDGET_TABLE

    from .fixtures import text_pdf

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
    from .fixtures import text_pdf

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
    from chat_document.llm_gateway import BUDGET_TABLE
    from chat_document.policy import CONTEXT_BUDGET

    from .fixtures import text_pdf

    class OversizedPromptGateway(LLMGateway):
        # Control only upstream prompt text; keep the real Gateway budget policy and guard.
        async def generate(self, call_type, messages, **kwargs):
            if call_type.endswith("summary"):
                async for event in super().generate(call_type, messages, **kwargs):
                    yield event
                return
            prompt = "x " * BUDGET_TABLE[call_type].prompt_limit
            async for event in super().generate(call_type, [{"role": "user", "content": prompt}]):
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
    from .fixtures import text_pdf

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
    assert llm.ask_calls == []


async def test_unexpected_llm_exception_emits_generic_error_and_trace():
    from .fixtures import text_pdf

    llm = ScriptedLLM([RuntimeError("Internal details must not appear to the user")])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    result = [e async for e in app.ask("What does this say?")]
    assert [e.type for e in result][-2:] == ["trace", "error"]
    assert "Internal details" not in result[-1].message
    assert not any(e.type == "final" for e in result)
    assert result[-2].calls[0].done_reason == "error"
