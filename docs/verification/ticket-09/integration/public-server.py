"""UI integration seam: real Application/Ollama embeddings, scripted external LLM only.

No routes, parser, retrieval, source data, or SSE events are replaced. This is
implementer evidence, not live-model Golden Facts or independent acceptance.
"""

import asyncio
import json
import re
import sys
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
# ruff: noqa: E402  # Fixture imports require the repository root on sys.path.

from chat_document.api import create_app
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from tests.integration.test_summary_tree import summary_pdf
from tests.integration.test_tables import authored_table_pdf

TEMP = Path("/private/tmp/nova-i09-public")
TEMP.mkdir(exist_ok=True)
(TEMP / "long-summary.pdf").write_bytes(summary_pdf(22))
(TEMP / "short-summary.pdf").write_bytes(summary_pdf(1))
(TEMP / "uncertain-table.pdf").write_bytes(authored_table_pdf(broken=True))


class ExternalLLM(ScriptedLLM):
    async def stream(self, request):
        self.calls.append(request)
        if request.call_type == "router":
            question = request.messages[-1]["content"].split("Current question: ", 1)[1]
            question = question.split("\n\n", 1)[0]
            text = json.dumps(
                {
                    "question_type": "Global"
                    if question.startswith(("Summarize", "請摘要"))
                    else "Lookup",
                    "standalone_question": question,
                    "sub_queries": [],
                }
            )
        elif request.call_type == "answer":
            prompt = "\n".join(message["content"] for message in request.messages)
            ids = sorted(set(re.findall(r"\[([CS]\d+)\]", prompt)))
            text = "\n\n".join(f"介面契約檢查：來源內容由公開端點提供。 [{id}]" for id in ids)
        else:
            text = {
                "section_summary": "Detailed finding. " * 100,
                "group_summary": "Grouped finding. " * 20,
                "document_summary": "Scripted Document overview for UI contract verification.",
            }[request.call_type]
            await asyncio.sleep(0.15)
        (TEMP / "llm-call-types.json").write_text(
            json.dumps(
                [
                    {
                        "call_type": call.call_type,
                        "think": call.think,
                        "num_predict": call.num_predict,
                    }
                    for call in self.calls
                ],
                indent=2,
            )
        )
        async for frame in ScriptedLLM([text]).stream(request):
            yield frame


if __name__ == "__main__":
    application = Application(
        OllamaEmbedder(),
        LLMGateway(ExternalLLM([])),
        cache=ProcessingCache(TEMP / "cache"),
    )
    uvicorn.run(create_app(application), host="127.0.0.1", port=8190)
