"""Run Golden Facts through the same upload Document / ask operations as HTTP."""

import hashlib
import inspect
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass, field
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
from chat_document.models import LLMCallTrace

from .checks import check_fact
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

    @property
    def passed(self) -> bool:
        return (
            bool(self.runs)
            and not self.upload_error
            and all(not run.error and all(fact.passed for fact in run.facts) for run in self.runs)
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
                    events = [event async for event in application.ask(case.question, **kwargs)]
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
                        FactResult(fact.id, fact.method, False, f"Application failure: {run.error}")
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
                run.calls = gateway.calls[call_start:].copy()
                run.latency_ms = (perf_counter() - started) * 1000
                report.runs.append(run)
    return report
