"""Interpret aligned table cells, retaining uncertainty instead of guessing values."""

import re
from dataclasses import replace


def _paired_grid(rows):
    """Repeated model subheaders beneath dataset headers, with paired percentage cells."""
    if len(rows) < 3:
        return None
    datasets = [_clean(line.text) for line in rows[0]]
    count = len(datasets)
    if count < 2 or len(rows[1]) != count * 2:
        return None
    centers = [(line.bbox[0] + line.bbox[2]) / 2 for line in rows[1]]
    headings = None
    output = []
    for row in rows[1:]:
        texts = [_clean(line.text) for line in row]
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
        *[
            f"{dataset} (baseline / {'variant' if len(baselines) == 1 else 'candidate'} win rate %)"
            for dataset in datasets
        ],
    ]
    return headers, output, meaning


def _clean(text: str) -> str:
    # Stray math-italic underscores are separators/suffixes, not identifier underscores.
    return re.sub(r"(?<![A-Za-z0-9])_|_(?![A-Za-z0-9])|(?<=\d)_(?=\d)", "", text)


def _numeric(text):
    return bool(re.search(r"\d", text)) and not re.search(r"[A-Za-z]", text)


def _reference_grid(rows):
    """Wrapped labels in a reference/identifier column define logical rows.

    Numeric model-version text stays in the label column. Every metric cell must
    align with a printed header and occur exactly once; missing/ambiguous cells
    return the raw fallback instead of shifting numbers between columns.
    """
    if not rows or len(rows[0]) < 4:
        return None
    header = rows[0]
    if _clean(header[0].text).casefold() not in {"ref", "reference", "id", "identifier"}:
        return None
    data_rows = [
        [
            replace(line, text=text, bbox=box)
            for line in row
            if not (
                re.fullmatch(r"continued(?:\s+on)?\s+(?:the\s+)?next\s+page", line.text, re.I)
                and line.bbox[0] > header[1].bbox[2]
            )
            for text, box in line.word_boxes
        ]
        if all(getattr(line, "word_boxes", ()) for line in row)
        else row
        for row in rows[1:]
    ]
    anchors = [
        line
        for row in data_rows
        for line in row
        if abs(line.bbox[0] - header[0].bbox[0]) <= line.size * 1.5
        and re.fullmatch(r"\[\d+\]|\d+", _clean(line.text))
    ]
    if not anchors:
        return None
    centers = [(line.bbox[1] + line.bbox[3]) / 2 for line in anchors]
    columns = [(line.bbox[0] + line.bbox[2]) / 2 for line in header]
    cells = [[[] for _ in header] for _ in anchors]
    for parts in data_rows:
        # MuPDF may merge adjacent text and numeric columns into one line.
        # Use its original word coordinates; never split a number by guessing
        # character widths or by interpreting a model-version label as a score.
        for line in parts:
            y = (line.bbox[1] + line.bbox[3]) / 2
            if y > max(centers) + line.size * 2.5 and (
                line.text == str(line.page) or line.text.casefold().startswith("continued")
            ):
                continue  # Physical page/continuation metadata outside the data rows.
            index = min(range(len(anchors)), key=lambda i: abs(y - centers[i]))
            if abs(y - centers[index]) > line.size * 2.5:
                return None
            x = (line.bbox[0] + line.bbox[2]) / 2
            col = min(range(len(header)), key=lambda i: abs(x - columns[i]))
            if abs(x - columns[col]) > line.size * 1.5:
                return None
            value = _clean(line.text)
            if col >= 2 and not _numeric(value):
                return None
            cells[index][col].append(value)
    if any(not cell for row in cells for cell in row) or any(
        len(cell) != 1 for row in cells for cell in [row[0], *row[2:]]
    ):
        return None
    return (
        [_clean(line.text) for line in header],
        [[" ".join(cell) for cell in row] for row in cells],
        "Identifiers and model-version numbers belong to the printed label column; "
        "the other columns contain the values named by their printed headers.",
    )


def _rectangular_grid(rows):
    if len(rows) < 2 or len(rows[0]) < 2 or any(len(row) != len(rows[0]) for row in rows):
        return None
    # Each column needs a consistent left edge, centre, or right edge; cell counts
    # alone do not identify a grid. Numeric data needs a nonnumeric row-label cell.
    for column in zip(*rows, strict=True):
        tolerance = max(line.size for line in column) * 1.5
        anchors = [
            (line.bbox[0], (line.bbox[0] + line.bbox[2]) / 2, line.bbox[2]) for line in column
        ]
        if not any(
            max(a[k] for a in anchors) - min(a[k] for a in anchors) <= tolerance for k in range(3)
        ):
            return None
    texts = [[_clean(line.text) for line in row] for row in rows]
    if not any(_numeric(cell) for row in texts[1:] for cell in row[1:]):
        return None
    if any(_numeric(row[0]) for row in texts[1:]):
        return None
    return texts[0], texts[1:], ""
