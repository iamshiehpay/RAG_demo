import json

from app.application import Application
from app.embedder import OllamaEmbedder
from eval.models import EvaluationCase, GoldenFact
from eval.report import write_report
from eval.runner import RecordingGateway, run_evaluation
from tests.support import SummaryScriptedLLM as ScriptedLLM
from tests.support import text_pdf

LOOKUP_PLAN = json.dumps(
    {"question_type": "Lookup", "standalone_question": "What does it say?", "sub_queries": []}
)


async def test_operations_report_all_calls_and_three_run_fact_rates(tmp_path):
    document_path = tmp_path / "document.pdf"
    document_path.write_bytes(text_pdf("The Document contains graph indexing."))
    answer = "Graph indexing. [C1]"
    llm = ScriptedLLM(
        [
            LOOKUP_PLAN,
            answer,
            json.dumps({"matched": True, "asserted": True, "evidence": "Graph indexing."}),
            LOOKUP_PLAN,
            answer,
            json.dumps({"matched": False, "asserted": False, "evidence": ""}),
            LOOKUP_PLAN,
            answer,
            json.dumps({"matched": True, "asserted": True, "evidence": "Graph indexing."}),
        ]
    )
    gateway = RecordingGateway(llm)
    case = EvaluationCase(
        "graph",
        "What does the Document contain?",
        (GoldenFact("indexing", "judge", "Graph indexing."),),
        "Lookup",
    )
    report = await run_evaluation(
        Application(OllamaEmbedder(), gateway), gateway, document_path, (case,), repeats=3
    )
    path = tmp_path / "report.md"
    write_report(report, path)
    content = path.read_text()
    assert "2/3 (66.7%)" in content
    assert len(report.runs) == 3
    assert len(llm.ask_calls) == 9
    assert all(len(run.calls) == 3 for run in report.runs)
    assert "prompt_eval_count" in content and "eval_count" in content
    assert "latency_ms" in content and "done_reason" in content
    assert content.count("| judge | low |") == 3 and content.count("| answer | medium |") == 3
    assert content.count("| router | low |") == 3
    assert all(run.answer == answer for run in report.runs)
    assert all(call.estimated_prompt_tokens + call.num_predict <= 10000 for call in gateway.calls)


async def test_failed_ask_records_failed_call_without_judging_provisional_answer(tmp_path):
    from app.llm_adapter import LLMFrame

    path = tmp_path / "document.pdf"
    path.write_bytes(text_pdf())
    llm = ScriptedLLM(
        [
            LOOKUP_PLAN,
            [LLMFrame(content="Unfinished claim"), LLMFrame(done=True, done_reason="length")],
            [LLMFrame(content="Unfinished retry"), LLMFrame(done=True, done_reason="length")],
        ]
    )
    gateway = RecordingGateway(llm)
    case = EvaluationCase(
        "failure", "What does it say?", (GoldenFact("claim", "judge", "A claim"),)
    )
    report = await run_evaluation(Application(OllamaEmbedder(), gateway), gateway, path, (case,))
    assert not report.passed
    run = report.runs[0]
    assert run.answer == "" and run.error
    assert not run.facts[0].passed
    assert len(llm.ask_calls) == 3 and run.calls[-1].done_reason == "length"
    assert llm.ask_calls[-1].think == "low"
    assert [call.call_type for call in run.calls] == ["router", "answer", "answer"]
    write_report(report, tmp_path / "failure.md")
    assert "length" in (tmp_path / "failure.md").read_text()


async def test_upload_error_still_reports_every_expected_fact(tmp_path):
    path = tmp_path / "scan.pdf"
    path.write_bytes(text_pdf(""))
    gateway = RecordingGateway(ScriptedLLM([]))
    case = EvaluationCase(
        "scan", "A question", (GoldenFact("term", "contains", "LightRAG"),), "Lookup"
    )
    report = await run_evaluation(
        Application(OllamaEmbedder(), gateway), gateway, path, (case,), repeats=3
    )
    write_report(report, tmp_path / "upload_failure.md")
    assert report.upload_error
    assert len(report.runs) == 3 and not report.passed
    assert "0/3 (0.0%)" in (tmp_path / "upload_failure.md").read_text()
    assert gateway.calls == []


async def test_ask_latency_excludes_judge_latency(tmp_path, monkeypatch):
    import app.llm_gateway
    import eval.runner

    clock = [0.0]
    monkeypatch.setattr(eval.runner, "perf_counter", lambda: clock[0])
    monkeypatch.setattr(app.llm_gateway, "perf_counter", lambda: clock[0])

    class TimedLLM(ScriptedLLM):
        async def stream(self, request):
            clock[0] += 0 if request.format else (5 if request.think == "low" else 1)
            async for frame in super().stream(request):
                yield frame

    path = tmp_path / "document.pdf"
    path.write_bytes(text_pdf())
    llm = TimedLLM(
        [
            LOOKUP_PLAN,
            "A claim [C1]",
            json.dumps({"matched": True, "asserted": True, "evidence": "A claim"}),
        ]
    )
    gateway = RecordingGateway(llm)
    case = EvaluationCase("timing", "What does it say?", (GoldenFact("claim", "judge", "A claim"),))
    report = await run_evaluation(Application(OllamaEmbedder(), gateway), gateway, path, (case,))
    run = report.runs[0]
    assert run.ask_latency_ms == 1000
    assert run.judge_latency_ms == 5000
    assert run.latency_ms == 6000
    write_report(report, tmp_path / "timing.md")
    text = (tmp_path / "timing.md").read_text()
    assert "Ask latency_ms: 1000.00" in text and "Judge latency_ms: 5000.00" in text


async def test_q3_requires_a_used_citation_to_a_table_source(tmp_path):
    path = tmp_path / "table.pdf"
    path.write_bytes(text_pdf("Table 2: ablation results."))
    gateway = RecordingGateway(
        ScriptedLLM([LOOKUP_PLAN, "Ablation results [C1]", LOOKUP_PLAN, "Ablation results [C9]"])
    )
    case = EvaluationCase(
        "Q3", "Ablation results?", required_citation_page=8, required_citation_term="Table 2"
    )
    report = await run_evaluation(
        Application(OllamaEmbedder(), gateway), gateway, path, (case,), repeats=2
    )
    assert report.runs[0].facts[0].passed
    assert not report.runs[1].facts[0].passed


async def test_canonical_router_cases_convert_history_and_isolate_independent_questions(tmp_path):
    from eval.golden_facts import router_cases
    from eval.router_cases import CASES

    cases = router_cases()
    assert len(cases) == 12
    assert [
        (list(case.history), case.question, case.expected_question_type) for case in cases
    ] == CASES
    selected = (cases[10], cases[11], cases[7])
    scripts = []
    for case, standalone in zip(
        selected,
        (
            "LightRAG 的檢索成本是多少？",
            "LightRAG 跟 GraphRAG 的比較是什麼？",
            selected[2].question,
        ),
        strict=True,
    ):
        scripts.extend(
            [
                json.dumps(
                    {
                        "question_type": case.expected_question_type,
                        "standalone_question": standalone,
                        "sub_queries": [],
                    }
                ),
                "證據 [C1]"
                if any("\u4e00" <= ch <= "\u9fff" for ch in case.question)
                else "Evidence [C1]",
            ]
        )
    llm = ScriptedLLM(scripts)
    gateway = RecordingGateway(llm)
    application = Application(OllamaEmbedder(), gateway)
    path = tmp_path / "document.pdf"
    path.write_bytes(text_pdf())
    report = await run_evaluation(application, gateway, path, selected)
    assert report.passed
    assert application.history == []
    requests = [request for request in llm.ask_calls if request.format]
    assert len(requests) == 3
    for request, case in zip(requests, selected, strict=True):
        assert request.messages[1:-1] == [
            {"role": role, "content": content} for role, content in case.history
        ]
        assert request.messages[-1]["role"] == "user"
        assert case.question in request.messages[-1]["content"]
