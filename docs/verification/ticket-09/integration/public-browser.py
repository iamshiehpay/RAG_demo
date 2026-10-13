"""Public controls against unmodified HTTP/SSE; observe responses without replacing them."""
# ruff: noqa: E501  # Embedded browser JavaScript retains readable expressions.

import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PHASE = sys.argv[1] if len(sys.argv) > 1 else "after"
LOG = []
FAILURES = []
OBSERVATIONS = []
(OUT / "evidence").mkdir(exist_ok=True)


def run(*args, code=None):
    result = subprocess.run(
        ["agent-browser", "--session", "nova-i09", *args],
        input=code,
        text=True,
        capture_output=True,
        timeout=90,
    )
    LOG.append(
        {
            "args": args,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    )
    (OUT / f"public-{PHASE}-commands.json").write_text(
        json.dumps(LOG, indent=2, ensure_ascii=False)
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def evaluate(code):
    return run("eval", "--stdin", code=code)


def check(condition, name):
    result = evaluate(f"({condition}) ? 'PASS: {name}' : 'FAIL: {name}'")
    if "FAIL:" in result:
        FAILURES.append(name)
    (OUT / f"public-{PHASE}-summary.json").write_text(
        json.dumps(
            {
                "phase": PHASE,
                "complete": False,
                "commands": len(LOG),
                "failures": FAILURES,
                "pass_assertions": sum(x["stdout"].count("PASS:") for x in LOG),
            },
            indent=2,
        )
    )


def click(selector):
    evaluate(
        "document.querySelector(" + json.dumps(selector) + ').scrollIntoView({block:"center"})'
    )
    run("click", selector)


def upload(path):
    evaluate("window.__responses=[]; window.__progress=[]")
    run("upload", "#document", str(path))
    run("wait", "--fn", "!document.querySelector('#question').disabled", "--timeout", "120000")
    run("wait", "--fn", 'window.__responses.some(x=>x.url.includes("/events"))')
    check(
        'document.querySelector(".document-overview")?.textContent.includes("Scripted Document overview")',
        "ready Document overview",
    )
    check(
        "window.__progress.some(x=>/^摘要 · \\d+ \\/ \\d+$/.test(x.text) && x.disabled)",
        "actual summary n/N progress and question gating",
    )
    OBSERVATIONS.append(
        {
            "operation": str(path),
            "data": json.loads(
                evaluate("({responses:window.__responses,progress:window.__progress})")
            ),
        }
    )


def ask(question):
    evaluate("window.__responses=[]")
    run("fill", "#question", question)
    click("button[type=submit]")
    run(
        "wait",
        "--fn",
        "document.querySelector('article:last-child .question-heading')?.textContent === "
        + json.dumps(question)
        + " && !!document.querySelector('article:last-child .stage-complete')",
        "--timeout",
        "120000",
    )
    run("wait", "--fn", 'window.__responses.some(x=>x.url==="/api/ask")')
    check('!document.querySelector("article:last-child .trace").open', "Trace collapsed by default")
    click("article:last-child .trace > summary")
    check(
        'Array.from(document.querySelectorAll("article:last-child [role=meter]")).every(x=>x.getAttribute("aria-valuemax")==="10000")',
        "fixed 10K token meter",
    )
    check(
        'document.querySelector("article:last-child .trace").textContent.includes("Chunks dropped because of Context Budget: 0")',
        "backend drop count visible",
    )
    OBSERVATIONS.append(
        {
            "operation": question,
            "data": json.loads(
                evaluate("({responses:window.__responses,progress:window.__progress})")
            ),
        }
    )


def table_citation(label):
    evaluate(
        """(() => {
      const lines=window.__responses.find(x=>x.url==='/api/ask').text.split('\\n');
      const events=lines.filter(x=>x.startsWith('data: ')).map(x=>JSON.parse(x.slice(6)));
      const chunk=events.find(x=>x.type==='retrieval').chunks.find(x=>x.chunk.table_label===__TABLE_LABEL__).chunk;
      const citation=events.find(x=>x.type==='citation_map').citations.find(x=>x.source_id===chunk.id);
      window.__expectedSource=chunk;
      window.__citation= citation.id;
    })()""".replace("__TABLE_LABEL__", json.dumps(label))
    )
    citation = json.loads(evaluate("window.__citation"))
    click(f'article:last-child .inline-citation[aria-label^="View {citation},"]')
    run("wait", "--fn", '!!document.querySelector("dialog .source-text, dialog table")')


run("open", "http://127.0.0.1:8190")
run("set", "viewport", "1440", "900")
run("reload")
evaluate("""(() => {
  window.__responses=[]; window.__progress=[];
  const original=window.fetch;
  window.fetch=async (...args)=>{
    const response=await original(...args);
    if (String(args[0]).startsWith('/api/')) response.clone().text().then(text=>
      window.__responses.push({url:String(args[0]),status:response.status,text}));
    return response;
  };
  new MutationObserver(()=>{
    const text=document.querySelector('.upload-progress')?.textContent;
    if (text && text!==window.__progress.at(-1)?.text)
      window.__progress.push({text,disabled:document.querySelector('#question')?.disabled});
  }).observe(document.body,{subtree:true,childList:true,characterData:true});
})()""")
upload(ROOT / "data/lightrag.pdf")
ask("Performance of ablated versions of LightRAG")
table_citation("Table 2")
check(
    'document.querySelector("dialog .source-table")?.rows.length === 17 && Array.from(document.querySelectorAll("dialog tbody tr")).every(x=>x.cells.length===6)',
    "real Table 2 typed 16x6 cells",
)
check(
    'document.querySelectorAll("dialog tbody tr").length===window.__expectedSource.table_rows.length && Array.from(document.querySelectorAll("dialog tbody tr")).every((row,i)=>Array.from(row.cells).every((cell,j)=>cell.textContent===window.__expectedSource.table_rows[i][j]))',
    "every rendered Table 2 cell equals parser payload",
)
check(
    'document.querySelector("#source-title").textContent.includes("p.8") && document.querySelector("dialog").textContent.includes("Table Chunk")',
    "table kind and page provenance",
)
run("screenshot", str(OUT / "evidence" / f"public-{PHASE}-table2.png"))
click("dialog .secondary-button")
upload(Path("/private/tmp/nova-i09-public/short-summary.pdf"))
ask("請摘要這份文件")
check(
    'document.querySelector("article:last-child .trace").textContent.includes("Summary Tree level: section")',
    "Global uses section level",
)
click('article:last-child .inline-citation[aria-label^="View S1,"]')
run("wait", "dialog .source-text")
check(
    'document.querySelector("dialog").textContent.includes("Section Summary") && document.querySelector("dialog ul[aria-label] li")',
    "S source kind and covered Sections",
)
run("screenshot", str(OUT / "evidence" / f"public-{PHASE}-section.png"))
click("dialog .secondary-button")
upload(Path("/private/tmp/nova-i09-public/long-summary.pdf"))
ask("請摘要這份長文件")
check(
    'document.querySelector("article:last-child .trace").textContent.includes("Summary Tree level: group:1")',
    "actual Group Summary level",
)
click('article:last-child .inline-citation[aria-label^="View S1,"]')
run("wait", "dialog .source-text")
check(
    'document.querySelector("dialog").textContent.includes("Group Summary") && document.querySelectorAll("dialog ul[aria-label] li").length>1 && document.querySelector("#source-title").textContent.includes("pp.")',
    "group kind covered Sections and page range",
)
run("screenshot", str(OUT / "evidence" / f"public-{PHASE}-group.png"))
click("dialog .secondary-button")
upload(Path("/private/tmp/nova-i09-public/uncertain-table.pdf"))
ask("What values does the measured table contain?")
table_citation("Table 7")
check(
    'document.querySelector("dialog .table-limitation")?.textContent.includes("結構未能可靠重建") && !document.querySelector("dialog table") && document.querySelector("dialog .source-text").textContent===window.__expectedSource.text',
    "uncertain typed table shows limitation and unchanged raw source",
)
run("screenshot", str(OUT / "evidence" / f"public-{PHASE}-uncertain.png"))
run("press", "Escape")
check(
    '!!document.querySelector("#document") && !document.querySelector("dialog") && document.activeElement.classList.contains("inline-citation")',
    "real source Escape restores page and citation focus",
)
(OUT / f"public-{PHASE}-responses.json").write_text(
    json.dumps(OBSERVATIONS, indent=2, ensure_ascii=False)
)
run("console")
run("errors")
run("close")
summary = {
    "phase": PHASE,
    "complete": True,
    "commands": len(LOG),
    "failures": FAILURES,
    "pass_assertions": sum(x["stdout"].count("PASS:") for x in LOG),
}
(OUT / f"public-{PHASE}-summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
sys.exit(1 if FAILURES else 0)
