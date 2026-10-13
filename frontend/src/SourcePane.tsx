import type { Ref } from 'react';
import type { Chunk } from './events';
import { ErrorState, pageRange } from './Shared';
import { SourceContent } from './SourceContent';

export interface SummarySource {
  id: string; kind: 'section' | 'group' | 'document'; section: string;
  page_start: number; page_end: number; text: string; section_titles: string[];
}
export type SourceContentData = Chunk | SummarySource;

function sourceLabel(source: SourceContentData) {
  if ('section_titles' in source) {
    return source.kind === 'group' ? 'Group 摘要' : source.kind === 'document' ? '文件概覽' : 'Section 摘要';
  }
  return source.kind === 'table' ? '表格' : '原文段落';
}

/** Right column: shows the text behind a clicked Citation. Both typed Chunk and Summary sources keep provenance. */
export function SourcePane({ source, citationId, loading, error, headingRef }: {
  source: SourceContentData | null; citationId: string; loading: boolean; error: string; headingRef?: Ref<HTMLDivElement>;
}) {
  const summary = source && 'section_titles' in source ? source : null;
  const empty = !source && !loading && !error;
  return <div className="source-pane" aria-live="polite">
    {empty && <p className="muted pane-hint">點回答中的來源編號（例如 C1），這裡就會顯示那一段原文。</p>}
    {(loading || source || error) && <div className="source-heading" ref={headingRef} tabIndex={-1}>
      <p className="label">{citationId ? `${citationId} · ` : ''}{source ? sourceLabel(source) : '來源'}</p>
      {source && <>
        <p className="source-location">{pageRange(source)} · {source.section}</p>
      </>}
    </div>}
    {loading && <p role="status" className="muted">正在讀取原文…</p>}
    {error && <ErrorState message={error} />}
    {summary && <div className="covered-sections"><p className="label">涵蓋章節</p>
      <ul aria-label="涵蓋章節">{summary.section_titles.map((title, i) => <li key={i}>{title}</li>)}</ul></div>}
    {source && <div className="source-body">
      {summary ? <pre className="source-text">{summary.text}</pre> : <SourceContent source={source as Chunk} />}
    </div>}
  </div>;
}
