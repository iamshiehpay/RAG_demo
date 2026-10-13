# #11 調參與最終驗收

Status: ready-for-human

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

- [x] 實驗結果表寫進 eval 報告，選定的設定也更新到 AGENTS.md。
- [x] Q1～Q3 的 Golden Facts 每題跑 N=3，報告每條 fact（含 forbidden claim）的通過率與失敗原因；調參與最終 eval 從開工起最多 3 小時（使用者決策，2026-10-13：由「必須通過」改為「量測並報告」）。
- [x] 從乾淨的 clone 開始，照 README 只裝 Python，加上開著的 Ollama，就能跑起來。
- [x] 兩份文件的快取已經建好。

## Blocked by

- #02、#03、#04、#05、#06、#07、#08、#09、#10（全部）

## 整合與最終人工驗收

已審 source `f089cae`／文件證據尾提交 `50eab20`，依 D10 A 接受明列逐項 Citation 支持限制並保留 FAIL；D09 由使用者依 [人工清單](../../../docs/verification/final-acceptance/manual-qa-checklist.md) 操作。

- 實驗／最終結果：`eval/reports/issue11-correction/`；27實際回答，raw品質FAIL保留，272呼叫均≤10K，正式Router/Answer無截斷。
- 完整初審及限定複審：`docs/verification/ticket-11/review-0c320a8.md`、`review-f089cae.md`。
- 修正後327確定性測試PASS；乾淨Python clone、前端build與兩份current pipeline快取證據已核對。
- 主工作區 `db64d84` 整合驗證：327 passed、3 eval deselected、zero skipped，263.68s；兩份current pipeline快取公開上傳皆Ready，0 LLM／0 embedding calls。詳見 [integration.md](../../../docs/verification/ticket-11/integration.md)。
- 最終人工QA：使用者確認Q3找到正確表格、接受簡短回答，其餘測試正常；A9已確認固定拒答；原文p.8有支持內容，保留FAIL且原因UNPROVEN。獨立重跑另見系統警告誤歸因，D14待真人處置，尚未done。原始回饋與判定邊界已寫入人工清單；不重新調Q3、不把原N3 FAIL改判。

- A9有界診斷：[report.md](../../../docs/verification/ticket-11/manual-a9/report.md)。沒有產品修改；D14兩項明列失敗待決，不以HTTP成功或有效Citation ID取代語意根據驗收。
