# #04 上傳進度與快取

Status: done

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

- [x] 上傳的請求會立刻回應，介面上的進度即時更新。
- [x] 處理完成前，提問框是停用的，並顯示原因。
- [x] 確定性測試：同一份檔案第二次上傳時，Embedder 和 LLM 都沒有被呼叫，系統直接進入 `ready`。
- [x] 確定性測試：改變處理流程的版本之後，同一份檔案會重新處理。
- [x] HTTP 契約測試：上傳的事件一定以 `ready` 或 `error` 結束。

## Blocked by

- #01（`01-walking-skeleton.md`）

## Comments

- 2026-10-13 nova：完成 #04。原實作 cf9c904 已整合於 4eee3d2；獨立 Review APPROVE（既有 .lat/briefs/t04-rereview-report.md）。獨立 QA nova-qa04-kilo（GPT6.1 medium，workspace-write/on-request）在整合後 d56e092 程式碼完成 5/5 AC PASS：focused 23 passed、full 192 passed/2 deselected，真 bge-m3、真實瀏覽器進度／停用狀態／快取／錯誤恢復與文件切換驗證。Main 查證 cd3e303 與 d56e092 的 src/frontend/tests/config 無差異。完整證據：[QA supplement](../../../docs/verification/ticket-04/qa/takeover-report.md)。#05 摘要／概覽相關共同驗收留在 #05，#09 定稿後上傳介面仍須回歸。
