"""Measure guarded Ollama Cloud Section Summary calls at configurable concurrency."""

import argparse
import asyncio
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from chat_document.cache import PIPELINE_VERSION
from chat_document.llm_adapter import OllamaLLM
from chat_document.summary_tree import summary_messages
from eval.provenance import repository_state
from eval.runner import RecordingGateway


async def measure(level: int, calls: int) -> dict:
    semaphore = asyncio.Semaphore(level)
    gateway = RecordingGateway(
        OllamaLLM(os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"))
    )
    active = maximum = 0

    async def summarize(index: int) -> dict:
        nonlocal active, maximum
        async with semaphore:
            active += 1
            maximum = max(maximum, active)
            start = perf_counter()
            text = ""
            try:
                evidence = (
                    "The Document studies graph indexing and dual-level retrieval. "
                    "Its evaluation compares Agriculture, CS, Legal and Mix. "
                    "Results favor the proposed approach on three datasets while Mix "
                    "slightly favors the baseline; universal superiority is not established. "
                    "Incremental updates integrate new data without rebuilding the graph."
                )
                async for event in gateway.generate(
                    "section_summary", summary_messages(evidence, 80, label="Section Summary")
                ):
                    if event.type == "delta":
                        text += event.text
                return {
                    "index": index,
                    "success": bool(text.strip()),
                    "text": text,
                    "latency_ms": (perf_counter() - start) * 1000,
                }
            except Exception as exc:
                return {
                    "index": index,
                    "success": False,
                    "error": f"{type(exc).__name__}: {exc}",
                    "latency_ms": (perf_counter() - start) * 1000,
                }
            finally:
                active -= 1

    start = perf_counter()
    results = await asyncio.gather(*(summarize(i) for i in range(1, calls + 1)))
    return {
        "concurrency": level,
        "maximum_in_flight": maximum,
        "wall_ms": (perf_counter() - start) * 1000,
        "results": results,
        "traces": [c.model_dump() for c in gateway.calls],
    }


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--levels", default="1,2,4,8")
    parser.add_argument("--calls", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    levels = [int(value) for value in args.levels.split(",")]
    if args.calls < 1 or any(level < 1 for level in levels):
        parser.error("calls and concurrency levels must be positive")
    report = {
        "created_at": datetime.now(UTC).isoformat(),
        "model": "gpt-oss:120b-cloud",
        "calls_per_level": args.calls,
        "measurements": [],
        "revision": repository_state()[0],
        "dirty": repository_state()[1],
        "pipeline_version": PIPELINE_VERSION,
        "limitation": "Short synthetic prompts; observed client in-flight success "
        "is not a universal service ceiling.",
    }
    for level in levels:
        result = await measure(level, args.calls)
        report["measurements"].append(result)
        successes = sum(r["success"] for r in result["results"])
        print(
            f"concurrency={level}: {successes}/{args.calls} succeeded; "
            f"wall={result['wall_ms'] / 1000:.2f}s",
            flush=True,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    asyncio.run(main())
