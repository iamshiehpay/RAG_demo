import json, hashlib, shutil, importlib.metadata as md
from pathlib import Path
import pymupdf
from chat_document.cache import CacheRecord, ProcessingCache, PIPELINE_VERSION
from chat_document.tokens import count_tokens
from chat_document.llm_gateway import BUDGET_TABLE
from chat_document.summary_context import select_summary_context
from eval.second_document import SECOND_DOCUMENT_CASES
R=Path('/Users/shiehpay/Desktop/resume/rag')
O=R/'docs/verification/ticket-10/qa'
pdf=R/'data/industrial-robotics.pdf'; data=pdf.read_bytes()
cachepath=R/'.worktrees/10-second-document/.cache/issue10-issue10-d08-final-n3/fc87348de6890de91aaa71bd551af28f8202c537e83c76664e24ecff64cda477.json'
record=CacheRecord.model_validate_json(cachepath.read_bytes());d=record.document;t=d.summary_tree
v=json.loads((R/'eval/reports/issue10-d08-final-n3.ingestion.json').read_text())
assert record.content_hash==hashlib.sha256(data).hexdigest()==v['pdf_sha256']
assert record.pipeline_version==PIPELINE_VERSION==v['pipeline_version']
assert record.processing_config=={'embedding_model':'bge-m3','chunk_token_target':500,'summary_model':'gpt-oss:120b-cloud'}
assert len(d.sections)==32 and len(d.chunks)==149 and len(t.section_summaries)==31
assert sum(count_tokens(s.text) for s in t.section_summaries)==7777
assert all(80<=count_tokens(s.text)<=500 for s in t.section_summaries)
assert len(t.group_levels)==1 and len(t.group_levels[0])==2
bysection={s.id:s for s in d.sections};bychunk={c.id:c for c in d.chunks}
for c in d.chunks:
 s=bysection[c.section_id]; assert s.page_start<=c.page_start<=c.page_end<=s.page_end
 assert c.section==s.title
 assert not any(40<=p<=70 for p in range(c.page_start,c.page_end+1))
for s in t.section_summaries:
 assert set(s.chunk_ids)=={c.id for c in d.chunks if c.section_id in s.section_ids}
 assert set(s.section_ids)<=set(bysection)
 assert all(x in bychunk for x in s.chunk_ids)
for layer in t.group_levels:
 assert {x for s in layer for x in s.section_ids}=={x for s in t.section_summaries for x in s.section_ids}
 assert {x for s in layer for x in s.chunk_ids}==set(bychunk)
assert {s.page_start for s in d.sections if s.is_appendix}=={71,74,77,92}
assert any(s.section=='Abstract' and s.page_start==1 for s in t.section_summaries)
for c in v['calls']:
 b=BUDGET_TABLE[c['call_type']]
 assert c['estimated_prompt_tokens']+c['num_predict']<=10000
 assert c['prompt_eval_count']+c['num_predict']<=10000
 assert c['num_predict']==b.num_predict and c['think'] in ['low','medium']
 assert c['estimated_prompt_tokens']<=b.prompt_limit+300
calls=v['calls'];assert len(calls)==107
responses=[json.loads(x) for x in (R/'eval/reports/issue10-d08-final-n3.responses.jsonl').read_text().splitlines()]
assert len(responses)==107
retrychecks=[]
for failed,retry in [(29,33),(39,44)]:
 f,r=responses[failed-1],responses[retry-1]
 assert calls[failed-1]['done_reason']=='length' and calls[retry-1]['done_reason']=='stop'
 assert f['source_label']==r['source_label']
 matched=[s for s in t.section_summaries if s.text.endswith(r['response'])]
 assert len(matched)==1 and f['response'] not in matched[0].text
 retrychecks.append({'failed':failed,'retry':retry,'published_section':matched[0].section,'discarded':True})
context,citations,level=select_summary_context(t,SECOND_DOCUMENT_CASES[1].question,current_question=SECOND_DOCUMENT_CASES[1].question)
assert level=='group:1'
cache=ProcessingCache(Path('/private/tmp/nova-qa10-run/cache'))
cache.directory.mkdir(parents=True,exist_ok=True); target=cache._path(data,record.processing_config);shutil.copyfile(cachepath,target)
assert cache.load(data,record.processing_config) is not None
primary=pymupdf.open(pdf)
for n in [1,4,28,29,30,31,39,71,74,77,92,109]:
 (Path('/private/tmp/nova-qa10-run')/f'page-{n}.txt').write_text(primary[n-1].get_text())
for n in [1,4,31,71,92]:
 pix=primary[n-1].get_pixmap(matrix=pymupdf.Matrix(1.6,1.6));pix.save(O/f'takeover-pdf-p{n}.png')
table9=[c for c in d.chunks if c.table_label=='Table 9'];assert len(table9)==1
print(table9[0].model_dump_json(indent=2))
audit={'main_commit':'7cf91851f9f86527d69c95910f9eadd58cf7b357','pipeline':PIPELINE_VERSION,'pdf_sha256':hashlib.sha256(data).hexdigest(),'page_count':len(primary),'processing_config':record.processing_config,'versions':{name:md.version(name) for name in ['PyMuPDF','tiktoken','fastapi','numpy','uvicorn']},'section_count':len(d.sections),'chunks':len(d.chunks),'summary_count':len(t.section_summaries),'summary_sum':7777,'summary_min':min(count_tokens(s.text) for s in t.section_summaries),'summary_max':max(count_tokens(s.text) for s in t.section_summaries),'group_levels':len(t.group_levels),'global_level':level,'calls':len(calls),'max_estimated_plus_reservation':max(c['estimated_prompt_tokens']+c['num_predict'] for c in calls),'max_actual_plus_reservation':max(c['prompt_eval_count']+c['num_predict'] for c in calls),'discarded_length_retries':retrychecks,'table9':table9[0].model_dump(),'section_inventory':[{'id':s.id,'title':s.title,'pages':[s.page_start,s.page_end],'appendix':s.is_appendix} for s in d.sections]}
(O/'takeover-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
