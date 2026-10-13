import pymupdf


def scanned_pdf():
    """A real image-only PDF, rather than an empty page."""
    with pymupdf.open() as document:
        page = document.new_page()
        pixmap = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 20, 20), False)
        pixmap.clear_with(240)
        page.insert_image(pymupdf.Rect(72, 72, 400, 500), pixmap=pixmap)
        return document.tobytes()


def text_pdf(text="hello Document"):
    with pymupdf.open() as document:
        page = document.new_page()
        if text:
            page.insert_text((72, 72), text)
        return document.tobytes()


def paragraph_pdf(text, *, cjk=False):
    """One tall text block keeps the oversized paragraph in a single virtual Section."""
    with pymupdf.open() as document:
        page = document.new_page(width=1200, height=14000)
        page.insert_text((72, 40), "Long paragraph", fontsize=12)
        remaining = page.insert_textbox(
            pymupdf.Rect(72, 72, 1128, 13928),
            text,
            fontname="china-t" if cjk else "helv",
            fontsize=10,
        )
        assert remaining >= 0, "Fixture text must fit entirely on the page"
        return document.tobytes()


def page_continuation_pdf(first, second, *, cjk=False):
    with pymupdf.open() as document:
        for number, text in enumerate([first, second]):
            page = document.new_page()
            if number == 0:
                page.insert_text((72, 60), "1 Results", fontsize=14)
            assert (
                page.insert_textbox(
                    pymupdf.Rect(72, 100 if number == 0 else 60, 540, 740),
                    text,
                    fontsize=10,
                    fontname="china-t" if cjk else "helv",
                )
                >= 0
            )
        return document.tobytes()


def page_top_interruption_pdf(top, *, cjk=False):
    """A caption/header and body continuation share typography and the left margin."""
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 40), "1 Results", fontsize=14)
        font = "china-t" if cjk else "helv"
        first = "觀察記錄" * 11 if cjk else "The body describes an unfinished comparison"
        page.insert_text((72, 60), first, fontname=font, fontsize=10)
        page = document.new_page()
        page.insert_text((72, 60), top, fontname=font, fontsize=10)
        second = "繼續的內容。" if cjk else "and continues with the actual body text."
        page.insert_text((72, 74), second, fontname=font, fontsize=10)
        return document.tobytes(), first, second


def cjk_layout_pdf(*, two_columns, full_lines=4):
    """Completed prose whose final PDF line fills the measured text area."""
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((50, 40), "1 Results", fontsize=14)
        if two_columns:
            texts = [
                (label * 20)[: 24 * full_lines - 1] + "。"
                for label in ["左欄觀察記錄", "右欄觀察記錄"]
            ]
            boxes = [pymupdf.Rect(50, 70, 296, 500), pymupdf.Rect(316, 70, 562, 500)]
        else:
            texts = ["觀察記錄" * 42 + "數據好。"]
            boxes = [pymupdf.Rect(50, 70, 480, 500)]
        for text, box in zip(texts, boxes, strict=True):
            assert page.insert_textbox(box, text, fontsize=10, fontname="china-t") >= 0
        return document.tobytes(), texts


def structured_pdf(body_size=10):
    """Separate/stacked Section numbers, relative-size and same-size bold headings."""
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 60), "1", fontsize=body_size * 1.2)
        page.insert_text((72, 78), "Introduction", fontsize=body_size * 1.2)
        page.insert_textbox(
            pymupdf.Rect(72, 110, 540, 180), "INTRO_ONLY " + "alpha " * 20, fontsize=body_size
        )
        page.insert_textbox(
            pymupdf.Rect(72, 190, 540, 260),
            "INTRO_SECOND " + "beta " * 20 + ".",
            fontsize=body_size,
        )
        page = document.new_page()
        page.insert_textbox(
            pymupdf.Rect(72, 60, 540, 130), "INTRO_CONTINUED " + "gamma " * 20, fontsize=body_size
        )
        page.insert_text((72, 160), "Methods", fontname="hebo", fontsize=body_size)
        page.insert_textbox(
            pymupdf.Rect(72, 190, 540, 260), "METHOD_ONLY " + "delta " * 20, fontsize=body_size
        )
        page.insert_text((72, 300), "References", fontsize=body_size * 1.2)
        page.insert_text((72, 330), "BIBLIOGRAPHY_ONLY do not index this.", fontsize=body_size)
        page.insert_text((72, 400), "Appendix A", fontsize=body_size * 1.2)
        page.insert_text((72, 430), "APPENDIX_ONLY retain this content.", fontsize=body_size)
        return document.tobytes()


def heading_free_pdf():
    with pymupdf.open() as document:
        for i in range(3):
            page = document.new_page()
            for j in range(8):
                page.insert_text(
                    (72, 72 + j * 70),
                    f"Document fact {i}-{j}: " + "ordinary body text " * 6,
                    fontsize=10,
                )
        return document.tobytes()


def review_pdf(case):
    """Small authored Documents expose layout regressions through real PDF extraction."""
    with pymupdf.open() as document:
        page = document.new_page(width=600, height=800)
        if case == "wrapped":
            page.insert_text((50, 60), "1. A Very Long Section Title That", fontsize=14)
            page.insert_text((50, 78), "Wraps Onto Two Lines", fontsize=14)
            page.insert_text(
                (50, 115), "WRAPPED_BODY is genuine paragraph evidence. " * 3, fontsize=10
            )
        elif case == "number":
            page.insert_text((50, 60), "1.", fontsize=14)
            page.insert_text((50, 78), "Introduction", fontsize=14)
            page.insert_text(
                (50, 115), "NUMBER_BODY is genuine paragraph evidence. " * 3, fontsize=10
            )
        elif case in {"lettered", "supplementary", "chinese"}:
            page.insert_text((50, 60), "1 Introduction", fontsize=14)
            page.insert_text((50, 100), "MAIN_BODY describes the theorem.", fontsize=10)
            page.insert_text((50, 180), "References", fontsize=14)
            page.insert_text(
                (50, 210), "BIBLIOGRAPHY_ONLY entry should not enter the Index.", fontsize=10
            )
            title = {
                "lettered": "A Proof of Theorem",
                "supplementary": "Supplementary Material",
                "chinese": "補充資料",
            }[case]
            page.insert_text(
                (50, 300), title, fontsize=14, fontname="china-t" if case == "chinese" else "helv"
            )
            page.insert_text((50, 340), "APPENDIX_BODY proves the theorem completely.", fontsize=10)
        elif case == "columns":
            # Deliberately row-interleaved content streams require geometric column ordering.
            page.insert_text((40, 60), "1 Introduction", fontsize=14)
            page.insert_text((330, 60), "3 Results", fontname="hebo", fontsize=10)
            page.insert_textbox(
                pymupdf.Rect(40, 95, 275, 175),
                "LEFT_INTRO " + "The introduction explains the question. " * 3,
                fontsize=10,
            )
            page.insert_textbox(
                pymupdf.Rect(330, 95, 565, 175),
                "RIGHT_RESULTS " + "The results explain the measurements. " * 3,
                fontsize=10,
            )
            page.insert_text((40, 210), "2 Methods", fontname="hebo", fontsize=10)
            page.insert_textbox(
                pymupdf.Rect(40, 245, 275, 310),
                "LEFT_METHOD " + "The methods explain the experiment. " * 3,
                fontsize=10,
            )
            page.insert_textbox(
                pymupdf.Rect(330, 245, 565, 310),
                "RIGHT_CONTINUED " + "The results continue on this column. " * 3,
                fontsize=10,
            )
        elif case == "subsection":
            page.insert_text((50, 60), "4 Evaluation", fontsize=14)
            page.insert_text(
                (50, 100), "EVALUATION_BODY describes the experimental setting.", fontsize=10
            )
            page.insert_text((50, 180), "4.3", fontsize=10)
            page.insert_text((80, 180), "ABLATION STUDY", fontsize=10)
            page.insert_text(
                (50, 220), "ABLATION_BODY contains Table 2 and the variant results.", fontsize=10
            )
        elif case == "figure":
            page.insert_text((50, 60), "1 Results", fontsize=14)
            page.insert_text((50, 100), "SHORT_REAL Yes.", fontsize=10)
            page.draw_rect(pymupdf.Rect(50, 130, 450, 250))
            page.insert_text((80, 180), "FIGURE_LABEL Query + LLM", fontsize=8)
            page.insert_text((50, 270), "Figure 1: Pipeline overview.", fontsize=10)
            page.draw_rect(pymupdf.Rect(50, 330, 450, 400))
            page.insert_text((70, 360), "Variant", fontsize=10)
            page.insert_text((230, 360), "64.8", fontsize=10)
            page.insert_text((50, 420), "Table 2: Variant results.", fontsize=10)
            page.insert_text(
                (50, 460), "TABLE_PARAGRAPH compares the variants in Table 2.", fontsize=10
            )
        elif case == "period-headings":
            page.insert_text((50, 60), "7 Appendix", fontsize=14)
            page.insert_text(
                (50, 100), "APPENDIX_MAIN describes the supplementary evidence.", fontsize=10
            )
            page.insert_text(
                (50, 180), "7.2 CASE EXAMPLE OF LIGHTRAG.", fontsize=10, fontname="hebo"
            )
            page.insert_text(
                (50, 220),
                "CASE_EXAMPLE_BODY keeps the example under the right Section.",
                fontsize=10,
            )
            page.insert_text((50, 300), "7.4", fontsize=10)
            page.insert_text((80, 300), "CASE STUDY OF NAIVERAG.", fontsize=10, fontname="tiro")
            page.insert_text(
                (50, 340), "CASE_STUDY_BODY keeps the study under the right Section.", fontsize=10
            )
        elif case == "references-only":
            page.insert_text((50, 60), "References", fontsize=14)
            page.insert_text((50, 100), "Only a bibliography entry exists here.", fontsize=10)
        else:
            raise AssertionError(case)
        return document.tobytes()


def shaded_prose_pdf():
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((50, 60), "1 Introduction", fontsize=14)
        page.draw_rect(pymupdf.Rect(50, 130, 500, 270), fill=(0.95, 0.95, 0.95))
        page.insert_text(
            (60, 155),
            "PROSE_ONE The system keeps every line of evidence\n"
            "PROSE_TWO when a paragraph wraps inside a shaded box\n"
            "PROSE_THREE even if the line does not end in punctuation\n"
            "PROSE_FOUR because the sentence continues on the next line\n"
            "PROSE_FIVE and every part belongs to this Section\n"
            "PROSE_SIX until the final sentence ends here.",
            fontsize=10,
        )
        page.insert_text((50, 290), "Figure 1: A separate diagram caption.", fontsize=10)
        return document.tobytes()


def page_frame_pdf(title="1 Introduction"):
    with pymupdf.open() as document:
        page = document.new_page()
        page.draw_rect(pymupdf.Rect(25, 25, 570, 790))
        page.insert_text((50, 60), title, fontsize=14)
        page.insert_text(
            (50, 130), "FRAME_BODY is real evidence inside the decorative page border.", fontsize=10
        )
        page.insert_text((50, 270), "Figure 1: A caption inside the same page frame.", fontsize=10)
        return document.tobytes()


def styled_figure_labels_pdf():
    with pymupdf.open() as document:
        page = document.new_page(width=600, height=800)
        page.insert_text((50, 60), "1 Introduction", fontsize=14)
        assert (
            page.insert_textbox(
                pymupdf.Rect(50, 90, 550, 150),
                "REAL_BEFORE The introduction describes how the system works and why every "
                "paragraph must remain assigned to its original Section.",
                fontsize=10,
            )
            >= 0
        )
        page.draw_rect(pymupdf.Rect(50, 180, 500, 320))
        page.insert_text((70, 220), "LLM", fontsize=10, fontname="hebo")
        page.insert_text((70, 245), "LLM AGENT", fontsize=10)
        page.insert_text((70, 275), "Dual-level Retrieval", fontsize=12)
        page.insert_text((50, 340), "Figure 1: System overview.", fontsize=10)
        assert (
            page.insert_textbox(
                pymupdf.Rect(50, 380, 550, 460),
                "REAL_CONTINUED The introduction continues after the diagram and still belongs "
                "to the same Section. Every statement has an identifiable original location.",
                fontsize=10,
            )
            >= 0
        )
        return document.tobytes()


def numbered_sentences_pdf(*, split=False):
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((50, 60), "1 Introduction", fontsize=14)
        page.insert_text(
            (50, 100), "BODY_BEFORE describes the experiment and its expected costs.", fontsize=10
        )
        if split:
            page.insert_text((50, 170), "2", fontsize=10)
            page.insert_text((65, 170), "GPU HOURS.", fontsize=10)
        else:
            page.insert_text((50, 170), "2 GPU HOURS.", fontsize=10)
        page.insert_text(
            (50, 210),
            "BODY_AFTER_COST continues the Introduction without a new heading.",
            fontsize=10,
        )
        page.insert_text((50, 280), "3. THE SOFTWARE IS PROVIDED AS IS.", fontsize=10)
        page.insert_text(
            (50, 320), "BODY_AFTER_LICENSE also belongs to the Introduction Section.", fontsize=10
        )
        return document.tobytes()
