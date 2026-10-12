# #04 上傳進度與快取

Status: ready-for-agent

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

- **背景處理：** 上傳後立刻回應，處理改在背景進行。用 SSE 推送 `stage` 事件，依序是：解析 → 切塊 → embedding → 摘要 n/N → 完成。其中「摘要 n/N」由 #05 加入。最後以 `ready` 或 `error` 結束。
- **介面：** 即時顯示進度。處理完成前，提問框是停用的，並說明原因。
- **快取：**
  - 鍵值是「檔案內容的雜湊值 + 處理流程的版本」，存放 Chunk 和 embedding。#05 合併後，也要存 Summary Tree。
  - 同一份檔案重新上傳時，直接取用快取。
  - 處理流程的版本改變時，舊快取自動失效。

**介面的部分：** 如果 #09 已經合併，就使用它提供的共用元件；如果還沒合併，先用最簡單的樣式，等合併時再換成共用元件。

## Acceptance criteria

- [ ] 上傳的請求會立刻回應，介面上的進度即時更新。
- [ ] 處理完成前，提問框是停用的，並顯示原因。
- [ ] 確定性測試：同一份檔案第二次上傳時，Embedder 和 LLM 都沒有被呼叫，系統直接進入 `ready`。
- [ ] 確定性測試：改變處理流程的版本之後，同一份檔案會重新處理。
- [ ] HTTP 契約測試：上傳的事件一定以 `ready` 或 `error` 結束。

## Blocked by

- #01（`01-walking-skeleton.md`）
