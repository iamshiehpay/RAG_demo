// Diagnostic fallback after agent-browser lost its product target. Owned Chrome only.
import fs from 'node:fs';
const out = new URL('./', import.meta.url);
const prefix=process.env.REVIEW_PREFIX || '';
const url=process.env.REVIEW_URL || 'http://127.0.0.1:8121/';
const port=process.env.REVIEW_CDP_PORT || '59809';
const log = x => { const s = JSON.stringify(x); console.log(s); fs.appendFileSync(new URL(prefix+'direct-cdp.txt', out), s+'\n'); };
const targets = await (await fetch('http://127.0.0.1:'+port+'/json/list',{signal:AbortSignal.timeout(3000)})).json();
const page = targets.find(x => x.url === 'about:blank' || x.url === url);
if (!page) throw Error('Owned blank target unavailable');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r=>ws.addEventListener('open',r,{once:true}));
let seq=0; const pending=new Map();
ws.addEventListener('message', e=>{const x=JSON.parse(e.data); if(x.id){const p=pending.get(x.id);if(p){pending.delete(x.id);clearTimeout(p.t);x.error?p.reject(x.error):p.resolve(x.result);}} else if(/crash|destroy|disconnect/i.test(x.method)) log(x);});
async function call(method,params={}){log({method,params});return await new Promise((resolve,reject)=>{const id=++seq;const t=setTimeout(()=>reject(Error('timeout '+method)),8000);pending.set(id,{resolve,reject,t});ws.send(JSON.stringify({id,method,params}));});}
const ev=async expression => (await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result?.value;
const state=async label=>log({label,state:await ev(`({url:location.href,asks:window.__t09?.asks,focus:{tag:document.activeElement?.tagName,class:document.activeElement?.className,label:document.activeElement?.getAttribute('aria-label')},textarea:[...document.querySelectorAll('textarea')].map(t=>({disabled:t.disabled,value:t.value,rect:t.getBoundingClientRect().toJSON(),display:getComputedStyle(t).display,visibility:getComputedStyle(t).visibility,hit:document.elementFromPoint(t.getBoundingClientRect().x+20,t.getBoundingClientRect().y+20)?.tagName})),right:!!document.querySelector('.pane-right'),notes:[...document.querySelectorAll('[role=note]')].map(t=>t.textContent)})`)});
async function click(selector){const p=await ev(`(()=>{const e=document.querySelector(${JSON.stringify(selector)});if(!e)throw Error('missing selector');e.scrollIntoView({block:'nearest'});const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};})()`);if(!p)throw Error('no click point');await call('Input.dispatchMouseEvent',{type:'mousePressed',...p,button:'left',clickCount:1});await call('Input.dispatchMouseEvent',{type:'mouseReleased',...p,button:'left',clickCount:1});}
async function key(key,code,virtual){await call('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode:virtual,nativeVirtualKeyCode:virtual});await call('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:virtual,nativeVirtualKeyCode:virtual});}
async function shot(name){const x=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(new URL(prefix+name,out),Buffer.from(x.data,'base64'));}
async function ask(s){await ev(`window.__t09.scenario=${JSON.stringify(s)}`);await click('textarea');await call('Input.insertText',{text:s});await click('button[type=submit]');await state('submitted '+s);}
try {
 await call('Page.enable');await call('Runtime.enable');
 await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:false});
 await call('Page.navigate',{url});
 for(let i=0;i<50;i++){if(await ev(`!!document.querySelector('input[type=file]')`))break;await new Promise(r=>setTimeout(r,100));}
 const fixture=fs.readFileSync('frontend/review/scripted-events.js','utf8');
 log({fixture:'frontend/review/scripted-events.js'});await ev(fixture);
 const root=await call('DOM.getDocument');const q=await call('DOM.querySelector',{nodeId:root.root.nodeId,selector:'input[type=file]'});
 await call('DOM.setFileInputFiles',{nodeId:q.nodeId,files:[process.cwd()+'/data/lightrag.pdf']});
 await state('ready');await ask('uncertain-table');
 await click('.turn:last-child .inline-citation');await state('uncertain open');
 await key('Escape','Escape',27);await state('uncertain escaped');
 await ask('compare');await click('.turn:last-child .inline-citation:nth-of-type(2)');
 await state('reconstructed open');await shot('cdp-reconstructed.png');
 await key('Escape','Escape',27);await state('reconstructed escaped');await shot('cdp-escaped.png');
 await ev(`window.__t09.scenario='q3'`);await click('textarea');await call('Input.insertText',{text:'q3'});await state('q3 typed');await shot('cdp-typed.png');
 await key('Enter','Enter',13);await state('q3 submitted once');await shot('cdp-final.png');
} catch(e){log({error:String(e)});process.exitCode=1;} finally {ws.close();}
