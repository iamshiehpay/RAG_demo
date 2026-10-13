"""Declared route alternatives still require a real valid Router result.

Adapters replace external services only to exercise the report predicate;
real mixed-question route and fact evidence is recorded separately in eval.
"""

import json

import pytest

from chat_document.application import Application
from eval.models import EvaluationCase
from eval.runner import RecordingGateway, run_evaluation

from .fixtures import SummaryScriptedLLM, text_pdf
from .test_second_document import DeterministicEmbedder


@pytest.mark.parametrize("route", ["Lookup", "Synthesis", "Global", "invalid"])
async def test_declared_route_set_accepts_only_valid_router_members(route, tmp_path):
    plan = (
        json.dumps(
            {
                "question_type": route,
                "standalone_question": "Explain measurements",
                "sub_queries": ["measurements"] if route == "Synthesis" else [],
            }
        )
        if route != "invalid"
        else "invalid JSON"
    )
    gateway = RecordingGateway(SummaryScriptedLLM([plan, "Supported measurements."]))
    app = Application(DeterministicEmbedder(), gateway)
    document = tmp_path / "measurements.pdf"
    document.write_bytes(text_pdf("Source measurements."))
    case = EvaluationCase(
        "mixed", "Explain measurements", accepted_question_types=("Lookup", "Synthesis")
    )
    report = await run_evaluation(app, gateway, document, (case,))
    assert report.passed == (route in {"Lookup", "Synthesis"})
    fact = next(f for f in report.runs[0].facts if f.fact_id == "question_type")
    assert fact.passed == (route in {"Lookup", "Synthesis"})
    if route == "invalid":
        assert fact.fallback
