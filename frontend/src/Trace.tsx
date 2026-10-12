import type { LLMCallTrace, RetrievedChunk } from './events';

export function Trace({ calls, chunks }: { calls: LLMCallTrace[]; chunks: RetrievedChunk[] }) {
  return <details className="trace"><summary>Trace · {calls.length} LLM call{calls.length === 1 ? '' : 's'}</summary>
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
      </dl>
      {call.thinking && <details><summary>Model thinking</summary><pre>{call.thinking}</pre></details>}
    </section>)}
    <h4>Retrieved Chunks · cosine similarity</h4>
    {chunks.map(item => <details key={item.chunk.id}>
      <summary>p.{item.chunk.page_start} · {item.chunk.section} · {item.score.toFixed(4)}</summary>
      <pre>{item.chunk.text}</pre>
    </details>)}
  </details>;
}
