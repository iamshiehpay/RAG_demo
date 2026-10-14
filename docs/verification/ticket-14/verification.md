# Issue 14 verification

Scope: behavior-preserving migration from base `5f5e35f`, authorized D24. Upload,
PDF parsing/Chunking, retrieval, prompts, budgets, models, frontend/dist and D23
shortcut remain unchanged. Main owns accepted standards/spec/ADR/tracker updates.

## Changed paths and responsibilities

- `src/chat_document/application.py`: public ask lifecycle/error handling delegates
  orchestration to real LangGraph; upload code unchanged.
- `src/chat_document/ask_graph.py`: request-scoped validate → plan → Global Summary
  Tree or Lookup/Synthesis ContextPacker evidence → generate → finalize. Explicit
  conditional paths, no checkpoint/store/agent loop or graph retry policy.
- `src/chat_document/answer_generator.py`: necessary `aclosing` around existing
  native gateway iterator; same prompts, retry logic and reservations.
- `tests/integration/test_ask_stream_lifecycle.py`: public incremental delivery,
  provider-initiated cancellation, pending cancellation, paused-delta close, ASGI disconnect, repeated cancellation
  with slow provider cleanup, and close-after-final history/task ownership.
- `pyproject.toml`, `uv.lock`: LangGraph 1.2.15 plus necessary dependencies; AnyIO
  explicitly declared for transport cancellation shielding.
- `README.md`: actual ask graph flow and Ready → Ask instructions.
- `docs/verification/ticket-14/**`: API research, verification, actual provider and
  HTTP events, runtime settings and independent review evidence.

Graph custom events carry a consumption acknowledgment. Nodes wait until the
public consumer resumes, preserving baseline lazy event/history ordering. A
bounded queue (capacity 1) bridges an owned graph `astream(custom, v1)` task to SSE.
Transport cancellation cancels this task once and joins it under AnyIO shielding;
repeated raw `Task.cancel()` also waits for cleanup before `_asking` decreases.
This task is not detached and is never used for persistence or LLM planning.

## Test sequence and installation

Baseline characterization: 34 passed (new pending-cancel/incremental contract plus
existing failure-handling and HTTP tests). Same 34 passed with actual LangGraph.
Five missing-PDF failures in a broader targeted run were environment failures:
`data/lightrag.pdf` was absent from the new worktree. Main's ignored PDFs were
copied read-only to this worktree's ignored `data/`, with no source/test weakening.

Two material RED observations informed the implementation:

1. ASGI disconnect returned while graph/native stream work was still pending.
   Public `astream` closing alone, then a direct cancellation-payload join, did
   not solve AnyIO's repeated cancellation of framework cleanup. Owned producer
   cancellation/join plus native iterator closing fixed it. Final lifecycle suite
   tests provider-finally markers, task inventory and `_asking`/history ordering.
2. Bounded queue's old terminal sentinel could overwrite an extraction failure
   with `QueueFull`. The intermediate fix sent terminal notification only on normal completion,
   preserving the original exception. The final completion-notification design
   below removes terminal/error queue sentinels entirely. Actual RED/GREEN evidence is
   in `extraction-red.txt` / `extraction-green.txt` (12/13 then isolated 1/1).

Initial targeted lifecycle/failure suite: 33 passed, 5 existing PyMuPDF warnings,
50.33s (`lifecycle-green.txt`). Static checks: Ruff on all changed Python files
and compileall on production files passed. This repo has no configured static
type checker; no new checker dependency was introduced. The first full ordinary suite passed 332/3 deselected in 272.98s
(`full-prior.txt`), before the additional producer-cancellation correction.
Two incomplete final-suite starts were intentionally interrupted before source
freeze: one lint exception-chaining correction, one completion-drain guard.
They are not complete-suite evidence. The material correction justifies the
completed final-source full run at
`source-freeze.json`; result appended after completion.

Own environment `.venv`, Python 3.12.10, built via `UV_CACHE_DIR=/private/tmp/rag-ticket14-uv
uv sync --locked`; dependency additions resolved into the lock. A separate empty
`UV_PROJECT_ENVIRONMENT=/private/tmp/rag-ticket14-clean-env` installation with
`uv sync --locked` succeeded, and imported `create_app()` successfully.
`clean-install.txt` and `environment.json` retain exact package evidence.

## Genuine provider and public HTTP smoke

`smoke.py` runs native Ollama `gpt-oss:120b-cloud`, actual local `bge-m3` and
public HTTP upload/job-SSE/ask-SSE on owned port 8340. The authored three-page
Cedar pilot has three Sections and is unrelated to Golden Facts. Every original
request, provider frame, embedding input, event and timestamp is retained.

`live-initial/`: genuine fresh upload (3 Section Summaries + Document Summary),
then actual Global, Lookup and Synthesis; 10 provider calls total. All completed
with `stop`; maximum estimated prompt + reserved output was 4,272. Each Citation
map preceded deltas; 28/6/33 deltas arrived incrementally, Final preceded Trace,
and all final Citation objects were in the supplied map. Global retrieval was
empty. Own-key second upload emitted only Ready, and reset history. The Synthesis
answer's final derived-difference sentence lacked Citation; this raw limitation
is preserved, not fixed or labelled universal grounding PASS. Prompt bytes and
answer modules' core behavior are unchanged, so this alone does not establish a
migration cause or general quality regression.

After this run, the bridge queue was bounded and its exceptional terminal path
fixed. Main required one second transport smoke at the then-frozen source, not quality iteration.
The initial TemporaryDirectory cache had already been cleaned, so second three-path
smoke genuinely rebuilt the same small authored Document and ran three asks
(another bounded 10 calls). `live/` records that then-frozen source (production hashes in
`source-freeze-prior.json`); `live-initial/`
remains unchanged. No Golden Facts/N3/prompt tuning or large-document reingestion
was run. Actual results are appended below.

Cache policy unchanged: existing `PIPELINE_SOURCES` includes
`answer_generator.py`, so its necessary cleanup edit invalidates every old
processing key. Baseline fingerprint:
`ingest-v2-58005fcc9975f854f1986b103d0f8cb3b0c2fc7e646a2fa5d168dfdb3198c81f`.
New fingerprint:
`ingest-v2-fabcd278cc5f6bbe34a64a8699925398e3bee6d9a9a275d0c0179b3430b971b8`.
Main's old keys will rebuild on reupload; they are not represented as new Ready
records. No cache version/key-policy shortcut was introduced.

## AGENTS pre-review self-check

- Real LLM protocol: genuine Router/Answer and upload summaries exercised; real
  malformed-JSON, length retry and cancellation are not forced by live smoke.
  Deterministic public tests cover these failures with scripted external frames.
- No teaching to tests: no production prompt/model/retrieval changes; smoke uses
  an unrelated authored Document and no Golden Facts labels or paper names.
- Chinese: existing regression coverage remains in ordinary suite; new authored
  live smoke is English and does not establish new Chinese-model quality.
- Layout: existing two-column/caption/table/boxed-heading tests remain unchanged;
  no PDF parser/Chunker/table extraction implementation changed.
- Shared paths/cache: no Main-owned standards/docs writes and no frontend/dist
  changes. Existing cache fingerprint correctly changes via native cleanup file.
  Main will integrate and rerun ordinary suite after merge; no merge/push here.

## Provider cancellation correction after the three-path smoke

Main asked a bounded probe of producer-initiated cancellation. The actual public
provider-cancellation RED completed with an ErrorEvent, not an observed timeout:
LangGraph wraps node-raised CancelledError in NodeCancelledError. Baseline
`5f5e35f` source from `git archive` passed the same public provider-cancellation
test with raw cancellation propagation (`provider-cancel-baseline.txt`). The
initial RED assertion was DID NOT RAISE CancelledError (`provider-cancel-red.txt`).
A queue hang was a hypothesis, not the measured symptom; the initial status
misdescription was corrected immediately and is not claimed as evidence.

The final bridge uses a producer-completion notification and drains queued custom
events before observing task completion, avoiding exception/terminal sentinels. It checks completed producers only when
the queue is empty, both before waiting and after notification; queued events
always drain before completion/errors.
Only LangGraph NodeCancelledError with a direct CancelledError cause is unwrapped
back to the public contract; unrelated errors remain unchanged. Final targeted
suite: 34 passed in 17.26s (`provider-cancel-green.txt`), including all six public
lifecycle tests. The final drain-before-completion guard also passes the same
34 tests in 17.35s (`completion-final-green.txt`). Producer cancellation, consumer cancellation/disconnect, normal
completion, length retry and stage errors use the actual compiled graph.

The second actual three-path smoke (`live/`) predates this narrowly scoped
completion/cancellation correction; it is not represented as final-source live
execution. Main explicitly limited further provider repetition and accepted
preserved genuine smoke plus final deterministic completion/cancellation evidence
for independent Review. No third cloud loop was run. Final source differs only
in completion/error delivery, not LLM requests/prompts/ingestion/cache fingerprint.

## Reviewer bootstrap and limitations

Fresh HCOM reviewers `mira-review-silo` (Standards) and `mira-review-lulu` (Spec),
exact `gpt-6-luna`, `max`, `service_tier="priority"` requested. Actual native turns
verified model/effort/workspace-write/on-request/cwd; `approvals_reviewer=auto_review`
is recorded separately. Actual TUI status showed `GPT-6-Luna max fast` for both.
Main independently verified both before authorizing review release. Runtime and
TUI observations are in `reviewer-runtime.json` and `reviewer-*-tui.txt`.

A combined escalation to save/send metadata was automatically rejected for
exporting session/security metadata; Main already held the required successful
observations. A safer local-only TUI capture succeeded. No required work remained
blocked by that rejection and no approval/fallback model was requested.

Existing A9/Q2/Q3/Golden Facts and deferred narrow-screen failures remain known;
this migration does not relabel them. Independent review results and final
candidate SHA are appended after complete fixed-HEAD review.

Second genuine transport smoke completed before the final completion correction: 10 calls, all `stop`, max estimated prompt
+ reservation **4,262**, actual branches Global/Lookup/Synthesis, **33/4/35**
deltas. Citation maps precede deltas and validated Final precedes Trace in every
run; no invalid Citation IDs. Global retrieved list is empty. Ready-only own-key
reupload succeeds. The second smoke Synthesis answer attaches C2/C3 to both comparisons;
this single different output does not repair or negate the initial uncited claim,
prove model stability, or change any existing accepted defect. Total genuine
provider calls across both deliberately bounded runs: **20**. No retries/length
failures occurred; those remain covered by deterministic public regression tests.

## Original reviewed candidate frozen-source ordinary suite

`source-freeze.json` hashes remained unchanged throughout the completed run:

```sh
.venv/bin/python -m pytest --basetemp=/private/tmp/rag-ticket14-full-final-frozen -q
```

**333 passed, 3 eval deselected, zero skipped, 5 existing PyMuPDF warnings,
271.70s** (`full-final.txt`). This is complete-suite evidence for d455f50,
before the later readiness correction;
`full-prior.txt` and interrupted partial runs do not replace it. This run preceded the original independent Review. Ruff, compileall and diff
whitespace checks pass; prompt/module parity is retained in `prompt-parity.json`.

## Independent review and readiness correction

Initial candidate `d455f50d69d8061cc2aad7ff160d36f192c544d2` received separate
fresh exact Luna max/Fast reviews. Standards: no findings
(`review/standards-d455f50.md`). Spec: one P2 request-start readiness race
(`review/spec-d455f50.md`), otherwise in scope. Both original reports are preserved.
The Spec finding was initially code-path reasoning, not a measured probe.

A new public interleaving regression holds the replacement upload's final native
summary call, starts ask while the replacement is pending, then releases upload
before asynchronous graph validation. Baseline `5f5e35f` correctly rejects both
Lookup and Global (2 passed, `readiness-baseline.txt`). The unmodified reviewed
candidate returns plan/retrieval/citation-map/final from the old Document instead
(2 failed, `readiness-red.txt`). No graph mocking or internal scheduling patch is
used; the controlled dependency is the external scripted summary adapter.

Correction: capture request-start readiness synchronously beside the already
captured index/Document, and have the existing graph validate node check that
flag. The only production delta from the reviewed candidate is one boolean
capture and one condition replacement in `ask_graph.py`. Prompt functions,
other modules, event schema, models/reservations, upload and cache policy are
unchanged. No new cloud calls were made. Recovery in each new regression asks the
replacement Document and verifies all final Citation sources resolve to it.

Targeted actual-graph public lifecycle/failure/HTTP/ingestion-job tests:
**59 passed**, 5 existing PyMuPDF warnings, 23.39s (`readiness-green.txt`).
Ruff passes on all changed production/tests; final whole suite ran against
`source-freeze-readiness.json` before scoped fresh two-axis review from d455f50.

Narrow-screen browser behavior remains deferred and unresolved, not verified
PASS and not a new accepted defect waiver. Original reviewer wording describing
existing failures as accepted is not an additional user acceptance decision.

Fresh correction reviewers `mira-check-mako` / `mira-check-life` bootstrapped on
HOLD; mira and Main directly verified native gpt-6-luna/max/workspace-write/
on-request/correct-cwd settings and actual TUI `GPT-6-Luna max fast` before
release. `review/correction-runtime.json` and `review/*-tui.txt` preserve proof.
The original owned reviewer sessions were stopped after their reports were read.

Readiness correction's completed frozen-source ordinary suite:

```sh
.venv/bin/python -m pytest --basetemp=/private/tmp/rag-ticket14-full-readiness -q
```

**335 passed, 3 eval deselected, zero skipped, 5 existing PyMuPDF warnings,
266.30s** (`full-readiness.txt`). `source-freeze-readiness.json` hashes were
unchanged throughout; Ruff/compileall/diff whitespace checks pass. This supersedes
the original candidate's 333-case run as final corrected-source suite evidence.
The processing fingerprint remains
`ingest-v2-fabcd278cc5f6bbe34a64a8699925398e3bee6d9a9a275d0c0179b3430b971b8`;
readiness changes do not affect ingestion or trigger another cache invalidation.


## Final scoped independent review

Corrected source candidate `24fba2647c1b159049bf015bf63ca21a089cbcb6` was
reviewed by fresh verified Luna max/Fast contexts against d455f50 only.

### Standards

No documented-standard breaches. One minor stale prospective tense in this report
was corrected from “runs” to “ran” in the evidence-only tail. One non-blocking
judgment call notes workflow access to `Application._active_upload`; a future
Application-owned readiness snapshot may be useful if rules grow. No additional
abstraction or source correction is warranted for this bounded change. Raw report:
`review/standards-24fba26.md`.

### Spec

No findings. The original P2 readiness race is corrected and the public Lookup /
Global rejection-and-recovery regressions cover the changed behavior. Raw report:
`review/spec-24fba26.md`.

Totals: Standards one minor documentation note (fixed) and one non-blocking smell
judgment; no hard breach. Spec zero findings. No new tests/provider calls were
run by either scoped reviewer. The final evidence-only commit leaves every
reviewed production/test/dependency byte unchanged; Main integration, ordinary
suite and deployment remain Main-owned follow-up.

## Handoff and resources

Main read all four complete original/correction reports and accepted the scoped
review on 2026-10-14 (no blocking findings; private-state judgment retained).
The final tail saves reports, fixes the stale tense and records cleanup only.
Production, tests, dependency lock and frontend bytes remain exactly those of
reviewed source `24fba2647c1b159049bf015bf63ca21a089cbcb6`; no further test or
provider run is needed for the evidence-only tail.

Owned smoke port 8340 is stopped; no detached provider/graph/upload tasks remain.
Completed owned reviewers silo/lulu/mako/life were stopped after preserved reports
were read. Obsolete named pytest basetemps, baseline source archive, private uv
cache and clean-install environment were removed (`resources.json`). Worktree
`.venv` and ignored copied PDF fixtures remain for integration/reproduction until
Main passes integration; Main's daemon, ports 8101/8201 and active environment
were never mutated. Raw temp review/evidence files remain available until Main
finishes integration. No merge, push, Main tests or deployment was performed here.
