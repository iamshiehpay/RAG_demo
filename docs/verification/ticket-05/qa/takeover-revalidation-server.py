"""QA05 final-UI harness: real application/bge-m3/guard, scripted external text only."""
import asyncio, importlib.util, json
from pathlib import Path
import uvicorn
spec=importlib.util.spec_from_file_location('qa05_original',Path(__file__).with_name('takeover-probe.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
from chat_document.application import Application
from chat_document.api import create_app
from chat_document.llm_gateway import LLMGateway
from chat_document.llm_adapter import ScriptedLLM

SHA='3432aa09ee7d9fcbdc9199ff9f0ee685961102e3'
ROOT=Path('/private/tmp/nova-qa05-revalidation');ROOT.mkdir(exist_ok=True)
(ROOT/'ordinary.pdf').write_bytes(h.document(n=18,repeats=15))
(ROOT/'replacement.pdf').write_bytes(h.document(n=1,repeats=5))
class States(h.QAResponses):
    async def stream(self,r):
        if r.call_type=='document_summary':
            await asyncio.sleep(.7)
            body='\n\n'.join(f'Overview paragraph {i}: calibrated instruments measure seasonal rainfall; supplied Section evidence remains available for source verification.' for i in range(1,49))+'\n\nEND_OF_DOCUMENT_OVERVIEW'
            coverage='MULTI_SECTION_OVERVIEW' if 'Group Summary' in r.messages[-1]['content'] else 'SINGLE_SECTION_OVERVIEW'
            self.scripts.append(coverage+'\n\n'+body)
            async for frame in ScriptedLLM.stream(self,r):yield frame
        else:
            async for frame in super().stream(r):yield frame
class ObservedApplication(Application):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.upload_records=[]
    async def upload_events(self,job):
        async for e in super().upload_events(job):
            self.upload_records.append(e.model_dump());yield e
llm=States(wide=True,delay=.7)
application=ObservedApplication(h.CountingEmbedder(),LLMGateway(llm))
web=create_app(application)
@web.get('/qa05-state')
async def state():
    return dict(sha=SHA,semantics='scripted external outputs; no cloud calls',document=application.document.model_dump() if application.document else None,calls=h.ledger(llm),upload_events=application.upload_records,embedding_calls=len(application.embedder.calls))
web.router.routes.insert(0,web.router.routes.pop())
uvicorn.run(web,host='127.0.0.1',port=8270)
