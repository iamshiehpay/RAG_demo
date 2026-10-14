# Issue05 integration verification after Issue02/03

## Candidate and binding scope

Main assigned integration at HCOM #7699, initial source base `5d6204cf78e3fe166abfc7bf719c1d0cf8118189`. Main docs-only checkpoints `ca8a02c` and `d371b79e000a63cec14ac26b4aecc63ea25af8dc` preserve source/test/frontend/scripts/eval/lock bytes. Final ancestry base is `d371b79`; Main owns its issue Comments. No merge, push, issue-comment edits, new agents, or self-review was performed.

Initial independent reviewer: `nova-r05-guru`. D04/HCOM #8242 changes final review to an independent Codex gpt-6-sol/high peer; Main will assign its name. No new review task was sent to the old reviewer after that steering. This report records implementation tests; it does not replace independent review or integrated QA.

The conservative upload capacity is authorized in the actual main Issue05 Comments and HCOM #6150/#7699. At the integrated prompt it computes to **4,242 tokens**, from the existing 6,700 answer-prompt cap, both 1,000-token question reservations, summary/language/table prompt overhead, join allowance and 6,000 evidence ceiling. Original Section Summaries remain selectable for short questions. No tree construction or truncation is introduced during ask.

## Integration behavior

- Main parser and table reconstruction modules are unchanged. Table-only Sections enter Summary Tree input even with no paragraphs; all original Chunk IDs and Section/page provenance are retained. Heading-only Sections stay excluded.
- Global branches before ContextPacker/query embedding. Empty RetrievalEvent defaults to zero drops; final Trace includes both summary_level and dropped_chunk_count. Lookup/Synthesis consume the integrated RetrievalEvent, preserve actual linked/neighbor scores and budget-drop fields. The shared asking/upload lifecycle remains intact.
- Shared answer prompt retains the integrated comparison-baseline, reference-row, same-dataset/metric, exceptions and uncertain-table rules. Explicit summary/chunk source choice and generic whole-document instruction remain from the approved corrections.
- Summary generation now preserves the exact uncertain-table warning when any supplied evidence carries it, even if the model omits it. The deterministic note passes through Section split/merge, Group and Document outputs, cache, S-source text and answer evidence. It does not reconstruct missing table cells or replace raw Table sources. The note is added after generation; subsequent prompts count its tokens normally through the unchanged guard.
- Main SourceContent still renders typed Table Chunks, including raw uncertain tables; Summary sources display text and covered Section/page metadata. Both summary-level and budget-drop Trace fields are retained. Generated frontend bundle was rebuilt.
- Cache fingerprint preserves main tables.py/embedder.py and all prior parser/chunker/token/model dependencies, plus summary modules, gateway, adapter, policy and answer prompt. Full Tree/typed Table metadata survives replay. Replay performs zero LLM calls.
- Existing #03 successful uploads use the shared explicit upload-summary fixture dispatch. Failed/early-exit ingestion assertions still inspect complete llm.calls. The new combined-source regression checks exact total Section/Group/Document calls and zero-call cache replay.

## New regression evidence

`test_table_only_sections_keep_all_sources_caveat_and_global_cache[1|18]` exercises real PyMuPDF input and local bge-m3 through Application.upload_document, disk cache replay, source and Global ask. Every page is a table-only Section with a deliberately missing cell. The 18-Section case builds Group evidence. It asserts full Chunk provenance, warning survival in every layer/overview, resolvable original Table Chunks, source text, cache equality, exact all-call counts, zero cache calls, no Global retrieval and both zero-drop fields.

Before the correction the regression fails because Section Summary omits `結構未能可靠重建` (`table-caveat-red.txt`). Final combined regression: **2 passed**, 6.50s (`table-caveat-green.txt`). Summary integration/corrections suite: **15 passed**, 55.78s (`summary-integration.txt`). All successful acceptance paths here use real bge-m3 with ScriptedLLM and real guarded requests, rather than a live answer-quality claim.

Earlier cancellation evidence wording is corrected in the original correction report, test docstring and AI log: sibling failure/cancellation uses real bge-m3. Only the exceptionally large 32-page recursive and pathological-provider probes use fixed fake embedding vectors.

An initial full run loaded the Global import before it was corrected; it was interrupted with 188 pass/4 missing-import failures and retained as `stale-run-interrupted.txt`. This is not final test evidence. A fresh complete run on the source checkpoint follows below.

## Fresh live AC6 evidence

Command (once): `UV_CACHE_DIR=/private/tmp/nova-i05-uv-cache uv run --no-sync pytest -q -m eval eval/test_live.py --eval-cases Q1,Q1_ZH_THREE_SENTENCES --eval-label summary-tree-global-integrated --eval-report eval/reports/summary-tree-global-integrated-q1.md`.

Source checkpoint: `aa5085918a8ff24fab22fc4c0ec845e6f83128da`; the report truthfully records uncommitted changes because test logs/report artifacts were being created. Source/tests/frontend were committed and not edited during the run. Raw answer whitespace is preserved. This single-run AC6 report is not the final N=3 #11 quality gate.

**FAIL**, 52.87s (exit 1): Q1 **5/8**, Chinese three-sentence **7/10**. Q1 motivation/dual-level/experiments fail because Judge excerpts are not verbatim. Chinese graph-indexing/dual-level/conclusion fail as required claims not asserted. Both route as Global; Chinese language and exactly three sentences pass. No Golden Facts/checker relaxation or topic fitting was applied. The earlier reports remain historical evidence for their own prompts.

All **49 calls** are retained in the report: 25 Section, 1 Group, 1 Document, 2 Router, 2 Answer, 18 Judge. Every call ends `stop`. Maximum estimated prompt plus output reservation is **8,394/10,000**; maximum provider prompt plus reservation is **8,169/10,000**. No truncation, low retry or budget violation. See raw report and `live-budget-summary.json` for the complete accounting. Quality failures remain open for #10/#11; successful budget/format checks do not establish semantic correctness.

## Remaining handoff item

Reviewer R-L1 is not waived: Group inputs still pack against min(6,000, group-call capacity). A Section layer above conservative answer capacity but below 6,000 can produce one all-Section Group, so a richer intermediate grouping may be possible. Main explicitly assigned assessment against the most-detailed-fitting requirement to #10/#11; no unsolicited packing change was made during this integration.

## Session and resource evidence

hcom list reports sari in the Issue05 worktree, Codex session `01a132cd-e8ef-7441-a8c0-4775d66eea70`. Latest transcript turn_context verifies model **gpt-6.1-sol**, effort **high**, approval_policy **on-request**, sandbox **workspace-write**, network enabled. Runtime permissions specify **approvals_reviewer=auto_review** and writable worktree/hcom/tmp roots. Git metadata and hcom's uv tool cache needed authorized escalations; no automatic-review rejection occurred. Settings were reported to Main/reviewer via hcom.

No service, browser, port, container or extra agent was started for this integration. Only temporary test/evidence directories and bounded test processes were used; the stale runner was stopped explicitly, and all final commands terminate before handoff.

## Final checks

- Full deterministic regression: `UV_CACHE_DIR=/private/tmp/nova-i05-uv-cache uv run --no-sync pytest -q` → **264 passed, 2 eval tests deselected**, 251.68s (`full-regression.txt`).
- Ruff check and format over src/tests/shared scripts (including measure_table_reading.py)/Golden Facts → **PASS**, 53 files formatted (`ruff.txt`, `format-check.txt`).
- Backend/frontend generated event parity → **PASS** (`event-parity.txt`).
- Frontend TypeScript and production build → **PASS** (`typecheck.txt`, `build.txt`); generated bundle retained in the rebased feature checkpoint.
- SourceContent static rendering of reconstructed cells and uncertain raw-source limitation → **PASS** (`source-display.txt`).
- Whitespace/conflict check → **PASS** (`diff-check.txt`).
- Live evaluation → **FAIL** as recorded above; final #11 quality gate remains outstanding.

The final rebase onto Main's docs-only d371b79 preserves all validated source/tests/frontend/script bytes from aa50859. No source tests are repeated solely for that documentation checkpoint. Final SHA, source equivalence and clean status are reported via hcom before independent review.
