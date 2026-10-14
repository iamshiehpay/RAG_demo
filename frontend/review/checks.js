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
    // window.__collectFailures = true records every FAIL instead of stopping at the first (used for the "before" run).
    if (!condition) { if (window.__collectFailures) { checks.push(`FAIL: ${name}`); return; } throw new Error(`FAIL: ${name}`); }
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
      if (rail) {
        check(Math.abs(rail.width - 64) < 1, `collapsed ${name} column is a 64px strip`);
        const label = document.querySelector(`${sel} .rail-label`);
        check(label && /^(文件|來源)$/.test(label.textContent) && parseFloat(getComputedStyle(label).fontSize) >= 14
          && label.getBoundingClientRect().height >= 28, `collapsed ${name} column shows a readable label`);
      }
    }
    // Source pane separator (desktop only): bounds are exposed and the conversation keeps its room
    const separator = document.querySelector('[role=separator]');
    if (document.querySelector('.pane-right')) {
      check(separator && separator.tabIndex === 0 && separator.getAttribute('aria-orientation') === 'vertical', 'source pane has a focusable vertical separator');
      const [now, min, max] = ['aria-valuenow', 'aria-valuemin', 'aria-valuemax'].map(name => Number(separator?.getAttribute(name)));
      check(min <= now && now <= max && Math.abs(now - rect('.pane-right').width) <= 1, 'separator aria values match the pane width and sit inside [min, max]');
      check(chat.width >= 360, 'conversation column keeps at least 360px beside the source pane');
    } else check(!separator, 'no separator while the source pane is collapsed');
  }
  check(document.querySelector('.pane-left, .rail-left').querySelector('button[aria-label]') !== null, 'column toggles are labelled buttons');
  check([...document.querySelectorAll('.icon-button')].every(button => button.getAttribute('aria-label')), 'icon buttons have aria-label');

  if (!wide) check(!document.querySelector('[role=separator]'), 'no separator on narrow screens (dragging is desktop only)');

  // Removed copy (D16): the visible hint and label are gone, the accessible name stays
  const hint = '回答以文件為依據；點回答中的編號可查看原文。';
  check(!text.includes(hint) && !text.includes('問這份文件'), 'hint line and the visible 問這份文件 label are removed');
  check(!document.querySelector('label[for=question]') && document.querySelector('#question')?.getAttribute('aria-label') === '問這份文件', 'textarea keeps an accessible (not visible) label');

  // Click-to-send questions
  const shortcutGroup = document.querySelector('.shortcuts');
  const shortcuts = [...document.querySelectorAll('.shortcuts button')];
  const headerStatus = document.querySelector('.header-status')?.textContent ?? '';
  const lightRag = !headerStatus.includes('·') || /lightrag/i.test(headerStatus); // no Document loaded: the full LightRAG set is shown disabled
  const expectedQuestions = ['Summary this document.', 'Compare LightRAG with GraphRAG.', 'Performance of ablated versions of LightRAG.', '這篇論文有什麼限制？', 'LightRAG 在 HotpotQA 上的分數是多少？'];
  check(shortcutGroup?.getAttribute('role') === 'group' && shortcutGroup.compareDocumentPosition(document.querySelector('.composer-box')) & Node.DOCUMENT_POSITION_PRECEDING, 'shortcut group sits below the composer box');
  check(shortcuts.every(button => button.tagName === 'BUTTON' && button.type === 'button'), 'shortcuts are real, non-submitting buttons');
  if (lightRag) check(JSON.stringify(shortcuts.map(button => button.textContent)) === JSON.stringify(expectedQuestions) && /LightRAG 論文範例問題/.test(shortcutGroup.textContent), 'five exact LightRAG example questions under a LightRAG-labelled group');
  else check(shortcuts.length === 1 && shortcuts[0].textContent === expectedQuestions[0] && !/LightRAG/.test(shortcutGroup.textContent), 'other Documents get only the general summary question, not labelled as LightRAG-specific');
  check(shortcuts.every(button => button.disabled === !!document.querySelector('#question')?.disabled), 'shortcut buttons are disabled exactly when the composer is (no Document, uploading or generating)');

  // Answers: no decorative underline anywhere, Citations stay recognisable chips
  const decorated = [...document.querySelectorAll('.answer-text, .answer-text *, .inline-citation, .unverified-mark, .stage-indicator *')]
    .filter(element => getComputedStyle(element).textDecorationLine !== 'none');
  check(decorated.length === 0, 'no text-decoration underline on answer text, citations, markers or stage labels');
  check([...document.querySelectorAll('.answer-text strong, .answer-text h1, .answer-text h2, .answer-text h3')].every(element => parseFloat(getComputedStyle(element).webkitTextStrokeWidth) > 0), 'emphasis and headings stay distinguishable without an underline (weight stroke)');
  check([...document.querySelectorAll('.answer-text strong, .answer-text a')].every(element => getComputedStyle(element).borderBottomWidth === '0px'), 'emphasis and links use no border-bottom underline');
  for (const chip of document.querySelectorAll('.answer-text .inline-citation')) {
    const style = getComputedStyle(chip);
    check(parseFloat(style.marginLeft) >= 3 && parseFloat(style.borderTopWidth) > 0 && chip.getBoundingClientRect().height <= 22,
      'citation chip is a bordered slate chip with space before it that does not inflate the line');
    break;
  }

  // Answer spacing rhythm: 12px between blocks, 24px above a heading, 8px under it, 4px between list items
  let measuredGaps = 0;
  for (const area of document.querySelectorAll('.answer-text')) {
    const blocks = [...area.children];
    for (let i = 1; i < blocks.length; i++) {
      const [prev, cur] = [blocks[i - 1], blocks[i]];
      const gap = cur.getBoundingClientRect().top - prev.getBoundingClientRect().bottom;
      const expected = /^H[1-6]$/.test(prev.tagName) ? 8 : /^H[1-6]$/.test(cur.tagName) ? 24 : 12;
      check(Math.abs(gap - expected) <= 1, `gap ${prev.tagName}→${cur.tagName} is ${expected}px (got ${gap.toFixed(1)})`);
      measuredGaps++;
    }
    for (const list of area.querySelectorAll('ul, ol')) {
      const items = [...list.children].filter(child => child.tagName === 'LI');
      for (let i = 1; i < items.length; i++) {
        const gap = items[i].getBoundingClientRect().top - items[i - 1].getBoundingClientRect().bottom;
        check(Math.abs(gap - 4) <= 1, `list items are 4px apart (got ${gap.toFixed(1)})`);
        measuredGaps++;
      }
    }
    // A list item holding one paragraph is exactly that paragraph tall: no stray blank line, marker on the text line
    for (const item of area.querySelectorAll('li')) {
      const only = [...item.children].length === 1 && item.firstElementChild.tagName === 'P' ? item.firstElementChild : null;
      if (only) check(Math.abs(item.getBoundingClientRect().height - only.getBoundingClientRect().height) <= 1, 'loose list item has no extra blank line');
    }
  }
  window.__t09 && (window.__t09.measuredGaps = measuredGaps);

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
