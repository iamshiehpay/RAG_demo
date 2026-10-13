import { useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import type { Chunk } from './events';

/** Horizontal scroll box for tables; shows a visible hint whenever the content is wider than the box. */
export function ScrollBox({ label, children }: { label: string; children: ReactNode }) {
  const box = useRef<HTMLDivElement>(null);
  const [wide, setWide] = useState(false);
  useEffect(() => {
    const element = box.current;
    if (!element) return;
    const measure = () => setWide(element.scrollWidth > element.clientWidth + 1);
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    if (element.firstElementChild) observer.observe(element.firstElementChild);
    return () => observer.disconnect();
  }, [children]);
  return <div className="scroll-wrap">
    <div className="scroll-box" ref={box} tabIndex={0} role="region" aria-label={label}>{children}</div>
    {wide && <p className="scroll-hint" role="note">表格較寬，可左右捲動</p>}
  </div>;
}

/** Typed source fields come from the parser; model output never supplies table cells. */
export function SourceContent({ source }: { source: Chunk }) {
  if (source.kind !== 'table') return <pre className="source-text">{source.text}</pre>;
  if (!source.table_reconstructed) return <>
    <p className="table-limitation" role="note">結構未能可靠重建：以下是未整理的原始文字，欄與列的對應可能不準確，請對照原文。</p>
    <pre className="source-text">{source.text}</pre>
  </>;
  return <>
    {source.table_caption && <p className="table-caption">{source.table_caption}</p>}
    {source.table_meaning && <p className="table-meaning">{source.table_meaning}</p>}
    <ScrollBox label={`${source.table_label ?? ''} 表格，可左右捲動`}>
      <table className="source-table" aria-label={source.table_caption ?? source.table_label ?? undefined}>
        <thead><tr>{source.table_headers.map((header, i) => <th scope="col" key={i}>{header}</th>)}</tr></thead>
        <tbody>{source.table_rows.map((row, i) => <tr key={i}>{row.map((cell, j) => j === 0
          ? <th scope="row" key={j}>{cell}</th> : <td key={j}>{cell}</td>)}</tr>)}</tbody>
      </table>
    </ScrollBox>
  </>;
}
