# QA re-verification 2: ticket #06 after Router repair

Model: claude-sonnet-5-5. main @ b005721 (includes f9f1651, 9d03295, 1da2d22). App on port 8202, real Ollama bge-m3 + gpt-oss:120b-cloud, real headless browser (session qa06b). First report `qa-report.md` is kept. No source modified, nothing committed.

Orchestrator decisions applied: live Q2 coverage of the 610-cost / incremental-update passages is deferred to #11 and reported as "FAIL, deferred to #11"; Q3 routed to Synthesis after history is acceptable.

## Results of the seven checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Q2 genuine Router plan | PASS | Trace: Synthesis, Plan source `router`, 3 Sub-queries (LightRAG vs GraphRAG mechanisms / performance metrics / cost and maintenance). `r2-q2-trace.txt`, `r2-02-q2.png`. Stage order 判斷問題類型 -> 檢索 -> 思考中 -> Answer complete (`r2-q2-stages.json`; 檢索 took about 19 s because pytest was running at the same time, a load artifact). |
| 1b | Q2 retrieval covers 610 cost and incremental update | FAIL, deferred to #11 | Retrieved chunks p.6, p.7, p.7, p.9; trace text contains neither "610" nor "incremental" (`r2-q2-retrieval-check.json`). The Sub-queries are short and generic; the answer lacks the cost and incremental-update points. Not counted as a #06 failure. |
| 2 | Follow-up "那它的成本呢？" | PASS | Standalone Question "LightRAG 的成本是多少？" (Traditional characters, referent resolved), plan source router (`r2-followup-trace.txt`, `r2-03-followup.png`). |
| 2b | Follow-up answer script | FAIL (minor, new finding) | The answer is in Simplified Chinese ("检索阶段", "增量更新阶段", "个 token") although the question is Traditional (`r2-followup-answer.txt`). The language rule works (Chinese for Chinese) but not script. Not on the coordinator's list; reproduce: ask Q2, then the follow-up, read the answer. |
| 3 | English Q3 after Chinese turns | PASS | Standalone Question in English, English answer (`r2-q3-after-chinese-answer.txt`, `r2-04-q3-english.png`). Table content quality (for example -Low missing, "High" mislabeled as a LightRAG variant) belongs to #03/#08, not graded here. |
| 4 | Fresh-session Q3 | PASS | Lookup, Plan source router, router done_reason stop (eval 109/600). `r2-q3-fresh-trace.json`. Earlier run failed with length. |
| 5 | Fallback visible | PASS | A 950-token repeated question reliably provokes it: Trace shows Plan source `fallback`, Fallback reason `length` (router eval_count 600/600). `r2-fallback-trace.txt`, `r2-05-fallback.png`, `r2-fallback-probe.txt` (3 of 3 fallback via SSE; 1 of 2 in UI, since another UI run returned router/Global). |
| 6 | Too-long rejection | PASS | UI shows 問題過長 plus "Question must not exceed 1,000 tokens."; Trace count unchanged (no LLM call), no retry button, input restored (9,749 chars). `r2-too-long-dom.json`, `r2-06-too-long.png`. Unchanged from report 1. |
| 7 | All calls <= 10K | PASS | Maximum observed: router 3,366 (with a 950-token question), answer 5,673; every call under 10,000. |

Extra observation: for the nonsense 950-token question the router returned Global, which goes through the Synthesis path (documented #05 deferral).

## Deterministic and live smoke

- `uv run pytest -q`: 68 passed, 1 deselected (`pytest-full-2.txt`).
- `uv run pytest -m eval tests/integration/test_router_smoke_eval.py -q`: 1 passed (`router-smoke-eval.txt`, `router-smoke-report.json`). Canonical 12/12 correct, 0 fallbacks, 0 rewrite failures. Held-out 8/8 correct, 0 fallbacks, 0 rewrite failures. The run also wrote `eval/reports/router-smoke-20261012T165103285734Z.json` (untracked, left for the coordinator to commit or discard).

## Acceptance criteria (#06)

| AC | Result | Basis |
|---|---|---|
| AC1 plan event and Trace show Type, Standalone Question, Sub-queries | PASS | Live Q2, follow-up and Q3; Trace adds Plan source and Fallback reason. FAIL-1 from report 1 is resolved. |
| AC2 malformed JSON gives Lookup | PASS | Deterministic test plus live fallback labelled in Trace. |
| AC3 >1,000 tokens rejected, 0 LLM calls | PASS | Check 6; boundary 1000/1001 checked in report 1. |
| AC4 history at most 2 rounds, 500 tokens each | PASS | Deterministic test; live follow-up and the English Q3 resolved correctly. |
| AC5 Q2 Sub-queries cover cost and incremental update | PASS (scripted) / live FAIL, deferred to #11 | Scripted test passes; live retrieval does not cover them (check 1b). |
| AC6 forced overflow gives batch extraction with valid Citations | PASS (deterministic) | Suite; not triggered live (default top-k fits). |
| AC7 router 12-question eval report | PASS for live smoke (12/12 canonical, 8/8 held-out); NOT_EXECUTED for #08 eval integration | #08 not merged. |

Gap 5 (rejection event) PASS. Gap 8 (configurable top-k) PASS (verified in report 1; suite still green).

## Test-list rows

| Row | Result |
|---|---|
| RT-01 | PASS (live and deterministic; plan source recorded) |
| RT-02 | PASS via live smoke (12/12, no Synthesis-to-Lookup errors); #08 eval report NOT_EXECUTED |
| RT-03 | PASS |
| RT-04 | PASS |
| RT-05 | PASS |
| RV-01 | PASS scripted; live FAIL, deferred to #11 |
| RV-02 | NOT_EXECUTED (#05) |
| RV-03 | PASS deterministic; not live |
| BG-01 | PASS for all live calls and the deterministic suite |
| FL-06 | PARTIAL (deterministic router and embedding failure tests PASS; UI retry owned by #07) |
| QA-03 | PARTIAL: Synthesis live PASS; forbidden-fact judging belongs to #08 (answer said LightRAG "consistently outperforms GraphRAG", which contradicts Mix Overall, left to #08) |
| QA-06 | UNPROVEN as specified (the Chinese follow-up answer was Chinese but Simplified; the specified question was not run) |
| QA-07 | UNPROVEN (limitations question not run live in this pass) |
| QA-08 | PASS live and deterministic (referent resolved in Traditional Chinese) |
| TR-01 | PASS (plan, plan source, sub-queries for Synthesis, none for Lookup, chunks, per-call budget) |
| UX-01 | PASS |

## Cleanup

Browser session qa06b closed, uvicorn on 8202 stopped, ports 8202-8209 free. Other agents' processes untouched.

## Final spot-check (main 5799106, fix for the Simplified-answer finding)

Real browser (session qa06c), port 8202, LightRAG uploaded; `uv run pytest -q`: 76 passed, 1 deselected (`r3-pytest.txt`).

| Check | Result | Evidence |
|---|---|---|
| Q2, then "那它的成本呢？" | PASS | Standalone "LightRAG 與 GraphRAG 的成本比較是什麼？", Synthesis, plan source router. The answer is in Traditional characters (檢索階段, 產生, 個, 呼叫, 增量更新) with no Simplified forms (`r3-followup-trad.json`, `r3-01-followup-trad.png`). Report-2 FAIL 2b is resolved. |
| Simplified question "这篇论文的主要贡献是什么？" | PASS | The answer stays Simplified (贡献, 检索, 图, 个) (`r3-simplified.json`, `r3-02-simplified.png`). Observation, not a failure: the router's Standalone Question converted this to Traditional ("這篇論文的主要貢獻是什麼？"); the answer script still followed the user's question. |
| English question | PASS | English Standalone Question and English answer (`r3-english.json`, `r3-03-english.png`). |

### Final per-AC verdict (#06)

| Item | Verdict |
|---|---|
| AC1 plan event and Trace (Type, Standalone Question, Sub-queries, plan source) | PASS |
| AC2 malformed JSON gives Lookup (fallback labelled) | PASS |
| AC3 >1,000 tokens rejected, 0 LLM calls, input restored | PASS |
| AC4 history 2 rounds, 500 tokens each, referent resolved | PASS |
| AC5 Q2 Sub-queries cover cost and incremental update | PASS scripted; live Q2 retrieval coverage is deferred to #11 (the Traditional follow-up did retrieve the 610 and incremental passages) |
| AC6 forced overflow gives batch extraction, valid Citations | PASS (deterministic) |
| AC7 router 12-case eval | PASS via live smoke (12/12 canonical, 8/8 held-out); #08 eval report pending (NOT_EXECUTED) |
| Gap 5 explicit rejection event | PASS |
| Gap 8 configurable top-k | PASS |

Cleanup: browser closed, uvicorn on 8202 stopped, ports 8202-8209 free.
