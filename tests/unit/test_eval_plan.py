from chat_document.events import FinalEvent, PlanEvent, ReadyEvent
from chat_document.llm_adapter import ScriptedLLM
from eval.models import EvaluationCase
from eval.report import write_report
from eval.runner import RecordingGateway, run_evaluation


async def test_router_lookup_passes_but_fallback_lookup_is_distinctly_failed(tmp_path):
    # Compatible scripted events while #06's provenance fields await integration.
    class ProvenancePlan(PlanEvent):
        plan_source: str
        fallback_reason: str | None = None

    class ScriptedApplication:
        async def upload_document(self, content, name):
            yield ReadyEvent(document_id="d", name=name, chunk_count=0)

        async def ask(self, question, *, history):
            yield plans.pop(0)
            yield FinalEvent(answer="Evidence", citations=[])

    plans = [
        ProvenancePlan(
            question_type="Lookup",
            standalone_question="Question?",
            sub_queries=[],
            plan_source="router",
        ),
        ProvenancePlan(
            question_type="Lookup",
            standalone_question="Question?",
            sub_queries=[],
            plan_source="fallback",
            fallback_reason="Invalid Router JSON",
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
    assert report.runs[1].fallback_reason == "Invalid Router JSON"
    write_report(report, tmp_path / "report.md")
    text = (tmp_path / "report.md").read_text()
    assert "| FALLBACK |" in text and "Invalid Router JSON" in text
    assert "1/2 (50.0%)" in text


async def test_follow_up_must_change_and_resolve_the_canonical_referents(tmp_path):
    from eval.golden_facts import router_cases

    class ProvenancePlan(PlanEvent):
        plan_source: str = "router"
        fallback_reason: str | None = None

    class ScriptedApplication:
        async def upload_document(self, content, name):
            yield ReadyEvent(document_id="d", name=name, chunk_count=0)

        async def ask(self, question, *, history):
            yield plans.pop(0)
            yield FinalEvent(answer="Evidence", citations=[])

    cost, comparison = router_cases()[10:12]
    plans = [
        ProvenancePlan(question_type="Lookup", standalone_question=cost.question, sub_queries=[]),
        ProvenancePlan(
            question_type="Lookup",
            standalone_question="What is its retrieval cost?",
            sub_queries=[],
        ),
        ProvenancePlan(
            question_type="Lookup",
            standalone_question="LightRAG 的檢索成本是多少？",
            sub_queries=[],
        ),
        ProvenancePlan(
            question_type="Synthesis",
            standalone_question="Compare GraphRAG with it.",
            sub_queries=[],
        ),
        ProvenancePlan(
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
