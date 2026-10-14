# D21 diagnosis checkpoint — not a repaired candidate

## Actual findings

Baseline 58586f7's public `Application.ask` reproduces the exact fixed-refusal symptom with an actual Synthesis classification, both without history and with one counterfactual overview-history round. This is distinct from the user's original Global/Section observation. That observation cannot be reconstructed exactly because its history and source payload are missing.

The baseline answer receives the author discussion from p8 §4.3, including removal of original text in `-Origin` and the conditional statement that irrelevant original text can introduce response noise. Retrieval therefore does not explain absence of that specific evidence in the standalone baseline. Baseline model reasoning treats absence of a dedicated self-limitations discussion as absence of an answer. This is evidence about this captured call, not a universal causal claim.

## Probe results

| Evidence | Upstream | Mechanical result | Grounding assessment |
| --- | --- | --- | --- |
| baseline-standalone | live Router + embedding | FAIL: fixed refusal | Relevant conditional source supplied; omitted |
| baseline-history | live, counterfactual overview | FAIL: Synthesis/refusal | Does not explain original Global observation |
| answer-scope-standalone | live | FAIL: refusal | No repair established |
| conditional-caveat-standalone | live | non-refusal + valid IDs | FAIL: reverses `-Origin` as retaining only original text; baseline/variant catalogue |
| controlled-scope | recorded baseline Router/vectors; live answer | FAIL: refusal | Same original sources; no repair |
| controlled-partial-evidence | controlled upstream; live answer | non-refusal + valid IDs | FAIL: variant catalogue and uncited unsupported necessity conclusion |
| controlled-subject | controlled upstream; live answer | non-refusal + valid IDs | FAIL: baseline/variant catalogue, unsupported full-method extrapolation |
| controlled-tail-scope | controlled upstream; live answer | FAIL: refusal | Scope reminder after context does not repair omission |

All raw requests, frames, Router JSON, rewritten questions, retrieval events, original Chunks, supplied source maps, final answers, and token traces are retained in `live/`. Controlled upstream is explicitly labelled; its Router trace is historical evidence, not a new model call. The script's non-refusal/Citation checks are mechanical only; they do not establish claim support.

Initial probes used thirteen actual provider calls including one minimal guarded preflight; no 429, retries or truncation. One subsequent independently proposed paragraph-presentation probe added one actual answer call (fourteen total); see `independent-diagnosis.md`. Largest initial estimated prompt plus output reservation is 7,741, under 10K. No full ordinary suite or final real acceptance set has run because no final repaired source exists. No broad N=3/eval, fresh ingestion, critic calls, model changes, or budget changes.

## Preserved failure and current source

The last failed source delta is saved as `failed-answer-candidate.patch`. All experimental production changes were then removed, restoring `answer_generator.py` to deployed 58586f7. No Router/history/application source change remains. This avoids presenting a known failed experiment as a deployment candidate. The strict baseline replay on the restored source still goes red on `Unexpected fixed refusal` and now rejects mismatched prompts rather than replaying old outputs under a changed prompt.

## Resources and provenance

- Own worktree: `/Users/shiehpay/Desktop/resume/rag/.worktrees/13-a9-routing`.
- Ignored copies: `data/lightrag.pdf`, `data/industrial-robotics.pdf`.
- Copied deployed cache records: `.cache/833ea057185857ffe9ebc55321a245c0c2765d32f8b43ded5b2b24e00f8c6802.json` and `.cache/eefa4dc0c41f780b997cd7024b870ac6d669b1ae61dae3820641c21fcfeac0bc.json`.
- Baseline fingerprint: `ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f`. Experimental answer changes honestly invalidated it; controlled runs explicitly loaded a frozen source fixture and never claimed public upload/Ready or rewrote a key. Restored source has baseline fingerprint again.
- Reused Main Python read-only; `chat_document.application.__file__` verified inside this worktree. Main cache, venv, old failed 9715538, frontend and running services were not mutated.
- No ports, browser, server, or background process owned. All CLI probes exited.
- An accidentally launched predefined code-mapper role was interrupted immediately for model-default mismatch; its conclusions were not used. A separate exact GPT6.1-sol medium built-in read-only map verified workspace-write/on-request, native thread `01a13826-357a-77b0-a606-f50024dc7ee3`; only public seams/fixture locations were used, no causal conclusions. Main was notified of the correction.

## Remaining work

A9 repair, final with/without-history and held-out checks, absent fixed-refusal check, unrelated author-qualified limitation/warning check, meaningful regressions, full ordinary suite, independent Standards/Spec reviews, and genuine current-key upload validation remain NOT_EXECUTED. Original Global cause remains unknown. No claim of delivery or defect acceptance.
