import type { Citation } from './events';

export function Answer({ text, citations, onSource }: {
  text: string; citations: Citation[]; onSource: (citation: Citation) => void;
}) {
  const byId = new Map(citations.map(citation => [citation.id, citation]));
  return <div className="answer-text">{text.split(/(\[C\d+\])/g).map((text, i) => {
    const citation = byId.get(text.slice(1, -1));
    return citation ? <button key={i} className="citation" onClick={() => onSource(citation)}
      aria-label={`View ${citation.id}, page ${citation.page_start}, ${citation.section}`}>
      {text}
    </button> : <span key={i}>{text}</span>;
  })}</div>;
}
