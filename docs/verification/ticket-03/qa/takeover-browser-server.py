import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'src'))
from chat_document.api import create_app
from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM,LLMFrame
from chat_document.llm_gateway import LLMGateway
from chat_document.cache import ProcessingCache
class CitationLLM(ScriptedLLM):
 def __init__(self):super().__init__([])
 async def stream(self,request):
  if request.call_type=='router':s='not JSON'
  else:
   content=request.messages[-1]['content']
   match=re.search(r'\[(C\d+)\][^\[]*?Table (?:2|9):',content,re.S)
   s='The source table reports the measured results. ['+(match[1] if match else 'C1')+']'
  self.scripts.append(s)
  async for f in super().stream(request):yield f
application=Application(OllamaEmbedder(),LLMGateway(CitationLLM()),cache=ProcessingCache(Path('/private/tmp/nova-qa03-cache')))
app=create_app(application)
