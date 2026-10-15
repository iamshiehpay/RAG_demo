# 驗證摘要

本檔維護目前交付變更的精簡結論，先前完整內容由 Git 保存；產物放置方式見 [開發指南](development.md#驗證產物放哪裡)。

## 2026-10-15：恢復追蹤 AGENTS 與 CONTEXT

來源基準：`9cff029`。依使用者指示恢復追蹤 AGENTS.md、CONTEXT.md，移除其忽略規則並同步文件入口；LangGraph ADR 與 AI 協作摘要維持僅限本機。CONTEXT 內容保持不變，AGENTS 更新交付範圍及相關導航。

以 Git index 檔案清單核對交付 Markdown 的本地連結、兩份文件已追蹤及另外兩份仍未追蹤；`git diff --check` 通過。僅文件與追蹤規則變更，未重跑程式測試。

## 2026-10-14：精簡文件與 GitHub 交付

來源基準：`490ab63`。使用者確認後，移除 `docs/verification/`、`docs/qa/` 共 1,449 個逐輪產物；移除前全部與 `archive/before-main-cleanup-20261014` 逐位元核對一致。docs 保留 11 個必要文件，`.scratch/chat-with-document/` 保留 19 個規劃與工作項目檔案。

- 需求與驗收敘述不變；歷史證據連結改為 GitHub 固定 commit，共 46 個連結的目標逐項核對存在於歸檔。
- 保留 Markdown 的本地檔案連結與 `git diff --check` 核對通過。
- 正式程式、前端、測試、依賴與最終評估未變更；不重跑程式測試或模型評估，既有 342 PASS 基準見下方。
- 使用者指定的 `iamshiehpay/RAG_demo` 已確認為私人 repository；交付 main 與歸檔標籤，完整證據查閱方式見 [歷史索引](history.md)。

## 2026-10-14：app 小幅精簡

來源基準：`2ace181`。移除未使用的 `Index.build` 和 `Application.chunk_token_target` 重複欄位；建構參數仍會更新共用 settings。四種錯誤分支共用一次 Trace 輸出，保留錯誤分類、訊息、Trace → Error 順序與取消清理。程式淨減 15 行；設定與 Ollama 模組尚未合併。

- `.venv/bin/python -m pytest tests eval -q`：342 passed、3 deselected，273.62 秒；5 個 SWIG 相依套件棄用警告。
- `.venv/bin/ruff check app/application.py app/index.py`、`git diff --check`：通過。
- 使用既有回歸測試；沒有改動 prompt 或模型輸出格式，未執行雲端評估與瀏覽器 QA。

此版本曾保留全部歷史文件與工作項目；後續核准的精簡範圍見本檔最新紀錄。8101 網站保持關閉。本次由同一 agent 修改與驗證。

## 2026-10-14：字型整併與驗證產物規則

來源基準：`6a618ef`。使用者要求關閉 8101 網站、刪減字型檔案並明確規範驗證紀錄位置。

| 檢查 | 結果 |
|---|---|
| 本機網站 | 對確認的 8101 程序送 SIGTERM，確認連接埠無監聽；完成後保持關閉 |
| 字型 | 同一 Noto Serif TC 2.003 版本；108 個分片 → 1 個 Regular WOFF2；3,035,932 → 2,473,812 bytes |
| 字元覆蓋 | 新字型 cmap 保留舊分片聯集的全部 12,377 個字元；靜態 weight=400，13,039 個 glyph |
| 前端建置 | `npm run build --prefix frontend` 通過（含 TypeScript），Vite 建置 729ms |
| 來源呈現 | `npm run test:source --prefix frontend` 通過 |
| 建置資產 | source／dist 各只有一個 WOFF2，內容逐位元一致；HTML／CSS 的資產路徑全部存在 |
| 文件 | 本地 Markdown 檔案連結核對通過；AGENTS 指向單一產物放置規則 |

字型來源、生成方式及 SHA-256 見 [前端設計](frontend.md#本地字型)。臨時轉換工具沒有加入產品依賴；沒有改動 app、模型 prompt 或套件鎖檔。首次載入會讀取整個字型，之後由瀏覽器快取。

本次沒有重新啟動網站做瀏覽器視覺 QA，也沒有執行後端全套或雲端模型評估。檢查範圍為字型資料、前端建置與靜態資產完整性。

## 已有的後端重構基準

`6a618ef`：342 項非雲端回歸通過、3 項 live eval 未執行；最終 unit 整併及全新環境安裝後各 123 PASS。兩份真實 PDF 的完整解析資料與重構前逐欄一致，236 個保留測試函式的 assertion AST 一致。完整當次結論可用 `git show 6a618ef:docs/validation.md` 取得。

最終模型品質報告仍為當時版本的 FAIL，A9 已知缺陷不改判；見 [評估結果](../eval/results/README.md)。本次均由同一 agent 完成，不宣稱獨立審查或品質提升。
