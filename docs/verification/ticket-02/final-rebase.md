# Ticket #02 — approved candidate on integrated main

Fourth review approved `f971978` (HCOM #3914). Requested base: `79c82a8`; rebased source checkpoint: `71b7762`. Final evidence head is supplied in the HCOM reply. Figure-step labels and frame-contained unnumbered-heading edge cases are deferred to #10 as instructed.

## Integration

- Combined #02 Citation side-notes with #07's `UnverifiedSpan` renderer, keeping Unicode code-point offsets, provisional styling, inline C/S citations and click-to-source behavior.
- Gateway retains #07's effective retry think and #02's recorded `call_type`. Application retains keyword-only validated settings/target and passes the effective target to parser and chunker. Its ask/failure behavior is unchanged from #07.
- Parser-dependent extraction regression keeps variable batch-count assertions and the terminal trace → error order. README retains both implemented scopes. AI logs preserve #02/#06/#07/#08 content in date order without duplicated blocks.
- Rebuilt and committed `frontend/dist` from combined source; a second build produces identical output. No changes to #07 `App.tsx`, event contracts, answer generator or Citation Validator.

## Checks

- `uv run pytest -q`: **173 passed, 2 deselected**, 105.27 s; six existing dependency warnings. Native cloud eval remains opt-in.
- `uv run ruff check src tests eval scripts`: PASS.
- `uv run ruff format --check src tests eval scripts`: PASS, 61 files.
- `uv run python scripts/generate_event_types.py --check`: PASS.
- `npm run build` in `frontend/`: PASS (`tsc --noEmit` + Vite).
- `git diff --check`: PASS.

## Real-browser LightRAG verification

FastAPI served the rebuilt production frontend at `http://127.0.0.1:8110`, using the native local Ollama bge-m3 and gpt-oss adapters. Isolated Chrome session: `t02-vida`.

1. Uploaded `data/lightrag.pdf` through the file control: **41 Chunks · Ready**.
2. Asked `How does dual-level retrieval work in LightRAG? Cite the source.`: finalized answer, no provisional styling. Side-notes displayed `[C2] · p.4–5` / `3.2 DUAL-LEVEL RETRIEVAL PARADIGM` and `[C4] · p.10` / `6 CONCLUSION`.
3. Clicked the C2 side-note: original source opened at `Source · p.4 · 3.2 DUAL-LEVEL RETRIEVAL PARADIGM`, showing specific/abstract queries, low/high-level retrieval and local/global keyword matching.
4. Browser errors/console: empty. Horizontal overflow: false. Screenshots visually inspected: [answer and side-notes](evidence/final-rebase-citation.png), [opened source](evidence/final-rebase-source.png).

The preceding live Table 2 question returned `Not mentioned in the document.` despite the known table facts. That result remains visible in the screenshots; it is not a Golden Facts pass. Table reconstruction and end-to-end quality remain #03/#11. This round verifies #02 upload/provenance/Citation UI behavior; no parser scope expansion was made.

Owned browser and backend processes were stopped before delivery.

## Current integration seams

- `src/chat_document/application.py:39`: `Application(embedder, gateway, *, settings=None, chunk_token_target=None)` resolves defaults and validates an explicit target through `RetrievalSettings`, passing the same settings to Context Packer.
- `src/chat_document/application.py:61`: upload clears current in-memory state, emits parsing/chunking/embedding stages, calls `parse_pdf(..., chunk_token_target=self.chunk_token_target)` and `chunk_sections(..., target=self.chunk_token_target)`, builds Index, then stores Document and emits ready/error. #04 owns atomic replacement/background/cache changes.
- `src/chat_document/models.py:15`: Section fields `paragraph_pages`, `is_appendix`, `is_virtual`; zero-Chunk Sections remain metadata and are excluded from Summary Tree input. Cache serialization must preserve these fields and include effective Chunk target in its processing identity.
- `frontend/src/Answer.tsx:10`: used C/S IDs select clickable page/Section side-notes around the existing structured Unverified renderer.
- `src/chat_document/llm_gateway.py:71`: requests use effective think and call type together.

All assigned #02 criteria remain covered by the passing suite and browser evidence. Awaiting Levi's integration verification; no merge or push.
