import asyncio
import json
from pathlib import Path
import pymupdf
from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens

async def main():
    Path('/private/tmp/nova-qa02-probes').mkdir(parents=True, exist_ok=True)
    records=[]
    for size in [9,14]:
        with pymupdf.open() as pdf:
            p=pdf.new_page(width=900,height=1200)
            y=65
            for title,marker in [('1 Instruments','INSTRUMENT'),('Methods','METHOD'),('References','BIBLIOGRAPHY'),('Appendix A','APPENDIX')]:
                p.insert_text((55,y),title,fontname='cobo' if title=='Methods' else 'cour',fontsize=size if title=='Methods' else size*1.4); y+=size*2.5
                for n in range(3):
                    p.insert_textbox(pymupdf.Rect(55,y,840,y+size*6),f'{marker}_{n} '+('measured independent evidence '*7)+'.',fontname='cour',fontsize=size); y+=size*6.5
            content=pdf.tobytes()
        Path(f'/private/tmp/nova-qa02-probes/structured-{size}.pdf').write_bytes(content)
        app=Application(OllamaEmbedder(),LLMGateway(ScriptedLLM([])),chunk_token_target=64)
        events=[e.model_dump() async for e in app.upload_document(content,f'structured-{size}.pdf')]
        assert events[-1]['type']=='ready'
        d=app.document
        assert [s.title for s in d.sections]==['1 Instruments','Methods','Appendix A']
        assert d.sections[-1].is_appendix
        assert 'BIBLIOGRAPHY' not in ''.join(c.text for c in d.chunks)
        for s in d.sections:
            chunks=[c for c in d.chunks if c.section_id==s.id]
            assert '\n\n'.join(c.text for c in chunks)=='\n\n'.join(s.paragraphs)
            assert all(count_tokens(c.text)<=64 for c in chunks)
            assert all(c.section==s.title for c in chunks)
        records.append({'size':size,'events':events,'document':d.model_dump()})
        await app.close()
    Path('docs/verification/ticket-02/qa/takeover-structure.json').write_text(json.dumps(records,indent=2))
    print('PASS Courier 9pt/14pt relative and same-size bold headings; whole paragraph packing; no overlap; References excluded; Appendix retained')
asyncio.run(main())
