# #15 開發指引與中文 README 整理

Status: ready-for-human

## Scope

真人 2026-10-14 訊息 msg_01a1390e-639d-76b1-b2c7-2c38370887b6 要求整理過長的 AGENTS.md，參考指定文章、盤點非執行必要程式，並重構中文 README。基準 Main 52e18c9。這是文件整理，不是新的功能或品質修復。

AGENTS 主檔保留各任務共同需要的硬限制、無法由程式推出的約束與有明確觸發條件的文件入口；詳規按任務拆分，優先重用既有權威文件，避免另存一份同時生效的完整副本。README 使用繁體中文，以評審的安裝、啟動、上傳及提問流程為先，開發／評估細節可移到按需文件。清楚區分執行、開發、證據與可再生資料；只提出排除／清理建議，本票不刪檔。

## Acceptance

- [x] AGENTS 顯著精簡且保留 10K guard、text→text、原生 Ollama gateway、LangGraph 僅提問編排、PDF/切塊/檢索自寫、Citation/拒答及既有交付約束。
- [x] 原有有效設計規則、經驗與實測來源能由明確任務入口找到；過期時程、已選定值仍稱起始值等陳述已校正，歷史證據不改寫成新結果。
- [x] README 繁體中文，Python/Ollama 啟動不需 Node、Cloud 資料流、文字 PDF/單文件限制、實際操作與進階文件入口清楚；不誇稱所有答案有逐論點引用或 A9 已修好。
- [x] 檔案用途盤點依實際 imports/入口/設定，說明 runtime、development、evidence、generated；保留 dist、測試、spikes/eval 證據、原文件與使用者資料，不執行刪除。
- [x] 命令、環境前提、相對連結及權威文件引用一致；只跑文件相關檢查，不執行 LLM/eval/全套測試，不改程式、依賴、dist、快取或服務。
- [x] 使用者後續明確取消 agent 委派；改由主對話自行完成文件檢查與提交，不進行獨立 agent Review。正式程式與網站資產未修改。

## 執行方式與成果

使用者後續指示「停止任何呼叫 agent 動作，我要你自己回答」，再授權主對話自行修改檔案並補充用途。因此原多 agent 分工取消，不恢復或重新啟動角色。

主對話修改 AGENTS、README、CONTEXT、eval 文件入口，新增 `docs/design.md` 與 `docs/development.md`。資料夾與主要檔案盤點直接放 README，不再增加另一份 inventory。程式、依賴、dist、快取與服務不變；不刪除檔案。Streamlit 僅為方案討論，未授權也未執行遷移。

驗證：48 個文件相對連結與錨點全部通過；設定/命令與 policy、settings、gateway、API、Vite、package scripts、tune CLI 核對一致；git diff --check 通過，變更皆為 Markdown。未執行 LLM、eval、完整 pytest 或 agent Review。
