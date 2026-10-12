"""Pack whole paragraphs within each virtual Section; bound oversized paragraphs."""

import re

from .models import Chunk, Section
from .policy import CHUNK_TOKEN_TARGET, OVERSIZED_PARAGRAPH_OVERLAP
from .tokens import count_tokens


def _prefix_end(text: str, start: int, target: int) -> int:
    """Find a token-bounded prefix while preserving complete Unicode characters."""
    low, high = start, len(text)
    while low < high:
        middle = (low + high + 1) // 2
        if count_tokens(text[start:middle]) <= target:
            low = middle
        else:
            high = middle - 1
    if low == start:
        raise ValueError("Chunk token target cannot fit one Unicode character.")
    return low


def _overlap_start(text: str, start: int, end: int, target: int) -> int:
    low, high = start + 1, end
    while low < high:
        middle = (low + high) // 2
        if count_tokens(text[middle:end]) <= target:
            high = middle
        else:
            low = middle + 1
    return low


def _paragraphs(text: str, target: int):
    if count_tokens(text) <= target:
        yield text
        return
    # Latin punctuation needs following whitespace; decimal/abbreviation dots stay intact.
    boundaries = [m.end() for m in re.finditer(r"(?<=[.!?])\s+|(?<=[。！？])\s*", text)]
    start, previous_end = 0, 0
    while start < len(text):
        hard_end = _prefix_end(text, start, target)
        if hard_end == len(text):
            yield text[start:]
            return
        end = max(
            (
                b
                for b in boundaries
                if previous_end < b <= hard_end and count_tokens(text[start:b]) <= target
            ),
            default=hard_end,
        )
        yield text[start:end]
        previous_end = end
        start = _overlap_start(text, start, end, round(target * OVERSIZED_PARAGRAPH_OVERLAP))


def chunk_sections(
    sections: list[Section], document_id: str, target: int = CHUNK_TOKEN_TARGET
) -> list[Chunk]:
    chunks = []
    for section in sections:
        current = []

        def flush(current=current, section=section):
            if current:
                chunks.append(
                    Chunk(
                        id=f"{document_id}:chunk-{len(chunks) + 1}",
                        section_id=section.id,
                        section=section.title,
                        page_start=section.page_start,
                        page_end=section.page_end,
                        text="\n\n".join(current),
                        order=len(chunks),
                    )
                )
                current.clear()

        for paragraph in section.paragraphs:
            for bounded in _paragraphs(paragraph, target):
                if current and count_tokens("\n\n".join([*current, bounded])) > target:
                    flush()
                current.append(bounded)
        flush()
    return chunks
