"""Implementer CR/CRLF browser checks against the production frontend bundle."""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PHASE = sys.argv[1] if len(sys.argv) > 1 else 'after'
URL = sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8190'
LOG = []
FAILURES = []
(OUT / 'evidence').mkdir(parents=True, exist_ok=True)


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


run('open', URL)
run('set', 'viewport', '1440', '900')
run('reload')
evaluate(OUT.parent.joinpath('scripted-events.js').read_text())
run('upload', '#document', str(ROOT / 'data/lightrag.pdf'))
run('wait', '--fn', "!document.querySelector('#question').disabled")
cases = [
    ('crlf', 'Bad claim one.\r\nNext valid [C1].', 'Bad claim one.', 'Next valid'),
    ('cr', 'Bad claim one.\rNext valid [C1].', 'Bad claim one.', 'Next valid'),
    ('entity-emoji', '😀 Bad R&amp;D claim.\r\nNext valid [C1].', '😀 Bad R&D claim.', 'Next valid'),
    ('quote', '> Bad R&amp;D claim.\r\n> Next valid [C1].', 'Bad R&D claim.', 'Next valid'),
    ('list', '- Bad 5 \\* 3 claim.\r\n  Next valid [C1].', 'Bad 5 * 3 claim.', 'Next valid'),
    ('middle-list', '- Earlier valid [C1].\r\n  Bad R&amp;D claim. Next valid [C1].', 'Bad R&D claim.', 'Next valid'),
]
for name, answer, bad, valid in cases:
    start = 0 if name == 'entity-emoji' else answer.index('Bad')
    end = answer.index('.', start) + 1
    question = 'Scripted newline regression ' + name
    evaluate('window.__t09.scenario = "custom"; window.__t09.customAnswer = ' +
             json.dumps(answer) + '; window.__t09.customSpans = ' +
             json.dumps([{'start': start, 'end': end}]))
    run('fill', '#question', question)
    evaluate('document.querySelector("button[type=submit]").scrollIntoView({block:"center"})')
    run('click', 'button[type=submit]')
    run('wait', '--fn', "document.querySelector('article:last-child .question-heading')?.textContent === " +
        json.dumps(question) + " && !!document.querySelector('article:last-child .stage-complete')")
    evaluate('''(() => {
      const text = document.querySelector('article:last-child .answer-text');
      const mark = text.querySelector('.unverified-mark');
      const before = mark?.previousSibling?.textContent.trim();
      const after = mark?.nextSibling?.textContent.trim();
      const citation = mark?.closest('.answer-paragraph')?.querySelector('.inline-citation:last-of-type');
      if (text.querySelectorAll('.unverified-mark').length !== 1 || !before?.endsWith(%s) ||
          !after?.startsWith(%s) || !citation ||
          !(mark.compareDocumentPosition(citation) & Node.DOCUMENT_POSITION_FOLLOWING)) {
        throw new Error('Newline boundary %s: ' + JSON.stringify({before, after}));
      }
      return 'PASS: %s marks the bad sentence before the next valid cited sentence';
    })()''' % (json.dumps(bad), json.dumps(valid), name, name), assertion=True)
    evaluate('document.querySelector("article:last-child .answer-text").scrollIntoView({block:"center"})')
    run('screenshot', str(OUT / 'evidence' / f'{PHASE}-{name}.png'))
run('console'); run('errors'); run('close')
summary = {'phase': PHASE, 'commands': len(LOG), 'failures': FAILURES,
           'pass_assertions': sum(x['stdout'].count('PASS:') for x in LOG)}
(OUT / f'{PHASE}-summary.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
sys.exit(1 if FAILURES else 0)
