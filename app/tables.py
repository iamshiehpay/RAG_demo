"""Render reconstructed or uncertain tables and split only at complete row boundaries."""

from .models import Table
from .policy import TABLE_TOKEN_LIMIT
from .tokens import count_tokens

LIMITATION = "結構未能可靠重建"


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

    if not table.reconstructed:
        bounded = []
        for row in units:
            remaining = row[0]
            while count_tokens(render([[remaining]])) > TABLE_TOKEN_LIMIT:
                low, high = 0, len(remaining)
                while low < high:
                    middle = (low + high + 1) // 2
                    if count_tokens(render([[remaining[:middle]]])) <= TABLE_TOKEN_LIMIT:
                        low = middle
                    else:
                        high = middle - 1
                if not low:
                    raise ValueError("Table caption leaves no room for raw source text.")
                bounded.append([remaining[:low]])
                remaining = remaining[low:]
            if remaining:
                bounded.append([remaining])
        units = bounded
    for row in units:
        if current and count_tokens(render([*current, row])) > TABLE_TOKEN_LIMIT:
            result.append((render(current), current if table.reconstructed else []))
            current = []
        current.append(row)
    if current:
        result.append((render(current), current if table.reconstructed else []))
    return result
