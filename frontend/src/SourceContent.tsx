import type { Chunk } from './events';

/** Typed source fields come from the parser; model output never supplies table cells. */
export function SourceContent({ source }: { source: Chunk }) {
  if (source.kind !== 'table') return <pre className="source-text">{source.text}</pre>;
  if (!source.table_reconstructed) return <>
    <p className="table-limitation" role="note">結構未能可靠重建：以下是未整理的原始文字，欄與列的對應可能不準確，請對照原文。</p>
    <pre className="source-text">{source.text}</pre>
  </>;
  return <>
    {source.table_meaning && <p>{source.table_meaning}</p>}
    <div className="source-table-scroll" tabIndex={0} role="region" aria-label={`${source.table_label ?? ''} 表格，可左右捲動`}>
      <table className="source-table">
        <caption>{source.table_caption}</caption>
        <thead><tr>{source.table_headers.map((header, i) => <th scope="col" key={i}>{header}</th>)}</tr></thead>
        <tbody>{source.table_rows.map((row, i) => <tr key={i}>{row.map((cell, j) => j === 0
          ? <th scope="row" key={j}>{cell}</th> : <td key={j}>{cell}</td>)}</tr>)}</tbody>
      </table>
    </div>
  </>;
}
