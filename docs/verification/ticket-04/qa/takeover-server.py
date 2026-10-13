import asyncio,json,sys,time
from pathlib import Path
sys.path.insert(0,'/Users/shiehpay/Desktop/resume/rag')
from chat_document.api import create_app
from chat_document.application import Application
from chat_document.cache import ProcessingCache,PIPELINE_VERSION
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from tests.integration.fixtures import text_pdf,scanned_pdf
import uvicorn,httpx
class ObservedEmbedder(OllamaEmbedder):
 def __init__(self):
  super().__init__();self.calls=[];self.permits=0;self.fail_next=False
 async def embed(self,texts):
  n=len(self.calls)+1;self.calls.append({'n':n,'size':len(texts),'entered':time.time(),'done':False})
  while n>self.permits: await asyncio.sleep(.05)
  if self.fail_next:
   self.fail_next=False;raise httpx.ConnectError('QA injected embedding disconnect')
  out=await super().embed(texts);self.calls[-1]['done']=True;return out
embedder=ObservedEmbedder()
llm=ScriptedLLM(['not JSON','QA original evidence answer. [C1]']*20)
application=Application(embedder,LLMGateway(llm),cache=ProcessingCache(Path('/private/tmp/nova-qa04-cache')))
app=create_app(application)
@app.get('/qa/stats')
async def stats():
 return {'pipeline':PIPELINE_VERSION,'embeddings':embedder.calls,'llm_calls':len(llm.calls),'history':len(application.history),'document':application.document.model_dump() if application.document else None,'active_upload':application._active_upload,'cache_files':[p.name for p in Path('/private/tmp/nova-qa04-cache').glob('*')]}
@app.post('/qa/release/{n}')
async def release(n:int): embedder.permits=n;return {'permits':n}
@app.post('/qa/fail-next')
async def fail(): embedder.fail_next=True;return {'fail_next':True}
for name,data in [('scan.pdf',scanned_pdf()),('replacement.pdf',text_pdf('GARDEN_EVIDENCE Plants need water and sunshine.')),('broken.pdf',b'not a PDF')]:
 Path('/private/tmp/nova-qa04-'+name).write_bytes(data)
from starlette.routing import Mount
mounts=[r for r in app.router.routes if isinstance(r,Mount)]
app.router.routes[:]=[r for r in app.router.routes if not isinstance(r,Mount)]+mounts
uvicorn.run(app,host='127.0.0.1',port=8180,log_level='info')
