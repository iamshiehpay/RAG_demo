"""Public regressions for independently reviewed source/summary defects."""

import pymupdf
import pytest

from chat_document.application import Application
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

from .fixtures import SummaryScriptedLLM
from .test_second_document import DeterministicEmbedder


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
