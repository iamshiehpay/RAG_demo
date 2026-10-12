"""Pack whole paragraphs inside Sections; only oversized paragraphs overlap."""

import re

from .models import Chunk, Section
from .policy import CHUNK_TOKEN_TARGET, OVERSIZED_PARAGRAPH_OVERLAP
from .tokens import count_tokens

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+|(?<=[。！？])\s*")
WHITESPACE = re.compile(r"\s+")
LATIN_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


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
    # Prefer a nearby sentence start, otherwise snap forward to a complete word.
    sentence_starts = [
        m.end()
        for m in SENTENCE_BOUNDARY.finditer(text, start + 1, end)
        if low <= m.end() < end and count_tokens(text[m.end() : end]) >= target / 2
    ]
    if sentence_starts:
        return sentence_starts[0]
    while low < end and text[low].isspace():
        low += 1
    for word in LATIN_WORD.finditer(text, start, end):
        if word.start() < low < word.end():
            low = word.end()
            while low < end and text[low].isspace():
                low += 1
            break
    return low


def _paragraphs(text: str, target: int):
    if count_tokens(text) <= target:
        yield text
        return
    # Latin punctuation needs following whitespace; decimal/abbreviation dots stay intact.
    boundaries = [m.end() for m in SENTENCE_BOUNDARY.finditer(text)]
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
        if end == hard_end:
            # A single sentence can itself exceed the target. Keep whole words where possible.
            end = max(
                (
                    m.end()
                    for m in WHITESPACE.finditer(text, start, hard_end)
                    if m.end() > previous_end
                ),
                default=hard_end,
            )
        yield text[start:end].strip()
        previous_end = end
        start = _overlap_start(text, start, end, round(target * OVERSIZED_PARAGRAPH_OVERLAP))


def chunk_sections(
    sections: list[Section], document_id: str, target: int = CHUNK_TOKEN_TARGET
) -> list[Chunk]:
    chunks = []
    for section in sections:
        current = []
        current_pages = []

        def flush(current=current, current_pages=current_pages, section=section):
            if current:
                chunks.append(
                    Chunk(
                        id=f"{document_id}:chunk-{len(chunks) + 1}",
                        section_id=section.id,
                        section=section.title,
                        page_start=min(p[0] for p in current_pages),
                        page_end=max(p[1] for p in current_pages),
                        text="\n\n".join(current),
                        order=len(chunks),
                    )
                )
                current.clear()
                current_pages.clear()

        for i, paragraph in enumerate(section.paragraphs):
            pages = (
                section.paragraph_pages[i]
                if section.paragraph_pages
                else (section.page_start, section.page_end)
            )
            for bounded in _paragraphs(paragraph, target):
                if current and count_tokens("\n\n".join([*current, bounded])) > target:
                    flush()
                current.append(bounded)
                current_pages.append(pages)
        flush()
    return chunks
