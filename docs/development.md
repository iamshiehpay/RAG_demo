# 開發指南

所有命令從 repository 根目錄執行。安裝與使用見 [README](../README.md)，功能規格見 [design.md](design.md)。

## 程式導覽

主要程式放在扁平的 `app/`，測試題與模型替身放在 `eval/`，不隨正式 Python 套件安裝。

- **上傳**：`api` → `Application.start_upload` → `ingestion.process_document` → PDF 解析／切塊／embedding／摘要 → 完整 Document 發布。
- **提問**：`api` → `Application.ask` → `AskWorkflow` → Router → 摘要或檢索證據 → 回答串流 → Citation 驗證 → 成功對話歷史。

| 模組 | 責任 |
|---|---|
| `api.py` | HTTP、SSE、前端靜態資產；啟動入口 `app.api:create_app` |
| `application.py` | 活動 Document、互斥操作、背景工作、來源查詢與公開問答入口 |
| `ingestion.py` | 文件處理管線、快取讀寫與上傳進度；準備完成後交由 Application 發布 |
| `ask_graph.py` | 每個請求的 LangGraph 狀態與節點、串流確認與取消清理 |
| `pdf_parser.py` | 公開 `parse_pdf()` 入口：驗證 PDF，組合版面、表格、Section 解析 |
| `pdf_layout.py` | 座標、閱讀順序、字型與文字行；辨識頁碼及圖形區域 |
| `pdf_sections.py` | 章節標題、正文／圖標籤判定、中英文段落接續與 Section 組裝 |
| `table_layout.py`、`table_grid.py` | 定位表格與續頁、解讀對齊格線；不可靠時保留原文 |
| `tables.py`、`chunker.py` | 表格文字輸出與依列分段、Section 內段落切塊 |
| `embedder.py`、`index.py` | 本地 embedding、dense／加權 BM25、相鄰與連結 Chunk |
| `router.py`、`context_packer.py` | 問題分類與追問改寫、檢索／分批抽取及證據容量 |
| `summary_tree.py`、`summary_selection.py`、`summary_context.py` | 摘要樹、表格密集原文選取、完整摘要層選擇 |
| `answer_generator.py`、`citation.py` | 串流回答與截斷重試、引用標記及來源映射 |
| `llm_adapter.py`、`llm_gateway.py`、`tokens.py` | 原生 Ollama、共用 budget guard 與 token 計數 |
| `models.py`、`events.py` | 領域資料與 SSE 事件契約 |
| `cache.py`、`policy.py`、`settings.py` | 處理快取、固定限制、可調參數 |

## 測試

```sh
uv sync --frozen
uv run --frozen pytest
```

| 範圍 | 命令 | 前置條件 |
|---|---|---|
| 離線回歸 | `uv run --frozen pytest` | 不需 Ollama |
| 整合回歸 | `uv run --frozen pytest tests/integration` | 本地 Ollama、bge-m3、下載的 PDF |
| 完整非雲端回歸 | `uv run --frozen pytest tests eval` | 同上；預設排除 eval marker |
| 真實回答與 Router | `uv run --frozen pytest eval -m eval -s` | 另需雲端模型權限；見 [eval 說明](../eval/README.md) |

不使用 uv 時，可在 README 的 Python 環境安裝 `pytest pytest-asyncio opencc ruff`；此替代方式不提供鎖定保證。`conftest.py` 依目錄加入 unit／integration 標記。測試按功能組織，不以 issue 編號命名；不從其他測試檔 import helper。

`tests/data/` 保存必要的逐字 Router 回應與長文件原文選取決策。真正需要下載 PDF 的測試放在 integration。模型替身驗證程式行為，不代表真實回答品質；相同測試的斷言不因檔案移動而刪除。

```sh
uv run --frozen ruff check app tests eval scripts
uv run --frozen python -m scripts.generate_event_types --check
```

只改文件時檢查連結與命令；修改處理程式時確認 `cache.PIPELINE_SOURCES` 包含新增模組。快取來源指紋改變會重建文件摘要，不保證舊快取可沿用。

## 驗證產物放哪裡

| 內容 | 位置 | 保留規則 |
|---|---|---|
| 一般測試結果 | 終端；需要保存時用 `.cache/verification/` | 不提交逐次 stdout、截圖或中間 JSON；確認結論後可刪除 |
| 新發現的 bug 與可重現案例 | `tests/`，必要輸入放 `tests/data/` | 併入相關功能測試，不再保留同用途的一次性腳本 |
| 模型評估的原始輸出 | `eval/reports/<實驗名稱>/` | 預設忽略，每次實驗使用新位置 |
| 值得交付的最終評估 | `eval/results/` | 只挑選最終報告、原始回答／判分與失敗分析，附來源版本與設定 |
| 本次完成工作的驗證結論 | `docs/validation.md` | 維護精簡摘要：範圍、命令、結果、限制與來源版本；舊版本交給 Git |
| 人改變方向、AI 建議被推翻或錯誤被修正 | `docs/ai-log.md` | 寫決策與原因，連到 commit／測試；不複製整份測試輸出 |

主分支不再為每次修正建立 `red/green/final/review` 報告目錄。同一結果由一處保存，其他文件連結即可。既有 docs 歷史證據與工作項目已依使用者要求復原；保留它們。未來新產物依上表挑選，不再擴增逐輪報告；完整當時版本另有 Git 標籤。

## 前端開發

需要 Node.js 20.19 以上，Vite 的 5101 代理 `/api` 至 8101。

```sh
npm ci --prefix frontend
npm run dev --prefix frontend
npm run typecheck --prefix frontend
npm run test:source --prefix frontend
npm run build --prefix frontend
```

前端修改後重新 build 並提交 `frontend/dist/`。`app/events.py` 是事件型別來源；執行 `uv run --frozen python -m scripts.generate_event_types` 更新 TypeScript，再以 `--check` 核對。[前端設計](frontend.md) 說明現行三欄與 Citation／Trace 互動。

## 可調參數

Application 與 eval 共用 `RetrievalSettings`；固定上限見 `app/policy.py` 和 `app/llm_gateway.py`。

| 環境變數 | 預設 |
|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` |
| `CHUNK_TOKEN_TARGET` | 500 |
| `LOOKUP_TOP_K` | 5 |
| `SYNTHESIS_TOP_K`、`SUB_QUERY_TOP_K` | 3、2 |
| `BM25_WEIGHT` | 0；可設 0–1，代表加權 RRF 的 BM25 比重 |
| `ANSWER_THINK` | `medium`，也可用 `low`；預留固定 3,000 |
| `SUMMARY_CONCURRENCY` | 4，須為正整數 |

中文詞彙缺少英文重疊時保留 dense 排名；Trace 的 cosine 與 RRF 分數不可直接比較。文件快取放在 `.cache/`，不快取回答或歷史。

## 交付

主分支包含正式程式與依要求復原的歷史文件。若要完整交付目前內容，提交後可使用 Git 內建功能：

```sh
git archive --format=zip --prefix=chat-with-document/ --output=../chat-with-document.zip HEAD
```

只包含已提交內容，不含 `.git`、安裝環境、PDF 或本地快取。README、原始碼、前端 build、必要測試、最終結果與 AI 協作摘要都在主分支；完整歷史查詢方式見 [history.md](history.md)。交付完整 repository 時也要帶上歸檔標籤。這些命令不會寄信或邀請協作者。
