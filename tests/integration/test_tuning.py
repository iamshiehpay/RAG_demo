"""Effective experiment settings at the public upload/ask seam, with real bge-m3.

Scripted answers test configuration and errors, not real model quality.
"""

import json

import httpx
import pymupdf
import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_gateway import LLMGateway
from chat_document.settings import RetrievalSettings
from eval.models import EvaluationCase, GoldenFact
from eval.runner import RecordingGateway, run_evaluation

from .fixtures import SummaryScriptedLLM, text_pdf


async def test_environment_answer_think_reaches_guarded_public_ask(monkeypatch):
    monkeypatch.setenv("ANSWER_THINK", "low")
    llm = SummaryScriptedLLM(
        [
            json.dumps(
                {
                    "question_type": "Lookup",
                    "standalone_question": "What is stated?",
                    "sub_queries": [],
                }
            ),
            "A supported statement. [C1]",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    try:
        upload = [e async for e in app.upload_document(text_pdf(), "Document.pdf")]
        assert upload[-1].type == "ready"
        events = [e async for e in app.ask("What is stated?")]
        assert any(e.type == "final" for e in events)
        trace = next(e for e in events if e.type == "trace")
        answer = next(c for c in trace.calls if c.call_type == "answer")
        assert answer.think == "low" and answer.num_predict == 3000
        assert answer.estimated_prompt_tokens + answer.num_predict <= 10000
        assert llm.ask_calls[-1].think == "low"
        assert llm.ask_calls[-1].messages[-1]["content"].count("What is stated?") == 1
    finally:
        await app.close()


@pytest.mark.parametrize("stage", ["router", "embedding"])
async def test_public_ask_error_identifies_http_status_or_invalid_query_embedding(stage):
    request = httpx.Request("POST", "http://localhost:11434/api/chat")
    failure = httpx.HTTPStatusError(
        "model missing", request=request, response=httpx.Response(404, request=request)
    )
    llm = SummaryScriptedLLM([failure] if stage == "router" else ["not JSON"])

    class FailingQueryEmbedder(OllamaEmbedder):
        fail = False

        async def embed(self, texts):
            if self.fail:
                raise ValueError("invalid query vectors")
            return await super().embed(texts)

    embedder = FailingQueryEmbedder()
    app = Application(embedder, LLMGateway(llm))
    try:
        assert [e async for e in app.upload_document(text_pdf(), "Document.pdf")][
            -1
        ].type == "ready"
        embedder.fail = stage == "embedding"
        events = [e async for e in app.ask("What is stated?")]
        assert events[-1].type == "error" and events[-1].code == f"{stage}_failed"
        assert not any(e.type == "final" for e in events)
        if stage == "router":
            assert "HTTP 404" in events[-1].message
            assert "connection failed" not in events[-1].message
    finally:
        await app.close()


async def test_eval_reports_simplified_answer_to_traditional_question_as_quality_failure(tmp_path):
    path = tmp_path / "Document.pdf"
    path.write_bytes(text_pdf())
    llm = SummaryScriptedLLM(["not JSON", "通过实验说明结果。 [C1]"])
    gateway = RecordingGateway(llm)
    app = Application(OllamaEmbedder(), gateway)
    try:
        report = await run_evaluation(
            app, gateway, path, (EvaluationCase("script", "說明這份文件的結果"),)
        )
        rows = [f for f in report.runs[0].facts if f.fact_id == "answer_script"]
        assert len(rows) == 1 and not rows[0].passed
        assert report.runs[0].answer and not report.runs[0].error
        assert not report.passed
    finally:
        await app.close()


async def test_eval_records_effective_configuration_and_pipeline(tmp_path, monkeypatch):
    monkeypatch.setenv("CHUNK_TOKEN_TARGET", "256")
    monkeypatch.setenv("LOOKUP_TOP_K", "7")
    monkeypatch.setenv("ANSWER_THINK", "low")
    path = tmp_path / "Document.pdf"
    path.write_bytes(text_pdf())
    llm = SummaryScriptedLLM(["not JSON", "A supported statement. [C1]"])
    gateway = RecordingGateway(llm)
    app = Application(OllamaEmbedder(), gateway)
    try:
        report = await run_evaluation(
            app,
            gateway,
            path,
            (
                EvaluationCase(
                    "term", "What is stated?", (GoldenFact("term", "contains", "supported"),)
                ),
            ),
        )
        settings = json.loads(report.metadata.get("Effective settings", "{}"))
        assert settings.get("chunk_token_target") == 256
        assert settings.get("lookup_top_k") == 7 and settings.get("answer_think") == "low"
        assert report.metadata.get("Pipeline version", "").startswith("ingest-")
        assert report.passed
    finally:
        await app.close()


async def test_weighted_bm25_public_evidence_keeps_cosine_scores():
    with pymupdf.open() as pdf:
        for i in range(6):
            page = pdf.new_page()
            page.insert_text((72, 60), f"{i + 1} Experiment {i}", fontsize=14)
            words = "ZXQ491 calibration " if i == 4 else "Rainfall observations "
            page.insert_textbox(pymupdf.Rect(72, 100, 520, 700), words * 80, fontsize=10)
        content = pdf.tobytes()
    llm = SummaryScriptedLLM(
        [
            json.dumps(
                {"question_type": "Lookup", "standalone_question": "ZXQ491", "sub_queries": []}
            ),
            "Calibration is described. [C1]",
        ]
    )
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), settings=RetrievalSettings(bm25_weight=1, lookup_top_k=1)
    )
    try:
        assert [e async for e in app.upload_document(content, "Measurements.pdf")][
            -1
        ].type == "ready"
        events = [e async for e in app.ask("ZXQ491")]
        evidence = next(e for e in events if e.type == "retrieval").chunks
        assert evidence and any("ZXQ491" in e.chunk.text for e in evidence)
        assert all(getattr(e, "ranking_score", None) is not None for e in evidence)
        primary = max(evidence, key=lambda e: e.ranking_score)
        assert "ZXQ491" in primary.chunk.text
        assert all(-1.00001 <= e.score <= 1.00001 for e in evidence)
        assert any(e.type == "final" for e in events)
    finally:
        await app.close()


async def test_eval_retains_original_public_citation_map_and_final_events(tmp_path):
    """Original mappings must be inspectable without reconstructing a later search."""
    path = tmp_path / "Independent-measurement.pdf"
    path.write_bytes(text_pdf("Independent measurement is recorded as 37 units."))
    llm = SummaryScriptedLLM(["not JSON", "The measurement is 37 units. [C1]"])
    gateway = RecordingGateway(llm)
    app = Application(OllamaEmbedder(), gateway)
    try:
        report = await run_evaluation(
            app, gateway, path, (EvaluationCase("measurement", "What is the measurement?"),)
        )
        captured = report.runs[0].events
        mapping = next(e for e in captured if e["type"] == "citation_map")
        final = next(e for e in captured if e["type"] == "final")
        retrieved = next(e for e in captured if e["type"] == "retrieval")
        assert final["answer"] == report.runs[0].answer
        citation = final["citations"][0]
        assert citation in mapping["citations"]
        source = next(
            c["chunk"] for c in retrieved["chunks"] if c["chunk"]["id"] == citation["source_id"]
        )
        assert "37 units" in source["text"]
    finally:
        await app.close()


async def test_controlled_retrieval_replay_uses_public_events_and_no_summary_calls(tmp_path):
    from chat_document.cache import ProcessingCache
    from chat_document.events import PlanEvent
    from scripts.tune import RetrievalReplayAdapter, public_retrieval

    content = text_pdf("The inspection campaign records 37 validated samples.")
    cache = ProcessingCache(tmp_path / "cache")
    prepared = Application(OllamaEmbedder(), LLMGateway(SummaryScriptedLLM([])), cache=cache)
    try:
        assert [e async for e in prepared.upload_document(content, "Inspection.pdf")][
            -1
        ].type == "ready"
    finally:
        await prepared.close()
    question = "How many validated samples were recorded?"
    plan = PlanEvent(question_type="Lookup", standalone_question=question, sub_queries=[])
    adapter = RetrievalReplayAdapter({question: plan})
    # This regression's cached summaries are scripted, not native-quality evidence.
    adapter.model = "scripted"
    app = Application(OllamaEmbedder(), RecordingGateway(adapter), cache=cache)
    try:
        ready = [e async for e in app.upload_document(content, "Inspection.pdf")]
        assert [e.type for e in ready] == ["ready"]
        retrieval, observed = await public_retrieval(app, question)
        assert observed == plan and observed.plan_source == "router"
        assert any("37 validated samples" in item.chunk.text for item in retrieval.chunks)
        assert adapter.scripted_calls == ["router", "answer"]
    finally:
        await app.close()
