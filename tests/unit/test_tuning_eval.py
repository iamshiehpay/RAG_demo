"""Regression of existing Golden Fact coverage and Judge evidence contract."""

import json
import subprocess
import sys

from chat_document.llm_adapter import ScriptedLLM
from eval.checks import check_fact
from eval.golden_facts import LIGHTRAG_CASES
from eval.models import GoldenFact
from eval.runner import RecordingGateway


async def test_q1_cases_check_the_existing_universal_graphrag_overclaim():
    claim = "LightRAG beats GraphRAG on all datasets."
    for case in LIGHTRAG_CASES:
        if case.id not in {"Q1", "Q1_ZH_THREE_SENTENCES"}:
            continue
        facts = [f for f in case.facts if f.id == "not_all_datasets"]
        assert len(facts) == 1
        gateway = RecordingGateway(
            ScriptedLLM([json.dumps({"matched": True, "asserted": True, "evidence": claim})])
        )
        result = await check_fact(claim, facts[0], gateway)
        assert not result.passed and result.reason == "Forbidden claim asserted"


async def test_judge_failure_explanation_is_retained_without_weakening_excerpt_checks():
    llm = ScriptedLLM(
        [
            json.dumps(
                {
                    "matched": False,
                    "asserted": False,
                    "evidence": "",
                    "reason": "The answer omits the conclusion.",
                }
            )
        ]
    )
    result = await check_fact(
        "Methods are described.",
        GoldenFact("conclusion", "judge", "A conclusion"),
        RecordingGateway(llm),
    )
    assert not result.passed
    assert "The answer omits the conclusion." in result.reason


def test_eval_case_selection_does_not_collect_unrequested_live_workloads():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-m",
            "eval",
            "--eval-cases",
            "Q3",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "eval/test_live.py::test_golden_facts_live" in result.stdout
    assert "test_live_router_canonical_and_held_out_cases" not in result.stdout
    assert "test_second_document_real_ingestion_and_golden_facts" not in result.stdout
