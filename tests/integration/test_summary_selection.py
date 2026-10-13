"""Table selection validates ORIGINAL source identities before publishing text."""

import json

import pymupdf
import pytest

from chat_document.application import Application
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

from .fixtures import SummaryScriptedLLM
from .test_second_document import DeterministicEmbedder


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


@pytest.mark.parametrize("malformed", [False, "unknown", "duplicate", "ignored_format"])
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
                        else json.dumps({"span_ids": selected})
                    )
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
    if malformed:
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
        assert "span_ids" not in node.text
        assert node.chunk_ids == [c.id for c in app.document.chunks]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in llm.calls)
