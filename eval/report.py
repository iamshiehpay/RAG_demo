"""Markdown reports preserve per-fact results and every LLM call's measured costs."""

import html
from collections import defaultdict
from pathlib import Path

from chat_document.models import LLMCallTrace

from .runner import EvaluationReport


def cell(value) -> str:
    return html.escape(str(value)).replace("|", "\\|").replace("\n", "<br>")


def calls_table(calls: list[LLMCallTrace]) -> list[str]:
    lines = [
        "| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | "
        "num_predict | context_budget | latency_ms | done_reason |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for index, call in enumerate(calls, 1):
        values = (
            index,
            call.call_type,
            call.think,
            call.estimated_prompt_tokens,
            call.prompt_eval_count,
            call.eval_count,
            call.num_predict,
            call.context_budget,
            f"{call.latency_ms:.2f}",
            call.done_reason,
        )
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    if not calls:
        lines.append("\nNo LLM calls.")
    return lines


def write_report(report: EvaluationReport, path: Path) -> Path:
    lines = [
        "# Golden Facts evaluation",
        "",
        f"Created: {report.created_at}",
        "",
        f"Document: {cell(report.document_name)}",
        "",
        f"Document SHA-256: `{report.document_sha256}`",
        "",
        f"Repetitions per question: {report.repeats}",
        "",
        f"Result: {report.status}",
        "",
        "Router classification requires plan_source=router. Fallback plans fail "
        "with status FALLBACK, even when their Question Type matches. "
        "Follow-up checks require a changed Standalone Question resolving the case referents; "
        "language-mismatch rewrites fail. Accepting a history argument is not a pass condition.",
        "",
    ]
    for key, value in report.metadata.items():
        lines.extend([f"{cell(key)}: {cell(value)}", ""])
    if report.upload_error:
        lines.extend([f"Upload failure: {cell(report.upload_error)}", ""])
    lines.extend(
        ["## Per-fact pass rates", "", "| Case | Fact | Method | Pass rate |", "|---|---|---|---|"]
    )
    grouped = defaultdict(list)
    for run in report.runs:
        for fact in run.facts:
            grouped[(run.case_id, fact.fact_id, fact.method)].append(fact.passed and not run.error)
    for (case_id, fact_id, method), results in grouped.items():
        count = sum(results)
        lines.append(
            f"| {cell(case_id)} | {cell(fact_id)} | {cell(method)} | "
            f"{count}/{len(results)} ({count / len(results):.1%}) |"
        )
    lines.extend(["", "## Upload LLM calls", "", *calls_table(report.upload_calls), ""])
    for index, run in enumerate(report.runs + report.judge_probes):
        if index == len(report.runs):
            lines.extend(["", "## Judge semantic probes (excluded from Golden Facts result)", ""])
        lines.extend(
            [
                f"## {cell(run.case_id)} — repetition {run.repetition}",
                "",
                f"Question: {cell(run.question)}",
                "",
                f"Question Type: {run.question_type}; expected: {run.expected_question_type}",
                "",
                f"Plan source: {cell(run.plan_source)}",
                "",
                f"Fallback reason: {cell(run.fallback_reason)}",
                "",
                f"Rewrite language mismatch: {run.rewrite_language_mismatch}",
                "",
                f"Raw Router Standalone Question: {cell(run.router_standalone_question)}",
                "",
                f"Standalone Question: {cell(run.standalone_question)}",
                "",
                f"Sub-queries: {cell(run.sub_queries)}",
                "",
                f"Ask latency_ms: {run.ask_latency_ms:.2f}",
                "",
                f"Judge latency_ms: {run.judge_latency_ms:.2f}",
                "",
                f"Total evaluation latency_ms: {run.latency_ms:.2f}",
                "",
            ]
        )
        if run.error:
            label = (
                "Harness/upstream bug"
                if run.error.startswith("budget_exceeded:")
                else "Application failure"
            )
            lines.extend([f"{label}: {cell(run.error)}", ""])
        lines.extend(
            [
                "### Fact results",
                "",
                "| Fact | Method | Result | Reason | Evidence |",
                "|---|---|---|---|---|",
            ]
        )
        for fact in run.facts:
            values = (
                fact.fact_id,
                fact.method,
                fact.status,
                fact.reason,
                fact.evidence,
            )
            lines.append("| " + " | ".join(cell(value) for value in values) + " |")
        lines.extend(
            [
                "",
                "### LLM calls",
                "",
                *calls_table(run.calls),
                "",
                "### Finalized answer",
                "",
                "<pre>" + html.escape(run.answer) + "</pre>",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
