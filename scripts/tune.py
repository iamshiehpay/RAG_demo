"""Issue11 bounded experiments and final N=3 through Application's existing seams.

Run from repo root with PYTHONPATH=src:. python -m scripts.tune PHASE.
Only aggregate experiment outcomes and final run artifacts are retained.
"""

import argparse
import asyncio
import json
import os
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from chat_document.application import Application
from chat_document.cache import PIPELINE_VERSION, ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.events import ErrorEvent, PlanEvent, ReadyEvent
from chat_document.llm_adapter import OllamaLLM
from chat_document.settings import RetrievalSettings
from chat_document.tokens import count_tokens
from eval.golden_facts import LIGHTRAG_CASES
from eval.provenance import repository_state
from eval.report import write_report
from eval.runner import RecordingGateway, run_evaluation
from eval.second_document import DOCUMENT, SECOND_DOCUMENT_CASES

OUT = Path("eval/reports/issue11")
EXPERIMENT_CACHE = Path(".cache/issue11-experiments")
LIGHTRAG = Path("data/lightrag.pdf")
BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")


def json_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, default=lambda v: v.model_dump()) + "\n"
    )


def provenance():
    revision, dirty = repository_state()
    return {
        "Revision": revision,
        "Uncommitted changes": dirty,
        "Pipeline version": PIPELINE_VERSION,
        "LLM": "gpt-oss:120b-cloud",
        "Embedder": "bge-m3",
        "Created": datetime.now(UTC).isoformat(),
    }


def application(settings, cache=EXPERIMENT_CACHE, *, ingestion_version=None):
    gateway = RecordingGateway(OllamaLLM(BASE_URL))
    return Application(
        OllamaEmbedder(BASE_URL),
        gateway,
        settings=settings,
        cache=ProcessingCache(
            cache, **({"pipeline_version": ingestion_version} if ingestion_version else {})
        ),
    ), gateway


def target(chunk, kind):
    text = chunk.context.casefold()
    if kind == "table2":
        return chunk.kind == "table" and chunk.table_label.casefold() == "table 2"
    if kind == "cost":
        return "610" in text and "token" in text
    return "incremental" in text and ("update" in text or "new" in text)


async def retrieval_matrix(*, controlled=False):
    results = {"provenance": provenance(), "uploads": [], "rows": []}
    previous = json.loads((OUT / "retrieval.json").read_text()) if controlled else None
    fixed_plans = (
        tuple(
            PlanEvent.model_validate(previous["uploads"][0][key]) for key in ("q2_plan", "q3_plan")
        )
        if previous
        else None
    )
    ingestion_version = previous["provenance"]["Pipeline version"] if previous else None
    output_name = "retrieval-controlled" if controlled else "retrieval"
    results["experimental_design"] = (
        "Fixed actual Router plan pair across all configurations; reuse measured original "
        "Chunks/vectors because parser/chunker/embedder and explicit Chunk targets are unchanged. "
        "Old Summary Trees are not final-cache evidence."
        if controlled
        else "Per-size actual Router plans confound across-size context comparisons."
    )
    results["ingestion_version"] = ingestion_version or PIPELINE_VERSION
    try:
        for size in (256, 500, 800):
            baseline, gateway = application(
                RetrievalSettings(chunk_token_target=size), ingestion_version=ingestion_version
            )
            started = perf_counter()
            uploaded = [
                e async for e in baseline.upload_document(LIGHTRAG.read_bytes(), LIGHTRAG.name)
            ]
            errors = [e.message for e in uploaded if isinstance(e, ErrorEvent)]
            results["uploads"].append(
                {
                    "chunk_target": size,
                    "latency_ms": (perf_counter() - started) * 1000,
                    "errors": errors,
                    "calls": gateway.calls.copy(),
                }
            )
            if not any(isinstance(e, ReadyEvent) for e in uploaded):
                await baseline.close()
                continue
            # Actual production Router produces the plans used by every comparison.
            calls = []
            if fixed_plans:
                q2, q3 = fixed_plans
            else:
                q2 = await baseline.router.plan("Compare LightRAG with GraphRAG.", [], calls)
                q3 = await baseline.router.plan(
                    "Performance of ablated versions of LightRAG.", [], calls
                )
            results["uploads"][-1].update(
                {
                    "chunk_count": len(baseline.document.chunks),
                    "q2_plan": q2.model_dump(),
                    "q3_plan": q3.model_dump(),
                    "router_calls": calls,
                }
            )
            for weight in (0, 0.1, 0.25, 0.5):
                for top in (3, 5, 7):
                    settings = RetrievalSettings(
                        chunk_token_target=size,
                        lookup_top_k=top,
                        synthesis_top_k=3 if top <= 5 else 5,
                        sub_query_top_k=2 if top <= 5 else 3,
                        bm25_weight=weight,
                    )
                    app, _ = application(settings, ingestion_version=ingestion_version)
                    replay = [
                        e async for e in app.upload_document(LIGHTRAG.read_bytes(), LIGHTRAG.name)
                    ]
                    if replay[-1].type != "ready":
                        raise RuntimeError("Experiment cache replay failed")
                    start = perf_counter()
                    lookup = await app.context_packer.retrieve(
                        app.index, q3, current_question=q3.standalone_question
                    )
                    synthesis = await app.context_packer.retrieve(
                        app.index, q2, current_question=q2.standalone_question
                    )
                    ranks = {}
                    for name, question in (
                        ("table2", q3.standalone_question),
                        (
                            "cost",
                            "How much does retrieval cost for GraphRAG compared with LightRAG?",
                        ),
                        ("update", "How are incremental updates handled when new data arrives?"),
                    ):
                        ranked = await app.index.retrieve(question, len(app.index.chunks))
                        ranks[name] = next(
                            (i for i, item in enumerate(ranked, 1) if target(item.chunk, name)),
                            None,
                        )
                    coverage = {
                        "table2": any(target(i.chunk, "table2") for i in lookup.chunks),
                        "cost": any(target(i.chunk, "cost") for i in synthesis.chunks),
                        "update": any(target(i.chunk, "update") for i in synthesis.chunks),
                    }
                    results["rows"].append(
                        {
                            "settings": settings.model_dump(),
                            "first_relevant_rank": ranks,
                            "context_coverage": coverage,
                            "mrr": sum(1 / r if r else 0 for r in ranks.values()) / 3,
                            "retrieved_sections": {
                                "lookup": [i.chunk.section for i in lookup.chunks],
                                "synthesis": [i.chunk.section for i in synthesis.chunks],
                            },
                            "context_tokens": sum(
                                count_tokens(i.chunk.context) for i in synthesis.chunks
                            ),
                            "latency_ms": (perf_counter() - start) * 1000,
                        }
                    )
                    await app.close()
            await baseline.close()
            json_write(OUT / (output_name + ".json"), results)
        if not results["rows"]:
            raise RuntimeError("No Chunk configuration uploaded successfully")

        def preference(row):
            s = row["settings"]
            # Coverage first; ties preserve the documented dense/500/5 defaults.
            distance = abs(s["chunk_token_target"] - 500) / 500 + abs(s["lookup_top_k"] - 5)
            return (sum(row["context_coverage"].values()), row["mrr"], -s["bm25_weight"], -distance)

        chosen = max(results["rows"], key=preference)
        results["selection"] = chosen["settings"]
        results["selection_reason"] = (
            "Maximize actual Router evidence coverage, then MRR; "
            "ties prefer dense and documented defaults."
        )
        json_write(OUT / (output_name + ".json"), results)
        rows = [
            "# Issue11 retrieval experiment",
            "",
            results["selection_reason"],
            "",
            "| Chunk | Lookup/Synthesis/Sub-query k | BM25 | MRR | Context coverage |",
            "|---|---|---|---|---|",
        ]
        for r in results["rows"]:
            s = r["settings"]
            rows.append(
                f"| {s['chunk_token_target']} | "
                f"{s['lookup_top_k']}/{s['synthesis_top_k']}/{s['sub_query_top_k']} | "
                f"{s['bm25_weight']} | {r['mrr']:.3f} | {r['context_coverage']} |"
            )
        rows += [
            "",
            "Selected effective settings: `" + json.dumps(results["selection"]) + "`",
            "",
            "These are retrieval measurements, not Golden Facts answer acceptance. "
            "Raw plans/settings/provenance are in retrieval.json.",
        ]
        rows += [
            "",
            results["experimental_design"],
            "Ingestion version: " + results["ingestion_version"],
        ]
        (OUT / (output_name + ".md")).write_text("\n".join(rows) + "\n")
        print("Selected:", results["selection"], flush=True)
    finally:
        json_write(OUT / (output_name + ".json"), results)


def selected_settings():
    path = OUT / "retrieval-controlled.json"
    if not path.exists():
        path = OUT / "retrieval.json"
    return (
        RetrievalSettings(**json.loads(path.read_text())["selection"])
        if path.exists()
        else RetrievalSettings.from_env()
    )


async def answer_comparison():
    outcomes = []
    for think in ("low", "medium"):
        settings = selected_settings().model_copy(update={"answer_think": think})
        app, gateway = application(settings)
        try:
            report = await run_evaluation(
                app,
                gateway,
                LIGHTRAG,
                tuple(c for c in LIGHTRAG_CASES if c.id in {"Q2", "Q3"}),
                repeats=1,
                metadata={**provenance(), "Label": "answer-think-" + think},
                progress=print,
            )
            write_report(report, OUT / ("answer-" + think + ".md"))
            outcomes.append(
                {
                    "think": think,
                    "functional_passed": report.functional_passed,
                    "fact_passes": sum(f.passed for r in report.runs for f in r.facts),
                    "facts": sum(len(r.facts) for r in report.runs),
                    "audit": report.call_audit(),
                    "latency_ms": sum(r.ask_latency_ms for r in report.runs),
                }
            )
        finally:
            await app.close()
    # Valid functional/no-length configurations first, then observed semantic rates.
    successful = [
        r
        for r in outcomes
        if r["functional_passed"] and not r["audit"]["router_answer_length_attempts"]
    ]
    if not successful:
        raise RuntimeError("Both think configurations failed functional/no-length experiment")
    best = max(successful, key=lambda r: (r["fact_passes"], r["think"] == "medium"))
    selection = selected_settings().model_copy(update={"answer_think": best["think"]})
    json_write(
        OUT / "answer-comparison.json",
        {
            "provenance": provenance(),
            "measurements": outcomes,
            "selection": selection.model_dump(),
            "limit": "One run per think; stochastic quality, not a reliable significance estimate.",
        },
    )
    print("Answer selection:", selection.model_dump(), flush=True)


async def final_run():
    path = OUT / "answer-comparison.json"
    settings = (
        RetrievalSettings(**json.loads(path.read_text())["selection"])
        if path.exists()
        else RetrievalSettings.from_env()
    )
    if settings != RetrievalSettings.from_env():
        raise RuntimeError("Chosen settings must match production defaults/env before final run")
    manifest = {"provenance": provenance(), "settings": settings.model_dump(), "documents": []}
    for name, document, cases in (
        (
            "lightrag",
            LIGHTRAG,
            tuple(
                c
                for c in LIGHTRAG_CASES
                if c.id
                in {
                    "Q1",
                    "Q2",
                    "Q3",
                    "Q1_ZH_THREE_SENTENCES",
                    "ABSENT_HOTPOT",
                    "ABSENT_LICENSE",
                    "ABSENT_GPU",
                }
            ),
        ),
        ("second", DOCUMENT, SECOND_DOCUMENT_CASES),
    ):
        app, gateway = application(settings, Path(".cache"))
        try:
            report = await run_evaluation(
                app,
                gateway,
                document,
                cases,
                repeats=3,
                metadata={
                    **provenance(),
                    "Label": "issue11-final-" + name,
                    "D05": "Report raw rates/causes; semantic defects do not block delivery.",
                },
                progress=lambda s, name=name: print(name, s, flush=True),
            )
            write_report(report, OUT / ("final-" + name + ".md"))
            json_write(OUT / ("final-" + name + ".json"), asdict(report))
            print(
                name,
                "quality",
                report.status,
                "functional",
                report.functional_passed,
                report.call_audit(),
                flush=True,
            )
            content = document.read_bytes()
            config = {
                "embedding_model": "bge-m3",
                "chunk_token_target": settings.chunk_token_target,
                "summary_model": "gpt-oss:120b-cloud",
            }
            cached = app.cache.load(content, config)
            if cached is None:
                raise RuntimeError("Ready result lacks a valid final pipeline cache")
            before = len(gateway.calls)
            replay = [e async for e in app.upload_document(content, document.name)]
            if len(gateway.calls) != before or replay[-1].type != "ready":
                raise RuntimeError("Final pipeline cache replay made model calls or failed")
            tree = cached.document.summary_tree
            manifest["documents"].append(
                {
                    "name": name,
                    "pdf_sha256": report.document_sha256,
                    "processing_config": cached.processing_config,
                    "pipeline_version": cached.pipeline_version,
                    "cache_path": str(app.cache._path(content, config)),
                    "cache_hit_model_calls": 0,
                    "cache_hit_events": [e.type for e in replay],
                    "chunk_count": len(cached.document.chunks),
                    "section_summary_tokens": sum(
                        count_tokens(s.text) for s in tree.section_summaries
                    ),
                    "group_levels": len(tree.group_levels),
                    "functional_passed": report.functional_passed,
                    "quality": report.status,
                    "audit": report.call_audit(),
                }
            )
            json_write(OUT / "cache-manifest.json", manifest)
            if not report.functional_passed:
                raise RuntimeError("Final application/hard-constraint failure; raw report retained")
        finally:
            await app.close()


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("retrieval", "retrieval-controlled", "answers", "final"))
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.phase == "retrieval-controlled":
        await retrieval_matrix(controlled=True)
        return
    await {"retrieval": retrieval_matrix, "answers": answer_comparison, "final": final_run}[
        args.phase
    ]()


if __name__ == "__main__":
    asyncio.run(main())
