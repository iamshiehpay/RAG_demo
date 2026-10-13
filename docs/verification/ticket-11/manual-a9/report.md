# Bounded A9 diagnosis — retrieval/model refusal; cause UNPROVEN

Base: `b95624782e669705189b8dd30967cdb2e122769d`, branch `lat/a9-document-diagnosis`. Runtime released by nova HCOM #15571 after direct verification of gpt-6.1-sol high / workspace-write / on-request. No production changes, no commit, no N3/eval tuning, no user browser interaction. One live answer request only (router plus answer), empty conversation history.

## Classification and confidence

**Original manual A9 is retrieval/model refusal, high confidence from direct human evidence.** Initially “回答找不到文件” was ambiguous. The human answered the asynchronous clarification with exact answer “文件中未提及” and a Synthesis Trace containing nine retrieved Chunks. This supports completed routing/retrieval and semantic refusal, not a missing-Document/API error. See `user-observation.md` for the verbatim supplied Trace. The original cause and repeatability remain UNPROVEN; no raw original SSE or prior history was available.

High confidence for this isolated observation: cached public upload succeeded, A9 routed Synthesis, retrieval ran, final answer appeared, Citation source returned 200. There was neither document-state/API failure nor fixed refusal in this one run. Therefore no live reproduction of the human's now-confirmed refusal was obtained; history-dependent/non-deterministic behavior remains unresolved.

Separate observed content defect: answer attributes the ingestion warning “結構未能可靠重建” to the paper as its own limitation. Raw answer/Trace and C4 source are saved. The marker is a program constant (`tables.py:11`) and absent from the physical p.9 PDF text. Citation mapping/HTTP success therefore does not make this answer semantically supported. Preserve this observation as FAIL; do not count the probe's transport assertion as A9 acceptance PASS. No causal hypothesis or correction was tested.

## Executed public-path loop

Start isolated unmodified default app:

`PYTHONPATH=src:. /Users/shiehpay/Desktop/resume/rag/.venv/bin/python -m uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8330`

Cold control:

`PYTHONPATH=src:. /Users/shiehpay/Desktop/resume/rag/.venv/bin/python .cache/a9-diagnosis/probe.py cold`

Exit 1 in 0.013s. HTTP 200 SSE with only error `{code: document_not_ready, message: Wait until Document processing is complete before asking.}`; no final, no literal “找不到文件”. This demonstrates the assertion catches document-state failure. It deliberately exercises no-document state, **not a reproduction of the manual A9 symptom**.

Warm bounded call:

`PYTHONPATH=src:. /Users/shiehpay/Desktop/resume/rag/.venv/bin/python .cache/a9-diagnosis/probe.py warm`

Exit 0, 9.733s. Public upload POST 202; upload SSE only Ready (42 chunks), proving cache-hit path before any live answer. Ask SSE event families: plan, retrieval, citation_map, thinking, delta, final, trace. No error/retry. Router: Synthesis, unchanged Standalone Question, Sub-queries “論文方法限制”, “論文數據限制”, “論文範圍限制”. Seven retrieved Chunks, top score 0.505610; C4 p.9 Figure 2 warning was cited. Source GET 200.

Final answer (verbatim):

> 這篇論文在成本比較圖（Figure 2）中指出，該圖的結構「未能可靠重建」，因此在呈現 GraphRAG 與 LightRAG 在 Legal 資料集上的代幣與 API 呼叫成本時，圖表的細節無法完整重建，成為文件本身的限制之一[C4]。

Router low: estimated prompt 838 + reserve 600; actual prompt 499, output 165; 1911ms, stop. Answer medium: estimated prompt 2653 + reserve 3000; actual prompt 2428, output 513; 3843ms, stop. Both below 10K. Invalid Citation count 0, dropped Chunk count 0. These are transport/budget observations only.

## Evidence and limits

All paths below are relative to this worktree, ignored under `.cache/`:

- `.cache/a9-diagnosis/probe.py`: repeatable HTTP discriminator; warm mode reuploads a cache-hit Document and clears history, one live answer per execution.
- `cold.sse`, `cold-result.json`, `cold-sources.json`: controlled error path.
- `upload-accepted.json`, `upload.sse`: public cached upload.
- `warm.sse`, `warm-result.json`, `warm-sources.json`: original live events/output/source.
- `.cache/a9-diagnosis/lightrag.pdf`: copied Main PDF.
- `.cache/833ea057185857ffe9ebc55321a245c0c2765d32f8b43ded5b2b24e00f8c6802.json`: copied validated Main cache, pipeline ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f, target500/dense defaults.

No browser used; original frontend/manual UI behavior is not independently verified. Existing frontend forwards error.message versus final.answer separately and emits Source not found for Citation 404; no literal Chinese “找不到文件” found in these seams. Human's clarified answer confirms generated refusal. Original A9 followed earlier manual turns; this isolated call uses empty history. Human's retrieved list differs from this run (nine Chunks rather than seven, no cost Figure 2 warning in the shown list), and its Standalone Question/Sub-queries also differ. A tight deterministic loop reproducing the **exact original refusal** is not established, so diagnosing-bugs Phases 2–5 are not claimed complete. The classifier asserts on that exact refusal and the cold controlled API failure, but the cold red run is not the original bug.

## Next action for Main

### Source-support check requested in HCOM #15705 (no extra live calls)

Read-only full PDF keyword scan plus cached 4.1–4.5/Conclusion source candidates are saved as `pdf-support-scan.txt` and `support-chunks.json`. The parsed section list has no dedicated Limitations section; Conclusion p.10 contains positive summary, not explicit self-limitations. Most literal limitations mentions concern prior RAG or ablated variants. **However, original PDF p.8 §4.3 contains a qualified caveat about this proposed method's use of original text**, verified directly in the PDF, not only cached metadata. Exact paragraph is saved as `own-method-caveat-p8.txt`: “the original text often contains irrelevant information that can introduce noise in the response.” Its surrounding paragraph explicitly says they eliminated original text in their retrieval process, -Origin did not significantly decline, and sometimes improved in Agriculture/Mix. This is a method-component caveat, not a limitation of prior RAG or a reconstruction warning. There is therefore source support for a qualified response to broad A9; absence of a titled Limitations section does not establish justified blanket refusal.

Concrete answerable scope/tradeoff evidence exists in the document and in sections shown by the human's retrieval Trace:

- §4.1 pp.5–6: evaluates four selected UltraDomain datasets out of 18 domains, questions generated by LLM using five users/tasks/question combinations (125 per dataset). This supports describing the evaluated scope; it does not justify inventing a demonstrated generalization failure.
- §4.3 p.8 text, cached chunk-23: low/high-only variants trade detail against breadth; original text can introduce noise, and the no-original-text variant improves in some cases. This is explicit qualified evidence about variants/using original text, not a blanket limitation of every full-system answer.
- §4.3 p.8 Table 2 and these same ablation observations are present in the document; original human Trace identifies the section/pages but lacks source IDs/text, so exact original coverage cannot be certified from the displayed list alone.

Thus **document-level source support exists; blanket absence is not justified for the broad question**. A9 can describe the original-text noise caveat with p.8 §4.3 Citation and distinguish it from variant-specific tradeoffs/evaluation scope. The visible original retrieval list includes p.8 §4.3 multiple times, but without source IDs/text cannot prove the exact caveat paragraph was in the original answer prompt. Retrieval omission versus model interpretation/over-refusal remains UNPROVEN; no evidence supports declaring one the cause. Do not claim adding one missing Chunk fixes A9 or that a score threshold caused this behavior. No threshold/prompt changes or second live call were performed. Preserve original A9 FAIL, and condition any revised expectation on document-supported caveats rather than assuming every paper has an explicit limitations section.

Exact answer and visible Trace are now obtained from the human. Main should keep A9 as retrieval/model refusal FAIL and original cause unproven. If Main elects further bounded diagnosis, preserve original SSE/source text/prior turns for a history-preserving refusal replay, rather than starting quality tuning. No ranked causal predictions have been tested because the original refusal was not reproduced in the isolated public loop. The separate warning-attribution defect is concrete evidence for Main's scope/integration decision, not a claim that it explains the original refusal. Existing FAILs/D10 remain unchanged. No production correction recommended from this evidence alone.

Resource cleanup: own 8330 server PID37799 stopped cleanly by Ctrl-C; no server/browser remains. 8101/8201/Ollama not restarted/stopped or reconfigured. Main cache/PDF read-only; only copied worktree cache/PDF used. `git status --short` and `git diff --stat` both empty after diagnostics. Agent remains available for Main.

## Main preservation

Main reviewed this report, the original live result and p.8 caveat. This directory retains the final diagnostic outcome/events/sources; original probe and full support scan remain in the ignored task archive. No production fix, original-refusal replay, or acceptance waiver is claimed. Existing manual A9 remains FAIL; the separate system-warning attribution is a grounding FAIL. D14 records the human disposition of these named limitations.
