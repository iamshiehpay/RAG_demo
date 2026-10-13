"""One generic real-model format smoke through frozen dist; no response fixtures."""
# ruff: noqa: E501  # Embedded browser JavaScript retains readable expressions.

import json
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
QUESTION = "請用繁體中文簡述這份文件的實驗測量結果，以條列列出實驗、準確率與成本，並附引用。"
LOG = []
(OUT / "evidence").mkdir(exist_ok=True)


def run(*args, code=None):
    result = subprocess.run(
        ["agent-browser", "--session", "nova-i09", *args],
        input=code,
        text=True,
        capture_output=True,
        timeout=240,
    )
    LOG.append(
        {
            "args": args,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    )
    (OUT / "browser-commands.json").write_text(json.dumps(LOG, indent=2, ensure_ascii=False))
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


run("open", "http://127.0.0.1:8190")
run("set", "viewport", "1280", "720")
run("reload")
evaluate("""(() => {
  window.__realResponses=[];
  const original=window.fetch;
  window.fetch=async (...args)=>{
    const response=await original(...args);
    if (String(args[0]).startsWith('/api/')) response.clone().text().then(text=>
      window.__realResponses.push({url:String(args[0]),status:response.status,text}));
    return response;
  };
  return 'Observation only: all requests/responses unchanged.';
})()""")
run("upload", "#document", "/private/tmp/nova-i09-real-smoke-input.pdf")
run("wait", "--fn", "!document.querySelector('#question').disabled", "--timeout", "180000")
run("fill", "#question", QUESTION)
click("button[type=submit]")
run(
    "wait",
    "--fn",
    "!!document.querySelector('article:last-child .stage-complete, "
    "article:last-child .stage-error') && !document.querySelector('#question').disabled",
    "--timeout",
    "180000",
)
run("wait", "--fn", 'window.__realResponses.some(x=>x.url==="/api/ask")')
observations = json.loads(evaluate("window.__realResponses"))
(OUT / "responses.json").write_text(json.dumps(observations, indent=2, ensure_ascii=False))
for response in observations:
    if response["url"] == "/api/ask":
        (OUT / "ask.sse").write_text(response["text"])
    elif response["url"].endswith("/events"):
        (OUT / "upload.sse").write_text(response["text"])
display = json.loads(
    evaluate("""(() => {
  const article=document.querySelector('article:last-child');
  const trace=article.querySelector('.trace');
  const answer=article.querySelector('.answer-text');
  return {question:article.querySelector('.question-heading').textContent,
    complete:!!article.querySelector('.stage-complete'),
    error:article.querySelector('.error-state')?.textContent||null,
    answer_text:answer?.textContent,answer_html:answer?.innerHTML,
    inline_citations:Array.from(article.querySelectorAll('.inline-citation')).map(x=>x.textContent),
    margin_citations:Array.from(article.querySelectorAll('.margin-citation')).map(x=>x.textContent),
    unverified_marks:article.querySelectorAll('.unverified-mark').length,
    trace_collapsed:!trace.open,
    thinking_collapsed:Array.from(article.querySelectorAll('.thinking-content')).every(x=>!x.open),
    heading_count:answer.querySelectorAll('h3').length,
    table_count:answer.querySelectorAll('table').length,
    list_count:answer.querySelectorAll('ul,ol').length,
    body_font:getComputedStyle(document.body).fontFamily,
    body_size:getComputedStyle(document.body).fontSize,
    viewport:[innerWidth,innerHeight],overflow:document.documentElement.scrollWidth>innerWidth};
})()""")
)
(OUT / "display.json").write_text(json.dumps(display, indent=2, ensure_ascii=False))
evaluate(
    'document.querySelector("article:last-child .answer-text").scrollIntoView({block:"start"})'
)
run("screenshot", "--full", str(OUT / "evidence/answer.png"))
click("article:last-child .trace > summary")
trace = json.loads(
    evaluate("""(() => {
  const trace=document.querySelector('article:last-child .trace');
  return {text:trace.textContent,meters:Array.from(trace.querySelectorAll('[role=meter]')).map(x=>
    ({max:x.getAttribute('aria-valuemax'),now:x.getAttribute('aria-valuenow')})),
    thinking_collapsed:Array.from(trace.querySelectorAll('.thinking-content')).every(x=>!x.open)};
})()""")
)
(OUT / "trace-display.json").write_text(json.dumps(trace, indent=2, ensure_ascii=False))
run("screenshot", "--full", str(OUT / "evidence/trace.png"))
if display["inline_citations"]:
    click("article:last-child .inline-citation")
    run("wait", "--fn", '!!document.querySelector("dialog .source-text, dialog table")')
    (OUT / "source-display.json").write_text(
        evaluate(
            '({title:document.querySelector("#source-title").textContent, '
            'text:document.querySelector("dialog").textContent})'
        )
    )
    run("screenshot", str(OUT / "evidence/source.png"))
    run("press", "Escape")
    evaluate("""(() => {
      if (document.querySelector('dialog') || !document.activeElement.classList.contains('inline-citation'))
        throw new Error('Source Escape/focus failed');
      return 'PASS: real-source Escape restores citation focus';
    })()""")
run("console")
run("errors")
run("close")
summary = {
    "complete": display["complete"],
    "commands": len(LOG),
    "failed_commands": sum(x["exit_code"] != 0 for x in LOG),
    "semantic_quality": "Not scored; final Issue11 gate remains separate.",
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
if not display["complete"]:
    raise SystemExit(1)
