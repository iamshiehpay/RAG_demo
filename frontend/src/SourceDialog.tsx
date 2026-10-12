import { useEffect, useRef } from 'react';
import type { Chunk } from './events';
import { ErrorState, pageRange } from './Shared';

export type SourceContent = Pick<Chunk, 'section' | 'page_start' | 'page_end' | 'text'>;
export type SourceTable = { headers: string[]; rows: string[][]; caption?: string };

/** #03/#05 can supply structured tables/Section Summary without changing the dialog. */
export function SourceDialog({ source, kind = 'Chunk', table, loading = false, error = '', onClose }: {
  source: SourceContent | null; kind?: 'Chunk' | 'Table Chunk' | 'Section Summary';
  table?: SourceTable; loading?: boolean; error?: string; onClose: () => void;
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
  return <dialog ref={dialog} className="source-dialog" onCancel={onClose} aria-labelledby="source-title">
    <header className="source-heading"><div><p className="eyebrow">Citation / {kind}</p>
      <h2 id="source-title">{source ? `${pageRange(source)} · ${source.section}` : 'Citation source'}</h2></div>
      <button className="secondary-button" onClick={onClose} autoFocus>關閉 · Close source</button>
    </header>
    {loading && <p role="status">正在讀取原文…</p>}
    {error && <ErrorState message={error} />}
    {source && (table ? <div className="source-table-scroll"><table>
      {table.caption && <caption>{table.caption}</caption>}
      <thead><tr>{table.headers.map((header, i) => <th key={i} scope="col">{header}</th>)}</tr></thead>
      <tbody>{table.rows.map((row, i) => <tr key={i}>{row.map((cell, j) => <td key={j}>{cell}</td>)}</tr>)}</tbody>
    </table></div> : <pre className="source-text">{source.text}</pre>)}
  </dialog>;
}
