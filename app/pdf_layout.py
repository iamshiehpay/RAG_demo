"""Extract PDF text geometry and reading order; no Section or Chunk decisions."""

import re
from collections import Counter
from dataclasses import dataclass

import pymupdf

_NUMBER = re.compile(r"(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?")
_SENTENCE_END = re.compile(r"[.!?。！？;；]$")
_PAGE_FRAME_COVERAGE_RATIO = 0.8
_LINE_WRAP_WIDTH_RATIO = 0.9
_NUMERIC_LINE = re.compile(r"[\d\s.,%+\-−]+")
_CAPTION = re.compile(r"(?:Table|Figure)\s+[A-Z]?\d", re.I)


@dataclass
class TextLine:
    text: str
    page: int
    block: int
    bbox: tuple[float, float, float, float]
    block_bbox: tuple[float, float, float, float]
    size: float
    bold: bool
    fonts: tuple[str, ...]
    flow_width: float = 0
    continuation_width: float = 0
    page_first: bool = False
    flowing_block: bool = False
    small_caps: bool = False
    font_change: bool = False
    shared_row: bool = False
    word_boxes: tuple[tuple[str, tuple[float, float, float, float]], ...] = ()


def _ordered_blocks(page: pymupdf.Page) -> tuple[list[dict], bool]:
    blocks = page.get_text("dict", sort=False)["blocks"]
    for block in blocks:
        for index, line in enumerate(block.get("lines", [])):
            line["source_line_index"] = index
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
        if re.match(r"Figure\s+[A-Z]?\d", "".join(s["text"] for s in line["spans"]), re.I)
    ]
    table_captions = [
        pymupdf.Rect(line["bbox"])
        for b in blocks
        for line in b.get("lines", [])
        if re.match(r"Table\s+[A-Z]?\d", "".join(s["text"] for s in line["spans"]), re.I)
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
                and not (
                    region.width >= page.rect.width * _PAGE_FRAME_COVERAGE_RATIO
                    and region.height >= page.rect.height * _PAGE_FRAME_COVERAGE_RATIO
                )
            ):
                # Some figure backgrounds extend through the caption into the next paragraph.
                regions.append(
                    pymupdf.Rect(region.x0, region.y0, region.x1, min(region.y1, caption_rect.y0))
                )
    return regions


def table_boxes(page: pymupdf.Page) -> list[tuple[float, float, float, float]]:
    """Find closed rule rectangles, including four separately emitted edges."""
    drawings = page.get_drawings()
    rectangles = [
        tuple(item[1]) for drawing in drawings for item in drawing["items"] if item[0] == "re"
    ]
    horizontal = [d["rect"] for d in drawings if d["rect"].height < 1 and d["rect"].width > 1]
    vertical = [d["rect"] for d in drawings if d["rect"].width < 1 and d["rect"].height > 1]

    def joined(rules, *, transpose=False):
        runs = []
        coordinates = sorted((r.x0, r.y0, r.y1) if transpose else (r.y0, r.x0, r.x1) for r in rules)
        for axis, start, end in coordinates:
            if runs and abs(axis - runs[-1][0]) <= 1 and start <= runs[-1][2] + 1:
                runs[-1][2] = max(runs[-1][2], end)
            else:
                runs.append([axis, start, end])
        return [
            pymupdf.Rect(axis, start, axis, end)
            if transpose
            else pymupdf.Rect(start, axis, end, axis)
            for axis, start, end in runs
        ]

    horizontal = joined(horizontal)
    vertical = joined(vertical, transpose=True)
    for top in horizontal:
        for bottom in horizontal:
            if bottom.y0 <= top.y0 or abs(top.x0 - bottom.x0) > 1 or abs(top.x1 - bottom.x1) > 1:
                continue
            if all(
                any(
                    abs(edge.x0 - x) <= 1 and edge.y0 <= top.y0 + 1 and edge.y1 >= bottom.y0 - 1
                    for edge in vertical
                )
                for x in (top.x0, top.x1)
            ):
                rectangles.append((top.x0, top.y0, top.x1, bottom.y0))
    return list(dict.fromkeys(rectangles))


def _page_folios(pdf: pymupdf.Document) -> set[tuple[int, tuple[float, ...]]]:
    """Recognize isolated, sequential folios at recurring margin positions.

    A low integer alone is insufficient: body/table/heading numbers remain
    evidence. Logical page numbers may start at an offset, and alternate left
    and right margins; each recurring position must have corroborating pages.
    """
    candidates = []
    for page_number, page in enumerate(pdf, 1):
        blocks = [b for b in page.get_text("dict")["blocks"] if "lines" in b]
        text_lines = [
            ("".join(s["text"] for s in line["spans"]).strip(), line)
            for block in blocks
            for line in block["lines"]
        ]
        sizes = Counter()
        for text, text_line in text_lines:
            if not text.isdigit():
                for span in text_line["spans"]:
                    sizes[round(span["size"])] += len(span["text"].strip())
        body_size = sizes.most_common(1)[0][0] if sizes else 0
        for block in blocks:
            if len(block["lines"]) != 1:
                continue
            line = block["lines"][0]
            text = "".join(s["text"] for s in line["spans"]).strip()
            if not text.isascii() or not text.isdigit():
                continue
            bbox = tuple(line["bbox"])
            x = (bbox[0] + bbox[2]) / (2 * page.rect.width)
            y = (bbox[1] + bbox[3]) / (2 * page.rect.height)
            if 0.25 <= y <= 0.75:
                continue
            size = max(s["size"] for s in line["spans"])
            # A separated, left-aligned larger/bold title authenticates an
            # upper-margin Section numeral even with a generous vertical gap.
            if y < 0.25 and any(
                re.search(r"[^\W\d_]", other_text)
                and 0 < other["bbox"][1] - bbox[1] <= size * 4
                and abs(other["bbox"][0] - bbox[0]) <= size * 2
                and any(s["size"] > body_size + 0.5 or s["flags"] & 16 for s in other["spans"])
                for other_text, other in text_lines
                if other is not line
            ):
                continue
            # Nearby title/body labels or aligned table cells disqualify a
            # number. Ignore other isolated digits; they cannot authenticate it.
            if any(
                other_text
                and not other_text.isdigit()
                and max(other["bbox"][1] - bbox[3], bbox[1] - other["bbox"][3], 0) < size * 1.5
                for other_text, other in text_lines
                if other is not line
            ):
                continue
            candidates.append((page_number, int(text) - page_number, x, y, bbox))
    return {
        (page, bbox)
        for page, offset, x, y, bbox in candidates
        if any(
            other_page != page
            and other_offset == offset
            and abs(other_x - x) < 0.025
            and abs(other_y - y) < 0.01
            for other_page, other_offset, other_x, other_y, _ in candidates
        )
    }


def read_layout(
    pdf: pymupdf.Document,
) -> tuple[list[TextLine], float, dict[int, list[pymupdf.Rect]]]:
    lines = []
    sizes: Counter[int] = Counter()
    font_sizes: Counter[tuple[int, str]] = Counter()
    regions_by_page = {}
    folios = _page_folios(pdf)
    for page_number, page in enumerate(pdf, 1):
        page_lines = []
        blocks, two_columns = _ordered_blocks(page)
        word_boxes = {}
        for word in page.get_text("words"):
            word_boxes.setdefault((word[5], word[6]), []).append((word[4], tuple(word[:4])))
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
                if (page_number, bbox) in folios:
                    continue  # Page numbers are not paragraphs or Section numbers.
                for span in spans:
                    sizes[round(span["size"])] += len(span["text"].strip())
                    font_sizes[(round(span["size"]), span["font"])] += len(span["text"].strip())
                max_size = max(s["size"] for s in spans)
                page_lines.append(
                    TextLine(
                        text=text,
                        page=page_number,
                        block=block_number,
                        bbox=bbox,
                        block_bbox=tuple(block["bbox"]),
                        size=max_size,
                        bold=all(s["flags"] & 16 for s in spans),
                        fonts=tuple(sorted({s["font"] for s in spans})),
                        word_boxes=tuple(
                            word_boxes.get((block["number"], line["source_line_index"]), [])
                        ),
                        small_caps=text.isupper()
                        and any(
                            s["size"] < max_size * 0.9 and any(char.isalpha() for char in s["text"])
                            for s in spans
                        ),
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
        if page_lines:
            page_lines[0].page_first = True
        for line in page_lines:
            line.flow_width = _measured_flow_width(line, page_lines)
            line.continuation_width = line.flow_width
        for block_number in {line.block for line in page_lines}:
            block_lines = [line for line in page_lines if line.block == block_number]
            width = max(line.bbox[2] - line.bbox[0] for line in block_lines)
            last = block_lines[-1]
            # A ragged final line or completed sentence spanning the page/column
            # gives evidence beyond comparing each row to its own block width.
            flowing = len(block_lines) > 1 and (
                last.bbox[2] - last.bbox[0] < width * _LINE_WRAP_WIDTH_RATIO
                or (
                    width >= last.flow_width * _LINE_WRAP_WIDTH_RATIO
                    and bool(_SENTENCE_END.search(last.text))
                )
            )
            for line in block_lines:
                line.flowing_block = flowing
        lines.extend(page_lines)
    body_size = sizes.most_common(1)[0][0] if sizes else 0
    body_fonts = Counter(
        {font: weight for (size, font), weight in font_sizes.items() if size == body_size}
    )
    body_font = body_fonts.most_common(1)[0][0] if body_fonts else ""
    for line in lines:
        line.font_change = bool(body_font and body_font not in line.fonts)
    return lines, body_size, regions_by_page


def aligned_style(left: TextLine, right: TextLine) -> bool:
    return (
        abs(left.size - right.size) < 0.5
        and left.fonts == right.fonts
        and left.bold == right.bold
        and abs(left.bbox[0] - right.bbox[0]) <= left.size * 2
    )


def _measured_flow_width(line: TextLine, page_lines: list[TextLine]) -> float:
    """Use actual aligned text, so column widths do not imply symmetric margins."""
    return max(
        (
            other.bbox[2] - other.bbox[0]
            for other in page_lines
            if aligned_style(line, other)
            and other.bbox[2] <= line.block_bbox[2] + line.size * 2
            and not other.shared_row
            and not _CAPTION.match(other.text)
            and not _NUMERIC_LINE.fullmatch(other.text)
        ),
        default=line.block_bbox[2] - line.block_bbox[0],
    )
