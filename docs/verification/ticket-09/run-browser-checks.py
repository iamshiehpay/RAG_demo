"""Implementer checks, not independent QA. Existing agent-browser CLI only."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
LOG = []


def run(*args, code=None):
    p = subprocess.run(
        ["agent-browser", "--session", "nova-i09", *args],
        input=code,
        text=True,
        capture_output=True,
        check=False,
    )
    LOG.append({"args": args, "stdout": p.stdout, "stderr": p.stderr, "exit_code": p.returncode})
    (OUT / "browser-commands.json").write_text(json.dumps(LOG, indent=2, ensure_ascii=False))
    if p.returncode:
        raise RuntimeError(f"{args}: {p.stdout} {p.stderr}")
    return p.stdout


def evaluate(code):
    return run("eval", "--stdin", code=code)


def screenshot(name):
    run("screenshot", "--full", str(OUT / "evidence" / (name + ".png")))


def ask(scenario):
    question = "Performance of ablated versions of LightRAG: " + scenario
    evaluate(
        "window.__t09.scenario = "
        + json.dumps(scenario)
        + "; window.__t09.askedQuestion = "
        + json.dumps(question)
    )
    run("fill", "#question", question)
    run("click", "button[type=submit]")
    run(
        "wait",
        "--fn",
        "document.querySelector('article:last-child .question-heading')?.textContent === (window.__t09.scenario === 'rejected' ? '問題過長' : window.__t09.askedQuestion)",
    )
    run(
        "wait",
        "--fn",
        "!document.querySelector('#question').disabled"
        if scenario not in ("provisional", "retry")
        else "!!document.querySelector('.stage-' + window.__t09.scenario.replace('provisional', 'answering'))",
    )
    if scenario not in ("rejected", "provisional", "retry"):
        run("wait", "article:last-child .trace")
        if evaluate("document.querySelector('article:last-child .trace').open").strip() == "false":
            evaluate(
                "window.scrollTo({top: window.scrollY + document.querySelector('article:last-child .trace > summary').getBoundingClientRect().top - 120})"
            )
            run("click", "article:last-child .trace > summary")
        run("wait", "--fn", "document.querySelector('article:last-child .trace').open")
    return evaluate((OUT / "checks.js").read_text())


run("open", "http://127.0.0.1:8190")
run("set", "viewport", "1440", "900")
run("network", "route", "https://**", "--abort")
run("reload")
run("wait", "--load", "networkidle")
screenshot("01-empty")
evaluate((OUT / "scripted-events.js").read_text())
evaluate("window.__t09.uploadHold = true")
run("upload", "#document", str(ROOT / "data/lightrag.pdf"))
run("wait", "--text", "18 / 52")
evaluate(
    "(() => { if (!document.querySelector('#question').disabled || !document.querySelector('progress')) throw new Error('Upload gating failed'); return 'PASS: processing state disables questions'; })()"
)
screenshot("02-background-upload")
evaluate("window.__t09.release()")
run("wait", "--fn", "!document.querySelector('#question').disabled")
ask("budget")
screenshot("03-q3-trace-10k")
run("find", "first", "article:last-child .margin-citation", "click")
run("wait", "#source-title")
evaluate(
    "(() => { if (!document.querySelector('#source-title').textContent.includes('pp.8–9')) throw new Error('Source page range lost'); return 'PASS: source page range'; })()"
)
screenshot("04-source-range")
run("press", "Escape")
evaluate(
    "(() => { if (document.querySelector('dialog') || !document.activeElement.classList.contains('margin-citation')) throw new Error('Dialog focus not restored'); return 'PASS: Escape closes and restores focus'; })()"
)
for w, h in [(1280, 720), (390, 844)]:
    run("set", "viewport", str(w), str(h))
    evaluate((OUT / "checks.js").read_text())
    screenshot(f"05-q3-{w}")
run("set", "viewport", "1440", "900")
for scenario in [
    "unverified",
    "markdown",
    "no-thinking",
    "rejected",
    "error",
    "provisional",
    "retry",
]:
    ask(scenario)
    screenshot("06-" + scenario)
    if scenario in ("provisional", "retry"):
        evaluate("window.__t09.release()")
        run("wait", "--fn", "!document.querySelector('#question').disabled")
    if scenario == "error":
        evaluate("window.__t09.scenario = 'q3'")
        run("click", "article:last-child .error-state button")
        run("wait", "--fn", "!document.querySelector('#question').disabled")
        evaluate(
            "(() => { if (!document.querySelector('article:last-child .stage-complete') || document.querySelector('article:last-child .error-state')) throw new Error('Retry failed'); return 'PASS: latest turn Retry replaces failed turn'; })()"
        )
# Structured spans in Markdown code/table/link/escaped text must still be visible.
custom = "😀 Verified. [C1]\n\n| Claim | Evidence |\n| --- | --- |\n| table claim. | [C1] |\n\n`inline code.` More prose. [C1]\n\n```\ncode block.\n```\n\n[linked claim.](https://example.com) [C1]\n\nEscaped &amp; claim. [C1]\n\n[Unverified](#unverified)"
spans = []
for phrase in [
    "table claim.",
    "inline code.",
    "code block.",
    "linked claim.",
    "Escaped &amp; claim.",
]:
    start = custom.index(phrase)
    spans.append({"start": start, "end": start + len(phrase)})
evaluate(
    "window.__t09.customAnswer = "
    + json.dumps(custom)
    + "; window.__t09.customSpans = "
    + json.dumps(spans)
)
ask("custom")
evaluate(
    "(() => { const t = document.querySelector('article:last-child .answer-text'); if (t.querySelectorAll('.unverified-mark').length !== 5 || t.querySelector('code .unverified-mark') || !t.querySelector('table .unverified-mark') || !t.querySelector('a[href=\"#unverified\"]')) throw new Error('Markdown span annotation failed'); return 'PASS: structured spans annotate code, table, link, entity; ordinary Unverified link unchanged'; })()"
)
screenshot("06-markdown-spans")
# An unsuccessful new upload retains previous Document and conversation.
evaluate(
    'window.__t09.uploadFailure = true; window.__turnCount = document.querySelectorAll("article").length'
)
run("upload", "#document", str(ROOT / "data/lightrag.pdf"))
run("wait", "--text", "Scripted invalid PDF")
evaluate(
    "(() => { if (document.querySelectorAll('article').length !== window.__turnCount || document.querySelector('#question').disabled) throw new Error('Previous Document lost'); return 'PASS: failed upload retains Document and turns'; })()"
)
# Replacing a ready Document: new progress must take priority over old Ready status.
evaluate("window.__t09.uploadFailure = false; window.__t09.uploadHold = true")
run("upload", "#document", str(ROOT / "data/lightrag.pdf"))
run("wait", "--text", "18 / 52")
evaluate(
    "(() => { if (!document.querySelector('#question').disabled || document.querySelector('.upload-progress').textContent.includes('完成')) throw new Error('Old Ready masked new upload'); return 'PASS: new upload progress precedes old Ready'; })()"
)
screenshot("07-replacing-document")
evaluate("window.__t09.release()")
run("wait", "--fn", "!document.querySelector('#question').disabled")
evaluate(
    "(() => { if (document.querySelector('article') || document.querySelector('#question').value) throw new Error('New Document not reset'); return 'PASS: ready resets conversation and input'; })()"
)
# Lost progress supports reconnect; a backend restart permits choosing PDF again.
evaluate("window.__t09.uploadHold = false; window.__t09.progressLost = true")
run("upload", "#document", str(ROOT / "data/lightrag.pdf"))
run("wait", "--text", "Reconnect upload progress")
screenshot("08-reconnect-progress")
run("find", "text", "Reconnect upload progress", "click")
run("wait", "--fn", "!document.querySelector('#question').disabled")
evaluate("window.__t09.progressLost = 'restart'")
run("upload", "#document", str(ROOT / "data/lightrag.pdf"))
run("wait", "--text", "Choose the PDF again.")
evaluate(
    "(() => { if (document.querySelector('#document').disabled || document.querySelector('progress')) throw new Error('Restart recovery stuck'); return 'PASS: restart offers selecting PDF again'; })()"
)
screenshot("09-restart-recovery")
(OUT / "fixture-events.json").write_text(evaluate("window.__t09.events"))
run("console")
run("errors")
print("Browser implementation checks passed; evidence saved to", OUT)
