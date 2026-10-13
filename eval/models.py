"""Definitions and results used by the Golden Facts harness."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class NumericBinding:
    variants: tuple[str, ...]
    value: str


@dataclass(frozen=True)
class GoldenFact:
    id: str
    method: Literal["contains", "judge", "forbidden"]
    requirement: str
    # Every alternative group must occur in the verbatim evidence for numeric facts.
    evidence_terms: tuple[tuple[str, ...], ...] = ()
    exact_answer: str | None = None
    answer_property: bool = False
    value_bindings: tuple[NumericBinding, ...] = ()

    def __post_init__(self):
        if self.method not in {"contains", "judge", "forbidden"}:
            raise ValueError(f"Unknown Golden Fact method: {self.method}")
        if not self.id.strip() or not self.requirement.strip():
            raise ValueError("Golden Facts require an id and requirement")
        if self.method == "contains" and any(char.isnumeric() for char in self.requirement):
            raise ValueError("contains cannot check numbers; use judge with numeric context")
        if any(not group or any(not term for term in group) for group in self.evidence_terms):
            raise ValueError("Evidence term groups must contain nonempty alternatives")


@dataclass(frozen=True)
class FactResult:
    fact_id: str
    method: str
    passed: bool
    reason: str
    evidence: str = ""
    harness_bug: bool = False
    fallback: bool = False

    @property
    def status(self) -> str:
        if self.harness_bug:
            return "HARNESS_BUG"
        if self.fallback:
            return "FALLBACK"
        return "PASS" if self.passed else "FAIL"


@dataclass(frozen=True)
class EvaluationCase:
    id: str
    question: str
    facts: tuple[GoldenFact, ...] = ()
    expected_question_type: str | None = None
    history: tuple[tuple[str, str], ...] = ()
    minimum_citation_sections: int = 0
    required_citation_page: int | None = None
    required_citation_term: str | None = None
    standalone_terms: tuple[tuple[str, ...], ...] = ()
    accepted_question_types: tuple[str, ...] = ()

    def __post_init__(self):
        if self.expected_question_type and self.accepted_question_types:
            raise ValueError("Use one fixed expected type or one declared accepted set, not both")
        if len(set(self.accepted_question_types)) != len(self.accepted_question_types) or any(
            value not in {"Global", "Lookup", "Synthesis"} for value in self.accepted_question_types
        ):
            raise ValueError("Accepted Question Types must be distinct valid routes")
