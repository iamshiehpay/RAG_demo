"""Opt-in real upload/ask/judge for the pinned long non-RAG Document.

Run: pytest eval/test_second_document_live.py -m eval --eval-report PATH
Each report uses a new ingestion cache directory; answers are never cached.
"""

import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from chat_document.application import Application
from chat_document.cache import PIPELINE_VERSION, ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.events import DeltaEvent
from chat_document.llm_adapter import OllamaLLM
from chat_document.tokens import count_tokens

from .provenance import repository_state
from .report import write_report
from .runner import RecordingGateway, run_evaluation
from .second_document import DOCUMENT, DOCUMENT_SHA256, DOCUMENT_URL, SECOND_DOCUMENT_CASES

pytestmark = pytest.mark.eval


async def test_second_document_real_ingestion_and_golden_facts(pytestconfig):
    path = pytestconfig.getoption("--eval-report") or Path("eval/reports") / (
        datetime.now(UTC).strftime("second-%Y%m%dT%H%M%S%fZ") + ".md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(DOCUMENT.read_bytes()).hexdigest() == DOCUMENT_SHA256
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

    class ObservedGateway(RecordingGateway):
        async def generate(self, call_type, messages, **kwargs):
            text = ""
            try:
                async for event in super().generate(call_type, messages, **kwargs):
                    if isinstance(event, DeltaEvent):
                        text += event.text
                    yield event
            finally:
                with path.with_suffix(".responses.jsonl").open("a") as out:
                    out.write(
                        json.dumps(
                            {
                                "call_type": call_type,
                                "source_label": messages[-1]["content"].split("\n", 2)[:2],
                                "response": text,
                                "response_tokens": count_tokens(text),
                            }
                        )
                        + "\n"
                    )

    gateway = ObservedGateway(OllamaLLM(base_url))
    events_path = path.with_suffix(".events.jsonl")

    class ObservedApplication(Application):
        async def upload_document(self, content, name):
            async for event in super().upload_document(content, name):
                with events_path.open("a") as out:
                    out.write(event.model_dump_json() + "\n")
                print(event.model_dump_json(), flush=True)
                yield event

    app = ObservedApplication(
        OllamaEmbedder(base_url),
        gateway,
        cache=ProcessingCache(Path(".cache") / ("issue10-" + path.stem)),
    )
    revision, dirty = repository_state()
    try:
        report = await run_evaluation(
            app,
            gateway,
            DOCUMENT,
            tuple(
                c
                for c in SECOND_DOCUMENT_CASES
                if not pytestconfig.getoption("--eval-cases")
                or c.id in {v.strip() for v in pytestconfig.getoption("--eval-cases").split(",")}
            ),
            repeats=pytestconfig.getoption("--eval-repeats"),
            metadata={
                "Revision": revision,
                "Uncommitted changes": dirty,
                "Fixed source": DOCUMENT_URL,
                "Pipeline version": PIPELINE_VERSION,
                "LLM": "gpt-oss:120b-cloud",
                "Embedder": "bge-m3",
                "Execution": "real Application upload/ask and Gateway judges; fresh cache",
                "Training provenance": "Public v1 postdates original August 2025 gpt-oss "
                "release; exact served cloud weights remain opaque/unproven.",
            },
            progress=lambda message: print(message, flush=True),
        )
        write_report(report, path)
        document = app.document
        tree = document.summary_tree if document else None
        statistics = {
            "revision": revision,
            "dirty": dirty,
            "pipeline_version": PIPELINE_VERSION,
            "pdf_sha256": DOCUMENT_SHA256,
            "upload_error": report.upload_error,
            "section_count": len(document.sections) if document else 0,
            "chunk_count": len(document.chunks) if document else 0,
            "section_summary_tokens": sum(count_tokens(s.text) for s in tree.section_summaries)
            if tree
            else 0,
            "group_levels": len(tree.group_levels) if tree else 0,
            "groups_per_level": [len(level) for level in tree.group_levels] if tree else [],
            "visible_truncated_calls": sum(c.done_reason == "length" for c in gateway.calls),
            "sections": [
                {
                    "title": s.section,
                    "pages": [s.page_start, s.page_end],
                    "tokens": count_tokens(s.text),
                    "target": s.target_tokens,
                    "source_section_ids": s.section_ids,
                    "source_chunk_ids": s.chunk_ids,
                }
                for s in tree.section_summaries
            ]
            if tree
            else [],
            "calls": [call.model_dump() for call in gateway.calls],
        }
        path.with_suffix(".ingestion.json").write_text(json.dumps(statistics, indent=2))
        print(
            json.dumps(
                {k: v for k, v in statistics.items() if k not in {"sections", "calls"}}, indent=2
            ),
            flush=True,
        )
        if not pytestconfig.getoption("--eval-record-only"):
            # D05: report semantic/forbidden pass rates honestly; they do not
            # replace or disable functional ingestion/provenance/budget guards.
            assert not report.upload_error, f"Document processing failed; see {path}"
            assert statistics["section_summary_tokens"] > 6000, f"No >6K actual summaries: {path}"
            assert statistics["group_levels"] >= 1, f"No Group layer: {path}"
            assert all(80 <= s["tokens"] <= 500 for s in statistics["sections"]), (
                f"Section Summary length contract failed: {path}"
            )
            assert tree and {
                s.page_start for s in tree.section_summaries if s.page_start >= 71
            } == {71, 74, 77, 92}
            assert gateway.calls and all(
                c.estimated_prompt_tokens + c.num_predict <= 10000
                and c.prompt_eval_count is not None
                and c.prompt_eval_count + c.num_predict <= 10000
                and c.done_reason in {"stop", "length"}
                for c in gateway.calls
            ), f"Budget/truncation failure: {path}"
    finally:
        await app.close()
