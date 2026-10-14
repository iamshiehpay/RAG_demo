"""Public PDF → Section entry point; compose layout, structure and table parsing."""

import logging

import pymupdf

from .models import Section
from .pdf_layout import read_layout, table_boxes
from .pdf_sections import DocumentError as DocumentError
from .pdf_sections import build_sections, filter_figure_labels, section_titles
from .policy import CHUNK_TOKEN_TARGET
from .table_layout import reconstruct_tables

logger = logging.getLogger(__name__)


def parse_pdf(content: bytes, *, chunk_token_target: int = CHUNK_TOKEN_TARGET) -> list[Section]:
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            if not pdf.is_pdf or not pdf.page_count:
                raise DocumentError("Please upload a valid PDF Document; this PDF is damaged.")
            if pdf.needs_pass:
                raise DocumentError("Password-protected PDFs are not supported.")
            if pdf.is_repaired:
                logger.warning("MuPDF repaired the uploaded PDF; continuing with readable text.")
            lines, body_size, regions = read_layout(pdf)
            lines, body_size = filter_figure_labels(lines, body_size, regions)
            if not lines:
                if pdf.is_repaired:
                    raise DocumentError(
                        "Please upload a valid PDF Document; this damaged PDF has no readable text."
                    )
                raise DocumentError(
                    "This Document has no text layer; scanned PDFs are not supported."
                )
            # Table detection precedes Section construction. Share the exact same
            # heading decisions, including split/wrapped titles, without importing
            # the parser from the table module or duplicating typography rules.
            titles = section_titles(lines, body_size)
            heading_lines = {
                i for start, (_, consumed) in titles.items() for i in range(start, start + consumed)
            }
            return build_sections(
                lines,
                body_size,
                chunk_token_target,
                reconstruct_tables(
                    lines,
                    page_widths={i: page.rect.width for i, page in enumerate(pdf, 1)},
                    heading_lines=heading_lines,
                    boxes_by_page={i: table_boxes(page) for i, page in enumerate(pdf, 1)},
                ),
                titles,
            )
    except (pymupdf.FileDataError, pymupdf.EmptyFileError) as exc:
        raise DocumentError("Please upload a valid PDF Document.") from exc
