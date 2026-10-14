"""Adversarial contextual numbers using names outside either selected paper."""

import json

import pytest

from app.llm_gateway import LLMGateway
from eval.checks import check_fact
from eval.fakes import ScriptedLLM
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


@pytest.mark.parametrize("reversed_values", [False, True])
async def test_table_comparison_column_cannot_reassign_primary_row_owner(reversed_values):
    control, filtered = ("0.745", "0.812") if reversed_values else ("0.812", "0.745")
    answer = (
        "Validation:\n| Setting | Compared with | Accuracy |\n|---|---|---|\n"
        f"| Control | Filtered | {control} |\n| Filtered | Control | {filtered} |"
    )
    fact = GoldenFact(
        "row_ownership",
        "judge",
        "Correct primary setting accuracy.",
        value_bindings=FACT.value_bindings[:2],
    )
    judge = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    assert (await check_fact(answer, fact, LLMGateway(judge))).passed == (not reversed_values)


@pytest.mark.parametrize("reversed_values", [False, True])
async def test_postpositive_labels_and_explicit_shared_metric_preserve_associations(
    reversed_values,
):
    first, second = ("0.745", "0.812") if reversed_values else ("0.812", "0.745")
    answer = (
        "Validation: With Filtered, accuracy drops from "
        f"{first} (Control) to {second} (Filtered), while F1 remains unchanged at 0.683."
    )
    fact = GoldenFact(
        "comparison",
        "judge",
        "Validation accuracy drops; F1 is unchanged in both settings.",
        value_bindings=FACT.value_bindings[:4],
    )
    judge = ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": answer})])
    assert (await check_fact(answer, fact, LLMGateway(judge))).passed == (not reversed_values)
