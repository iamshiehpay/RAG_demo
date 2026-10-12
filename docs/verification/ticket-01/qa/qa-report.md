# QA report: ticket #01 Walking skeleton (integrated, main @ cf49802)

Model: claude-sonnet-5-5. Date 2026-10-12. Server started per README on port 8201 (`uv run uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8201`). UI driven with agent-browser (real Chromium, upload through the page's file input, no JS dialogs).

Summary: acceptance criteria 7 PASS / 0 FAIL / 0 UNPROVEN. Test-list rows mapped to #01: see second table. Observations (not #01 failures) at the end.

## Acceptance criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| AC1 | One command starts; upload LightRAG in the browser, then ask | PASS | README command ran as written; `03-ready.png` ("lightrag.pdf · 37 Chunks · Ready", Ask enabled after Ready; input disabled before upload in `01-home.png`) |
| AC2 | Q3 streams; `[C#]` opens original text + page | PASS | `q3-stream-poll.txt` (text grows in "Provisional answer" state, then "Answer complete"); `06-q3-citation-open.png`, `q3-c3-source-text.txt`: C3 opens "Source · p.8", text starts "Table 2: Performance of ablated versions of LightRAG..."; PyMuPDF confirms that text is on PDF page 8 only. Also `[C4]` clickable mid-stream before final (`09-zh-streaming-provisional.png`), opens p.9 text containing 610 |
| AC3 | Trace: per-call estimated tokens, prompt_eval_count, think, 10K bar, retrieved Chunks + scores | PASS | `07-q3-trace-open.png`, `q3-trace-text.txt`: "answer · think=medium", estimated prompt 2075 (incl. 300 margin), prompt_eval_count 1850, reservation 3000, eval_count 1645, latency, done_reason stop; `<meter max=10000 value=5075>`; 5 retrieved Chunks with cosine scores (p.8 0.7241 first, Table 2 chunk); Model thinking collapsed. Chunks expandable |
| AC4 | DET: every fake-LLM call prompt + reservation <= 10,000 | PASS | `uv run pytest -q`: 20 passed in 9.3s (`pytest.txt`); test_operations.py line 45 asserts `prompt_tokens + num_predict <= CONTEXT_BUDGET`; real bge-m3 used |
| AC5 | DET: guard trips, ask emits `error`, no `final` | PASS | `test_guard_emits_error_without_final_or_llm_call` (code budget_exceeded, no final, zero LLM calls) passed; also `test_real_10k_*` tests |
| AC6 | HTTP contract: plan -> retrieval -> citation_map -> delta... -> final -> trace | PASS | pytest `test_ask_http_sse_order_and_citation_source`; independent live check `sse-order.txt` (plan, retrieval, citation_map, 241 delta, final, trace; plan = Lookup) |
| AC7 | Frontend TS event types match backend models | PASS | `test_frontend_types_match_backend_event_models` passed; `scripts/generate_event_types.py --check` -> "Backend and frontend event types match." ruff check and format --check clean |

## Test-list rows mapped to #01

| ID | Result | Evidence / reason |
|---|---|---|
| ST-01 (#01 part: README start, site loads, dist committed) | PASS (partial scope) | Start via README command and page load verified. Not verified: clean clone, no-node machine, `git diff` empty after rebuild (needs node/clean clone; owned by #09/#11) -> UNPROVEN for those sub-claims |
| ST-02 (#01 part: fetch_data.sh) | NOT_EXECUTED | Used existing data/lightrag.pdf; script not run (would touch data/); hash stability, ignore rules and README Ollama note not checked |
| TB-02 (#01 part: Lookup top 5) | PASS (partial) | Q3 retrieval top-1 is p.8 Table 2 chunk (0.7241); prompt order/links belong to #03 |
| BG-01 (#01 general) | PASS (DET, for #01 call types) | AC4 evidence; other call types belong to later tickets |
| BG-02 | PASS | AC5 evidence (DET). UI display of budget error not exercised in browser -> UI half NOT_EXECUTED |
| BG-03 | PASS | AC3 evidence: all fields present; estimate >= prompt_eval_count in all 4 calls (2075/1850, 2285/2060, 2184/1959). Latency, done_reason shown |
| BG-04 | PASS | scripted/recording LLM drives full upload+ask in pytest; same event contract as live (AC6) |
| FL-07 (#01: order, types) | PASS | AC6 and AC7. `thinking` event not emitted (none in live SSE); GAP, not #01 scope |
| CT-01 (#01: popup, 404) | PASS | Popup shows original Chunk text, page matches PDF (p.8, p.9). Unknown id: `source-404.txt` `{"detail":"Source not found."} HTTP 404` (also with a Document loaded, via browser fetch of `C3` -> 404). Position labels come from backend map (aria-label "View C3, page 8, Virtual Section 8"). Margin-note placement is #02/#09 |
| CT-03 | PASS | `[C4]` was a clickable button while status was still "Provisional answer"; `[C3]` clickable after final |
| QA-05 (#01 prompt rule, D01 Q2=A) | PASS | "What license is LightRAG released under?" -> exactly "Not mentioned in the document." (`q4-license-text.txt`); no invented content, no citation. Trace shows highest similarity 0.5142 in retrieved list (`q4-license-trace.txt`). Chinese "LightRAG 的授權條款是什麼？" -> "文件中未提及" (`q6-zh-license-text.txt`) |
| QA-06 (#01 prompt rule) | PASS | Chinese question 成本差異 -> Chinese answer retrieving English text; numbers preserved (1,399, 610, 1,000, < 100 tokens, one API call), `[C4]`/`[C5]` valid (`q5-zh-cost-text.txt`, `10-zh-cost.png`). Semantic judgement by QA: correct per Golden Fact cost point |
| TR-01 (#01: chunks+scores, no sub-queries for Lookup) | PASS | `q3-trace-text.txt`. Question Type / Standalone Question / Sub-queries not displayed in Trace (plan event only carries them) -> not required by #01 |
| TR-02 | PASS (bar), UNPROVEN (width ratio) | meter min 0 max 10000 value = 5075 = prompt estimate + 3000 (value matches call numbers); rendered bar visibly half-full; no explicit 10K tick label; ratio of DOM width not measured |
| UX-01 (#01: delta increments) | PASS | 241 delta events live; poll shows stages "Retrieving evidence…" -> "Thinking…" -> provisional text -> complete (`q3-stream-poll.txt`). Stage labels differ from the final design (#06/#09) |
| FL-03 (#01 part) | PASS (partial) | Provisional label + italic status during stream, "Answer complete" after final. Full "no definitive style mid-stream" check by DOM only |
| UP-01..UP-08, PA-*, TB-01/03/04, SM-*, RT-*, RV-*, FL-01/02/04/05/06, CT-02, QA-01..04/07..09, TR-03/04, UX-02/03, EV-*, D2-* | NOT_EXECUTED | Mapped to other tickets, not part of #01 |

D01 check: Q1=A (prompt requires citation on every claim; only invalid ids get Unverified in #07: not implemented yet in #01, correctly out of scope); Q2=A verified in English and Chinese above.

## Observations (not counted as #01 FAIL)

1. Q3 answer quality (semantic): the model describes "LightRAG vs NaiveRAG / NaiveRAG-High" figures as if they were ablated versions, never mentions `-Low`/`-Origin`, so it misses both Golden-Fact counterintuitive points, and concludes "ablated versions consistently outperform NaiveRAG". Only one `[C3]` appears, at the very end, although the prompt requires a citation on every claim. README states precise Table 2 interpretation is not a #01 claim; belongs to #03/#08.
2. Answer text shows raw markdown (`**Agriculture:**`, `- `) because the UI renders plain text. Cosmetic, #09.
3. Table 2 source popup renders one cell per line (structure lost), expected until #03.
4. Tool artifact: my first click on `[C3]` did nothing because agent-browser clicked at off-viewport coordinates; after scrolling into view it opened correctly (server log shows `GET /api/sources/...chunk-18 200`). Not an app defect.
5. Working tree shows ` M .scratch/chat-with-document/EXECUTION.md`; not modified by QA.

## Cleanup

agent-browser session closed, uvicorn killed, `lsof -i :8201-8209` empty. No source/commit changes; only new files under `docs/verification/ticket-01/qa/`.
