# #08 Eval harness 與 Golden Facts

Status: done

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

用一個指令跑回答評估（`-m eval`）。評估透過同樣的兩個操作進行，但使用真的 gpt-oss。

- **Golden Facts：** 依 AGENTS.md 的清單，定義 LightRAG Q1～Q3 的 Golden Facts。
  - 必須出現的事實：數字類的要寫明變體、資料集、指標和比較方向。
  - forbidden claim：不得出現的錯誤結論。
- **其他測試題：** 3 題文件裡沒有答案的問題；router 的 12 題回歸測試（題目來自實測腳本）。
- **三種檢查方式：**
  - **`contains`：** 只用來檢查專有名詞。比對前，先統一連字號（包括 U+2011）、空格和百分比的寫法。
  - **`judge`：** 用 `low`。judge 必須逐字摘錄回答中的證據句，再由程式確認這句話真的出現在回答裡；不在回答裡就判定失敗。
  - **`forbidden`：** judge 只要能摘錄出這個錯誤結論，就判定失敗。
- **報告：** 寫成 markdown，存到報告目錄。內容包括每條 fact 是否通過、每次呼叫的 token 用量和延遲。可以設定每題跑 N 次，並計算通過率。

## Acceptance criteria

- [x] 一個指令就能跑完 eval，並產生 markdown 報告。
- [x] 確定性測試：檢查方式本身的邏輯，用固定的回答和假的 judge 驗證：
  - judge 摘錄的句子不在回答裡時，判定失敗。
  - `contains` 能處理 U+2011 連字號，以及「67.6 %」這種數字和 % 之間有空格的寫法。
  - 只寫到 `-High` 的 64.8 的回答，不能滿足「Mix 資料集上 `-Low` 是 64.8」這條 fact。
- [x] 報告列出每次呼叫的 token 用量和延遲。設定 N=3 時，會顯示每條 fact 的通過率。
- [x] commit 第一份基準報告。目前的通過情況照實記錄，不要求全部通過。

## Blocked by

- #01（`01-walking-skeleton.md`）

## Comments

- 2026-10-13 Orchestrator：完成。實作 levi-t08-fire（Codex gpt-6.1-sol high）；交付至 `11968fd`，已在 `main`。
  - Review（Claude Opus 5.5 high）：四輪。抓到逐字證據比對不容空白差異、Golden Facts 比 AGENTS 更嚴、數值錨點只看出現與否、`LightRAG‑Low` 複合寫法回歸、Router fallback 被算成正確等問題，修正後 APPROVE。`AGENTS.md` 的 forbidden 規則句依授權改為「明確斷言才算」。
  - QA（Claude Sonnet 5.5 high）：PASS 18、FAIL 0、UNPROVEN 3、NOT_EXECUTED 3（屬其他票）；沒有發現 harness 誤判。報告 `docs/verification/ticket-08/qa/qa-report.md`；live 報告 `eval/reports/qa-08-*.md`、`router-provenance-baseline.md`（同時結案 #06 AC7）。
  - 目前 Golden Facts 通過率低（7/24），屬回答品質，由 #02/#03/#05/#11 處理。
