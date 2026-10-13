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
from chat_document.events import ErrorEvent, PlanEvent, ReadyEvent, RetrievalEvent
from chat_document.llm_adapter import OllamaLLM, ScriptedLLM
from chat_document.settings import RetrievalSettings
from chat_document.tokens import count_tokens
from eval.golden_facts import LIGHTRAG_CASES
from eval.provenance import repository_state
from eval.report import write_report
from eval.runner import RecordingGateway, run_evaluation
from eval.second_document import DOCUMENT, SECOND_DOCUMENT_CASES

ORIGINAL_OUT = Path("eval/reports/issue11")
OUT = ORIGINAL_OUT
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


def application(settings, cache=EXPERIMENT_CACHE, *, ingestion_version=None, adapter=None):
    gateway = RecordingGateway(adapter or OllamaLLM(BASE_URL))
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


class RetrievalReplayAdapter:
    """External LLM seam only; summaries must come from a real measured cache.

    Router output replays saved native plans. Answer/extraction output is scripted,
    never assessed as a real answer or used to claim native model accounting.
    The model field describes the reused native Summary cache, not scripted calls.
    """

    model = "gpt-oss:120b-cloud"

    def __init__(self, plans):
        self.plans = plans
        self.scripted_calls = []

    async def stream(self, request):
        if request.call_type.endswith("summary"):
            raise RuntimeError("Retrieval-only replay requires a valid measured Summary cache")
        self.scripted_calls.append(request.call_type)
        if request.call_type == "router":
            question = (
                request.messages[-1]["content"]
                .removeprefix("Current question: ")
                .split("\n\n", 1)[0]
            )
            plan = self.plans.get(question) or PlanEvent(
                question_type="Lookup", standalone_question=question, sub_queries=[]
            )
            text = json.dumps(
                {
                    key: getattr(plan, key)
                    for key in ("question_type", "standalone_question", "sub_queries")
                }
            )
        elif request.call_type == "fact_extraction":
            text = "Retrieval-only scripted placeholder. [C1]"
        else:
            text = "Not mentioned in the document."
        async for frame in ScriptedLLM([text]).stream(request):
            yield frame


async def public_retrieval(app, question):
    events = [e async for e in app.ask(question, history=[])]
    retrieval = next((e for e in events if isinstance(e, RetrievalEvent)), None)
    if retrieval is None or any(isinstance(e, ErrorEvent) for e in events):
        raise RuntimeError("Public retrieval probe failed")
    return retrieval, next(e for e in events if isinstance(e, PlanEvent))


async def retrieval_matrix(*, controlled=False):
    results = {"provenance": provenance(), "uploads": [], "rows": []}
    previous = json.loads((ORIGINAL_OUT / "retrieval.json").read_text()) if controlled else None
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
        "Public upload/ask PlanEvent and RetrievalEvent. Controlled replay uses saved native "
        "Router plans and scripted non-evaluated answers/extraction at the external adapter. "
        "Real cached PDF Chunks/vectors and local embeddings; zero native replay calls. "
        "Original source-order hits are separate from score-sorted returned-hit diagnostics; "
        "returned-hit RR is NOT full-index MRR or end-to-end answer quality. "
        "Old Summary Trees are not final-cache evidence."
    )
    results["ingestion_version"] = ingestion_version or PIPELINE_VERSION
    q2_question = "Compare LightRAG with GraphRAG."
    q3_question = "Performance of ablated versions of LightRAG."
    cost_question = "How much does retrieval cost for GraphRAG compared with LightRAG?"
    update_question = "How are incremental updates handled when new data arrives?"
    for size in (256, 500, 800):
        if fixed_plans:
            q2, q3 = fixed_plans
        else:
            baseline, native_gateway = application(RetrievalSettings(chunk_token_target=size))
            try:
                uploaded = [
                    e async for e in baseline.upload_document(LIGHTRAG.read_bytes(), LIGHTRAG.name)
                ]
                if not any(isinstance(e, ReadyEvent) for e in uploaded):
                    raise RuntimeError("Native public plan upload failed")
                _, q2 = await public_retrieval(baseline, q2_question)
                _, q3 = await public_retrieval(baseline, q3_question)
                results["uploads"].append(
                    {
                        "chunk_target": size,
                        "native_calls": [c.model_dump() for c in native_gateway.calls],
                    }
                )
            finally:
                await baseline.close()
        plans = {q2_question: q2, q3_question: q3}
        for weight in (0, 0.1, 0.25, 0.5):
            for top in (3, 5, 7):
                settings = RetrievalSettings(
                    chunk_token_target=size,
                    lookup_top_k=top,
                    synthesis_top_k=3 if top <= 5 else 5,
                    sub_query_top_k=2 if top <= 5 else 3,
                    bm25_weight=weight,
                )
                adapter = RetrievalReplayAdapter(plans)
                app, gateway = application(
                    settings, ingestion_version=ingestion_version, adapter=adapter
                )
                try:
                    start = perf_counter()
                    uploaded = [
                        e async for e in app.upload_document(LIGHTRAG.read_bytes(), LIGHTRAG.name)
                    ]
                    ready = next((e for e in uploaded if isinstance(e, ReadyEvent)), None)
                    if ready is None:
                        raise RuntimeError("Measured experiment cache replay failed")
                    probes = {}
                    observed_plans = {}
                    for label, question in (
                        ("lookup", q3_question),
                        ("synthesis", q2_question),
                        ("cost", cost_question),
                        ("update", update_question),
                    ):
                        probes[label], observed_plans[label] = await public_retrieval(app, question)
                    ranks = {}
                    score_orders = {}
                    for name, probe in (
                        ("table2", probes["lookup"]),
                        ("cost", probes["cost"]),
                        ("update", probes["update"]),
                    ):
                        ranked = sorted(
                            probe.chunks,
                            key=lambda item: (
                                -(
                                    item.ranking_score
                                    if item.ranking_score is not None
                                    else item.score
                                )
                            ),
                        )
                        ranks[name] = next(
                            (i for i, item in enumerate(ranked, 1) if target(item.chunk, name)),
                            None,
                        )
                        score_orders[name] = [item.chunk.id for item in ranked]
                    coverage = {
                        "table2": any(target(i.chunk, "table2") for i in probes["lookup"].chunks),
                        "cost": any(target(i.chunk, "cost") for i in probes["synthesis"].chunks),
                        "update": any(
                            target(i.chunk, "update") for i in probes["synthesis"].chunks
                        ),
                    }
                    results["rows"].append(
                        {
                            "settings": settings.model_dump(),
                            "first_relevant_returned_hit_rank": ranks,
                            "returned_hit_rr_mean": sum(1 / r if r else 0 for r in ranks.values())
                            / 3,
                            "context_coverage": coverage,
                            "plans": {k: v.model_dump() for k, v in observed_plans.items()},
                            "public_retrieval_events": {
                                k: v.model_dump() for k, v in probes.items()
                            },
                            "score_sorted_returned_hit_ids": score_orders,
                            "upload_ready": ready.model_dump(),
                            "scripted_call_types": adapter.scripted_calls,
                            "native_replay_calls": 0,
                            "latency_ms": (perf_counter() - start) * 1000,
                        }
                    )
                finally:
                    await app.close()
        json_write(OUT / (output_name + ".json"), results)

    def preference(row):
        values = row["settings"]
        distance = abs(values["chunk_token_target"] - 500) / 500 + abs(values["lookup_top_k"] - 5)
        return (
            sum(row["context_coverage"].values()),
            row["returned_hit_rr_mean"],
            -values["bm25_weight"],
            -distance,
        )

    chosen = max(results["rows"], key=preference)
    results["selection"] = chosen["settings"]
    results["selection_reason"] = (
        "Public context coverage, then returned-hit RR; ties retain defaults"
    )
    json_write(OUT / (output_name + ".json"), results)
    lines = [
        "# Public-event retrieval experiment",
        "",
        results["experimental_design"],
        "",
        "| Chunk | Lookup/Synthesis/Sub k | BM25 | Returned-hit RR mean | Coverage |",
        "|---|---|---|---|---|",
    ]
    for row in results["rows"]:
        values = row["settings"]
        lines.append(
            f"| {values['chunk_token_target']} | {values['lookup_top_k']}/"
            f"{values['synthesis_top_k']}/{values['sub_query_top_k']} | "
            f"{values['bm25_weight']} | {row['returned_hit_rr_mean']:.3f} | "
            f"{row['context_coverage']} |"
        )
    lines.extend(
        [
            "",
            "Selected settings: `" + json.dumps(results["selection"]) + "`",
            "",
            f"Raw public events/ordering/plans/provenance: `{output_name}.json`.",
            "",
            "This scripted retrieval-only replay does not establish native answer quality, "
            "global full-index MRR, final cache identity or universal grounding.",
        ]
    )
    (OUT / (output_name + ".md")).write_text("\n".join(lines) + "\n")
    print("selected", results["selection"], flush=True)


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
    parser.add_argument("--output", type=Path, default=ORIGINAL_OUT)
    args = parser.parse_args()
    global OUT
    OUT = args.output
    OUT.mkdir(parents=True, exist_ok=True)
    if args.phase == "retrieval-controlled":
        await retrieval_matrix(controlled=True)
        return
    await {"retrieval": retrieval_matrix, "answers": answer_comparison, "final": final_run}[
        args.phase
    ]()


if __name__ == "__main__":
    asyncio.run(main())
