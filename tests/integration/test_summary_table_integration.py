"""Integrated table sources, Summary Tree provenance and cache through public operations."""

import json

import pymupdf
import pytest

from app.application import Application
from app.cache import ProcessingCache
from app.embedder import OllamaEmbedder
from app.llm_gateway import LLMGateway
from app.tables import LIMITATION
from app.tokens import count_tokens
from eval.fakes import ScriptedLLM
from tests.support import DeterministicEmbedder, SummaryScriptedLLM, selection_response


def table_only_pdf(section_count):
    with pymupdf.open() as pdf:
        for index in range(section_count):
            page = pdf.new_page()
            page.insert_text((50, 50), f"{index + 1} Measurements", fontsize=14)
            page.insert_text((50, 90), "Table 7: Measured results.", fontsize=10)
            for row, values in enumerate(
                [
                    ["Experiment", "Accuracy", "Cost"],
                    ["alpha", "12.5%", "3.75"],
                    ["beta", "", "4.75"],  # Missing cell: reconstruction is uncertain.
                ]
            ):
                for x, value in zip([50, 250, 400], values, strict=True):
                    if value:
                        page.insert_text((x, 120 + row * 18), value, fontsize=10)
        return pdf.tobytes()


@pytest.mark.parametrize("section_count", [1, 18])
async def test_table_only_sections_keep_all_sources_caveat_and_global_cache(
    section_count, tmp_path, monkeypatch
):
    class SummariesLLM(ScriptedLLM):
        async def stream(self, request):
            self.scripts.append(
                {
                    "section_summary": "Measured result. " * (95 if section_count > 1 else 25),
                    "group_summary": "Grouped measurement.",
                    "document_summary": "Overview.",
                    "router": json.dumps(
                        {
                            "question_type": "Global",
                            "standalone_question": "Summarize",
                            "sub_queries": [],
                        }
                    ),
                    "answer": "Table structure could not be reliably reconstructed. [S1]",
                }[request.call_type]
            )
            async for frame in super().stream(request):
                yield frame

    content = table_only_pdf(section_count)
    llm = SummariesLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm), cache=ProcessingCache(tmp_path))
    events = [e async for e in app.upload_document(content, "tables.pdf")]
    assert events[-1].type == "ready", events[-1]
    tree = app.document.summary_tree
    assert len(tree.section_summaries) == section_count
    assert all(not s.paragraphs and s.tables for s in app.document.sections)
    assert all(c.kind == "table" and not c.table_reconstructed for c in app.document.chunks)
    for summary in tree.section_summaries:
        assert summary.chunk_ids == [
            c.id for c in app.document.chunks if c.section_id in summary.section_ids
        ]
        assert LIMITATION in summary.text
    assert LIMITATION in events[-1].document_summary
    if section_count > 1:
        assert tree.group_levels
        assert all(LIMITATION in s.text for level in tree.group_levels for s in level)
        assert [id for s in tree.group_levels[-1] for id in s.chunk_ids] == [
            c.id for c in app.document.chunks
        ]

    assert [c.call_type for c in llm.calls].count("section_summary") == section_count
    assert [c.call_type for c in llm.calls].count("group_summary") == sum(
        len(level) for level in tree.group_levels
    )
    assert [c.call_type for c in llm.calls].count("document_summary") == 1
    assert len(llm.calls) == section_count + sum(len(level) for level in tree.group_levels) + 1
    for chunk in app.document.chunks:
        assert app.source(chunk.id) == chunk  # The original uncertain Table Chunk stays resolvable.

    replay_llm = SummariesLLM([])
    replay = Application(OllamaEmbedder(), LLMGateway(replay_llm), cache=ProcessingCache(tmp_path))
    assert [e.type async for e in replay.upload_document(content, "cached.pdf")] == ["ready"]
    assert replay.document == app.document.model_copy(update={"name": "cached.pdf"})
    assert replay_llm.calls == []

    async def must_not_retrieve(*args, **kwargs):
        pytest.fail("Global must bypass query embedding and retrieval")

    monkeypatch.setattr(replay.context_packer, "retrieve", must_not_retrieve)
    asked = [e async for e in replay.ask("Summarize", history=[])]
    assert not any(e.type == "error" for e in asked)
    retrieved = next(e for e in asked if e.type == "retrieval")
    assert retrieved.chunks == [] and retrieved.dropped_chunk_count == 0
    assert asked[-1].summary_level == ("section" if section_count == 1 else "group:1")
    assert asked[-1].dropped_chunk_count == 0
    final = next(e for e in asked if e.type == "final")
    assert LIMITATION in replay.source(final.citations[0].source_id).text
    assert LIMITATION in replay_llm.calls[-1].messages[-1]["content"]
    assert [c.call_type for c in replay_llm.calls] == ["router", "answer"]
    assert all(
        c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls + replay_llm.calls
    )


async def test_section_summary_partitions_preserve_complete_table_chunks():
    with pymupdf.open() as pdf:
        for index in range(12):
            page = pdf.new_page(width=600, height=1600)
            if index == 0:
                page.insert_text((50, 40), "1 Measurements", fontsize=14)
            page.insert_text((50, 80), f"Table {index + 1}: Measurement comparison.", fontsize=10)
            for row in range(71):
                cells = (
                    ["Trial", "Baseline", "Variant"]
                    if row == 0
                    else [f"trial_{index}_{row}", f"{row}.2%", f"{row}.8%"]
                )
                for x, text in zip([50, 240, 420], cells, strict=True):
                    page.insert_text((x, 110 + row * 16), text, fontsize=10)
        content = pdf.tobytes()

    class SummariesLLM(ScriptedLLM):
        async def stream(self, request):
            self.scripts.append(
                selection_response(request)
                if request.format and "span_ids" in str(request.format)
                else "Measured finding. " * 25
            )
            async for frame in super().stream(request):
                yield frame

    llm = SummariesLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(content, "table-heavy.pdf")]
    assert events[-1].type == "ready", events[-1]
    assert len(app.document.sections) == 1
    chunks = app.document.chunks
    assert chunks and all(c.kind == "table" and count_tokens(c.text) <= 2000 for c in chunks)
    requests = [
        c
        for c in llm.calls
        if c.call_type == "section_summary" and "Table " in c.messages[-1]["content"]
    ]
    assert len(requests) > 1
    assert app.document.summary_tree.section_summaries[0].chunk_ids == [c.id for c in chunks]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)
    for chunk in chunks:
        complete_parts = []
        for request in requests:
            if request.format and "span_ids" in str(request.format):
                original = json.loads(request.messages[-1]["content"])["source_units"].values()
                if any(
                    unit["chunk_id"] == chunk.id and unit.get("original_text") == chunk.text
                    for unit in original
                ):
                    complete_parts.append(request)
            elif chunk.text in request.messages[-1]["content"]:
                complete_parts.append(request)
        assert len(complete_parts) == 1, f"{chunk.id} was split inside a Table Chunk"
    originals = {chunk.id: chunk for chunk in chunks}
    for request in requests:
        if not (request.format and "span_ids" in str(request.format)):
            continue
        payload = json.loads(request.messages[-1]["content"])
        for span in payload["spans"]:
            source = payload["source_units"][span["source_unit"]]
            original = originals[source["chunk_id"]]
            assert span["text"] in original.text, "A generated draft replaced original evidence"
            if span["kind"] == "row":
                assert source["caption"] == original.table_caption
                assert source["header"] == " | ".join(original.table_headers)


async def test_upload_keeps_recursive_selection_batches_feasible_after_narrowing():
    """Replay the native selection decisions that reached the 74-token dead end.

    The replay uses fresh public PDF upload and original source validation, not
    direct builder calls. Recorded IDs are decisions, never generated evidence.
    Newly balanced pools use a source-only scripted selection at the same seam.
    """
    from collections import defaultdict, deque
    from pathlib import Path

    from eval.second_document import DOCUMENT
    from tests.support import selection_response

    if not DOCUMENT.exists():
        pytest.skip("Fetch the pinned second Document before this source regression")
    decisions = defaultdict(deque)
    fixture = Path(__file__).parents[1] / "data/summary_selection_replay.json"
    for recorded in json.loads(fixture.read_text())["decisions"]:
        decisions[tuple(recorded["offered_span_ids"])].append(recorded["response"])

    class ReplayLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.format and "span_ids" in str(request.format):
                self.calls.append(request)
                payload = json.loads(request.messages[-1]["content"])
                key = tuple(s["id"] for s in payload["spans"])
                script = (
                    decisions[key].popleft()
                    if payload["section"] == "Appendix C Industrial Implications" and decisions[key]
                    else selection_response(request)
                )
                async for frame in ScriptedLLM([script]).stream(request):
                    yield frame
            else:
                async for frame in super().stream(request):
                    yield frame

    llm = ReplayLLM([])
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    try:
        events = [
            e async for e in app.upload_document(DOCUMENT.read_bytes(), "narrowed-source.pdf")
        ]
        assert events[-1].type == "ready", events[-1]
        requests = [
            json.loads(c.messages[-1]["content"])
            for c in llm.calls
            if c.format and "span_ids" in str(c.format)
        ]
        appendix = [p for p in requests if p["section"] == "Appendix C Industrial Implications"]
        assert len(appendix) > 4 and any(
            any("original_text" not in unit for unit in p["source_units"].values())
            for p in appendix
        )
        for node in app.document.summary_tree.section_summaries:
            assert 80 <= count_tokens(node.text) <= 500
            assert node.chunk_ids and all(app.source(i).id == i for i in node.chunk_ids)
        assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)
    finally:
        await app.close()
