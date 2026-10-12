import { useMemo } from 'react';
import type { ReactNode } from 'react';
import Markdown from 'react-markdown';
import type { Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { visit } from 'unist-util-visit';
import type { Root, PhrasingContent } from 'mdast';
import type { Element, RootContent } from 'hast';
import type { Citation, UnverifiedSpan } from './events';
import { pageRange, UnverifiedMark } from './Shared';

export function MarginCitation({ citation, onSource }: { citation: Citation; onSource: (citation: Citation) => void }) {
  return <button className="margin-citation" onClick={event => { event.currentTarget.focus(); onSource(citation); }}
    aria-label={`View ${citation.id}, ${pageRange(citation)}, ${citation.section}`}>
    <span className="citation-location">[{citation.id}] · {pageRange(citation)}</span>
    <span className="citation-section">{citation.section}</span>
  </button>;
}

function nodeText(node: Element | RootContent | undefined): string {
  if (!node) return '';
  if (node.type === 'text') return node.value;
  return 'children' in node ? node.children.map(nodeText).join('') : '';
}

export function Answer({ text, citations, onSource, provisional = false, unverified = [] }: {
  text: string; citations: Citation[]; onSource: (citation: Citation) => void;
  provisional?: boolean; unverified?: UnverifiedSpan[];
}) {
  // Backend spans use Python Unicode code-point offsets, including Markdown.
  // Insert marks at those exact offsets before safe Markdown rendering; never match
  // sentence text, since an identical sentence may be verified elsewhere.
  const characters = Array.from(text);
  const markedText = [...unverified].sort((a, b) => b.end - a.end).reduce((answer, span) => {
    if (span.start < 0 || span.end > characters.length || span.start >= span.end) return answer;
    const offset = characters.slice(0, span.end).join('').length;
    return answer.slice(0, offset) + ' [未驗證 · Unverified](#unverified)' + answer.slice(offset);
  }, text);
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

  function row(children: ReactNode, node?: Element) {
    const content = nodeText(node);
    const ids = [...new Set(Array.from(content.matchAll(/\[([CS]\d+)\]/g), match => match[1]))];
    const notes = ids.flatMap(id => byId.has(id) ? [byId.get(id)!] : []);
    return <div className="answer-row"><div className="answer-paragraph">{children}</div><aside className="margin-citations" aria-label="Citation margin notes">
      {notes.map(citation => <MarginCitation key={citation.id} citation={citation} onSource={onSource} />)}
    </aside></div>;
  }

  // Stable renderers keep Citation triggers mounted during source-dialog updates.
  const components = useMemo<Components>(() => ({
      p: ({ children, node }) => row(children, node),
      li: ({ children, node }) => <li>{node?.children.some(child => child.type === 'element' && child.tagName === 'p')
        ? children : row(children, node)}</li>,
      table: ({ children, node }) => row(<div className="source-table-scroll"><table>{children}</table></div>, node),
      a: ({ children, href }) => {
        if (href === '#unverified') return <UnverifiedMark />;
        const citation = href?.startsWith('#citation-') ? byId.get(href.slice(10)) : undefined;
        return citation ? <button className="inline-citation" onClick={event => { event.currentTarget.focus(); onSource(citation); }}
          aria-label={`View ${citation.id}, ${pageRange(citation)}, ${citation.section}`}>{children}</button> :
          <a href={href} rel="noreferrer">{children}</a>;
      },
    }), [citations, onSource, unverified]);

  return <div className={`answer-text${provisional ? ' provisional-text' : ''}`} data-unverified-count={unverified.length}>
    <Markdown skipHtml remarkPlugins={[remarkGfm, citationTokens]} components={components}>{markedText}</Markdown>
  </div>;
}
