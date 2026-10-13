"""Adversarial contextual numbers using names outside either selected paper."""

import json

import pytest

from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from eval.checks import check_fact
from eval.models import GoldenFact, NumericBinding

FACT = GoldenFact(
    "authored_settings",
    "judge",
    "Validation accuracy for Control is 0.812 and Filtered is 0.745.",
    value_bindings=(
        NumericBinding(("Control",), "0.812", ("accuracy",), ("Validation",)),
        NumericBinding(("Filtered",), "0.745", ("accuracy",), ("Validation",)),
        # Other declared measurements are context barriers, never interchangeable.
        NumericBinding(("Control",), "0.683", ("F1",), ("Validation",)),
        NumericBinding(("Filtered",), "0.683", ("F1",), ("Validation",)),
        NumericBinding(("Control",), "0.700", ("accuracy",), ("Test",)),
        NumericBinding(("Filtered",), "0.650", ("accuracy",), ("Test",)),
    ),
)


@pytest.mark.parametrize(
    "first",
    [
        (
            "Validation: Control accuracy 0.812 and F1 0.683; Filtered uses 242 items; "
            "accuracy 0.745 and F1 0.683."
        ),
        (
            "Validation: Control accuracy 0.812 and F1 0.683; Filtered uses 242 items；"
            "accuracy 0.745 and F1 0.683."
        ),
    ],
)
async def test_semicolon_keeps_subject_but_numbers_remain_metric_scoped(first):
    answer = first + "\nTest: Control accuracy 0.700; Filtered accuracy 0.650."
    judge = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    assert (await check_fact(answer, FACT, LLMGateway(judge))).passed


@pytest.mark.parametrize(
    "answer",
    [
        (
            "Validation: Control accuracy 0.745 F1 0.683 while Filtered accuracy 0.812 F1 0.683."
            "\nTest: Control accuracy 0.700, Filtered accuracy 0.650."
        ),
        (
            "Validation: Control accuracy 0.683 F1 0.812 while Filtered accuracy 0.683 F1 0.745."
            "\nTest: Control accuracy 0.700, Filtered accuracy 0.650."
        ),
        (
            "Test: Control accuracy 0.812 F1 0.683; Filtered accuracy 0.745 F1 0.683."
            "\nValidation: Control accuracy 0.700; Filtered accuracy 0.650."
        ),
    ],
)
async def test_swapped_settings_metrics_and_subsets_cannot_pass_affirmative_judge(answer):
    judge = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    assert not (await check_fact(answer, FACT, LLMGateway(judge))).passed


@pytest.mark.parametrize("reversed_values", [False, True])
async def test_reviewer_reported_reversed_settings_are_generic(reversed_values):
    answer = (
        "Control reached 0.745 while Filtered reached 0.812."
        if reversed_values
        else "Control reached 0.812 while Filtered reached 0.745."
    )
    fact = GoldenFact(
        "pair",
        "judge",
        "Correct setting values.",
        value_bindings=(
            NumericBinding(("Control",), "0.812"),
            NumericBinding(("Filtered",), "0.745"),
        ),
    )
    judge = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    assert (await check_fact(answer, fact, LLMGateway(judge))).passed == (not reversed_values)
