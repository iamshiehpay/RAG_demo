"""Final bounded prepared cases: literal S, Markdown spans, Global viewport, fresh fonts."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent;src=(p/'takeover-scripted.py').read_text().split("run('reload');run('set'")[0];exec(src.replace('takeover-scripted-','takeover-remaining-'))
run('tab','new','http://127.0.0.1:8290');run('set','viewport','1280','720')
# Upload summary/embedding faults through visible file selection, labelled event fixtures.
for name in ['summary','embedding']:
 f=(ROOT/'docs/verification/ticket-09/scripted-events.js').read_text();f=f.replace("emit({ type: 'stage', stage: 'complete', completed: 1, total: 1 });", "emit({type:'stage',stage:'"+name+"',completed:1,total:2}); emit({type:'error',code:'upload_failed',message:'QA controlled "+name+" failure'}); return;")
 js(f);run('upload','#document',str(ROOT/'data/lightrag.pdf'));run('wait','--text','QA controlled '+name+' failure');check(name+' upload failure blocks composer and no ready',"document.querySelector('#question').disabled&&!document.querySelector('.document-meta')&&!!document.querySelector('.upload .error-state')");shot('upload-'+name+'-error')
js((ROOT/'docs/verification/ticket-09/scripted-events.js').read_text());run('upload','#document',str(ROOT/'data/lightrag.pdf'));ready();check('upload model-fault recovery via new PDF selection',"!document.querySelector('#question').disabled&&!!document.querySelector('.document-meta')")
ask('error','Earlier failed question');ask('error','Latest failed question');check('only latest failed turn offers retry',"!document.querySelector('article:first-child .error-state button')&&!!document.querySelector('article:last-child .error-state button')")
js("window.__t09.scenario='q3'");click('article:last-child .error-state button');ready();check('latest retry replaces failure',"!!document.querySelector('article:last-child .stage-complete')&&!document.querySelector('article:last-child .error-state')")
js("const previous404=window.fetch;window.fetch=async(u,o)=>String(u).startsWith('/api/sources/')?Response.json({detail:'QA source not found after restart'},{status:404}):previous404(u,o)");click('article:last-child .inline-citation');run('wait','--fn',"!!document.querySelector('dialog .error-state')");check('source404 readable without stale source',"document.querySelector('dialog .error-state').textContent.includes('QA source not found')&&!document.querySelector('dialog .source-text,dialog table')");shot('source404');run('press','Escape')
run('console');run('errors');print(json.dumps({'checks':len(RESULTS),'failed':[r for r in RESULTS if not r['pass']]}))
