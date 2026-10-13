import json

import httpx
from fastapi.testclient import TestClient

from chat_document.api import create_app
from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import LLMFrame
from chat_document.llm_gateway import LLMGateway

from .fixtures import SummaryScriptedLLM as ScriptedLLM
from .fixtures import structured_pdf, text_pdf
from .test_ingestion_jobs import RecordingEmbedder


def events(response):
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    return [
        json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")
    ]


def upload(client, content=None):
    response = client.post(
        "/api/documents",
        files={"document": ("sample.pdf", text_pdf() if content is None else content)},
    )
    assert response.status_code == 202
    accepted = response.json()
    assert accepted["events_url"] == f"/api/documents/{accepted['job_id']}/events"
    return events(client.get(accepted["events_url"]))


def test_upload_http_emits_ready_or_error_and_serves_committed_frontend():
    with TestClient(
        create_app(Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([]))))
    ) as client:
        result = upload(client)
        assert result[-1]["type"] == "ready"
        assert list(dict.fromkeys(e["stage"] for e in result if e["type"] == "stage")) == [
            "parsing",
            "chunking",
            "embedding",
            "summary",
            "complete",
        ]
        summary_progress = [e for e in result if e["type"] == "stage" and e["stage"] == "summary"]
        assert [(e["completed"], e["total"]) for e in summary_progress] == [(0, 2), (1, 2), (2, 2)]
        assert result[-1]["chunk_count"] == 1
        failed = upload(client, text_pdf(""))
        assert [event["type"] for event in failed] == ["stage", "error"]
        assert failed[-1]["code"] == "invalid_document"
        assert client.get("/api/documents/unknown/events").status_code == 404
        home = client.get("/")
        assert home.status_code == 200
        assert "Chat with Document" in home.text
        # Source lookup must fail clearly rather than fall through to the SPA.
        missing = client.get("/api/sources/unknown-id")
        assert missing.status_code == 404
        assert missing.json()["detail"] == "Source not found."


def test_default_app_reads_chunk_size_from_environment_and_anchors_cache(monkeypatch, tmp_path):
    # The real factory/Embedder path is exercised with a scripted external LLM.
    monkeypatch.setattr("chat_document.api.OllamaLLM", lambda *args: ScriptedLLM([]))
    monkeypatch.setenv("CHUNK_TOKEN_TARGET", "35")
    monkeypatch.setenv("LOOKUP_TOP_K", "1")
    monkeypatch.chdir(tmp_path)
    content = structured_pdf()
    with TestClient(create_app()) as client:
        result = upload(client, content)
        assert result[-1]["type"] == "ready"
        assert result[-1]["chunk_count"] == 5
    from hashlib import sha256
    from pathlib import Path

    assert not (tmp_path / ".cache").exists()
    cache_directory = Path(__file__).resolve().parents[2] / ".cache"
    assert any(
        json.loads(entry.read_text())["content_hash"] == sha256(content).hexdigest()
        for entry in cache_directory.glob("*.json")
    )


def test_ask_http_sse_order_and_citation_source():
    llm = ScriptedLLM(
        [
            json.dumps(
                dict(
                    question_type="Synthesis",
                    standalone_question="What does the Document say?",
                    sub_queries=["hello", "Document"],
                )
            ),
            [
                LLMFrame(content="The Document says "),
                LLMFrame(content="hello. [C1]"),
                LLMFrame(done=True, prompt_eval_count=90, eval_count=10, done_reason="stop"),
            ],
        ]
    )
    with TestClient(create_app(Application(OllamaEmbedder(), LLMGateway(llm)))) as client:
        upload(client)
        result = events(client.post("/api/ask", json={"question": "What does the Document say?"}))
        assert [event["type"] for event in result] == [
            "plan",
            "retrieval",
            "citation_map",
            "delta",
            "delta",
            "final",
            "trace",
        ]
        assert result[0] == dict(
            type="plan",
            question_type="Synthesis",
            standalone_question="What does the Document say?",
            sub_queries=["hello", "Document"],
            plan_source="router",
            fallback_reason=None,
            rewrite_language_mismatch=False,
            router_standalone_question=None,
        )
        assert result[3]["text"] + result[4]["text"] == result[5]["answer"]
        citation = result[5]["citations"][0]
        source = client.get("/api/sources/" + citation["source_id"])
        assert source.status_code == 200
        assert source.json()["text"] == "hello Document"
        assert source.json()["page_start"] == citation["page_start"] == 1


def test_rejected_http_sse_is_terminal_without_final_or_model_call():
    llm = ScriptedLLM([])
    with TestClient(create_app(Application(OllamaEmbedder(), LLMGateway(llm)))) as client:
        upload(client)
        result = events(client.post("/api/ask", json={"question": "question " * 1001}))
        assert [event["type"] for event in result] == ["rejected"]
        assert result[0]["token_limit"] == 1000 and result[0]["question_tokens"] > 1000
        assert result[0]["code"] == "question_too_long"
        assert llm.ask_calls == []


async def test_upload_http_returns_202_while_embedding_is_pending_and_blocks_ask():
    import asyncio

    embedder = RecordingEmbedder(hold=True)
    llm = ScriptedLLM([])
    application = Application(embedder, LLMGateway(llm))
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_app(application)), base_url="http://test"
    ) as client:
        accepted = await asyncio.wait_for(
            client.post("/api/documents", files={"document": ("sample.pdf", text_pdf())}),
            timeout=2,
        )
        assert accepted.status_code == 202
        await asyncio.wait_for(embedder.entered.wait(), timeout=5)
        rejected = events(await client.post("/api/ask", json={"question": "hello?"}))
        assert rejected[-1]["code"] == "document_not_ready"
        conflict = await client.post(
            "/api/documents", files={"document": ("other.pdf", text_pdf())}
        )
        assert conflict.status_code == 409
        assert llm.calls == []
        embedder.release.set()
        result = events(await client.get(accepted.json()["events_url"]))
        assert result[-1]["type"] == "ready"
        assert [c.call_type for c in llm.calls] == ["section_summary", "document_summary"]
