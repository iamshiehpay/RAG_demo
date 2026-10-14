/* Review-only network fixture: inject with agent-browser eval --stdin.
   Not imported by production. Every answer/summary here is scripted evidence. */
(() => {
  const nativeFetch = window.fetch.bind(window);
  const chunk = { id: 'review-table2', section_id: 'review-4.3', section: '4.3 Ablation Study',
    page_start: 8, page_end: 9, order: 1,
    text: 'Table 2. Overall win rates of each variant against NaiveRAG.\n\nDataset       LightRAG     -Low     -Origin\nMix              60.0       64.8       63.6\nAgriculture      67.6       61.6       74.4\n\nThese are variant win rates against NaiveRAG, not direct pairwise comparisons between variants.\n\nReview fixture: this text is scripted for design approval, not extracted by the backend.' };
  const citations = [{ id: 'C1', source_id: chunk.id, section: chunk.section, page_start: 8, page_end: 9 }];
  const answer = '### 消融結果：先確認比較基準\n\nTable 2 的數字是各變體**相對 NaiveRAG 的勝率**，不是變體之間直接對戰的勝率。以下比較同一資料集的 Overall 指標。[C1]\n\n- **Mix**：`-Low` 的 Overall 為 64.8%，高於完整版 LightRAG 的 60.0%。[C1]\n- **Agriculture**：`-Origin` 的 Overall 為 74.4%，高於完整版的 67.6%。[C1]\n\n因此，完整版並非在所有資料集、所有指標上都最好。不同元件的效果需要依資料集與評估指標判讀。[C1]';
  const call = { call_type: 'answer', estimated_prompt_tokens: 2100, prompt_eval_count: 1875,
    eval_count: 620, think: 'medium', num_predict: 3000, context_budget: 10000, safety_margin: 300,
    thinking: 'Scripted review thinking: identify the comparison baseline, then compare Overall within each dataset.',
    latency_ms: 4200, done_reason: 'stop', discarded_fact_lines: 0, plan_source: null, fallback_reason: null, rewrite_language_mismatch: false, router_standalone_question: null };
  window.__t09 = { scenario: 'q3', events: [], uploadHold: false, release: () => {}, answer, chunk, citations };
  const pause = () => new Promise(resolve => { window.__t09.release = resolve; });
  const response = (generate) => new Response(new ReadableStream({
    async start(controller) {
      const emit = (event) => { window.__t09.events.push(event); controller.enqueue(new TextEncoder().encode(`event: ${event.type}\ndata: ${JSON.stringify(event)}\n\n`)); };
      await generate(emit);
      controller.close();
    },
  }), { headers: { 'Content-Type': 'text/event-stream' } });
  window.fetch = async (url, options) => {
    if (url === '/api/documents') {
      if (window.__t09.uploadFailure) return Response.json({detail: 'Scripted invalid PDF; previous Document retained.'}, {status: 400});
      return Response.json({job_id: 'review', events_url: '/api/jobs/review/events'}, {status: 202});
    }
    if (url === '/api/jobs/review/events') {
      if (window.__t09.progressLost === 'restart') return Response.json({detail: 'Upload job not found after restart.'}, {status: 404});
      if (window.__t09.progressLost) { window.__t09.progressLost = false; throw new Error('Scripted progress connection interrupted.'); }
      return response(async emit => {
      emit({ type: 'stage', stage: 'parsing', completed: 0, total: 1 });
      emit({ type: 'stage', stage: 'chunking', completed: 0, total: 1 });
      emit({ type: 'stage', stage: 'embedding', completed: 18, total: 52 });
      if (window.__t09.uploadHold) await pause();
      emit({ type: 'stage', stage: 'complete', completed: 1, total: 1 });
      emit({ type: 'ready', document_id: 'review', name: 'LightRAG.pdf · scripted review', chunk_count: 52,
        document_summary: '設計稿示例：LightRAG 以 graph-based indexing 與 dual-level retrieval 回答文件問題，並討論增量更新、成本與實驗結果。此概覽為設計審閱用腳本，並非模型產生的結果。' });
    });
    }
    if (String(url).startsWith('/api/sources/')) return Response.json(chunk);
    if (url === '/api/ask') return response(async emit => {
      const scenario = window.__t09.scenario;
      if (scenario === 'rejected') { emit({type: 'rejected', code: 'question_too_long', message: 'Scripted question too long; limit 1,000 tokens.', question_tokens: 1001, token_limit: 1000}); return; }
      emit({ type: 'plan', question_type: 'Lookup', standalone_question: 'Performance of ablated versions of LightRAG', sub_queries: [], plan_source: 'fallback', fallback_reason: 'missing_rewrite', rewrite_language_mismatch: true, router_standalone_question: 'Scripted wrong-language rewrite' });
      emit({ type: 'retrieval', chunks: [{ chunk, score: .7218 }] });
      emit({ type: 'citation_map', citations });
      if (scenario !== 'no-thinking') emit({ type: 'thinking', text: 'Review-only streamed thinking content.' });
      emit({ type: 'delta', text: 'Table 2 的比較基準是各變體相對 NaiveRAG 的勝率。[C1]' });
      if (scenario === 'provisional') await pause();
      if (scenario === 'retry') {
        emit({ type: 'retry', reason: 'length' });
        await pause();
      }
      if (scenario === 'error') {
        emit({ type: 'error', code: 'answer_failed', message: '回答被截斷，重新產生仍未完成。請重試此問題。' });
        emit({ type: 'trace', invalid_citation_count: 0, calls: [{ ...call, done_reason: 'length' }, { ...call, think: 'low', done_reason: 'length' }] });
        return;
      }
      let result = answer;
      let unverified = [];
      if (scenario === 'unverified') {
        const claim = '這個推論找不到有效來源。';
        const prefix = `😀 ${claim} [C1]\n\n`;
        result = prefix + claim + ' ' + claim;
        const start = Array.from(prefix).length;
        unverified = [{start, end: start + Array.from(claim).length}, {start: start + Array.from(claim).length + 1, end: Array.from(result).length}];
      }
      if (scenario === 'no-thinking') { call.thinking = ''; }
      if (scenario === 'markdown') result = '**Safe bold** and *safe emphasis*. [C1]\n\n<script>window.__unsafe = true</script>\n\n[unsafe](javascript:alert(1))\n\n| Dataset | Overall |\n| --- | --- |\n| Mix | 64.8% |';
      if (scenario === 'custom') { result = window.__t09.customAnswer; unverified = window.__t09.customSpans; }
      emit({ type: 'final', answer: result, citations, unverified });
      emit({ type: 'trace', invalid_citation_count: unverified.length, calls: scenario === 'budget' ? [
        { ...call, call_type: 'router', estimated_prompt_tokens: 1200, prompt_eval_count: 975, num_predict: 600, think: 'low', eval_count: 115 },
        { ...call, estimated_prompt_tokens: 6990, prompt_eval_count: 6765 },
      ] : [call] });
    });
    return nativeFetch(url, options);
  };
  return 'Review fixture installed; use normal upload and ask controls.';
})();
