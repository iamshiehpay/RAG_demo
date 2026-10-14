# #07 失敗處理與串流狀態

Status: done

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

- **暫定文字：** 串流出來的文字先標示為「暫定」，收到 `final` 才定稿。
- **截斷就重試：** 只要 `done_reason=length` 就算失敗，即使已經有內容也一樣。
  - 失敗後改用 `low` 重試一次，並發出 `retry` 事件；介面清除原本的暫定文字，顯示「重新產生中」。
  - 再失敗的話，發出 `error`，不發出 `final`。
- **Citation Validator：** 遇到不存在的編號時，移除該編號，並把那句話標成 Unverified；Trace 記錄無效引用的數量。
- **連線失敗：** Router、Embedder 或 LLM 連線失敗或逾時時，發出 `error` 事件。介面顯示錯誤訊息和重試按鈕。

**介面的部分：** 如果 #09 已經合併，就使用它提供的共用元件；如果還沒合併，先用最簡單的樣式，等合併時再換成共用元件。

## Acceptance criteria

- [x] 確定性測試：假 LLM 第一次回傳「有內容但 `done_reason=length`」，重試後成功。事件中會有 `retry`，最後是 `final`。
- [x] 確定性測試：連續兩次被截斷時，最後是 `error`，而且沒有 `final`。
- [x] 確定性測試：回答引用了不存在的 `[C99]` 時，`final` 裡的那句話被標成 Unverified，Trace 記錄的無效引用數量是 1。
- [x] 確定性測試：Embedder 連線失敗時，會發出 `error` 事件。
- [x] 介面：暫定文字有明顯的樣式；收到 `retry` 時，暫定文字被清除；出錯時顯示重試按鈕，按下後重新提問。

## Blocked by

- #01（`01-walking-skeleton.md`）

## Comments

- 2026-10-13 Orchestrator：完成。實作 levi-t07-bali（Codex gpt-6.1-sol high）；交付至 `9538b88`，已在 `main`。
  - Review（Claude Opus 5.5 high）：第一輪 CHANGES_REQUESTED（Unverified 用文字中的「未驗證」字串判斷，正常句子會被誤標；分批抽取不展開範圍引用；錯誤代碼不分階段；重試狀態被覆蓋；舊回合重試順序錯亂），修正後 APPROVE。裁決：超出對照表的範圍引用整個標為 Unverified。
  - QA（Claude Opus 5.5 high；真實 gpt-oss＋以劇本 LLM 驅動的真實 UI）：16 PASS、0 FAIL；報告 `docs/verification/ticket-07/qa/qa-report.md`。
  - 移交：錯誤狀態仍是斜體、Unverified 標籤緊貼下一句 → #09；上傳時 Ollama 失敗 → #04；HTTPStatusError／ValueError 分類 → #11。
