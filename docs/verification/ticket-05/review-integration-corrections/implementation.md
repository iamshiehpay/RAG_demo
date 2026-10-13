# Issue05 independent integration corrections

Old frozen head: `0663db096056c985f9e414509ee16efd32f67a31`; unchanged ancestry base `d371b79e000a63cec14ac26b4aecc63ea25af8dc`. Independent D04 reviewer `nova-r05sol-zero` authorized the bounded source transition in HCOM #8552; Main/reviewer were notified before edits. Main confirmed the defect blocks Issue05 integration and authorized this correction in #8635; reviewer confirmed snapshot reads complete in #8643. No merge/push/self-review or extra agents.

## Deterministic source defect and correction

The reviewer reproduced a Section built from valid Table Chunks below 2,000 tokens. Flattening their text and applying split_text at the Section capacity cut rows/cells and allowed a partial request without its original Table caption/header. This can change numerical comparison meaning before summarization.

The new test `test_section_summary_partitions_preserve_complete_table_chunks` reproduces through **Application.upload_document, actual PyMuPDF parser/chunker, real local bge-m3, ScriptedLLM and actual LLMGateway**. Its 12-page PDF contains one Section with 12 Table Chunks of 1,064–1,125 tokens. Before the fix, the raw Section requests split Chunk 8, failing the assertion that every entire original Table Chunk appears in exactly one request (`table-boundary-red.txt`). No guards or budgets are mocked/bypassed.

The Section summary seam now receives the ordered list of original Chunk texts and packs them with the existing whole-unit batches helper. It reserves the same actual prompt/title overhead, respects the same 8,500 prompt cap, and keeps original Table captions/headers/rows together. No Table parser/Chunker, group packing threshold, answer/summary prompt, model, budget or fact/checker changes were made. Oversized individual source units still fail explicitly rather than being cut or silently truncated; supported Chunking bounds Table units to 2,000 tokens. Split/recursive merge titles, all-Chunk provenance, warning propagation and completion/cancellation behavior remain intact.

The three summary integration files pass **27 tests**, 77.02s (`summary-green.txt`), including the new public-path regression and existing multi-round recursion/provenance/cancellation checks. Full/static/build results follow below.

README now describes [C#] Chunk and [S#] Summary Citations, summary n/N upload progress, whole-Chunk Section packing, and only the final Tufte design as a later ticket.

## Live semantic finding and Issue11 handoff

The original live report is preserved unchanged: `eval/reports/summary-tree-global-integrated-q1.md`, actual source revision aa50859, Q1 5/8 and Chinese 7/10 FAIL, all 49 calls stop and within guard. It contains the Chinese assertion:

> 在农业、计算机、法律和混合四个领域的实验中，LightRAG 在全面性、 多样性、赋能和整体四个维度上相较于 NaiveRAG、RQ‑RAG、HyDE 和 GraphRAG 均取得更高的胜率，尤其在大型数据集上表现出显著优势。[S11][S12]

This overstates the source: Table1 Mix Overall has GraphRAG50.4% versus LightRAG49.6%. Its recorded NOT_ALL_BEST forbidden result is PASS. The deterministic coverage probe imports the actual Golden Facts and shows **Q1 lacks Q2's GraphRAG all-datasets forbidden fact**; Chinese inherits the Q1 facts. Existing NOT_ALL_BEST targets a different universal claim (best on every dataset/metric, particularly full-system/ablation comparisons). No run applies the Q2 fact to that answer, so this does not establish a same-fact judge false negative. Judge adherence also remains imperfect: earlier Q1 fact excerpts are genuinely nonverbatim.

The recorded Section calls have estimated prompts of at most2,303 tokens, far below the8,500-token Section cap; the oversized split defect does not explain this particular live overclaim. The report contains call counts and finalized answers but not the generated summary texts. It cannot determine whether the specific Table1 exception was lost during upload or answer generation. No semantic correction or new current-source live quality pass is claimed. Main explicitly assigned final semantic quality/evaluator reliability to #11 (#8517), and the exact observed claim, original outcome and proven fact-coverage gap were sent to `nova-i11-meme` with reviewer/Main copied. Its handoff acknowledgement #8573 distinguishes those findings. No topic-specific prompt fitting or fact/checker relaxation was applied. The final #11 N=3 gate remains outstanding.

The latest Section-packing correction invalidates the upload cache by the existing source fingerprint. Historical live report remains tied to its actual earlier revision; it is not relabeled as a live run of this revision.

## Nonblocking findings and evidence

Independent reviewer #8613 found no additional blocking deterministic Issue05 defect. P1 generic warning lacks precise affected table identity but retains the limitation and Section/page provenance (low UX precision). P2 several ask_calls==[] tests can hide unexpected summary calls but current ask never invokes the builder and separate full-call cache checks exist (nonblocking test hygiene). Neither is silently fixed or waived; both are recorded for later follow-up. R-L1 richer Group packing/detail assessment remains assigned to #10/#11.

Settings remain gpt-6.1-sol/high; workspace-write/on-request, network true, runtime auto_review. No new services/ports/browser/containers were started. Temporary read-only probes used /private/tmp; a pytest collection attempt there encountered an unreadable unrelated directory and was replaced by direct invocation of the same async test. The repository test then reproduced the actual defect and its fix. All worktree changes remain within Issue05 and evidence/docs.

## Path inventory

- `src/chat_document/summary_tree.py`: Section input changes from flattened string/character split to list of whole Chunk texts and batch packing.
- `tests/integration/test_summary_table_integration.py`: new real-bge public upload regression for a long table-only Section; exact request-level complete-Chunk coverage, all Section source IDs and guarded budgets.
- `README.md`: C/S sources, summary n/N, implemented scope and whole-Chunk batching.
- `docs/ai-log.md`: deterministic splitting error and explicit separation of observed overclaim, coverage gap and unproven same-fact Judge failure.
- `docs/verification/ticket-05/review-integration-corrections/`: RED/GREEN, full/static/build/source-render logs, read-only coverage probe and this report.

No other production/test/frontend/eval code changes since0663db0. Frontend production build is identical; prior generated bundle remains committed. Parser, Table Chunking, RetrievalEvent/drop fields, Summary warnings, SourceContent and Golden Facts/checker bytes are unchanged.

## Final verification

Full deterministic suite: **265 passed, 2 eval tests deselected**, 241.55s (`full-regression.txt`). Prior integrated run was264 passed in251.68s; this run adds the public table-boundary regression and finishes10.13s faster. Main's wall-clock observation of a potentially slow run did not indicate a test stall; progress continued and no workload was restarted. No material runtime/environment degradation was observed. Both runs use the same local bge-m3 and scripted LLM with no cloud answering.

Static checks pass:

- Ruff/format: PASS, 53 formatted files.
- Event parity: PASS.
- TypeScript and production build: PASS.
- SourceContent uncertain/reconstructed source render: PASS.
- Diff check: PASS.

Revised exact SHA and clean status will be sent to the independent reviewer/Main for read-only review. This report makes no review verdict claim.
