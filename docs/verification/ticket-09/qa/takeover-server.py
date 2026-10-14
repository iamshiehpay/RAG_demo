"""Independent QA observation seam; real requests and frames pass unchanged."""
import json
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
SHA = '3432aa09ee7d9fcbdc9199ff9f0ee685961102e3'

class Recording(OllamaLLM):
    def __init__(self):
        super().__init__()
        self.records = []

    async def stream(self, request):
        record = {'request': asdict(request), 'model': self.model, 'frames': []}
        self.records.append(record)
        try:
            async for frame in super().stream(request):
                record['frames'].append(asdict(frame))
                yield frame
        except BaseException as exc:
            record['error'] = str(exc)
            raise
        finally:
            (OUT / 'takeover-live-model-frames.json').write_text(json.dumps(
                {'sha': SHA, 'calls': self.records}, ensure_ascii=False, indent=2))

application = Application(OllamaEmbedder(), LLMGateway(Recording()),
    cache=ProcessingCache(Path('/private/tmp/nova-qa09-real/cache')))
uvicorn.run(create_app(application), host='127.0.0.1', port=8290)
