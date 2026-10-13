import { useState } from 'react';
import type { ReadyEvent, StageEvent } from './events';
import { Answer } from './Answer';
import { EMBEDDING_MODEL, LLM_MODEL } from './models';
import { ErrorState, UploadProgress } from './Shared';

/** Left column: choose or replace the Document, show processing state and the Document Summary. */
export function DocumentPane({ document, uploadName, uploading, busy, uploadStage, canReconnect, error, onUpload, onReconnect }: {
  document: ReadyEvent | null; uploadName: string; uploading: boolean; busy: boolean; uploadStage: StageEvent | null;
  canReconnect: boolean; error: string; onUpload: (file: File) => void; onReconnect: () => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const summary = document?.document_summary ?? null;
  return <div className="document-pane">
    <section className="upload" aria-label="上傳文件">
      <p className="doc-name">{uploading ? uploadName : document ? document.name : '尚未選擇檔案'}</p>
      <input id="document" className="visually-hidden" type="file" accept="application/pdf,.pdf" disabled={busy || uploading}
        onChange={event => { const file = event.target.files?.[0]; if (file) onUpload(file); event.target.value = ''; }} />
      <label className="file-button" htmlFor="document">{document ? '換一份文件' : '選擇 PDF'}</label>
      <p className="file-help">支援有文字層的 PDF；換文件會清空目前的對話。</p>
      {uploading && <UploadProgress stage={uploadStage} busy ready={false} />}
      {document && !uploading && <p className="document-meta">處理完成 · {document.chunk_count} 段原文 · 可提問</p>}
      {canReconnect && <button className="secondary-button" onClick={onReconnect}>重新連線，取得處理進度</button>}
      {error && <ErrorState message={error} />}
    </section>
    <section className="document-overview" aria-label="文件概覽">
      <p className="label">文件概覽</p>
      {summary ? <>
        <div className={`overview-text${expanded ? '' : ' clamped'}`}><Answer text={summary} citations={[]} onSource={() => {}} /></div>
        {summary.length > 120 && <button className="link-button" aria-expanded={expanded} onClick={() => setExpanded(value => !value)}>
          {expanded ? '收合概覽' : '展開全文概覽'}</button>}
      </> : <p className="muted">{document ? '此版本尚未提供文件概覽。' : '處理完成後，文件概覽會顯示在這裡。'}</p>}
    </section>
    <p className="model-note muted">回答模型 {LLM_MODEL} · 檢索模型 {EMBEDDING_MODEL}</p>
  </div>;
}
