import type { LLMCallTrace, PlanEvent, RetrievedChunk } from './events';
import { pageRange, ThinkingContent, TokenBar } from './Shared';

export function Trace({ calls, chunks, plan, thinking = '', invalidCitationCount = 0, droppedChunkCount = 0, summaryLevel = null }: {
  calls: LLMCallTrace[]; chunks: RetrievedChunk[]; plan?: PlanEvent | null;
  thinking?: string; invalidCitationCount?: number; droppedChunkCount?: number; summaryLevel?: string | null;
}) {
  return <details className="trace"><summary>Trace <span className="trace-count">{calls.length} LLM call{calls.length === 1 ? '' : 's'} · {chunks.length} Chunks</span></summary>
    <div className="trace-content">
      {plan && <dl className="trace-plan">
        <div><dt>Question Type</dt><dd>{plan.question_type}</dd></div>
        <div><dt>Standalone Question</dt><dd>{plan.standalone_question}</dd></div>
        <div><dt>Plan source</dt><dd>{plan.plan_source}</dd></div>
        {plan.fallback_reason && <div><dt>Fallback reason</dt><dd>{plan.fallback_reason}</dd></div>}
        {plan.rewrite_language_mismatch && <>
          <div><dt>Rewrite language mismatch</dt><dd>Original question retained; Question Type preserved.</dd></div>
          <div><dt>Router rewrite</dt><dd>{plan.router_standalone_question}</dd></div>
        </>}
        {plan.sub_queries.length > 0 && <div><dt>Sub-queries</dt><dd><ol>{plan.sub_queries.map((query, i) => <li key={i}>{query}</li>)}</ol></dd></div>}
      </dl>}
      <p className={invalidCitationCount ? 'error' : 'muted'}>Invalid Citations: {invalidCitationCount}</p>
      <p className="muted">Chunks dropped because of Context Budget: {droppedChunkCount}</p>
      <p className="muted">Highest retrieved cosine similarity: {chunks.length ? Math.max(...chunks.map(item => item.score)).toFixed(4) : 'Not retrieved'}</p>
      {summaryLevel && <p className="muted">Summary Tree level: {summaryLevel}</p>}
      {calls.map((call, i) => <section className="trace-call" key={i} aria-label={`LLM call ${i + 1}`}>
        <h4><span>{String(i + 1).padStart(2, '0')} / {call.call_type}</span><span className="call-think">think={call.think}</span></h4>
        <TokenBar call={call} />
        <dl className="metrics">
          <div><dt>prompt_eval_count</dt><dd>{call.prompt_eval_count ?? 'Not reported'}</dd></div>
          <div><dt>eval_count</dt><dd>{call.eval_count ?? 'Not reported'}</dd></div>
          <div><dt>安全邊際 · Safety margin</dt><dd>{call.safety_margin}</dd></div>
          <div><dt>延遲 · Latency</dt><dd>{(call.latency_ms / 1000).toFixed(2)} s</dd></div>
          <div><dt>done_reason</dt><dd>{call.done_reason}</dd></div>
        </dl>
        {call.discarded_fact_lines > 0 && <p className="muted">Discarded extraction lines: {call.discarded_fact_lines}</p>}
        <ThinkingContent text={call.thinking} />
      </section>)}
      {!calls.some(call => call.thinking) && <ThinkingContent text={thinking} />}
      {chunks.length > 0 && <div className="retrieved-chunks"><h4>檢索到的 Chunks · cosine similarity</h4>
        {chunks.map(item => <details key={item.chunk.id}>
          <summary>{pageRange(item.chunk)} · {item.chunk.section}<span className="similarity">{item.score.toFixed(4)}</span></summary>
          {item.ranking_score != null && <p className="muted">Weighted RRF score: {item.ranking_score.toFixed(6)}</p>}
          <pre>{item.chunk.text}</pre>
        </details>)}
      </div>}
    </div>
  </details>;
}
