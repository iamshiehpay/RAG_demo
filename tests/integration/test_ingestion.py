from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens
from tests.support import SummaryScriptedLLM as ScriptedLLM
from tests.support import (
    cjk_layout_pdf,
    heading_free_pdf,
    page_top_interruption_pdf,
    paragraph_pdf,
    router_script,
    scanned_pdf,
    structured_pdf,
    text_pdf,
)


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
    assert any(s.title.startswith("Appendix — 7.2 ") for s in document.sections)
    assert any(s.title.startswith("Appendix — 7.4 ") for s in document.sections)
    assert all(
        not s.title.endswith(".")
        for s in document.sections
        if s.title.startswith(("Appendix — 7.2 ", "Appendix — 7.4 "))
    )
    assert document.sections[0].title == "LIGHTRAG: SIMPLE AND FAST RETRIEVAL-AUGMENTED GENERATION"
    ablation = [c for c in document.chunks if c.section.startswith("4.3 ")]
    assert ablation and any(c.page_start == c.page_end == 8 for c in ablation)
    assert all(c.section.startswith("4.3 ") for c in document.chunks if "Table 2:" in c.text)
    assert not any(
        "Beekeeper" in p or "Query + LLM" in p or p == "\x10"
        for s in document.sections
        for p in s.paragraphs
    )
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
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=500)
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
    llm = ScriptedLLM(
        [
            router_script(question="What text does the Document contain?"),
            "The Document contains ordinary body text. [C1]",
        ]
    )
    app = Application(OllamaEmbedder(), LLMGateway(llm), chunk_token_target=500)
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
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=500)
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
    from chat_document.settings import RetrievalSettings

    llm = ScriptedLLM([router_script(question="Introduction"), "Evidence [C1]."])
    app = Application(
        OllamaEmbedder(),
        LLMGateway(llm),
        chunk_token_target=target,
        settings=RetrievalSettings(lookup_top_k=1),
    )
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
    answer = [e async for e in app.ask("Introduction")]
    retrieved = next(e for e in answer if e.type == "retrieval").chunks
    primary = await app.index.retrieve("Introduction", 1)
    assert {item.chunk.id for item in primary} <= {item.chunk.id for item in retrieved}
    assert 1 <= len(retrieved) <= 3
    assert any(e.type == "final" for e in answer)


@pytest.mark.parametrize("cjk", [False, True], ids=["english", "chinese"])
async def test_long_paragraphs_split_at_sentence_boundaries_with_overlap(cjk):
    text = (
        "".join(f"這是第{i}句文件內容，保留數字和完整句子。" for i in range(100))
        if cjk
        else " ".join(f"Sentence {i} describes the Document and its evidence!" for i in range(100))
    )
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=500)
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


@pytest.mark.parametrize(
    "case,title",
    [
        ("wrapped", "1. A Very Long Section Title That Wraps Onto Two Lines"),
        ("number", "1. Introduction"),
    ],
)
async def test_wrapped_and_number_only_headings_keep_the_complete_title(case, title):
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf(case), "heading.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == [title]
    assert all(c.section == title for c in app.document.chunks)


@pytest.mark.parametrize("case", ["lettered", "supplementary", "chinese"])
async def test_appendices_after_references_resume_indexing(case):
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf(case), "appendix.pdf")]
    assert events[-1].type == "ready"
    appendix = app.document.sections[-1]
    assert appendix.is_appendix and "Appendix" in appendix.title
    assert "APPENDIX_BODY" in "\n".join(appendix.paragraphs)
    assert "BIBLIOGRAPHY_ONLY" not in "\n".join(c.text for c in app.document.chunks)


async def test_two_column_reading_order_keeps_same_size_bold_headings_and_provenance():
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf("columns"), "columns.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == ["1 Introduction", "2 Methods", "3 Results"]
    for section, markers in zip(
        app.document.sections,
        [["LEFT_INTRO"], ["LEFT_METHOD"], ["RIGHT_RESULTS", "RIGHT_CONTINUED"]],
        strict=True,
    ):
        text = "\n".join(section.paragraphs)
        assert all(marker in text for marker in markers)
        assert all(
            marker not in text
            for marker in {"LEFT_INTRO", "LEFT_METHOD", "RIGHT_RESULTS", "RIGHT_CONTINUED"}
            - set(markers)
        )
        assert all(
            c.section == section.title for c in app.document.chunks if c.section_id == section.id
        )


async def test_body_size_numbered_small_caps_subsection_forms_a_chunk_boundary():
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf("subsection"), "subsection.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == ["4 Evaluation", "4.3 ABLATION STUDY"]
    assert "ABLATION_BODY" not in app.document.chunks[0].text
    assert "ABLATION_BODY" in app.document.chunks[1].text


async def test_figure_labels_are_filtered_without_discarding_short_prose_or_table_cells():
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf("figure"), "figure.pdf")]
    assert events[-1].type == "ready"
    text = "\n".join(c.text for c in app.document.chunks)
    assert "FIGURE_LABEL" not in text
    assert all(
        value in text
        for value in [
            "SHORT_REAL Yes.",
            "Figure 1",
            "Variant",
            "64.8",
            "Table 2",
            "TABLE_PARAGRAPH",
        ]
    )


async def test_references_only_document_reports_no_indexable_text():
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf("references-only"), "references.pdf")]
    assert events[-1].type == "error"
    assert "no indexable text outside References" in events[-1].message
    assert app.document is None


async def test_readable_repaired_pdf_is_accepted_and_logged(caplog):
    repaired = text_pdf("A readable repaired Document retains its real text.")[:-100]
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(repaired, "repaired.pdf")]
    assert events[-1].type == "ready"
    assert "readable repaired Document" in app.document.chunks[0].text
    assert "repair" in caplog.text.casefold()


async def test_configured_target_also_bounds_virtual_sections():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=80)
    events = [e async for e in app.upload_document(heading_free_pdf(), "plain.pdf")]
    assert events[-1].type == "ready"
    assert all(
        s.is_virtual and count_tokens("\n\n".join(s.paragraphs)) <= 80
        for s in app.document.sections
    )


async def test_settings_from_env_control_real_and_virtual_chunk_bounds(monkeypatch):
    from chat_document.settings import RetrievalSettings

    monkeypatch.setenv("CHUNK_TOKEN_TARGET", "80")
    settings = RetrievalSettings.from_env()
    assert settings.chunk_token_target == 80
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), settings=settings)
    events = [e async for e in app.upload_document(heading_free_pdf(), "settings.pdf")]
    assert events[-1].type == "ready"
    assert all(count_tokens(c.text) <= 80 for c in app.document.chunks)
    assert all(count_tokens("\n\n".join(s.paragraphs)) <= 80 for s in app.document.sections)


async def test_shaded_prose_above_a_figure_caption_preserves_every_line():
    from tests.support import shaded_prose_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(shaded_prose_pdf(), "shaded.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == ["1 Introduction"]
    text = "\n".join(c.text for c in app.document.chunks)
    assert all(f"PROSE_{word}" in text for word in ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX"])


@pytest.mark.parametrize(
    "title", ["1 Introduction", "Introduction"], ids=["numbered", "unnumbered"]
)
async def test_page_frame_does_not_remove_the_section_heading(title):
    from tests.support import page_frame_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(page_frame_pdf(title), "frame.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == [title]
    assert not app.document.sections[0].is_virtual
    assert "FRAME_BODY" in app.document.chunks[0].text


async def test_numbered_all_caps_period_headings_keep_their_own_appendix_content():
    from tests.support import review_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(review_pdf("period-headings"), "period.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == [
        "7 Appendix",
        "Appendix — 7.2 CASE EXAMPLE OF LIGHTRAG",
        "Appendix — 7.4 CASE STUDY OF NAIVERAG",
    ]
    for section, marker in zip(
        app.document.sections,
        ["APPENDIX_MAIN", "CASE_EXAMPLE_BODY", "CASE_STUDY_BODY"],
        strict=True,
    ):
        assert marker in "\n".join(section.paragraphs)
        assert all(c.section == section.title for c in app.document.chunks if marker in c.text)


async def test_bold_and_larger_figure_labels_do_not_create_sections_or_enter_prose():
    from tests.support import styled_figure_labels_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(styled_figure_labels_pdf(), "styled-figure.pdf")]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == ["1 Introduction"]
    text = "\n".join(c.text for c in app.document.chunks)
    assert all(value in text for value in ["REAL_BEFORE", "REAL_CONTINUED", "Figure 1"])
    assert "LLM" not in text and "Dual-level Retrieval" not in text
    assert all(c.section == "1 Introduction" for c in app.document.chunks)


@pytest.mark.parametrize("split", [False, True], ids=["inline", "split-number"])
async def test_numbered_uppercase_body_sentences_do_not_open_sections(split):
    from tests.support import numbered_sentences_pdf

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e async for e in app.upload_document(numbered_sentences_pdf(split=split), "sentences.pdf")
    ]
    assert events[-1].type == "ready"
    assert [s.title for s in app.document.sections] == ["1 Introduction"]
    text = "\n".join(c.text for c in app.document.chunks)
    assert all(
        value in text
        for value in [
            "BODY_BEFORE",
            "GPU HOURS.",
            "3. THE SOFTWARE IS PROVIDED AS IS.",
            "BODY_AFTER_COST",
            "BODY_AFTER_LICENSE",
        ]
    )
    assert all(c.section == "1 Introduction" for c in app.document.chunks)


async def test_wrapped_chinese_paragraph_splits_only_between_complete_sentences():
    sentences = [
        f"第{n}項觀察顯示，月球玄武岩的鐵含量在區域{n}中達到{n * 3 + 7}個單位。"
        for n in range(1, 161)
    ]
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=500)
    events = [
        e
        async for e in app.upload_document(
            paragraph_pdf("".join(sentences), cjk=True), "wrapped.pdf"
        )
    ]
    assert events[-1].type == "ready"
    chunks = app.document.chunks
    assert len(chunks) > 1
    assert all(count_tokens(sentence) < 50 for sentence in sentences)
    assert all(c.text.rstrip().endswith("。") for c in chunks)
    assert all(count_tokens(c.text) <= 500 for c in chunks)
    source = "\n\n".join(p for s in app.document.sections for p in s.paragraphs)
    assert all(f"區域{n}中達到{n * 3 + 7}個單位" in source for n in range(1, 161))
    combined = "".join(c.text.replace("\n", "") for c in chunks)
    assert all(sentence in combined for sentence in sentences)
    for chunk in chunks:
        # PDF line wraps must not change which complete source sentences a Chunk contains.
        compact = chunk.text.replace("\n", "")
        assert all(piece + "。" in sentences for piece in compact.split("。") if piece)


async def test_cjk_line_wraps_keep_numbers_intact_and_preserve_latin_spacing():
    prefix = "觀察記錄" * 8
    measurement = "測量記錄" * 8
    continuation = "測量記錄" * 7
    text = (
        f"{prefix}月球區域1\n4中含量為{measurement}4\n"
        f"9個單位，{continuation}觀察持續穩\n定。\n"
        "Sample 14\nstayed stable.\n英文版本Sample\n14也保留分隔。"
    )
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e async for e in app.upload_document(paragraph_pdf(text, cjk=True), "mixed-wraps.pdf")
    ]
    assert events[-1].type == "ready"
    source = "\n\n".join(p for s in app.document.sections for p in s.paragraphs)
    chunks = "\n\n".join(c.text for c in app.document.chunks)
    for extracted in (source, chunks):
        assert f"月球區域14中含量為{measurement}49個單位，{continuation}觀察持續穩定。" in extracted
        assert "Sample 14\nstayed stable." in extracted
        assert "Sample\n14也保留分隔。" in extracted


@pytest.mark.parametrize(
    "text",
    [
        "區域 數值\n1.2\n3.4\n2023\n2024",
        "數值\n" + "\n".join(["2023", "2024"] * 4),
        "區域 數值\n1 234\n2 345",
    ],
)
async def test_stacked_numeric_values_in_a_cjk_block_keep_their_separators(text):
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [e async for e in app.upload_document(paragraph_pdf(text, cjk=True), "values.pdf")]
    assert events[-1].type == "ready"
    assert app.document.sections[0].paragraphs == [text]
    assert app.document.chunks[0].text == text


@pytest.mark.parametrize("cjk", [False, True], ids=["english", "chinese"])
@pytest.mark.parametrize("finished", [False, True], ids=["continues", "new-paragraph"])
async def test_page_break_only_ends_a_paragraph_when_the_sentence_has_finished(cjk, finished):
    from tests.support import page_continuation_pdf

    first, second = (
        ("第一頁的段落延續到", "第二頁才結束。")
        if cjk
        else (
            "The first page describes the lunar rocks and continues",
            "onto the next page with the same paragraph.",
        )
    )
    if finished:
        first += "。" if cjk else "."
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e
        async for e in app.upload_document(
            page_continuation_pdf(first, second, cjk=cjk), "pages.pdf"
        )
    ]
    assert events[-1].type == "ready"
    section = app.document.sections[0]
    assert (section.page_start, section.page_end) == (1, 2)
    if finished:
        assert section.paragraphs == [first, second]
        assert section.paragraph_pages == [(1, 1), (2, 2)]
    else:
        assert len(section.paragraphs) == 1
        assert first in section.paragraphs[0] and second in section.paragraphs[0]
        assert section.paragraph_pages == [(1, 2)]
        assert "\n\n" not in app.document.chunks[0].text
    assert (app.document.chunks[0].page_start, app.document.chunks[0].page_end) == (1, 2)


async def test_short_cjk_sentence_overlap_starts_with_a_complete_sentence():
    sentences = [
        sentence
        for n in range(1, 9)
        for sentence in [f"第{n}次觀察" + "玄武岩含量" * 30 + "。", f"完成{n}！"]
    ]
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=200)
    events = [
        e
        async for e in app.upload_document(paragraph_pdf("".join(sentences), cjk=True), "short.pdf")
    ]
    assert events[-1].type == "ready"
    chunks = app.document.chunks
    assert len(chunks) > 1
    for chunk in chunks:
        assert count_tokens(chunk.text) <= 200
        assert any(chunk.text.startswith(sentence) for sentence in sentences)
    for left, right in zip(chunks, chunks[1:], strict=False):
        assert any(
            left.text.endswith(sentence) and right.text.startswith(sentence)
            for sentence in sentences
        )


@pytest.mark.parametrize(
    ("top", "cjk"),
    [
        ("Figure 3: An overview of the pipeline", False),
        ("Table 1: Comparison of the methods", False),
        ("期刊名稱 第十卷", True),
    ],
)
async def test_page_top_caption_or_header_does_not_extend_body_provenance(top, cjk):
    content, first, second = page_top_interruption_pdf(top, cjk=cjk)
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=40)
    try:
        events = [e async for e in app.upload_document(content, "interruption.pdf")]
        assert events[-1].type == "ready"
        section = app.document.sections[0]
        paragraph = next(p for p in section.paragraphs if first in p)
        assert paragraph == first
        assert section.paragraph_pages[section.paragraphs.index(paragraph)] == (1, 1)
        assert any(second in p and top not in p for p in section.paragraphs)
        assert any(top in p for p in section.paragraphs)  # Preserve source text.
        assert all(
            first + "\n\n" + top in c.text
            for c in app.document.chunks
            if first in c.text and top in c.text
        )  # Small independent paragraphs may share a Chunk, with their separator intact.
    finally:
        await app.close()


async def test_lightrag_page_top_tables_do_not_enter_previous_page_body():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    try:
        events = [
            e
            async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "paper.pdf")
        ]
        assert events[-1].type == "ready"
        for title, phrase, pages, caption in [
            ("4.2 ", "we draw the following conclusions:", (6, 6), "Table 1:"),
            ("4.4 ", "which combines in-depth", (8, 8), "Table 3:"),
        ]:
            section = next(s for s in app.document.sections if s.title.startswith(title))
            paragraph = next(p for p in section.paragraphs if phrase in p)
            assert caption not in paragraph
            assert section.paragraph_pages[section.paragraphs.index(paragraph)] == pages
        # The existing genuine continuations must survive the caption correction.
        for title, pages in [("4.5 ", (9, 10)), ("Appendix — 7.2 ", (13, 14))]:
            section = next(s for s in app.document.sections if s.title.startswith(title))
            assert pages in section.paragraph_pages
    finally:
        await app.close()


@pytest.mark.parametrize(
    "text",
    [
        "區域甲 1.2\n區域乙 3.4\n區域丙 5.6",
        "區域甲 123.45\n區域乙 678.90\n區域丙 5.6",
        "觀察記錄" * 11 + "1\n" + "觀察記錄" * 11 + "2",
    ],
    ids=["labelled-measurements", "short-final-row", "equal-width-list-items"],
)
async def test_labelled_cjk_numeric_rows_keep_source_and_chunk_separators(text):
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    try:
        events = [e async for e in app.upload_document(paragraph_pdf(text, cjk=True), "rows.pdf")]
        assert events[-1].type == "ready"
        assert app.document.sections[0].paragraphs == [text]
        assert app.document.chunks[0].text == text
    finally:
        await app.close()


async def test_genuine_cjk_wrap_with_a_full_final_line_keeps_source_text_intact():
    # Two naturally wrapped prose lines; the final one is almost as long as the first.
    text = "觀察記錄" * 52 + "。"
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    try:
        events = [e async for e in app.upload_document(paragraph_pdf(text, cjk=True), "flow.pdf")]
        assert events[-1].type == "ready"
        assert app.document.sections[0].paragraphs == [text]
        assert app.document.chunks[0].text == text
    finally:
        await app.close()


@pytest.mark.parametrize(
    ("two_columns", "full_lines"),
    [(False, 4), (True, 4), (True, 5)],
    ids=["asymmetric-margins", "two-columns-96-characters", "two-columns-120-characters"],
)
async def test_cjk_full_final_lines_use_the_actual_column_or_text_width(two_columns, full_lines):
    content, texts = cjk_layout_pdf(two_columns=two_columns, full_lines=full_lines)
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    try:
        events = [e async for e in app.upload_document(content, "layout.pdf")]
        assert events[-1].type == "ready"
        section = app.document.sections[0]
        assert section.paragraphs == texts
        assert section.paragraph_pages == [(1, 1)] * len(texts)
        assert app.document.chunks[0].text == "\n\n".join(texts)
    finally:
        await app.close()




async def test_uploaded_oversized_paragraph_keeps_decimals_and_abbreviations():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=500)
    text = "Win rate 64.8% vs 60.0%, e.g. an ablation. " * 100
    result = [e async for e in app.upload_document(paragraph_pdf(text), "numbers.pdf")]
    assert result[-1].type == "ready"
    assert any(count_tokens(p) > 500 for s in app.document.sections for p in s.paragraphs)
    chunks = app.document.chunks
    assert len(chunks) > 1
    combined = "\n".join(c.text for c in chunks)
    assert "64.8" in combined and "60.0" in combined and "e.g." in combined
    assert "64.\n8" not in combined and "60.\n0" not in combined


async def test_uploaded_cjk_paragraph_splits_on_characters_with_overlap():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])), chunk_token_target=500)
    text = "".join(f"龜測試{i:04d}" for i in range(600))
    result = [e async for e in app.upload_document(paragraph_pdf(text, cjk=True), "cjk.pdf")]
    assert result[-1].type == "ready"
    chunks = app.document.chunks
    assert len(chunks) > 1
    assert all("\ufffd" not in c.text and count_tokens(c.text) <= 500 for c in chunks)
    for left, right in zip(chunks, chunks[1:], strict=False):
        shared = max(
            (
                size
                for size in range(1, min(len(left.text), len(right.text)) + 1)
                if left.text[-size:] == right.text[:size]
            ),
            default=0,
        )
        assert 40 <= count_tokens(left.text[-shared:]) <= 50
