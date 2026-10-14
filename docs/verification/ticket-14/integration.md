# Issue 14 Main integration

Merged evidence head: `64b4f3d1bcaeadf879eec118e4e89b3afc023a16`.
Reviewed production/test/dependency source: `24fba2647c1b159049bf015bf63ca21a089cbcb6`.
Main integration checkpoint: `a5b70a0670259ee6f85a3fbe7f8d289639397eb7`.

Main directly read both original reviews and both fresh scoped correction reviews,
the final 335-pass suite, clean installation record, source changes, and all six
actual smoke answers. The initial Spec readiness race was reproduced and fixed;
fresh Standards and Spec reviews have no blocking findings. The private lifecycle
field coupling is a non-blocking observation, not a new refactoring requirement.
All reviewer runtime records and TUI observations confirm requested Luna max/Fast.

The merge was fast-forward, without conflicts. Git comparison of Main to reviewed
24fba26 is empty for `src`, `tests`, `pyproject.toml`, `uv.lock`, `frontend`,
`scripts`, and `eval`. Main-owned ADR/AGENTS/tracker/AI-log/manual QA records are
included in the integration checkpoint. Existing product prompts/models/ingestion
and frontend remain as scoped in the reviewed report.

## Post-merge verification

Completed: one ordinary complete suite in Main using the isolated
`.lat/venvs/issue14-main` environment, installed from the committed lock with
`uv sync --frozen`. Main source remained frozen during this run. Evidence is
`integration-pytest.txt` and `integration-environment.json`; candidate-worktree
results are not represented as Main integration results.

**335 passed, 3 eval deselected, zero skipped, 5 existing PyMuPDF warnings,
273.62s; explicit exit code 0.** The before/after Main HEAD stayed a5b70a0.
Main independently verified module imports and the installed editable distribution
URL point to Main, not the worktree.

After this passed, Main rechecked the existing 8101 listener and command, stopped
only project PID 17054, installed locked dependencies into production `.venv`
with `uv sync --frozen`, and started PID **3808** on the same address.
`integration-http.json` records production imports, LangGraph 1.2.15, the
processing fingerprint, and exact local asset matches: homepage, JavaScript,
CSS and one CJK font all HTTP 200. An empty-question POST to the real ask endpoint
returned the expected `document_not_ready` SSE error and completed without LLM
calls. This verifies live transport/preflight, not user UI or answer quality.

## Limits and user verification

The 20 genuine model calls belong to two bounded pre-final-lifecycle-correction
smokes, as explicitly recorded in `verification.md`. Final cancellation/readiness
behavior is covered by actual-graph public deterministic regressions. No further
quality loop or final N=3 was run. Existing A9, grounding/Golden Facts limitations
and deferred narrow-screen behavior remain recorded; this migration does not
mark them fixed.

The processing key changes to
`ingest-v2-fabcd278cc5f6bbe34a64a8699925398e3bee6d9a9a275d0c0179b3430b971b8`;
old document processing caches rebuild on reupload. No cache policy or artifact
was forged to claim a hit. Final website use remains user-run under D09, with
F1-F3 in `../final-acceptance/manual-qa-checklist.md` released and not yet executed.

## Resource handoff

Main verified all listed task temporary paths are absent, closed the remaining
recorded implementer, and removed the clean merged worktree and branch with
`git worktree remove` and `git branch -d`. All four reviewers were already stopped.
Production `.venv`, PDFs, `.cache`, PID 3808, Ollama and unrelated worktrees remain.
The resource manifest records the final state; no additional tests or cloud calls
were made during cleanup.
