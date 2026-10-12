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
            pymupdf.Rect(72, 190, 540, 260), "INTRO_SECOND " + "beta " * 20, fontsize=body_size
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
