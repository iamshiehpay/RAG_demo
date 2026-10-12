import type { LLMCallTrace, PlanEvent, RetrievedChunk } from './events';
import { ThinkingContent } from './Shared';

export function Trace({ calls, chunks, plan, thinking = '', invalidCitationCount = 0, droppedChunkCount = 0, summaryLevel = null }: {
  calls: LLMCallTrace[]; chunks: RetrievedChunk[]; plan: PlanEvent | null;
  thinking?: string; invalidCitationCount?: number; droppedChunkCount?: number;
  summaryLevel?: string | null;
}) {
  return <details className="trace"><summary>Trace · {calls.length} LLM call{calls.length === 1 ? '' : 's'}</summary>
    <p>Invalid Citations: {invalidCitationCount}</p>
    <p>Chunks dropped because of Context Budget: {droppedChunkCount}</p>
    {summaryLevel && <p>Summary Tree level: {summaryLevel}</p>}
    {calls.length === 0 && <ThinkingContent text={thinking} />}
    {plan && <section aria-label="Question plan"><h4>Question plan</h4>
      <dl className="metrics">
        <div><dt>Question Type</dt><dd>{plan.question_type}</dd></div>
        <div><dt>Standalone Question</dt><dd>{plan.standalone_question}</dd></div>
        <div><dt>Plan source</dt><dd>{plan.plan_source}</dd></div>
        {plan.fallback_reason && <div><dt>Fallback reason</dt><dd>{plan.fallback_reason}</dd></div>}
        {plan.rewrite_language_mismatch && <>
          <div><dt>Rewrite language mismatch</dt><dd>Original question retained; Question Type preserved.</dd></div>
          <div><dt>Router rewrite</dt><dd>{plan.router_standalone_question}</dd></div>
        </>}
      </dl>
      {plan.sub_queries.length > 0 && <><h4>Sub-queries</h4>
        <ol>{plan.sub_queries.map((query, i) => <li key={i}>{query}</li>)}</ol></>}
    </section>}
    {calls.map((call, i) => <section key={i} aria-label={`LLM call ${i + 1}`}>
      <h4>{call.call_type} · think={call.think}</h4>
      <label>Context Budget: {call.estimated_prompt_tokens + call.num_predict} / {call.context_budget}
        <meter min={0} max={call.context_budget} value={call.estimated_prompt_tokens + call.num_predict}
          aria-label="Context Budget token usage" />
      </label>
      <dl className="metrics">
        <div><dt>Estimated prompt (includes {call.safety_margin} safety margin)</dt><dd>{call.estimated_prompt_tokens}</dd></div>
        <div><dt>prompt_eval_count</dt><dd>{call.prompt_eval_count ?? 'Not reported'}</dd></div>
        <div><dt>Output reservation (thinking + answer)</dt><dd>{call.num_predict}</dd></div>
        <div><dt>eval_count</dt><dd>{call.eval_count ?? 'Not reported'}</dd></div>
        <div><dt>Latency</dt><dd>{(call.latency_ms / 1000).toFixed(2)} s</dd></div>
        <div><dt>done_reason</dt><dd>{call.done_reason}</dd></div>
        {call.discarded_fact_lines > 0 && <div><dt>Discarded extraction lines</dt>
          <dd>{call.discarded_fact_lines}</dd></div>}
      </dl>
      <ThinkingContent text={call.thinking} />
    </section>)}
    <h4>Retrieved Chunks · cosine similarity</h4>
    {chunks.map(item => <details key={item.chunk.id}>
      <summary>p.{item.chunk.page_start} · {item.chunk.section} · {item.score.toFixed(4)}</summary>
      <pre>{item.chunk.text}</pre>
    </details>)}
  </details>;
}
