/* Browser acceptance assertions, run in the real rendered document. */
(() => {
  const checks = [];
  const check = (condition, name) => {
    if (!condition) throw new Error(`FAIL: ${name}`);
    checks.push(`PASS: ${name}`);
  };
  check(getComputedStyle(document.body).fontSize === '16px', '16px body text');
  check(getComputedStyle(document.body).fontFamily.includes('Noto Serif TC'), 'Noto Serif TC family');
  check([...document.fonts].some(font => font.family === 'Noto Serif TC' && font.status === 'loaded'), 'bundled Noto font loaded');
  check(document.documentElement.scrollWidth <= window.innerWidth, 'no page horizontal overflow');
  check(performance.getEntriesByType('resource').filter(entry => entry.name.includes('.woff')).every(entry => new URL(entry.name).origin === location.origin), 'all font requests local');
  check(![...document.querySelectorAll('*')].some(element => getComputedStyle(element).animationName !== 'none'), 'no decorative animation');
  const turn = document.querySelector('article:last-child');
  if (turn) {
    const scenario = window.__t09?.scenario;
    const text = turn.querySelector('.answer-text');
    if (scenario === 'retry') check(!text.textContent.trim() && turn.textContent.includes('重新產生中'), 'retry clears provisional answer');
    else if (scenario === 'error') check(!text.textContent.trim() && turn.querySelector('.error-state button'), 'failure clears answer and offers Retry');
    else {
      check(turn.querySelectorAll('.margin-citation').length > 0, 'Citation margin notes rendered');
      check(turn.querySelectorAll('.inline-citation').length > 0, 'inline Citation buttons rendered');
      if (innerWidth > 600) {
        const row = turn.querySelector('.answer-row');
        check(row.querySelector('.margin-citations').getBoundingClientRect().left > row.querySelector('.answer-paragraph').getBoundingClientRect().right, 'Citations in right margin');
      }
    }
    if (scenario === 'provisional') check(turn.querySelector('.provisional-text') && turn.textContent.includes('暫定'), 'streaming answer visibly provisional');
    if (scenario === 'unverified') check(turn.querySelector('.unverified-mark'), 'Unverified marker visible');
    if (scenario === 'markdown') {
      check(text.querySelector('strong') && text.querySelector('em') && text.querySelector('table'), 'Markdown emphasis and table render');
      check(!window.__unsafe && !text.querySelector('script') && !text.querySelector('a[href^="javascript:"]'), 'HTML and unsafe URL disabled');
      check(!text.textContent.includes('**Safe bold**'), 'raw Markdown delimiters absent');
    }
    const meters = turn.querySelectorAll('[role=meter]');
    for (const meter of meters) {
      check(meter.getAttribute('aria-valuemax') === '10000' && meter.parentElement.textContent.includes('10K'), 'token meter has fixed 10K scale/tick');
      const encodedWidth = [...meter.children].reduce((sum, span) => sum + span.getBoundingClientRect().width, 0);
      check(Math.abs(encodedWidth / meter.getBoundingClientRect().width - Number(meter.getAttribute('aria-valuenow')) / 10000) < .002, 'token bar width matches reserved Context Budget ratio');
    }
    check([...turn.querySelectorAll('.thinking-content')].every(element => !element.open), 'thinking collapsed by default');
  }
  return { checks, fontBytes: performance.getEntriesByType('resource').filter(entry => entry.name.includes('.woff')).reduce((sum, entry) => sum + entry.transferSize, 0), viewport: [innerWidth, innerHeight] };
})();
