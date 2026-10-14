"""Public ask lifecycle contracts; provider scripts are deterministic, not live evidence."""

import asyncio

import pytest

from app.application import Application
from app.embedder import OllamaEmbedder
from app.ingestion import UploadBusy
from app.llm_adapter import LLMFrame
from app.llm_gateway import LLMGateway
from tests.support import SummaryScriptedLLM, text_pdf


async def test_cancel_pending_answer_closes_provider_and_releases_document():
    entered = asyncio.Event()
    closed = asyncio.Event()

    class BlockingLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.call_type != "answer":
                async for frame in super().stream(request):
                    yield frame
                return
            try:
                yield LLMFrame(content="First provisional [C1].")
                entered.set()
                await asyncio.Event().wait()
            finally:
                closed.set()

    app = Application(OllamaEmbedder(), LLMGateway(BlockingLLM(["not JSON"])))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    stream = app.ask("What does this say?")
    seen = []
    while not seen or seen[-1].type != "delta":
        seen.append(await anext(stream))
    assert [e.type for e in seen] == ["plan", "retrieval", "citation_map", "delta"]
    assert not entered.is_set(), "First delta must arrive before provider finishes"
    assert app.history == []
    with pytest.raises(UploadBusy):
        app.start_upload(text_pdf(), "busy.pdf")
    pending = asyncio.create_task(anext(stream))
    await asyncio.wait_for(entered.wait(), 2)
    pending.cancel()
    with pytest.raises(asyncio.CancelledError):
        await pending
    await stream.aclose()
    assert closed.is_set()
    assert app.history == []
    job_id = app.start_upload(text_pdf(), "after-cancel.pdf")
    assert [e async for e in app.upload_events(job_id)][-1].type == "ready"
    await app.close()


async def test_close_paused_delta_closes_provider_before_returning_without_history():
    closed = asyncio.Event()
    advanced = asyncio.Event()

    class PausedLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.call_type != "answer":
                async for frame in super().stream(request):
                    yield frame
                return
            try:
                yield LLMFrame(content="Provisional [C1].")
                advanced.set()
                yield LLMFrame(done=True, done_reason="stop")
            finally:
                closed.set()

    app = Application(OllamaEmbedder(), LLMGateway(PausedLLM(["not JSON"])))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    stream = app.ask("What does this say?")
    while (await anext(stream)).type != "delta":
        pass
    assert not advanced.is_set()
    await stream.aclose()
    assert closed.is_set(), "Public close must await native provider cleanup"
    assert not advanced.is_set()
    assert app.history == []
    assert app._asking == 0


async def test_http_disconnect_cancels_pending_native_answer_without_detached_work():
    from app.api import create_app

    closed = asyncio.Event()
    first_delta = asyncio.Event()

    class DisconnectLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.call_type != "answer":
                async for frame in super().stream(request):
                    yield frame
                return
            try:
                yield LLMFrame(content="Provisional [C1].")
                await asyncio.Event().wait()
            finally:
                closed.set()

    app = Application(OllamaEmbedder(), LLMGateway(DisconnectLLM(["not JSON"])))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    baseline_tasks = set(asyncio.all_tasks())
    messages = []
    request_sent = False

    async def receive():
        nonlocal request_sent
        if not request_sent:
            request_sent = True
            return {"type": "http.request", "body": b'{"question":"What does this say?"}'}
        await first_delta.wait()
        return {"type": "http.disconnect"}

    async def send(message):
        messages.append(message)
        if b"event: delta" in message.get("body", b""):
            first_delta.set()

    await asyncio.wait_for(
        create_app(app)(
            {
                "type": "http",
                "asgi": {"version": "3.0", "spec_version": "2.3"},
                "http_version": "1.1",
                "method": "POST",
                "scheme": "http",
                "path": "/api/ask",
                "raw_path": b"/api/ask",
                "query_string": b"",
                "headers": [(b"content-type", b"application/json")],
                "client": ("127.0.0.1", 1234),
                "server": ("127.0.0.1", 8340),
            },
            receive,
            send,
        ),
        3,
    )
    assert closed.is_set()
    assert app._asking == 0
    assert app.history == []
    assert not any(b"event: final" in item.get("body", b"") for item in messages)
    assert not (set(asyncio.all_tasks()) - baseline_tasks)


async def test_repeated_cancel_joins_slow_provider_cleanup():
    entered = asyncio.Event()
    cleaning = asyncio.Event()
    release = asyncio.Event()
    closed = asyncio.Event()

    class SlowCleanupLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.call_type != "answer":
                async for frame in super().stream(request):
                    yield frame
                return
            try:
                entered.set()
                await asyncio.Event().wait()
                yield LLMFrame(done=True, done_reason="stop")
            finally:
                cleaning.set()
                await release.wait()
                closed.set()

    app = Application(OllamaEmbedder(), LLMGateway(SlowCleanupLLM(["not JSON"])))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    before = set(asyncio.all_tasks())
    stream = app.ask("What does this say?")
    for expected in ["plan", "retrieval", "citation_map"]:
        assert (await anext(stream)).type == expected
    pending = asyncio.create_task(anext(stream))
    await asyncio.wait_for(entered.wait(), 2)
    pending.cancel()
    await asyncio.wait_for(cleaning.wait(), 2)
    pending.cancel()
    # A second cancellation must not let the caller return while cleanup runs.
    await asyncio.sleep(0)
    assert not pending.done()
    assert app._asking == 1
    release.set()
    with pytest.raises(asyncio.CancelledError):
        await pending
    await stream.aclose()
    assert closed.is_set()
    assert app._asking == 0
    assert app.history == []
    assert not (set(asyncio.all_tasks()) - before)


async def test_close_after_final_retains_successful_history_and_joins_graph():
    app = Application(
        OllamaEmbedder(), LLMGateway(SummaryScriptedLLM(["not JSON", "Supported [C1]."]))
    )
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    before = set(asyncio.all_tasks())
    stream = app.ask("What does this say?")
    while (event := await anext(stream)).type != "final":
        assert app.history == []
    assert app.history[-1].answer == event.answer
    await stream.aclose()
    assert app._asking == 0
    assert not (set(asyncio.all_tasks()) - before)


async def test_provider_initiated_cancellation_propagates_and_releases_document():
    class CancelledLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.call_type != "answer":
                async for frame in super().stream(request):
                    yield frame
                return
            raise asyncio.CancelledError("provider stopped")
            yield  # Preserve the adapter async-iterator protocol.

    app = Application(OllamaEmbedder(), LLMGateway(CancelledLLM(["not JSON"])))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    stream = app.ask("What does this say?")
    for expected in ["plan", "retrieval", "citation_map"]:
        assert (await anext(stream)).type == expected
    before = set(asyncio.all_tasks())
    pending = asyncio.create_task(anext(stream))
    # asyncio.wait does not cancel the request, so timeout cannot hide a hang.
    done, _ = await asyncio.wait({pending}, timeout=1)
    try:
        assert pending in done, "Provider cancellation must reach the public consumer"
        with pytest.raises(asyncio.CancelledError):
            await pending
    finally:
        if not pending.done():
            pending.cancel()
            with pytest.raises(asyncio.CancelledError):
                await pending
        await stream.aclose()
    assert app._asking == 0
    assert app.history == []
    assert not (set(asyncio.all_tasks()) - before)


@pytest.mark.parametrize("question_type", ["Lookup", "Global"])
async def test_ask_started_during_replacement_stays_rejected_when_upload_finishes(question_type):
    import json

    held = asyncio.Event()
    release = asyncio.Event()

    class HeldSummaryLLM(SummaryScriptedLLM):
        hold = False

        async def stream(self, request):
            if request.call_type == "document_summary" and self.hold:
                held.set()
                await release.wait()
            async for frame in super().stream(request):
                yield frame

    route = json.dumps(
        {
            "question_type": question_type,
            "standalone_question": "Describe the Document",
            "sub_queries": [],
        }
    )
    citation = "S1" if question_type == "Global" else "C1"
    llm = HeldSummaryLLM([route, f"Evidence [{citation}]."] * 2)
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    original = [e async for e in app.upload_document(text_pdf("Original Document"), "old.pdf")]
    assert original[-1].type == "ready"
    llm.hold = True
    replacement = app.start_upload(text_pdf("Replacement Document"), "new.pdf")
    await asyncio.wait_for(held.wait(), 3)
    stream = app.ask("Describe the Document")
    # FIFO scheduling: ask begins while upload is held; releasing the final
    # external summary call lets upload publish before asynchronous graph work.
    pending = asyncio.create_task(anext(stream))
    release.set()
    first = await asyncio.wait_for(pending, 3)
    uploaded = [e async for e in app.upload_events(replacement)]
    assert uploaded[-1].type == "ready"
    assert uploaded[-1].document_id != original[-1].document_id
    events = [first, *[e async for e in stream]]
    assert [e.type for e in events] == ["error"], [e.model_dump() for e in events]
    assert events[0].code == "document_not_ready"
    assert llm.ask_calls == []
    assert app.history == []
    assert app._asking == 0
    recovered = [e async for e in app.ask("Describe the Document")]
    final = next(e for e in recovered if e.type == "final")
    assert final.citations
    assert all(app.source(c.source_id) for c in final.citations)
    assert all(c.source_id.startswith(uploaded[-1].document_id) for c in final.citations)
    assert len(app.history) == 1
