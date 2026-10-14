"""Independent QA harness; application operations only, scripted semantic output labelled."""
import asyncio, hashlib, json, sys, tempfile
from pathlib import Path
import numpy as np
import pymupdf
from chat_document.application import Application
from chat_document.api import create_app
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM, LLMFrame
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

OUT=Path('docs/verification/ticket-05/qa')
TMP=Path('/private/tmp/nova-qa05-batch'); TMP.mkdir(exist_ok=True)
SHA='0718466a1dae475417f61f622f796ddf77429d27'

class CountingEmbedder(OllamaEmbedder):
    def __init__(self):
        super().__init__(); self.calls=[]
    async def embed(self,texts):
        self.calls.append(texts); return await super().embed(texts)
class SupplementalEmbedder:
    model='qa05-supplemental-fixed'
    async def embed(self,texts): return np.ones((len(texts),3),dtype=np.float32)

class QAResponses(ScriptedLLM):
    model='qa05-recorded-scripted'
    def __init__(self,wide=False,progressive=False,delay=0):
        super().__init__([]); self.wide=wide; self.progressive=progressive; self.delay=delay
    async def stream(self,r):
        if self.delay: await asyncio.sleep(self.delay)
        content=r.messages[-1]['content']
        if r.call_type=='router':
            current=content.split('Current question: ',1)[-1].split('\n')[0]
            mode='Lookup' if 'lookup' in current.lower() else 'Global'
            standalone=('Summarize '+ 'detail '*490) if count_tokens(current)>900 else current
            text=json.dumps(dict(question_type=mode,standalone_question=standalone,sub_queries=[]))
        elif r.call_type=='answer':
            ref='C1' if '[C#]' in r.messages[0]['content'] else 'S1'
            text=f'The supplied Document reports calibrated measurements. [{ref}]'
            self.scripts.append([LLMFrame(content=text[:30]),LLMFrame(content=text[30:]),LLMFrame(done=True,done_reason='stop',prompt_eval_count=100,eval_count=count_tokens(text))])
            async for frame in super().stream(r): yield frame
            return
        elif r.call_type=='section_summary':
            text=('Measured finding. '*249 if self.progressive else 'Rainfall finding. '*75 if self.wide else 'Measurements use calibration and report seasonal results.')
        elif r.call_type=='group_summary': text='Grouped measurements. '*(160 if self.progressive else 20)
        else: text='Document Overview: calibrated instruments measure seasonal conditions across the supplied Sections.'
        self.scripts.append(text)
        async for frame in super().stream(r): yield frame

def document(n=2, repeats=6, parent=False, table=False):
    with pymupdf.open() as pdf:
        if parent:
            p=pdf.new_page(); p.insert_text((50,50),'1 Measurements',fontsize=16)
        for i in range(n):
            p=pdf.new_page(width=1200,height=1800)
            p.insert_text((50,50),f'{i+2 if parent else i+1} Calibration {i}',fontsize=14)
            if table and i==0:
                p.insert_text((50,90),'Table 41: Seasonal observations.',fontsize=10)
                for row,values in enumerate([['Trial','Temperature','Cost'],['alpha','12.5','3.75'],['beta','','4.75']]):
                    for x,v in zip([50,300,550],values):
                        if v:p.insert_text((x,120+row*20),v,fontsize=10)
            else:
                txt=(f'UNIQUE_{i} instrument measures seasonal rainfall with calibration error. Supplementary [S1] remains literal original text. '*repeats)
                assert p.insert_textbox(pymupdf.Rect(50,90,1150,1700),txt,fontsize=10)>=0
        return pdf.tobytes()

def tables():
    with pymupdf.open() as pdf:
        for t in range(10):
            p=pdf.new_page(width=700,height=2000)
            if t==0:p.insert_text((45,40),'1 Seasonal trials',fontsize=15)
            p.insert_text((45,80),f'Table {t+41}: Independent seasonal comparison.',fontsize=10)
            for row in range(83):
                vals=['Trial','Baseline','Variant'] if row==0 else [f'season_{t}_{row}',f'{row}.3%',f'{row}.7%']
                for x,v in zip([45,300,520],vals):p.insert_text((x,120+row*20),v,fontsize=10)
        return pdf.tobytes()

def ledger(llm):
    return [dict(type=r.call_type,think=r.think,reserve=r.num_predict,prompt=r.estimated_prompt_tokens,total=r.estimated_prompt_tokens+r.num_predict,messages=r.messages) for r in llm.calls]
def budget(llm):
    assert all(r.estimated_prompt_tokens+r.num_predict<=10000 for r in llm.calls)
def provenance(doc):
    tree=doc.summary_tree
    wanted=[c.id for c in doc.chunks]
    for level in [tree.section_summaries,*tree.group_levels,[tree.document_summary]]:
        assert [c for s in level for c in s.chunk_ids]==wanted
        assert all(doc_source_id in {s.id for s in doc.sections} for s in level for doc_source_id in s.section_ids)
    return dict(chunk_count=len(wanted),section_count=len(tree.section_summaries),group_levels=list(map(len,tree.group_levels)))
async def upload(app,data,name):
    e=[x async for x in app.upload_document(data,name)]
    assert e[-1].type=='ready',str(e[-1]); return e
async def main():
    result={'sha':SHA,'semantics':'Scripted output; proves orchestration not Cloud quality','checks':{}}
    content=document(parent=True,table=True); (TMP/'ordinary.pdf').write_bytes(content)
    embed=CountingEmbedder(); llm=QAResponses(); cache_dir=Path(tempfile.mkdtemp(prefix='nova-qa05-public-cache-',dir='/private/tmp')); cache=ProcessingCache(cache_dir)
    app=Application(embed,LLMGateway(llm),cache=cache); events=await upload(app,content,'ordinary.pdf')
    doc=app.document; inv=provenance(doc)
    assert len(doc.summary_tree.section_summaries)==2
    assert any(c.kind=='table' for c in doc.chunks)
    assert doc.sections[0].id not in [s for q in doc.summary_tree.section_summaries for s in q.section_ids]
    from chat_document.tables import LIMITATION
    assert LIMITATION in doc.summary_tree.document_summary.text
    for q in doc.summary_tree.section_summaries:
        section=next(s for s in doc.sections if s.id==q.section_ids[0])
        source='\n\n'.join(section.paragraphs+[c.text for c in doc.chunks if c.section_id==section.id and c.kind=='table'])
        assert q.target_tokens==max(80,min(500,round(count_tokens(source)*.15)))
    result['checks']['ordinary_full_source_and_target']=inv
    result['ordinary_events']=[e.model_dump() for e in events]
    # Full no-call replay using fresh counting external dependencies.
    replay_llm=QAResponses(); replay_embed=CountingEmbedder()
    replay=Application(replay_embed,LLMGateway(replay_llm),cache=cache)
    replay_events=await upload(replay,content,'ordinary.pdf')
    assert [e.type for e in replay_events]==['ready'] and not replay_llm.calls and not replay_embed.calls
    assert replay.document==doc
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in cache_dir.iterdir() if p.is_file()}
    for question in ['Summarize.','Summarize.','Lookup supplementary measurement.']:
        start=len(replay_llm.calls); ec=len(replay_embed.calls)
        asked=[e async for e in replay.ask(question,history=[])]
        assert not any(e.type=='error' for e in asked)
        final=next(e for e in asked if e.type=='final')
        assert replay.source(final.citations[0].source_id).kind in (('text','table') if 'Lookup' in question else ('section',))
        assert [c.call_type for c in replay_llm.calls[start:]]==['router','answer']
        if 'Lookup' not in question:
            assert len(replay_embed.calls)==ec
            assert next(e for e in asked if e.type=='retrieval').chunks==[]
        assert [e.type for e in asked].index('citation_map')<[e.type for e in asked].index('delta')
    assert hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in cache_dir.iterdir() if p.is_file()}
    result['checks']['cache_replay_and_fresh_answers']={'llm_replay_calls':0,'embedding_replay_calls':0,'cache_hashes':hashes}
    budget(llm);budget(replay_llm);result['ordinary_calls']=ledger(llm)+ledger(replay_llm)
    # Independent public-upload long-table defect regression.
    data=tables();(TMP/'long-tables.pdf').write_bytes(data)
    tl=QAResponses();ta=Application(CountingEmbedder(),LLMGateway(tl));te=await upload(ta,data,'long-tables.pdf')
    chunks=ta.document.chunks; assert len(ta.document.sections)==1 and len(chunks)>=10
    raw=[r for r in tl.calls if r.call_type=='section_summary' and 'Table ' in r.messages[-1]['content']]
    assert len(raw)>1
    for c in chunks:
        assert c.kind=='table' and count_tokens(c.text)<=2000
        assert sum(c.text in r.messages[-1]['content'] for r in raw)==1
        assert c.table_caption and c.table_headers and c.table_rows
    assert all('Section: '+ta.document.sections[0].title in r.messages[-1]['content'] for r in raw)
    result['checks']['long_table_whole_chunk_preservation']=provenance(ta.document)|{'raw_batches':len(raw),'tables':[dict(id=c.id,tokens=count_tokens(c.text),rows=len(c.table_rows),caption=c.table_caption,columns=c.table_headers) for c in chunks]}
    result['table_calls']=ledger(tl);budget(tl)
    # Independent boundary Document with real bge-m3.
    data=document(n=18,repeats=80);(TMP/'boundary.pdf').write_bytes(data)
    bl=QAResponses(wide=True);be=CountingEmbedder();ba=Application(be,LLMGateway(bl));await upload(ba,data,'boundary.pdf')
    pi=provenance(ba.document);assert ba.document.summary_tree.group_levels
    choices=[]
    for q in ['Summarize.','Summarize '+'detail '*996]:
        assert count_tokens(q)<=1000
        before=len(bl.calls);ec=len(be.calls)
        ev=[e async for e in ba.ask(q,history=[])]
        assert not any(e.type=='error' for e in ev)
        trace=next(e for e in ev if e.type=='trace');choices.append(trace.summary_level)
        assert len(be.calls)==ec and [c.call_type for c in bl.calls[before:]]==['router','answer']
    assert choices==['section','group:1'],choices
    result['checks']['deepest_fitting_short_exact1000']=pi|{'choices':choices,'long_question_tokens':1000}
    result['boundary_calls']=ledger(bl);budget(bl)
    # Expensive recursive edge: public upload with explicitly supplemental fixed embeddings.
    pl=QAResponses(progressive=True);pa=Application(SupplementalEmbedder(),LLMGateway(pl))
    pe=await upload(pa,document(n=48,repeats=15),'progressive-supplemental.pdf')
    pp=provenance(pa.document);assert len(pa.document.summary_tree.group_levels)>=2
    stages=[e for e in pe if e.type=='stage' and e.stage=='summary']
    assert [e.completed for e in stages]==sorted(e.completed for e in stages)
    assert all(e.completed<e.total for e in stages[:-1]) and stages[-1].completed==stages[-1].total
    result['checks']['supplemental_recursive_layers']=pp|{'progress':[[e.completed,e.total] for e in stages]}
    budget(pl);result['progressive_calls']=ledger(pl)
    (OUT/'takeover-public-probes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result['checks'],ensure_ascii=False,indent=2))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='serve':
        import uvicorn
        model=QAResponses(wide=True,delay=.8)
        application=Application(CountingEmbedder(),LLMGateway(model),cache=ProcessingCache(TMP/'browser-cache'))
        web=create_app(application)
        @web.get('/qa05-state')
        async def state():
            return dict(sha=SHA,document=application.document.model_dump() if application.document else None,calls=ledger(model),embedding_calls=len(application.embedder.calls))
        web.router.routes.insert(0, web.router.routes.pop())  # diagnostic precedes static mount
        uvicorn.run(web,host='127.0.0.1',port=8270)
    else:asyncio.run(main())
