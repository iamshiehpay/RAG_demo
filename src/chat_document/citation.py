"""Normalize and validate short Citation IDs against supplied sources."""

import re
from dataclasses import dataclass

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
    ids = set(re.findall(r"\[([CS]\d+)\]", answer))
    return [citation for citation in citations if citation.id in ids]


@dataclass(frozen=True)
class ValidatedAnswer:
    answer: str
    citations: list[Citation]
    unverified: list[str]
    invalid_citation_count: int


def validate_citations(answer: str, citations: list[Citation]) -> ValidatedAnswer:
    """D01: flag only sentences containing an invalid Citation, preserving their prose."""
    valid_ids = {citation.id for citation in citations}
    unverified = []
    invalid_count = 0
    output = []
    # Keep trailing Citation tokens with the preceding sentence. Decimal points do
    # not end a sentence; newlines also delimit unpunctuated Markdown list items.
    sentences = re.findall(
        r".+?(?:[。！？!?]|\.(?=\s|\[|$)|(?=\n)|$)(?:[ \t]*\[[CS][^\]\n]*\])*|\n",
        answer,
    )
    for sentence in sentences:
        count = 0

        def replace(match: re.Match) -> str:
            nonlocal count
            if match[1] in valid_ids:
                return match[0]
            count += 1
            return ""

        cleaned = re.sub(r"\[([CS]\d+(?:\s*[-–—]\s*[CS]\d+)?)\]", replace, sentence)
        if count:
            cleaned = re.sub(r"[ \t]+(?=[。！？!?.])", "", cleaned)
            unverified.append(cleaned.strip())
            cleaned = cleaned.rstrip() + " 未驗證"
        invalid_count += count
        output.append(cleaned)
    validated = "".join(output)
    return ValidatedAnswer(
        validated, cited_sources(validated, citations), unverified, invalid_count
    )


class CitationText:
    """Canonicalize Citation brackets without losing IDs or ordinary prose.

    Buffer only a possible Citation prefix, so tokens like 【 / C3 / 】 work
    across frames. Unknown IDs stay intact for the later Citation Validator.
    """

    def __init__(self, citations: list[Citation] | None = None):
        self.pending = ""
        self.valid_ids = {citation.id for citation in citations or []}

    def normalize(self, body: str) -> str:
        output = []
        for token in re.findall(r"[CS]\d+(?:\s*[-–—]\s*[CS]\d+)?", body):
            ids = re.findall(r"[CS]\d+", token)
            if len(ids) == 1:
                output.append(f"[{ids[0]}]")
                continue
            first, last = ids
            start, end = int(first[1:]), int(last[1:])
            # Bound expansion by the supplied map, including adversarial huge endpoints.
            if first[0] == last[0] and 0 <= end - start < len(self.valid_ids):
                expanded = [f"{first[0]}{i}" for i in range(start, end + 1)]
                if all(id in self.valid_ids for id in expanded):
                    output.extend(f"[{id}]" for id in expanded)
                    continue
            output.append(f"[{first}–{last}]")  # Validator flags this whole invalid range.
        return "".join(output)

    def feed(self, text: str) -> str:
        output = []
        for character in text:
            if not self.pending and character not in "[【［":
                output.append(character)
                continue
            self.pending += character
            complete = re.fullmatch(
                r"[\[【［]\s*([CS]\d+(?:\s*[-–—]\s*[CS]\d+)?"
                r"(?:(?:\s*,\s*|\s+)[CS]\d+(?:\s*[-–—]\s*[CS]\d+)?)*)"
                r"\s*(?:†L\d+(?:-L\d+)?)?[\]】］]",
                self.pending,
            )
            if complete:
                output.append(self.normalize(complete[1]))
                self.pending = ""
            elif not re.fullmatch(
                r"[\[【［]\s*(?:[CS][\dCS\s,–—-]*"
                r"\s*(?:†(?:L\d*(?:-(?:L\d*)?)?)?)?)?",
                self.pending,
            ):
                output.append(self.flush())
        return "".join(output)

    def flush(self) -> str:
        text, self.pending = self.pending, ""
        return text
