# #05 Summary Tree 與 Global 回答（Q1）

Status: ready-for-agent

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

- **上傳時建立 Summary Tree：**
  - **Section Summary：** 長度約為原文的 15%，最短 80、最長 500 tokens；同時最多 4 個平行呼叫（可以設定）。
  - **Group Summary：** Section Summary 加起來超過額度時，才一層層往上合併。
  - **Document Summary：** 最頂層。
  - 處理進度顯示「摘要 n/N」，Summary Tree 也存進快取。
- **追溯來源：** Section Summary 記錄它所屬 Section 的全部 Chunk；Group Summary 記錄它涵蓋的 Section。
- **文件概覽：** 處理完成時，把 Document Summary 顯示為文件概覽；對話期間也一直看得到。
- **Global 回答：** 用 `medium`，依據 Summary Tree 中「放得進額度的最詳細那一層」，並用 `[S#]` 標示引用。點 `[S#]` 時，顯示該 Section 的頁碼範圍和摘要。

**介面的部分：** 如果 #09 已經合併，就使用它提供的共用元件；如果還沒合併，先用最簡單的樣式，等合併時再換成共用元件。

## Acceptance criteria

- [ ] 處理完成時顯示文件概覽，對話期間也一直看得到。
- [ ] 問 Q1 時走 Global 路徑；回答用 `[S#]` 引用，點開後能看到 Section 的頁碼範圍和摘要。
- [ ] 確定性測試：Section Summary 的輸出長度設定符合「約 15%、最短 80、最長 500」的規則。
- [ ] 確定性測試：在測試中產生一份有很多 Section、Section Summary 加起來超過額度的文件。系統會建立 Group Summary 這一層，Global 回答使用放得下的那一層；假 LLM 記錄的每一次呼叫都 ≤ 10,000。
- [ ] 確定性測試：同一份檔案第二次上傳時，不會再呼叫摘要的 LLM。
- [ ] 如果 #08 已經合併：Q1 的 Golden Facts，以及「用三句話、中文總結」的格式要求，寫進 eval 報告。

## Blocked by

- #02（`02-structure-aware-chunking.md`）
- #04（`04-ingest-progress-and-cache.md`）
- #06（`06-router-synthesis.md`）
