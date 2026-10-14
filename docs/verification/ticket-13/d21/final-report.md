# D21 final diagnostic handoff — A9 unresolved

Main #18792 closed this bounded diagnostic phase after the independently proposed presentation hypothesis failed. This branch contains evidence and an agent-runnable feedback harness only. Product source and ordinary tests equal deployed baseline `58586f786bc507c1b8e1d933974e1e4eb7c46bf6`; no experimental source/test remains. Failed patches and the presentation contract test are retained exclusively under this diagnostic directory. No repaired candidate, formal product Review, approval, defect waiver, old `9715538` adoption, or delivery is claimed.

## Findings and limitations

Actual standalone A9 and one explicitly counterfactual prior-overview history both chose Synthesis and returned exact `文件中未提及`. The author's qualified original-text/noise statement was supplied in C5 p8 §4.3. Captured thinking dismisses the Chunk as ablation evidence, then equates absence of an explicit limitations discussion with absence of an answer. Generic instruction probes alternated refusal with invalid subject/variant claims; paragraph rendering alone still refused with upstream Router/query/source inputs held fixed. Valid Citation IDs and non-refusal did not establish source support.

The original Global/Section observation remains unexplained: original user history and source payload are unavailable. Counterfactual histories and recorded upstream controls are labelled and cannot establish that original cause. There is no claim of model reliability from these bounded calls. Final acceptance checks, fresh ingestion/current-key upload, full ordinary suite, and product review were intentionally not run on a known failed candidate.

## Calls and checks

- **14 actual gpt-oss:120b-cloud calls**: one guarded preflight, eight live Router/answer calls in four standalone/history probes, and five controlled live answer calls. Recorded Router replays are excluded from this total.
- Maximum estimated prompt plus output reservation: **7,741 tokens**, `live/baseline-history.json`.
- Maximum provider-reported prompt plus generated tokens: **5,017 tokens**, `live/controlled-partial-evidence.json`.
- Zero 429 responses, length completions, retry calls, model/account workarounds, critic calls or budget changes.
- Strict public-path baseline replay: FAIL on exact unexpected refusal; rejects changed prompts to prevent stale replay from appearing to prove a semantic fix.
- Paragraph public-path contract: RED on baseline (1 failed, 0.49s), GREEN on experimental formatter (1 passed, 0.30s). Live semantic check remained FAIL. Test is archived with its failed patch, outside the ordinary test directory.
- `git diff 58586f7 -- src tests`: empty. Worktree clean after evidence commits.

## Runtime provenance

Worker native session: `/Users/shiehpay/.codex/sessions/2026/10/14/rollout-2026-10-14T10-00-32-01a13823-cce1-7132-8bd4-a8f3983b74ad.jsonl`; initial turn `01a13824-22ba-7c12-8c93-841cc3ea7f2e` at 02:00:56.375Z. Actual `gpt-6.1-sol`, `medium`, `workspace-write`, `on-request`; Main directly verified before release. Correct isolated cwd/branch, read-only Main Python reused, local Application import verified.

Independent diagnostician `gera-a9diag-dale`: native session `/Users/shiehpay/.codex/sessions/2026/10/14/rollout-2026-10-14T10-12-44-01a1382e-f592-70b2-8ce5-856ea8a3feba.jsonl`; turn `01a1382e-f64d-7661-9527-dea0c3ba4484` at 02:12:46.108Z. Exact same model/effort/permissions verified directly and sent to Main before read-only release. No provider/edit/test work by diagnostician; its diagnosis was not approval. Completed context is stopped, transcript retained.

An accidentally started predefined role with mismatched defaults was immediately interrupted and not used. This correction was reported to Main. The separate verified exact GPT6.1 medium built-in path map supplied public seam locations only; see `assessment.md`.

## Preserved inventory and cleanup

Branch/worktree: `lat/13-a9-routing`, `/Users/shiehpay/Desktop/resume/rag/.worktrees/13-a9-routing`.

Tracked evidence: this directory's complete requests, frames, Router outputs, rewritten questions, sources, original Chunks, final answers, traces, hypotheses, independent diagnosis, two failed patches, archived contract test, replay harness and SHA256 manifest.

Ignored owned copies retained for explicit follow-up:

- `data/lightrag.pdf`, `data/industrial-robotics.pdf`.
- `.cache/833ea057185857ffe9ebc55321a245c0c2765d32f8b43ded5b2b24e00f8c6802.json`.
- `.cache/eefa4dc0c41f780b997cd7024b870ac6d669b1ae61dae3820641c21fcfeac0bc.json`.

Restored source retains baseline fingerprint `ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f`. Experimental source honestly invalidated keys; frozen source runs never rewrote keys or claimed upload/Ready. Main cache/venv, frontend, old failed worktree and deployed services were untouched.

No owned server, port, browser, background diagnostic process or ordinary temporary file remains. All probes exited; the external diagnostician was closed and stopped status verified. Worktree/cache remain as Main explicitly requested. Main owns integration, user reporting and closure.
