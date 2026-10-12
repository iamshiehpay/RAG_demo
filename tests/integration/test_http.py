import json

from fastapi.testclient import TestClient

from chat_document.api import create_app
from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import LLMFrame, ScriptedLLM
from chat_document.llm_gateway import LLMGateway

from .fixtures import text_pdf


def events(response):
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    return [
        json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")
    ]


def test_upload_http_emits_ready_and_serves_committed_frontend():
    with TestClient(
        create_app(Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([]))))
    ) as client:
        result = events(
            client.post("/api/documents", files={"document": ("sample.pdf", text_pdf())})
        )
        assert [event["type"] for event in result] == ["stage", "stage", "stage", "ready"]
        assert result[-1]["chunk_count"] == 1
        home = client.get("/")
        assert home.status_code == 200
        assert "Chat with Document" in home.text
        # Source lookup must fail clearly rather than fall through to the SPA.
        missing = client.get("/api/sources/unknown-id")
        assert missing.status_code == 404
        assert missing.json()["detail"] == "Source not found."


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
        events(client.post("/api/documents", files={"document": ("sample.pdf", text_pdf())}))
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
        events(client.post("/api/documents", files={"document": ("sample.pdf", text_pdf())}))
        result = events(client.post("/api/ask", json={"question": "question " * 1001}))
        assert [event["type"] for event in result] == ["rejected"]
        assert result[0]["token_limit"] == 1000 and result[0]["question_tokens"] > 1000
        assert result[0]["code"] == "question_too_long"
        assert llm.calls == []
