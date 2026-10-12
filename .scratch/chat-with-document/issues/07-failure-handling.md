# #07 失敗處理與串流狀態

Status: ready-for-agent

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

- [ ] 確定性測試：假 LLM 第一次回傳「有內容但 `done_reason=length`」，重試後成功。事件中會有 `retry`，最後是 `final`。
- [ ] 確定性測試：連續兩次被截斷時，最後是 `error`，而且沒有 `final`。
- [ ] 確定性測試：回答引用了不存在的 `[C99]` 時，`final` 裡的那句話被標成 Unverified，Trace 記錄的無效引用數量是 1。
- [ ] 確定性測試：Embedder 連線失敗時，會發出 `error` 事件。
- [ ] 介面：暫定文字有明顯的樣式；收到 `retry` 時，暫定文字被清除；出錯時顯示重試按鈕，按下後重新提問。

## Blocked by

- #01（`01-walking-skeleton.md`）
