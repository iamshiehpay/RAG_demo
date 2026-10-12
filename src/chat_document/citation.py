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


class CitationText:
    """Canonicalize Citation brackets without losing IDs or ordinary prose.

    Buffer only a possible Citation prefix, so tokens like 【 / C3 / 】 work
    across frames. Unknown IDs stay intact for the later Citation Validator.
    """

    def __init__(self):
        self.pending = ""

    def feed(self, text: str) -> str:
        output = []
        for character in text:
            if not self.pending and character not in "[【［":
                output.append(character)
                continue
            self.pending += character
            complete = re.fullmatch(
                r"[\[【［]\s*(C\d+(?:\s*,\s*C\d+)*)\s*(?:†L\d+(?:-L\d+)?)?[\]】］]", self.pending
            )
            if complete:
                output.append("".join(f"[{id}]" for id in re.findall(r"C\d+", complete[1])))
                self.pending = ""
            elif not re.fullmatch(
                r"[\[【［]\s*(?:C\d*(?:\s*,\s*(?:C\d*)?)*\s*(?:†(?:L\d*(?:-(?:L\d*)?)?)?)?)?",
                self.pending,
            ):
                output.append(self.flush())
        return "".join(output)

    def flush(self) -> str:
        text, self.pending = self.pending, ""
        return text
