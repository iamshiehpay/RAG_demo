# Issue05 independent integration Code Review — frozen `0663db0`

**Verdict: CHANGES_REQUESTED for the reviewed candidate.** This report reviews the full `d371b79e000a63cec14ac26b4aecc63ea25af8dc...0663db096056c985f9e414509ee16efd32f67a31` diff on `lat/05-summary-tree-global`, not merely its last fix. Its blocking deterministic defect is the oversized Section splitter crossing complete Table Chunk boundaries. A later correction at `ca66429077c4cb1be770f177a10b3c4450462e2c` exists but is **not reviewed here**; the LAT handoff assigns its diff since `0663db0` to a fresh independent Reviewer. No source or tests were edited by this Reviewer.

## Runtime, fixed point and method

- Reviewer `nova-r05sol-zero`, Codex session `01a13305-1d9b-77a2-ac89-6e579549025b`: actual latest `turn_context` was `gpt-6-sol`, `high`, `workspace-write`, `on-request` (`approvals_reviewer=auto_review`). Working directory was the Issue05 worktree. `git merge-base d371b79 0663db0` is exactly `d371b79`; the seven issue commits appear in `git log d371b79..0663db0 --oneline`.
- `/code-review` Standards and Spec axes were independent. Native inherited child contexts unexpectedly changed to **medium** effort (Standards `01a13306-fcde-78d3-9e01-89bed9e85385`, Spec `01a13307-141a-7273-9373-6f25976cd6b7`) and stopped before review; their outputs were excluded. Explicit `gpt-6-sol/high` replacements verified actual `workspace-write/on-request`: Standards `/root/standards_high` session `01a13308-554f-7270-af55-3c819153be08`; Spec `/root/spec_high` session `01a13308-7be8-70d3-9ee5-6f9d72825c9d`. I independently inspected implementation, tests, logs and live report and ran the probes below.
- Binding sources: `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `.scratch/chat-with-document/PRD.md`, `issues/05-summary-tree-global.md` including L2 Comment, `test-list.md`, `EXECUTION.md`, shared `.lat/decisions/D01–D04`, historical `.lat/briefs/nova-r05-review.md`. Historical Opus findings/checks are identified as historical, not credited as my verification.
- The tested source revision `aa5085918a8ff24fab22fc4c0ec845e6f83128da` and reviewed `0663db0` had no diff under `src/ tests/ frontend/ scripts/ eval/golden_facts.py pyproject.toml uv.lock` (direct `git diff` was empty). Implementer's `post-issue03/rebase-equivalence.json` independently records 83 source/test/frontend/script/eval-config files byte-identical through the rebase. The worktree was clean at `0663db0` during review.

## Standards

1. **Low, documented behavior mismatch — README.** `README.md:3` describes only `[C#]` Citations although Global now uses `[S#]`; `README.md:36` omits `摘要 n/N` from the shipped upload progression; `README.md:44` still calls Summary Tree a later ticket. `AGENTS.md` §上傳處理與快取 and Issue05 `What to build` require the summary stage and overview. Update these lines to describe the integrated behavior. This is a real reader-facing documentation inconsistency. **One documented Standards finding.**
2. **Low judgment call — test coupling.** `tests/integration/test_summary_corrections.py:232–266` imports private `_pipeline_version` and checks its digest rather than only public upload/replay behavior; several tests import `summary_pdf` from sibling `test_summary_tree.py`. The PRD §Testing Decisions asks that tests assert upload/ask events and Documents to avoid internal coupling. The test also exercises public operations, so this is a maintainability concern, not a hard breach or a blocker. Prefer a shared fixture and public cache-replay assertion when touching these tests. **One heuristic observation.**

The repo's documented rules override Fowler smell heuristics; no other clear Standards issue was found. Ruff/format matters were left to tooling.

## Spec

1. **High, blocking — oversized Section split destroys Table Chunk context.** `src/chat_document/summary_tree.py:89–112` joins all original Chunk text and calls `split_text(evidence, capacity)`, which cuts at arbitrary character positions. This bypasses the complete Table Chunk and repeated-header rule in `AGENTS.md` §切塊規則 4, and weakens its requirement that numerical claims retain meaningful headers and baselines. My guarded builder probe used one Section with 12 legal Table Chunks of 1,460–1,700 tokens, each containing its caption and headers. At the actual 8,311-token Section evidence capacity, three partial `section_summary` requests were sent. Request 2 began mid-row with ` variant 511.2%.`; request 3 began mid-cell with `1%, variant 1019.2%.` and had **no Table caption/header anywhere**. The original Chunks were complete; it is the Issue05 Section Summary packing that loses context. The first two requests remained 9,936/10,000 including reservation, proving the budget guard cannot detect the semantic loss. Sari independently reproduced the same class through public upload of a 12-page, one-Section PDF using real bge-m3, guarded ScriptedLLM and 12 Table Chunks, and preserved RED evidence. Preserve complete Chunk/Table boundaries in each Section summary batch, with repeated context if a legal Chunk ever needs splitting; keep all Chunk IDs and guard limits. This is a deterministic current-source defect, not a stochastic answer failure.

**Acceptance and remaining quality evidence, separately from the blocking source defect:** The committed fresh AC6 report `eval/reports/summary-tree-global-integrated-q1.md` is honestly **FAIL**: Q1 5/8 and Chinese three-sentence 7/10, with Global routing, Chinese language and exact three-sentence format passing. All 49 Cloud calls ended `stop`; maximum estimated prompt plus output reservation was 8,394/10,000. English motivation/dual-level/experiments failures are nonverbatim Judge excerpts; Chinese graph-indexing/dual-level/conclusion claims are not asserted. The finalized Chinese answer at report line 210 asserts higher win rates across all four domains and four dimensions against every named baseline including GraphRAG, contradicted by Mix Overall GraphRAG 50.4% versus LightRAG 49.6% (`AGENTS.md` Golden Facts). The report's Q1 `not_all_best` forbidden row nevertheless passed; Q1's fact is narrower than Q2's explicit `not_all_datasets`. The report lacks generated summary text, so the source of this answer claim cannot be localized to upload summaries versus answer generation. Its Section requests were all far below the oversized split cap (maximum estimated prompt 2,303), so finding 1 **cannot explain that live claim**. Issue05 AC6 asks for an honest report; all-Golden-Facts N=3 semantic/evaluator reliability remains the explicit Issue11 gate. Raw evidence was handed directly to `nova-i11-meme`; do not relax facts/checkers or fit prompts to LightRAG.

**Nonblocking observation:** `_group_inputs` packs against up to 6,000 tokens while conservative upload answer capacity is 4,242. A Section level between these bounds can become one compressed Group; the live LightRAG report indeed records one Group call. This may lose useful detail compared with multiple smaller Groups, but Global still chooses the most detailed *available* complete level that fits. Prior reviewer R-L1 and Main assigned this quality/tuning question to Issues10/11; no present deterministic violation was established. Historical P1 (generic uncertain-table warning lacks exact table identity) is low UI precision, not loss of the required warning. Historical P2 (some ask tests filter `ask_calls`) is test hygiene; current ask does not build summaries, and full-call cache replay assertions exist.

**Spec finding count:** one blocking deterministic Issue05 source defect; one observed live semantic quality failure with evaluator coverage gap carried to Issue11; one nonblocking Group-detail observation. No clear scope creep.

## Actual implementation path inventory and regression risks

| Path / trigger | Integrated execution and expected visible result | Evidence or risk |
|---|---|---|
| HTTP upload and cache hit | `api.py` POST → `Application.start_upload` (`application.py:89`) → background `_run_upload` → `_process_document` (`:157`). Cache hit at `:165–176` restores Document/embeddings/Tree and emits `ready` directly. | `ProcessingCache.load` rejects missing trees/invalid vectors (`cache.py:67–92`). My replay used zero model calls. |
| Cache miss and build | Parse → Section-aware Chunking → batches of eight bge-m3 embeddings (`application.py:177–197`) → `SummaryTreeBuilder.build` (`:198–203`) → atomic cache write → complete/ready (`:204–215`). | Table-only Sections must enter; heading-only parents must not. Failure/cancel must retain prior Document and no partial cache. |
| Section summaries | `summary_tree.py:178–231`: filter by actual Chunk presence; semaphore default 4; original Section text sets 15%, 80–500 target; all original Chunk IDs retained; `as_completed` progress, sibling cancellation. Oversized Section route `:89–137` splits/merges via guarded calls. | The reviewed version's arbitrary split is the blocking defect. All Section, merge, Group and Document calls share `LLMGateway` budget guard. |
| Group/Document summaries | `summary_tree.py:232–270`: if Section context exceeds upload capacity, adjacent Groups build recursively; dynamic `n/N` adds Group work, then Document Summary. Source IDs/Section titles/page ranges/Chunk IDs flow through each level. | Model omission of `結構未能可靠重建` is caught by deterministic warning carry at `_generate:73–81`; Group packing detail is followup. |
| Global ask | `application.py:284–299` Router first, then Global branches **before** query embedding/retrieve/pack. `summary_context.py:41–73` checks the full answer prompt for each level in order section→groups→document, selecting deepest fitting complete level. It emits empty `RetrievalEvent` with zero drops and an `[S#]` citation map before answer. | Own mixed PDF ask confirmed empty retrieval, S1 source p.2, `trace.summary_level=section` and zero drops. The 1,000-token question boundary and short-question branch have guarded regression coverage. |
| Lookup/Synthesis ask | `application.py:300–315` keeps integrated `RetrievalEvent.chunks` and `dropped_chunk_count`, sorts original Chunk order, maps `[C#]`, and uses ContextPacker (including table links/neighbors and fact extraction). | Explicit `sources="summary"` only for Global (`:317–324`); `[S1]` in raw Chunk cannot change citation mode. Shared #02/#03 tests are in full suite. |
| Answer, source, Trace and UI | `answer_generator.py` builds generic source-aware prompt, medium answer with low retry on length; `application.py:337–352` validates citations and emits final/trace. `Application.source` (`:241–255`) resolves all Section, Group, Document summaries or original Chunks; API 404 otherwise. `frontend/src/App.tsx` keeps overview visible and renders summary Section/page range, `Shared.tsx` progress, `Trace.tsx` level/drop fields, generated `events.ts` and committed `dist/`. | Actual browser UI acceptance belongs to independent QA05; static source/display/type/build evidence is available. |

## Verification and limits

- **My independent public success-path probe:** Real PyMuPDF three-page PDF: heading-only parent; uncertain table-only child (missing cell); text Section. `Application.upload_document` used real local `bge-m3`, `SummaryScriptedLLM` and real guarded gateway with a temporary disk cache. It produced exactly two Section Summaries covering both Chunk IDs; only the table summary carried `結構未能可靠重建`; summary progress ran 0/3 through 3/3; max upload estimated+reservation was 2,977/10K. New Application replay emitted only `ready`, with **zero LLM calls**. Global ask on replay emitted plan→empty retrieval→citation map→delta→final→trace, only Router+Answer calls, S1 resolving to p.2 and warning-bearing source; max ask budget 3,763/10K. This is an independent acceptance-path probe, not browser QA.
- **My adversarial edge supplement:** The 12-Table-Chunk synthetic `SummaryTreeBuilder.build` repro above used the real guard and ScriptedLLM, without bge-m3 because it targets the exact prompt-packing boundary. The construction and observed prefixes are reproduced below; this is not substituted for the public success-path probe.
Reproduction shape at `0663db0` (run from worktree root with `PYTHONPATH=src:. .venv/bin/python`):

```python
import asyncio
from chat_document.models import Section, Chunk, Document
from chat_document.summary_tree import SummaryTreeBuilder
from chat_document.llm_gateway import LLMGateway
from chat_document.llm_adapter import ScriptedLLM
from chat_document.tokens import count_tokens

chunks = []
for t in range(12):
    body = (f"Table {t+1}: Accuracy by group. Columns: dataset, baseline win rate, variant win rate.\n"
            + "".join(f"Group {i}: baseline {i}.1%, variant {i}.2%.\n"
                      for i in range(t * 90, (t + 1) * 90)))
    assert count_tokens(body) < 2000
    chunks.append(Chunk(id=f"c{t}", section_id="s", section="7 Experimental data",
                        page_start=1, page_end=1, text=body, order=t, kind="table"))
doc = Document(id="d", name="probe.pdf",
               sections=[Section(id="s", title="7 Experimental data", page_start=1,
                                 page_end=1, paragraphs=[])], chunks=chunks)
llm = ScriptedLLM(["partial 1", "partial 2", "partial 3", "section", "overview"])
async def run():
    _ = [item async for item in SummaryTreeBuilder(LLMGateway(llm)).build(doc)]
    partials = [c for c in llm.calls if c.call_type == "section_summary"][:3]
    for call in partials:
        print(call.messages[-1]["content"][:160],
              call.estimated_prompt_tokens + call.num_predict)
asyncio.run(run())
```

At the old head, partial 2 begins `Document evidence:\nSection: 7 Experimental data\n variant 511.2%.`; partial 3 begins `...\n1%, variant 1019.2%.` and contains no `Table n:` header. The first two guarded requests each total 9,936/10,000.

- **Valid implementer artifacts, inspected rather than rerun:** `docs/verification/ticket-05/post-issue03/full-regression.txt` records 264 passed / 2 eval deselected (251.68s); `summary-integration.txt` 15 passed; `table-caveat-green.txt` 2 passed. `ruff.txt`, `format-check.txt`, `event-parity.txt`, `typecheck.txt`, `build.txt`, `source-display.txt` pass. I checked `git diff aa50859 0663db0 -- src tests frontend scripts eval/golden_facts.py pyproject.toml uv.lock` was empty; thus these logs apply to reviewed source. I did not duplicate a four-minute suite merely for docs-only rebase. `git diff --check d371b79...0663db0 -- src tests frontend scripts eval/golden_facts.py README.md` was clean; preserved raw eval/test logs contain trailing whitespace and were not reformatted.
- **Not verified here:** Real browser UI acceptance (QA05); Issue11 N=3 all-Golden-Facts result and second long non-RAG Document; effectiveness of the later table-boundary correction at `ca66429`. I opened no server/port and made no source, test, frontend, evaluator, issue or dependency edits.

**Two-axis summary:** Standards: one low documentation mismatch plus one low heuristic test-coupling note. Spec: one high blocking table-boundary defect in this exact candidate; quality/evaluator failure and Group-detail concern are recorded with their assigned gates. The later correction requires a fresh Reviewer comparing `0663db0...ca66429` under the updated LAT rule.
