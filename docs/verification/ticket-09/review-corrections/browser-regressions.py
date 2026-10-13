"""M1/m1/m2 real-browser regressions, executed by the implementer (not QA)."""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
BASE = OUT.parent
PHASE = sys.argv[1] if len(sys.argv) > 1 else 'after'
LOG = []
FAILURES = []


def run(*args, code=None, assertion=False):
    result = subprocess.run(['agent-browser', '--session', 'nova-i09', *args],
                            input=code, text=True, capture_output=True, timeout=45)
    LOG.append({'args': args, 'stdout': result.stdout, 'stderr': result.stderr,
                'exit_code': result.returncode})
    (OUT / f'{PHASE}-commands.json').write_text(json.dumps(LOG, indent=2, ensure_ascii=False))
    if result.returncode:
        if assertion:
            FAILURES.append(result.stderr)
        else:
            raise RuntimeError(result.stderr)
    return result.stdout


def evaluate(code, assertion=False):
    return run('eval', '--stdin', code=code, assertion=assertion)


def check(code):
    return evaluate(code, assertion=True)


def click(selector):
    evaluate('window.scrollTo({top: window.scrollY + document.querySelector(' +
             json.dumps(selector) + ').getBoundingClientRect().top - 120})')
    run('click', selector)


def ask(answer, spans, name):
    evaluate('window.__t09.scenario = "custom"; window.__t09.customAnswer = ' +
             json.dumps(answer) + '; window.__t09.customSpans = ' + json.dumps(spans))
    run('fill', '#question', name)
    click('button[type=submit]')
    run('wait', '--fn', "document.querySelector('article:last-child .question-heading')?.textContent === " + json.dumps(name) + " && !!document.querySelector('article:last-child .stage-complete')")


run('open', 'http://127.0.0.1:8190')
run('set', 'viewport', '1440', '900')
run('reload')
evaluate(BASE.joinpath('scripted-events.js').read_text())
run('upload', '#document', str(ROOT / 'data/lightrag.pdf'))
run('wait', '--fn', "!document.querySelector('#question').disabled")
cases = [
    ('escape', r'Bad 5 \* 3 claim. Next valid sentence [C1].', 'Bad 5 * 3 claim.', 'Next valid sentence'),
    ('entity', 'Bad R&amp;D claim. Next [C1].', 'Bad R&D claim.', 'Next'),
    ('list', '- Item one bad claim.\n  continuation valid [C1].', 'Item one bad claim.', 'continuation valid'),
    ('quote', '> Bad R&amp;D claim.\n> Next valid sentence [C1].', 'Bad R&D claim.', 'Next valid sentence'),
    ('numeric-emoji', '😀 Bad R&#38;D claim. Next valid sentence [C1].', '😀 Bad R&D claim.', 'Next valid sentence'),
]
for name, answer, expected_bad, expected_valid in cases:
    start = answer.index('Bad') if name not in ('list', 'numeric-emoji') else (2 if name == 'list' else 0)
    end = answer.index('.') + 1
    ask(answer, [{'start': start, 'end': end}], 'Scripted regression ' + name)
    check('''(() => {
      const text = document.querySelector('article:last-child .answer-text');
      const mark = text.querySelector('.unverified-mark');
      const paragraph = mark?.closest('.answer-paragraph');
      const citation = paragraph?.querySelector('.inline-citation');
      const bad = %s;
      const valid = %s;
      const before = mark?.previousSibling?.textContent.trim();
      const after = mark?.nextSibling?.textContent.trim();
      if (text.querySelectorAll('.unverified-mark').length !== 1 || before !== bad ||
          !after?.startsWith(valid) || !citation ||
          !(mark.compareDocumentPosition(citation) & Node.DOCUMENT_POSITION_FOLLOWING)) {
        throw new Error('Unverified boundary: %s: ' + JSON.stringify({before, after}));
      }
      return 'PASS: %s Unverified is immediately after bad sentence and before valid cited sentence';
    })()''' % (json.dumps(expected_bad), json.dumps(expected_valid), name, name))
    run('screenshot', '--full', str(OUT / 'evidence' / f'{PHASE}-{name}.png'))
# Both C1 and C2 are held; old success/error/finally must not change C2's dialog.
evaluate('''(() => {
  const original = window.fetch;
  const second = {...window.__t09.chunk, id: 'review-c2', section: 'Current C2', text: 'Current C2 source text', page_start: 10, page_end: 11};
  window.__t09.citations.push({id:'C2', source_id:second.id, section:second.section, page_start:10, page_end:11});
  window.fetch = async (url, options) => {
    if (String(url).startsWith('/api/sources/')) {
      const isSecond = String(url).endsWith(second.id);
      window.__t09[isSecond ? 'c2Requested' : 'c1Requested'] = true;
      await new Promise(resolve => { window.__t09[isSecond ? 'releaseC2' : 'releaseC1'] = resolve; });
      if (!isSecond && window.__t09.lateC1Error) throw new Error('Late C1 failure');
      window.__t09[isSecond ? 'c2Returned' : 'c1Returned'] = true;
      return Response.json(isSecond ? second : window.__t09.chunk);
    }
    return original(url, options);
  };
})()''')
ask('Scripted source C1 [C1]. Current source C2 [C2].', [], 'Scripted source fetch race')
for late_error in [False, True]:
    evaluate('window.__t09.c1Requested = false; window.__t09.c2Requested = false; window.__t09.c1Returned = false; window.__t09.lateC1Error = ' + json.dumps(late_error))
    click('article:last-child .inline-citation[aria-label^="View C1,"]')
    run('wait', '--fn', 'window.__t09.c1Requested')
    click('dialog .secondary-button')
    click('article:last-child .inline-citation[aria-label^="View C2,"]')
    run('wait', '--fn', 'window.__t09.c2Requested')
    if not late_error:
        evaluate('window.__t09.releaseC1()')
        run('wait', '--fn', 'window.__t09.c1Returned')
        check("(() => { const d=document.querySelector('dialog'); if (!d?.textContent.includes('正在讀取原文') || d.querySelector('.source-text') || d.querySelector('.error-state')) throw new Error('Old C1 altered pending C2 source/loading'); return 'PASS: late C1 success/finally cannot change pending C2'; })()")
    evaluate('window.__t09.releaseC2()')
    run('wait', '--text', 'Current C2 source text')
    if late_error:
        evaluate('window.__t09.releaseC1(); window.__t09.sourceSettled = new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
        evaluate('window.__t09.sourceSettled.then(() => true)')
    check("(() => { const d=document.querySelector('dialog'); if (!d?.querySelector('#source-title').textContent.includes('pp.10–11 · Current C2') || d.querySelector('.source-text')?.textContent !== 'Current C2 source text' || d.querySelector('.error-state')) throw new Error('Stale C1 corrupted C2 dialog'); return 'PASS: only current C2 source/title displayed, stale success/error ignored'; })()")
    run('screenshot', str(OUT / 'evidence' / f'{PHASE}-source-race-{late_error}.png'))
    click('dialog .secondary-button')
# Real controls exercise the backend-restart 404 response seam, with an old Document.
evaluate('window.__t09.progressLost = true')
run('upload', '#document', str(ROOT / 'data/lightrag.pdf'))
run('wait', '--text', 'Reconnect upload progress')
evaluate("window.__t09.progressLost = 'restart'")
click('.upload .secondary-button')
run('wait', '--text', 'Choose the PDF again.')
check("(() => { if (!document.querySelector('#question').disabled || !document.querySelector('button[type=submit]').disabled || document.querySelector('article') || document.querySelector('.document-meta') || document.querySelector('#document').disabled || document.querySelector('dialog')) throw new Error('Restart left stale Document askable'); return 'PASS: restart clears stale Document/turns/source and disables questions; PDF selectable'; })()")
run('screenshot', '--full', str(OUT / 'evidence' / f'{PHASE}-restart.png'))
evaluate('window.__t09.progressLost = false')
run('upload', '#document', str(ROOT / 'data/lightrag.pdf'))
run('wait', '--fn', "!document.querySelector('#question').disabled")
check("(() => { if (!document.querySelector('.document-meta')) throw new Error('Reupload failed'); return 'PASS: reupload after restart restores ready gating'; })()")
run('console'); run('errors'); run('close')
summary = {'phase': PHASE, 'commands': len(LOG), 'failures': FAILURES,
           'pass_assertions': sum(x['stdout'].count('PASS:') for x in LOG)}
(OUT / f'{PHASE}-summary.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
sys.exit(1 if FAILURES else 0)
