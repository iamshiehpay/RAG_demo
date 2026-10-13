"""Independent acceptance at frozen e59e096; real PDF/embedding, public App seams."""
import asyncio
import hashlib
import json
import re
from pathlib import Path
import pymupdf
from chat_document.application import Application
from chat_document.cache import ProcessingCache, PIPELINE_VERSION
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

OUT = Path('docs/verification/ticket-02/qa')
TMP = Path('/private/tmp/nova-qa02-probes')
TMP.mkdir(parents=True, exist_ok=True)
ORIGINAL = Path('/private/tmp/claude-501/-Users-shiehpay-Desktop-resume-rag/44a7f6f1-f8d4-42b7-b00e-717c58dfdaa7/scratchpad/qa02/pdfs/qa-chinese.pdf')
results = []
class RecordingEmbedder(OllamaEmbedder):
    def __init__(self):
        super().__init__(); self.batches=[]
    async def embed(self, texts):
        self.batches.append(len(texts)); return await super().embed(texts)

def generated(name, pages, *, cjk=False, heading=True, boxes=None):
    with pymupdf.open() as pdf:
        for n, text in enumerate(pages):
            p=pdf.new_page(width=600,height=850)
            if heading and n==0: p.insert_text((55,40),'1 Observations',fontsize=15)
            box = boxes[n] if boxes else (55,80 if n==0 else 55,545,800)
            assert p.insert_textbox(pymupdf.Rect(*box),text,fontname='china-t' if cjk else 'helv',fontsize=10)>=0
        content=pdf.tobytes()
    (TMP/name).write_bytes(content); return content

def router(q): return json.dumps({'question_type':'Lookup','standalone_question':q,'sub_queries':[]})

async def upload(name, content, *, target=500, cache=None, scripts=None):
    emb=RecordingEmbedder(); llm=ScriptedLLM(scripts or [])
    app=Application(emb,LLMGateway(llm),chunk_token_target=target,cache=cache)
    events=[e.model_dump() async for e in app.upload_document(content,name)]
    assert events[-1]['type']=='ready', (name,events)
    d=app.document
    for c in d.chunks:
        s=next(s for s in d.sections if s.id==c.section_id)
        assert c.section==s.title and s.title in c.context
        assert s.page_start<=c.page_start<=c.page_end<=s.page_end
        assert count_tokens(c.text)<=target
    results.append({'case':name,'events':events,'embedding_batches':emb.batches,'document':d.model_dump()})
    return app, emb, llm

async def main():
    lr=Path('data/lightrag.pdf').read_bytes()
    app,_,_=await upload('lightrag.pdf',lr)
    d=app.document
    titles={s.title for s in d.sections}
    expected={'1 INTRODUCTION','2 RETRIEVAL-AUGMENTED GENERATION','3 THE LIGHTRAG ARCHITECTURE','4 EVALUATION','5 RELATED WORK','6 CONCLUSION','7 APPENDIX'}
    assert expected<=titles
    assert not any(11<=c.page_start<=12 or 11<=c.page_end<=12 for c in d.chunks)
    assert 'Rag-ex: A generic' not in '\n'.join(c.text for c in d.chunks)
    assert all(s.is_appendix for s in d.sections if s.page_start>=13)
    checks=[]
    for prefix,needle,pages in [('4.2','we draw the following conclusions',(6,6)),('4.4','combines in-depth',(8,8)),('4.5','',(9,10)),('Appendix — 7.2','',(13,14))]:
        s=next(s for s in d.sections if s.title.startswith(prefix))
        pairs=[(p,pg) for p,pg in zip(s.paragraphs,s.paragraph_pages) if (needle in p if needle else pg==pages)]
        assert pairs and any(pg==pages for _,pg in pairs)
        if needle: assert all('Table 1:' not in p and 'Table 3:' not in p for p,_ in pairs)
        checks.append({'section':s.title,'paragraphs':pairs})
    results.append({'case':'LightRAG provenance','checks':checks})
    await app.close()
    # Original archived QA stimulus, verified rather than reconstructed.
    zh=ORIGINAL.read_bytes(); assert hashlib.sha256(zh).hexdigest()=='5e6db1bb64b839cfceb2414e86c96e5ea2ac6647d22d35adf9c0e4774e0510d8'
    cache=ProcessingCache(TMP/'cache')
    a,ea,la=await upload('original160.pdf',zh,cache=cache)
    b,eb,lb=await upload('renamed160.pdf',zh,cache=cache)
    assert a.document.sections==b.document.sections and a.document.chunks==b.document.chunks
    assert eb.batches==[] and not la.calls and not lb.calls
    assert results[-1]['events'][0]['type']=='ready' and len(results[-1]['events'])==1
    source='\n\n'.join(p for s in b.document.sections for p in s.paragraphs)
    compact=''.join(c.text.replace('\n','') for c in b.document.chunks)
    assert all(f'區域{n}中達到{n*3+7}個單位' in source for n in range(1,161))
    assert all(f'第{n}項觀察顯示，月球玄武岩的鐵含量在區域{n}中達到{n*3+7}個單位。' in compact for n in range(1,161))
    assert all(c.text.rstrip().endswith('。') for c in b.document.chunks)
    overlaps=[]
    for left,right in zip(b.document.chunks,b.document.chunks[1:]):
        shared=max((i for i in range(1,min(len(left.text),len(right.text))+1) if left.text[-i:]==right.text[:i]),default=0)
        overlaps.append(count_tokens(left.text[-shared:]) if shared else 0)
    assert all(0<n<=60 for n in overlaps[:-1])
    assert '短段落' in b.document.chunks[-1].text
    results.append({'case':'original160 assertions','hash':hashlib.sha256(zh).hexdigest(),'facts':160,'chunks':len(b.document.chunks),'overlap_tokens':overlaps,'pipeline':PIPELINE_VERSION})
    await a.close(); await b.close()
    # Independently varied labelled and numeric-only rows.
    for name,text in [('labels.pdf','測站甲 17.25\n測站乙 39.75\n測站丙 4.5'),('numbers.pdf','2026\n2027\n2030'),('labels-short.pdf','月球甲 11.2\n月球乙 15.4\n月 2')]:
        app,_,_=await upload(name,generated(name,[text],cjk=True))
        src='\n\n'.join(p for s in app.document.sections for p in s.paragraphs)
        assert text in src,(name,src)
        await app.close()
    # Measured body width in asymmetric single and right column: new geometry.
    for name,width,start,chars in [('asymmetric.pdf',390,65,156),('right-column.pdf',220,330,88)]:
        text=('玄武岩測量數據'*30)[:chars-1]+'。'
        content=generated(name,[text],cjk=True,boxes=[(start,80,start+width+1,800)])
        app,_,_=await upload(name,content)
        assert ''.join(p for s in app.document.sections for p in s.paragraphs)==text
        await app.close()
    # Page-leading caption/header must remain separate even with same typography.
    for name,top,cjk in [('table-negative.pdf','Table 7: Independent measurements',False),('figure-negative.pdf','Figure 8: Instrument diagram',False),('header-negative.pdf','月球期刊 第十二卷',True)]:
        first='本次觀察記錄'*12 if cjk else 'The independent comparison remains unfinished'
        second='實驗數據持續測量。' if cjk else 'and the instrument continues measuring.'
        content=generated(name,[first,top+'\n'+second],cjk=cjk)
        app,_,_=await upload(name,content)
        paragraphs=[p for s in app.document.sections for p in s.paragraphs]
        assert all(not(first in p and top in p) for p in paragraphs)
        assert any(top in p for p in paragraphs)
        await app.close()
    # Genuine same-column English/CJK continuation, source and chunk provenance.
    for name,first,second,cjk in [('english-pages.pdf','The independent sensor measured','an iron level of 19 units.',False),('chinese-pages.pdf','實驗觀察記錄'*12,'後續量測值為十九個單位。',True)]:
        content=generated(name,[first,second],cjk=cjk)
        app,_,_=await upload(name,content)
        expected=first+('' if cjk else '\n')+second
        s=app.document.sections[0]
        matching=[i for i,p in enumerate(s.paragraphs) if p.replace('\n','')==expected.replace('\n','')]
        assert matching,(name,s.paragraphs)
        assert s.paragraph_pages[matching[0]]==(1,2)
        assert any(c.page_start==1 and c.page_end==2 for c in app.document.chunks)
        await app.close()
    # Mixed punctuation and config probes; independent long paragraph.
    text=''.join(f'樣本{i}！測量是否可信？Sample {i} records {i+71} units. ' for i in range(1,91))
    with pymupdf.open() as pdf:
        p=pdf.new_page(width=1100,height=9000); p.insert_text((60,40),'1 Mixed',fontsize=15)
        assert p.insert_textbox(pymupdf.Rect(60,70,1040,8900),text,fontname='china-t',fontsize=10)>=0
        mixed=pdf.tobytes(); (TMP/'mixed.pdf').write_bytes(mixed)
    sizes=[]
    for target in [256,500,800]:
        app,_,_=await upload(f'mixed-{target}.pdf',mixed,target=target)
        assert all(re.search(r'[。！？.!?]$',c.text.rstrip()) for c in app.document.chunks)
        sizes.append(len(app.document.chunks)); await app.close()
    assert sizes[0]>sizes[1]>sizes[2]
    # No heading, error and recovery at app seam; script answer tests plumbing only.
    plain=generated('noheadings.pdf',['Independent quasar observation number 73 is 144 units. '*90]*2,heading=False)
    q='What is observation number 73?'
    app,_,llm=await upload('noheadings.pdf',plain,scripts=[router(q),'Observation 73 is 144 units. [C1]',router(q),'Observation 73 remains 144 units. [C1]'])
    assert all(s.is_virtual for s in app.document.sections)
    for _ in range(2):
        ev=[e.model_dump() async for e in app.ask(q)]
        assert [e['type'] for e in ev][-2:]==['final','trace']
        final=next(e for e in ev if e['type']=='final')
        assert final['citations']; citation=final['citations'][0]; src=app.source(citation['source_id'])
        assert (src.page_start,src.page_end)==(citation['page_start'],citation['page_end'])
        results.append({'case':'noheading ask','events':ev})
    assert len(llm.calls)==4
    await app.close()
    with pymupdf.open() as pdf:
        p=pdf.new_page(); pm=pymupdf.Pixmap(pymupdf.csRGB,pymupdf.IRect(0,0,25,25),False); pm.clear_with(127); p.insert_image(pymupdf.Rect(40,40,540,750),pixmap=pm); scan=pdf.tobytes()
    (TMP/'scan.pdf').write_bytes(scan); (TMP/'notpdf.pdf').write_bytes(b'independent invalid content'); (TMP/'corrupt.pdf').write_bytes(lr[:len(lr)//2])
    for name,data,needle in [('scan.pdf',scan,'no text layer'),('notpdf.pdf',b'independent invalid content','valid PDF'),('corrupt.pdf',lr[:len(lr)//2],'damaged')]:
        app=Application(RecordingEmbedder(),LLMGateway(ScriptedLLM([])))
        ev=[e.model_dump() async for e in app.upload_document(data,name)]
        assert ev[-1]['type']=='error' and needle in ev[-1]['message'] and not app.embedder.batches
        recovered=[e.model_dump() async for e in app.upload_document(plain,'recovered.pdf')]
        assert recovered[-1]['type']=='ready'
        results.append({'case':name,'error':ev,'recovery':recovered})
        await app.close()
    (OUT/'takeover-independent.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print('PASS independent scenarios:',len(results),'mixed chunk counts:',sizes)

if __name__=='__main__':
    try: asyncio.run(main())
    finally:
        (OUT/'takeover-independent-partial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
