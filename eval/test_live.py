"""Real Ollama evaluation. Explicitly selected by pytest -m eval."""

import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import OllamaLLM

from .checks import check_fact
from .golden_facts import LIGHTRAG_CASES, NOT_ALL_BEST, router_cases
from .models import FactResult
from .provenance import repository_state
from .report import write_report
from .runner import QuestionRun, RecordingGateway, run_evaluation

pytestmark = pytest.mark.eval


async def test_golden_facts_live(pytestconfig):
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    gateway = RecordingGateway(OllamaLLM(base_url))
    cases = LIGHTRAG_CASES + router_cases()
    selection = pytestconfig.getoption("--eval-cases")
    if selection:
        ids = {value.strip() for value in selection.split(",")}
        cases = tuple(case for case in cases if case.id in ids)
    revision, dirty = repository_state()
    report = await run_evaluation(
        Application(OllamaEmbedder(base_url), gateway),
        gateway,
        pytestconfig.getoption("--eval-document"),
        cases,
        repeats=pytestconfig.getoption("--eval-repeats"),
        metadata={
            "Label": pytestconfig.getoption("--eval-label"),
            "Revision": revision,
            "Uncommitted changes": dirty,
            "LLM": "gpt-oss:120b-cloud",
            "Embedder": "bge-m3",
            "Execution": "Application.upload_document / Application.ask; Gateway judge calls",
            "Router case source": "chat_document.router_regression.CASES (#06 canonical 12 cases)",
        },
        progress=print,
    )
    # Real semantic probes verify that the judge rejects affirmative forbidden claims
    # and accepts explicit negation. These test the checker, not Document answering.
    for repetition in range(1, report.repeats + 1):
        for id, answer, expected in (
            ("JUDGE_ASSERTED", "Full LightRAG is best on every dataset and every metric.", False),
            (
                "JUDGE_NEGATED",
                "It is false that full LightRAG is best on every dataset and every metric. "
                "On Mix, -Low's Overall is higher.",
                True,
            ),
        ):
            start = len(gateway.calls)
            checked = await check_fact(answer, NOT_ALL_BEST, gateway)
            matched_expectation = checked.passed == expected and checked.reason == (
                "No asserted forbidden claim" if expected else "Forbidden claim asserted"
            )
            report.judge_probes.append(
                QuestionRun(
                    id,
                    repetition,
                    "Fixed-answer judge semantic probe",
                    answer=answer,
                    facts=[
                        FactResult(
                            "semantic_contract",
                            "judge",
                            matched_expectation,
                            f"Expected checker pass={expected}; actual={checked.passed}: "
                            f"{checked.reason}",
                            checked.evidence,
                            harness_bug=checked.harness_bug,
                        )
                    ],
                    calls=gateway.calls[start:].copy(),
                    judge_latency_ms=sum(call.latency_ms for call in gateway.calls[start:]),
                    latency_ms=sum(call.latency_ms for call in gateway.calls[start:]),
                )
            )
    path = pytestconfig.getoption("--eval-report") or Path("eval/reports") / (
        datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + ".md"
    )
    write_report(report, path)
    print(f"Golden Facts report: {path}")
    if not pytestconfig.getoption("--eval-record-only"):
        assert report.functional_passed, f"Application operation failed; see {path}"
