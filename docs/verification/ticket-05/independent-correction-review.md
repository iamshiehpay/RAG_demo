# Issue05 correction re-review — frozen `ca66429`

**Verdict: APPROVE** the correction diff `0663db096056c985f9e414509ee16efd32f67a31...ca66429077c4cb1be770f177a10b3c4450462e2c` (three-dot merge-base comparison). Integration base remains `d371b79e000a63cec14ac26b4aecc63ea25af8dc`. The only commit in this range is `ca66429 fix: Preserve complete table chunks in section summary batches`. The worktree was clean at the frozen candidate. This is a correction-only review; the initial full review is history, not this verdict.

## Runtime and independent axes

Main reviewer `nova-r05fix-nano`, HCOM session `01a13317-a4ed-7a20-8d96-93b4dcc78014`: actual `turn_context` has `model=gpt-6-sol`, `effort=high`, `approval_policy=on-request`, `sandbox_policy.type=workspace-write`, `approvals_reviewer=auto_review`. The two independent `/code-review` contexts used explicit `fork_turns=none`, `gpt-6-sol/high`; neither edited source:

- Standards `/root/standards`, thread `01a13318-5ada-7df1-ac3f-baaf9dd78162`, verified its own `turn_context` ordinal 47: `gpt-6-sol/high/on-request/workspace-write`.
- Spec `/root/spec`, thread `01a13318-7756-7192-8369-2c8646e694ff`, verified its own `turn_context`: `gpt-6-sol/high/on-request/workspace-write`.

Read binding `AGENTS.md` including the main repo's uncommitted self-check, `CLAUDE.md`, `CONTEXT.md`, PRD, Issue05 with L2 comment, test-list PA-04, EXECUTION, D01–D04, LAT/hcom-spawn/code-review skills, and implementation evidence. No pending human decision applies. No server, port, browser, source edit, commit, merge or push.

## Standards

**APPROVE — 0 actionable findings.** The Standards context found no documented-rule violation or applicable Fowler smell in the correction. Its review inspected the source, new public-upload regression, README/AI log, and RED/GREEN/full-suite artifacts. The new test exercises actual `Application.upload_document` with PyMuPDF, local bge-m3, and guarded ScriptedLLM rather than duplicating implementation internals. Tooling checks were not treated as code-review findings.

## Spec

**APPROVE — 0 actionable findings.** The Spec context found the original defect closed: the Section builder now passes the ordered original Chunk texts to the existing whole-unit `batches` helper, instead of flattening all text and applying `split_text` at arbitrary character positions. This preserves each legal Table Chunk's caption, headers and rows in one raw Section request. Section merge, summary target, Section title, all original Chunk IDs, and gateway budget guard remain in the path. README now states the implemented summary n/N stage and full-Chunk packing. No scope creep was found.

The frozen candidate's live Q1/Chinese report is **not** reinterpreted as a current semantic pass. Its failed Golden Facts and GraphRAG universal overclaim occurred without oversized Section splitting, and the Q1 fact coverage gap remains with Issue11's final quality/evaluator gate. The earlier nonblocking generic table-warning precision, filtered ask-call test hygiene, and Group-detail concern remain in their existing follow-up ownership. They do not make this correction diff fail.

## Changed and affected path inventory

| Entry / branch | Actual flow and failure or recovery behavior |
|---|---|
| `src/chat_document/summary_tree.py:89–139` | `_section_text` receives ordered complete Chunk strings, computes guarded Section capacity including heading/join allowance, packs whole units, sends each raw batch through `LLMGateway.generate(section_summary)`, then merges partials through guarded Group/Section calls until one Section Summary fits. An individual unit larger than capacity raises before a model call; nonreducing merge raises. No silent source truncation. |
| `src/chat_document/summary_tree.py:180–272` | `build` filters heading-only Sections, computes target from original Section text plus Table Chunk text, processes Sections under a semaphore, retains all Chunk IDs in Section/Group/Document provenance, emits summary n/N, cancels and awaits siblings on failure. Failure in the upload path emits an error and does not publish/cache a partial Document. |
| `src/chat_document/context_packer.py:52–66` | Existing `batches` helper appends complete units in order and raises on an oversized unit. The correction imports this helper; retrieval/fact extraction logic is untouched. |
| `src/chat_document/application.py:157–235` and cache path | Cache miss parses/Chunks/embeds before summary build; only a completed tree reaches cache and `ready`. Cache hit restores the existing tree. Summary failure surfaces as terminal upload error. Summary source fingerprint already includes `summary_tree.py`, invalidating old cache content. |
| `tests/integration/test_summary_table_integration.py:116–156` | New 12-page public upload test constructs a single Section of legal Table Chunks, checks each complete original text appears exactly once among raw Section requests, checks all source IDs and reserved budgets, and verifies ready. |
| `README.md`, `docs/ai-log.md`, `docs/verification/ticket-05/review-integration-corrections/` | User documentation catches up with summary progress/Citation/packing behavior; AI log records the discovered error and separate semantic evidence; artifacts retain RED/GREEN and static/build results. Frontend/eval/Golden Facts source bytes are unchanged. |

## Verification and limits

- Independently reran the exact new public-upload regression: **1 passed in 7.40s**, using the current worktree, actual parser and local bge-m3. Its committed RED evidence on the old head fails specifically because Chunk 8 is absent as a complete Table Chunk; GREEN log reports **27 passed in 77.02s** across the three summary integration files.
- The independent Spec context also reran the new public-upload regression (1 passed, 4.30s) and three focused existing regressions for split/merge title, multiple recursive merge rounds with provenance, and Group/Document progress (3 passed, 24.43s); commands used `PYTHONDONTWRITEBYTECODE=1` and disabled pytest cache writes.
- Independently probed an ordinary synthetic oversized Section through the real `SummaryTreeBuilder` and `LLMGateway` with ScriptedLLM: 38 distinct source Chunks, 27,702 source tokens, four raw Section calls, six calls total. Every original Chunk appeared in exactly one raw request, all 38 IDs remained in Section provenance, and maximum estimated prompt plus reserved output was **9,644/10,000**. This checks non-table batching after the change without starting a service.
- Inspected the same-SHA full deterministic suite artifact: **265 passed, 2 eval deselected, 241.55s**. Ruff/format, event parity, TypeScript typecheck, production build, source-render and diff-check logs pass. `git diff --check` on code/test/README/AI-log changes is clean; `git status --short` is clean. Existing full-suite evidence is reused because no source changed after its frozen SHA.
- No new live Cloud answer-quality or browser UI claim is made by this correction review. Issue11 retains the final N=3 Golden Facts gate; independent QA retains UI acceptance.

**Counts:** Standards 0 findings (worst: none); Spec 0 findings (worst: none). **Final: APPROVE** for this exact frozen correction.
