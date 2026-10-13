import asyncio,json
from pathlib import Path
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import OllamaLLM
from chat_document.tokens import count_tokens
from eval.runner import RecordingGateway
import pymupdf

async def main():
    source='''Field calibration protocol. A coastal monitoring station uses six independent sensors. Each complete calibration takes seventeen minutes. Operators place the sensors in the same reference chamber, collect readings, and compare every channel with the reference instrument. The reference instrument records a stable baseline before the calibration starts. A supervisor reviews the individual residuals and records the final configuration. The protocol separates calibration from ordinary monitoring, so the duration does not describe continuous observation. After calibration, the station resumes normal sampling. The report describes routine validation, maintenance responsibilities and the limitations of the chamber procedure. It does not identify a manufacturer or provide procurement terms. The supervisor keeps the original observations so that a later reader can reproduce the comparison and understand the local setup. Weather forecasts and emergency procedures are outside this report's scope. Operators repeat the same preparation for each calibration, without assuming that an earlier configuration is still valid. They document interruptions and repeat incomplete measurements before declaring a run complete.'''
    with pymupdf.open() as pdf:
        page=pdf.new_page()
        remaining=page.insert_textbox(pymupdf.Rect(72,72,523,770),source,fontsize=11)
        assert remaining>=0
        content=pdf.tobytes()
    gateway=RecordingGateway(OllamaLLM())
    app=Application(OllamaEmbedder(),gateway,cache=ProcessingCache(Path('/private/tmp/nova-i11-heldout-cache')))
    results={'label':'held-out generalization smoke, not Golden Facts N3','source':source,'effective_settings':app.settings.model_dump(),'questions':[]}
    try:
        upload=[e async for e in app.upload_document(content,'field-calibration.pdf')]
        results['upload_events']=[e.model_dump() for e in upload]
        if upload[-1].type!='ready': raise RuntimeError('Held-out upload did not become Ready')
        for question in ['How many independent sensors are used, and how long is calibration?','校準需要多少分鐘？','校准使用多少个独立传感器？','Which manufacturer supplied the sensors?']:
            [e async for e in app.upload_document(content,'field-calibration.pdf')]
            events=[e async for e in app.ask(question)]
            results['questions'].append({'question':question,'events':[e.model_dump() for e in events]})
        results['calls']=[c.model_dump() for c in gateway.calls]
        results['maximum_estimated_plus_reservation']=max(c.estimated_prompt_tokens+c.num_predict for c in gateway.calls)
        results['maximum_reported_plus_reservation']=max(c.prompt_eval_count+c.num_predict for c in gateway.calls)
    finally:
        await app.close()
        Path('docs/verification/ticket-11/heldout-native.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
asyncio.run(main())
