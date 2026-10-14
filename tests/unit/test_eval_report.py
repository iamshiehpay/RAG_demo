"""Focused regressions grouped by feature; helpers remain outside test modules."""

from eval.models import FactResult
from eval.provenance import repository_state
from eval.report import write_report
from eval.runner import EvaluationReport, QuestionRun


def test_judge_probe_failures_do_not_change_golden_facts_result(tmp_path):
    report = EvaluationReport("test.pdf", "hash", 1)
    report.runs.append(
        QuestionRun("Q", 1, "question", facts=[FactResult("fact", "judge", True, "supported")])
    )
    report.judge_probes.append(
        QuestionRun("JUDGE", 1, "probe", facts=[FactResult("probe", "judge", False, "failed")])
    )
    write_report(report, tmp_path / "report.md")
    text = (tmp_path / "report.md").read_text()
    assert report.passed
    assert "Result: PASS" in text
    assert "Judge semantic probes (excluded from Golden Facts result)" in text
    assert "JUDGE" not in text.split("## Per-fact pass rates")[1].split("## Upload LLM calls")[0]


def test_budget_failure_has_a_distinct_status_in_report(tmp_path):
    report = EvaluationReport("test.pdf", "hash", 1)
    report.runs.append(
        QuestionRun(
            "Q",
            1,
            "question",
            facts=[
                FactResult(
                    "budget",
                    "judge",
                    False,
                    "Harness/upstream bug: BudgetExceeded",
                    harness_bug=True,
                )
            ],
        )
    )
    write_report(report, tmp_path / "report.md")
    assert "Result: HARNESS_BUG" in (tmp_path / "report.md").read_text()
    assert "| HARNESS_BUG |" in (tmp_path / "report.md").read_text()


def test_zip_without_git_metadata_has_unknown_provenance(tmp_path):
    assert repository_state(tmp_path) == ("unknown", "unknown")
