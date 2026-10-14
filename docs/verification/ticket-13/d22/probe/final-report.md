# D22 final diagnostic handoff — seven calls, no repair candidate

A9 remains unresolved. Seven fresh gpt-oss calls completed; no eighth call, answer candidate, product edit or deployment. Full-context baseline/gated extraction refuse; neutral full-context inventory omits the key caveat and contaminates author provenance. Complete-C5-only inventory recovers the caveat, but complete-C5-only baseline answer reverses variants and invents limitations. Local non-refusal is not source support.

| Ordinal / condition | Frozen condition | Concrete result | Estimated prompt + 3000 | Provider prompt + generated | Latency ms |
|---|---|---|---:|---:|---:|
| 1 / 17 | Full baseline | exact refusal; known supplied support omitted | 4104+3000 | 3879+249 | 2259 |
| 2 / 42 | Full gated evidence extraction | exact refusal; relevance-gate confound | 4262+3000 | 4037+412 | 2123 |
| 3 / 63 | Full neutral inventory | correct removal definitions, but no noise caveat; annotation labelled author claim | 4010+3000 | 3785+2825 | 8987 |
| 4 / 28 | Baseline qualified synthetic control | subject/condition/author hedge preserved | 854+3000 | 629+370 | 2023 |
| 5 / 91 | Baseline absent synthetic control | exact 文件中未提及 | 853+3000 | 628+105 | 1295 |
| 6 / 54 | C5-only neutral inventory | target caveat/removal recovered; literal quote fidelity still flawed | 1010+3000 | 785+2047 | 6598 |
| 7 / 76 | C5-only baseline answer | reversed variants; unsupported full-method and original-text-loss claims | 1104+3000 | 879+508 | 2260 |

All seven completed with stop. Zero provider errors, length failures, retries, extra judges, Router/embedding calls, account workarounds or budget/model changes. Existing gateway policy medium/3000, gpt-oss:120b-cloud, temperature0, formatNone. Maximum estimated total7262; provider total6610. Source trace, all stream frames, final output and gateway token/latency events are preserved per condition. Thinking is raw provenance only, not causal proof.

## Actionable findings and limits

- Full-context neutral inventory condition63 recovers -Origin's original-text removal and -High's high-order removal but omits the final C5 sentence about irrelevant original text often introducing possible response noise. It labels an added C4 “Include that row” instruction as author text and claims every entry is authored. Several purported exact quotations use altered text/ellipses. It fails the preregistered readiness gate, so no generic answer candidate exists.
- C5-only neutral inventory condition54 now includes the original-text often/irrelevant/can-noise sentence and removal definition. It quotes with inserted Markdown emphasis and typographic hyphen changes, uses the unsupported exclusive label “semantic-graph-only,” and calls “Surprisingly” a hedge. Semantic recovery alone is not flawless exact evidence extraction or a public-path fix.
- C5-only baseline answer condition76 labels -Low low-level-only and -High high-level-only, reversing the supplied definitions. It invents a full-method need for a balance to avoid the ablated deficiencies and speculates that losing original-text detail causes limitations. It does not recover the authors' noise caveat as the answer. Valid C5 IDs or non-refusal cannot validate those claims.
- The synthetic two-subject qualified control preserves Cedar's condition, occasional observation, author hypothesis/may-contribute language and nonsole-cause limitation without importing Birch's restriction. Raw output uses 【C1】. Correction to earlier v2 framing: this is a raw ASCII-instruction variation, not a new product Citation failure or semantic failure. Existing CitationText normalized the captured frames to [C1] in a deterministic one-shot seam check; full public Application normalization was not exercised. The absent question returns the exact fixed refusal.

Full/local neutral pair changes only complete supplied source composition/length (six other sources removed), with identical system instruction, user-question tail, C5 text/header/ID and model options. Full/local baseline pair does likewise. This is evidence that the task's output differs with these contexts in these single samples; it cannot isolate source interference, position, length or randomness as a cause. It does not show that all extraction tasks fail, that model understanding is impossible, that an extra LLM call is necessary, or that any retrieval change repairs A9. Original uncaptured Global/Section/history failure remains unexplained.

Recommended next step for Main: preserve these FAILs and decide separately whether to fund a small, preregistered evidence-fidelity study before any product answer candidate. The two necessary output criteria are independent: faithful complete evidence inventory and faithfully scoped final answer. This experiment does not justify integrating either tested task or changing retrieval/model/budget. No unused-call prompt variants are proposed for this run.

## Protocol, independent assessment and inventory

protocol.md/results.md retain v1; protocol-v2.md/results-v2.md retain the explicitly authorized neutral/control amendment; protocol-v3.md freezes Main's mutually exclusive C5-only branch after full-inventory FAIL. Later disposition/corrections in this report supersede provisional outcome language without deleting it. Main message references: #19089 neutral/control amendment; #19138/#19154 local branch and stop-at7; #19157 existing Citation normalization clarification.

Assessor Muko owns ../assessment/** and independently judges condition outputs. Neutral IDs provide output-label blinding only; raw task instructions reveal condition. No full blinded assessment or product Review is claimed. Complete raw files condition-{17,42,63,28,91,54,76}.json; call-accounting.json; frozen neutral-instruction.txt/controls.json/local-context.json; deterministic invariants-v3.json and citation-normalization.json; manifest.json includes SHA256 of all owned evidence. manifest-v1/v2 preserve pre-amendment hash snapshots, including earlier run.py hash states; final manifest is authoritative for current files.

Gina native session01a13851-ca3f-7e81-bac0-c503c8d4684a; Main directly verified turn01a13853-93d6-7693-86a4-16d35bd02eb3 as exact gpt-6.1-sol medium/workspace-write/on-request. auto_review is escalation reviewer, a different setting. No delegation.

Only probe/** written by Gina; assessment/** is Muko-owned. No services, ports, /tmp artifacts, browser or background probe process; Main Python reused read-only with PYTHONDONTWRITEBYTECODE=1. No PDF ingestion/cache rebuild or ordinary suite needed for diagnostic-only artifacts. Product source, tests, retrieval, Golden Facts, frontend/dist and prior FAILs remain unchanged. Shared task-card cleanup information was sent to Main. No merge/push. Evidence commit remains coordinated with assessor completion/Main; no delivery claim.
