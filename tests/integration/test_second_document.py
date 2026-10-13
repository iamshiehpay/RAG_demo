"""Generic layout regressions through upload; live evidence covers model behavior.

The deterministic Embedder and summary adapter replace external services here;
these tests prove source parsing/provenance, never generated-summary acceptance.
"""

import numpy as np
import pymupdf

from chat_document.application import Application
from chat_document.llm_gateway import LLMGateway

from .fixtures import SummaryScriptedLLM


class DeterministicEmbedder:
    async def embed(self, texts):
        return np.ones((len(texts), 2), dtype=np.float32)


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


async def test_numbered_document_keeps_front_matter_and_emphasis_out_of_summary_boundaries():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 40), "Measurements in Practice", fontsize=18)
        page.insert_text((50, 70), "Ada Example and Bea Example", fontsize=12)
        for n, y in enumerate([110, 260, 410], 1):
            page.insert_text((50, y), f"{n} Measurements", fontsize=14)
            page.insert_text((50, y + 30), "Emphasized observation", fontsize=10, fontname="hebo")
            page.insert_text(
                (50, y + 55), "EVIDENCE_ONLY documents the actual observed results.", fontsize=10
            )
        content = pdf.tobytes()
    app = Application(DeterministicEmbedder(), LLMGateway(SummaryScriptedLLM([])))
    assert [e async for e in app.upload_document(content, "structured-report.pdf")][
        -1
    ].type == "ready"
    assert len(app.document.summary_tree.section_summaries) == 3
    assert {s.section for s in app.document.summary_tree.section_summaries} == {
        "1 Measurements",
        "2 Measurements",
        "3 Measurements",
    }
    assert all("Emphasized observation" in c.text for c in app.document.chunks)
    assert not any("Ada Example" in c.text for c in app.document.chunks)


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
