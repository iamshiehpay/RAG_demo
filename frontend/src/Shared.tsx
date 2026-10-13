import type { Citation, StageEvent } from './events';

export function pageRange(source: Pick<Citation, 'page_start' | 'page_end'>) {
  return source.page_start === source.page_end ? `p.${source.page_start}` : `pp.${source.page_start}–${source.page_end}`;
}

export function UnverifiedMark() {
  return <span className="unverified-mark" role="note">未驗證</span>;
}

export function ErrorState({ message, onRetry, disabled = false }: {
  message: string; onRetry?: () => void; disabled?: boolean;
}) {
  return <div className="error-state" role="alert"><p>{message}</p>
    {onRetry && <button className="secondary-button" disabled={disabled} onClick={onRetry}>重試這個問題</button>}
  </div>;
}

export type AskStage = 'planning' | 'retrieval' | 'thinking' | 'answering' | 'retry' | 'complete' | 'error' | 'rejected';
const askStages = ['判斷問題類型', '找相關段落', '思考中', '回答中', '完成'];
const stageIndex: Record<AskStage, number> = { planning: 0, retrieval: 1, thinking: 2, answering: 3, retry: 3, complete: 5, error: -1, rejected: -1 };
const statusLabels: Record<AskStage, string> = {
  planning: '判斷問題類型中', retrieval: '正在找相關段落', thinking: '思考中', answering: '暫定，完成後定稿',
  retry: '重新產生中', complete: '回答完成', error: '回答失敗', rejected: '問題過長，請縮短問題',
};

export function StageIndicator({ stage }: { stage: AskStage }) {
  return <div className={`stage-indicator stage-${stage}`} role="status">
    <ol aria-label="回答階段">{askStages.map((label, i) => <li key={label}
      aria-current={stageIndex[stage] === i ? 'step' : undefined}
      className={stageIndex[stage] > i ? 'completed' : stageIndex[stage] === i ? 'current' : ''}>{label}</li>)}</ol>
    <span className="answer-status">{statusLabels[stage]}</span>
  </div>;
}

const uploadLabels: Record<StageEvent['stage'], string> = { parsing: '解析', chunking: '切塊', embedding: '建立向量', summary: '產生摘要', complete: '完成' };
export function UploadProgress({ stage, busy, ready, name }: {
  stage: StageEvent | null; busy: boolean; ready: boolean; name?: string;
}) {
  return <div className="upload-progress" role="status">
    <span>{busy ? stage ? `${uploadLabels[stage.stage]} · ${stage.completed} / ${stage.total}` : '正在上傳文件…' : ready ? `${name} · 完成` : '尚未上傳文件'}</span>
    {busy && stage && <progress max={Math.max(1, stage.total)} value={stage.completed} aria-label={`${uploadLabels[stage.stage]}進度`} />}
  </div>;
}
