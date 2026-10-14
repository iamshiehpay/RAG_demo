"""Application regressions with real parser and shared guard.

Success paths use real local bge-m3 and a scripted LLM. The exceptionally large
recursive and pathological-provider probes use fake embeddings; the sibling
failure/cancellation probe uses real bge-m3.
These prove orchestration and request contracts, not cloud answer quality (#11).
"""

import json

import numpy as np
import pytest

from app.application import Application
from app.embedder import OllamaEmbedder
from app.llm_gateway import LLMGateway
from tests.support import SummaryScriptedLLM, summary_response, text_pdf


class FixedEmbedder:
    model = "test-embedding"

    async def embed(self, texts):
        return np.ones((len(texts), 3), dtype=np.float32)


@pytest.mark.parametrize("question_type", ["Lookup", "Synthesis"])
async def test_literal_summary_marker_in_chunk_keeps_chunk_citations(question_type):
    class PromptDrivenLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if not request.call_type.endswith("summary"):
                self.scripts.append(
                    json.dumps(
                        dict(
                            question_type=question_type,
                            standalone_question="Explain the measurement.",
                            sub_queries=[],
                        )
                    )
                    if request.call_type == "router"
                    else "The measurement is stable "
                    + ("[S1]." if "[S#]" in request.messages[0]["content"] else "[C1].")
                )
            async for frame in super().stream(request):
                yield frame

    llm = PromptDrivenLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [
        e
        async for e in app.upload_document(
            text_pdf("Measurement is stable, as shown in supplementary [S1]."), "measurement.pdf"
        )
    ][-1].type == "ready"
    events = [e async for e in app.ask("Explain the measurement.")]
    final = next(e for e in events if e.type == "final")
    assert not final.unverified
    assert [c.id for c in final.citations] == ["C1"]
    prompt = llm.ask_calls[-1].messages
    assert "[C#]" in prompt[0]["content"]
    assert "[S#]" not in prompt[0]["content"]
    assert "[S1]" in prompt[-1]["content"]


async def test_global_non_rag_document_uses_generic_whole_document_prompt():
    llm = SummaryScriptedLLM(
        [
            json.dumps(
                dict(
                    question_type="Global",
                    standalone_question="Summarize in three sentences.",
                    sub_queries=[],
                )
            ),
            "The instrument measures rainfall [S1].",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [
        e
        async for e in app.upload_document(
            text_pdf(
                "A rainfall instrument measures seasonal precipitation and calibration error."
            ),
            "rainfall.pdf",
        )
    ][-1].type == "ready"
    events = [e async for e in app.ask("Summarize in three sentences.")]
    assert next(e for e in events if e.type == "final").citations[0].id == "S1"
    system = llm.ask_calls[-1].messages[0]["content"].lower()
    for topic in (
        "lightrag",
        "graphrag",
        "graph indexing",
        "retrieval levels",
        "incremental updates",
        "experimental datasets",
        "adaptability",
    ):
        assert topic not in system
    assert "whole document" in system
    assert "requested format" in system
    assert "baselines" in system and "qualifiers" in system
    assert "operation it measures" in system
    assert "[s#]" in system and "[c#]" not in system


async def test_supported_long_global_question_uses_upload_built_group_and_short_uses_sections():
    from eval.fakes import ScriptedLLM
    from tests.support import summary_pdf

    class SummaryResponses(ScriptedLLM):
        async def stream(self, request):
            self.scripts.append(
                {
                    "section_summary": "Rainfall finding. " * 75,
                    "group_summary": "Grouped precipitation findings. " * 30,
                    "document_summary": "Rainfall overview.",
                    "router": json.dumps(
                        dict(
                            question_type="Global",
                            standalone_question="Summarize " + "detail " * 490,
                            sub_queries=[],
                        )
                    ),
                    "answer": "Rainfall is measured [S1].",
                }[request.call_type]
            )
            # Keep a short standalone question when the current question is short.
            if (
                request.call_type == "router"
                and "Current question: Summarize.\n" in request.messages[-1]["content"]
            ):
                self.scripts[-1] = json.dumps(
                    dict(question_type="Global", standalone_question="Summarize.", sub_queries=[])
                )
            async for frame in super().stream(request):
                yield frame

    llm = SummaryResponses([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    uploaded = [e async for e in app.upload_document(summary_pdf(18), "rainfall.pdf")]
    assert uploaded[-1].type == "ready"
    tree = app.document.summary_tree
    from app.summary_context import summary_context
    from app.tokens import count_tokens

    assert 5000 < count_tokens(summary_context(tree.section_summaries)) < 6000
    short = [e async for e in app.ask("Summarize.", history=[])]
    assert next(e for e in short if e.type == "trace").summary_level == "section"
    count_before = len(llm.calls)
    question = "Summarize " + "detail " * 996
    assert count_tokens(question) == 1000
    long = [e async for e in app.ask(question, history=[])]
    assert next(e for e in long if e.type == "trace").summary_level == "group:1"
    assert tree.group_levels
    assert [c.call_type for c in llm.calls[count_before:]] == ["router", "answer"]
    assert not any(e.type == "error" for e in short + long)
    assert next(e for e in short if e.type == "retrieval").chunks == []
    assert next(e for e in long if e.type == "retrieval").chunks == []
    final = next(e for e in long if e.type == "final")
    assert app.source(final.citations[0].source_id).kind == "group"
    selected = tree.group_levels[0]
    assert [id for s in selected for id in s.chunk_ids] == [c.id for c in app.document.chunks]
    assert [id for s in selected for id in s.section_ids] == [s.id for s in app.document.sections]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


async def test_summary_progress_advances_during_group_and_document_calls():
    from eval.fakes import ScriptedLLM
    from tests.support import summary_pdf

    class ProgressLLM(ScriptedLLM):
        async def stream(self, request):
            self.scripts.append(
                "Evidence finding. " * 100
                if request.call_type == "section_summary"
                else "Merged finding."
            )
            async for frame in super().stream(request):
                yield frame

    llm = ProgressLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(summary_pdf(22), "progress.pdf")]
    assert events[-1].type == "ready"
    progress = [e for e in events if e.type == "stage" and e.stage == "summary"]
    section_count = len(app.document.summary_tree.section_summaries)
    group_count = sum(map(len, app.document.summary_tree.group_levels))
    assert group_count > 1
    assert progress[-1].completed == progress[-1].total == section_count + group_count + 1
    assert [e.completed for e in progress] == sorted(e.completed for e in progress)
    assert set(range(section_count + 1, section_count + group_count + 2)).issubset(
        e.completed for e in progress
    )
    assert all(e.completed < e.total for e in progress[:-1])
    assert (
        events.index(progress[-1])
        < next(i for i, e in enumerate(events) if e.type == "stage" and e.stage == "complete")
        < len(events) - 1
    )
    assert events[-1].document_summary == app.document.summary_tree.document_summary.text


async def test_each_oversized_section_part_and_merge_retains_section_title():
    from eval.fakes import ScriptedLLM
    from tests.support import summary_pdf

    llm = ScriptedLLM(
        ["First evidence", "Second evidence", summary_response("Merged evidence"), "Overview"]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [
        e async for e in app.upload_document(summary_pdf(words=2200, height=18000), "oversized.pdf")
    ]
    assert events[-1].type == "ready"
    requests = [c for c in llm.calls if c.call_type == "section_summary"]
    assert len(requests) == 3
    assert all("incomplete part" in c.messages[-1]["content"] for c in requests[:2])
    assert "Partial evidence summary 1/2" in requests[-1].messages[-1]["content"]
    assert "Partial evidence summary 2/2" in requests[-1].messages[-1]["content"]
    title = app.document.sections[0].title
    assert all(f"Section: {title}\n" in c.messages[-1]["content"] for c in requests)
    assert app.document.summary_tree.section_summaries[0].chunk_ids == [
        c.id for c in app.document.chunks
    ]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


async def test_adapter_and_answer_prompt_semantics_invalidate_upload_cache(tmp_path, monkeypatch):
    from pathlib import Path

    from app.cache import ProcessingCache, _pipeline_version

    llm = SummaryScriptedLLM([])
    content = text_pdf()
    before = _pipeline_version()
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path, pipeline_version=before)
    )
    assert [e async for e in app.upload_document(content, "first.pdf")][-1].type == "ready"
    call_count = len(llm.calls)
    assert call_count == 2
    assert [e async for e in app.upload_document(content, "replay.pdf")][-1].type == "ready"
    assert len(llm.calls) == call_count
    original_read = Path.read_bytes
    for dependency in ("llm_adapter.py", "answer_generator.py"):
        with monkeypatch.context() as patch:

            def changed_source(path, dependency=dependency):
                data = original_read(path)
                return (
                    data + b"\n# changed request semantics\n" if path.name == dependency else data
                )

            patch.setattr(Path, "read_bytes", changed_source)
            after = _pipeline_version()
        assert after != before
        replay = Application(
            OllamaEmbedder(),
            LLMGateway(llm),
            cache=ProcessingCache(tmp_path, pipeline_version=after),
        )
        assert [e async for e in replay.upload_document(content, "changed.pdf")][-1].type == "ready"
        assert len(llm.calls) == call_count + 2
        call_count = len(llm.calls)


async def test_oversized_section_recursively_merges_multiple_rounds_with_provenance():
    import pymupdf

    from eval.fakes import ScriptedLLM

    with pymupdf.open() as pdf:
        for index in range(32):
            page = pdf.new_page(width=1200, height=18000)
            if index == 0:
                page.insert_text((72, 60), "1 Rainfall measurements", fontsize=14)
            assert (
                page.insert_textbox(
                    pymupdf.Rect(72, 90, 1128, 17940),
                    "SOURCE_EVIDENCE records seasonal rainfall. " * 1800,
                    fontsize=8,
                )
                >= 0
            )
        content = pdf.tobytes()

    class RecursiveLLM(SummaryScriptedLLM):
        async def stream(self, request):
            evidence = request.messages[-1]["content"]
            if request.call_type == "section_summary":
                text = (
                    "Partial " * 1100
                    if "SOURCE_EVIDENCE" in evidence
                    else summary_response("Final finding")
                )
            elif request.call_type == "group_summary":
                text = "First " * 2400 if "Partial " in evidence else "Second " * 300
            else:
                text = "Overview"
            # Direct ScriptedLLM enforces output reservation for every generated script.
            self.calls.append(request)
            async for frame in ScriptedLLM([text]).stream(request):
                yield frame

    llm = RecursiveLLM([])
    app = Application(FixedEmbedder(), LLMGateway(llm))
    uploaded = [e async for e in app.upload_document(content, "recursive.pdf")]
    assert uploaded[-1].type == "ready", uploaded[-1]
    assert len(app.document.sections) == 1
    group_requests = [c for c in llm.calls if c.call_type == "group_summary"]
    assert any("Partial " in c.messages[-1]["content"] for c in group_requests)
    assert any("First " in c.messages[-1]["content"] for c in group_requests)
    assert app.document.summary_tree.section_summaries[0].chunk_ids == [
        c.id for c in app.document.chunks
    ]
    assert all(
        "Section: 1 Rainfall measurements\n" in c.messages[-1]["content"] for c in group_requests
    )
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


async def test_multiple_group_levels_preserve_all_original_sources():
    from eval.fakes import ScriptedLLM
    from tests.support import summary_pdf

    class MultiLevelLLM(ScriptedLLM):
        async def stream(self, request):
            evidence = request.messages[-1]["content"]
            self.scripts.append(
                # Published Section Summaries now enforce the existing 500-token
                # maximum. Group stress responses remain deliberately long to
                # exercise recursive complete-level provenance.
                "Section " * 450
                if request.call_type == "section_summary"
                else ("Group " * 2200 if "Section Section " in evidence else "Compressed finding.")
                if request.call_type == "group_summary"
                else "Overview"
            )
            async for frame in super().stream(request):
                yield frame

    llm = MultiLevelLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(summary_pdf(32), "levels.pdf")][-1].type == "ready"
    tree = app.document.summary_tree
    assert len(tree.group_levels) >= 2
    for level in tree.group_levels:
        assert [id for s in level for id in s.chunk_ids] == [c.id for c in app.document.chunks]
        assert [id for s in level for id in s.section_ids] == [s.id for s in app.document.sections]
        assert [title for s in level for title in s.section_titles] == [
            s.title for s in app.document.sections
        ]
    assert tree.document_summary.chunk_ids == [c.id for c in app.document.chunks]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)


@pytest.mark.parametrize("cancel_upload", [False, True])
async def test_inflight_section_siblings_cancel_and_replacement_is_transactional(
    tmp_path, cancel_upload
):
    import asyncio

    from app.cache import ProcessingCache
    from tests.support import summary_pdf

    class HeldFailureLLM(SummaryScriptedLLM):
        failing = False

        def __init__(self):
            super().__init__([])
            self.started = 0
            self.cancelled = 0
            self.entered = asyncio.Event()
            self.fail = asyncio.Event()

        async def stream(self, request):
            if not self.failing:
                async for frame in super().stream(request):
                    yield frame
                return
            self.calls.append(request)
            self.started += 1
            first = self.started == 1
            if self.started == 3:
                self.entered.set()
            try:
                if first and not cancel_upload:
                    await self.fail.wait()
                    raise ValueError("Section generation failed")
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                self.cancelled += 1
                raise

    llm = HeldFailureLLM()
    app = Application(
        OllamaEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path), summary_concurrency=3
    )
    assert [e async for e in app.upload_document(text_pdf(), "original.pdf")][-1].type == "ready"
    previous = app.document
    records = sorted(tmp_path.glob("*.json"))
    llm.failing = True
    job = app.start_upload(summary_pdf(6), "replacement.pdf")
    await asyncio.wait_for(llm.entered.wait(), 10)
    assert [e async for e in app.ask("Summarize")][-1].code == "document_not_ready"
    if cancel_upload:
        await app.close()
    else:
        llm.fail.set()
    events = await asyncio.wait_for(_collect_upload(app, job), 10)
    assert events[-1].type == "error"
    assert not any(e.type == "ready" for e in events)
    assert llm.cancelled == llm.started - (0 if cancel_upload else 1)
    assert 3 <= llm.started <= 4
    assert app.document is previous
    assert sorted(tmp_path.glob("*.json")) == records
    assert not list(tmp_path.glob("*.tmp"))


async def _collect_upload(app, job):
    return [e async for e in app.upload_events(job)]


@pytest.mark.parametrize("oversized_section", [False, True])
async def test_nonreducing_external_summary_response_fails_without_partial_publication(
    tmp_path, oversized_section
):
    """A pathological provider ignores output limits; merge defense must terminate.

    Every request still uses the real fixed guard. This is a failure injection,
    not evidence that an overlong provider response fits its output reservation.
    """
    import pymupdf

    from app.cache import ProcessingCache
    from app.llm_adapter import LLMFrame
    from eval.fakes import ScriptedLLM
    from tests.support import summary_pdf

    if oversized_section:
        with pymupdf.open() as pdf:
            for i in range(12):
                page = pdf.new_page(width=1200, height=18000)
                if i == 0:
                    page.insert_text((72, 60), "1 Rainfall measurements", fontsize=14)
                assert (
                    page.insert_textbox(
                        pymupdf.Rect(72, 90, 1128, 17940),
                        "SOURCE_EVIDENCE describes rainfall. " * 1800,
                        fontsize=8,
                    )
                    >= 0
                )
            replacement = pdf.tobytes()
    else:
        replacement = summary_pdf(22)

    class NonReducingLLM(SummaryScriptedLLM):
        failing = False

        async def stream(self, request):
            if not self.failing:
                async for frame in super().stream(request):
                    yield frame
                return
            self.calls.append(request)
            if request.call_type == "group_summary":
                yield LLMFrame(content=request.messages[-1]["content"])
                yield LLMFrame(done=True, done_reason="stop")
            else:
                # Oversized-Section partials are intermediate merge inputs;
                # ordinary published Sections must meet the 500-token maximum.
                async for frame in ScriptedLLM(
                    ["Finding " * (1100 if oversized_section else 450)]
                ).stream(request):
                    yield frame

    llm = NonReducingLLM([])
    app = Application(FixedEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path))
    assert [e async for e in app.upload_document(text_pdf(), "original.pdf")][-1].type == "ready"
    previous = app.document
    records = sorted(tmp_path.glob("*.json"))
    llm.failing = True
    events = [e async for e in app.upload_document(replacement, "replacement.pdf")]
    assert events[-1].type == "error"
    assert "did not reduce" in events[-1].message
    assert app.document is previous
    assert sorted(tmp_path.glob("*.json")) == records
    assert not list(tmp_path.glob("*.tmp"))
