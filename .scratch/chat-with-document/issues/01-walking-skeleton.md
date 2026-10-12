# #01 Walking skeleton：上傳 → 提問 → 串流出附 Citation 的回答

Status: ready-for-agent

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

用最簡單的方式，把整條流程從頭到尾打通：

1. 使用者在網頁上傳 PDF。系統同步處理：每一頁先當作一個虛擬 Section，把段落裝進 Chunk，再用 bge-m3 做 embedding。
2. 使用者提問。這個階段一律走 Lookup，檢索前 5 名的 Chunk。
3. 透過 LLM Gateway 產生回答（`medium`，輸出預留 3,000），再用 SSE 串流事件給前端。
4. 介面顯示三樣東西：
   - 逐字出現的回答。
   - 可以點開的 `[C#]` Citation，點下去看到原文和頁碼。
   - Trace：每次 LLM 呼叫的估算 tokens、`prompt_eval_count`、think 等級、以 10K 為滿格的長條，以及檢索到的 Chunk 和相似度分數。

這個切片要建好之後所有切片共用的骨架：

- **應用層的兩個操作**（上傳 Document、提問），以及它們的事件格式，見 PRD 的事件契約。這個切片先發出這幾種事件：`plan`（固定為 Lookup）、`retrieval`、`citation_map`、`delta`、`final`、`trace`、`error`。
- **LLM 和 Embedder 兩個可替換的 adapter**，以及一個照劇本回應、並記錄每次呼叫的假 LLM。
- **LLM Gateway：** 依呼叫類型查 Context Budget 表；用 `o200k_harmony` 估算 tokens，再加 300 的安全邊際；超過額度就 raise，並發出 `error` 事件。
- **回答 prompt 的基本規則：** 只根據提供的內容回答；用編號標示引用；找不到答案時回答固定的一句話；用提問的語言回答。
- **專案骨架：**
  - Python 端：uv、pytest、ruff、FastAPI。
  - 前端：React + Vite + TypeScript。build 好的前端由 FastAPI 提供，並且一起 commit。
  - README 寫明只要 Python 和 Ollama 就能啟動。
  - 測試前用下載腳本取得 LightRAG 論文。

## Acceptance criteria

- [ ] 一行指令就能啟動。用瀏覽器上傳 LightRAG 論文後，可以提問。
- [ ] 問 Q3 時，回答會串流出來；`[C#]` 點開後能看到原文和頁碼。
- [ ] Trace 顯示每次 LLM 呼叫的估算 tokens、`prompt_eval_count`、think 等級、10K 長條，以及檢索到的 Chunk 和分數。
- [ ] 確定性測試（假 LLM 加上真的 bge-m3）：假 LLM 記錄下來的每一次呼叫，prompt tokens 加上輸出預留都 ≤ 10,000。
- [ ] 確定性測試：把額度設定到一定會超過的值時，guard 會被觸發，提問會發出 `error` 事件，而且不會發出 `final`。
- [ ] HTTP 契約測試：提問的 SSE 事件順序是 `plan` → `retrieval` → `citation_map` → `delta`… → `final` → `trace`。
- [ ] 前端的 TypeScript 事件型別和後端的事件模型一致。

## Blocked by

None - can start immediately
