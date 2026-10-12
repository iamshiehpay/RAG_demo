"""Coordinate reconstruction of captioned tables; uncertain layouts retain source text."""

import re
from dataclasses import dataclass
from statistics import median

from .models import Table
from .policy import TABLE_TOKEN_LIMIT
from .tokens import count_tokens

LIMITATION = "結構未能可靠重建"
CAPTION = re.compile(r"^((?:Table|Figure)\s+\d+)\s*[:.．]", re.I)


@dataclass
class TableRegion:
    table: Table
    line_indices: set[int]
    anchor: int


def _rows(lines):
    rows = []
    for line in sorted(lines, key=lambda line: (line.bbox[1], line.bbox[0])):
        center = (line.bbox[1] + line.bbox[3]) / 2
        if rows and abs(center - rows[-1][0]) < line.size * 0.45:
            rows[-1][1].append(line)
        else:
            rows.append((center, [line]))
    return [sorted(row, key=lambda line: line.bbox[0]) for _, row in rows]


def _paired_grid(rows):
    """Repeated model subheaders beneath dataset headers, with paired percentage cells."""
    if len(rows) < 3:
        return None
    datasets = [line.text for line in rows[0]]
    count = len(datasets)
    if count < 2 or len(rows[1]) != count * 2:
        return None
    centers = [(line.bbox[0] + line.bbox[2]) / 2 for line in rows[1]]
    headings = None
    output = []
    for row in rows[1:]:
        texts = [line.text for line in row]
        if len(row) == count * 2 and not any("%" in text for text in texts):
            headings = texts
            continue
        if headings is None or len(row) != count * 2 + 1:
            return None
        if not all(re.fullmatch(r"\d+(?:\.\d+)?%", text) for text in texts[1:]):
            return None
        # Reject shifted/missing cells instead of quietly associating numbers to wrong columns.
        if any(
            abs((line.bbox[0] + line.bbox[2]) / 2 - x) > line.size * 1.5
            for line, x in zip(row[1:], centers, strict=True)
        ):
            return None
        pairs = [f"{headings[j]} / {headings[j + 1]}" for j in range(0, count * 2, 2)]
        if len(set(pairs)) != 1:
            return None
        output.append(
            [pairs[0], texts[0], *[f"{texts[j]} / {texts[j + 1]}" for j in range(1, len(texts), 2)]]
        )
    if not output:
        return None
    comparisons = list(dict.fromkeys(row[0] for row in output))
    baselines = {comparison.split(" / ")[0] for comparison in comparisons}
    if len(baselines) == 1:
        baseline = next(iter(baselines))
        meaning = (
            f"每格是 {baseline} 勝率 / 變體勝率 "
            f"({baseline} win rate / variant win rate, %). "
            "These are separate comparisons against the named baseline, "
            "not direct wins against the full system."
        )
        systems = [comparison.split(" / ")[1] for comparison in comparisons]
        # Explicit shortened variant labels refer back to the one unmodified named row.
        named = [system for system in systems if not system.startswith("-")]
        if len(named) == 1 and any(system.startswith("-") for system in systems):
            meaning += (
                f" Unmodified system row: {named[0]} "
                "(the named row without a '-' variant label). "
                "Include that row when comparing systems on the same metric and dataset."
            )
    else:
        meaning = (
            "Each cell is baseline win rate / candidate win rate (%); "
            "the Comparison column names both systems in that order."
        )
    headers = [
        "Comparison",
        "Metric",
        *[f"{dataset} (baseline / variant win rate %)" for dataset in datasets],
    ]
    return headers, output, meaning


def reconstruct_tables(lines) -> list[TableRegion]:
    regions = []
    used = set()
    for i, caption in enumerate(lines):
        match = CAPTION.match(caption.text)
        if not match or i in used:
            continue
        caption_lines = [
            (j, line)
            for j, line in enumerate(lines)
            if line.page == caption.page and line.block == caption.block
        ]
        caption_bottom = max(line.bbox[3] for _, line in caption_lines)
        # PDF blocks are in reading order, but cells are grouped in geometric rows.
        candidates = [
            (j, line)
            for j, line in enumerate(lines)
            if line.page == caption.page
            and line.bbox[1] >= caption_bottom
            and line.bbox[0] >= caption.bbox[0] - 40
            and j not in used
        ]
        candidates.sort(key=lambda item: (item[1].bbox[1], item[1].bbox[0]))
        chosen = []
        bottom = caption_bottom
        height = None
        for j, line in candidates:
            h = line.bbox[3] - line.bbox[1]
            if line.bbox[1] - bottom > 2.2 * (height or h):
                break
            if chosen and (line.size > chosen[0][1].size * 1.2 or CAPTION.match(line.text)):
                break
            chosen.append((j, line))
            bottom = max(bottom, line.bbox[3])
            height = median([cell.bbox[3] - cell.bbox[1] for _, cell in chosen])
        if not chosen:
            continue
        rows = _rows([line for _, line in chosen])
        if match.group(1).lower().startswith("figure") and not (
            len(rows) >= 2 and len(rows[0]) >= 2 and len(rows[1]) >= 2
        ):
            continue
        grid = _paired_grid(rows)
        if (
            grid is None
            and len(rows) >= 2
            and len(rows[0]) >= 2
            and all(len(row) == len(rows[0]) for row in rows)
        ):
            grid = (
                [line.text for line in rows[0]],
                [[line.text for line in row] for row in rows[1:]],
                "",
            )
        raw = "\n".join(" ".join(line.text for line in row) for row in rows)
        table = Table(
            label=match.group(1),
            caption=" ".join(line.text for _, line in caption_lines),
            page_start=caption.page,
            page_end=caption.page,
            raw_text=raw.replace("_", "") if match.group(1).lower().startswith("figure") else raw,
        )
        if grid:
            table.headers, table.rows, table.meaning = grid
            table.reconstructed = True
        indices = {*(j for j, _ in caption_lines), *(j for j, _ in chosen)}
        used.update(indices)
        regions.append(TableRegion(table, indices, i))
    return regions


def table_text(table: Table, rows: list[list[str]] | None = None) -> str:
    prefix = f"{table.caption}\n{table.meaning}".strip()
    if not table.reconstructed:
        return f"{prefix}\n{LIMITATION}\n{table.raw_text}"
    rendered_rows = []
    for row in table.rows if rows is None else rows:
        if table.headers[:2] == ["Comparison", "Metric"]:
            # Repeat dataset and metric at every numeric pair, so values remain unambiguous
            # even when a reader quotes only one cell instead of the complete row.
            values = [
                f"{header.split(' (')[0]} / {row[1]}: {value}"
                for header, value in zip(table.headers[2:], row[2:], strict=True)
            ]
            rendered_rows.append(" | ".join([row[0], row[1], *values]))
        else:
            rendered_rows.append(" | ".join(row))
    return "\n".join([prefix, " | ".join(table.headers), *rendered_rows])


def split_table(table: Table) -> list[tuple[str, list[list[str]]]]:
    """Repeat caption/header and preserve whole source rows in each Table Chunk."""
    if count_tokens(table_text(table)) <= TABLE_TOKEN_LIMIT:
        return [(table_text(table), table.rows)]
    units = table.rows if table.reconstructed else [[line] for line in table.raw_text.splitlines()]
    result = []
    current = []

    def render(rows):
        if table.reconstructed:
            return table_text(table, rows)
        return table_text(table.model_copy(update={"raw_text": "\n".join(row[0] for row in rows)}))

    for row in units:
        if current and count_tokens(render([*current, row])) > TABLE_TOKEN_LIMIT:
            result.append((render(current), current if table.reconstructed else []))
            current = []
        current.append(row)
    if current:
        result.append((render(current), current if table.reconstructed else []))
    return result
