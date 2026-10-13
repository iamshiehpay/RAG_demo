import asyncio,json
from pathlib import Path
import pymupdf
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import OllamaLLM
from eval.runner import RecordingGateway

async def main():
    with pymupdf.open() as pdf:
        page=pdf.new_page()
        page.insert_text((72,50),'1 Inspection campaign measurements',fontsize=14)
        for label,y,row in [('Table 7: Shoreline campaign measurements.',85,('shoreline','37','0.42')),('Table 8: Inland campaign measurements.',200,('inland','59','0.73'))]:
            page.insert_text((72,y),label,fontsize=10)
            for x,text in zip([72,250,380],['Campaign','Samples','Mean residual (mm)']):page.insert_text((x,y+25),text,fontsize=10)
            for x,text in zip([72,250,380],row):page.insert_text((x,y+45),text,fontsize=10)
        context='''The inspection report describes two separate field campaigns. Each table identifies its population, sample count and the mean residual measured in millimetres. The shoreline and inland campaigns use the same reporting method but represent different observations, so their values must not be exchanged. Operators record the observations before calculating the residual. A supervisor checks the logs and keeps the individual measurements available for later verification. The report presents local measurements rather than a universal assessment of every inspection site. An omitted manufacturing detail is outside the scope of this report. The table captions distinguish the two observation populations and the column headings identify the units. These measurements are illustrative field observations and do not determine future campaign results.'''
        assert page.insert_textbox(pymupdf.Rect(72,300,523,770),context,fontsize=11)>=0
        content=pdf.tobytes()
    gateway=RecordingGateway(OllamaLLM())
    app=Application(OllamaEmbedder(),gateway,cache=ProcessingCache(Path('/private/tmp/nova-i11-numeric-cache')))
    report={'label':'unrelated numeric adjacent-table native smoke N1; not universal grounding proof','question':"What are the shoreline campaign's sample count and mean residual?",'effective_settings':app.settings.model_dump(),'events':[]}
    try:
        upload=[e async for e in app.upload_document(content,'Campaign-measurements.pdf')]
        report['upload_events']=[e.model_dump(mode='json') for e in upload]
        if upload[-1].type!='ready':raise RuntimeError('Held-out upload failed')
        events=[e async for e in app.ask(report['question'],history=[])]
        report['events']=[e.model_dump(mode='json') for e in events]
        final=next(e for e in events if e.type=='final')
        retrieved=next(e for e in events if e.type=='retrieval')
        report['answer']=final.answer
        used_sources={c.source_id for c in final.citations}
        report['used_original_sources']=[i.chunk.model_dump() for i in retrieved.chunks if i.chunk.id in used_sources]
        report['source_table_check']=any(i.chunk.table_label=='Table 7' and '37' in i.chunk.text and '0.42' in i.chunk.text for i in retrieved.chunks if i.chunk.id in used_sources)
    finally:
        report['calls']=[c.model_dump() for c in gateway.calls]
        await app.close()
        Path('docs/verification/ticket-11/corrected-heldout-numeric.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
asyncio.run(main())
