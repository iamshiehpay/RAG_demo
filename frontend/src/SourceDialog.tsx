import { useEffect, useRef } from 'react';
import type { Chunk } from './events';
import { ErrorState, pageRange } from './Shared';
import { SourceContent } from './SourceContent';

export interface SummarySource {
  id: string; kind: 'section' | 'group' | 'document'; section: string;
  page_start: number; page_end: number; text: string; section_titles: string[];
}

/** Both typed Chunk and Summary sources retain their backend provenance. */
export function SourceDialog({ source, kind = 'Chunk', loading = false, error = '', onClose }: {
  source: Chunk | SummarySource | null; kind?: 'Chunk' | 'Section Summary';
  loading?: boolean; error?: string; onClose: () => void;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const returnFocus = useRef(document.activeElement);
  useEffect(() => {
    const element = dialog.current;
    const previousFocus = returnFocus.current;
    if (element && !element.open) element.showModal();
    return () => {
      if (element?.open) element.close();
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus();
    };
  }, []);
  const summary = source && 'section_titles' in source ? source : null;
  const label = summary ? summary.kind === 'group' ? 'Group Summary' : summary.kind === 'document' ? 'Document Summary' : 'Section Summary'
    : source?.kind === 'table' ? 'Table Chunk' : kind;
  return <dialog ref={dialog} className="source-dialog" onCancel={onClose} aria-labelledby="source-title">
    <header className="source-heading"><div><p className="eyebrow">Citation / {label}</p>
      <h2 id="source-title">{source ? `${pageRange(source)} · ${source.section}` : 'Citation source'}</h2></div>
      <button className="secondary-button" onClick={onClose} autoFocus>關閉 · Close source</button>
    </header>
    {loading && <p role="status">正在讀取原文…</p>}
    {error && <ErrorState message={error} />}
    {summary && <ul aria-label="Covered Sections">{summary.section_titles.map((title, i) => <li key={i}>{title}</li>)}</ul>}
    {source && ('section_titles' in source ? <pre className="source-text">{source.text}</pre> : <SourceContent source={source} />)}
  </dialog>;
}
