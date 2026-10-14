from pathlib import Path
import json,pymupdf
from chat_document.pdf_parser import parse_pdf
from chat_document.chunker import chunk_sections
records=[]
for columns in [False,True]:
 with pymupdf.open() as d:
  p=d.new_page(width=680,height=850);p.insert_text((45,40),'1 Observations',fontsize=14)
  boxes=[pymupdf.Rect(45,80,305,480),pymupdf.Rect(360,80,620,480)] if columns else [pymupdf.Rect(45,80,515,480)]
  texts=[]
  for i,b in enumerate(boxes):
   t=('左側測量紀錄' if i==0 else '右側測量紀錄')*21+'測量值為98.76，時間為54.32秒。';texts.append(t)
   assert p.insert_textbox(b,t,fontname='china-t',fontsize=10)>=0
  sections=parse_pdf(d.tobytes());cs=chunk_sections(sections,'cjk')
  compact=''.join(''.join(c.text.split()) for c in cs)
  assert all(t in compact for t in texts)
  assert all(c.page_start==c.page_end==1 for c in cs)
  records.append({'columns':columns,'result':'PASS','expected':texts,'chunks':[c.model_dump() for c in cs]})
with pymupdf.open() as d:
 p=d.new_page();p.insert_text((45,40),'1 Observations',fontsize=14)
 p.insert_text((45,100),'測量數據為98.76，後續處理',fontname='china-t',fontsize=10)
 p=d.new_page();p.insert_text((45,60),'延續這項觀察並保存54.32秒。',fontname='china-t',fontsize=10)
 p.insert_text((45,130),'Table 12: New page values.',fontsize=10)
 for i,row in enumerate([['Trial','Count'],['delta','73.1'],['omega','89.2']]):
  for x,v in zip([45,230],row):p.insert_text((x,155+i*16),v,fontsize=10)
 s=parse_pdf(d.tobytes());cs=chunk_sections(s,'pages');table=next(c for c in cs if c.kind=='table');text=next(c for c in cs if '98.76' in c.text)
 assert text.page_start==1 and text.page_end==2
 assert table.page_start==table.page_end==2
 assert '73.1' not in text.text and '89.2' not in text.text
 records.append({'cross_page':'PASS','chunks':[c.model_dump() for c in cs]})
Path('docs/verification/ticket-03/qa/takeover-cjk-independent.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
print('PASS: independent measured single/two-column CJK preservation and cross-page paragraph/table provenance')
