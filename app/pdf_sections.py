"""Resolve headings and flowing paragraphs into Sections with source provenance."""

import re

import pymupdf

from .chunker import chunk_sections
from .models import Section, Table
from .pdf_layout import (
    _CAPTION,
    _LINE_WRAP_WIDTH_RATIO,
    _NUMBER,
    _NUMERIC_LINE,
    _SENTENCE_END,
    TextLine,
    aligned_style,
)
from .table_layout import TableRegion
from .tables import LIMITATION

_NUMBERED_TITLE = re.compile(r"^(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?\s+\S")
_FIGURE_LABEL_WORD_LIMIT = 15
_PROSE_LINE_WIDTH_RATIO = 0.55
_CJK_CHARACTERS = r"\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af\U00020000-\U000323af"
_CJK_TEXT = re.compile(f"[{_CJK_CHARACTERS}]")
_CJK_LINE_WRAP = re.compile(rf"(?<=[{_CJK_CHARACTERS}\d])\n(?=[{_CJK_CHARACTERS}\d])")
_LABELLED_NUMERIC_ROW = re.compile(r"\S.*\s[\d\s.,%+\-−]+$")
_APPENDIX = re.compile(r"^(?:appendix\b|附錄|supplementary\b|補充)", re.I)
_ABSTRACT = re.compile(r"(?P<label>abstract|摘要)(?:\s*[:：]\s*(?P<body>.*))?", re.I)


class DocumentError(ValueError):
    """An invalid PDF or a Document without supported text content."""


def _is_figure_label(line: TextLine, regions: list[pymupdf.Rect]) -> bool:
    return (
        len(line.text.split()) < _FIGURE_LABEL_WORD_LIMIT
        and not _SENTENCE_END.search(line.text)
        and any(region.contains(pymupdf.Rect(line.bbox)) for region in regions)
    )


def _contains_prose(region: pymupdf.Rect, lines: list[TextLine], body_size: float) -> bool:
    contained = [line for line in lines if region.contains(pymupdf.Rect(line.bbox))]
    if any(
        region.contains(pymupdf.Rect(line.bbox))
        and _opens_numbered_section(lines, index, body_size)
        for index, line in enumerate(lines)
    ):
        return True
    body_lines = [line for line in contained if abs(line.size - body_size) < 0.5]
    for block in {line.block for line in body_lines}:
        paragraph = [line for line in body_lines if line.block == block]
        if len(paragraph) >= 2 and (
            any(_SENTENCE_END.search(line.text) for line in paragraph)
            or sum(
                line.bbox[2] - line.bbox[0] > region.width * _PROSE_LINE_WIDTH_RATIO
                for line in paragraph
            )
            > len(paragraph) / 2
        ):
            return True
    return False


def _opens_numbered_section(lines: list[TextLine], index: int, body_size: float) -> bool:
    text = lines[index].text
    if not (_NUMBERED_TITLE.match(text) or _NUMBER.fullmatch(text)):
        return False
    title, _ = _section_title(lines, index, body_size)
    return bool(_NUMBERED_TITLE.match(title))


def _heading(line: TextLine, body_size: float, *, numbered: bool = False) -> bool:
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
        and not re.match(r"(?:Table|Figure)\s+[A-Z]?\d|[•●]|\(?[ivx]+\)", text, re.I)
        and (
            not _SENTENCE_END.search(text)
            or (
                text.endswith(".")
                and text.isupper()
                and (numbered or _NUMBERED_TITLE.match(text))
                and (
                    line.bold or line.small_caps or line.font_change or line.size > body_size + 0.5
                )
            )
        )
    )


def _section_title(lines: list[TextLine], index: int, body_size: float) -> tuple[str, int]:
    line = lines[index]
    consumed = 1
    title = line.text
    # A labelled appendix opener may be split into same-baseline text objects.
    # Require larger heading typography and a nearby matching-style continuation;
    # ordinary shared table rows must still fail the normal heading check.
    if _APPENDIX.match(title) and line.size > body_size + 0.5:
        while index + consumed < len(lines):
            following = lines[index + consumed]
            if not (
                following.page == line.page
                and abs(following.bbox[1] - line.bbox[1]) < line.size * 0.5
                and 0 <= following.bbox[0] - line.bbox[2] <= line.size * 3
                and abs(following.size - line.size) < 0.5
                and following.bold == line.bold
                and following.fonts == line.fonts
            ):
                break
            title += f" {following.text}"
            line = following
            consumed += 1
    # Number and title can be separate PDF lines, on the same baseline or stacked.
    if consumed > 1:
        pass
    elif _NUMBER.fullmatch(line.text) and index + 1 < len(lines):
        following = lines[index + 1]
        if (
            following.page == line.page
            and _heading(following, body_size, numbered=True)
            and abs(following.bbox[1] - line.bbox[1])
            <= line.size
            * (4 if line.size > body_size + 0.5 and abs(following.size - line.size) < 0.5 else 2)
            and (
                (
                    abs(following.bbox[1] - line.bbox[1]) < line.size * 0.5
                    and 0 <= following.bbox[0] - line.bbox[2] <= line.size * 3
                )
                or (not line.shared_row and abs(following.bbox[0] - line.bbox[0]) <= line.size * 3)
            )
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
            and (
                not _NUMBERED_TITLE.match(following.text)
                or (title.endswith(":") and following.text.startswith(("A ", "An ", "The ")))
            )
            and not _NUMBER.fullmatch(following.text)
            and abs(following.size - line.size) < 0.5
            and following.bold == line.bold
            and following.fonts == line.fonts
            and 0 < following.bbox[1] - line.bbox[1] <= 1.5 * (line.bbox[3] - line.bbox[1])
            and abs(following.bbox[0] - line.bbox[0]) <= line.size * 3
        ):
            break
        title = (
            title[:-1] + following.text
            if title.endswith("-") and following.text[:1].islower()
            else f"{title} {following.text}"
        )
        line = following
        consumed += 1
    return title.removesuffix("."), consumed


def section_titles(lines: list[TextLine], body_size: float) -> dict[int, tuple[str, int]]:
    """Resolve a repeated numbered hierarchy before identifying table boundaries.

    In a document with a demonstrated larger-type numbered hierarchy, body-size
    emphasis is paragraph content. Preserve numbered subsections, explicit
    References/Appendix openers, and larger headings. Without that evidence the
    existing relative-size/bold fallback remains available to unnumbered layouts.
    """
    titles = {}
    index = 0
    while index < len(lines):
        title, consumed = _section_title(lines, index, body_size)
        abstract = _ABSTRACT.fullmatch(lines[index].text)
        if abstract and not abstract.group("body"):
            title, consumed = abstract.group("label"), 1
        if title:
            titles[index] = (title, consumed)
        index += consumed
    main_numbers = {
        match.group(1)
        for i, (title, _) in titles.items()
        if (match := re.match(r"^(\d+)(?:\.\d+)*\.?\s", title)) and lines[i].size > body_size + 0.5
    }
    if len(main_numbers) >= 3:
        for i, (title, _) in list(titles.items()):
            normalized = re.sub(r"^[\d.]+\s+", "", title).strip().casefold()
            number = re.match(r"^(\d+)(?:\.\d+)*\.?\s", title)
            if (
                lines[i].size <= body_size + 0.5
                and not (number and number.group(1) in main_numbers)
                and not _APPENDIX.match(normalized)
                and normalized not in {"references", "bibliography", "參考文獻", "abstract", "摘要"}
            ):
                del titles[i]
    return titles


def _virtual_sections(section: Section, target: int) -> list[Section]:
    # Table Chunks remain typed even when no headings can be identified.
    chunks = chunk_sections([section], "virtual", target=target)
    output = []
    for i, chunk in enumerate(chunks, 1):
        tables = []
        if chunk.kind == "table":
            # Rebuild directly from this Chunk's source fields: repeated labels on
            # different pages must not select another Table's caption or data.
            prefix = f"{chunk.table_caption}\n{chunk.table_meaning}".strip()
            tables = [
                Table(
                    label=chunk.table_label,
                    caption=chunk.table_caption,
                    page_start=chunk.page_start,
                    page_end=chunk.page_end,
                    headers=chunk.table_headers,
                    rows=chunk.table_rows,
                    meaning=chunk.table_meaning,
                    reconstructed=chunk.table_reconstructed,
                    raw_text=(
                        chunk.text.removeprefix(f"{prefix}\n{LIMITATION}\n")
                        if not chunk.table_reconstructed
                        else ""
                    ),
                )
            ]
        output.append(
            Section(
                id=f"virtual-{i}",
                title=f"Virtual Section {i}",
                page_start=chunk.page_start,
                page_end=chunk.page_end,
                paragraphs=[] if tables else [chunk.text],
                paragraph_pages=[] if tables else [(chunk.page_start, chunk.page_end)],
                tables=tables,
                is_virtual=True,
            )
        )
    return output


def _body_continuation_target(line: TextLine) -> bool:
    # A matching font alone cannot establish prose: captions and short top-of-page
    # labels can use body typography too. Require sentence or text-flow evidence.
    return (
        not _CAPTION.match(line.text)
        and not line.shared_row
        and not _NUMERIC_LINE.fullmatch(line.text)
        and (
            bool(_SENTENCE_END.search(line.text))
            or (line.text[0].isascii() and line.text[0].islower())
            or line.bbox[2] - line.bbox[0] >= line.continuation_width * _LINE_WRAP_WIDTH_RATIO
        )
    )


def _continues_on_next_page(previous: TextLine, following: TextLine) -> bool:
    # Called for adjacent source lines; a new Section heading already flushed the paragraph.
    return (
        following.page == previous.page + 1
        and not _SENTENCE_END.search(previous.text)
        and not _NUMERIC_LINE.fullmatch(previous.text)
        and not previous.text.endswith((":", "："))
        and not _CAPTION.match(previous.text)
        and _body_continuation_target(following)
        and aligned_style(previous, following)
    )


def _wraps_line(previous: TextLine, following: TextLine) -> bool:
    right_edge = previous.block_bbox[2]
    block_width = right_edge - previous.block_bbox[0]
    return (
        (
            (
                previous.page == following.page
                and previous.block == following.block
                and following.bbox[1] > previous.bbox[1]
            )
            or _continues_on_next_page(previous, following)
        )
        and (previous.flowing_block or previous.page != following.page)
        and previous.bbox[2] - previous.bbox[0] >= block_width * _LINE_WRAP_WIDTH_RATIO
        and not _NUMERIC_LINE.fullmatch(previous.text)
        and not _NUMERIC_LINE.fullmatch(following.text)
        # Repeated label/value rows can have a shorter final row too. Their
        # whitespace-delimited numeric cells are evidence against flowing prose.
        and not (
            _CJK_TEXT.search(previous.text)
            and _CJK_TEXT.search(following.text)
            and _LABELLED_NUMERIC_ROW.fullmatch(previous.text)
            and _LABELLED_NUMERIC_ROW.fullmatch(following.text)
        )
    )


def build_sections(
    lines: list[TextLine],
    body_size: float,
    target: int,
    tables: list[TableRegion],
    titles: dict[int, tuple[str, int]],
) -> list[Section]:
    sections: list[Section] = []
    current = Section(
        id="section-1",
        title="Front matter",
        page_start=lines[0].page,
        page_end=lines[0].page,
        paragraphs=[],
        paragraph_pages=[],
    )
    pending: list[TextLine] = []
    pending_start = pending_end = lines[0].page
    previous: TextLine | None = None
    excluded = appendix = detected = False

    def flush_paragraph():
        if pending:
            has_cjk = any(_CJK_TEXT.search(line.text) for line in pending)
            paragraph = pending[0].text
            for previous_line, following in zip(pending, pending[1:], strict=False):
                separator = (
                    ""
                    if has_cjk
                    and _wraps_line(previous_line, following)
                    and _CJK_LINE_WRAP.search(previous_line.text[-1:] + "\n" + following.text[:1])
                    else "\n"
                )
                paragraph += separator + following.text
            current.paragraphs.append(paragraph)
            current.paragraph_pages.append((pending_start, pending_end))
            current.page_end = pending_end
            pending.clear()

    def flush_section():
        flush_paragraph()
        if current.paragraphs or current.tables or current.title != "Front matter":
            sections.append(current)

    table_anchors = {region.anchor: region.table for region in tables}
    table_lines = {i for region in tables for i in region.line_indices}
    index = 0
    numbered = [i for i, (title, _) in titles.items() if re.match(r"^\d+(?:\.\d+)*\.?\s", title)]
    if numbered and 0 in titles and lines[0].size > lines[numbered[0]].size + 0.5:
        # Keep the title as metadata and exclude author/affiliation lines, but
        # resume at substantive Abstract content before the numbered hierarchy.
        current.title = titles[0][0]
        index = next(
            (i for i in range(titles[0][1], numbered[0]) if _ABSTRACT.fullmatch(lines[i].text)),
            numbered[0],
        )
    while index < len(lines):
        line = lines[index]
        if index in table_lines:
            flush_paragraph()
            if index in table_anchors and not excluded:
                table = table_anchors[index]
                table.paragraph_index = len(current.paragraphs)
                current.tables.append(table)
                current.page_end = max(current.page_end, table.page_end)
            previous = None
            index += 1
            continue
        abstract = _ABSTRACT.fullmatch(line.text)
        if abstract and abstract.group("body"):
            flush_section()
            current = Section(
                id=f"section-{len(sections) + 1}",
                title=abstract.group("label"),
                page_start=line.page,
                page_end=line.page,
                paragraphs=[abstract.group("body")],
                paragraph_pages=[(line.page, line.page)],
            )
            detected = True
            previous = None
            index += 1
            continue
        title, consumed = titles.get(index, ("", 1))
        if title:
            normalized = re.sub(r"^[\d.]+\s+", "", title).strip().casefold()
            if normalized in {"references", "bibliography", "參考文獻"}:
                flush_section()
                excluded = True
            elif _APPENDIX.match(normalized) or (
                excluded and re.match(r"^[A-Z](?:\.\d+)*\.?\s", title)
            ):
                if not excluded:
                    flush_section()
                excluded = False
                appendix = detected = True
                current = Section(
                    id=f"section-{len(sections) + 1}",
                    title=title if normalized.startswith("appendix") else f"Appendix — {title}",
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
            if previous and (
                (line.page != previous.page and not _continues_on_next_page(previous, line))
                or (line.page == previous.page and line.block != previous.block)
                or (previous.page_first and not _body_continuation_target(previous))
            ):
                flush_paragraph()
            if not pending:
                pending_start = line.page
            pending_end = line.page
            pending.append(line)
            previous = line
        index += 1
    if not excluded:
        flush_section()
    if not any(section.paragraphs or section.tables for section in sections):
        raise DocumentError("This Document has no indexable text outside References.")
    if not detected:
        return _virtual_sections(sections[0], target)
    return sections


def filter_figure_labels(lines, body_size, regions_by_page):
    for page_number, regions in regions_by_page.items():
        page_lines = [line for line in lines if line.page == page_number]
        regions_by_page[page_number] = [
            region for region in regions if not _contains_prose(region, page_lines, body_size)
        ]
    retained = [line for line in lines if not _is_figure_label(line, regions_by_page[line.page])]
    for index, line in enumerate(retained):
        previous = retained[index - 1] if index else None
        line.page_first = previous is None or line.page != previous.page
        if previous and line.page_first and aligned_style(previous, line):
            # A short header cannot establish body width by referring to itself.
            # Carry the measured preceding body flow only into page-target checks.
            line.continuation_width = max(line.flow_width, previous.flow_width)
    return retained, body_size
