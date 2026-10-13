"""Viewport checks through public controls with explicitly scripted HTTP events.

Run before/after on the Issue09 bundle; optional 'main-before' uses Main's frozen
bundle, served read-only at the owned port 8191. Evidence is not model quality.
"""
# ruff: noqa: E501  # Embedded browser JavaScript retains readable expressions.

import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
ROOT = BASE.parents[2]
PHASE = sys.argv[1] if len(sys.argv) > 1 else "after"
URL = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8190"
LOG = []
FAILURES = []
MEASUREMENTS = []
(OUT / "evidence").mkdir(exist_ok=True)


def run(*args, code=None):
    result = subprocess.run(
        ["agent-browser", "--session", "nova-i09", *args],
        input=code,
        text=True,
        capture_output=True,
        timeout=45,
    )
    LOG.append(
        {
            "args": args,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    )
    (OUT / f"viewport-{PHASE}-commands.json").write_text(
        json.dumps(LOG, indent=2, ensure_ascii=False)
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def evaluate(code):
    return run("eval", "--stdin", code=code)


def click(selector):
    evaluate(
        "document.querySelector(" + json.dumps(selector) + ').scrollIntoView({block:"center"})'
    )
    run("click", selector)


def measure(name, require_visible=True):
    measurement = json.loads(
        evaluate("""(() => {
      const panel=document.querySelector('.document-overview, .overview');
      const rect=panel.getBoundingClientRect();
      const answer=panel.querySelector('.answer-text');
      const answerRect=answer?.getBoundingClientRect();
      const visible=rect.top<innerHeight && rect.bottom>0;
      const readable=answerRect && Math.min(answerRect.bottom,rect.bottom,innerHeight)>Math.max(answerRect.top,rect.top,0);
      const composer=document.querySelector('#question').getBoundingClientRect();
      return {viewport:[innerWidth,innerHeight],scrollY,top:rect.top,bottom:rect.bottom,
        intersectsViewport:visible,readable:!!readable,scrollHeight:panel.scrollHeight,clientHeight:panel.clientHeight,
        contained:rect.top>=0 && rect.bottom<=innerHeight,
        composerVisible:composer.top<innerHeight && composer.bottom>0,
        questionCount:document.querySelectorAll('article').length,
        overflow:document.documentElement.scrollWidth>innerWidth,text:panel.textContent};
    })()""")
    )
    MEASUREMENTS.append({"scenario": name, **measurement})
    (OUT / f"viewport-{PHASE}-measurements.json").write_text(
        json.dumps(MEASUREMENTS, indent=2, ensure_ascii=False)
    )
    desktop = measurement["viewport"][0] > 900
    if (
        (
            require_visible
            and not (
                measurement["intersectsViewport"]
                and measurement["readable"]
                and (not desktop or measurement["contained"])
            )
        )
        or measurement["overflow"]
        or ("composer" in name and not measurement["composerVisible"])
    ):
        FAILURES.append(name)
    run("screenshot", str(OUT / "evidence" / f"viewport-{PHASE}-{name}.png"))


def install(long=False):
    run("reload")
    fixture = BASE.joinpath("scripted-events.js").read_text()
    fixture = fixture.replace(
        "const chunk = {",
        "const chunk = { kind: '" + ("document" if long else "section") + "', "
        "section_titles: ['4.3 Ablation Study'], section_ids: ['review-4.3'], "
        "chunk_ids: ['review-table2'], target_tokens: 80,",
    )
    fixture = fixture.replace("question_type: 'Lookup'", "question_type: 'Global'")
    fixture = fixture.replace(
        "chunks: [{ chunk, score: .7218 }]", "chunks: [], dropped_chunk_count: 3"
    )
    fixture = fixture.replace(
        "invalid_citation_count:",
        "summary_level: '" + ("document" if long else "section") + "', "
        "dropped_chunk_count: 3, invalid_citation_count:",
    )
    fixture = fixture.replace("id: 'C1'", "id: 'S1'").replace("[C1]", "[S1]")
    if long:
        start = fixture.index("document_summary: '") + len("document_summary: '")
        end = fixture.index("' });", start)
        fixture = (
            fixture[:start]
            + ("長文件的完整概覽，保留段落與具體數字 64.8%。\\n\\n" * 45)
            + fixture[end:]
        )
    evaluate(fixture)
    run("upload", "#document", str(ROOT / "data/lightrag.pdf"))
    run("wait", "--fn", "!document.querySelector('#question').disabled")


def six_queries():
    for index in range(1, 7):
        question = f"Summarize the measurements, round {index}."
        run("fill", "#question", question)
        click("button[type=submit]")
        run(
            "wait",
            "--fn",
            "document.querySelectorAll('article').length === "
            + str(index)
            + " && !document.querySelector('#question').disabled",
        )


run("open", URL)
run("set", "viewport", "1280", "720")
install()
six_queries()
evaluate('document.querySelector("#question").scrollIntoView({block:"center"})')
measure("six-short-Global-composer")
if PHASE != "main-before":
    click("article:last-child .trace > summary")
    evaluate(
        "(() => { const text=document.querySelector('article:last-child .trace').textContent; if (!text.includes('Chunks dropped because of Context Budget: 3') || !text.includes('Summary Tree level: section')) throw new Error('Scripted Trace fields missing'); return 'PASS: nonzero drop count and summary level from typed event contract'; })()"
    ) if PHASE == "after" else None
    click("article:last-child .inline-citation")
    run("wait", "dialog .source-text")
    run("press", "Escape")
    measure("source-close")
    install(long=True)
    six_queries()
    evaluate('document.querySelector("#question").scrollIntoView({block:"center"})')
    measure("long-overview-composer")
    evaluate('document.querySelector(".document-overview").scrollTop=1e9')
    measure("overview-internal-scroll")
    run("set", "viewport", "390", "844")
    evaluate('document.querySelector(".document-overview").scrollIntoView({block:"start"})')
    measure("phone-overview")
    evaluate('document.querySelector("#question").scrollIntoView({block:"center"})')
    measure("phone-composer", require_visible=False)
    click("article:last-child .inline-citation")
    run("wait", "dialog .source-text")
    evaluate(
        "(() => { if (document.querySelector('dialog').getBoundingClientRect().width>innerWidth || !document.querySelector('dialog .source-text').textContent.includes('Table 2')) throw new Error('Phone source unusable'); return 'PASS: phone source dialog'; })()"
    )
    evaluate(
        "(() => { const d=document.querySelector('dialog'); "
        "if (!d.textContent.includes('Document Summary') || !d.querySelector('ul[aria-label] li')) "
        "throw new Error('Typed Document Summary kind/covered Sections missing'); "
        "return 'PASS: scripted typed Document Summary source kind and covered Sections'; })()"
    )
    run("press", "Escape")
run("console")
run("errors")
run("close")
summary = {
    "phase": PHASE,
    "commands": len(LOG),
    "failures": FAILURES,
    "measurements": len(MEASUREMENTS),
}
(OUT / f"viewport-{PHASE}-summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
sys.exit(1 if FAILURES else 0)
