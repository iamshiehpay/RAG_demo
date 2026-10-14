import asyncio, json, re, sys
from pathlib import Path
import pymupdf
sys.path.insert(0, str(Path.cwd()/'src'))
from chat_document.pdf_parser import parse_pdf
from chat_document.chunker import chunk_sections
from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
OUT=Path('docs/verification/ticket-03/qa')
PDF=Path('data/lightrag.pdf')

def authored(case):
 with pymupdf.open() as d:
  p=d.new_page(width=660,height=5600 if case=='large' else 900)
  p.insert_text((42,45),'1 Measurements',fontsize=14)
  def line(y,text,x=42,size=10,font='helv'):p.insert_text((x,y),text,fontsize=size,fontname=font)
  def grid(y,rows,xs=(42,242,430)):
   for i,row in enumerate(rows):
    for x,v in zip(xs,row):line(y+i*16,v,x)
  rows=[['Trial','Score','Seconds'],['amber','17.3','21.9'],['violet','38.7','41.2'],['silver','59.1','61.4']]
  if case=='wrapped':
   line(75,'The measured system is discussed in the following block.\nTable 9. Values describe independent observations across trials.')
   grid(130,rows);line(207,'Table 9: Verified trial measurements.')
  elif case=='below':grid(95,rows);line(172,'Table 9: Verified trial measurements.')
  elif case=='cross-column':
   line(75,'Table 9: Verified trial measurements.')
   grid(105,rows,(42,145,235))
   p.insert_textbox(pymupdf.Rect(350,75,625,240),'The separate right column has only explanatory prose. It must not enter the table or change its measured values.',fontsize=10)
  elif case=='cross-page':
   line(75,'Table 9: Verified trial measurements.');grid(105,rows[:3])
   p=d.new_page(width=660,height=900)
   line(45,'Table 9: Verified trial measurements (continued).');grid(75,[rows[0],rows[3]])
  else:
   line(75,'Table 9: Verified trial measurements.')
   if case=='group':rows.insert(3,['Second cohort'])
   if case=='uncertain':rows[2]=['violet','41.2']
   if case=='large':rows=[rows[0]]+[[f'trial{i}',f'{i}.37',f'{i}.93'] for i in range(310)]
   grid(105,rows)
   if case=='heading':line(173,'2 SECOND MEASUREMENT',size=10,font='hebo');line(205,'This subsequent Section records separate observations.')
   elif case=='list':line(173,'(a) Review recorded scores');line(189,'(b) Review recorded times')
  if case not in ('heading','list','large','cross-page'):
   line(290,'The results in Table 9 describe all measured trial values.')
  data=d.tobytes();Path('/private/tmp/nova-qa03-work/'+case+'.pdf').write_bytes(data);return data

async def main():
 sections=parse_pdf(PDF.read_bytes()); chunks=chunk_sections(sections,'independent')
 comparisons=[]
 with pymupdf.open(PDF) as d:
  for number,page in [(1,6),(2,7)]:
   words=d[page].get_text('words'); metrics=['Comprehensiveness','Diversity','Empowerment','Overall']
   ys=sorted(w[1] for w in words if w[4] in metrics and w[1]<310)
   assert len(ys)==16,(number,ys)
   table=next(c for c in chunks if c.table_label==f'Table {number}')
   for i,y in enumerate(ys):
    vals=sorted((w for w in words if abs(w[1]-y)<.3 and re.fullmatch(r'\d+\.\d+%',w[4])),key=lambda w:w[0]);assert len(vals)==8
    header=sorted((w for w in words if 170<w[0]<510 and w[1]<y and w[4] in ['NaiveRAG','LightRAG','RQ-RAG','HyDE','GraphRAG','-High','-Low','-Origin']),key=lambda w:(-w[1],w[0]))[:8]
    header=sorted(header,key=lambda w:w[0]);assert len(header)==8
    expected_label=header[0][4]+' / '+header[1][4]
    assert table.table_rows[i][:2]==[expected_label,metrics[i%4]],(i,header,table.table_rows[i])
    for j,dataset in enumerate(['Agriculture','CS','Legal','Mix']):
     v=vals[2*j][4]+' / '+vals[2*j+1][4];actual=table.table_rows[i][j+2]
     assert v==actual,(number,i,j,v,actual)
     comparisons.append(dict(table=number,page=page+1,comparison=expected_label,metric=metrics[i%4],dataset=dataset,pdf=v,parsed=actual,pdf_y=y))
 OUT.joinpath('takeover-labelled-cells.json').write_text(json.dumps(comparisons,indent=2))
 reports=[]
 for case in ['above','below','cross-column','cross-page','heading','list','group','wrapped','uncertain','large']:
  cs=chunk_sections(parse_pdf(authored(case)),'authored'); tables=[c for c in cs if c.kind=='table'];prose='\n'.join(c.text for c in cs if c.kind=='text')
  numeric=['17.3','21.9','38.7','41.2','59.1','61.4'] if case!='uncertain' else ['17.3','21.9','41.2','59.1','61.4']
  if case!='large':assert all(v in '\n'.join(c.text for c in tables) for v in numeric),(case,[c.model_dump() for c in cs])
  if case=='heading':assert any(c.section.startswith('2 SECOND') for c in cs)
  if case=='list':assert '(a) Review' in prose and '(b) Review' in prose
  if case=='wrapped':assert 'Table 9. Values' in prose and all(c.table_caption.startswith('Table 9: Verified') for c in tables)
  if case in ['group','uncertain']:assert all(not c.table_reconstructed for c in tables)
  if case=='large':
   from chat_document.tokens import count_tokens
   assert len(tables)>1 and all(count_tokens(c.text)<=2000 and c.table_headers==['Trial','Score','Seconds'] for c in tables)
   assert sum(len(c.table_rows) for c in tables)==310
  reports.append(dict(case=case,tables=[c.model_dump() for c in tables],prose=prose,result='PASS'))
 OUT.joinpath('takeover-authored-probes.json').write_text(json.dumps(reports,indent=2))
 llm=ScriptedLLM(['not JSON','The comparison uses the reported measurements [C1].'])
 app=Application(OllamaEmbedder(),LLMGateway(llm))
 assert [e async for e in app.upload_document(PDF.read_bytes(),'LightRAG.pdf')][-1].type=='ready'
 ev=[e async for e in app.ask('Performance of ablated versions of LightRAG.')]
 assert not any(e.type=='error' for e in ev)
 prompt=llm.calls[-1].messages[-1]['content']
 assert 'Table 2: Performance' in prompt and 'Semantic Graph Excels' in prompt
 OUT.joinpath('takeover-q3-prompt.txt').write_text(prompt)
 OUT.joinpath('takeover-q3-events.json').write_text(json.dumps([e.model_dump() for e in ev],indent=2))
 print('PASS: 128 labelled paired cells / 256 numerical values; 10 independent authored layout probes; real bge-m3 public Q3 prompt contains Table2 and discussion. Scripted answer is not a live GoldenFact claim.')
asyncio.run(main())
