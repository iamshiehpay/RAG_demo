# Independent diagnosis and one presentation probe

Independent diagnostician: `gera-a9diag-dale`, native session `/Users/shiehpay/.codex/sessions/2026/10/14/rollout-2026-10-14T10-12-44-01a1382e-f592-70b2-8ce5-856ea8a3feba.jsonl`, bootstrap turn `01a1382e-f64d-7661-9527-dea0c3ba4484` at 02:12:46.108Z. Parent directly verified exact `gpt-6.1-sol`, `medium`, `workspace-write`, `on-request`, correct isolated cwd. Main was sent the locator/settings before diagnosis. Read-only release followed verification. No edits, tests, provider calls, or delegation by diagnostician; this is not formal Review or approval.

Conclusion from hcom request #18665: captured baseline model judges source relevance at Chunk grain. It dismisses C5 as ablation evidence, also missing the distinct conditional original-text/noise claim in that Chunk. Paragraph presentation might contribute because one header combines three retrieval-mode discussions and the original-text paragraph after a large table. Request construction, missing source, truncation, malformed Router output, or summary-only instruction conflict is unsupported in the captured Synthesis path. Original Global cause is unknown.

Exactly one minimal candidate was proposed and then authorized by Main #18687: repeat the same C# plus original Section/page metadata around each verbatim blank-line-delimited text paragraph. Preserve order, whole Table Chunks, original source lookup/Citation IDs. Use identical formatting for retrieval sizing, pack, and AnswerGenerator fallback. No semantic tagging, source removal, question-specific selection, new call or prompt-rule change.

## Contract and live check

The public `Application.ask` contract test in retained `test_paragraph_evidence.py` first FAILed on deployed 58586f7 because the second prose paragraph lacked repeated source metadata (1 failed, 0.49s). With `failed-paragraph-candidate.patch` applied, it PASSed (1 passed, 0.30s), confirming paragraph identity/order, intact table, original Citation lookup, two-call path, and guarded budget. Scripted outputs in this test do not establish semantic fidelity; it tests presentation only.

Live controlled command:

`PYTHONPATH=src:. /Users/shiehpay/Desktop/resume/rag/.venv/bin/python docs/verification/ticket-13/d21/feedback.py --frozen-document .cache/833ea057185857ffe9ebc55321a245c0c2765d32f8b43ded5b2b24e00f8c6802.json --controlled-upstream docs/verification/ticket-13/d21/live/baseline-standalone.json --output docs/verification/ticket-13/d21/live/controlled-paragraph.json`

Result: FAIL, exact fixed refusal `文件中未提及`, no Citations. The raw source/answer request retains the original conditional statement, now independently source-labelled; response still omits it. One new actual answer provider call, fixed recorded Router/query vectors, no retrieval/prompt changes. This weakens the paragraph-presentation hypothesis as an effective repair; no non-refusal or grounding PASS.

The full failed source delta is retained in `failed-paragraph-candidate.patch`, with its contract test archived beside it. Experimental production changes were removed and the ordinary test directory restored, leaving only evidence/harness files. No current-key upload or full ordinary suite was spent on the failed candidate. No further prompt or provider variants were attempted after this failure.

Both proposed repairs remain failed evidence. A9 is not repaired; no acceptance/Review/deployment is claimed.
