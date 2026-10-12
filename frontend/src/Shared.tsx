/** Minimal state components; #09 supplies the final design. */
import type { StageEvent } from './events';

export function UploadProgress({ stage, busy, ready, name }: {
  stage: StageEvent | null; busy: boolean; ready: boolean; name?: string;
}) {
  const labels = { parsing: '解析', chunking: '切塊', embedding: 'Embedding', summary: '摘要', complete: '完成' };
  return <div role="status" aria-live="polite">
    {busy ? <>
      <p>{stage ? `${labels[stage.stage]} · ${stage.completed}/${stage.total}` : 'Uploading Document…'}</p>
      {stage && <progress aria-label={labels[stage.stage]} value={stage.completed} max={Math.max(1, stage.total)} />}
    </> : ready ? <p>{name} · Ready</p> : <p>Upload a PDF with a text layer to begin.</p>}
  </div>;
}

export function UnverifiedMark() {
  return <span className="unverified-mark" role="note">未驗證 · Unverified</span>;
}

export function ThinkingContent({ text }: { text: string }) {
  if (!text) return null;
  return <details className="thinking-content"><summary>Model thinking</summary><pre>{text}</pre></details>;
}
