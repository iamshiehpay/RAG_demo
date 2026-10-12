"""Walking skeleton parser: one virtual Section per PDF page (#02 replaces this)."""

import pymupdf

from .models import Section


class DocumentError(ValueError):
    pass


def parse_pdf(content: bytes) -> list[Section]:
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise DocumentError("Password-protected PDFs are not supported.")
            sections = []
            for page_number, page in enumerate(pdf, start=1):
                paragraphs = [
                    block[4].strip()
                    for block in page.get_text("blocks", sort=True)
                    if block[6] == 0 and block[4].strip()
                ]
                sections.append(
                    Section(
                        id=f"page-{page_number}",
                        title=f"Virtual Section {page_number}",
                        page_start=page_number,
                        page_end=page_number,
                        paragraphs=paragraphs,
                    )
                )
            if not any(section.paragraphs for section in sections):
                raise DocumentError(
                    "This Document has no text layer; scanned PDFs are not supported."
                )
            return sections
    except (pymupdf.FileDataError, pymupdf.EmptyFileError) as exc:
        raise DocumentError("Please upload a valid PDF Document.") from exc
