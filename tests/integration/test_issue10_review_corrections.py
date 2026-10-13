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
