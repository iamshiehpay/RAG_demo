"""Map short Citation IDs to stable Chunk IDs (validation arrives in #07)."""

import re

from .models import Chunk, Citation


def citation_map(chunks: list[Chunk]) -> list[Citation]:
    return [
        Citation(
            id=f"C{i}",
            source_id=chunk.id,
            section=chunk.section,
            page_start=chunk.page_start,
            page_end=chunk.page_end,
        )
        for i, chunk in enumerate(chunks, start=1)
    ]


def cited_sources(answer: str, citations: list[Citation]) -> list[Citation]:
    ids = set(re.findall(r"\[(C\d+)\]", answer))
    return [citation for citation in citations if citation.id in ids]
