"""Compare source Section/page structure and all numerical tokens with reviewed baseline."""
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

SNAPSHOT = r"""
import collections,json,re,sys
sys.path.insert(0,sys.argv[1])
from chat_document.pdf_parser import parse_pdf
from chat_document.chunker import chunk_sections
sections=parse_pdf(Path(sys.argv[2]).read_bytes())
chunks=chunk_sections(sections,"evidence")
numbers=collections.Counter()
for chunk in chunks:
    numbers.update(re.findall(r"\d+(?:[.,]\d+)*",chunk.text.replace("_","")))
print(json.dumps({"sections":[[s.title,s.page_start,s.page_end] for s in sections],"numbers":numbers}))
""".replace("import collections,json,re,sys", "import collections,json,re,sys\nfrom pathlib import Path")
root=Path(__file__).resolve().parents[4]
baseline=Path(sys.argv[1])
data=root/"data/lightrag.pdf"
def snapshot(source):
    return json.loads(subprocess.check_output([str(root/".venv/bin/python"),"-I","-c",SNAPSHOT,str(source),str(data)]))
a,b=snapshot(baseline),snapshot(root/"src")
missing=collections.Counter(a["numbers"])-collections.Counter(b["numbers"])
extra=collections.Counter(b["numbers"])-collections.Counter(a["numbers"])
report={"baseline_source":str(baseline),"current_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip(),"sections_identical":a["sections"]==b["sections"],"baseline_number_count":sum(a["numbers"].values()),"candidate_number_count":sum(b["numbers"].values()),"missing":dict(missing),"extra":dict(extra)}
print(json.dumps(report,indent=2))
assert report["sections_identical"] and not missing and not extra
