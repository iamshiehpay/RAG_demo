"""Pinned non-RAG Document and independent primary-source Golden Facts.

The public March 2026 version postdates original gpt-oss weights released in
August 2025. Exact weights of the opaque Ollama cloud tag are not established.
These answer expectations are eval-only and never enter production prompts.
"""

from pathlib import Path

from .models import EvaluationCase, GoldenFact, NumericBinding

DOCUMENT = Path("data/industrial-robotics.pdf")
DOCUMENT_SHA256 = "8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9"
DOCUMENT_URL = "https://arxiv.org/pdf/2603.06749v1"

SECOND_DOCUMENT_CASES = (
    EvaluationCase(
        "SECOND_NUMBER",
        "How many model papers were manually annotated for expert validation? In that comparison, "
        "how does InfoFound affect overall accuracy "
        "and positive-class F1 relative to All? Include the evaluation counts for both settings.",
        (
            GoldenFact(
                "expert_agreement",
                "judge",
                "Table 9, physical PDF p.31: expert-validation All has N=447, overall "
                "accuracy 0.966; InfoFound has N=304, accuracy 0.951 (lower). Positive-class "
                "F1 remains 0.762 in both. These counts are criterion evaluations of the "
                "three expert-annotated papers, not the full model corpus. Bind setting, "
                "subset, metric, value and comparison direction correctly.",
                (
                    ("All",),
                    ("three", "3"),
                    ("papers", "paper", "models", "model"),
                    ("InfoFound",),
                    ("accuracy", "Acy"),
                    ("F1",),
                    ("447",),
                    ("304",),
                    ("0.966",),
                    ("0.951",),
                    ("0.762",),
                ),
                value_bindings=(
                    NumericBinding(("All",), "0.966"),
                    NumericBinding(("InfoFound",), "0.951"),
                ),
            ),
            GoldenFact(
                "no_filter_improvement",
                "forbidden",
                "The InfoFound filter increases expert-validation overall accuracy or "
                "positive-class F1 relative to All. Only an explicit affirmative claim "
                "is forbidden; negating this claim is correct.",
            ),
        ),
        "Synthesis",
        required_citation_page=31,
        required_citation_term="Table 9",
    ),
    EvaluationCase(
        "SECOND_SUMMARY",
        "Summarize the whole document's motivation, assessment method, main findings "
        "and limitations. Explain how unreported model capabilities affect the assessment "
        "and the scope of expert validation, "
        "and give the purpose of each appendix.",
        (
            GoldenFact(
                "whole_document_coverage",
                "judge",
                "Covers industrial robot-control deployment constraints motivating a "
                "readiness framework; literature/robotics and hardware assessment; "
                "eleven implications and 149 criteria used to assess 324 models; "
                "conservative evidence-based evaluation checked against experts; "
                "limited/uneven maturity and gaps in integrated safety, real-time "
                "performance, perception/interaction or deployment stacks; limitations "
                "of missing reported evidence and the small expert-validation subset. "
                "Appendices provide related surveys, search queries, the full criteria "
                "catalogue and model-level results. Does not claim a model is universally "
                "production-ready. Motivation, method, findings and limitations must "
                "all be supported by verbatim excerpts from the answer.",
            ),
        ),
        "Global",
    ),
)
