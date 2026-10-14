"""Frozen-source D22 calls, existing gateway and D21 CaptureLLM; never auto-retry."""
import argparse
import asyncio
import copy
import hashlib
import json
from pathlib import Path
import runpy
from datetime import datetime, timezone

from chat_document.llm_gateway import LLMGateway

ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT.parents[1] / 'd21/live/baseline-standalone.json'
BASE = json.loads(BASE_PATH.read_text())
REQUEST = next(r for r in BASE['llm'] if r['call_type'] == 'answer')
CaptureLLM = runpy.run_path(str(ROOT.parents[1] / 'd21/feedback.py'))['CaptureLLM']
EXTRACT = '''\nFor this diagnostic task, instead of composing a final answer, extract the evidence relevant to the current question. Return a concise evidence ledger in the current user's language. For each item give: the precise subject (distinguishing a full method, a named variant, and earlier systems); any relevant variant definition (what is removed or retained); a verbatim supporting quotation from the supplied excerpt; all conditions, frequency words, epistemic hedges and author attribution; the supplied Citation; and whether it supports an answer about the question's subject or only a different subject. Preserve original-language wording in quotations. Do not treat a section heading as a requirement for evidence. Do not infer a limitation from a performance difference alone. If no supplied statement supports the question's subject, use the prescribed fixed refusal.'''

async def run(condition, mode):
    ledger_path = ROOT / 'call-accounting.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else []
    assert len(ledger) < 8, 'Call ceiling reached'
    assert not any(x['condition']==condition for x in ledger), 'No repeated condition ID'
    messages = copy.deepcopy(REQUEST['messages'])
    sources = BASE['sources']
    if mode in ('neutral-local','baseline-local'):
        if mode == 'neutral-local':
            messages[0]['content'] = (ROOT / 'neutral-instruction.txt').read_text()
        local = json.loads((ROOT / 'local-context.json').read_text())
        messages[1]['content'] = local['user_message']
        sources = local['sources']
    elif mode == 'neutral':
        messages[0]['content'] = (ROOT / 'neutral-instruction.txt').read_text()
    elif mode == 'extract':
        messages[0]['content'] += EXTRACT
    elif mode == 'candidate':
        messages[0]['content'] += (ROOT / 'candidate-instruction.txt').read_text()
    elif mode in ('qualified', 'absent', 'baseline-qualified', 'baseline-absent'):
        if not mode.startswith('baseline-'):
            messages[0]['content'] += (ROOT / 'candidate-instruction.txt').read_text()
        control = json.loads((ROOT / 'controls.json').read_text())
        messages[1]['content'] = control[mode.removeprefix('baseline-')]['user_message']
        sources = control[mode.removeprefix('baseline-')]['sources']
    elif mode != 'baseline':
        raise ValueError(mode)
    artifact = {'condition':condition, 'provenance':'NEW live provider call; fixed-source diagnostic; no Router/embedding call',
                'baseline_path':str(BASE_PATH), 'baseline_sha256':hashlib.sha256(BASE_PATH.read_bytes()).hexdigest(),
                'sources':sources,'original_chunks':BASE['original_chunks'] if mode not in ('qualified','absent','baseline-qualified','baseline-absent') else [],
                'llm':[], 'events':[], 'final_answer':'', 'started':datetime.now(timezone.utc).isoformat()}
    entry={'condition':condition,'ordinal':len(ledger)+1,'status':'started','artifact':condition+'.json','mode':mode}
    ledger.append(entry)
    ledger_path.write_text(json.dumps(ledger,indent=2))
    provider = CaptureLLM(artifact['llm'])
    gateway = LLMGateway(provider)
    output = ROOT / (condition+'.json')
    try:
        async for event in gateway.generate('answer',messages,format=REQUEST['format'],think=REQUEST['think']):
            artifact['events'].append(event.model_dump(mode='json'))
            if event.type == 'delta':
                artifact['final_answer'] += event.text
            output.write_text(json.dumps(artifact,ensure_ascii=False,indent=2))
        entry['status']='complete'
    except Exception as exc:
        artifact['error']=repr(exc)
        entry['status']='failed'
        raise
    finally:
        artifact['completed']=datetime.now(timezone.utc).isoformat()
        artifact['wire_settings']={'model':provider.provider.model,'base_url':provider.provider.base_url,'stream':True,'options':{'num_predict':3000,'temperature':0}}
        output.write_text(json.dumps(artifact,ensure_ascii=False,indent=2))
        ledger_path.write_text(json.dumps(ledger,indent=2))
        print(json.dumps({'condition':condition,'status':entry['status'],'final_answer':artifact['final_answer']},ensure_ascii=False))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('condition')
    parser.add_argument('mode',choices=['neutral-local','baseline-local','baseline','extract','neutral','candidate','qualified','absent','baseline-qualified','baseline-absent'])
    args=parser.parse_args()
    asyncio.run(run(args.condition,args.mode))
