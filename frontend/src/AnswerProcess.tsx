import { useState } from 'react';
import type { LLMCallTrace, PlanEvent, RetrievedChunk } from './events';
import { EMBEDDING_MODEL, LLM_MODEL } from './models';
import { pageRange } from './Shared';

const BUDGET = 10000;
const PREVIEW_CHUNKS = 3;

const questionTypeName = { Lookup: '查找細節', Synthesis: '跨章節比較', Global: '全文摘要' } as const;
const questionTypeHint = {
  Lookup: '答案在文件的某一處，直接找出相關原文',
  Synthesis: '答案散在不同章節，要分頭找再合併',
  Global: '針對整份文件，使用上傳時建好的摘要',
} as const;
const stepNames: Record<string, string> = {
  router: '判斷問題類型', answer: '產生回答', fact_extraction: '分批抽取事實',
  section_summary: '產生 Section 摘要', group_summary: '產生 Group 摘要', document_summary: '產生文件概覽', judge: '評分（評估用）',
};
const thinkNames: Record<string, string> = { low: '少', medium: '中', high: '多' };
const fallbackReasons: Record<string, string> = {
  length: '判斷問題類型時，模型的輸出被截斷',
  invalid_json: '模型回覆的格式不正確',
  invalid_plan: '模型回覆的內容無法使用',
  missing_rewrite: '模型沒有提供改寫後的完整問題',
};

const num = (value: number) => value.toLocaleString('en-US');
const seconds = (ms: number) => `${(ms / 1000).toFixed(1)} 秒`;
const callTotal = (call: LLMCallTrace) => call.estimated_prompt_tokens + call.num_predict;

/** Global answers use the Summary Tree; the level string comes from the backend ("section", "group:2", "document"). */
export function summaryLevelName(level: string) {
  if (level === 'section') return 'Section';
  if (level === 'document') return '文件概覽';
  const group = /^group:(\d+)$/.exec(level);
  return group ? `Group ${group[1]}` : level;
}

function summaryLine({ plan, chunks, calls, summaryLevel }: {
  plan: PlanEvent | null; chunks: RetrievedChunk[]; calls: LLMCallTrace[]; summaryLevel: string | null;
}) {
  const parts: string[] = [];
  if (plan) parts.push(questionTypeName[plan.question_type]);
  if (plan?.question_type === 'Global') {
    if (summaryLevel) parts.push(`使用摘要層：${summaryLevelName(summaryLevel)}`);
  } else if (chunks.length > 0) parts.push(`找到 ${chunks.length} 段原文`);
  if (calls.length > 0) {
    parts.push(`呼叫模型 ${calls.length} 次`);
    parts.push(`單次最多 ${num(Math.max(...calls.map(callTotal)))} / ${num(BUDGET)} tokens`);
  }
  return parts.join(' · ');
}

function BudgetBar({ call }: { call: LLMCallTrace }) {
  const total = callTotal(call);
  const percent = (tokens: number) => `${Math.max(0, Math.min(100, tokens / (BUDGET / 100)))}%`;
  return <div className="token-bar" role="meter" aria-label="送入模型的內容加上預留的輸出，以 10,000 為滿格"
    aria-valuemin={0} aria-valuemax={BUDGET} aria-valuenow={total} aria-valuetext={`${num(total)} / ${num(BUDGET)} tokens`}>
    <span className="token-prompt" style={{ width: percent(call.estimated_prompt_tokens) }} />
    <span className="token-reserved" style={{ width: percent(call.num_predict) }} />
  </div>;
}

function Understanding({ plan }: { plan: PlanEvent }) {
  const fellBack = plan.plan_source === 'fallback';
  return <section className="process-section" aria-label="系統怎麼理解這個問題">
    <h4 className="label">1　系統怎麼理解這個問題</h4>
    <dl className="process-facts">
      <dt>問題類型</dt>
      <dd>{questionTypeName[plan.question_type]}：{questionTypeHint[plan.question_type]}
        {fellBack && <span className="fallback-note"> 無法判斷問題類型，改用查找細節
          {plan.fallback_reason ? `（原因：${fallbackReasons[plan.fallback_reason] ?? plan.fallback_reason}）` : ''}。</span>}
      </dd>
      <dt>改寫成完整問題</dt>
      <dd>{plan.standalone_question}
        {plan.rewrite_language_mismatch && <span className="fallback-note"> 模型改寫的語言與原問題不同，已改用原問題
          {plan.router_standalone_question ? `（模型的改寫：${plan.router_standalone_question}）` : ''}。</span>}
      </dd>
      {plan.sub_queries.length > 0 && <><dt>拆成子問題</dt>
        <dd><ol>{plan.sub_queries.map((query, i) => <li key={i}>{query}</li>)}</ol></dd></>}
    </dl>
  </section>;
}

function Models({ plan, calls, chunks, invalidCitationCount, droppedChunkCount }: {
  plan: PlanEvent | null; calls: LLMCallTrace[]; chunks: RetrievedChunk[];
  invalidCitationCount: number; droppedChunkCount: number;
}) {
  const retrieves = plan !== null && plan.question_type !== 'Global' && (calls.length > 0 || chunks.length > 0);
  const best = chunks.length ? Math.max(...chunks.map(item => item.score)) : null;
  // The query embedding runs right after the router call, before any answer-side call.
  const retrievalAt = calls[0]?.call_type === 'router' ? 1 : 0;
  const seen = new Map<string, number>();
  const rows: Array<{ kind: 'call'; call: LLMCallTrace; label: string } | { kind: 'retrieval' }> = [];
  calls.forEach((call, i) => {
    if (retrieves && i === retrievalAt) rows.push({ kind: 'retrieval' });
    const count = seen.get(call.call_type) ?? 0;
    seen.set(call.call_type, count + 1);
    const name = stepNames[call.call_type] ?? call.call_type;
    // fact_extraction runs once per batch; only a second answer call is a retry.
    const label = call.call_type === 'fact_extraction' ? `${name} 第 ${count + 1} 批`
      : call.call_type === 'answer' && count > 0 ? `${name}（重試）` : name;
    rows.push({ kind: 'call', call, label });
  });
  if (retrieves && retrievalAt >= calls.length) rows.push({ kind: 'retrieval' });
  const over = calls.some(call => callTotal(call) > BUDGET);
  return <section className="process-section" aria-label="每一步用了哪個模型">
    <h4 className="label">2　每一步用了哪個模型、多少 token</h4>
    <div className="process-table" role="table" aria-label="模型呼叫明細">
      <div className="process-row process-head" role="row">
        <span role="columnheader">步驟</span><span role="columnheader">模型</span><span role="columnheader">思考量</span>
        <span role="columnheader">用量（滿格 = 上限 {num(BUDGET)}）</span><span role="columnheader">送入 ＋ 預留</span><span role="columnheader">時間</span>
      </div>
      {rows.map((row, i) => row.kind === 'retrieval'
        ? <div className="process-row" role="row" key={`r${i}`}>
          <span role="cell" className="step-name">找相關段落</span><span role="cell">{EMBEDDING_MODEL}</span><span role="cell">—</span>
          <span role="cell" className="muted retrieval-note">
            找到 {chunks.length} 段{best !== null ? `，最高相似度 ${best.toFixed(2)}` : ''}；不佔 {num(BUDGET)} 上限
          </span><span role="cell">—</span><span role="cell">—</span>
        </div>
        : <div className="process-row" role="row" key={`c${i}`}>
          <span role="cell" className="step-name">{row.label}</span>
          <span role="cell">{LLM_MODEL}</span>
          <span role="cell">{thinkNames[row.call.think] ?? row.call.think}</span>
          <span role="cell"><BudgetBar call={row.call} /></span>
          <span role="cell" className="tabular">{num(row.call.estimated_prompt_tokens)} ＋ {num(row.call.num_predict)}</span>
          <span role="cell" className="tabular">{seconds(row.call.latency_ms)}</span>
        </div>)}
    </div>
    <div className="process-legend muted">
      <span><i className="swatch swatch-prompt" /> 送進模型的內容</span>
      <span><i className="swatch swatch-reserved" /> 預留給思考與回答</span>
    </div>
    <p className={invalidCitationCount ? 'error' : 'muted'}>無效引用 {invalidCitationCount}　因額度略過的段落 {droppedChunkCount}</p>
    {over && <p className="error">有一次呼叫超過 {num(BUDGET)} tokens 上限。</p>}
  </section>;
}

function FoundChunks({ chunks }: { chunks: RetrievedChunk[] }) {
  const [all, setAll] = useState(false);
  const sorted = [...chunks].sort((a, b) => b.score - a.score);
  const shown = all ? sorted : sorted.slice(0, PREVIEW_CHUNKS);
  return <section className="process-section" aria-label="找到的原文段落">
    <h4 className="label">3　找到的原文段落（依相似度排序）</h4>
    {shown.map(item => <details className="found-chunk" key={item.chunk.id}>
      <summary><span className="found-page">{pageRange(item.chunk)}</span><span className="found-section">{item.chunk.section}</span>
        <span className="found-score tabular">{item.score.toFixed(3)}</span></summary>
      <pre>{item.chunk.text}</pre>
    </details>)}
    {sorted.length > PREVIEW_CHUNKS && <button className="link-button" aria-expanded={all} onClick={() => setAll(value => !value)}>
      {all ? '只顯示前 3 段' : `顯示其餘 ${sorted.length - PREVIEW_CHUNKS} 段`}</button>}
  </section>;
}

function TechnicalDetails({ calls, thinking, chunks }: { calls: LLMCallTrace[]; thinking: string; chunks: RetrievedChunk[] }) {
  const anyCallThinking = calls.some(call => call.thinking);
  const weighted = chunks.filter(item => item.ranking_score != null);
  return <details className="tech-details">
    <summary>技術細節（開發用）</summary>
    <p className="muted">模型實際回報的 token 數、安全邊際、結束原因，以及模型的思考原文。</p>
    {calls.map((call, i) => <div className="tech-call" key={i}>
      <h4 className="label">{i + 1}. {call.call_type}（think={call.think}）</h4>
      <dl className="tech-metrics">
        <div><dt>prompt_eval_count</dt><dd>{call.prompt_eval_count ?? '未回報'}</dd></div>
        <div><dt>eval_count</dt><dd>{call.eval_count ?? '未回報'}</dd></div>
        <div><dt>估算的 prompt</dt><dd>{num(call.estimated_prompt_tokens)}</dd></div>
        <div><dt>安全邊際</dt><dd>{call.safety_margin}</dd></div>
        <div><dt>done_reason</dt><dd>{call.done_reason}</dd></div>
        {call.discarded_fact_lines > 0 && <div><dt>捨棄的抽取行</dt><dd>{call.discarded_fact_lines}</dd></div>}
      </dl>
      {call.thinking && <details className="thinking-content"><summary>思考原文</summary><pre>{call.thinking}</pre></details>}
    </div>)}
    {!anyCallThinking && thinking && <details className="thinking-content"><summary>思考原文</summary><pre>{thinking}</pre></details>}
    {weighted.length > 0 && <p className="muted">加權 RRF 分數：{weighted.map(item => item.ranking_score!.toFixed(6)).join('、')}</p>}
  </details>;
}

export function AnswerProcess({ calls, chunks, plan, thinking = '', invalidCitationCount = 0, droppedChunkCount = 0, summaryLevel = null }: {
  calls: LLMCallTrace[]; chunks: RetrievedChunk[]; plan?: PlanEvent | null;
  thinking?: string; invalidCitationCount?: number; droppedChunkCount?: number; summaryLevel?: string | null;
}) {
  const line = summaryLine({ plan: plan ?? null, chunks, calls, summaryLevel });
  return <details className="answer-process">
    <summary><span className="process-title">回答過程</span><span className="process-line">{line}</span></summary>
    <div className="process-content">
      {plan && <Understanding plan={plan} />}
      {(calls.length > 0 || chunks.length > 0) && <Models plan={plan ?? null} calls={calls} chunks={chunks}
        invalidCitationCount={invalidCitationCount} droppedChunkCount={droppedChunkCount} />}
      {chunks.length > 0 && <FoundChunks chunks={chunks} />}
      <TechnicalDetails calls={calls} thinking={thinking} chunks={chunks} />
    </div>
  </details>;
}
