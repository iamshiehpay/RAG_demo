# #11 調參與最終驗收

Status: ready-for-agent

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

用 eval 做實驗，決定最終設定，再完成交付前的準備。

- **實驗項目：**
  - Chunk 大小：256 / 500 / 800。
  - 前幾名的數量。
  - 加權的 BM25 hybrid 和純 dense 比較。
  - 產生回答用 `low` 還是 `medium`。
  - Ollama Cloud 的同時呼叫數上限。
  - 確認在所有 eval 執行中，正式的額度（router 600、回答 3,000）都沒有發生截斷。
- **記錄結果：** 選定的設定寫回 AGENTS.md（數值的唯一來源），實驗中觀察到的事記進 ai-log。
- **交付前準備：**
  - 定稿 README。
  - 最後一次 build 前端。
  - 跑最終的 eval 報告：Q1～Q3 每題跑 N=3。
  - demo 前，先把兩份文件都上傳一次，讓快取預先建好。

## Acceptance criteria

- [ ] 實驗結果表寫進 eval 報告，選定的設定也更新到 AGENTS.md。
- [ ] Q1～Q3 的 Golden Facts 每題跑 N=3，報告每條 fact（含 forbidden claim）的通過率與失敗原因；調參與最終 eval 從開工起最多 3 小時（使用者決策，2026-10-13：由「必須通過」改為「量測並報告」）。
- [ ] 從乾淨的 clone 開始，照 README 只裝 Python，加上開著的 Ollama，就能跑起來。
- [ ] 兩份文件的快取已經建好。

## Blocked by

- #02、#03、#04、#05、#06、#07、#08、#09、#10（全部）
