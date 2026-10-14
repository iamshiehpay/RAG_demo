"""Transparent real Ollama adapter recording; production requests/frames are unchanged."""

import hashlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import uvicorn

from chat_document.api import create_app
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import OllamaLLM
from chat_document.llm_gateway import LLMGateway

OUT = Path(__file__).resolve().parent
SOURCE = "cb4f1c9a164a40243a38358e59f2ed5c126bcf7c"


class RecordingOllama(OllamaLLM):
    def __init__(self):
        super().__init__()
        self.records = []

    async def stream(self, request):
        record = {
            "id": len(self.records) + 1,
            "model": self.model,
            "base_url": self.base_url,
            "call_type": request.call_type,
            "think": request.think,
            "num_predict": request.num_predict,
            "estimated_prompt_tokens": request.estimated_prompt_tokens,
            "estimated_prompt_plus_reservation": request.estimated_prompt_tokens
            + request.num_predict,
            "request_sha256": hashlib.sha256(
                json.dumps(asdict(request), ensure_ascii=False, sort_keys=True).encode()
            ).hexdigest(),
            "frames": [],
        }
        self.records.append(record)
        started = time.perf_counter()
        try:
            async for frame in super().stream(request):
                record["frames"].append(asdict(frame))
                yield frame
        except BaseException as error:
            record["error"] = str(error)
            raise
        finally:
            record["latency_ms"] = (time.perf_counter() - started) * 1000
            (OUT / "model-frames.json").write_text(
                json.dumps(
                    {"source_sha": SOURCE, "calls": self.records}, ensure_ascii=False, indent=2
                )
            )


if __name__ == "__main__":
    sys.path.insert(0, str(OUT.parents[3]))
    from tests.integration.test_tables import authored_table_pdf

    content = authored_table_pdf()
    Path("/private/tmp/nova-i09-real-smoke-input.pdf").write_bytes(content)
    (OUT / "input.json").write_text(
        json.dumps(
            {
                "source_sha": SOURCE,
                "fixture": "tests/integration/test_tables.py::authored_table_pdf() (unchanged)",
                "content_sha256": hashlib.sha256(content).hexdigest(),
                "runtime_file": "/private/tmp/nova-i09-real-smoke-input.pdf",
            },
            indent=2,
        )
    )
    application = Application(
        OllamaEmbedder(),
        LLMGateway(RecordingOllama()),
        cache=ProcessingCache(Path("/private/tmp/nova-i09-real-smoke-cache")),
    )
    uvicorn.run(create_app(application), host="127.0.0.1", port=8190)
