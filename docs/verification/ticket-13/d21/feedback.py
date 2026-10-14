"""Public Application feedback loop; live capture or deterministic provider replay.

Replay proves orchestration only; actual classification/grounding requires live evidence.
Histories supplied with --history are counterfactual unless captured from the user.
Run with PYTHONPATH=src:. and the project's Python.
"""

import argparse
import asyncio
import json
from pathlib import Path

import numpy as np

from chat_document.application import Application
from chat_document.cache import CacheRecord, ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.index import Index
from chat_document.llm_adapter import LLMFrame, OllamaLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.models import ConversationTurn
from chat_document.policy import FIXED_REFUSALS


class CaptureLLM:
    model = "gpt-oss:120b-cloud"

    def __init__(self, records, replay=False, controlled=None):
        self.records = records
        self.replay = replay
        self.cursor = 0
        self.provider = OllamaLLM()
        self.controlled = controlled

    async def stream(self, request):
        if self.replay:
            record = self.records[self.cursor]
            self.cursor += 1
            assert record["call_type"] == request.call_type
            assert record["messages"] == request.messages, (
                "Replay prompt mismatch; semantic repair UNPROVEN"
            )
            assert record["think"] == request.think
            assert record["num_predict"] == request.num_predict
            assert record["format"] == request.format
            for frame in record["frames"]:
                yield LLMFrame(**frame)
            return
        record = {
            "call_type": request.call_type,
            "messages": request.messages,
            "format": request.format,
            "think": request.think,
            "num_predict": request.num_predict,
            "estimated_prompt_tokens": request.estimated_prompt_tokens,
            "frames": [],
        }
        self.records.append(record)
        try:
            if self.controlled and request.call_type != "answer":
                source = next(r for r in self.controlled if r["call_type"] == request.call_type)
                assert source["messages"] == request.messages, "Controlled upstream input changed"
                record["provenance"] = (
                    "recorded upstream control; not a new provider classification"
                )
                for raw in source["frames"]:
                    record["frames"].append(raw)
                    yield LLMFrame(**raw)
                return
            async for frame in self.provider.stream(request):
                record["frames"].append(vars(frame))
                yield frame
        except Exception as exc:
            record["error"] = str(exc)
            raise


class CaptureEmbedder:
    model = "bge-m3"

    def __init__(self, records, replay=False):
        self.records, self.replay, self.cursor = records, replay, 0
        self.provider = OllamaEmbedder()

    async def embed(self, texts):
        if self.replay:
            record = self.records[self.cursor]
            self.cursor += 1
            assert record["texts"] == texts
            return np.asarray(record["vectors"], dtype=np.float32)
        vectors = await self.provider.embed(texts)
        self.records.append({"texts": texts, "vectors": vectors.tolist()})
        return vectors


async def run(args):
    out = Path(args.output)
    payload = (
        json.loads(Path(args.replay).read_text())
        if args.replay
        else {
            "question": args.question,
            "history": json.loads(Path(args.history).read_text()) if args.history else [],
            "history_provenance": "counterfactual" if args.history else "none",
            "llm": [],
            "embedding": [],
        }
    )
    controlled = (
        json.loads(Path(args.controlled_upstream).read_text()) if args.controlled_upstream else None
    )
    llm = CaptureLLM(payload["llm"], bool(args.replay), controlled["llm"] if controlled else None)
    gateway = LLMGateway(llm)
    if args.preflight:
        try:
            async for event in gateway.generate(
                "router", [{"role": "user", "content": "Reply OK."}]
            ):
                print(event.model_dump_json())
        finally:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    app = Application(
        CaptureEmbedder(
            controlled["embedding"] if controlled else payload["embedding"],
            bool(args.replay or controlled),
        ),
        gateway,
        cache=ProcessingCache(Path(args.cache)),
    )
    if controlled:
        payload["embedding"] = controlled["embedding"]
        payload["upstream_provenance"] = args.controlled_upstream
    pdf = Path(args.pdf)
    config = {
        "embedding_model": "bge-m3",
        "chunk_token_target": app.chunk_token_target,
        "summary_model": llm.model,
    }
    # Never accidentally trigger an expensive fresh ingestion during diagnosis.
    if not args.frozen_document:
        assert app.cache.load(pdf.read_bytes(), config) is not None, "Compatible cache required"
    payload["events"] = []
    try:
        if args.frozen_document:
            record = CacheRecord.model_validate_json(Path(args.frozen_document).read_bytes())
            app.document = record.document
            app.index = Index(
                app.document.chunks,
                np.asarray(record.embeddings, dtype=np.float32),
                app.embedder,
                bm25_weight=app.settings.bm25_weight,
            )
            payload["document_provenance"] = {
                "mode": "frozen deployed source; no upload/Ready",
                "path": args.frozen_document,
                "pipeline_version": record.pipeline_version,
            }
        else:
            upload = [
                e.model_dump(mode="json")
                async for e in app.upload_document(pdf.read_bytes(), pdf.name)
            ]
            assert [e["type"] for e in upload] == ["ready"], upload
            payload["upload"] = upload
        async for event in app.ask(
            payload["question"], history=[ConversationTurn(**t) for t in payload["history"]]
        ):
            payload["events"].append(event.model_dump(mode="json"))
        citation_map = next(
            (e["citations"] for e in payload["events"] if e["type"] == "citation_map"), []
        )
        payload["sources"] = {
            c["id"]: app.source(c["source_id"]).model_dump(mode="json") for c in citation_map
        }
        payload["original_chunks"] = [c.model_dump(mode="json") for c in app.document.chunks]
        final = next((e for e in payload["events"] if e["type"] == "final"), None)
        plan = next((e for e in payload["events"] if e["type"] == "plan"), None)
        print(json.dumps({"plan": plan, "final": final}, ensure_ascii=False))
        assert final is not None, payload["events"][-1]
        if args.expect == "supported":
            assert final["answer"] != FIXED_REFUSALS["zh"], "Unexpected fixed refusal"
            assert final["citations"] and not final["unverified"], "Citation evidence required"
        elif args.expect == "absent":
            assert final["answer"] == FIXED_REFUSALS["zh"], "Expected exact fixed refusal"
        if args.route:
            assert plan["question_type"] == args.route, "Incorrect requested evidence scope"
    finally:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        await app.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", default="這篇論文有什麼限制？")
    parser.add_argument("--history")
    parser.add_argument("--pdf", default="data/lightrag.pdf")
    parser.add_argument("--cache", default=".cache")
    parser.add_argument(
        "--frozen-document", help="Explicit retained source fixture; not a cache/Ready claim"
    )
    parser.add_argument(
        "--controlled-upstream", help="Retained Router/embedding outputs; only answer is live"
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--replay")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--expect", choices=["supported", "absent", "capture"], default="supported")
    parser.add_argument("--route", choices=["Global", "Synthesis", "Lookup"])
    asyncio.run(run(parser.parse_args()))
