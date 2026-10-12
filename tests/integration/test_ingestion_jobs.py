import asyncio

import httpx
import pytest

from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway

from .fixtures import text_pdf


class RecordingEmbedder(OllamaEmbedder):
    """Record calls and optionally hold real bge-m3 at the external dependency seam."""

    def __init__(self, *, hold=False):
        super().__init__()
        self.calls = []
        self.entered = asyncio.Event()
        self.release = asyncio.Event()
        if not hold:
            self.release.set()

    async def embed(self, texts):
        self.calls.append(texts)
        self.entered.set()
        await self.release.wait()
        return await super().embed(texts)


async def test_upload_returns_job_before_embedding_and_progress_replays_to_ready():
    embedder = RecordingEmbedder(hold=True)
    llm = ScriptedLLM([])
    app = Application(embedder, LLMGateway(llm))
    job_id = app.start_upload(text_pdf(), "sample.pdf")
    await asyncio.wait_for(embedder.entered.wait(), timeout=5)
    assert app.document is None
    rejected = [event async for event in app.ask("What does the Document say?")]
    assert [event.code for event in rejected] == ["document_not_ready"]
    assert llm.calls == []
    embedder.release.set()
    result = [event async for event in app.upload_events(job_id)]
    assert [event.stage for event in result if event.type == "stage"] == [
        "parsing",
        "chunking",
        "embedding",
        "complete",
    ]
    assert result[-1].type == "ready"
    assert app.document.id == result[-1].document_id
    replay = [event async for event in app.upload_events(job_id)]
    assert replay == result


async def test_same_document_uses_persisted_cache_without_embedding_or_llm(tmp_path):
    content = text_pdf()
    cache = ProcessingCache(tmp_path / ".cache", pipeline_version="test-v1")
    embedder = RecordingEmbedder()
    llm = ScriptedLLM([])
    app = Application(embedder, LLMGateway(llm), cache=cache)
    first = [event async for event in app.upload_document(content, "sample.pdf")]
    assert first[-1].type == "ready"
    chunks = app.document.chunks
    assert len(embedder.calls) == 1
    # A fresh Application demonstrates a disk hit rather than an in-memory shortcut.
    second_embedder = RecordingEmbedder()
    second = Application(second_embedder, LLMGateway(llm), cache=cache)
    result = [event async for event in second.upload_document(content, "renamed.pdf")]
    assert [event.type for event in result] == ["ready"]
    assert second.document.chunks == chunks
    assert second.document.name == "renamed.pdf"
    assert second_embedder.calls == llm.calls == []
    assert second.index.vectors.tolist() == app.index.vectors.tolist()


async def test_pipeline_version_and_content_changes_reprocess_the_document(tmp_path):
    content = text_pdf()
    embedder = RecordingEmbedder()
    llm = ScriptedLLM([])
    for version, uploaded in [("v1", content), ("v2", content), ("v2", text_pdf("new Document"))]:
        app = Application(
            embedder, LLMGateway(llm), cache=ProcessingCache(tmp_path, pipeline_version=version)
        )
        result = [event async for event in app.upload_document(uploaded, "sample.pdf")]
        assert result[-1].type == "ready"
        assert [event.stage for event in result if event.type == "stage"] == [
            "parsing",
            "chunking",
            "embedding",
            "complete",
        ]
    assert len(embedder.calls) == 3
    assert llm.calls == []


async def test_failed_replacement_preserves_document_index_and_history_until_success(tmp_path):
    llm = ScriptedLLM(["not JSON", "Original answer. [C1]"])
    app = Application(RecordingEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path))
    assert [e async for e in app.upload_document(text_pdf(), "original.pdf")][-1].type == "ready"
    assert [e async for e in app.ask("What does this say?")][-2].type == "final"
    original, original_index, original_history = app.document, app.index, list(app.history)
    failed = [e async for e in app.upload_document(text_pdf(""), "scan.pdf")]
    assert failed[-1].code == "invalid_document"
    assert app.document == original and app.index is original_index
    assert app.history == original_history
    embedder = RecordingEmbedder(hold=True)
    app.embedder = embedder
    job_id = app.start_upload(text_pdf("Replacement Document"), "replacement.pdf")
    await asyncio.wait_for(embedder.entered.wait(), timeout=5)
    assert app.document == original
    assert [e async for e in app.ask("What now?")][-1].code == "document_not_ready"
    embedder.release.set()
    assert [e async for e in app.upload_events(job_id)][-1].type == "ready"
    assert app.document.name == "replacement.pdf" and app.history == []
    assert app.index is not original_index
    with pytest.raises(KeyError):
        app.source(original.chunks[0].id)


async def test_embedding_failure_is_stage_specific_and_leaves_no_cache_then_recovers(tmp_path):
    class FailingEmbedder(OllamaEmbedder):
        async def embed(self, texts):
            raise httpx.ConnectError("connection refused")

    llm = ScriptedLLM([])
    app = Application(FailingEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path))
    content = text_pdf()
    result = [event async for event in app.upload_document(content, "sample.pdf")]
    assert result[-1].code == "embedding_failed"
    assert "local Ollama daemon" in result[-1].message
    assert "ready" not in [event.type for event in result]
    assert list(tmp_path.iterdir()) == []
    app.embedder = RecordingEmbedder()
    recovered = [event async for event in app.upload_document(content, "sample.pdf")]
    assert recovered[-1].type == "ready"
    assert len(app.embedder.calls) == 1 and llm.calls == []


async def test_disconnected_progress_subscriber_does_not_cancel_background_ingestion():
    embedder = RecordingEmbedder(hold=True)
    app = Application(embedder, LLMGateway(ScriptedLLM([])))
    job_id = app.start_upload(text_pdf(), "sample.pdf")
    subscriber = app.upload_events(job_id)
    assert (await anext(subscriber)).stage == "parsing"
    await subscriber.aclose()
    await asyncio.wait_for(embedder.entered.wait(), timeout=5)
    embedder.release.set()
    result = [e async for e in app.upload_events(job_id)]
    assert result[-1].type == "ready"


async def test_answers_are_never_cached_even_for_a_cached_document(tmp_path):
    content = text_pdf()
    llm = ScriptedLLM(["not JSON", "Unique first answer. [C1]", "not JSON", "Unique second. [C1]"])
    app = Application(RecordingEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path))
    assert [e async for e in app.upload_document(content, "sample.pdf")][-1].type == "ready"
    assert [e async for e in app.upload_document(content, "sample.pdf")][0].type == "ready"
    entries_before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    first = [e async for e in app.ask("What does this say?")]
    second = [e async for e in app.ask("What does this say?")]
    assert len(llm.calls) == 4
    assert next(e.answer for e in first if e.type == "final") == "Unique first answer. [C1]"
    assert next(e.answer for e in second if e.type == "final") == "Unique second. [C1]"
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == entries_before


async def test_cache_publication_failure_keeps_current_document_and_removes_partial_entry(
    tmp_path, monkeypatch
):
    import os

    app = Application(
        RecordingEmbedder(), LLMGateway(ScriptedLLM([])), cache=ProcessingCache(tmp_path)
    )
    content = text_pdf()
    assert [e async for e in app.upload_document(content, "original.pdf")][-1].type == "ready"
    original = app.document
    entries_before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}

    def fail_replace(*args):
        raise OSError("disk full")

    with monkeypatch.context() as fault:
        fault.setattr(os, "replace", fail_replace)
        result = [e async for e in app.upload_document(text_pdf("Replacement"), "new.pdf")]
    assert result[-1].type == "error"
    assert app.document == original
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == entries_before
    recovered = [e async for e in app.upload_document(text_pdf("Replacement"), "new.pdf")]
    assert recovered[-1].type == "ready"


async def test_unreadable_cache_reprocesses_instead_of_publishing_an_invalid_document(tmp_path):
    app = Application(
        RecordingEmbedder(), LLMGateway(ScriptedLLM([])), cache=ProcessingCache(tmp_path)
    )
    content = text_pdf()
    assert [e async for e in app.upload_document(content, "sample.pdf")][-1].type == "ready"
    next(tmp_path.glob("*.json")).write_text('{"document":')
    result = [e async for e in app.upload_document(content, "sample.pdf")]
    assert result[-1].type == "ready"
    assert len(app.embedder.calls) == 2


async def test_shutdown_ends_pending_upload_with_error_and_no_cache(tmp_path):
    embedder = RecordingEmbedder(hold=True)
    app = Application(embedder, LLMGateway(ScriptedLLM([])), cache=ProcessingCache(tmp_path))
    job_id = app.start_upload(text_pdf(), "sample.pdf")
    await asyncio.wait_for(embedder.entered.wait(), timeout=5)
    await app.close()
    result = [e async for e in app.upload_events(job_id)]
    assert result[-1].code == "ingestion_cancelled"
    assert app.document is None
    assert list(tmp_path.iterdir()) == []


async def test_shutdown_before_worker_starts_still_terminates_progress(tmp_path):
    app = Application(
        RecordingEmbedder(), LLMGateway(ScriptedLLM([])), cache=ProcessingCache(tmp_path)
    )
    job_id = app.start_upload(text_pdf(), "sample.pdf")
    await app.close()
    result = [e async for e in app.upload_events(job_id)]
    assert [e.type for e in result] == ["error"]
    assert result[-1].code == "ingestion_cancelled"
    assert list(tmp_path.iterdir()) == []


async def test_upload_cannot_replace_document_during_an_active_ask():
    app = Application(RecordingEmbedder(), LLMGateway(ScriptedLLM(["not JSON"])))
    assert [e async for e in app.upload_document(text_pdf(), "original.pdf")][-1].type == "ready"
    original = app.document
    answer = app.ask("What does this say?")
    assert (await anext(answer)).type == "plan"
    rejected = [e async for e in app.upload_document(text_pdf("Replacement"), "new.pdf")]
    assert [e.type for e in rejected] == ["error"]
    assert rejected[0].code == "document_busy" and app.document == original
    await answer.aclose()
    assert [e async for e in app.upload_document(text_pdf("Replacement"), "new.pdf")][
        -1
    ].type == "ready"
