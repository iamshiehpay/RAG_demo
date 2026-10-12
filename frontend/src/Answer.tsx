import type { ReactNode } from 'react';
import type { Citation, UnverifiedSpan } from './events';
import { UnverifiedMark } from './Shared';

export function Answer({ text, citations, onSource, provisional = false, unverified = [] }: {
  text: string; citations: Citation[]; onSource: (citation: Citation) => void;
  provisional?: boolean; unverified?: UnverifiedSpan[];
}) {
  const byId = new Map(citations.map(citation => [citation.id, citation]));
  const renderText = (text: string, key: string) => text.split(/(\[[CS]\d+\])/g).map((text, i) => {
    const citation = byId.get(text.slice(1, -1));
    return citation ? <button key={`${key}-${i}`} className="citation" onClick={() => onSource(citation)}
      aria-label={`View ${citation.id}, page ${citation.page_start}, ${citation.section}`}>
      {text}
    </button> : <span key={`${key}-${i}`}>{text}</span>;
  });
  // Python offsets count Unicode code points; Array.from preserves the same indices.
  const characters = Array.from(text);
  const content: ReactNode[] = [];
  let offset = 0;
  for (const [i, span] of unverified.entries()) {
    content.push(...renderText(characters.slice(offset, span.start).join(''), `${i}-before`));
    content.push(<span className="unverified-sentence" key={`unverified-${i}`}>
      {renderText(characters.slice(span.start, span.end).join(''), `${i}-sentence`)} <UnverifiedMark />
    </span>);
    offset = span.end;
  }
  content.push(...renderText(characters.slice(offset).join(''), 'after'));
  return <div className={`answer-text${provisional ? ' provisional-text' : ''}`}
    data-unverified-count={unverified.length}>{content}</div>;
}
