"""Independent prepared-batch user actions; live response observer only."""
import json,subprocess,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
SHA='3432aa09ee7d9fcbdc9199ff9f0ee685961102e3'
LOG=[]
def run(*args,code=None):
 p=subprocess.run(['agent-browser','--session','nova-qa09',*args],input=code,text=True,capture_output=True,timeout=240)
 LOG.append({'args':args,'stdout':p.stdout,'stderr':p.stderr,'exit':p.returncode})
 (OUT/'takeover-live-browser-commands.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout

def js(code):return run('eval','--stdin',code=code)
def save(name,code):
 data=json.loads(js(code));(OUT/('takeover-live-'+name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2));return data

def click(sel):
 js('document.querySelector('+json.dumps(sel)+').scrollIntoView({block:"center"})');run('click',sel)
def shot(name):run('screenshot',str(OUT/('takeover-live-'+name+'.png')))
run('set','viewport','1280','720')
run('network','route','https://**','--abort')
run('reload')
run('snapshot','-i')
js('''(()=>{window.__qa={responses:[],states:[]};const f=window.fetch;window.fetch=async(...a)=>{const r=await f(...a);if(String(a[0]).startsWith('/api/'))r.clone().text().then(text=>window.__qa.responses.push({url:String(a[0]),status:r.status,text}));return r};const track=()=>{const q=document.querySelector('#question'),s=document.querySelector('.upload-progress'),a=document.querySelector('article:last-child');const v={at:Date.now(),upload:s?.textContent,disabled:q?.disabled,stage:a?.querySelector('.stage-indicator')?.className,answer:a?.querySelector('.answer-text')?.textContent,citations:a?.querySelectorAll('.inline-citation').length};const prev=window.__qa.states.at(-1);if(!prev||JSON.stringify({...prev,at:0})!==JSON.stringify({...v,at:0}))window.__qa.states.push(v)};new MutationObserver(track).observe(document.body,{subtree:true,childList:true,attributes:true,characterData:true});track();return 'Observer only; native responses unchanged'})()''')
run('upload','#document',str(ROOT/'data/lightrag.pdf'))
run('snapshot','-i');shot('processing')
run('wait','--fn',"!document.querySelector('#question').disabled || !!document.querySelector('.upload .error-state')",'--timeout','180000')
run('snapshot');shot('ready')
save('upload',"window.__qa")
if json.loads(js("document.querySelector('#question').disabled")):raise RuntimeError('Real ingestion failed; see upload evidence')
run('fill','#question','Performance of ablated versions of LightRAG.')
click('button[type=submit]')
run('wait','--fn',"!!document.querySelector('article:last-child .stage-complete,article:last-child .stage-error') && !document.querySelector('#question').disabled",'--timeout','180000')
run('wait','--fn',"window.__qa.responses.some(x=>x.url==='/api/ask')")
run('snapshot');shot('answer')
save('responses','window.__qa')
d=save('display',"""(()=>{const a=document.querySelector('article:last-child');return {sha:"3432aa09ee7d9fcbdc9199ff9f0ee685961102e3",answer:a.querySelector('.answer-text')?.textContent,html:a.querySelector('.answer-text')?.innerHTML,complete:!!a.querySelector('.stage-complete'),error:a.querySelector('.error-state')?.textContent,citations:[...a.querySelectorAll('.inline-citation')].map(x=>x.textContent),margins:[...a.querySelectorAll('.margin-citation')].map(x=>x.textContent),traceCollapsed:!a.querySelector('.trace')?.open,bodyFont:getComputedStyle(document.body).fontFamily,bodySize:getComputedStyle(document.body).fontSize,fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>({family:f.family,status:f.status})),resources:performance.getEntriesByType('resource').map(r=>r.name),animations:document.getAnimations().length,overflow:document.documentElement.scrollWidth>innerWidth}})()""")
if d.get('complete'):
 click('article:last-child .trace > summary');shot('trace')
 save('trace',"""(()=>{const t=document.querySelector('article:last-child .trace');return {text:t.textContent,meters:[...t.querySelectorAll('[role=meter]')].map(m=>({max:m.getAttribute('aria-valuemax'),now:m.getAttribute('aria-valuenow'),width:m.getBoundingClientRect().width,prompt:m.querySelector('.token-prompt').getBoundingClientRect().width,reserve:m.querySelector('.token-reserved').getBoundingClientRect().width})),thinking:[...t.querySelectorAll('.thinking-content')].map(x=>({open:x.open,text:x.textContent}))}})()""")
 if d['citations']:
  click('article:last-child .inline-citation');run('wait','--fn',"!!document.querySelector('dialog .source-text,dialog table,dialog .error-state')");shot('source');save('source',"({title:document.querySelector('#source-title').textContent,text:document.querySelector('dialog').textContent,html:document.querySelector('dialog').innerHTML})");run('press','Tab');run('press','Escape');save('focus',"({closed:!document.querySelector('dialog'),active:document.activeElement.className})")
run('console');run('errors')
print(json.dumps({'sha':SHA,'complete':d.get('complete'),'citations':len(d['citations']),'commands':len(LOG)}))
