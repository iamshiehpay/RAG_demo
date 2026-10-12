"""Resolve typography into Sections while retaining paragraph page provenance."""

import logging
import re
from collections import Counter
from dataclasses import dataclass

import pymupdf

from .chunker import chunk_sections
from .models import Section
from .policy import CHUNK_TOKEN_TARGET

logger = logging.getLogger(__name__)
_NUMBER = re.compile(r"(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?")
_NUMBERED_TITLE = re.compile(r"^(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?\s+\S")


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
    fonts: tuple[str, ...]
    shared_row: bool = False


def _ordered_blocks(page: pymupdf.Page) -> tuple[list[dict], bool]:
    blocks = page.get_text("dict", sort=False)["blocks"]
    midpoint = page.rect.width / 2
    # Require substantial prose on both sides: table cells alone do not define columns.
    prose = [
        b
        for b in blocks
        if page.rect.width * 0.22 < b["bbox"][2] - b["bbox"][0] < page.rect.width * 0.55
        and sum(len(s["text"]) for line in b.get("lines", []) for s in line["spans"]) > 60
    ]
    two_columns = any(b["bbox"][2] <= midpoint for b in prose) and any(
        b["bbox"][0] >= midpoint for b in prose
    )
    if not two_columns:
        return sorted(blocks, key=lambda b: (b["bbox"][3], b["bbox"][0])), False
    # MuPDF can group same-row text from both columns into one block.
    split_blocks = []
    for block in blocks:
        groups = [
            [line for line in block.get("lines", []) if line["bbox"][2] <= midpoint],
            [line for line in block.get("lines", []) if line["bbox"][0] >= midpoint],
        ]
        if all(groups) and sum(map(len, groups)) == len(block["lines"]):
            for group in groups:
                bbox = pymupdf.Rect(group[0]["bbox"])
                for line in group[1:]:
                    bbox |= pymupdf.Rect(line["bbox"])
                split_blocks.append({**block, "lines": group, "bbox": tuple(bbox)})
        else:
            split_blocks.append(block)
    blocks = split_blocks
    # Full-width blocks divide the page into reading bands; each band is column-major.
    spanning = sorted(
        [b for b in blocks if b["bbox"][0] < midpoint < b["bbox"][2]],
        key=lambda b: b["bbox"][1],
    )
    remaining = [b for b in blocks if b not in spanning]
    ordered = []
    for separator in [*spanning, None]:
        band = [b for b in remaining if separator is None or b["bbox"][1] < separator["bbox"][1]]
        ordered.extend(
            sorted(band, key=lambda b: (b["bbox"][0] >= midpoint, b["bbox"][1], b["bbox"][0]))
        )
        remaining = [b for b in remaining if b not in band]
        if separator is not None:
            ordered.append(separator)
    return ordered, True


def _figure_regions(page: pymupdf.Page, blocks: list[dict]) -> list[pymupdf.Rect]:
    captions = [
        line
        for b in blocks
        for line in b.get("lines", [])
        if re.match(r"Figure\s+\d", "".join(s["text"] for s in line["spans"]), re.I)
    ]
    table_captions = [
        pymupdf.Rect(line["bbox"])
        for b in blocks
        for line in b.get("lines", [])
        if re.match(r"Table\s+\d", "".join(s["text"] for s in line["spans"]), re.I)
    ]
    candidates = [d["rect"] for d in page.get_drawings()] + [
        pymupdf.Rect(b["bbox"]) for b in blocks if b.get("type") == 1
    ]
    regions = []
    for caption in captions:
        caption_rect = pymupdf.Rect(caption["bbox"])
        for region in candidates:
            if (
                region.width > page.rect.width * 0.2
                and region.height > 2 * caption_rect.height
                and (
                    0 <= caption_rect.y0 - region.y1 <= 3 * caption_rect.height
                    or region.contains(caption_rect)
                )
                and not any(region.contains(table) for table in table_captions)
            ):
                # Some figure backgrounds extend through the caption into the next paragraph.
                regions.append(
                    pymupdf.Rect(region.x0, region.y0, region.x1, min(region.y1, caption_rect.y0))
                )
    return regions


def _lines(pdf: pymupdf.Document) -> tuple[list[_Line], float]:
    lines = []
    sizes: Counter[int] = Counter()
    regions_by_page = {}
    for page_number, page in enumerate(pdf, 1):
        page_lines = []
        blocks, two_columns = _ordered_blocks(page)
        regions_by_page[page_number] = _figure_regions(page, blocks)
        for block_number, block in enumerate(blocks):
            for line in block.get("lines", []):
                if line["dir"] != (1.0, 0.0):
                    continue  # Rotated arXiv stamps are not Document prose.
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                text = "".join(s["text"] for s in line["spans"]).strip()
                bbox = tuple(line["bbox"])
                if all(char.isspace() or ord(char) < 32 for char in text):
                    continue  # Font-mapped control glyphs; retain mathematical/table symbols.
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
                        fonts=tuple(sorted({s["font"] for s in spans})),
                    )
                )
        for line in page_lines:
            line.shared_row = any(
                other is not line
                and abs(other.bbox[1] - line.bbox[1]) < line.size * 0.3
                and (
                    not two_columns
                    or (other.bbox[0] >= page.rect.width / 2)
                    == (line.bbox[0] >= page.rect.width / 2)
                )
                and not _NUMBER.fullmatch(other.text)
                for other in page_lines
            )
        lines.extend(page_lines)
    body_size = sizes.most_common(1)[0][0] if sizes else 0
    for page_number, regions in regions_by_page.items():
        page_lines = [line for line in lines if line.page == page_number]
        regions_by_page[page_number] = [
            region for region in regions if not _contains_prose(region, page_lines, body_size)
        ]
    return [
        line
        for line in lines
        if not (
            len(line.text.split()) < 15
            and not _heading(line, body_size, numbered=True)
            and not _NUMBER.fullmatch(line.text)
            and not re.search(r"[.!?。！？]$", line.text)
            and any(
                region.contains(pymupdf.Rect(line.bbox)) for region in regions_by_page[line.page]
            )
        )
    ], body_size


def _contains_prose(region: pymupdf.Rect, lines: list[_Line], body_size: float) -> bool:
    contained = [line for line in lines if region.contains(pymupdf.Rect(line.bbox))]
    if any(_heading(line, body_size, numbered=True) for line in contained):
        return True  # A page frame or text box containing a heading is not a figure.
    body_lines = [line for line in contained if abs(line.size - body_size) < 0.5]
    for block in {line.block for line in body_lines}:
        paragraph = [line for line in body_lines if line.block == block]
        if len(paragraph) >= 2 and (
            any(re.search(r"[.!?。！？]$", line.text) for line in paragraph)
            or sum(line.bbox[2] - line.bbox[0] > region.width * 0.55 for line in paragraph)
            > len(paragraph) / 2
        ):
            return True
    return False


def _heading(line: _Line, body_size: float, *, numbered: bool = False) -> bool:
    text = line.text
    # Whole heading lines, not an emphasized phrase inside prose or a caption.
    return (
        (
            line.size > body_size + 0.5
            or (line.bold and line.size >= body_size - 0.5 and not line.shared_row)
            or (
                (numbered or _NUMBERED_TITLE.match(text))
                and text.isupper()
                and line.size >= body_size - 0.5
            )
        )
        and len(text) <= 160
        and not line.shared_row
        and not re.match(r"(?:Table|Figure)\s+\d|[•●]|\(?[ivx]+\)", text, re.I)
        and (
            not re.search(r"[.!?。！？;；]$", text)
            or (text.endswith(".") and text.isupper() and (numbered or _NUMBERED_TITLE.match(text)))
        )
    )


def _section_title(lines: list[_Line], index: int, body_size: float) -> tuple[str, int]:
    line = lines[index]
    consumed = 1
    title = line.text
    # Number and title can be separate PDF lines, on the same baseline or stacked.
    if _NUMBER.fullmatch(line.text) and index + 1 < len(lines):
        following = lines[index + 1]
        if (
            following.page == line.page
            and _heading(following, body_size, numbered=True)
            and abs(following.bbox[1] - line.bbox[1]) <= line.size * 2
            and re.search(r"[^\W\d_]", following.text)
        ):
            title = f"{line.text} {following.text}"
            consumed = 2
            line = following
        else:
            return "", 1
    elif not _heading(line, body_size):
        return "", 1
    if not re.search(r"[^\W\d_]", title):
        return "", 1
    while index + consumed < len(lines):
        following = lines[index + consumed]
        if not (
            following.page == line.page
            and _heading(following, body_size, numbered=True)
            and not _NUMBERED_TITLE.match(following.text)
            and not _NUMBER.fullmatch(following.text)
            and abs(following.size - line.size) < 0.5
            and following.bold == line.bold
            and following.fonts == line.fonts
            and 0 < following.bbox[1] - line.bbox[1] <= 1.5 * (line.bbox[3] - line.bbox[1])
            and abs(following.bbox[0] - line.bbox[0]) <= line.size * 2
        ):
            break
        title += f" {following.text}"
        line = following
        consumed += 1
    return title, consumed


def _virtual_sections(section: Section, target: int) -> list[Section]:
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
        for i, chunk in enumerate(chunk_sections([section], "virtual", target=target), 1)
    ]


def _sections(lines: list[_Line], body_size: float, target: int) -> list[Section]:
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
        if current.paragraphs or current.title != "Front matter":
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
            elif (
                "appendix" in normalized
                or normalized.startswith(("附錄", "supplementary", "補充"))
                or (excluded and re.match(r"^[A-Z](?:\.\d+)*\.?\s", title))
            ):
                if not excluded:
                    flush_section()
                excluded = False
                appendix = detected = True
                current = Section(
                    id=f"section-{len(sections) + 1}",
                    title=title if "appendix" in normalized else f"Appendix — {title}",
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
    if not any(section.paragraphs for section in sections):
        raise DocumentError("This Document has no indexable text outside References.")
    if not detected:
        return _virtual_sections(sections[0], target)
    return sections


def parse_pdf(content: bytes, *, chunk_token_target: int = CHUNK_TOKEN_TARGET) -> list[Section]:
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            if not pdf.is_pdf or not pdf.page_count:
                raise DocumentError("Please upload a valid PDF Document; this PDF is damaged.")
            if pdf.needs_pass:
                raise DocumentError("Password-protected PDFs are not supported.")
            if pdf.is_repaired:
                logger.warning("MuPDF repaired the uploaded PDF; continuing with readable text.")
            lines, body_size = _lines(pdf)
            if not lines:
                if pdf.is_repaired:
                    raise DocumentError(
                        "Please upload a valid PDF Document; this damaged PDF has no readable text."
                    )
                raise DocumentError(
                    "This Document has no text layer; scanned PDFs are not supported."
                )
            return _sections(lines, body_size, chunk_token_target)
    except (pymupdf.FileDataError, pymupdf.EmptyFileError) as exc:
        raise DocumentError("Please upload a valid PDF Document.") from exc
