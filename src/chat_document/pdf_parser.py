"""Resolve typography into Sections while retaining paragraph page provenance."""

import re
from collections import Counter
from dataclasses import dataclass

import pymupdf

from .chunker import chunk_sections
from .models import Section


class DocumentError(ValueError):
    pass


@dataclass
class _Line:
    text: str
    page: int
    block: int
    bbox: tuple[float, float, float, float]
    size: float
    bold: bool
    shared_row: bool = False


def _lines(pdf: pymupdf.Document) -> tuple[list[_Line], float]:
    lines = []
    sizes: Counter[int] = Counter()
    for page_number, page in enumerate(pdf, 1):
        page_lines = []
        for block_number, block in enumerate(page.get_text("dict", sort=True)["blocks"]):
            for line in block.get("lines", []):
                if line["dir"] != (1.0, 0.0):
                    continue  # Rotated arXiv stamps are not Document prose.
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                text = "".join(s["text"] for s in line["spans"]).strip()
                bbox = tuple(line["bbox"])
                if text.isdigit() and bbox[1] > page.rect.height * 0.9:
                    continue  # Page numbers are not paragraphs or Section numbers.
                for span in spans:
                    sizes[round(span["size"])] += len(span["text"].strip())
                page_lines.append(
                    _Line(
                        text=text,
                        page=page_number,
                        block=block_number,
                        bbox=bbox,
                        size=max(s["size"] for s in spans),
                        bold=all(s["flags"] & 16 for s in spans),
                    )
                )
        for line in page_lines:
            line.shared_row = any(
                other is not line
                and abs(other.bbox[1] - line.bbox[1]) < line.size * 0.3
                and not re.fullmatch(r"\d+(?:\.\d+)*\.?", other.text)
                for other in page_lines
            )
        lines.extend(page_lines)
    return lines, sizes.most_common(1)[0][0] if sizes else 0


def _heading(line: _Line, body_size: float) -> bool:
    text = line.text
    # Whole heading lines, not an emphasized phrase inside prose or a caption.
    return (
        (
            line.size > body_size + 0.5
            or (line.bold and line.size >= body_size - 0.5 and not line.shared_row)
        )
        and len(text) <= 160
        and not re.match(r"(?:Table|Figure)\s+\d|[•●]|\(?[ivx]+\)", text, re.I)
        and not re.search(r"[.!?。！？;；]$", text)
    )


def _section_title(lines: list[_Line], index: int, body_size: float) -> tuple[str, int]:
    line = lines[index]
    if not _heading(line, body_size):
        return "", 1
    # Number and title can be separate PDF lines, on the same baseline or stacked.
    if re.fullmatch(r"(?:\d+(?:\.\d+)*|[A-Z])\.?", line.text) and index + 1 < len(lines):
        following = lines[index + 1]
        if (
            following.page == line.page
            and _heading(following, body_size)
            and abs(following.bbox[1] - line.bbox[1]) <= line.size * 2
            and re.search(r"[^\W\d_]", following.text)
        ):
            return f"{line.text} {following.text}", 2
        return "", 1
    if not re.search(r"[^\W\d_]", line.text):
        return "", 1
    return line.text, 1


def _virtual_sections(section: Section) -> list[Section]:
    # Fixed-length virtual Sections use the same Unicode/sentence-safe bounds as Chunks.
    return [
        Section(
            id=f"virtual-{i}",
            title=f"Virtual Section {i}",
            page_start=chunk.page_start,
            page_end=chunk.page_end,
            paragraphs=[chunk.text],
            paragraph_pages=[(chunk.page_start, chunk.page_end)],
            is_virtual=True,
        )
        for i, chunk in enumerate(chunk_sections([section], "virtual"), 1)
    ]


def _sections(lines: list[_Line], body_size: float) -> list[Section]:
    sections: list[Section] = []
    current = Section(
        id="section-1",
        title="Front matter",
        page_start=lines[0].page,
        page_end=lines[0].page,
        paragraphs=[],
        paragraph_pages=[],
    )
    pending: list[str] = []
    pending_start = pending_end = lines[0].page
    previous: _Line | None = None
    excluded = appendix = detected = False

    def flush_paragraph():
        if pending:
            current.paragraphs.append("\n".join(pending))
            current.paragraph_pages.append((pending_start, pending_end))
            current.page_end = pending_end
            pending.clear()

    def flush_section():
        flush_paragraph()
        if current.paragraphs:
            sections.append(current)

    index = 0
    while index < len(lines):
        line = lines[index]
        title, consumed = _section_title(lines, index, body_size)
        if title:
            normalized = re.sub(r"^[\d.]+\s+", "", title).strip().casefold()
            if normalized in {"references", "bibliography", "參考文獻"}:
                flush_section()
                excluded = True
            elif "appendix" in normalized or normalized.startswith("附錄"):
                if not excluded:
                    flush_section()
                excluded = False
                appendix = detected = True
                current = Section(
                    id=f"section-{len(sections) + 1}",
                    title=title,
                    page_start=line.page,
                    page_end=line.page,
                    paragraphs=[],
                    paragraph_pages=[],
                    is_appendix=True,
                )
            elif not excluded:
                detected = True
                flush_section()
                current = Section(
                    id=f"section-{len(sections) + 1}",
                    title=f"Appendix — {title}" if appendix else title,
                    page_start=line.page,
                    page_end=line.page,
                    paragraphs=[],
                    paragraph_pages=[],
                    is_appendix=appendix,
                )
            previous = None
            index += consumed
            continue
        if not excluded:
            if previous and (line.page != previous.page or line.block != previous.block):
                flush_paragraph()
            if not pending:
                pending_start = line.page
            pending_end = line.page
            pending.append(line.text)
            previous = line
        index += 1
    if not excluded:
        flush_section()
    if not sections:
        raise DocumentError("This Document has no indexable text outside References.")
    if not detected:
        return _virtual_sections(sections[0])
    return sections


def parse_pdf(content: bytes) -> list[Section]:
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            if not pdf.is_pdf or pdf.is_repaired:
                raise DocumentError("Please upload a valid PDF Document; this PDF is damaged.")
            if pdf.needs_pass:
                raise DocumentError("Password-protected PDFs are not supported.")
            lines, body_size = _lines(pdf)
            if not lines:
                raise DocumentError(
                    "This Document has no text layer; scanned PDFs are not supported."
                )
            return _sections(lines, body_size)
    except (pymupdf.FileDataError, pymupdf.EmptyFileError) as exc:
        raise DocumentError("Please upload a valid PDF Document.") from exc
