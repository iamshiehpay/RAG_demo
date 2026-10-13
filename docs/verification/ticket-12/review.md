# Ticket #12 review record

- Spec: D11 (chat layout redesign). Process: D12 (levi implements, nova merges). Reviewer model: D13 (user accepted Opus 5.5).
- Candidate: branch `lat/12-chat-layout`, rebased onto main `b956247`. Head `35b7eb8`.
  - The tree for `frontend/` and `docs/verification/ticket-12/` is identical to the reviewed head `1c274e4`, checked with `git diff 1c274e4 35b7eb8` (empty).
  - The rebase only moved the base over the docs-only commit `b956247`.
- Scope: frontend and evidence only. No changes under `src/`, `tests/`, `scripts/` or `frontend/src/events.ts`.

## Runtime (from the subagents' API response metadata)

| Role | Model actually used | Spawn parameters | Transcript locator |
|---|---|---|---|
| Implementer, initial build and fixes (same agent, resumed) | `claude-sonnet-5-5` (207 responses) | `model: sonnet`, `effort: high`, `subagent_type: general-purpose` | Parent Claude Code session `206d3598-8358-4a3e-98df-6b18252ec1a4` (levi), task output `a7d6809ed4e6be36c.output` |
| Reviewer 1 (full, two axes) | `claude-opus-5-5` (63 responses) | `model: opus`, `subagent_type: general-purpose` | Same parent, `a3d8ffd9534c848da.output` |
| Reviewer 2 (scoped re-review, fresh context) | `claude-opus-5-5` (46 responses) | `model: opus`, `subagent_type: general-purpose` | Same parent, `a00a5c51be5b10d52.output` |

- Task outputs live under `/private/tmp/claude-501/-Users-shiehpay-Desktop-resume-rag/206d3598-8358-4a3e-98df-6b18252ec1a4/tasks/`. They are temporary files and are not committed.
- The user's later conversation continued in transcript `b9ac5768-6334-4812-bb21-2905b25bf430`.
- **Effort:** the transcript does not echo effort. The only evidence for `high` is the spawn parameter.
- **Permissions:** subagents inherit levi's session permission mode. Their briefs added three limits:
  - work only inside the worktree;
  - use ports 8121 (implementer) and 8122 (reviewers); never touch 8101;
  - make no commits outside `lat/12-chat-layout`.
  The reviewers were also read-only.

## Review 1: full review of `d7fd1d7`

**Verdict:** Spec CHANGES REQUESTED; Standards CHANGES REQUESTED.

| # | Severity | Finding | Location (pre-fix) |
|---|---|---|---|
| 1 | Major | Cells in answer tables inherited `overflow-wrap: anywhere`, and the table was squeezed to its `min-width`. Numbers split across lines; `11.1` became `11`/`.1` at 920 and 390. | `styles.css:95,109` |
| 2 | Medium | Narrow overlays had four problems: (a) focus stayed under the overlay and Escape did not close it; (b) both overlays could be open at once; (c) a citation click permanently set `rightPref`, so after a wide→narrow resize the overlay covered the conversation. | `App.tsx:62-63,179`; `styles.css:213-215` |
| 3 | Medium | The native file input showed English "Choose File / No file chosen". | `DocumentPane.tsx:17-19` |
| 4 | Medium | A repeated `call_type` was labelled （重試）. Batched `fact_extraction` calls were therefore mislabelled as retries. | `AnswerProcess.tsx:97-99,118` |
| 5 | Low | Source-pane tables scrolled but showed no affordance: the caption sat inside the scroll box, and macOS hides scrollbars. | `SourceContent.tsx:12-14`; `styles.css:191-196` |
| 6 | Low | Not blocking: the backend "System extraction warning" appears in the overview. This is backend content, left for a follow-up. | `summary_selection.py:102`, `summary_tree.py:119` |
| 7 | Low | `role="log"` announced streamed text; UnverifiedMark mixed Chinese and English; the reserved-output bar contrast was 1.86:1. | `App.tsx:224` etc. |

**Verified in the browser** (server on port 8122, real cached Document and real `/api/sources`, scripted `/api/ask`):
- uncertain-table note (`chunk-25`)
- 404 text
- 暫定 label and the disabled-ask reason
- scroll stays pinned to the newest message
- dist identical to a temp rebuild
- typecheck, test:source and check:events pass
- pytest: 6 passed
- no external fonts, CDN or animation
- no page-level horizontal overflow at 1440, 920 and 390
- text contrast 5.8–8.0:1

**Verified by reading code only:** upload reconnect, rejected / error / retry, 重新產生中, Unverified, clearing on replacement, `[S#]` sources.

## Fixes: `dbde97f` and `1c274e4` (rebased as `7a5ea24` and `35b7eb8`)

All six findings were addressed. Finding 6 (the backend warning) is out of scope and remains a known limitation.

## Review 2: scoped re-review of `d7fd1d7..1c274e4`, fresh reviewer

**Verdict:** APPROVE. All six findings FIXED, no blocking regression.

| # | Evidence |
|---|---|
| 1 | At 390 the widetable box is 356 px with 984 px of content; 0 of 27 decimal cells wrap; page scrollWidth equals the viewport. At 920 with both panes open, 0 cells split. |
| 2 | At 390 a citation moves focus to `.source-heading`. Escape closes the overlay and returns focus to the citation. Overlays are mutually exclusive. A narrow citation click saved no wide preference. Opening the source wide and resizing to 390 leaves no overlay. |
| 3 | The upload control reads 選擇 PDF / 尚未選擇檔案, then the filename while uploading, then 換一份文件. The input is focusable with accessible name 選擇 PDF and shows a 2 px outline. No "Choose File" text appears. |
| 4 | Steps read 判斷問題類型, 找相關段落, 分批抽取事實 第 1 批, 第 2 批, 產生回答. Retry appears as 產生回答（重試）. |
| 5 | The caption and meaning sit outside the scroll box. The hint shows only when the table overflows (321 vs 910 px at 390). |
| 6 | Unverified mark reads 未驗證; no `role=log`; reserved-output bar contrast 3.29:1. |

**Checks run in this review:**
- typecheck and test:source pass
- temp `vite build` matches the committed dist by hash
- pytest (`test_http` + `test_event_types`): 6 passed
- `checks.js`: 36/36 runs across 12 scenarios at 1440, 920 and 390

**Non-blocking notes:**
- Escape returns focus to the last citation even when the overlay was opened from the header (`App.tsx:152,213`).
- The ScrollBox ResizeObserver is re-created on every render (`SourceContent.tsx:19`).
- A stale overlay may show for one frame on resize (`App.tsx:141`).
- Focus return after a mouse click is untested in Safari.

**Not verified in review 2:**
- real LLM answers (scripted fixtures only)
- opening the native file dialog from the keyboard
- Safari, Firefox and screen readers

## Implementation path coverage

| Entry point / path | Branches and recovery | Evidence |
|---|---|---|
| Upload (`DocumentPane` → `App.upload` → upload SSE) | Progress stages; cache hit goes straight to ready; error; reconnect after the progress stream drops; replacing a document clears the conversation; ask disabled while busy | Real cached upload on 8121 in both rounds; scripted error scenario; reconnect, replace and clear verified by code read only |
| Ask (`Composer` → `App.ask` → ask SSE) | Enter / Shift+Enter / IME guard; plan → retrieval → thinking → delta (暫定) → final; rejected; error with retry button; length retry (重新產生中) | Real compare (twice) and summary (once) on 8121; scripted provisional, retry, error and fallback scenarios; IME tested with synthetic `isComposing` and keyCode 229 only |
| Citations (`Answer` → `showSource` → `SourcePane`) | `[C#]` chunk or table, `[S#]` Section/Group/Document summary; loading, error and 404; wide pane vs narrow overlay; focus and Escape | Real C2 table and S1 summary; scripted missing-source (404); review 2 focus measurements |
| 回答過程 (`AnswerProcess`) | Lookup, Synthesis and Global summary lines; fallback reason; one row per call with model and think level; batch labels; retry label; retrieval row hidden for Global; 技術細節 collapsed | Real compare and global runs; scripted compare (two batches), error (answer retry) and fallback |
| Layout | Wide three columns; 56 px collapsed rails; 920; narrow overlays; resize across the breakpoint | `checks.js` at 1440, 920 and 390; review 2 resize tests |

## Resources (owned by levi's #12 work)

- Worktree `.worktrees/12-chat-layout` contains copied `.cache/` and `data/*.pdf`, plus a `.venv/` created by `uv run` (all gitignored). Remove the worktree after merge.
- Temp PDF copies under `/tmp` were used for agent-browser uploads.
- Servers on 8121 and 8122 are stopped. 8101 (the user's) was never touched.
- The mockup lives in `.lat/layout-mockup/` (ignored).
