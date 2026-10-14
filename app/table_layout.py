"""Find captioned table regions and continuation pages using PDF coordinates."""

import re
from dataclasses import dataclass
from statistics import median

from .models import Table
from .table_grid import _clean, _numeric, _paired_grid, _rectangular_grid, _reference_grid

CAPTION = re.compile(r"^((?:Table|Figure)\s+[A-Z]?\d+)\s*[:.．]", re.I)


@dataclass
class TableRegion:
    table: Table
    line_indices: set[int]
    anchor: int
    bounds: tuple[float, float] | None = None


def _rows(lines):
    rows = []
    for line in sorted(lines, key=lambda line: (line.bbox[1], line.bbox[0])):
        center = (line.bbox[1] + line.bbox[3]) / 2
        if rows and abs(center - rows[-1][0]) < line.size * 0.45:
            rows[-1][1].append(line)
        else:
            rows.append((center, [line]))
    return [sorted(row, key=lambda line: line.bbox[0]) for _, row in rows]


def _column_bounds(caption, page_lines, page_width):
    left = min(line.bbox[0] for line in page_lines)
    right = max(line.bbox[2] for line in page_lines)
    middle = page_width / 2
    # Centred/full-width captions use the whole text region. Narrow side captions
    # share a column only when there is separate text in the opposite half.
    other_right = [
        line
        for line in page_lines
        if line.bbox[0] >= middle
        and (
            len(line.text.split()) >= 7
            or CAPTION.match(line.text)
            or (getattr(line, "flowing_block", False) and len(line.text.split()) >= 4)
        )
    ]
    if caption.bbox[2] <= middle and other_right:
        return left, min(line.bbox[0] for line in other_right) - 2
    other_left = [
        line
        for line in page_lines
        if line.bbox[0] < middle
        and line.bbox[2] <= caption.bbox[0] - 2
        and (
            len(line.text.split()) >= 7
            or CAPTION.match(line.text)
            or (getattr(line, "flowing_block", False) and len(line.text.split()) >= 4)
        )
    ]
    if caption.bbox[0] >= middle and other_left:
        return max(line.bbox[2] for line in other_left) + 2, right
    return left, right


def _prose(line, width):
    words = line.text.split()
    if (
        not words
        or sum(bool(re.search(r"[A-Za-z\u4e00-\u9fff]", word)) for word in words) < len(words) * 0.7
    ):
        return False
    return (len(words) >= 7 and line.bbox[2] - line.bbox[0] >= width * 0.72) or (
        len(words) >= 4 and bool(re.search(r"[.!?。！？](?:\s|$)", line.text))
    )


def _grid_follows(rows, formed, width, *, above, heading_lines, indices):
    """Keep an internal divider when nearby rows resume the same numeric grid."""
    size = max(line.size for row in formed for line in row)
    for prior, row in zip(rows, rows[1:], strict=False):
        gap = (
            min(line.bbox[1] for line in prior) - max(line.bbox[3] for line in row)
            if above
            else min(line.bbox[1] for line in row) - max(line.bbox[3] for line in prior)
        )
        height = median(line.bbox[3] - line.bbox[1] for line in prior)
        if (
            gap > 2.2 * height
            or any(indices[id(line)] in heading_lines for line in row)
            or any(CAPTION.match(line.text) for line in row)
            or any(abs(line.size - size) >= 0.5 for line in row)
            or (len(row) == 1 and _prose(row[0], width))
        ):
            return False
        extended = _rows([*(line for group in formed for line in group), *row])
        if _paired_grid(extended) or _rectangular_grid(extended):
            return True
    return False


def _collect(candidates, caption_edge, width, *, above=False, heading_lines=frozenset()):
    rows = _rows([line for _, line in candidates])
    if above:
        rows.reverse()
    indices = {id(line): j for j, line in candidates}
    chosen = []
    edge = caption_edge
    first_size = None
    height = None
    text_cell_x = None
    for position, row in enumerate(rows):
        if any(indices[id(line)] in heading_lines for line in row):
            break
        top, bottom = min(line.bbox[1] for line in row), max(line.bbox[3] for line in row)
        h = median(line.bbox[3] - line.bbox[1] for line in row)
        gap = edge - bottom if above else top - edge
        if gap > 2.2 * (height or h):
            break
        if any(CAPTION.match(line.text) for line in row):
            break
        if first_size is not None and any(line.size > first_size * 1.2 for line in row):
            break
        # Once numeric cells form a reliable grid, a trailing list/equation is
        # body content. A damaged numeric row is still table evidence: retain it
        # and mark the whole region uncertain instead of silently losing cells.
        if chosen and not any(_numeric(line.text) for line in row):
            formed = _rows([line for _, line in chosen])
            extended = _rows([*(line for _, line in chosen), *row])
            if (_paired_grid(formed) or _rectangular_grid(formed)) and not (
                _paired_grid(extended) or _rectangular_grid(extended)
            ):
                if not _grid_follows(
                    rows[position:],
                    formed,
                    width,
                    above=above,
                    heading_lines=heading_lines,
                    indices=indices,
                ):
                    break
        prose = [line for line in row if _prose(line, width)]
        if prose:
            # A labelled prose cell is source table content, but plain paragraph
            # lines (including aligned lines from two body columns) never start a grid.
            labelled = len(row) >= 2 and not _prose(row[0], width)
            continuation = (
                text_cell_x is not None
                and all(line.bbox[0] >= text_cell_x - 2 for line in row)
                and all(abs(line.size - first_size) < 0.5 for line in row)
            )
            if not labelled and not continuation:
                break
            if labelled:
                text_cell_x = prose[0].bbox[0]
        chosen.extend((indices[id(line)], line) for line in row)
        edge = top if above else bottom
        height = h
        if first_size is None:
            first_size = max(line.size for line in row)
    return chosen


def _continue_tables(regions, lines, heading_lines):
    """Repeated geometric headers identify continuation pages, not prose guesses.

    Keep each page's own provenance. A text-rich or damaged grid is retained as
    raw rows with its original caption and an explicit reconstruction limitation.
    """
    result = []
    occupied = {i for region in regions for i in region.line_indices}
    for region in regions:
        candidates = [
            lines[i]
            for i in sorted(region.line_indices)
            if not CAPTION.match(lines[i].text) and lines[i].block != lines[region.anchor].block
        ]
        rows = _rows(candidates)
        # The caption can precede or follow the grid; use its existing detected
        # raw region's first multi-cell, nonnumeric header row as the signature.
        headers = next(
            (r for r in rows if len(r) >= 2 and not any(_numeric(line.text) for line in r)), []
        )
        continuations = []
        if headers:
            for page in range(region.table.page_end + 1, max(line.page for line in lines) + 1):
                page_indices = [i for i, line in enumerate(lines) if line.page == page]
                page_rows = _rows([lines[i] for i in page_indices])
                if not page_rows:
                    break
                first = page_rows[0]
                if len(first) != len(headers) or not all(
                    re.sub(r"[↑↓\s]", "", _clean(a.text)).casefold()
                    == re.sub(r"[↑↓\s]", "", _clean(b.text)).casefold()
                    and abs(a.bbox[0] - b.bbox[0]) <= b.size * 1.5
                    and abs(a.size - b.size) < 0.5
                    for a, b in zip(first, headers, strict=True)
                ):
                    break
                if region.bounds:
                    shift = first[0].bbox[0] - headers[0].bbox[0]
                    left, right = region.bounds
                    page_indices = [
                        i
                        for i in page_indices
                        if lines[i].bbox[0] >= left + shift - 2
                        and lines[i].bbox[2] <= right + shift + 2
                    ]
                if any(i in occupied or i in heading_lines for i in page_indices) or any(
                    CAPTION.match(lines[i].text) for i in page_indices
                ):
                    break
                continuations.append(page_indices)
        if continuations:
            start_y = min(line.bbox[1] for line in headers)
            first_indices = {
                i
                for i, line in enumerate(lines)
                if line.page == region.table.page_start
                and line.bbox[1] >= start_y
                and i not in heading_lines
                and (
                    region.bounds is None
                    or (
                        line.bbox[0] >= region.bounds[0] - 2
                        and line.bbox[2] <= region.bounds[1] + 2
                    )
                )
            }
            # Expansion is safe only for a dedicated first table page: another
            # caption or Section after the header ends the region instead.
            if any(CAPTION.match(lines[i].text) for i in first_indices) or any(
                line.page == region.table.page_start
                and line.bbox[1] >= start_y
                and i in heading_lines
                for i, line in enumerate(lines)
            ):
                continuations = []
            else:
                caption_indices = region.line_indices - {
                    i for i in region.line_indices if lines[i] in candidates
                }
                region.line_indices = first_indices | caption_indices
                region.table.raw_text = "\n".join(
                    " ".join(_clean(line.text) for line in row)
                    for row in _rows([lines[i] for i in sorted(first_indices)])
                )
                first_rows = _rows([lines[i] for i in first_indices])
                grid = (
                    _paired_grid(first_rows)
                    or _rectangular_grid(first_rows)
                    or _reference_grid(first_rows)
                )
                region.table.reconstructed = bool(grid)
                region.table.headers, region.table.rows, region.table.meaning = grid or ([], [], "")
        result.append(region)
        for indices in continuations:
            page_rows = _rows([lines[i] for i in indices])
            grid = (
                _paired_grid(page_rows)
                or _rectangular_grid(page_rows)
                or _reference_grid(page_rows)
            )
            table = region.table.model_copy(
                update={
                    "page_start": lines[indices[0]].page,
                    "page_end": lines[indices[0]].page,
                    "raw_text": "\n".join(
                        " ".join(_clean(line.text) for line in row) for row in page_rows
                    ),
                    "reconstructed": bool(grid),
                    "headers": grid[0] if grid else [],
                    "rows": grid[1] if grid else [],
                    "meaning": grid[2] if grid else "",
                }
            )
            result.append(TableRegion(table, set(indices), min(indices)))
            occupied.update(indices)
    return sorted(result, key=lambda region: region.anchor)


def reconstruct_tables(
    lines, *, page_widths=None, heading_lines=frozenset(), boxes_by_page=None
) -> list[TableRegion]:
    regions = []
    used = set()
    for i, caption in enumerate(lines):
        match = CAPTION.match(caption.text)
        if not match or i in used:
            continue
        page_lines = [line for line in lines if line.page == caption.page]
        preceding = [
            line for line in lines[:i] if line.page == caption.page and line.block == caption.block
        ]
        # A wrapped body sentence beginning "Table N." is not a caption.
        # Distinct caption typography can still open a caption within a block.
        if preceding and all(
            abs(line.size - caption.size) < 0.5
            and line.bold == caption.bold
            and line.fonts == caption.fonts
            for line in preceding
        ):
            continue
        page_width = (page_widths or {}).get(caption.page, max(line.bbox[2] for line in page_lines))
        left, right = _column_bounds(caption, page_lines, page_width)
        caption_lines = [
            (j, line)
            for j, line in enumerate(lines)
            if line.page == caption.page
            and line.block == caption.block
            and j >= i
            and line.bbox[0] >= left - 2
            and line.bbox[2] <= right + 2
        ]
        caption_top = min(line.bbox[1] for _, line in caption_lines)
        caption_bottom = max(line.bbox[3] for _, line in caption_lines)
        available = [
            (j, line)
            for j, line in enumerate(lines)
            if line.page == caption.page
            and j not in used
            and line.bbox[0] >= left - 2
            and line.bbox[2] <= right + 2
            and line.block != caption.block
        ]
        chosen = _collect(
            [(j, line) for j, line in available if line.bbox[1] >= caption_bottom],
            caption_bottom,
            right - left,
            heading_lines=heading_lines,
        )
        # Captions below a table must not swallow the following body paragraph.
        if not any(len(row) >= 2 for row in _rows([line for _, line in chosen])):
            chosen = _collect(
                [(j, line) for j, line in available if line.bbox[3] <= caption_top],
                caption_top,
                right - left,
                above=True,
                heading_lines=heading_lines,
            )
        rows = _rows([line for _, line in chosen])
        if len(rows) < 2 or not any(len(row) >= 2 for row in rows):
            # A captioned closed cell is still a table when it contains one
            # column (e.g. code/query strings). Geometry bounds the raw fallback;
            # ordinary neighboring prose must not become an invented grid.
            boxed = []
            if match.group(1).casefold().startswith("table"):
                for box in (boxes_by_page or {}).get(caption.page, []):
                    x0, y0, x1, y1 = box
                    gap = min(abs(y0 - caption_bottom), abs(caption_top - y1))
                    if gap > caption.size * 3 or not (x0 - 2 <= caption.bbox[0] <= x1 + 2):
                        continue
                    contained = [
                        (j, line)
                        for j, line in available
                        if line.bbox[0] >= x0 - 1
                        and line.bbox[2] <= x1 + 1
                        and line.bbox[1] >= y0 - 1
                        and line.bbox[3] <= y1 + 1
                    ]
                    if contained and not any(j in heading_lines for j, _ in contained):
                        boxed.append(((x1 - x0) * (y1 - y0), contained))
            if not boxed:
                continue
            chosen = max(boxed, key=lambda value: value[0])[1]
            rows = _rows([line for _, line in chosen])
        grid = _paired_grid(rows) or _rectangular_grid(rows) or _reference_grid(rows)
        raw = "\n".join(" ".join(_clean(line.text) for line in row) for row in rows)
        table = Table(
            label=match.group(1),
            caption=" ".join(line.text for _, line in caption_lines),
            page_start=caption.page,
            page_end=caption.page,
            raw_text=raw,
        )
        if grid:
            table.headers, table.rows, table.meaning = grid
            table.reconstructed = True
        indices = {*(j for j, _ in caption_lines), *(j for j, _ in chosen)}
        used.update(indices)
        regions.append(TableRegion(table, indices, min(indices), (left, right)))
    return _continue_tables(regions, lines, heading_lines)
