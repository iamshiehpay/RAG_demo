"""Bounded genuine public HTTP smoke; run once, without prompt/quality tuning."""

import asyncio
import json
import tempfile
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

import httpx
import pymupdf
import uvicorn

from chat_document.api import create_app
from chat_document.application import Application
from chat_document.cache import PIPELINE_VERSION, ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import OllamaLLM
from chat_document.llm_gateway import LLMGateway

OUTPUT = Path(__file__).parent / "live"


class RecordedLLM(OllamaLLM):
    async def stream(self, request):
        record = {"request": asdict(request), "model": self.model, "frames": []}
        started = perf_counter()
        try:
            async for frame in super().stream(request):
                record["frames"].append(asdict(frame))
                yield frame
        except BaseException as exc:
            record["error"] = repr(exc)
            raise
        finally:
            record["latency_ms"] = (perf_counter() - started) * 1000
            with (OUTPUT / "provider.jsonl").open("a") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")


class RecordedEmbedder(OllamaEmbedder):
    async def embed(self, texts):
        started = perf_counter()
        vectors = await super().embed(texts)
        with (OUTPUT / "embedding.jsonl").open("a") as handle:
            handle.write(
                json.dumps(
                    {
                        "model": self.model,
                        "texts": texts,
                        "shape": list(vectors.shape),
                        "latency_ms": (perf_counter() - started) * 1000,
                    }
                )
                + "\n"
            )
        return vectors


def document():
    sections = [
        (
            "1 Motivation",
            "The Cedar pilot studies water use in a greenhouse. The purpose is "
            "to compare a timer schedule with a moisture-sensor schedule. Both schedules were "
            "tested for fourteen days under the same greenhouse conditions. The pilot measures "
            "water volume and plant height. It does not investigate outdoor farms or long-term "
            "crop yields. Each schedule used six trays with the same soil and seedlings. "
            "The team recorded irrigation volume daily and measured plant height at the end. "
            "The report is a small descriptive pilot rather than a claim about all crops. "
            "The practical motivation is reducing unnecessary irrigation while maintaining "
            "growth. The same caretaker inspected both groups each morning. Equipment failures "
            "were recorded before daily totals were calculated.",
        ),
        (
            "2 Timer Results",
            "The timer schedule delivered 42 liters of water across its six "
            "trays during the fourteen-day pilot. Mean final plant height was 18 centimeters. "
            "The timer ran at fixed intervals independent of soil moisture. Daily records showed "
            "that some irrigation occurred while the soil was already moist. No timer failures "
            "were reported during the observation period. These measurements describe the "
            "timer group only. Water volume includes all irrigation during the pilot and is "
            "not a per-tray quantity. Height is a group mean measured at the end. The report "
            "does not provide variance estimates or a significance test. Future tests should "
            "include different soils, larger groups and longer observation periods.",
        ),
        (
            "3 Sensor Results",
            "The sensor schedule delivered 30 liters of water across its six "
            "trays during the fourteen-day pilot. Mean final plant height was 19 centimeters. "
            "The sensor activated irrigation when measured moisture fell below the configured "
            "threshold. One loose cable was repaired before the first day of measurement. "
            "No failures occurred during the recorded period. The pilot therefore observed "
            "lower total water volume with the sensor schedule, alongside a similar final "
            "plant height. The report does not establish causality or long-term crop yield. "
            "The conclusion recommends a larger controlled trial before changing greenhouse "
            "practice. Threshold calibration and sensor maintenance require further study. "
            "The authors explicitly limit these observations to the tested trays and conditions.",
        ),
    ]
    with pymupdf.open() as pdf:
        for title, body in sections:
            page = pdf.new_page()
            page.insert_text((50, 60), title, fontsize=14)
            assert page.insert_textbox(pymupdf.Rect(50, 100, 540, 700), body, fontsize=11) >= 0
        return pdf.tobytes()


async def capture(client, method, path, **kwargs):
    started = perf_counter()
    events = []
    async with client.stream(method, path, **kwargs) as response:
        response.raise_for_status()
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                events.append(
                    {"elapsed_ms": (perf_counter() - started) * 1000, "event": json.loads(line[6:])}
                )
    return events


async def main():
    OUTPUT.mkdir(exist_ok=True)
    assert not (OUTPUT / "provider.jsonl").exists(), "Do not silently repeat live calls"
    with tempfile.TemporaryDirectory(prefix="rag-ticket14-smoke-") as cache:
        application = Application(
            RecordedEmbedder(), LLMGateway(RecordedLLM()), cache=ProcessingCache(Path(cache))
        )
        server = uvicorn.Server(
            uvicorn.Config(
                create_app(application), host="127.0.0.1", port=8340, log_level="warning"
            )
        )
        serving = asyncio.create_task(server.serve())
        try:
            while not server.started:
                if serving.done():
                    serving.result()
                await asyncio.sleep(0.01)
            async with httpx.AsyncClient(base_url="http://127.0.0.1:8340", timeout=240) as client:
                pdf = document()
                upload = await client.post(
                    "/api/documents",
                    files={"document": ("cedar-pilot.pdf", pdf, "application/pdf")},
                )
                upload.raise_for_status()
                ingestion = await capture(client, "GET", upload.json()["events_url"])
                (OUTPUT / "upload.json").write_text(json.dumps(ingestion, indent=2))
                assert ingestion[-1]["event"]["type"] == "ready", ingestion[-1]
                questions = [
                    "Summarize the whole document in three sentences.",
                    "How much water did the timer schedule deliver?",
                    "Compare the timer and sensor schedules in water use and plant height.",
                ]
                asks = []
                for question in questions:
                    events = await capture(client, "POST", "/api/ask", json={"question": question})
                    asks.append({"question": question, "events": events})
                    (OUTPUT / "asks.json").write_text(
                        json.dumps(asks, ensure_ascii=False, indent=2)
                    )
                    assert any(e["event"]["type"] == "final" for e in events), events[-1]
                reupload = await client.post(
                    "/api/documents",
                    files={"document": ("cedar-pilot.pdf", pdf, "application/pdf")},
                )
                reupload.raise_for_status()
                replay = await capture(client, "GET", reupload.json()["events_url"])
                (OUTPUT / "reupload.json").write_text(json.dumps(replay, indent=2))
                assert [e["event"]["type"] for e in replay] == ["ready"]
                (OUTPUT / "manifest.json").write_text(
                    json.dumps(
                        {
                            "pipeline_version": PIPELINE_VERSION,
                            "port": 8340,
                            "document": "authored three-page Cedar pilot",
                            "settings": application.settings.model_dump(),
                            "history_after_reupload": [t.model_dump() for t in application.history],
                            "scope": (
                                "genuine Ollama/bge upload, three ask paths, "
                                "own-key cache replay; no N3"
                            ),
                        },
                        indent=2,
                    )
                )
        finally:
            server.should_exit = True
            await serving
            await application.close()


if __name__ == "__main__":
    asyncio.run(main())
