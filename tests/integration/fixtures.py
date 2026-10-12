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
        remaining = page.insert_textbox(
            pymupdf.Rect(72, 72, 1128, 13928),
            text,
            fontname="china-t" if cjk else "helv",
            fontsize=10,
        )
        assert remaining >= 0, "Fixture text must fit entirely on the page"
        return document.tobytes()
