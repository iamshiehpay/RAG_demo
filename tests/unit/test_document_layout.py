"""Generic layout regressions through upload; live evidence covers model behavior.

The deterministic Embedder and summary adapter replace external services here;
these tests prove source parsing/provenance, never generated-summary acceptance.
"""

import pymupdf
import pytest

from app.application import Application
from app.llm_gateway import LLMGateway
from tests.support import DeterministicEmbedder, SummaryScriptedLLM


def appendix_layout_pdf():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14, fontname="hebo")
        page.insert_text(
            (50, 95), "The report discusses the measurements and evidence.", fontsize=10
        )
        page.insert_text((50, 125), "See details in the Appendix,", fontsize=10, fontname="hebo")
        page.insert_text((50, 155), "2 Discussion", fontsize=14, fontname="hebo")
        page.insert_text(
            (50, 185), "BODY_RESULT has genuine evidence and a conclusion.", fontsize=10
        )
        page.insert_text((50, 240), "References", fontsize=14, fontname="hebo")
        page.insert_text((50, 270), "BIBLIOGRAPHY_ONLY do not index this entry.", fontsize=10)
        page = pdf.new_page()
        # One heading emitted as separate text objects on a shared baseline.
        page.insert_text((50, 60), "Appendix A", fontsize=14, fontname="hebo")
        page.insert_text((150, 60), "Additional", fontsize=14, fontname="hebo")
        page.insert_text((150, 77), "Measurements", fontsize=14, fontname="hebo")
        page.insert_text(
            (50, 115), "APPENDIX_RESULT records supplementary measurements.", fontsize=10
        )
        return pdf.tobytes()


async def test_upload_resumes_split_appendix_heading_after_references():
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    events = [e async for e in app.upload_document(appendix_layout_pdf(), "measurements.pdf")]
    assert events[-1].type == "ready"
    document = app.document
    appendix = [s for s in document.sections if s.is_appendix]
    assert [s.title for s in appendix] == ["Appendix A Additional Measurements"]
    assert all(not s.is_appendix for s in document.sections if s.page_start == 1)
    assert "APPENDIX_RESULT" in "\n".join(c.text for c in document.chunks)
    assert "BIBLIOGRAPHY_ONLY" not in "\n".join(c.text for c in document.chunks)
    summary = document.summary_tree.section_summaries[-1]
    assert summary.section_ids == [appendix[0].id]
    assert summary.page_start == summary.page_end == 2
    assert all(app.source(id).section_id == appendix[0].id for id in summary.chunk_ids)


async def test_upload_keeps_indented_wrapped_heading_as_one_section():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1.2 Evaluation of Deployment:", fontsize=12, fontname="hebo")
        page.insert_text((80, 74), "A Criteria Catalogue", fontsize=12, fontname="hebo")
        page.insert_text((50, 110), "RESULT_ONLY supplies the actual evidence.", fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "wrapped.pdf")][-1].type == "ready"
    assert [s.title for s in app.document.sections] == [
        "1.2 Evaluation of Deployment: A Criteria Catalogue"
    ]
    assert len(app.document.summary_tree.section_summaries) == 1


async def test_numeric_cell_before_next_table_row_cannot_open_a_section():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_text((50, 95), "Table 7: Evaluated criteria.", fontsize=10)
        for y, cells in zip(
            [125, 141, 157, 173],
            [
                ["Criterion", "Success", "Count"],
                ["I1", "3", "8"],
                ["I2", "1", "1"],
                ["I3", "2", "3"],
            ],
            strict=True,
        ):
            for x, text in zip([50, 150, 220], cells, strict=True):
                page.insert_text((x, y), text, fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "criteria.pdf")][-1].type == "ready"
    assert [s.title for s in app.document.sections] == ["1 Measurements"]
    table = next(c for c in app.document.chunks if c.table_label == "Table 7")
    assert table.table_rows == [["I1", "3", "8"], ["I2", "1", "1"], ["I3", "2", "3"]]


async def test_letter_prefixed_appendix_table_is_typed_and_keeps_uncertain_numeric_rows():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "Appendix B Measurements", fontsize=14)
        page.insert_text((50, 95), "Table B2: Measured outcomes.", fontsize=10)
        for y, cells in zip(
            [125, 141, 157],
            [
                ["Setting", "Accuracy", "Cost"],
                ["alpha", "0.812", "17"],
                ["beta", "", "23"],
            ],
            strict=True,
        ):
            for x, text in zip([50, 180, 260], cells, strict=True):
                if text:
                    page.insert_text((x, y), text, fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "supplement.pdf")][-1].type == "ready"
    tables = [c for c in app.document.chunks if c.table_label == "Table B2"]
    assert tables and all(c.kind == "table" and not c.table_reconstructed for c in tables)
    assert "結構未能可靠重建" in tables[0].text
    assert all(value in tables[0].text for value in ["alpha", "0.812", "17", "beta", "23"])
    assert all(c.section == "Appendix B Measurements" for c in tables)


async def test_repeated_header_on_next_page_keeps_table_provenance_and_raw_rows():
    with pymupdf.open() as pdf:
        for n in range(2):
            page = pdf.new_page()
            if n == 0:
                page.insert_text((50, 50), "Appendix A Measurements", fontsize=14)
                page.insert_text((50, 85), "Table A1: Extended measurements.", fontsize=10)
            top = 115 if n == 0 else 50
            for y, cells in [
                (top, ["Setting", "Accuracy ↓" if n == 0 else "Accuracy", "Cost"]),
                (top + 18, ["alpha" if n == 0 else "beta", "0.812", str(17 + n)]),
            ]:
                for x, text in zip([50, 180, 320], cells, strict=True):
                    page.insert_text(
                        (x, y),
                        text,
                        fontsize=10,
                        fontname="china-t" if text.startswith("Accuracy") else "helv",
                    )
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "extended.pdf")][-1].type == "ready"
    beta = [c for c in app.document.chunks if "beta" in c.text]
    assert beta and all(c.kind == "table" and c.table_label == "Table A1" for c in beta)
    assert all(c.page_start == c.page_end == 2 for c in beta)
    assert all("Accuracy" in c.text and "Cost" in c.text for c in beta)


async def test_continued_column_table_does_not_absorb_neighboring_body_prose():
    with pymupdf.open() as pdf:
        for n in range(2):
            page = pdf.new_page(width=600, height=800)
            if not n:
                page.insert_text((40, 50), "1 Results", fontsize=14)
                page.insert_text((40, 85), "Table 4: Results.", fontsize=10)
                page.insert_textbox(
                    pymupdf.Rect(330, 125, 560, 260),
                    "RIGHT_BODY contains a separate paragraph about the experiment. " * 3,
                    fontsize=10,
                )
            for y, cells in [
                (115 if not n else 50, ["Setting", "Accuracy"]),
                (135 if not n else 70, ["alpha" if not n else "beta", "0.812"]),
            ]:
                for x, text in zip([40, 200], cells, strict=True):
                    page.insert_text((x, y), text, fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "columns.pdf")][-1].type == "ready"
    body = [c for c in app.document.chunks if "RIGHT_BODY" in c.text]
    assert body and all(c.kind == "text" for c in body)
    assert any(c.kind == "table" and "beta" in c.text for c in app.document.chunks)


@pytest.mark.parametrize("fragmented_edges", [False, True])
async def test_captioned_single_cell_box_keeps_raw_text_and_excludes_outside_prose(
    fragmented_edges,
):
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "Appendix A Queries", fontsize=14)
        page.insert_text((50, 100), "Table A2: Recorded query strings.", fontsize=10)
        for first, last in [
            ((50, 115), (500, 115)),
            ((50, 200), (500, 200)),
            ((50, 115), (50, 200)),
            ((500, 115), (500, 200)),
        ]:
            if fragmented_edges:
                for i in range(10):
                    a = tuple(first[k] + (last[k] - first[k]) * i / 10 for k in range(2))
                    b = tuple(first[k] + (last[k] - first[k]) * (i + 1) / 10 for k in range(2))
                    page.draw_line(a, b)
            else:
                page.draw_line(first, last)
        page.insert_text((60, 140), "SELECT measure WHERE count > 17", fontname="cour", fontsize=8)
        page.insert_text((50, 240), "OUTSIDE_BODY explains the methodology.", fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "query.pdf")][-1].type == "ready"
    table = next((c for c in app.document.chunks if c.table_label == "Table A2"), None)
    assert table is not None and not table.table_reconstructed
    assert "SELECT measure WHERE count > 17" in table.text
    assert "結構未能可靠重建" in table.text and "OUTSIDE_BODY" not in table.text
    assert any(c.kind == "text" and "OUTSIDE_BODY" in c.text for c in app.document.chunks)


@pytest.mark.parametrize("missing_cell", [False, True])
async def test_reference_table_keeps_wrapped_model_version_out_of_numeric_scores(missing_cell):
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_text((50, 100), "Table 7: Model measurements.", fontsize=10)
        for x, text in zip([50, 130, 240, 320], ["Ref", "Model", "Score", "Cost"], strict=True):
            page.insert_text((x, 130), text, fontsize=10)
        page.insert_text((130, 158), "Alpha", fontsize=10)
        page.insert_text((130, 182), "1.7", fontsize=10)
        for x, text in [(50, "[11]"), (240, "0.25"), (320, "17")]:
            page.insert_text((x, 170), text, fontsize=10)
        for x, text in [(50, "[12]"), (130, "Beta"), (240, "0.32"), (320, "19")]:
            if not (missing_cell and x == 320):
                page.insert_text((x, 215), text, fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "models.pdf")][-1].type == "ready"
    table = next(c for c in app.document.chunks if c.table_label == "Table 7")
    if missing_cell:
        assert not table.table_reconstructed and "結構未能可靠重建" in table.text
        assert all(v in table.text for v in ["Alpha", "1.7", "0.25", "Beta", "0.32"])
    else:
        assert table.table_reconstructed
        assert table.table_rows == [
            ["[11]", "Alpha 1.7", "0.25", "17"],
            ["[12]", "Beta", "0.32", "19"],
        ]


@pytest.mark.parametrize("inline", [False, True])
async def test_upload_preserves_substantive_abstract_without_author_metadata(inline):
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 40), "Measurements in Practice", fontsize=18)
        page.insert_text((50, 70), "Ada Example and Bea Example", fontsize=12)
        if inline:
            page.insert_text(
                (50, 100), "Abstract: UNIQUE_ABSTRACT records the main uncertainty.", fontsize=10
            )
        else:
            # Abstract headings need not be larger than the body or bold.
            page.insert_text((50, 100), "Abstract", fontsize=10)
            page.insert_text(
                (50, 125), "UNIQUE_ABSTRACT records the main uncertainty.", fontsize=10
            )
        for n, y in enumerate([180, 330, 480], 1):
            page.insert_text((50, y), f"{n} Measurements", fontsize=14)
            page.insert_text((50, y + 30), "BODY_EVIDENCE records observed results.", fontsize=10)
        content = pdf.tobytes()
    llm = SummaryScriptedLLM([])
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(content, "abstract-report.pdf")][
        -1
    ].type == "ready"
    abstract = next(s for s in app.document.sections if s.title == "Abstract")
    assert "UNIQUE_ABSTRACT" in "\n".join(abstract.paragraphs)
    assert not any("Ada Example" in c.text for c in app.document.chunks)
    summary = next(
        s for s in app.document.summary_tree.section_summaries if s.section == "Abstract"
    )
    assert summary.page_start == summary.page_end == 1
    assert summary.chunk_ids and summary.section_ids == [abstract.id]
    assert any(
        "UNIQUE_ABSTRACT" in request.messages[-1]["content"]
        for request in llm.calls
        if request.call_type == "section_summary"
    )


@pytest.mark.parametrize("footer_side", ["bottom", "top"])
@pytest.mark.parametrize("first_folio", [7, 28])
async def test_upload_and_global_answer_exclude_sequential_margin_folios(footer_side, first_folio):
    """A folio above the old 90% cutoff must not become a validation count."""
    with pymupdf.open() as pdf:
        for index in range(2):
            page = pdf.new_page(width=600, height=800)
            # Logical folios need not equal the physical PDF page number.
            page.insert_text(
                (295, 680 if footer_side == "bottom" else 32), str(index + first_folio), fontsize=10
            )
            if index == 0:
                page.insert_text((50, 80), "1 Evaluation", fontsize=14)
                page.insert_text((50, 540), "BODY_COUNT records", fontsize=10)
                page.insert_text((50, 557), "99", fontsize=10)
                page.insert_text((50, 630), "The pipeline was checked against", fontsize=10)
            else:
                page.insert_text(
                    (50, 80), "expert judgements on three independent reports.", fontsize=10
                )
                page.insert_text((50, 160), "2 Measurements", fontsize=14)
                page.insert_text((50, 200), "Table 1: Recorded counts", fontsize=10)
                page.insert_text((50, 220), "Setting", fontsize=10)
                page.insert_text((230, 220), "Count", fontsize=10)
                page.insert_text((50, 240), "Control", fontsize=10)
                page.insert_text((230, 240), "23", fontsize=10)
                # A legitimate isolated integer near the lower margin is not a
                # sequential recurring folio and must remain original evidence.
                page.insert_text((50, 640), "LEGITIMATE_COUNT", fontsize=10)
                page.insert_text((50, 658), "41", fontsize=10)
        content = pdf.tobytes()
    llm = SummaryScriptedLLM(
        [
            '{"question_type":"Global","standalone_question":"Summarize evaluation.",'
            '"sub_queries":[]}',
            "The pipeline was checked against expert judgements on three independent reports [S1].",
        ]
    )
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    try:
        assert [e async for e in app.upload_document(content, "margin-folios.pdf")][
            -1
        ].type == "ready"
        source = "\n".join(c.text for c in app.document.chunks)
        folios = {str(first_folio), str(first_folio + 1)}
        assert not any(line.strip() in folios for line in source.splitlines())
        assert all(value in source for value in ("BODY_COUNT", "99", "23", "41"))
        assert any(s.title.startswith("2 Measurements") for s in app.document.sections)
        assert "against" in source and "expert judgements" in source
        summary_requests = [c for c in llm.calls if c.call_type == "section_summary"]
        assert summary_requests and all(
            not any(line.strip() in folios for line in c.messages[-1]["content"].splitlines())
            for c in summary_requests
        )
        events = [e async for e in app.ask("Summarize evaluation.")]
        final = next(e for e in events if e.type == "final")
        assert "three independent reports" in final.answer and final.citations
        assert "28 expert judgments" not in final.answer
        for citation in final.citations:
            summary = app.source(citation.source_id)
            assert summary.chunk_ids
            assert all(app.source(chunk_id).id == chunk_id for chunk_id in summary.chunk_ids)
    finally:
        await app.close()


@pytest.mark.parametrize("title_y", [68, 80])
async def test_upload_preserves_isolated_top_margin_section_numbers(title_y):
    with pymupdf.open() as pdf:
        for number, title in [(1, "Evaluation"), (2, "Methods")]:
            page = pdf.new_page(width=600, height=800)
            page.insert_text((50, 32), str(number), fontsize=14)
            page.insert_text((50, title_y), title, fontsize=14)
            page.insert_text(
                (50, 120), "Observed measurements retain their original source scope.", fontsize=10
            )
            page.insert_text((295, 680), str(number + 27), fontsize=10)
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    try:
        events = [e async for e in app.upload_document(content, "isolated-headings.pdf")]
        assert events[-1].type == "ready"
        source = "\n".join(c.context for c in app.document.chunks)
        assert any(s.title.startswith("1 Evaluation") for s in app.document.sections)
        assert any(s.title.startswith("2 Methods") for s in app.document.sections)
        assert "1 Evaluation" in source and "2 Methods" in source
        assert not any(line.strip() in {"28", "29"} for line in source.splitlines())
        for summary in app.document.summary_tree.section_summaries:
            assert summary.chunk_ids and all(app.source(i).id == i for i in summary.chunk_ids)
    finally:
        await app.close()
