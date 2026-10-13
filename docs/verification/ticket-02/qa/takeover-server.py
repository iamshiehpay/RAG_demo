"""Temporary QA server: real bge-m3; scripted answers only for Citation/UI plumbing."""
import json
import re
from pathlib import Path
from chat_document.api import create_app
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway

class SourceScript(ScriptedLLM):
    async def stream(self, request):
        if request.call_type=='router':
            q=request.messages[-1]['content'].split('Current question: ',1)[-1].split('\n\n',1)[0]
            self.scripts.append(json.dumps({'question_type':'Lookup','standalone_question':q,'sub_queries':[]}))
        else:
            context=request.messages[-1]['content'].split('\n\nQuestion:',1)[0]
            ids=list(dict.fromkeys(re.findall(r'\[(C\d+)\]',context)))
            self.scripts.append('Independent scripted source check. '+''.join(f'[{i}]' for i in ids))
        async for frame in super().stream(request): yield frame
class RecordedEmbedder(OllamaEmbedder):
    def __init__(self): super().__init__(); self.batches=[]
    async def embed(self,texts):
        self.batches.append(len(texts)); return await super().embed(texts)
embedder=RecordedEmbedder(); llm=SourceScript([])
application=Application(embedder,LLMGateway(llm),cache=ProcessingCache(Path('/private/tmp/nova-qa02-probes/browser-cache')))
app=create_app(application)
@app.get('/qa/state')
async def state():
    return {'document':application.document.model_dump() if application.document else None,'batches':embedder.batches,'calls':len(llm.calls)}
# QA audit route must precede the production static catch-all mount.
app.router.routes.insert(0, app.router.routes.pop())
