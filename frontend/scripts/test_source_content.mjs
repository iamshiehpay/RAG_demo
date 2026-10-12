import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { runInNewContext } from 'node:vm';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import ts from 'typescript';

const code = ts.transpileModule(readFileSync(new URL('../src/SourceContent.tsx', import.meta.url), 'utf8'), {
  compilerOptions: { jsx: ts.JsxEmit.ReactJSX, module: ts.ModuleKind.CommonJS },
}).outputText;
const exports = {};
runInNewContext(code, { exports, require: createRequire(import.meta.url) });
const source = {
  kind: 'table', table_reconstructed: false, text: 'raw <cell> 12',
  table_label: 'Table 7', table_caption: 'Measured values',
  table_headers: ['Experiment', 'Count'], table_rows: [['alpha', '12']],
};
const uncertain = renderToStaticMarkup(createElement(exports.SourceContent, { source }));
assert.match(uncertain, /role="note"/);
assert.match(uncertain, /結構未能可靠重建/);
assert.match(uncertain, /raw &lt;cell&gt; 12/);
assert.doesNotMatch(uncertain, /<table/);
const grid = renderToStaticMarkup(createElement(exports.SourceContent, {
  source: { ...source, table_reconstructed: true },
}));
assert.match(grid, /<caption>Measured values<\/caption>/);
assert.match(grid, /<th scope="row">alpha<\/th><td>12<\/td>/);
assert.doesNotMatch(grid, /role="note"/);
console.log('SourceContent: uncertain source note and reconstructed cells passed');
