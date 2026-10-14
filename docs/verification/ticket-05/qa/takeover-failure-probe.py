"""Independent upload failure/cancellation probes through public application seam."""
import asyncio, importlib.util, json, tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('qa05_harness',Path(__file__).with_name('takeover-probe.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
from chat_document.application import Application
from chat_document.cache import ProcessingCache
from chat_document.llm_gateway import LLMGateway

async def main():
    results=[]
    for failed in ['section_summary','group_summary','document_summary']:
        class Failing(h.QAResponses):
            async def stream(self,r):
                if r.call_type==failed: raise ValueError('QA05 injected '+failed+' failure')
                async for f in super().stream(r):yield f
        llm=Failing(wide=True);cache=ProcessingCache(Path(tempfile.mkdtemp(prefix='nova-qa05-failure-',dir='/private/tmp')))
        app=Application(h.CountingEmbedder(),LLMGateway(llm),cache=cache)
        data=h.document(n=18 if failed=='group_summary' else 2,repeats=5)
        events=[e async for e in app.upload_document(data,failed+'.pdf')]
        assert events[-1].type=='error' and not any(e.type=='ready' for e in events)
        assert app.document is None and (not cache.directory.exists() or not list(cache.directory.iterdir()))
        healthy=h.QAResponses(wide=True); recovery=Application(h.CountingEmbedder(),LLMGateway(healthy),cache=cache)
        ready=await h.upload(recovery,data,'recovery.pdf')
        assert any(c.call_type=='section_summary' for c in healthy.calls)
        results.append(dict(failed=failed,error=events[-1].model_dump(),cache_empty_before_recovery=True,recovery='ready',calls=h.ledger(healthy)))
    entered=asyncio.Event()
    class Held(h.QAResponses):
        async def stream(self,r):
            entered.set();await asyncio.Event().wait()
            async for f in super().stream(r):yield f
    cache=ProcessingCache(Path(tempfile.mkdtemp(prefix='nova-qa05-cancel-',dir='/private/tmp')))
    app=Application(h.CountingEmbedder(),LLMGateway(Held()),cache=cache)
    job=app.start_upload(h.document(n=5),'cancel.pdf')
    await asyncio.wait_for(entered.wait(),30)
    rejected=[e async for e in app.ask('Summarize.')]
    assert rejected[-1].code=='document_not_ready'
    await app.close()
    events=[e async for e in app.upload_events(job)]
    assert events[-1].type=='error' and events[-1].code=='ingestion_cancelled'
    assert app.document is None and not list(cache.directory.iterdir())
    results.append(dict(cancelled=True,error=events[-1].model_dump(),cache_empty=True,ask_during_processing=rejected[-1].model_dump()))
    # Public identity change: explicit cache version and chunk-target seams, no source mutation.
    data=h.document();root=Path(tempfile.mkdtemp(prefix='nova-qa05-identity-',dir='/private/tmp'))
    for version,target in [('qa05-v1',500),('qa05-v2',500),('qa05-v2',256)]:
        llm=h.QAResponses();embed=h.CountingEmbedder()
        app=Application(embed,LLMGateway(llm),cache=ProcessingCache(root,pipeline_version=version),chunk_token_target=target)
        await h.upload(app,data,'identity.pdf')
        assert llm.calls and embed.calls
        results.append(dict(identity=[version,target],reprocessed=True,llm_calls=len(llm.calls),embedding_calls=len(embed.calls)))
    Path('docs/verification/ticket-05/qa/takeover-failure-probes.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
    print('PASS: Section/Group/Document failure + recovery, cancellation/no partial cache, readiness and public identity change')
asyncio.run(main())
