import re
import sys

import pymupdf as fitz
import tiktoken

pdf = sys.argv[1]
doc = fitz.open(pdf)
enc = tiktoken.get_encoding("o200k_harmony")

print(f"pages: {len(doc)}")
full = []
for i, page in enumerate(doc):
    text = page.get_text()
    full.append(text)
    print(f"  p{i+1:>2}: {len(enc.encode(text)):>5} tokens")

all_text = "\n".join(full)
total = len(enc.encode(all_text))
print(f"total tokens (o200k_harmony): {total}")

ref_idx = all_text.find("\nREFERENCES")
if ref_idx < 0:
    ref_idx = all_text.find("\nReferences")
if ref_idx > 0:
    body = all_text[:ref_idx]
    print(f"tokens before References: {len(enc.encode(body))}")

print("\n=== headings (numbered) ===")
for line in all_text.splitlines():
    if re.match(r"^\d+(\.\d+)*\s+[A-Z][A-Za-z\- ]{3,60}$", line.strip()):
        print("  ", line.strip())

print("\n=== table captions ===")
for i, page in enumerate(doc):
    for m in re.finditer(r"Table \d+:[^\n]*", page.get_text()):
        print(f"  p{i+1}: {m.group(0)[:120]}")

print("\n=== find_tables() ===")
for i, page in enumerate(doc):
    tabs = page.find_tables()
    for t in tabs.tables:
        print(f"\n--- p{i+1} bbox={tuple(round(x) for x in t.bbox)} rows={t.row_count} cols={t.col_count}")
        print(t.to_markdown()[:1800])
