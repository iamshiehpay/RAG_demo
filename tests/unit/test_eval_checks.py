import json

from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from eval.checks import check_fact
from eval.models import GoldenFact


async def test_judge_cannot_pass_with_an_invented_evidence_sentence():
    llm = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": "invented"})])
    result = await check_fact(
        "The answer says something else.",
        GoldenFact("motivation", "judge", "Explains the motivation."),
        LLMGateway(llm),
    )
    assert not result.passed
    assert "verbatim" in result.reason
    assert llm.calls[0].think == "low"
    assert llm.calls[0].num_predict == 1000


async def test_typography_matches_terms_but_numbers_cannot_use_contains():
    import pytest

    from eval.checks import normalize

    result = await check_fact(
        "The ‑Origin variant.",
        GoldenFact("origin", "contains", "-Origin"),
        LLMGateway(ScriptedLLM([])),
    )
    assert result.passed
    assert normalize("67.6 %") == normalize("67.6％") == normalize("67.6%")
    assert normalize("dual\n level") == normalize("dual  level")
    with pytest.raises(ValueError, match="contains cannot check numbers"):
        GoldenFact("invalid", "contains", "64.8")


async def test_wrong_variant_with_the_same_number_cannot_satisfy_numeric_fact():
    answer = "Mix: -High Overall is 64.8%, above LightRAG's 60.0%."
    llm = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    fact = GoldenFact(
        "mix_low",
        "judge",
        "Mix -Low Overall win rate against NaiveRAG is 64.8%, above full LightRAG 60.0%.",
        (("Mix",), ("-Low",), ("Overall",), ("64.8%",), ("LightRAG",), ("60.0%",)),
    )
    assert not (await check_fact(answer, fact, LLMGateway(llm))).passed


async def test_forbidden_check_distinguishes_assertion_from_explicit_negation():
    fact = GoldenFact("all_best", "forbidden", "Full LightRAG is best on every dataset and metric.")
    asserted = "Full LightRAG is best on every dataset and metric."
    negated = "It is false that full LightRAG is best on every dataset and metric."
    llm = ScriptedLLM(
        [
            json.dumps({"matched": True, "asserted": True, "evidence": asserted}),
            json.dumps({"matched": False, "asserted": False, "evidence": ""}),
            json.dumps({"matched": True, "asserted": False, "evidence": negated}),
        ]
    )
    gateway = LLMGateway(llm)
    assert not (await check_fact(asserted, fact, gateway)).passed
    assert (await check_fact(negated, fact, gateway)).passed
    assert (await check_fact(negated, fact, gateway)).passed


async def test_bad_judge_output_and_truncation_fail_closed_even_for_forbidden():
    from chat_document.llm_adapter import LLMFrame

    fact = GoldenFact("bad", "forbidden", "An unsupported claim.")
    llm = ScriptedLLM(
        [
            "not JSON",
            json.dumps({"matched": "false", "asserted": False, "evidence": ""}),
            [LLMFrame(content='{"matched": false}'), LLMFrame(done=True, done_reason="length")],
        ]
    )
    gateway = LLMGateway(llm)
    for _ in range(3):
        assert not (await check_fact("Some answer", fact, gateway)).passed


async def test_judge_guard_rejects_an_over_budget_answer_before_adapter_call():
    llm = ScriptedLLM([])
    result = await check_fact(
        "token " * 9000, GoldenFact("budget", "judge", "A claim"), LLMGateway(llm)
    )
    assert not result.passed
    assert "BudgetExceeded" in result.reason
    assert llm.calls == []


async def test_correct_numeric_context_passes_after_typography_normalization():
    from eval.golden_facts import MIX_LOW

    answer = "On Mix, ‑Low Overall is 64.8 %, higher than full LightRAG's 60.0％."
    llm = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    assert (await check_fact(answer, MIX_LOW, LLMGateway(llm))).passed


async def test_forbidden_judge_with_invented_evidence_cannot_pass():
    fact = GoldenFact("bad_evidence", "forbidden", "A forbidden claim.")
    llm = ScriptedLLM([json.dumps({"matched": False, "asserted": False, "evidence": "invented"})])
    assert not (await check_fact("Actual answer", fact, LLMGateway(llm))).passed


async def test_fixed_refusal_does_not_accept_extra_invented_content():
    llm = ScriptedLLM([])
    fact = GoldenFact("absent", "judge", "No unsupported content", exact_answer="文件中未提及")
    assert not (await check_fact("文件中未提及。但可能是 90%。", fact, LLMGateway(llm))).passed
    assert llm.calls == []
