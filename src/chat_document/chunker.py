"""Pack whole paragraphs within each virtual Section; bound oversized paragraphs."""

import re

from .models import Chunk, Section
from .tokens import TOKENIZER, count_tokens, encode


def _paragraphs(text: str, target: int):
    if count_tokens(text) <= target:
        yield text
        return
    sentences = re.split(r"(?<=[.!?。！？])\s*", text)
    current = ""
    for sentence in sentences:
        if count_tokens(sentence) > target:
            if current:
                yield current
                current = ""
            tokens = encode(sentence)
            for start in range(0, len(tokens), target):
                yield TOKENIZER.decode(tokens[start : start + target])
        elif current and count_tokens(current + "\n" + sentence) > target:
            yield current
            current = sentence
        else:
            current = f"{current}\n{sentence}".strip()
    if current:
        yield current


def chunk_sections(sections: list[Section], document_id: str, target: int = 500) -> list[Chunk]:
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
