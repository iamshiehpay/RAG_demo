# QA report: ticket #06 Router and Synthesis (integrated main @ 79aac57)

Model: claude-sonnet-5-5. App on port 8202 (+8203 for top-k diagnostic), real Ollama bge-m3 and gpt-oss:120b-cloud, real headless browser (agent-browser, session qa06). No source modified, nothing committed.

## Verdict

Deterministic layer: PASS (43/43 full suite; 22/22 #06 files). Live layer: **FAIL**. The live gpt-oss Router almost never returns JSON that passes `RouterPlan` validation, so every live question silently falls back to Lookup with the original question. Live Q2 shows Question Type Lookup, no Sub-queries, and an unresolved follow-up. The fake-LLM tests cannot detect this because ScriptedLLM always returns schema-valid JSON.

## FAIL-1 (blocker for AC1 live behaviour): live Router plan is almost always the silent fallback

Reproduce: start app, upload data/lightrag.pdf, ask "Compare LightRAG with GraphRAG", open Trace. It shows Question Type Lookup, Standalone Question equal to the raw question, no Sub-queries. The router thinking text says "It's synthesis. Provide sub_queries list.", so the model decided Synthesis but its JSON was rejected.

Root cause evidence (`router-probe-q2.txt`, `router-probe-others.txt`, `router-probe-12.txt`): the same request (Router system prompt, `format=RouterPlan.model_json_schema()`, think=low, num_predict=600) sent straight to Ollama. Ollama Cloud does not enforce `format`, and the prompt never names the field keys. Replies omit the required `standalone_question`, use `type` instead of `question_type`, or add `answer` / `answer_format`, which `extra="forbid"` rejects. Across the 12 labeled cases only 1/12 validated. Valid plans on the Q2 phrasing: 0/3.

Other live effects:
- Follow-up "那它的成本呢？" gave Standalone Question "那它的成本呢？", pronoun not resolved (`followup-trace.json`). History was sent (router prompt_eval 657 vs 227), but the rewrite is lost.
- Q3 router call hit done_reason=length (eval_count 600/600) and fell back to Lookup (`q3-trace-final.txt`).
- Trace never says "fallback" vs genuine Lookup, so a user cannot tell.
- Q2 answer lacks the cost and incremental-update evidence, because the Sub-queries are never used. It also leads with "LightRAG generally outperforms GraphRAG ... consistently" while citing Mix Overall 49.6, which is eval/#08 territory but a symptom.

Suggested fix directions (not applied): spell out the exact JSON keys in the prompt, add lenient key normalization (`type`, missing standalone_question defaulting to the original question), raise the reservation or tighten thinking, record `router_fallback` in Trace, and add a live Router smoke check.

## Acceptance criteria

| AC | Result | Evidence |
|---|---|---|
| AC1 plan event has Type, Standalone Question, Sub-queries; Trace shows them | **FAIL live / PASS deterministic** | Plan event and Trace plan section render (`04-q2-trace.png`, `q2-trace.txt`), but live content is always the Lookup fallback (FAIL-1). `test_router_plan_drives_answer_and_is_recorded_with_json_schema` and 5 `test_router_review` cases PASS. |
| AC2 malformed JSON gives Lookup | PASS | `test_malformed_router_json_falls_back_to_lookup_with_original_question`; confirmed live (the fallback is exactly what fires in FAIL-1). |
| AC3 >1,000 tokens gives rejection, 0 LLM calls | PASS | Live SSE: only `rejected` event, code question_too_long, 1908 tokens (`too-long-sse.txt`). UI shows 問題過長 with "Question must not exceed 1,000 tokens.", no Trace for that turn, no retry button, input restored (9,749 chars) (`07-too-long.png`, `too-long-dom.json`). Boundary check (`topk-diagnostic.txt`): 1000 tokens proceeds, 1001 rejected. The suite tests only 1001. |
| AC4 history max 2 rounds, each ≤500 tokens | PASS | `test_router_history_keeps_only_two_rounds_each_at_most_500_tokens`. Live: the follow-up router prompt carried history. |
| AC5 Q2 Sub-queries cover cost and incremental update | PASS (scripted) | `test_q2_sub_queries_cover_cost_and_incremental_update_in_document_order`, real bge-m3. Not reproducible live because of FAIL-1. |
| AC6 forced overflow gives batch extraction; Citations resolve | PASS (deterministic) | `test_oversized_synthesis_extracts_facts_and_keeps_original_citation_sources`, `test_extracted_facts_are_reduced_again...`, review normalization tests. Live not triggerable: Synthesis never reached. |
| AC7 router 12-question eval report | NOT_EXECUTED | #08 not merged, as expected. Live probe in `router-probe-12.txt` is a diagnostic, not the eval: 1/12 schema-valid. |

Gaps: Gap 5 (explicit rejection event) PASS (typed event, TS parity check passes). Gap 8 (configurable top-k) PASS: `LOOKUP_TOP_K=2` gave 2 retrieved chunks and the default gave 5 on the same question. `LOOKUP_TOP_K=0` fails at startup with a validation error. The Synthesis counts (1 + 4 per Sub-query) are verified only in the scripted test.

## Test-list rows

| Row | Result | Evidence |
|---|---|---|
| RT-01 one router call, think low, 600/9,100, schema, plan shape | PASS (DET) / live plan content FAIL | Live Trace: router think=low, reservation 600, budget 1172/10000. Plan shape is a fallback. |
| RT-02 router 12-question eval | NOT_EXECUTED | Needs #08. |
| RT-03 bad JSON gives Lookup | PASS | DET and live. |
| RT-04 history 2 rounds, ≤500 each | PASS | DET. |
| RT-05 1,001 vs 1,000 tokens | PASS | Live and UI; 1000 boundary live. |
| RV-01 Q2 retrieval covers cost and incremental update | PASS (scripted) / UNPROVEN live | See FAIL-1. |
| RV-02 Global uses Summary Tree | NOT_EXECUTED | Owned by #05; Global is intentionally routed through Synthesis (documented). |
| RV-03 batch extraction and merge | PASS (DET) | See AC6. |
| BG-01 every call ≤10K and matches the budget table | PARTIAL: PASS for observed live calls | All 7 live calls ≤10K (router 1172 to 1859, answer 5066 to 5599). Extraction budget table is checked in DET (`call.estimated_prompt_tokens + num_predict <= 10000`). |
| FL-06 connection failure and retry | PARTIAL (DET) | Router transport failure and query embedding failure tests PASS; UI retry button not exercised (owned by #07). |
| QA-03 Q2 Question Type Synthesis | **FAIL live** | FAIL-1; answer quality not judged against forbidden fact. The answer says LightRAG "consistently" wins, though the Mix Overall figure it cites shows GraphRAG ahead. |
| QA-06 Chinese answer | UNPROVEN | The follow-up answer was Chinese, but this is not the specified question. |
| QA-07 Limitations question is Synthesis | UNPROVEN, live probe says Router returns `type` key, so would fall back | `router-probe-others.txt`. |
| QA-08 follow-up rewrite | **FAIL live** / PASS DET | `test_successful_turns_supply_history_to_later_follow_up`; live Standalone Question stayed unresolved. |
| TR-01 Trace content | PARTIAL PASS | Plan, chunks with cosine, per-call think/reservation/estimate/prompt_eval_count render. Q2 and Q3 show no Sub-queries because of FAIL-1. |
| UX-01 stage order | PASS | Mutation log: 判斷問題類型 (12.04 s) then 檢索 (14.38 s) then 思考中 (14.51 s) then deltas then Answer complete (`02-q2-stage-early.png`). |

## Other checks

- `uv run pytest -q`: 43 passed (also 43 in the first run); `test_router_synthesis.py` + `test_router_review.py`: 22 passed.
- Ticket's "32 tests" claim is superseded: 43 is correct after review follow-up.
- Observation: Router-lookup trace for Q3 shows a router `done_reason=length` call on a live path; this is retained in Trace (correct per review test).

## Cleanup

Browser session qa06 closed; both uvicorn servers (8202, 8203) stopped; `lsof` shows ports 8202 to 8209 free. Only `docs/verification/ticket-06/` is untracked in git. Port 8110 (t02 UI app) and other Chrome processes belong to other agents and were left alone.

## Evidence files (this directory)

Screenshots `01-ready.png` to `07-too-long.png`; `q2-trace.txt`, `followup-trace.json`, `q3-trace-final.txt`, `too-long-sse.txt`, `too-long-dom.json`, `topk-diagnostic.txt`, `router-probe-q2.txt`, `router-probe-others.txt`, `router-probe-12.txt`, `pytest-06.txt`, `pytest-full.txt`.
