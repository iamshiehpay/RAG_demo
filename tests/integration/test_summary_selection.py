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


async def test_upload_keeps_recursive_selection_batches_feasible_after_narrowing():
    """Replay the native selection decisions that reached the 74-token dead end.

    The replay uses fresh public PDF upload and original source validation, not
    direct builder calls. Recorded IDs are decisions, never generated evidence.
    Newly balanced pools use a source-only scripted selection at the same seam.
    """
    from collections import defaultdict, deque
    from pathlib import Path

    from eval.second_document import DOCUMENT

    from .fixtures import selection_response

    if not DOCUMENT.exists():
        pytest.skip("Fetch the pinned second Document before this source regression")
    decisions = defaultdict(deque)
    evidence = Path("eval/reports/issue10-d06-recovery-n3.responses.jsonl")
    for line in evidence.read_text().splitlines():
        recorded = json.loads(line)
        label = recorded["source_label"][-1]
        if not label.startswith("{"):
            continue
        payload = json.loads(label)
        if payload.get("section") == "Appendix C Industrial Implications":
            key = tuple(s["id"] for s in payload["spans"])
            try:
                choice = json.loads(recorded["response"])
            except ValueError:
                continue
            if isinstance(choice, dict) and set(choice) == {"span_ids"}:
                decisions[key].append(recorded["response"])

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
