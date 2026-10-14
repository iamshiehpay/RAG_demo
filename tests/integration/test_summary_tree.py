import json
from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens
from tests.support import structured_pdf, summary_pdf, summary_response


async def test_upload_builds_proportional_section_summaries_and_overview():
    llm = ScriptedLLM(
        [
            summary_response("Introduction summary"),
            summary_response("Methods summary"),
            summary_response("Appendix summary"),
            "Overview",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(structured_pdf(), "Document.pdf")]
    assert events[-1].type == "ready"
    assert events[-1].document_summary == "Overview"
    tree = app.document.summary_tree
    assert tree.document_summary.text == "Overview"
    assert len(tree.section_summaries) == 3
    for summary, request in zip(tree.section_summaries, llm.calls, strict=False):
        chunks = [c for c in app.document.chunks if c.section_id in summary.section_ids]
        target = max(80, min(500, round(count_tokens("\n\n".join(c.text for c in chunks)) * 0.15)))
        assert summary.target_tokens == target
        assert summary.chunk_ids == [c.id for c in chunks]
        assert f"Target {target} tokens" in request.messages[0]["content"]
        assert request.call_type == "section_summary"
        assert request.think == "low" and request.num_predict == 1200
    progress = [e for e in events if e.type == "stage" and e.stage == "summary"]
    assert [e.completed for e in progress] == [0, 1, 2, 3, 4]
    assert all(e.total == 4 for e in progress)


async def test_global_uses_summary_sources_without_query_embedding_and_cache_reuses_tree(tmp_path):
    class RecordingEmbedder(OllamaEmbedder):
        def __init__(self):
            super().__init__()
            self.calls = []

        async def embed(self, texts):
            self.calls.append(texts)
            return await super().embed(texts)

    llm = ScriptedLLM(
        [
            summary_response("Introduction summary"),
            summary_response("Methods summary"),
            summary_response("Appendix summary"),
            "Overview",
            json.dumps(
                {"question_type": "Global", "standalone_question": "Summarize", "sub_queries": []}
            ),
            "Summary answer [S1].",
        ]
    )
    embedder = RecordingEmbedder()
    app = Application(embedder, LLMGateway(llm), cache=ProcessingCache(tmp_path))
    content = structured_pdf()
    assert [e async for e in app.upload_document(content, "first.pdf")][-1].type == "ready"
    embedding_count = len(embedder.calls)
    events = [e async for e in app.ask("Summarize", history=[])]
    assert next(e for e in events if e.type == "retrieval").chunks == []
    assert len(embedder.calls) == embedding_count

    final = next(e for e in events if e.type == "final")
    assert final.citations[0].id == "S1"
    source = app.source(final.citations[0].source_id)
    assert source.text == summary_response("Introduction summary")
    assert (source.page_start, source.page_end) == (1, 2)
    assert source.section_ids == [app.document.sections[0].id]
    assert llm.calls[-1].think == "medium" and llm.calls[-1].call_type == "answer"
    assert "Introduction summary" in llm.calls[-1].messages[-1]["content"]
    assert next(e for e in events if e.type == "trace").summary_level == "section"
    replay_llm = ScriptedLLM([])
    replay = Application(embedder, LLMGateway(replay_llm), cache=ProcessingCache(tmp_path))
    uploaded = [e async for e in replay.upload_document(content, "second.pdf")]
    assert [e.type for e in uploaded] == ["ready"]
    assert uploaded[-1].document_summary == "Overview"
    assert replay.document.summary_tree == app.document.summary_tree
    assert replay_llm.calls == []
    assert len(embedder.calls) == embedding_count


async def test_long_document_builds_adjacent_groups_and_global_uses_best_fitting_layer():
    class SummariesLLM(ScriptedLLM):
        async def stream(self, request):
            text = {
                "section_summary": "Detailed finding. " * 100,
                "group_summary": "Grouped finding. " * 20,
                "document_summary": "Overview",
                "router": json.dumps(
                    {
                        "question_type": "Global",
                        "standalone_question": "Summarize",
                        "sub_queries": [],
                    }
                ),
                "answer": "Grouped answer [S1].",
            }[request.call_type]
            self.scripts.append(text)
            async for frame in super().stream(request):
                yield frame

    llm = SummariesLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    uploaded = [e async for e in app.upload_document(summary_pdf(22), "long.pdf")]
    assert uploaded[-1].type == "ready"
    tree = app.document.summary_tree
    assert tree.group_levels
    assert [id for s in tree.group_levels[0] for id in s.section_ids] == [
        id for s in tree.section_summaries for id in s.section_ids
    ]
    events = [e async for e in app.ask("Summarize", history=[])]
    assert events[-1].summary_level == "group:1"
    final = next(e for e in events if e.type == "final")
    source = app.source(final.citations[0].source_id)
    assert source.kind == "group"
    assert len(source.section_ids) > 1
    assert source.section_titles
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


async def test_oversized_section_is_split_and_merged_before_budget_guard():
    llm = ScriptedLLM(
        [
            "First evidence summary",
            "Second evidence summary",
            summary_response("Merged summary"),
            "Overview",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    uploaded = [
        e async for e in app.upload_document(summary_pdf(words=2200, height=18000), "oversized.pdf")
    ]
    assert uploaded[-1].type == "ready", uploaded[-1]
    source = "\n\n".join(c.text for c in app.document.chunks)
    assert count_tokens(source) > 8500
    summaries = [c for c in llm.calls if c.call_type == "section_summary"]
    assert len(summaries) == 3
    assert "First evidence summary" in summaries[-1].messages[-1]["content"]
    assert "Second evidence summary" in summaries[-1].messages[-1]["content"]
    tree = app.document.summary_tree
    assert len(tree.section_summaries) == 1
    assert tree.section_summaries[0].target_tokens == 500
    assert tree.section_summaries[0].chunk_ids == [c.id for c in app.document.chunks]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


async def test_heading_only_sections_are_skipped():
    from tests.support import SummaryScriptedLLM

    llm = SummaryScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    uploaded = [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ]
    assert uploaded[-1].type == "ready"
    empty = {
        s.id
        for s in app.document.sections
        if not any(c.section_id == s.id for c in app.document.chunks)
    }
    assert empty
    tree = app.document.summary_tree
    assert not tree.group_levels
    assert not empty.intersection(id for s in tree.section_summaries for id in s.section_ids)
    assert len([c for c in llm.calls if c.call_type == "section_summary"]) == len(
        app.document.sections
    ) - len(empty)


@pytest.mark.parametrize("configured,expected", [(None, 4), (2, 2)])
async def test_summary_concurrency_is_bounded_and_progress_keeps_ask_disabled(
    configured, expected, monkeypatch
):
    import asyncio

    class HeldLLM(ScriptedLLM):
        def __init__(self):
            super().__init__([summary_response("Summary")] * 7)
            self.active = self.maximum = 0
            self.entered = asyncio.Event()
            self.release = asyncio.Event()

        async def stream(self, request):
            self.active += 1
            self.maximum = max(self.maximum, self.active)
            if self.active == expected:
                self.entered.set()
            try:
                await self.release.wait()
                async for frame in super().stream(request):
                    yield frame
            finally:
                self.active -= 1

    llm = HeldLLM()
    monkeypatch.delenv("SUMMARY_CONCURRENCY", raising=False)
    app = Application(OllamaEmbedder(), LLMGateway(llm), summary_concurrency=configured)
    job = app.start_upload(summary_pdf(6), "Document.pdf")
    await asyncio.wait_for(llm.entered.wait(), timeout=15)
    assert app.document is None
    assert [e async for e in app.ask("Summarize")][-1].code == "document_not_ready"
    llm.release.set()
    uploaded = [e async for e in app.upload_events(job)]
    assert uploaded[-1].type == "ready"
    assert llm.maximum == expected and llm.active == 0


@pytest.mark.parametrize("words", [1, 200, 1000])
async def test_section_summary_length_target_covers_minimum_proportional_and_maximum(words):
    llm = ScriptedLLM([summary_response("Section Summary"), "Overview"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    uploaded = [e async for e in app.upload_document(summary_pdf(words=words), "Document.pdf")]
    assert uploaded[-1].type == "ready"
    original = "\n\n".join(app.document.sections[0].paragraphs)
    target = max(80, min(500, round(count_tokens(original) * 0.15)))
    assert app.document.summary_tree.section_summaries[0].target_tokens == target
    assert f"Target {target} tokens" in llm.calls[0].messages[0]["content"]
    assert target == 80 if words == 1 else target == 500 if words == 1000 else 80 < target < 500
    assert llm.calls[0].num_predict == 1200


async def test_failed_summary_replacement_keeps_previous_document_and_no_partial_cache(tmp_path):
    from chat_document.llm_adapter import LLMFrame

    llm = ScriptedLLM(
        [
            summary_response("Original Section Summary"),
            "Original Overview",
            [LLMFrame(content="Truncated summary"), LLMFrame(done=True, done_reason="length")],
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path))
    content = summary_pdf()
    assert [e async for e in app.upload_document(content, "original.pdf")][-1].type == "ready"
    previous = app.document
    records = list(tmp_path.glob("*.json"))
    failed = [e async for e in app.upload_document(summary_pdf(words=101), "replacement.pdf")]
    assert failed[-1].type == "error"
    assert not any(e.type == "ready" for e in failed)
    assert "truncated" in failed[-1].message.lower()
    assert app.document is previous
    assert list(tmp_path.glob("*.json")) == records
    assert not list(tmp_path.glob("*.tmp"))
