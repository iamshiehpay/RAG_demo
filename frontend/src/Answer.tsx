import { isValidElement, useMemo } from 'react';
import type { ReactNode } from 'react';
import Markdown from 'react-markdown';
import type { Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { decodeString } from 'micromark-util-decode-string';
import { visit } from 'unist-util-visit';
import type { Root, RootContent as MarkdownContent, PhrasingContent, Parents } from 'mdast';
import type { Element as HastElement, ElementContent, Root as HastRoot } from 'hast';
import type { Citation, UnverifiedSpan } from './events';
import { pageRange, UnverifiedMark } from './Shared';
import { ScrollBox } from './SourceContent';

/** Align raw Markdown positions with a decoded text node without moving sentence marks. */
function sourceValueOffsets(source: string, value: string): number[] | undefined {
  const offsets = [0];
  let raw = 0;
  let rendered = 0;
  let linePrefix = true;
  while (raw < source.length) {
    const reference = /^(?:\\[!-/:-@[-`{-~]|&(?:#(?:\d{1,7}|[xX][\da-fA-F]{1,6})|[\da-zA-Z]{1,31});)/.exec(source.slice(raw));
    const token = reference?.[0] ?? (source.startsWith('\r\n', raw) ? '\r\n' : source[raw]);
    // mdast keeps CR/CRLF verbatim, so preserve their widths when mapping positions.
    const decoded = reference ? decodeString(token) : token;
    if (value.startsWith(decoded, rendered)) {
      for (let i = 1; i <= token.length; i++) offsets[raw + i] = rendered + decoded.length;
      raw += token.length;
      rendered += decoded.length;
      if (decoded === '\n' || decoded === '\r' || decoded === '\r\n') linePrefix = true;
      else if (!/^[ \t]*$/.test(decoded)) linePrefix = false;
    } else if (linePrefix && /[ \t>]/.test(source[raw])) {
      // List indentation and blockquote prefixes are absent from mdast text values.
      offsets[++raw] = rendered;
    } else {
      return undefined;
    }
  }
  return rendered === value.length ? offsets : undefined;
}

const BLOCK_TAGS = new Set(['p', 'ul', 'ol', 'li', 'pre', 'blockquote', 'table', 'thead', 'tbody', 'tr', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']);
// Containers whose children are all blocks: any whitespace between them is structural.
const BLOCK_ONLY = new Set(['ul', 'ol', 'blockquote', 'table', 'thead', 'tbody', 'tr']);
const isBlock = (node: ElementContent | undefined) => node?.type === 'element' && BLOCK_TAGS.has(node.tagName);
/** Markdown parsers keep the newline between block children as text. Answer paragraphs and list items preserve
 *  soft line breaks (white-space: pre-wrap), so those structural newlines would otherwise render as blank lines.
 *  Only newline-only text beside a block child is dropped: a plain space between inline children
 *  ("**a** **b**", "`x` `y`", "text [link](u) more") is content and must stay. */
function trimStructuralWhitespace() {
  return (tree: HastRoot) => {
    visit(tree, 'element', (node: HastElement) => {
      if (node.tagName !== 'li' && !BLOCK_ONLY.has(node.tagName)) return;
      const children = node.children;
      node.children = children.filter((child, i) => {
        if (child.type !== 'text' || child.value.trim() !== '') return true;
        if (BLOCK_ONLY.has(node.tagName)) return false;
        return !(child.value.includes('\n') && (isBlock(children[i - 1]) || isBlock(children[i + 1])));
      });
      if (node.tagName !== 'li') return;
      node.children.forEach((child, i) => {
        // "item text\n" directly before a nested list: the break belongs to the block boundary.
        const next = node.children[i + 1];
        if (child.type === 'text' && next?.type === 'element' && (next.tagName === 'ul' || next.tagName === 'ol')) {
          child.value = child.value.replace(/\s+$/, '');
        }
      });
    });
  };
}

function plainText(node: ReactNode): string {
  if (typeof node === 'string' || typeof node === 'number') return String(node);
  if (Array.isArray(node)) return node.map(plainText).join('');
  if (isValidElement<{ children?: ReactNode }>(node)) return plainText(node.props.children);
  return '';
}
const numericCell = (children: ReactNode) => { const text = plainText(children); return /\d/.test(text) && text.length <= 24; };

export function Answer({ text, citations, onSource, provisional = false, unverified = [] }: {
  text: string; citations: Citation[]; onSource: (citation: Citation) => void;
  provisional?: boolean; unverified?: UnverifiedSpan[];
}) {
  // Python offsets count Unicode code points; Markdown positions use UTF-16.
  const characters = Array.from(text);
  function unverifiedSpans() {
    return (tree: Root) => {
      const targets = new Map<MarkdownContent, { parent: Parents; marks: number[] }>();
      for (const span of unverified) {
        const start = characters.slice(0, span.start).join('').length;
        const end = characters.slice(0, span.end).join('').length;
        let target: { node: MarkdownContent; parent: Parents; score: number } | undefined;
        visit(tree, (node, _index, parent) => {
          if (!parent || !['text', 'inlineCode', 'code', 'html', 'link', 'image'].includes(node.type)) return;
          if (parent.type === 'link' || parent.type === 'linkReference') return;
          const from = node.position?.start.offset;
          const to = node.position?.end.offset;
          if (from === undefined || to === undefined || from >= end || to <= start) return;
          const score = Math.min(to, end);
          if (!target || score >= target.score) target = { node: node as MarkdownContent, parent, score };
        });
        if (target) {
          const existing = targets.get(target.node) ?? { parent: target.parent, marks: [] };
          existing.marks.push(end);
          targets.set(target.node, existing);
        }
      }
      for (const [node, { parent, marks }] of targets) {
        const marker = (): PhrasingContent => ({ type: 'link', url: '#unverified',
          data: { hProperties: { 'data-unverified': true } },
          children: [{ type: 'text', value: '未驗證' }] });
        const replacements: MarkdownContent[] = [];
        const from = node.position?.start.offset ?? 0;
        const to = node.position?.end.offset ?? from;
        const valueOffsets = node.type === 'text' ? sourceValueOffsets(text.slice(from, to), node.value) : undefined;
        if (node.type === 'text' && valueOffsets) {
          let offset = 0;
          for (const end of marks.sort((a, b) => a - b)) {
            const next = valueOffsets[Math.max(0, Math.min(to - from, end - from))];
            replacements.push({ type: 'text', value: node.value.slice(offset, next) }, marker());
            offset = next;
          }
          replacements.push({ type: 'text', value: node.value.slice(offset) });
        } else {
          // Code/HTML or unalignable text remains intact. Put the label beside its node,
          // rather than injecting Markdown into a code span, link, or table syntax.
          replacements.push(node);
          for (const _end of marks) replacements.push(parent.type === 'root'
            ? { type: 'paragraph', children: [marker()] } : marker());
        }
        const children = parent.children as MarkdownContent[];
        children.splice(children.indexOf(node), 1, ...replacements);
      }
    };
  }
  const byId = new Map(citations.map(citation => [citation.id, citation]));
  // Convert only recognized Citation text tokens into safe, internal Markdown links.
  // HTML and code nodes are never interpreted as Citation text.
  function citationTokens() {
    return (tree: Root) => {
      visit(tree, 'text', (node, index, parent) => {
        if (!parent || index === undefined || parent.type === 'link' || parent.type === 'linkReference') return;
        const replacements: PhrasingContent[] = [];
        let start = 0;
        for (const match of node.value.matchAll(/\[([CS]\d+)\]/g)) {
          if (match[1] && !byId.has(match[1])) continue;
          if (match.index > start) replacements.push({ type: 'text', value: node.value.slice(start, match.index) });
          replacements.push({ type: 'link', url: `#citation-${match[1]}`,
            children: [{ type: 'text', value: match[0] }] });
          start = match.index + match[0].length;
        }
        if (!replacements.length) return;
        if (start < node.value.length) replacements.push({ type: 'text', value: node.value.slice(start) });
        parent.children.splice(index, 1, ...replacements);
        return index + replacements.length;
      });
    };
  }

  // Stable renderers keep Citation triggers mounted while the source pane updates.
  const components = useMemo<Components>(() => ({
      table: ({ children }) => <ScrollBox label="表格，可左右捲動"><table>{children}</table></ScrollBox>,
      // Short cells holding a number never wrap, so a wide table scrolls instead of splitting "11.1".
      th: ({ node: _node, children, ...rest }) => <th {...rest} className={numericCell(children) ? 'num-cell' : undefined}>{children}</th>,
      td: ({ node: _node, children, ...rest }) => <td {...rest} className={numericCell(children) ? 'num-cell' : undefined}>{children}</td>,
      a: ({ children, href, node }) => {
        if (node?.properties['data-unverified']) return <UnverifiedMark />;
        const citation = href?.startsWith('#citation-') ? byId.get(href.slice(10)) : undefined;
        return citation ? <button className="inline-citation" onClick={event => { event.currentTarget.focus(); onSource(citation); }}
          aria-label={`查看來源 ${citation.id}，${pageRange(citation)}，${citation.section}`}
          title={`${pageRange(citation)} · ${citation.section}`}>{citation.id}</button> :
          <a href={href} rel="noreferrer">{children}</a>;
      },
    }), [citations, onSource, unverified]);

  return <div className={`answer-text${provisional ? ' provisional-text' : ''}`} data-unverified-count={unverified.length}>
    <Markdown skipHtml remarkPlugins={[remarkGfm, unverifiedSpans, citationTokens]} rehypePlugins={[trimStructuralWhitespace]} components={components}>{text}</Markdown>
  </div>;
}
