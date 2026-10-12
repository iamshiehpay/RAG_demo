from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

from .fixtures import heading_free_pdf, paragraph_pdf, scanned_pdf, structured_pdf, text_pdf


@pytest.mark.parametrize(
    "content", [b"not a PDF", b"", text_pdf("")[:-100]], ids=["non-pdf", "empty", "truncated"]
)
async def test_invalid_document_has_a_distinct_error_from_missing_text_layer(content):
    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(content, "invalid.pdf")]
    assert [e.type for e in events] == ["stage", "error"]
    assert events[-1].code == "invalid_document"
    assert "valid PDF" in events[-1].message
    assert "text layer" not in events[-1].message
    assert app.document is None and llm.calls == []


async def test_lightrag_sections_exclude_references_and_keep_appendix():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "lightrag.pdf")
    ]
    assert events[-1].type == "ready"
    document = app.document
    titles = {s.title.upper() for s in document.sections}
    assert {
        "1 INTRODUCTION",
        "2 RETRIEVAL-AUGMENTED GENERATION",
        "3 THE LIGHTRAG ARCHITECTURE",
        "4 EVALUATION",
        "5 RELATED WORK",
        "6 CONCLUSION",
        "7 APPENDIX",
    } <= titles
    # These bibliography-only pages and a distinctive bibliography entry never enter the Index.
    assert not any(c.page_start <= 12 and c.page_end >= 11 for c in document.chunks)
    assert "Rag-ex: A generic" not in "\n".join(c.text for c in document.chunks)
    appendix = [c for c in document.chunks if c.page_start >= 13]
    assert appendix and all("APPENDIX" in c.section.upper() for c in appendix)
    # Table headers remain content of their actual Section, not artificial headings.
    assert not any(s.title.casefold().endswith("— mix") for s in document.sections)
    assert "Statistics" in "\n".join(c.text for c in appendix)
    for chunk in document.chunks:
        section = next(s for s in document.sections if s.id == chunk.section_id)
        assert chunk.section == section.title
        assert section.page_start <= chunk.page_start <= chunk.page_end <= section.page_end
        assert section.title in chunk.context


async def test_image_only_document_reports_missing_text_layer_before_embedding():
    llm = ScriptedLLM([])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(scanned_pdf(), "scan.pdf")]
    assert [e.type for e in events] == ["stage", "error"]
    assert events[-1].code == "invalid_document"
    assert "no text layer" in events[-1].message
    assert "scanned PDFs" in events[-1].message
    assert app.document is None and llm.calls == []


@pytest.mark.parametrize("body_size", [8, 13])
async def test_relative_headings_preserve_paragraphs_section_boundaries_and_pages(body_size):
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(structured_pdf(body_size), "structure.pdf")]
    assert events[-1].type == "ready"
    document = app.document
    assert [s.title for s in document.sections] == ["1 Introduction", "Methods", "Appendix A"]
    intro = document.sections[0]
    assert (intro.page_start, intro.page_end) == (1, 2)
    assert len(intro.paragraphs) == 3
    for chunk in document.chunks:
        section = next(s for s in document.sections if s.id == chunk.section_id)
        assert chunk.text == "\n\n".join(section.paragraphs)
        assert count_tokens(chunk.text) <= 500
        assert "BIBLIOGRAPHY_ONLY" not in chunk.text
        markers = {"INTRO_", "METHOD_", "APPENDIX_"}
        assert sum(marker in chunk.text for marker in markers) == 1
        assert chunk.page_start == section.page_start and chunk.page_end == section.page_end
    assert document.sections[-1].is_appendix


async def test_heading_free_document_uses_bounded_virtual_sections_and_can_be_asked():
    llm = ScriptedLLM(["The Document contains ordinary body text. [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(heading_free_pdf(), "plain.pdf")]
    assert events[-1].type == "ready"
    assert len(app.document.sections) > 1
    assert all(
        s.is_virtual and s.title.startswith("Virtual Section") for s in app.document.sections
    )
    assert all(count_tokens("\n\n".join(s.paragraphs)) <= 500 for s in app.document.sections)
    assert all(count_tokens(c.text) <= 500 for c in app.document.chunks)
    answer = [e async for e in app.ask("What text does the Document contain?")]
    assert any(e.type == "final" and e.citations for e in answer)
    assert not any(e.type == "error" for e in answer)
    citation = next(e for e in answer if e.type == "final").citations[0]
    source = app.source(citation.source_id)
    assert source.section == citation.section
    assert (source.page_start, source.page_end) == (citation.page_start, citation.page_end)


async def test_long_paragraph_overlap_starts_on_a_complete_word():
    words = [f"encyclopediawordnumber{i}" for i in range(400)]
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(paragraph_pdf(" ".join(words)), "words.pdf")]
    assert events[-1].type == "ready"
    chunks = app.document.chunks
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.text.split()[0] in words
        assert chunk.text.split()[-1] in words
        assert count_tokens(chunk.text) <= 500
    for left, right in zip(chunks, chunks[1:], strict=False):
        left_words, right_words = left.text.split(), right.text.split()
        overlap = left_words.index(right_words[0])
        assert left_words[overlap:] == right_words[: len(left_words) - overlap]
        assert 35 <= count_tokens(" ".join(left_words[overlap:])) <= 60


@pytest.mark.parametrize("target", [35, 60])
async def test_configured_chunk_size_packs_whole_paragraphs_without_overlap(target):
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=target)
    events = [e async for e in app.upload_document(structured_pdf(), "structure.pdf")]
    assert events[-1].type == "ready"
    document = app.document
    assert len(document.chunks) > len(document.sections)
    for section in document.sections:
        chunks = [c for c in document.chunks if c.section_id == section.id]
        assert "\n\n".join(c.text for c in chunks) == "\n\n".join(section.paragraphs)
        assert all(count_tokens(c.text) <= target for c in chunks)
        for chunk in chunks:
            contained = [i for i, p in enumerate(section.paragraphs) if p in chunk.text]
            assert contained
            assert chunk.page_start == min(section.paragraph_pages[i][0] for i in contained)
            assert chunk.page_end == max(section.paragraph_pages[i][1] for i in contained)


@pytest.mark.parametrize("cjk", [False, True], ids=["english", "chinese"])
async def test_long_paragraphs_split_at_sentence_boundaries_with_overlap(cjk):
    text = (
        "".join(f"這是第{i}句文件內容，保留數字和完整句子。" for i in range(100))
        if cjk
        else " ".join(f"Sentence {i} describes the Document and its evidence!" for i in range(100))
    )
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(paragraph_pdf(text, cjk=cjk), "sentences.pdf")]
    assert events[-1].type == "ready"
    chunks = app.document.chunks
    assert len(chunks) > 1
    assert all(c.text.rstrip().endswith("。" if cjk else "!") for c in chunks)
    assert all(count_tokens(c.text) <= 500 for c in chunks)
    for left, right in zip(chunks, chunks[1:], strict=False):
        shared = max(
            (
                size
                for size in range(1, min(len(left.text), len(right.text)) + 1)
                if left.text[-size:] == right.text[:size]
            ),
            default=0,
        )
        assert shared > 0
        assert 20 <= count_tokens(left.text[-shared:]) <= 55
