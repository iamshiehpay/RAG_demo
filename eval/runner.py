"""Run Golden Facts through the same upload Document / ask operations as HTTP."""

import hashlib
import inspect
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from chat_document.application import Application
from chat_document.events import (
    DeltaEvent,
    ErrorEvent,
    FinalEvent,
    PlanEvent,
    ReadyEvent,
    TraceEvent,
)
from chat_document.llm_gateway import LLMGateway
from chat_document.models import Chunk, LLMCallTrace

from .checks import check_fact, normalize
from .models import EvaluationCase, FactResult


class RecordingGateway(LLMGateway):
    """Record all Gateway traces, including calls an operation catches or retries."""

    def __init__(self, adapter, **kwargs):
        super().__init__(adapter, **kwargs)
        self.calls: list[LLMCallTrace] = []

    async def generate(
        self, call_type, messages, **kwargs
    ) -> AsyncIterator[DeltaEvent | TraceEvent]:
        async for event in super().generate(call_type, messages, **kwargs):
            if isinstance(event, TraceEvent):
                self.calls.extend(event.calls)
            yield event


@dataclass
class QuestionRun:
    case_id: str
    repetition: int
    question: str
    answer: str = ""
    question_type: str | None = None
    expected_question_type: str | None = None
    standalone_question: str = ""
    sub_queries: list[str] = field(default_factory=list)
    facts: list[FactResult] = field(default_factory=list)
    calls: list[LLMCallTrace] = field(default_factory=list)
    error: str = ""
    latency_ms: float = 0
    ask_latency_ms: float = 0
    judge_latency_ms: float = 0


@dataclass
class EvaluationReport:
    document_name: str
    document_sha256: str
    repeats: int
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, str] = field(default_factory=dict)
    upload_calls: list[LLMCallTrace] = field(default_factory=list)
    upload_error: str = ""
    runs: list[QuestionRun] = field(default_factory=list)
    judge_probes: list[QuestionRun] = field(default_factory=list)

    @property
    def status(self) -> str:
        if any(run.error.startswith("budget_exceeded:") for run in self.runs) or any(
            fact.harness_bug for run in self.runs for fact in run.facts
        ):
            return "HARNESS_BUG"
        return "PASS" if self.passed else "FAIL"

    @property
    def passed(self) -> bool:
        return (
            bool(self.runs)
            and not self.upload_error
            and all(not run.error and all(fact.passed for fact in run.facts) for run in self.runs)
        )


def check_source_citation(
    application: Application, finals: list[FinalEvent], case: EvaluationCase
) -> FactResult:
    def matches(source: Chunk) -> bool:
        label = getattr(source, "table_label", "")
        if case.required_citation_term is not None and label:
            return normalize(case.required_citation_term) == normalize(label)
        return (
            case.required_citation_page is not None
            and source.page_start <= case.required_citation_page <= source.page_end
        ) or (
            case.required_citation_term is not None
            and normalize(case.required_citation_term) in normalize(source.context)
        )

    # #03 can add kind/table_label metadata without weakening the existing
    # untyped-Chunk fallback used by the Lookup skeleton.
    table_ids = {
        chunk.id
        for chunk in (application.document.chunks if application.document else [])
        if getattr(chunk, "kind", None) == "table" and matches(chunk)
    }
    for final in finals:
        for citation in final.citations:
            if f"[{citation.id}]" not in final.answer:
                continue
            try:
                source = application.source(citation.source_id)
            except KeyError:
                continue
            if not isinstance(source, Chunk):
                continue
            source_matches = source.id in table_ids if table_ids else matches(source)
            if source_matches:
                return FactResult(
                    "table2_citation",
                    "events",
                    True,
                    "Used Citation resolves to the required Table Chunk"
                    if table_ids
                    else "Used Citation resolves to the required source Chunk (metadata fallback)",
                    citation.id,
                )
    return FactResult(
        "table2_citation",
        "events",
        False,
        "No used Citation resolves to a Chunk on the required page "
        "or containing the required table label",
    )


async def run_evaluation(
    application: Application,
    gateway: RecordingGateway,
    document_path: Path,
    cases: tuple[EvaluationCase, ...],
    *,
    repeats: int = 1,
    metadata: dict[str, str] | None = None,
    progress: Callable[[str], None] | None = None,
) -> EvaluationReport:
    if repeats < 1:
        raise ValueError("repeats must be a positive integer")
    if not cases or len({case.id for case in cases}) != len(cases):
        raise ValueError("Provide nonempty cases with unique ids")
    content = document_path.read_bytes()
    report = EvaluationReport(
        document_path.name, hashlib.sha256(content).hexdigest(), repeats, metadata=metadata or {}
    )
    upload_start = len(gateway.calls)
    try:
        uploaded = [
            event async for event in application.upload_document(content, document_path.name)
        ]
        errors = [
            f"{event.code}: {event.message}" for event in uploaded if isinstance(event, ErrorEvent)
        ]
        if errors or not any(isinstance(event, ReadyEvent) for event in uploaded):
            report.upload_error = "; ".join(errors) or "Upload did not produce ready"
    except Exception as exc:
        report.upload_error = f"{type(exc).__name__}: {exc}"
    report.upload_calls = gateway.calls[upload_start:].copy()

    history_supported = "history" in inspect.signature(application.ask).parameters
    for case in cases:
        for repetition in range(1, repeats + 1):
            if progress:
                progress(f"{case.id} {repetition}/{repeats}")
            run = QuestionRun(
                case.id,
                repetition,
                case.question,
                expected_question_type=case.expected_question_type,
            )
            started, call_start = perf_counter(), len(gateway.calls)
            try:
                if report.upload_error:
                    run.error = report.upload_error
                else:
                    kwargs = {}
                    if history_supported:
                        from chat_document.models import ConversationTurn

                        kwargs["history"] = [
                            ConversationTurn(
                                question=case.history[i][1], answer=case.history[i + 1][1]
                            )
                            for i in range(0, len(case.history), 2)
                        ]
                    ask_started = perf_counter()
                    try:
                        events = [event async for event in application.ask(case.question, **kwargs)]
                    finally:
                        run.ask_latency_ms = (perf_counter() - ask_started) * 1000
                    for event in events:
                        if isinstance(event, PlanEvent):
                            run.question_type = event.question_type
                            run.standalone_question = event.standalone_question
                            run.sub_queries = event.sub_queries
                        elif isinstance(event, FinalEvent):
                            run.answer = event.answer
                        elif isinstance(event, ErrorEvent):
                            run.error = f"{event.code}: {event.message}"
                    finals = [event for event in events if isinstance(event, FinalEvent)]
                    if not finals and not run.error:
                        run.error = "Ask did not produce a finalized answer"
                    if case.required_citation_page is not None or case.required_citation_term:
                        run.facts.append(check_source_citation(application, finals, case))
                    if case.minimum_citation_sections:
                        sections = {c.section for final in finals for c in final.citations}
                        run.facts.append(
                            FactResult(
                                "citation_sections",
                                "events",
                                len(sections) >= case.minimum_citation_sections,
                                f"{len(sections)} distinct cited Sections; "
                                f"requires {case.minimum_citation_sections}",
                            )
                        )
                if case.expected_question_type:
                    run.facts.append(
                        FactResult(
                            "question_type",
                            "events",
                            run.question_type == case.expected_question_type,
                            f"Expected {case.expected_question_type}; actual {run.question_type}",
                        )
                    )
                if case.history:
                    run.facts.append(
                        FactResult(
                            "history_supported",
                            "events",
                            history_supported,
                            "Explicit history supported"
                            if history_supported
                            else "Lookup-only baseline has no history input",
                        )
                    )
                for fact in case.facts:
                    run.facts.append(
                        FactResult(
                            fact.id,
                            fact.method,
                            False,
                            f"Application failure: {run.error}",
                            harness_bug=run.error.startswith("budget_exceeded:"),
                        )
                        if run.error
                        else await check_fact(run.answer, fact, gateway)
                    )
            except Exception as exc:
                run.error = f"{type(exc).__name__}: {exc}"
                recorded = {fact.fact_id for fact in run.facts}
                for fact in case.facts:
                    if fact.id not in recorded:
                        run.facts.append(FactResult(fact.id, fact.method, False, run.error))
            finally:
                if run.error.startswith("budget_exceeded:"):
                    run.facts = [replace(fact, harness_bug=True) for fact in run.facts]
                run.calls = gateway.calls[call_start:].copy()
                run.latency_ms = (perf_counter() - started) * 1000
                run.judge_latency_ms = sum(
                    call.latency_ms for call in run.calls if call.call_type == "judge"
                )
                report.runs.append(run)
    return report
