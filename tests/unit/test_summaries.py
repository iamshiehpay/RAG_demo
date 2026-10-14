"""Table selection validates ORIGINAL source identities before publishing text."""

import json

import pymupdf
import pytest

from chat_document.application import Application
from chat_document.llm_adapter import LLMFrame, ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens
from tests.support import DeterministicEmbedder, SummaryScriptedLLM, summary_response


def table_catalogue_pdf():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 40), "1 Assay catalogue", fontsize=14)
        caption = (
            "Assay observations were collected for independent sample batches. Preparation "
            "and calibration are described in the Methods section. An interrupted "
            "reading was excluded after detector power loss. The remaining readings "
            "retain their original order. These are observations for individual "
            "sample batches, not instrument rankings or a statement of population "
            "extrema. Independent calibration was not performed for the evening "
            "batch; this limitation applies only to that batch."
        )
        assert page.insert_textbox(pymupdf.Rect(50, 65, 535, 180), caption, fontsize=10) >= 0
        page.insert_text((50, 210), "Table 6: Recorded detector measurements.", fontsize=10)
        for y, cells in [
            (240, ["Batch", "Intensity", "Count"]),
            *[
                (260 + 17 * i, [f"Sample{i}", f"{0.71 + i / 100:.2f}", str(13 + i)])
                for i in range(18)
            ],
        ]:
            for x, cell in zip([50, 220, 370], cells, strict=True):
                page.insert_text((x, y), cell, fontsize=10)
        return pdf.tobytes()


@pytest.mark.parametrize(
    "malformed",
    [False, "commentary", "unknown", "duplicate", "ignored_format", "missing", "wrong_type"],
)
async def test_table_summary_selects_original_spans_or_fails_closed(malformed):
    class SelectionLLM(SummaryScriptedLLM):
        async def stream(self, request):
            if request.call_type == "section_summary":
                self.calls.append(request)
                if request.format and "span_ids" in str(request.format):
                    payload = json.loads(request.messages[-1]["content"])
                    ids = [
                        span["id"]
                        for span in payload["spans"]
                        if span["kind"] in {"caption", "prose"}
                    ]
                    rows = [span["id"] for span in payload["spans"] if span["kind"] == "row"]
                    selected = ids + rows[:2]
                    if malformed == "unknown":
                        selected.append("UNKNOWN")
                    elif malformed == "duplicate":
                        selected.append(selected[0])
                    text = (
                        "The output ignores the requested format and invents unvalidated claims."
                        if malformed == "ignored_format"
                        else json.dumps(
                            {"span_ids": selected, "note": "INVENTED_NOTE must never be published"}
                            if malformed == "commentary"
                            else {"span_ids": selected}
                        )
                    )
                    if malformed == "missing":
                        text = json.dumps({"note": "No IDs"})
                    elif malformed == "wrong_type":
                        text = json.dumps({"span_ids": "E1"})
                else:
                    text = (
                        "UNSUPPORTED_METHOD_CLAIM: The catalogue has no independent validation. "
                        "It omits all control experiments and statistical analysis. " * 8
                    )
                async for frame in ScriptedLLM([text]).stream(request):
                    yield frame
                return
            async for frame in super().stream(request):
                yield frame

    llm = SelectionLLM([])
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(table_catalogue_pdf(), "assays.pdf")]
    if malformed and malformed != "commentary":
        assert events[-1].type == "error" and app.document is None
        assert "selection" in events[-1].message.lower()
    else:
        assert events[-1].type == "ready"
        node = app.document.summary_tree.section_summaries[0]
        assert 80 <= count_tokens(node.text) <= 500
        assert "UNSUPPORTED_METHOD_CLAIM" not in node.text
        assert "Independent calibration was not performed" in node.text
        assert "Batch | Intensity | Count" in node.text
        assert "Sample0 | 0.71 | 13" in node.text
        assert "Sample1 | 0.72 | 14" in node.text
        assert "span_ids" not in node.text and "INVENTED_NOTE" not in node.text
        assert node.chunk_ids == [c.id for c in app.document.chunks]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)






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
            summary_response("Complete supported summary"),
            "Overview.",
        ]
    )
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(content, "retry.pdf")][-1].type == "ready"
    tree = app.document.summary_tree
    assert tree.section_summaries[0].text == summary_response("Complete supported summary")
    assert "FAILED_DRAFT" not in tree.document_summary.text
    assert [c.done_reason for c in tree.calls] == ["length", "stop", "stop"]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in tree.calls)


async def test_global_group_context_identifies_every_covered_section():
    from tests.support import summary_pdf

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


async def test_summary_length_correction_uses_original_source_not_the_failed_draft():
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_text(
            (50, 100), "SOURCE_TRUTH: the measurement is supported by evidence.", fontsize=10
        )
        content = pdf.tobytes()
    llm = ScriptedLLM(
        ["UNSUPPORTED_DRAFT claim. " * 100, summary_response("Supported measurement"), "Overview."]
    )
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(content, "measurements.pdf")][-1].type == "ready"
    corrective = llm.calls[1].messages[-1]["content"]
    assert "SOURCE_TRUTH" in corrective and "UNSUPPORTED_DRAFT" not in corrective




@pytest.mark.parametrize("succeeds", [True, False])
async def test_short_section_summary_regenerates_from_original_source_or_fails(succeeds):
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((50, 60), "1 Measurements", fontsize=14)
        page.insert_textbox(
            pymupdf.Rect(50, 100, 530, 650),
            "SOURCE measurements identify independent errors and conservative uncertainty. " * 30,
            fontsize=10,
        )
        content = pdf.tobytes()
    valid = (
        "The source records measurements of independent errors, with conservative uncertainty. "
        "The observations describe the measurement procedure and its scope, rather than "
        "establishing a universal result. Errors remain part of the reported evidence. "
        "The uncertainty applies to the measurements described here; the supplied text "
        "does not establish a different experiment, a stronger numerical result or a "
        "broader validation claim. The summary therefore retains the measured errors "
        "and the conservative qualification together within the stated scope."
    )
    assert 80 <= count_tokens(valid) <= 500
    short = "UNSUPPORTED_DRAFT substitutes another experiment."
    llm = ScriptedLLM([short, valid, "Overview"] if succeeds else [short] * 5)
    app = Application(DeterministicEmbedder(), LLMGateway(llm))
    events = [e async for e in app.upload_document(content, "short-summary.pdf")]
    if succeeds:
        assert events[-1].type == "ready"
        summary = app.document.summary_tree.section_summaries[0]
        assert summary.text == valid and 80 <= count_tokens(summary.text) <= 500
        assert len(llm.calls) == 3
        correction = llm.calls[1].messages
        assert "SOURCE" in correction[-1]["content"]
        assert "UNSUPPORTED_DRAFT" not in correction[-1]["content"]
    else:
        assert events[-1].type == "error" and app.document is None
        assert "length" in events[-1].message.lower()
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)
