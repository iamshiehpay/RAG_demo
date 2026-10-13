/* Review-only network fixture: inject with agent-browser eval --stdin.
   Not imported by production. Every answer/summary here is scripted evidence.
   Set window.__t09.scenario before pressing 送出. Scenarios:
   q3 (default) | compare | widetable | global | fallback | provisional | retry | error | unverified | markdown | budget | missing-source */
(() => {
  const nativeFetch = window.fetch.bind(window);
  const chunk = { id: 'review-table2', section_id: 'review-4.3', section: '4.3 Ablation Study',
    page_start: 8, page_end: 8, order: 1, kind: 'text', table_label: null, table_caption: null, table_meaning: '',
    table_headers: [], table_rows: [], table_reconstructed: false, linked_chunk_ids: [],
    text: 'Table 2. Overall win rates of each variant against NaiveRAG.\n\nDataset       LightRAG     -Low     -Origin\nMix              60.0       64.8       63.6\nAgriculture      67.6       61.6       74.4\n\nThese are variant win rates against NaiveRAG, not direct pairwise comparisons between variants.\n\nReview fixture: this text is scripted for design approval, not extracted by the backend.' };
  const tableChunk = { ...chunk, id: 'review-table1', section: '4.2 Comparison', page_start: 7, page_end: 7, kind: 'table',
    table_label: 'Table 1', table_caption: 'Table 1. Win rates of GraphRAG against LightRAG.', table_reconstructed: true,
    table_meaning: '每格是 GraphRAG 勝率 / LightRAG 勝率（%）。', table_headers: ['Dataset', 'GraphRAG', 'LightRAG'],
    table_rows: [['Agriculture', '45.2', '54.8'], ['CS', '48.0', '52.0'], ['Legal', '47.2', '52.8'], ['Mix (Overall)', '50.4', '49.6']] };
  const wideCols = ['Dataset', 'Comprehensiveness', 'Diversity', 'Empowerment', 'Overall', 'Win rate 11.1', 'Win rate 22.2', 'Win rate 33.3', 'Delta -0.4', 'Cost 610.5'];
  const wideChunk = { ...tableChunk, id: 'review-wide', section: '4.4 Wide table', page_start: 9, page_end: 9, table_label: 'Table 9',
    table_caption: 'Table 9. A ten-column table used to check horizontal scrolling and number wrapping.',
    table_meaning: '每格是各資料集在該指標下的勝率（%）；此表為設計審閱用腳本。', table_headers: wideCols,
    table_rows: ['Agriculture', 'Legal', 'Mix'].map((name, r) => [name, ...wideCols.slice(1).map((_, i) => (11.1 + r * 9.7 + i * 1.7).toFixed(1))]) };
  const summary = { id: 'review-summary', kind: 'section', section: '3 The LightRAG Architecture', page_start: 3, page_end: 6,
    section_titles: ['3 The LightRAG Architecture', '3.1 Graph-based indexing'],
    text: 'Review fixture summary: 說明 LightRAG 的圖索引與雙層檢索流程。此文字為設計審閱用腳本。' };
  const citations = [{ id: 'C1', source_id: chunk.id, section: chunk.section, page_start: 8, page_end: 8 }];
  const answer = '### 消融結果：先確認比較基準\n\nTable 2 的數字是各變體**相對 NaiveRAG 的勝率**，不是變體之間直接對戰的勝率。以下比較同一資料集的 Overall 指標。[C1]\n\n- **Mix**：`-Low` 的 Overall 為 64.8%，高於完整版 LightRAG 的 60.0%。[C1]\n- **Agriculture**：`-Origin` 的 Overall 為 74.4%，高於完整版的 67.6%。[C1]\n\n因此，完整版並非在所有資料集、所有指標上都最好。不同元件的效果需要依資料集與評估指標判讀。[C1]';
  const call = { call_type: 'answer', estimated_prompt_tokens: 2100, prompt_eval_count: 1875,
    eval_count: 620, think: 'medium', num_predict: 3000, context_budget: 10000, safety_margin: 300,
    thinking: 'Scripted review thinking: identify the comparison baseline, then compare Overall within each dataset.',
    latency_ms: 4200, done_reason: 'stop', discarded_fact_lines: 0, plan_source: null, fallback_reason: null,
    rewrite_language_mismatch: false, router_standalone_question: null };
  const routerCall = { ...call, call_type: 'router', estimated_prompt_tokens: 880, prompt_eval_count: 805, num_predict: 600,
    think: 'low', eval_count: 115, latency_ms: 900, thinking: '', plan_source: 'router' };
  window.__t09 = { scenario: 'q3', uploadHold: false, release: () => {}, answer, chunk, citations };
  const pause = () => new Promise(resolve => { window.__t09.release = resolve; });
  const response = (generate) => new Response(new ReadableStream({
    async start(controller) {
      const emit = (event) => controller.enqueue(new TextEncoder().encode(`event: ${event.type}\ndata: ${JSON.stringify(event)}\n\n`));
      await generate(emit);
      controller.close();
    },
  }), { headers: { 'Content-Type': 'text/event-stream' } });
  const plan = (over = {}) => ({ type: 'plan', question_type: 'Lookup', standalone_question: 'Performance of ablated versions of LightRAG',
    sub_queries: [], plan_source: 'router', fallback_reason: null, rewrite_language_mismatch: false, router_standalone_question: null, ...over });
  window.fetch = async (url, options) => {
    if (url === '/api/documents') return Response.json({ job_id: 'review-job', events_url: '/api/review-events' }, { status: 202 });
    if (url === '/api/review-events') return response(async emit => {
      emit({ type: 'stage', stage: 'parsing', completed: 0, total: 1 });
      emit({ type: 'stage', stage: 'chunking', completed: 0, total: 1 });
      emit({ type: 'stage', stage: 'embedding', completed: 18, total: 52 });
      if (window.__t09.uploadHold) await pause();
      emit({ type: 'ready', document_id: 'review', name: 'LightRAG.pdf · scripted review', chunk_count: 52,
        document_summary: '設計稿示例：LightRAG 以 graph-based indexing 與 dual-level retrieval 回答文件問題，並討論增量更新、成本與實驗結果。此概覽為設計審閱用腳本，並非模型產生的結果。第二段用來讓概覽超過可見行數，測試「展開全文概覽」：實驗在多個資料集上與 NaiveRAG、GraphRAG 比較，並以消融實驗檢視各元件的貢獻。' });
    });
    if (String(url).startsWith('/api/sources/')) {
      if (window.__t09.scenario === 'missing-source') return new Response('{}', { status: 404 });
      const id = decodeURIComponent(String(url).slice('/api/sources/'.length));
      return Response.json(id === summary.id ? summary : id === tableChunk.id ? tableChunk : id === wideChunk.id ? wideChunk : chunk);
    }
    if (url === '/api/ask') return response(async emit => {
      const scenario = window.__t09.scenario;
      const compare = scenario === 'compare';
      const globalQ = scenario === 'global';
      const mapped = scenario === 'widetable' ? [{ id: 'C1', source_id: wideChunk.id, section: wideChunk.section, page_start: 9, page_end: 9 }] : globalQ ? [{ id: 'S1', source_id: summary.id, section: summary.section, page_start: 3, page_end: 6 }]
        : compare ? [...citations, { id: 'C2', source_id: tableChunk.id, section: tableChunk.section, page_start: 7, page_end: 7 }] : citations;
      emit(plan(globalQ ? { question_type: 'Global', standalone_question: '請摘要這份文件' }
        : compare ? { question_type: 'Synthesis', standalone_question: 'LightRAG 和 GraphRAG 的差異是什麼？',
          sub_queries: ['GraphRAG 的檢索成本', 'LightRAG 的檢索成本'] }
        : scenario === 'fallback' ? { plan_source: 'fallback', fallback_reason: 'invalid_json' } : {}));
      const found = globalQ ? [] : compare
        ? [{ chunk: tableChunk, score: .7412 }, { chunk, score: .7218 }, ...[3, 4, 5, 6, 7].map(n => ({ chunk: { ...chunk, id: `review-extra-${n}`, section: `5.${n} Extra section`, page_start: n + 8, page_end: n + 8 }, score: .7 - n / 100 }))]
        : [{ chunk, score: .7218 }];
      emit({ type: 'retrieval', chunks: found, dropped_chunk_count: compare ? 1 : 0 });
      emit({ type: 'citation_map', citations: mapped });
      emit({ type: 'thinking', text: 'Review-only streamed thinking content.' });
      emit({ type: 'delta', text: globalQ ? '這份文件介紹 LightRAG 的圖索引與雙層檢索。[S1]' : 'Table 2 的比較基準是各變體相對 NaiveRAG 的勝率。[C1]' });
      if (scenario === 'provisional') await pause();
      if (scenario === 'retry') {
        emit({ type: 'retry', reason: 'length' });
        await pause();
      }
      if (scenario === 'error') {
        emit({ type: 'error', code: 'answer_failed', message: '回答被截斷，重新產生仍未完成。請重試此問題。' });
        emit({ type: 'trace', calls: [{ ...call, done_reason: 'length' }, { ...call, think: 'low', done_reason: 'length' }], invalid_citation_count: 0, dropped_chunk_count: 0, summary_level: null });
        return;
      }
      let result = globalQ ? '這份文件介紹 LightRAG 的圖索引與雙層檢索，並說明增量更新與實驗結果。[S1]' : answer;
      let unverified = [];
      if (scenario === 'unverified') {
        const claim = '這個推論找不到有效來源。';
        const start = Array.from(answer).length + 2;
        result = `${answer}\n\n${claim}`;
        unverified = [{ start, end: start + Array.from(claim).length }];
      }
      if (scenario === 'compare') result = '兩者都用知識圖譜，但檢索成本不同。[C1][C2]\n\n| 面向 | GraphRAG | LightRAG |\n| --- | --- | --- |\n| 檢索方式 | 遍歷 community 報告後再合併回答 | 雙層關鍵字對應實體與關係 |\n| 檢索成本 | 約 610 × 1,000 tokens，多次呼叫 | 少於 100 tokens，1 次呼叫 |\n| 增量更新 | 需重建 community，成本高 | 新節點直接合併進圖 |\n\n勝率並非全面領先：Mix 資料集的 Overall，GraphRAG 為 50.4%，LightRAG 為 49.6%。[C2]';
      if (scenario === 'widetable') {
        const cols = ['Dataset', 'Comprehensiveness', 'Diversity', 'Empowerment', 'Overall', 'Win rate 11.1', 'Win rate 22.2', 'Win rate 33.3', 'Delta -0.4', 'Cost 610.5'];
        const row = (name, base) => `| ${name} | ${cols.slice(1).map((_, i) => (base + i * 1.7).toFixed(1)).join(' | ')} |`;
        result = `下表有 10 欄小數，窄螢幕應該左右捲動而不是把數字拆開。[C1]\n\n| ${cols.join(' | ')} |\n| ${cols.map(() => '---').join(' | ')} |\n${row('Agriculture', 11.1)}\n${row('Legal', 20.5)}\n${row('Mix', 49.6)}\n\n以上為設計審閱用腳本資料。[C1]`;
      }
      if (scenario === 'markdown') result = '**Safe bold** and *safe emphasis*. [C1]\n\n<script>window.__unsafe = true</script>\n\n[unsafe](javascript:alert(1))\n\n| Dataset | Overall |\n| --- | --- |\n| Mix | 64.8% |';
      emit({ type: 'final', answer: result, citations: mapped, unverified });
      emit({ type: 'trace', invalid_citation_count: scenario === 'unverified' ? 1 : 0, dropped_chunk_count: compare ? 1 : 0,
        summary_level: globalQ ? 'group:1' : null,
        calls: scenario === 'budget' ? [
          { ...routerCall, estimated_prompt_tokens: 1200 },
          { ...call, estimated_prompt_tokens: 6990, prompt_eval_count: 6765 },
        ] : [routerCall, ...(compare ? [1, 2].map(n => ({ ...call, call_type: 'fact_extraction', think: 'low', estimated_prompt_tokens: 7000 + n * 300, num_predict: 1000, latency_ms: 1900 + n * 200, discarded_fact_lines: n - 1 })) : []), { ...call, estimated_prompt_tokens: compare ? 5940 : 2100 }] });
    });
    return nativeFetch(url, options);
  };
  return 'Review fixture installed; use normal upload and ask controls.';
})();
