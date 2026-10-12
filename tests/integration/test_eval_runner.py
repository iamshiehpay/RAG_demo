import json

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from eval.models import EvaluationCase, GoldenFact
from eval.report import write_report
from eval.runner import RecordingGateway, run_evaluation

from .fixtures import text_pdf


async def test_operations_report_all_calls_and_three_run_fact_rates(tmp_path):
    document_path = tmp_path / "document.pdf"
    document_path.write_bytes(text_pdf("The Document contains graph indexing."))
    answer = "Graph indexing. [C1]"
    llm = ScriptedLLM(
        [
            answer,
            json.dumps({"matched": True, "asserted": True, "evidence": "Graph indexing."}),
            answer,
            json.dumps({"matched": False, "asserted": False, "evidence": ""}),
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
    assert len(llm.calls) == 6
    assert all(len(run.calls) == 2 for run in report.runs)
    assert "prompt_eval_count" in content and "eval_count" in content
    assert "latency_ms" in content and "done_reason" in content
    assert content.count("| judge | low |") == 3 and content.count("| answer | medium |") == 3
    assert all(run.answer == answer for run in report.runs)
    assert all(call.estimated_prompt_tokens + call.num_predict <= 10000 for call in gateway.calls)


async def test_failed_ask_records_failed_call_without_judging_provisional_answer(tmp_path):
    from chat_document.llm_adapter import LLMFrame

    path = tmp_path / "document.pdf"
    path.write_bytes(text_pdf())
    llm = ScriptedLLM(
        [[LLMFrame(content="Unfinished claim"), LLMFrame(done=True, done_reason="length")]]
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
    assert len(llm.calls) == 1 and run.calls[0].done_reason == "length"
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
