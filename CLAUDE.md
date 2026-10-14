@AGENTS.md

# Claude 工作入口

共用限制、修改流程與保留規則以匯入的 [AGENTS.md](AGENTS.md) 為準；更新共用規則時修改該檔，本檔只補文件導航。

## 依任務讀取

| 任務 | 入口 |
|---|---|
| 安裝、啟動網站 | [README](README.md#快速啟動)；目前 factory 為 `app.api:create_app` |
| 理解程式、測試或前端建置 | [開發指南](docs/development.md)；正式 Python 程式在 `app/` |
| 確認需求與驗收條件 | [.scratch PRD](.scratch/chat-with-document/PRD.md)、[工作項目](.scratch/chat-with-document/issues/)、[原始測試清單](.scratch/chat-with-document/test-list.md) |
| 修改設計或領域用語 | [設計規格](docs/design.md)、[CONTEXT](CONTEXT.md)、[ADR](docs/adr/) |
| 保存驗證結果、整理檔案 | [產物保留規則](docs/development.md#驗證產物放哪裡)、[最新驗證摘要](docs/validation.md) |
| 查閱舊 verification／QA 證據 | [歷史索引](docs/history.md)；從固定版本或歸檔標籤讀取，日常開發維持精簡工作目錄 |

PRD、tickets 與 AI log 包含當時的路徑、命令和狀態；啟動與測試使用現行 README／開發指南。規格衝突先指出差異，依本次使用者指示與現行設計處理，不把歷史結果當成目前版本的驗證。
