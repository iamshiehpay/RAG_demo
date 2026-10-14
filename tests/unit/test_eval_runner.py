"""Focused regressions grouped by feature; helpers remain outside test modules."""

import json

import pytest

from app.application import Application
from app.events import FinalEvent, PlanEvent, ReadyEvent
from app.models import Chunk, Citation, Document
from eval.fakes import ScriptedLLM
from eval.models import EvaluationCase
from eval.report import write_report
from eval.runner import RecordingGateway, check_source_citation, run_evaluation
from tests.support import DeterministicEmbedder, SummaryScriptedLLM, text_pdf


async def test_router_lookup_passes_but_fallback_lookup_is_distinctly_failed(tmp_path):
    class ScriptedApplication:
        async def upload_document(self, content, name):
            yield ReadyEvent(document_id="d", name=name, chunk_count=0)

        async def ask(self, question, *, history):
            yield plans.pop(0)
            yield FinalEvent(answer="Evidence", citations=[])

    plans = [
        PlanEvent(
            question_type="Lookup",
            standalone_question="Question?",
            sub_queries=[],
            plan_source="router",
        ),
        PlanEvent(
            question_type="Lookup",
            standalone_question="Question?",
            sub_queries=[],
            plan_source="fallback",
            fallback_reason="invalid_json",
        ),
    ]
    path = tmp_path / "document.pdf"
    path.write_bytes(b"scripted Document")
    case = EvaluationCase("lookup", "Question?", expected_question_type="Lookup")
    report = await run_evaluation(
        ScriptedApplication(), RecordingGateway(ScriptedLLM([])), path, (case,), repeats=2
    )
    assert report.runs[0].facts[0].passed
    assert report.runs[1].facts[0].status == "FALLBACK"
    assert not report.runs[1].facts[0].passed
    assert report.runs[1].fallback_reason == "invalid_json"
    write_report(report, tmp_path / "report.md")
    text = (tmp_path / "report.md").read_text()
    assert "| FALLBACK |" in text and "invalid_json" in text
    assert "1/2 (50.0%)" in text


async def test_follow_up_must_change_and_resolve_the_canonical_referents(tmp_path):
    from eval.golden_facts import router_cases

    class ScriptedApplication:
        async def upload_document(self, content, name):
            yield ReadyEvent(document_id="d", name=name, chunk_count=0)

        async def ask(self, question, *, history):
            yield plans.pop(0)
            yield FinalEvent(answer="Evidence", citations=[])

    cost, comparison = router_cases()[10:12]
    plans = [
        PlanEvent(question_type="Lookup", standalone_question=cost.question, sub_queries=[]),
        PlanEvent(
            question_type="Lookup",
            standalone_question="What is its retrieval cost?",
            sub_queries=[],
        ),
        PlanEvent(
            question_type="Lookup",
            standalone_question="LightRAG 的檢索成本是多少？",
            sub_queries=[],
        ),
        PlanEvent(
            question_type="Synthesis",
            standalone_question="Compare GraphRAG with it.",
            sub_queries=[],
        ),
        PlanEvent(
            question_type="Synthesis",
            standalone_question="Compare LightRAG with GraphRAG.",
            sub_queries=[],
        ),
    ]
    path = tmp_path / "document.pdf"
    path.write_bytes(b"scripted Document")
    gateway = RecordingGateway(ScriptedLLM([]))
    cost_report = await run_evaluation(ScriptedApplication(), gateway, path, (cost,), repeats=3)
    comparison_report = await run_evaluation(
        ScriptedApplication(), gateway, path, (comparison,), repeats=2
    )
    rewrite_results = [
        next(f for f in run.facts if f.fact_id == "standalone_rewrite")
        for run in cost_report.runs + comparison_report.runs
    ]
    assert [fact.passed for fact in rewrite_results] == [False, False, True, False, True]
    assert all(f.fact_id != "history_supported" for run in cost_report.runs for f in run.facts)


async def test_flagged_language_mismatch_cannot_pass_as_a_router_rewrite(tmp_path):
    from eval.golden_facts import router_cases

    class ScriptedApplication:
        async def upload_document(self, content, name):
            yield ReadyEvent(document_id="d", name=name, chunk_count=0)

        async def ask(self, question, *, history):
            yield PlanEvent(
                question_type="Lookup",
                standalone_question="LightRAG 的檢索成本是多少？",
                sub_queries=[],
                rewrite_language_mismatch=True,
                router_standalone_question="What is LightRAG's retrieval cost?",
            )
            yield FinalEvent(answer="Evidence", citations=[])

    path = tmp_path / "document.pdf"
    path.write_bytes(b"scripted Document")
    report = await run_evaluation(
        ScriptedApplication(), RecordingGateway(ScriptedLLM([])), path, (router_cases()[10],)
    )
    rewrite = next(f for f in report.runs[0].facts if f.fact_id == "standalone_rewrite")
    assert not rewrite.passed
    assert report.runs[0].rewrite_language_mismatch
    write_report(report, tmp_path / "report.md")
    text = (tmp_path / "report.md").read_text()
    assert "Rewrite language mismatch: True" in text
    assert "LightRAG&#x27;s retrieval cost" in text


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


def test_citation_prefers_a_labeled_table_chunk_when_available():
    class TableChunk(Chunk):
        kind: str = "table"
        table_label: str = "Table 2"

    common = dict(section_id="s", section="Results", page_start=8, page_end=8)
    paragraph = Chunk(id="paragraph", text="The discussion of Table 2.", order=0, **common)
    table = TableChunk(id="table", text="Ablation win rates", order=1, **common)
    application = Application(None, None)
    application.document = Document(id="d", name="test", sections=[], chunks=[paragraph, table])
    case = EvaluationCase(
        "Q3", "question", (), required_citation_page=8, required_citation_term="Table 2"
    )

    def final(source):
        citation = Citation(
            id="C1", source_id=source.id, section="Results", page_start=8, page_end=8
        )
        return [FinalEvent(answer="Evidence [C1]", citations=[citation])]

    assert not check_source_citation(application, final(paragraph), case).passed
    assert check_source_citation(application, final(table), case).passed
    application.document.chunks = [paragraph]
    assert check_source_citation(application, final(paragraph), case).passed
