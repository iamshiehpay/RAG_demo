import type { Citation, LLMCallTrace, StageEvent } from './events';

export function pageRange(source: Pick<Citation, 'page_start' | 'page_end'>) {
  return source.page_start === source.page_end ? `p.${source.page_start}` : `pp.${source.page_start}–${source.page_end}`;
}

export function UnverifiedMark() {
  return <span className="unverified-mark" role="note">未驗證 · Unverified</span>;
}

export function ThinkingContent({ text }: { text: string }) {
  if (!text) return null;
  return <details className="thinking-content"><summary>模型思考 · Model thinking</summary><pre>{text}</pre></details>;
}

export function ErrorState({ message, onRetry, disabled = false }: {
  message: string; onRetry?: () => void; disabled?: boolean;
}) {
  return <div className="error-state" role="alert"><p>{message}</p>
    {onRetry && <button className="secondary-button" disabled={disabled} onClick={onRetry}>重試 · Retry question</button>}
  </div>;
}

export type AskStage = 'planning' | 'retrieval' | 'thinking' | 'answering' | 'retry' | 'complete' | 'error' | 'rejected';
const askStages = ['判斷問題類型', '檢索', '思考中', '回答中'];
const stageIndex: Record<AskStage, number> = { planning: 0, retrieval: 1, thinking: 2, answering: 3, retry: 3, complete: 4, error: -1, rejected: -1 };
const statusLabels: Record<AskStage, string> = { planning: '判斷問題類型', retrieval: '檢索證據', thinking: '思考中', answering: '暫定 · Provisional', retry: '重新產生中', complete: '回答完成', error: '回答失敗', rejected: '問題過長，請縮短問題' };

export function StageIndicator({ stage }: { stage: AskStage }) {
  return <div className={`stage-indicator stage-${stage}`} role="status">
    <ol aria-label="回答階段">{askStages.map((label, i) => <li key={label}
      aria-current={stageIndex[stage] === i ? 'step' : undefined}
      className={stageIndex[stage] > i ? 'completed' : stageIndex[stage] === i ? 'current' : ''}>{label}</li>)}</ol>
    <span className="answer-status">{statusLabels[stage]}</span>
  </div>;
}

const uploadLabels: Record<StageEvent['stage'], string> = { parsing: '解析', chunking: '切塊', embedding: 'Embedding', complete: '完成' };
export function UploadProgress({ stage, busy, ready, name }: {
  stage: StageEvent | null; busy: boolean; ready: boolean; name?: string;
}) {
  return <div className="upload-progress" role="status">
    <span>{busy ? stage ? `${uploadLabels[stage.stage]} · ${stage.completed} / ${stage.total}` : '正在上傳 Document…' : ready ? `${name} · 完成` : '尚未上傳 Document'}</span>
    {busy && stage && <progress max={Math.max(1, stage.total)} value={stage.completed} aria-label={`${uploadLabels[stage.stage]}進度`} />}
  </div>;
}

/** The scale is always 10K, so calls remain directly comparable. */
export function TokenBar({ call }: { call: LLMCallTrace }) {
  const total = call.estimated_prompt_tokens + call.num_predict;
  const percent = (tokens: number) => `${Math.max(0, Math.min(100, tokens / 100))}%`;
  return <div className="token-bar-group">
    <div className="token-bar-label"><span>Context Budget</span><span>{total.toLocaleString('en-US')} / 10,000</span></div>
    <div className="token-bar" role="meter" aria-label="Context Budget: estimated prompt plus output reservation"
      aria-valuemin={0} aria-valuemax={10000} aria-valuenow={total} aria-valuetext={`${total} of 10000 tokens`}>
      <span className="token-prompt" style={{ width: percent(call.estimated_prompt_tokens) }} />
      <span className="token-reserved" style={{ width: percent(call.num_predict) }} />
    </div>
    <div className="token-bar-scale" aria-hidden="true"><span>0</span><span>10K</span></div>
    <div className="token-bar-key"><span>估算 prompt {call.estimated_prompt_tokens.toLocaleString('en-US')}</span><span>輸出預留 {call.num_predict.toLocaleString('en-US')}</span></div>
    {total > 10000 && <p className="error">Context Budget exceeded</p>}
  </div>;
}
