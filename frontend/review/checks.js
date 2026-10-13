/* Browser acceptance assertions for the three-column chat layout, run in the real rendered document.
   Inject with: agent-browser eval --stdin < review/checks.js
   Set window.__t09.scenario (see scripted-events.js) before asking so scenario-specific checks apply. */
(() => {
  const checks = [];
  const luminance = css => {
    const [r, g, b] = css.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; });
    return .2126 * r + .7152 * g + .0722 * b;
  };
  const contrast = (a, b) => { const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x); return (hi + .05) / (lo + .05); };
  const check = (condition, name) => {
    if (!condition) throw new Error(`FAIL: ${name}`);
    checks.push(`PASS: ${name}`);
  };
  const wide = innerWidth > 900;
  const rect = selector => document.querySelector(selector)?.getBoundingClientRect();
  const text = document.body.innerText;

  // Typography and local assets
  check(getComputedStyle(document.body).fontSize === '16px', '16px body text');
  check(getComputedStyle(document.body).fontFamily.includes('Noto Serif TC'), 'Noto Serif TC family');
  check([...document.fonts].some(font => font.family === 'Noto Serif TC' && font.status === 'loaded'), 'bundled Noto font loaded');
  check(performance.getEntriesByType('resource').every(entry => new URL(entry.name).origin === location.origin || entry.name.startsWith('data:')), 'every request is same-origin (no CDN or external font)');
  check(performance.getEntriesByType('resource').filter(entry => entry.name.includes('.woff')).every(entry => new URL(entry.name).origin === location.origin), 'all font requests local');
  check(![...document.querySelectorAll('*')].some(element => getComputedStyle(element).animationName !== 'none'), 'no decorative animation');
  check(![...document.querySelectorAll('*')].some(element => parseFloat(getComputedStyle(element).transitionDuration) > 0), 'no transitions');

  // Page frame: nothing scrolls horizontally, the page itself never scrolls vertically
  check(document.documentElement.scrollWidth <= innerWidth && document.body.scrollWidth <= innerWidth, 'no page horizontal overflow');
  check(document.documentElement.scrollHeight <= innerHeight + 1, 'page does not scroll; the conversation scrolls on its own');
  const messages = document.querySelector('.messages');
  check(['auto', 'scroll'].includes(getComputedStyle(messages).overflowY), 'conversation scrolls independently');

  // Removed copy
  check(!text.includes('讓每個回答'), 'old header slogan removed');
  check(!/Question\s*\d\d/.test(text) && !text.includes('02 / Conversation'), 'Question numbering and section labels removed');
  check(!text.includes('Model thinking') && !text.includes('模型思考') && !text.includes('Unverified') && !text.includes('Choose File') && !text.includes('No file chosen'), 'default UI has no model-thinking label');
  check(!document.querySelector('dialog') && !document.querySelector('.margin-citation'), 'no source dialog or margin notes');
  check(!document.querySelector('[role=log]') && [...document.querySelectorAll('.answer-text')].every(el => !el.closest('[aria-live=polite],[aria-live=assertive]')), 'streamed answer text is not a live region');

  // Three columns
  const composer = rect('.composer');
  check(Math.abs(composer.bottom - innerHeight) < 2, 'input is pinned at the bottom of the middle column');
  const left = rect('.pane-left') ?? rect('.rail-left');
  const chat = rect('.chat');
  const right = rect('.pane-right') ?? rect('.rail-right');
  check(left && chat && right, 'left, middle and right columns exist');
  if (wide) {
    check(left.right <= chat.left + 1 && chat.right <= right.left + 1, 'columns are laid out left to right');
    for (const [sel, name] of [['.rail-left', 'left'], ['.rail-right', 'right']]) {
      const rail = rect(sel);
      if (rail) check(Math.abs(rail.width - 56) < 1, `collapsed ${name} column is a 56px strip`);
    }
  }
  check(document.querySelector('.pane-left, .rail-left').querySelector('button[aria-label]') !== null, 'column toggles are labelled buttons');
  check([...document.querySelectorAll('.icon-button')].every(button => button.getAttribute('aria-label')), 'icon buttons have aria-label');

  // Narrow screens: panes are overlays and must not cover the conversation unless the person opened one
  if (!wide && document.querySelector('article.turn')) {
    check(!document.querySelector('.pane') || window.__t09?.overlayExpected, 'no overlay covers the conversation unless opened');
  }
  if (!wide && window.__t09?.overlayExpected === 'right') {
    check(document.querySelector('.pane-right')?.contains(document.activeElement), 'opening the source overlay moves focus into it');
    check(!document.querySelector('.pane-left'), 'only one overlay is open at a time');
  }
  // Upload control is Chinese and keyboard reachable (no native English file label)
  const fileInput = document.querySelector('#document');
  const fileLabel = document.querySelector('label[for=document]');
  if (fileInput && fileLabel && document.querySelector('.pane-left')) {
    check(/^(選擇 PDF|換一份文件)$/.test(fileLabel.textContent.trim()), 'upload button label is Chinese');
    check(fileInput.getBoundingClientRect().width <= 1 && fileInput.tabIndex === 0, 'native file input is visually hidden but focusable');
  }
  // Tables never split a number; wide tables scroll inside their box and say so
  for (const box of document.querySelectorAll('.scroll-box')) {
    const decimals = [];
    const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      for (const match of node.data.matchAll(/\d+[.,]\d+/g)) {
        const range = document.createRange();
        range.setStart(node, match.index); range.setEnd(node, match.index + match[0].length);
        decimals.push(new Set([...range.getClientRects()].map(rect => Math.round(rect.top))).size);
      }
    }
    check(decimals.every(lines => lines <= 1), `no decimal number splits across lines in a table (${decimals.length} checked)`);
    const overflowing = box.scrollWidth > box.clientWidth + 1;
    check(!overflowing || (getComputedStyle(box).overflowX === 'auto' && box.parentElement.querySelector('.scroll-hint')), 'overflowing table scrolls and shows the 表格較寬 hint');
    check(overflowing || !box.parentElement.querySelector('.scroll-hint'), 'hint hidden when the table fits');
    if (window.__t09?.scenario === 'widetable' && box.closest('.answer-text') && innerWidth <= 920) {
      check(overflowing, 'ten-column table scrolls horizontally at narrow widths');
    }
  }

  // Composer: Enter during IME composition must not submit
  const input = document.querySelector('#question');
  if (input && !input.disabled) {
    const before = document.querySelectorAll('article.turn').length;
    input.value = '';
    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, isComposing: true }));
    check(document.querySelectorAll('article.turn').length === before, 'Enter while composing does not submit');
  }

  // Latest turn
  const turn = document.querySelector('article.turn:last-child');
  if (turn) {
    const scenario = window.__t09?.scenario;
    const answerText = turn.querySelector('.answer-text');
    const bubble = turn.querySelector('.user-bubble').getBoundingClientRect();
    const column = turn.getBoundingClientRect();
    check(column.right - bubble.right < 2 && bubble.left > column.left, 'question is a right-aligned bubble');
    check(turn.querySelector('.answer-process > summary .process-title')?.textContent === '回答過程' || scenario === 'provisional' || scenario === 'retry', '回答過程 replaces Trace');
    check(!/\bTrace\b/.test(turn.innerText), 'no Trace wording in the turn');
    if (scenario === 'retry') check(!answerText.textContent.trim() && turn.textContent.includes('重新產生中'), 'retry clears provisional answer');
    else if (scenario === 'error') check(!answerText.textContent.trim() && turn.querySelector('.error-state button'), 'failure clears answer and offers 重試');
    else {
      const chips = turn.querySelectorAll('.inline-citation');
      check(chips.length > 0, 'inline citation buttons rendered inside the sentence');
      check([...chips].every(chip => chip.tagName === 'BUTTON' && chip.closest('p, li, td')), 'citation chips are real buttons inside answer text');
    }
    if (scenario === 'provisional') check(turn.querySelector('.provisional-text') && turn.textContent.includes('暫定'), 'streaming answer visibly provisional');
    if (scenario === 'unverified') check(turn.querySelector('.unverified-mark'), 'Unverified marker visible');
    if (scenario === 'markdown' || scenario === 'compare' || scenario === 'widetable') {
      const table = answerText.querySelector('table');
      check(table, 'Markdown table renders');
      const box = table.closest('.scroll-box');
      check(box && getComputedStyle(box).overflowX === 'auto', 'table sits in an overflow-x:auto box');
      check(box.getBoundingClientRect().right <= chat.right + 1, 'table box stays inside the middle column');
    }
    if (scenario === 'markdown') {
      check(answerText.querySelector('strong') && answerText.querySelector('em'), 'Markdown emphasis renders');
      check(!window.__unsafe && !answerText.querySelector('script') && !answerText.querySelector('a[href^="javascript:"]'), 'HTML and unsafe URL disabled');
      check(!answerText.textContent.includes('**Safe bold**'), 'raw Markdown delimiters absent');
    }
    check([...turn.querySelectorAll('.thinking-content, .tech-details')].every(element => !element.open), 'thinking and technical details collapsed by default');
    const process = turn.querySelector('.answer-process');
    if (process) process.open = true; // measure bars in the expanded view
    const meters = turn.querySelectorAll('[role=meter]');
    for (const meter of meters) {
      check(contrast(getComputedStyle(meter.querySelector('.token-reserved')).backgroundColor, getComputedStyle(meter).backgroundColor) >= 3, 'reserved-output color has at least 3:1 contrast against the track');
      check(meter.getAttribute('aria-valuemax') === '10000', 'token meter has fixed 10,000 scale');
      const encodedWidth = [...meter.children].reduce((sum, span) => sum + span.getBoundingClientRect().width, 0);
      check(Math.abs(encodedWidth / meter.getBoundingClientRect().width - Number(meter.getAttribute('aria-valuenow')) / 10000) < .002, 'token bar width matches reserved Context Budget ratio');
    }
  }
  return { checks, fontBytes: performance.getEntriesByType('resource').filter(entry => entry.name.includes('.woff')).reduce((sum, entry) => sum + entry.transferSize, 0), viewport: [innerWidth, innerHeight] };
})();
