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
- [ ] eval 報告列出第二份文件 Golden Facts 的通過率（N=3）與失敗原因，而且所有呼叫都 ≤ 10K。品質調整做到 2026-10-13 17:45 為止（使用者決策，2026-10-13）。
- [ ] 在 ai-log 記錄泛化時遇到的問題和修正。

## Blocked by

- #03（`03-table-reconstruction.md`）
- #05（`05-summary-tree-global.md`）
- #08（`08-eval-harness.md`）

## 實作裁決（2026-10-13，Main）

表格主導的 Section／局部摘要可採來源錨定的抽取式選文，以攔下來源未明言的評論。選文須核對原始 evidence，保留脈絡、作者真實限制與 provenance；沿用既有摘要 call budget、SummaryNode 與長度；Golden Facts 驗收依 D05 改為 N=3 量測報告，不新增 auditor 階段。此為 Review 後的內部修正，仍須 fresh Review 與獨立整合 QA。

## 收斂決策 D06（2026-10-13，真人核准）

本輪合併前只要求完成通用頁碼污染修正（含合法數字／跨頁句子回歸與一次 fresh N=3）、成功 `upload_error` 判斷、ai-log 與最終結果。數字檢查器的殘留誤判不阻擋合併；報告保留原始通過率、檢查器／judge 原因、Table9 與回答人工核對，以及已知 false-accept 情境。已完成且通過的修正保留。

下一輪獨立複審限定上述修改與回歸風險，不重新完整審查。新發現只有10K、Citation有根據、固定拒答或確定性測試失敗才擋合併，其他寫入已知缺陷供#11／交付報告。D05時間上限／品質量測／合併後一次QA不變。

## D08 最小恢復修正（真人核准）

在 D06 限定修正上追加：選文只消費並嚴格驗證 span_ids，丟棄額外模型註解；每次收斂／分批保留足以滿足 80–500 tokens 的原始候選。來源、表格脈絡與 10K guard 維持，不補字、不重複、不降低下限。補必要回歸，完成 fresh N=3，再依 D06 限定複審與整合 QA；未核准 N=3 未完成的驗收豁免。授權原文與定位見 Main 共用 `.lat/decisions/D08-second-document-live-recovery.md`。
