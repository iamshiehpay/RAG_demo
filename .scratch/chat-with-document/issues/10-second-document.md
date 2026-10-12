# #10 第二份文件與泛化驗證

Status: ready-for-agent

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

拿第二份文件驗證系統的泛化能力。

1. **由 AI 挑選文件。** 條件：2026 年發表的 arXiv 論文、雙欄排版、含附錄 40 頁以上、主題不是 RAG。把固定版本加進下載腳本。
2. **寫 2～3 條 Golden Facts：** 一個數字題、一個摘要題。
3. **驗證四件事：**
   - 換了不同的模板，章節偵測仍然合理。
   - Group Summary 確實被觸發。
   - 所有 LLM 呼叫都 ≤ 10K。
   - Golden Facts 通過。
4. **加分項：** 加入一份中文 PDF，驗證中文的斷句。
5. **把觀察到的問題記進 ai-log。**

## Acceptance criteria

- [ ] 下載腳本能取得第二份文件的固定版本。
- [ ] 處理成功；報告中記錄偵測到的 Section 數量，以及 Group Summary 的層數（至少 1 層）。
- [ ] eval 報告裡，第二份文件的 Golden Facts 通過，而且所有呼叫都 ≤ 10K。
- [ ] 在 ai-log 記錄泛化時遇到的問題和修正。

## Blocked by

- #03（`03-table-reconstruction.md`）
- #05（`05-summary-tree-global.md`）
- #08（`08-eval-harness.md`）
