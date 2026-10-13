import asyncio,json,sys,tempfile
from pathlib import Path
sys.path.insert(0,'/Users/shiehpay/Desktop/resume/rag')
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from tests.integration.fixtures import text_pdf
class Recorder(OllamaEmbedder):
 def __init__(self):super().__init__();self.calls=[]
 async def embed(self,texts):self.calls.append(len(texts));return await super().embed(texts)
async def main():
 results=[]; original=text_pdf('Independent QA content: rabbits eat grass.'); changed=text_pdf('Independent QA content: turtles eat lettuce.')
 with tempfile.TemporaryDirectory(prefix='nova-qa04-independent-',dir='/private/tmp') as d:
  for version,content,name,expected in [('A',original,'first.pdf',True),('A',original,'renamed.pdf',False),('B',original,'version.pdf',True),('B',changed,'content.pdf',True)]:
   e=Recorder();l=ScriptedLLM([]);a=Application(e,LLMGateway(l),cache=ProcessingCache(Path(d),pipeline_version=version))
   events=[x.model_dump() async for x in a.upload_document(content,name)]
   assert events[-1]['type']=='ready';assert bool(e.calls)==expected;assert len(l.calls)==0
   if not expected: assert [x['type'] for x in events]==['ready']
   assert sum(x['type'] in ('ready','error') for x in events)==1
   results.append({'version':version,'name':name,'events':events,'embedding_batches':e.calls,'llm_calls':len(l.calls),'cache_records':len(list(Path(d).glob('*.json'))),'result':'PASS'})
   await a.close()
 Path('docs/verification/ticket-04/qa/takeover-independent-cache.json').write_text(json.dumps(results,indent=2))
asyncio.run(main())
