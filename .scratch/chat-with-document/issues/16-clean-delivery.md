# #16 精簡交付與測試入口

Status: in-progress

## 需求與範圍

使用者希望交付的程式碼簡潔，且能證明如何與 AI 協作，授權開始重構。沿用「停止 agent 委派、由主對話自行處理」的指示。

- 按功能與外部依賴整理測試，共用 helper 不再放在被其他測試 import 的 test module。
- 預設執行不需 Ollama 的測試，本地整合與雲端評估明確指定。
- 產生可執行程式包與補充證據包，精選協作摘要連到實測、修正與版本，不刪歷史紀錄。
- 不變更網站行為、模型、prompt、檢索、快取或前端，不新增 DB，不寄信或上傳。

## 驗收

- [x] 原有 236 個 test function 全部保留，assert AST 一致；僅 CLI 收集測試增加明確的 eval 路徑。
- [x] 收集範圍為 120 unit、219 integration、3 live eval（新增 4 個打包測試）。
- [x] `pytest` 預設只跑 unit；測試檔不再互相 import。
- [x] 打包測試覆蓋只讀 committed HEAD、排除本機資料、保留前端 build、雜湊、可重現、禁止覆寫、拒絕 symlink 與兩包不互相覆寫。
- [ ] 完整非雲端回歸與實際交付包驗證通過。
- [ ] 保存 commit、交付包及驗證摘要。

證據見 `docs/verification/release-refactor.md`。本輪沒有 agent Review 或新雲端評估。
