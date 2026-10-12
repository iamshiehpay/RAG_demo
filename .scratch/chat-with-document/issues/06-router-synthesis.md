# #06 Router 與 Synthesis 回答（Q2、追問、超額處理）

Status: done

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

- **Router：** 一次 LLM 呼叫（`low`，用 JSON schema 輸出），產出 Question Type、Standalone Question 和 Sub-queries。
  - Prompt 規定：不確定是 Lookup 還是 Synthesis 時，選 Synthesis。
  - JSON 壞掉時，退回 Lookup。
  - #05 合併之前，判斷為 Global 的問題先走 Synthesis。
- **追問：** 只帶最近 2 輪對話歷史，每輪截到 500 tokens。
- **問題太長：** 超過 1,000 tokens 時，不呼叫 LLM，直接發出拒絕事件，並說明原因。
- **Synthesis 檢索：**
  - Standalone Question 取前 3 名，每個 Sub-query 取前 2 名。
  - 合併後去除重複，依原文順序排列。
- **超額時分批抽取：** 內容超過約 6,000 tokens 時，分批抽取事實，每條事實都要保留 `[C#]`。抽出的事實仍然放不下時，再分批合併一次。
- **介面：**
  - Trace 顯示 `plan`：Question Type、Standalone Question、Sub-queries。
  - 提問時顯示目前階段：判斷問題類型 → 檢索 → 思考中。

**介面的部分：** 如果 #09 已經合併，就使用它提供的共用元件；如果還沒合併，先用最簡單的樣式，等合併時再換成共用元件。

## Acceptance criteria

- [x] `plan` 事件含有 Question Type、Standalone Question 和 Sub-queries，Trace 也會顯示它們。
- [x] 確定性測試：假 LLM 回傳壞掉的 JSON 時，系統走 Lookup 路徑。
- [x] 確定性測試：問題超過 1,000 tokens 時，會收到拒絕事件，而且 LLM 的呼叫次數是 0。
- [x] 確定性測試：router 收到的 prompt 裡，對話歷史最多只有 2 輪，每輪都不超過 500 tokens。
- [x] 確定性測試：照劇本給出 Q2 的 Sub-queries 時，檢索結果涵蓋成本分析和增量更新的段落。
- [x] 確定性測試：強迫內容超額時，系統改用分批抽取；最後回答裡的 Citation，都能對回原始的 Chunk。
- [x] 如果 #08 已經合併：router 的 12 題回歸測試寫進 eval 報告。

## Blocked by

- #01（`01-walking-skeleton.md`）

## Comments

- 2026-10-13 Orchestrator：完成。實作 levi-t06-miso（Codex gpt-6.1-sol high）。交付 commit：`b185c97`～`4b192b3`（初版）、`f9f1651`、`9d03295`、`1da2d22`、`5799106`（QA 修正），皆已在 `main`。
  - Review（Claude Opus 5.5 high）：初版 CHANGES_REQUESTED → APPROVE；QA 修正後再審三輪（含「prompt 教到測試題」的評估洩漏）→ APPROVE。
  - QA（Claude Sonnet 5.5 high，真實瀏覽器＋真實 gpt-oss）：第一輪 FAIL（Ollama Cloud 不強制 `format`，Router 幾乎全退回 Lookup；劇本 LLM 掩蓋了這個缺陷）；修正後複驗 PASS；最後抽查繁／簡／英文回答語言 PASS。報告 `docs/verification/ticket-06/qa/qa-report.md`、`qa-report-2.md`。
  - Router live smoke：canonical 12/12、held-out 8/8、0 fallback（`eval/reports/router-smoke-*.json`）。AC7 的 #08 eval 報告：`eval/reports/router-provenance-baseline.md`（隨 #08 合併）。
  - 延後：live Q2 檢索涵蓋成本／增量更新段落 → #11；其他見 `EXECUTION.md`。
