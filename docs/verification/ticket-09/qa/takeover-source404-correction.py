"""Correct overly specific QA error-copy expectation; no product change."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent;src=(p/'takeover-scripted.py').read_text().split("run('reload');run('set'")[0];exec(src.replace('takeover-scripted-','takeover-source404-correction-'))
click('article:last-child .inline-citation');run('wait','--fn',"!!document.querySelector('dialog .error-state')");check('source404 clear accessible error and no stale content',"document.querySelector('dialog .error-state').getAttribute('role')==='alert'&&document.querySelector('dialog .error-state').textContent==='Source not found.'&&!document.querySelector('dialog .source-text,dialog table')");run('press','Escape');check('source404 close restores Citation focus',"!document.querySelector('dialog')&&document.activeElement.classList.contains('inline-citation')");print(json.dumps(RESULTS))
