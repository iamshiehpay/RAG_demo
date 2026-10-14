# Ticket #12 layout update (supersedes the margin-note, Trace and dialog decisions below)

Approved in `.lat/decisions/D11` and `D12`. The interface is now a three-column, collapsible chat view with a Traditional Chinese UI.

- Left column: Document (upload or replace, processing progress, Chunk count, Document Summary). Middle: conversation with the input pinned at the bottom. Right: source text for the clicked Citation (replaces the modal dialog and the margin notes). Side columns collapse to 56px strips; at 900px and below they become overlays opened from the header.
- Questions are right-aligned bubbles; Citations are small buttons inside the sentence (`C#` and `S#`). Markdown tables sit in an `overflow-x: auto` box.
- 回答過程 replaces Trace: one summary line, then three sections (how the question was understood, which model each step used with a 10,000-full token bar, the retrieved passages), then 技術細節（開發用）, closed by default, which holds the raw counters and the model's thinking text.
- Model names are constants in `src/models.ts` (the event contract has no model field); keep them in sync with the backend.
- Enter sends, Shift+Enter inserts a newline, Enter during IME composition never sends.
- Palette, Noto Serif TC at 16px and the no-animation rule are unchanged. `review/checks.js` and `review/scripted-events.js` were rewritten for this structure; `docs/verification/ticket-12/` holds the evidence.

---

# Ticket #09 — first design draft

Status: awaiting user direction approval. This is the Phase 1 checkpoint, not final acceptance.

## Design decisions

The interface reads as research notes with evidence in the margin. It is a visual overhaul of the walking skeleton, retaining its upload/ask endpoints, form fields, generated event types and source lookup. The main audience is the interviewer viewing a screen-share demo on a laptop.

- Recipe: `web-design-engineer` / `tufte-dataink`.
- Design Read dials: visual variance 4 (one asymmetric reading grid), motion 1 (none), density 7 (evidence and Trace), asset dependence 2 (type and data), brand fidelity 5 (new visual vocabulary, retained product contracts).
- Narrative role: upload establishes the Document; the answer is the reading surface; Citations and Trace supply evidence. Laptop viewing requires 16px body text and a distinct 44px title. The temperature is quiet and scholarly.
- Paper `#FBFAF6`, ink `#1B1B1A`, slate `#3E4A5C`, red `#A6300E` for errors and Unverified. Reference rules `#D8D2C2`; lighter slate denotes output reservation.
- Noto Serif TC at 16px/1.8 for reading, serif headings, small sans labels for measurements. No decorative images, shadows, rounded cards, transitions or animation.
- Spacing: 4/8/12/16/24/32/48px. A sticky Document sidebar keeps the overview alongside the conversation. Desktop paragraph/list/table rows have a dedicated Citation margin. At small widths, notes move directly beneath the corresponding text.
- Trace defaults collapsed; each thinking disclosure also defaults collapsed. The token bar directly labels prompt and output reservation and has explicit 0 and 10K endpoint ticks.
- Source uses a native modal dialog, with loading/error states, Escape/Close, and focus returned to the Citation trigger.

The already-confirmed project recipe and Phase 1 assignment authorized building this concrete draft before the human checkpoint. Finalization waits for the user approval relayed by levi and recorded in `.lat/decisions/`.

## Shared components and extension seams

| Component | Current usage | Next-ticket seam |
| --- | --- | --- |
| `Answer` / `MarginCitation` | App answers and Document Summary; `[C#]`/`[S#]`, page range, Section, safe Markdown | #05 supplies actual summary sources; #07 normalizes grouped Citation markers |
| `SourceDialog` | Existing Chunk source lookup; text preserved as supplied | `kind` supports Section Summary/Table Chunk; optional `table` supplies caption, headers and rows for #03 |
| `TokenBar` | Every Trace LLM call, fixed 10,000 scale | Uses generated LLMCallTrace directly |
| `StageIndicator` | Every ask turn | #06 can retain these components while adding rejection handling |
| `UploadProgress` | Current parsing/chunking/embedding stages and numeric progress | #04/#05 extend generated stages for summary progress |
| `ErrorState` | Upload, ask, and source errors; ask Retry | #07 supplies backend retry/error behavior |
| `UnverifiedMark` | Matching final-event sentences and backend inline marks | D01: frontend does not independently flag uncited prose |
| `ThinkingContent` | Trace call thinking or live thinking event fallback | #07 emits streaming thinking; no empty disclosure when absent |

`react-markdown` renders React elements with raw HTML disabled (`skipHtml`), its default URL safety transform retained, and `remark-gfm` supplies tables/lists. Citation text tokens become safe internal links and the custom link renderer turns only mapped IDs into source buttons. No `dangerouslySetInnerHTML` or `rehype-raw` is used. See [react-markdown](https://github.com/remarkjs/react-markdown) and [remark-gfm](https://github.com/remarkjs/remark-gfm).

## Bundled font

Vendored from `@fontsource/noto-serif-tc` 5.3.1, weight 400 normal. The SIL Open Font License is retained at `src/fonts/LICENSE`. Only WOFF2 resources referenced by the Unicode-range CSS are included: 108 subsets, 3,035,932 font bytes. The browser loads ranges on demand; the scripted Chinese Q3 page transferred 500,476 font bytes on its cold first load. The real English Q3 page transferred 440,516 font bytes. Font requests were all from the local origin. No external font stylesheet or font service is used.

The full Traditional Chinese ranges are kept to support arbitrary Document/answer text. No coverage-limiting subset based only on current UI strings is used.

## Browser evidence

Chromium via `agent-browser`, committed production `dist` served by FastAPI at `http://127.0.0.1:8140`. Scripted screenshots deliberately label their Document/summary/source as review fixtures. They demonstrate visual states, not Golden Facts/model quality.

| Evidence | Purpose |
| --- | --- |
| [01-upload.png](evidence/01-upload.png) | Empty upload and disabled question with reason |
| [02-upload-progress.png](evidence/02-upload-progress.png) | Embedding 18/52; question disabled |
| [03-q3-citations.png](evidence/03-q3-citations.png) | Scripted Q3 with paragraph-aligned margin Citations |
| [04-trace-tokens.png](evidence/04-trace-tokens.png) | 5,100/10,000 token bar, 0/10K ticks, metrics, collapsed thinking |
| [05-source-dialog.png](evidence/05-source-dialog.png) | Source text/table content and page/Section |
| [06-provisional.png](evidence/06-provisional.png) | Provisional text and live thinking in Trace |
| [07-retry.png](evidence/07-retry.png) | Cleared provisional answer; 重新產生中 |
| [08-error.png](evidence/08-error.png) | No failed answer retained; error and Retry; two calls |
| [09-unverified.png](evidence/09-unverified.png) | Unverified prose mark and Trace count |
| [10-markdown-safe.png](evidence/10-markdown-safe.png) | Safe emphasis/table; script and javascript URL suppressed |
| [11-laptop-local-fonts.png](evidence/11-laptop-local-fonts.png) | 1280×720, external HTTPS blocked, local fonts remain available |
| [12-mobile.png](evidence/12-mobile.png) | 390×844, notes below text, no page overflow |
| [13-live-q3.png](evidence/13-live-q3.png) | Actual uploaded LightRAG, actual gpt-oss answer/Trace at 1280×720 |
| [14-live-source.png](evidence/14-live-source.png) | Actual Chunk source fetched from #01 source API |
| [15-thinking-expanded.png](evidence/15-thinking-expanded.png) | Thinking disclosure expanded with keyboard |
| [16-near-full-budget.png](evidence/16-near-full-budget.png) | Two calls on the same scale, including 9,990/10,000 |

Browser assertions in `checks.js` passed for desktop (1440×900), laptop (1280×720) and small screen (390×844). They check font family/load/local origin, body size, overflow, animation, Citation layout/buttons, state-specific outcomes, safe Markdown, 10K scale and measured token-bar width ratios. Browser errors/console were empty on scripted acceptance. Live application emitted no page errors. Escape closes the source dialog and restores focus to its Citation trigger. The Retry button successfully resends the same question and receives a new complete answer.

External HTTPS blocking tests internet-independent font loading while localhost remains accessible. They do not claim that a stopped local server can serve the application offline.

## Reproduce scripted acceptance

Start the existing backend on the assigned port, using the rebuilt dist:

```sh
uv run uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8140
```

From the worktree root, in another terminal:

```sh
agent-browser --session t09-review open http://127.0.0.1:8140
agent-browser --session t09-review set viewport 1440 900
agent-browser --session t09-review eval --stdin < frontend/review/scripted-events.js
agent-browser --session t09-review upload '#document' "$(pwd)/data/lightrag.pdf"
agent-browser --session t09-review fill '#question' 'Performance of ablated versions of LightRAG'
agent-browser --session t09-review click 'button[type=submit]'
agent-browser --session t09-review eval --stdin < frontend/review/checks.js
agent-browser --session t09-review screenshot --full /tmp/t09-review.png
agent-browser --session t09-review close
```

Set `window.__t09.scenario` before asking to `provisional`, `retry`, `error`, `unverified` `markdown` or `budget`; default is `q3`. For provisional/retry, `window.__t09.release()` resumes the held SSE stream. Set `uploadHold = true` before uploading to hold Embedding 18/52. Reload/reinject between independent screenshots. The fixture is review tooling only; production does not import it or expose a mock mode.

For live acceptance, omit fixture injection and use the absolute Document path. This invokes the existing real bge-m3/gpt-oss adapters. Stop all started browser/server sessions after review.

## Verification and remaining checkpoint

- `npm run typecheck --prefix frontend`: PASS.
- `npm run build --prefix frontend`: PASS; source/dist synchronized; no missing-font warning.
- `uv run pytest`: PASS, 20 tests, real local bge-m3 with recording scripted LLM; no cloud eval in this suite.
- `uv run ruff check src tests scripts/generate_event_types.py`: PASS.
- `uv run ruff format --check src tests scripts/generate_event_types.py`: PASS.
- `uv run python scripts/generate_event_types.py --check`: PASS; generated event contract unchanged.
- `git diff --check`: PASS.

All nine shared component categories have a first implementation and the current applicable paths use them. Structured source tables, real Section Summary sources, background summary upload stages, invalid-Citation validation and automatic backend retry remain the assigned later-ticket integrations; no backend behavior was added here. The actual #01 UI explicitly says its Document Summary is unavailable when `document_summary` is null.

User approval is PENDING. Final acceptance, independent review fixes, rebase and integration checks proceed only after levi relays recorded user approval.

## D16 follow-up (2026-10-14, user feedback items 2–6)

Frontend only; palette, local Noto Serif TC 16px, spacing scale and "no shadows or animation" are unchanged.

- **Source pane.** Collapsed rails are 64px wide and carry a vertical 14px label (來源 / 文件) beside the icon. On desktop the expanded pane is resized by a `role="separator"` on its left edge: default 400px, min 260px, max `min(720, window − left column − 8 − 360)`, so the conversation keeps at least 360px. Pointer events use pointer capture; `pointerup`, `pointercancel` and `lostpointercapture` end the drag. Keyboard: Arrow keys ±16px (Shift ±64), Home/End jump to min/max; ArrowLeft widens because the edge moves left. The width is re-clamped on every render, so window resize and collapsing the left column cannot leave it out of bounds. It is remembered in `localStorage` (`chat-document.source-width`, wrapped in try/catch). Narrow screens (≤900px) keep the overlay, Escape and focus return; no separator is rendered there.
- **Composer.** Radius 6px, 1px warm-neutral border, slate border plus 2px ring on focus, 44px-class send button (filled slate when it can send, outlined and muted when it cannot). The visible 問這份文件 label and the 回答以文件為依據… hint are gone; the textarea keeps `aria-label="問這份文件"`. The help line now reads "Enter 送出，Shift+Enter 換行" when ready, and still gives the reason when the composer is disabled.
- **Example questions.** Five real `<button type="button">`s under the composer, exact strings from the assignment plus the two chosen additions. Enabled only when a Document is Ready and nothing is generating. They call the same `ask()` as typing; a synchronous `asking` ref makes repeated clicks send once, and a typed draft is kept. **Decision for other Documents:** decided by filename (`/lightrag/i`, no backend field). A non-LightRAG Document shows only `Summary this document.` under the neutral label 「範例問題」; the LightRAG-specific four never appear. With no Document the LightRAG set is shown disabled. On narrow screens the row scrolls inside itself.
- **No underlines in answers.** `text-decoration` is `none` everywhere in an answer. Emphasis and headings use a 0.4–0.5px `-webkit-text-stroke` (the bundled Noto face has only a regular weight and synthetic bold does not render). Citations stay slate chips (11px, bordered, space before them). 未驗證 keeps its meaning as a danger-colour dotted chip with the text 未驗證.
- **Spacing.** One rhythm for rendered Markdown: 12px between blocks, 24px above a heading, 8px under it, 4px between list items. The old loose-list gap came from structural newline text nodes rendered by `white-space: pre-wrap`; a small rehype step now drops them.
- **Harness.** `scripted-events.js` adds `replay-cost` and `replay-q3` (replays of stored real output pasted in the feedback, not a fresh model run; the recorded Q3 factual FAIL is kept verbatim), a synthetic `spacing` scenario, `documentName` and an `asks` log. `checks.js` gained assertions for the items above (`window.__collectFailures = true` records every FAIL instead of stopping). `followup.sh` drives real mouse and keyboard input.
