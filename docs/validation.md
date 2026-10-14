# 主分支重構驗證（2026-10-14）

使用者核准精簡主分支並將 `src/chat_document/` 搬至 `app/`。重構前版本與全部歷史證據由 [歸檔標籤](history.md) 保存。本次未呼叫其他 agent，由同一位 agent 實作與檢查；不宣稱獨立審查。

主分支追蹤檔案由 **1,948 減至 337（減少 82.7%）**：docs 1,457→8、eval 119→22、tests 37→31、scripts 6→2。前端 237 個保留檔案包含原始碼、字型分片與 build；app 共 29 個扁平模組，最長 473 行。

## 實作與驗證

| 項目 | 結果 |
|---|---|
| 正式入口 | `app.api:create_app`；HTTP 資產與快取根目錄隨搬移修正 |
| 文件處理 | 從 Application 抽出 `ingestion.process_document`，完成後才發布活動 Document |
| PDF／表格 | 分開版面、Section 組裝、表格定位、格線判讀及輸出；兩份真實 PDF 的完整解析資料與重構前逐欄一致 |
| 正式套件 | Router 題庫、劇本模型移至 eval；app 不 import eval 或 tests |
| 功能回歸 | `pytest tests eval -q`：342 PASS、3 live eval deselected、0 skip，276.93 秒 |
| 測試整併後 | 小型 unit 檔依功能合併；重跑 unit：123 PASS；最終收集仍為 342 項非雲端／3 項 live |
| 案例保留 | 原有 236 個保留測試函式的全部 assertion AST 一致；移除 4 個已歸檔雙 zip 工具測試，新增 3 個函式／7 個案例 |
| 全新環境 | 獨立目錄 `uv sync --frozen` 安裝 57 個套件；123 unit PASS、0 skip，事件型別同步檢查 PASS |
| 靜態檢查 | `ruff check app tests eval scripts`、事件型別核對及文件本地連結檢查通過 |
| 資料完整性 | 四份最終評估原始檔與歸檔版本逐位元相同；17 個核心模組除位置外逐位元相同 |
| 本機網站 | 8101 以新入口重啟；首頁／JS／CSS 200 且位元一致；未上傳提問回 document_not_ready，零模型呼叫 |

新入口與 ingestion 介面先以失敗測試確認不存在，再實作到通過。PDF 比對包含 Section、段落、表格欄位、頁碼與來源，不只比較數量。原本的雙欄、圖標籤、caption、中文與表格回歸持續保留。

## 過程中發現的問題

- 本機 editable 安裝仍指舊路徑，獨立腳本 import 失敗；重新安裝本專案後修正。
- 新環境的 offline 安裝因缺少 langsmith 快取失敗；改為依同一份鎖檔下載依賴後完成，未變更依賴版本。
- 新處理模組納入快取來源指紋，避免新增檔案變動卻沿用舊快取。重啟需重新上傳，舊來源指紋的快取會失效。

## 驗證邊界

未調整產品 prompt、模型、檢索設定或 SSE 契約；不重跑雲端回答品質評估。既有 N=3 結果仍為當時版本的 FAIL，A9 已知缺陷不改判。本次沒有宣稱人工瀏覽器 QA、模型品質提升或逐論點 grounding 已全面通過。前端原始碼／dist 與依賴鎖檔未變動，不需要重新 build。

完整非雲端回歸先於最後的 unit 檔案整併；整併後另驗證 unit、收集清單、斷言 AST 與乾淨安裝。測試警告僅為既有 PyMuPDF SWIG 型別的 DeprecationWarning。
