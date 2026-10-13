"""Integrated table sources, Summary Tree provenance and cache through public operations."""

import json

import pymupdf
import pytest

from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tables import LIMITATION


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
                    "section_summary": "Measured result. " * (95 if section_count > 1 else 1),
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
