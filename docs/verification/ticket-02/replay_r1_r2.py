import asyncio
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from chat_document.application import Application
from chat_document.cache import PIPELINE_VERSION, ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens


class RecordingEmbedder(OllamaEmbedder):
    def __init__(self):
        super().__init__()
        self.calls = 0

    async def embed(self, texts):
        self.calls += 1
        return await super().embed(texts)


async def main():
    source = Path(sys.argv[1])
    content = source.read_bytes()
    with TemporaryDirectory(prefix="nova-i02-cache-", dir="/private/tmp") as directory:
        cache = ProcessingCache(Path(directory))
        first_embedder, second_embedder = RecordingEmbedder(), RecordingEmbedder()
        llm = ScriptedLLM([])
        first = Application(first_embedder, LLMGateway(llm), cache=cache)
        second = Application(second_embedder, LLMGateway(llm), cache=cache)
        try:
            initial = [e async for e in first.upload_document(content, "qa-chinese.pdf")]
            replay = [e async for e in second.upload_document(content, "renamed-chinese.pdf")]
            assert initial[-1].type == "ready"
            assert [e.type for e in replay] == ["ready"]
            a, b = first.document, second.document
            assert a.sections == b.sections and a.chunks == b.chunks
            compact = "".join(c.text.replace("\n", "") for c in b.chunks)
            sentences = [
                f"第{n}項觀察顯示，月球玄武岩的鐵含量在區域{n}中達到{n * 3 + 7}個單位。"
                for n in range(1, 161)
            ]
            preserved = sum(sentence in compact for sentence in sentences)
            source_text = "\n\n".join(p for s in b.sections for p in s.paragraphs)
            source_facts = sum(
                f"區域{n}中達到{n * 3 + 7}個單位" in source_text for n in range(1, 161)
            )
            assert source_facts == 160
            endings = sum(c.text.rstrip().endswith("。") for c in b.chunks)
            assert preserved == 160 and endings == len(b.chunks)
            assert max(count_tokens(c.text) for c in b.chunks) <= 500
            assert second_embedder.calls == 0 and llm.calls == []
            assert "短段落" in b.chunks[-1].text
            record = {
                "pipeline_version": PIPELINE_VERSION,
                "fresh_embedding_calls": first_embedder.calls,
                "cache_replay_embedding_calls": second_embedder.calls,
                "cache_replay_events": [e.type for e in replay],
                "sections_equal": a.sections == b.sections,
                "chunks_equal": a.chunks == b.chunks,
                "replay_name": b.name,
                "chunks": len(b.chunks),
                "max_tokens": max(count_tokens(c.text) for c in b.chunks),
                "sentence_ending_chunks": endings,
                "numeric_facts_preserved": preserved,
                "source_facts_without_compacting": source_facts,
                "short_concluding_paragraph_retained": True,
                "llm_calls": len(llm.calls),
            }
            output = (
                Path(sys.argv[2])
                if len(sys.argv) > 2
                else Path("docs/verification/ticket-02/qa-r1-r2-cache-replay.json")
            )
            output.write_text(json.dumps(record, indent=2) + "\n")
            print(json.dumps(record, indent=2))
        finally:
            await first.close()
            await second.close()


asyncio.run(main())
