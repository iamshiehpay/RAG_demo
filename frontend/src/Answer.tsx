import type { Citation } from './events';
import { UnverifiedMark } from './Shared';

export function Answer({ text, citations, onSource, provisional = false, unverified = [] }: {
  text: string; citations: Citation[]; onSource: (citation: Citation) => void;
  provisional?: boolean; unverified?: string[];
}) {
  const byId = new Map(citations.map(citation => [citation.id, citation]));
  return <div className={`answer-text${provisional ? ' provisional-text' : ''}`}
    data-unverified-count={unverified.length}>{text.split(/(\[[CS]\d+\]|未驗證)/g).map((text, i) => {
    if (text === '未驗證') return <UnverifiedMark key={i} />;
    const citation = byId.get(text.slice(1, -1));
    return citation ? <button key={i} className="citation" onClick={() => onSource(citation)}
      aria-label={`View ${citation.id}, page ${citation.page_start}, ${citation.section}`}>
      {text}
    </button> : <span key={i}>{text}</span>;
  })}</div>;
}
