"""Reproduce the authorized generic-table Q3/held-out measurement from the repo root.

Run with: uv run python -m scripts.measure_table_reading
Move the fixed output reports first; historical measurement evidence is never overwritten.
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.events import FinalEvent, PlanEvent, TraceEvent
from chat_document.llm_adapter import OllamaLLM
from eval.golden_facts import LIGHTRAG_CASES
from eval.provenance import repository_state
from eval.report import write_report
from eval.runner import RecordingGateway, run_evaluation


async def main():
    outputs = [
        Path("eval/reports") / name
        for name in ("table-reconstruction-q3-generic-n3.md", "table-reconstruction-heldout.md")
    ]
    if any(path.exists() for path in outputs):
        raise FileExistsError("Move existing measurement reports before reproducing this run.")
    gateway = RecordingGateway(OllamaLLM())
    application = Application(OllamaEmbedder(), gateway)
    revision, dirty = repository_state()
    report = await run_evaluation(
        application,
        gateway,
        Path("data/lightrag.pdf"),
        tuple(c for c in LIGHTRAG_CASES if c.id == "Q3"),
        repeats=3,
        metadata={
            "Label": "table-reconstruction-generic-followup",
            "Revision": revision,
            "Uncommitted changes": dirty,
            "LLM": "gpt-oss:120b-cloud",
            "Embedder": "bge-m3",
            "Execution": "Application operations; generic table-reading rules; Levi #4532",
        },
        progress=lambda value: print(value, flush=True),
    )
    write_report(report, Path("eval/reports/table-reconstruction-q3-generic-n3.md"))
    # Same Application/Gateway and source Document; no Golden Facts values in this question.
    question = (
        "In Table 1's Legal dataset, compare HyDE and LightRAG on Diversity and Empowerment. "
        "State both win rates for each metric."
    )
    print("Held-out Table 1 question", flush=True)
    events = [e async for e in application.ask(question, history=[])]
    final = next((e for e in events if isinstance(e, FinalEvent)), None)
    plan = next((e for e in events if isinstance(e, PlanEvent)), None)
    trace = next((e for e in events if isinstance(e, TraceEvent)), None)
    source_rows = (
        {
            citation.id: application.source(citation.source_id).model_dump()
            for citation in final.citations
        }
        if final
        else {}
    )
    result = {
        "question": question,
        "answer": final.answer if final else "",
        "plan": plan.model_dump() if plan else None,
        "trace": trace.model_dump() if trace else None,
        "citations": [c.model_dump() for c in final.citations] if final else [],
        "sources": source_rows,
        "errors": [e.model_dump() for e in events if e.type == "error"],
    }
    lines = [
        "# Held-out Table 1 reading measurement",
        "",
        f"Created: {datetime.now(UTC).isoformat()}",
        "",
        f"Revision: `{revision}`; uncommitted changes: {dirty}",
        "",
        "Same Application/Gateway session as the authorized follow-up Q3 N=3 evaluation.",
        "Question selected outside Golden Facts. No reference answer or numeric hints supplied.",
        "",
        f"Question: {question}",
        "",
        "## Finalized answer",
        "",
        result["answer"],
        "",
        "## Plan, Trace, Citations and original sources",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    Path("eval/reports/table-reconstruction-heldout.md").write_text("\n".join(lines))
    print("Q3 Golden Facts overall:", report.passed, flush=True)
    print("Held-out answer:", result["answer"], flush=True)


if __name__ == "__main__":
    asyncio.run(main())
