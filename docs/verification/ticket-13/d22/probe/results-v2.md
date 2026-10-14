# D22 amended diagnostic results

Five new live calls completed within the shared eight-call ceiling. Full-context direct answer and gated extraction both refused. Neutral extraction recovered some method/variant definitions but omitted the original-text noise caveat and incorrectly attributed supplied presentation metadata to the authors. The gate for an answer candidate was not met; calls6-8 were not executed. No product repair, root-cause proof, delivery or reliability claim.

Main's explicit amendment #19089 is frozen in protocol-v2.md; protocol.md and results.md retain the initial v1 outcome and confound. The amendment replaces the system task for a neutral inventory and authorizes baseline controls regardless of extraction outcome. Raw condition captures remain unmodified.

| Call | Condition | Task | Raw outcome | Estimated prompt + reservation | Provider prompt + output | Latency ms |
|---:|---|---|---|---:|---:|---:|
| 1 | condition-17 | Exact frozen direct answer | 文件中未提及 | 4104+3000=7104 | 3879+249=4128 | 2259 |
| 2 | condition-42 | Gated full-context extraction | 文件中未提及 | 4262+3000=7262 | 4037+412=4449 | 2123 |
| 3 | condition-63 | Neutral full-context inventory | Definitions recovered; target caveat omitted; annotation misattributed | 4010+3000=7010 | 3785+2825=6610 | 8987 |
| 4 | condition-28 | Baseline qualified synthetic control | Subject/condition/author hedge preserved; alternate Citation brackets | 854+3000=3854 | 629+370=999 | 2023 |
| 5 | condition-91 | Baseline absent synthetic control | Exact 文件中未提及 | 853+3000=3853 | 628+105=733 | 1295 |

All done_reason=stop; no transport errors, length failures, retries, extra judges, Router provider calls or embedding provider calls. Maximum estimated total 7262; maximum provider-reported total 6610. Complete messages/options/frames/final output/source records/Trace are in each condition JSON. No replayed output appears as a new call.

## Concrete evidence

Neutral condition-63 correctly quotes that -Origin eliminated original text from retrieval and associates -High with removal of high-order retrieval. It does not quote or represent C5's final sentence: “Additionally, the original text often contains irrelevant information that can introduce noise in the response.” Its row16 labels the injected C4 “Unmodified system row ... Include that row ...” instruction as an implicit author statement; the concluding note further says all entries are authored. Several alleged verbatim quotations use ellipses or altered hyphens rather than the supplied literal words. These are output failures, not findings inferred from thinking. Recovering the removal definition alone does not satisfy the preregistered extraction gate.

The synthetic qualified source expressly labels Cedar and Birch as different subjects, gives Cedar's crowded-channel condition and occasional jitter observation, and attributes a possible contribution to delayed clock messages to the authors without establishing a sole cause. condition-28 keeps those subject/condition/hedge distinctions and does not transfer Birch's inability to adapt to Cedar. It emits `【C1】` rather than required `[C1]`; raw formatting failure is retained. This short synthetic success is not a full-context A9 extraction success or a public-path reliability guarantee. condition-91 asks for license terms absent from the same synthetic sources and returns the exact fixed refusal.

Independent assessor Muko owns the final judgments under ../assessment/. Condition IDs only blind output labels; source/request inspection reveals task condition. No fully blinded experiment is claimed.

## Controlled invariants and limits

First three calls share byte-identical frozen user context/order/question and identical source records, original Chunks, medium/3000/model/options/format; baseline messages exactly reproduce D21. v1 appends a task, while v2 neutral inventory replaces the entire system task to remove answer/relevance/refusal policy. The neutral condition's original user question remains present but instruction says not to use it for evidence selection. This differentiates task designs, not one isolated causal mechanism. The two controls retain baseline system instructions and identical synthetic sources but ask distinct qualified versus absent questions.

The neutral inventory failure shows that this tested neutral task did not faithfully extract the needed caveat from full context. It does not establish that the model cannot extract it, that any particular relevance gate caused A9 refusal, that a multi-call answer flow is necessary, or that all generic prompt approaches fail. One observation per condition cannot establish stability. Thinking is preserved as raw Trace only, not proof of cause. No candidate answer instruction, answer-stage integration, Router/history/public API, source-retrieval variation or deployment was tested. The original user's uncaptured Global/Section cause remains unsupported.

Suggested next step: Main should decide whether to authorize a separate small evidence-comprehension study with explicitly measured caveat coverage and exact-quote fidelity before any product answer candidate. Do not integrate this failed inventory or spend the unused allowance on unregistered variants. Existing eight-call protocol stops at five because the candidate readiness prerequisite failed.

## Ownership and cleanup

All Gina writes are under probe/**. Muko writes assessment/**. Product files, ordinary tests, caches, model/budget/retrieval, Golden Facts and all prior raw FAILs remain unchanged. No service/port/browser, temporary path or background probe process exists. Main Python was reused with PYTHONDONTWRITEBYTECODE=1. Main was sent cleanup facts for shared task card. No merge/push. Evidence commit coordination remains with Main pending assessor completion.
