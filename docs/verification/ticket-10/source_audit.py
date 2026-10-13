"""Read-only structural and source-token evidence; no service/model calls.

Run with PYTHONPATH=src from the repository root. Pass --output for a JSON file.
Independent QA still owns acceptance; these checks do not verify every semantic
association in a reconstructed table or actual generated summary lengths.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import pymupdf

from chat_document.chunker import chunk_sections
from chat_document.pdf_parser import parse_pdf
from chat_document.tokens import count_tokens


def audit(path):
    sections = parse_pdf(path.read_bytes())
    chunks = chunk_sections(sections, "audit")
    rows = []
    for section in sections:
        own = [c for c in chunks if c.section_id == section.id]
        tokens = count_tokens(
            "\n\n".join(section.paragraphs + [c.text for c in own if c.kind == "table"])
        )
        rows.append(
            {
                "id": section.id,
                "title": section.title,
                "pages": [section.page_start, section.page_end],
                "appendix": section.is_appendix,
                "source_tokens": tokens,
                "target": max(80, min(500, round(tokens * 0.15))) if own else 0,
                "chunks": len(own),
                "tables": [
                    {
                        "label": t.label,
                        "pages": [t.page_start, t.page_end],
                        "reconstructed": t.reconstructed,
                        "rows": len(t.rows),
                        "raw_sha256": hashlib.sha256(t.raw_text.encode()).hexdigest(),
                    }
                    for t in section.tables
                ],
            }
        )
    return (
        sections,
        chunks,
        {
            "pdf": str(path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "sections": rows,
            "source_bearing_sections": sum(bool(r["chunks"]) for r in rows),
            "chunk_count": len(chunks),
            "target_total": sum(r["target"] for r in rows),
            "all_chunk_pages_inside_own_section": all(
                s.page_start <= c.page_start <= c.page_end <= s.page_end
                for s in sections
                for c in chunks
                if c.section_id == s.id
            ),
        },
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    primary, primary_chunks, light = audit(Path("data/lightrag.pdf"))
    sections, chunks, second = audit(Path("data/industrial-robotics.pdf"))
    table2 = next(c for c in primary_chunks if c.table_label == "Table 2")
    original_table2 = next(t for s in primary for t in s.tables if t.label == "Table 2")
    light["table2"] = {
        "text_sha256": hashlib.sha256(table2.text.encode()).hexdigest(),
        "tokens": count_tokens(table2.text),
        "raw_tokens": count_tokens(original_table2.raw_text),
        "raw_sha256": hashlib.sha256(original_table2.raw_text.encode()).hexdigest(),
        "rows": table2.table_rows,
        "section": table2.section,
        "pages": [table2.page_start, table2.page_end],
    }
    tables = [t for s in sections for t in s.tables if t.label == "Table D5"]
    model_rows = [row for t in tables for row in t.rows]
    # Independent PDF-word census excludes the Model label/version column by
    # printed header geometry. Compare all metric values without guessing rows.
    raw_values = []
    with pymupdf.open("data/industrial-robotics.pdf") as pdf:
        for page in pdf[92:104]:
            words = page.get_text("words")
            model = next(w for w in words if w[4] == "Model")
            total = next(w for w in words if w[4] == "Total")
            boundary = (model[2] + total[0]) / 2
            import re

            raw_values.extend(
                w[4]
                for w in words
                if (w[0] + w[2]) / 2 > boundary
                and w[1] > model[3]
                and re.fullmatch(r"\d+\.\d+", w[4])
            )
    output = {
        "lightrag": light,
        "second_document": second,
        "D5": {
            "rows": len(model_rows),
            "numeric_cells": sum(len(r[2:]) for r in model_rows),
            "independent_pdf_numeric_cells": len(raw_values),
            "all_numeric_values_preserved": Counter(raw_values)
            == Counter(v for r in model_rows for v in r[2:]),
            "first_two_rows": model_rows[:2],
            "caveat": "Counter conservation plus spot-checked rows does not independently "
            "validate every association.",
        },
        "Table9": [t.model_dump() for s in sections for t in s.tables if t.label == "Table 9"],
    }
    serialized = json.dumps(output, indent=2)
    if args.output:
        args.output.write_text(serialized)
    else:
        print(serialized)


if __name__ == "__main__":
    main()
