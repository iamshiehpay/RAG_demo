import json
from pathlib import Path
import uvicorn
from chat_document.api import create_app
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import OllamaLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.events import TraceEvent

class ObservedGateway(LLMGateway):
    async def generate(self,*args,**kwargs):
        async for event in super().generate(*args,**kwargs):
            if isinstance(event,TraceEvent):
                with Path('/private/tmp/nova-qa10-run/ui-calls.jsonl').open('a') as out:
                    for c in event.calls: out.write(c.model_dump_json()+'\n')
            yield event
application=Application(OllamaEmbedder('http://localhost:11434'),ObservedGateway(OllamaLLM('http://localhost:11434')),cache=ProcessingCache(Path('/private/tmp/nova-qa10-run/cache')))
uvicorn.run(create_app(application),host='127.0.0.1',port=8300,log_level='info')
