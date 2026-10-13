"""Generic layout regressions through upload; live evidence covers model behavior.

The deterministic Embedder and summary adapter replace external services here;
these tests prove source parsing/provenance, never generated-summary acceptance.
"""

import json

import numpy as np
import pymupdf
import pytest

from chat_document.application import Application
from chat_document.llm_adapter import LLMFrame, ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

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


@pytest.mark.parametrize("correction_succeeds", [True, False])
async def test_overlong_section_summary_is_regenerated_or_upload_fails(correction_succeeds):
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_text(
            (50, 100), "The measured finding is supported by source evidence.", fontsize=10
        )
        content = pdf.tobytes()
    overlong = "The measured finding is supported. " * 100
    assert 500 < count_tokens(overlong) < 1200
    corrected = "The measured finding is supported by source evidence. " * 10
    llm = ScriptedLLM([overlong, corrected, "Overview."] if correction_succeeds else [overlong] * 5)
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(content, "measured.pdf")]
    if correction_succeeds:
        assert events[-1].type == "ready"
        summary = app.document.summary_tree.section_summaries[0]
        assert summary.text.strip() == corrected.strip()
        assert summary.chunk_ids and count_tokens(summary.text) <= 500
        assert len(llm.calls) == 3
        assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)
    else:
        assert events[-1].type == "error" and app.document is None
        assert "length" in events[-1].message.lower()


async def test_truncated_summary_is_discarded_before_retry_and_every_call_is_recorded():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_text((50, 100), "Source measurement has complete evidence.", fontsize=10)
        content = pdf.tobytes()
    llm = ScriptedLLM(
        [
            [
                LLMFrame(content="FAILED_DRAFT must not be published."),
                LLMFrame(done=True, done_reason="length"),
            ],
            "Complete supported summary.",
            "Overview.",
        ]
    )
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(content, "retry.pdf")][-1].type == "ready"
    tree = app.document.summary_tree
    assert tree.section_summaries[0].text == "Complete supported summary."
    assert "FAILED_DRAFT" not in tree.document_summary.text
    assert [c.done_reason for c in tree.calls] == ["length", "stop", "stop"]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in tree.calls)


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


async def test_global_group_context_identifies_every_covered_section():
    from .test_summary_tree import summary_pdf

    class GroupedLLM(ScriptedLLM):
        async def stream(self, request):
            self.scripts.append(
                {
                    "section_summary": "Measurements are supported. " * 100,
                    "group_summary": "Grouped supported findings.",
                    "document_summary": "Supported overview.",
                    "router": json.dumps(
                        {
                            "question_type": "Global",
                            "standalone_question": "Summarize",
                            "sub_queries": [],
                        }
                    ),
                    "answer": "Supported findings. [S1]",
                }[request.call_type]
            )
            async for frame in super().stream(request):
                yield frame

    llm = GroupedLLM([])
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(summary_pdf(18), "measurements.pdf")][
        -1
    ].type == "ready"
    events = [e async for e in app.ask("Summarize", history=[])]
    assert next(e for e in events if e.type == "trace").summary_level.startswith("group:")
    prompt = next(c for c in reversed(llm.calls) if c.call_type == "answer").messages[-1]["content"]
    assert "Covered Sections:" in prompt
    assert all(s.title in prompt for s in app.document.sections)


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


async def test_summary_length_correction_uses_original_source_not_the_failed_draft():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_text(
            (50, 100), "SOURCE_TRUTH: the measurement is supported by evidence.", fontsize=10
        )
        content = pdf.tobytes()
    llm = ScriptedLLM(["UNSUPPORTED_DRAFT claim. " * 100, "Supported measurement.", "Overview."])
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(content, "measurements.pdf")][-1].type == "ready"
    corrective = llm.calls[1].messages[-1]["content"]
    assert "SOURCE_TRUTH" in corrective and "UNSUPPORTED_DRAFT" not in corrective
