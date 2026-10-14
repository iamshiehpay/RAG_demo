# Chat with Document｜與 PDF 對話

本機執行的文件問答網站：上傳一份 PDF，使用中文或英文提問，點擊回答中的 Citation 查看來源章節與頁碼，並透過 Trace 檢查檢索結果、模型呼叫與 token 用量。

支援有文字層的 PDF、串流回答和多輪追問。全文問題使用上傳時建立的 Summary Tree；細節與比較問題檢索原文 Chunk。每次 LLM 呼叫的 prompt、思考與回答合計限制在 **10,000 tokens**。

> 這是 PEGAAI AI Engineer 面試作業。功能與回答品質分開驗證：網站可正常操作，不代表所有回答都完整或正確；已知失敗與實測結果保留在評估報告中。

## 快速啟動

需要 **Python 3.12 以上**、[Ollama](https://ollama.com/) 與能使用 `gpt-oss:120b-cloud` 的 Ollama 帳號。先啟動本機 Ollama，再準備模型：

```sh
ollama signin
ollama pull bge-m3
```

在 repository 根目錄執行：

```sh
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101
```

開啟 **http://127.0.0.1:8101**。Windows 請把 `.venv/bin/python` 換成 `.venv\Scripts\python.exe`。

若已安裝 [uv](https://docs.astral.sh/uv/)，可改用鎖定依賴的啟動方式：

```sh
uv run --frozen --no-dev uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101
```

- 執行網站**不需要 Node.js 或自行編譯前端**；FastAPI 直接提供已提交的 `frontend/dist/`。
- 不需另外設定 API key，但須登入 Ollama 並具備雲端模型使用權限。
- Embedding 由本機 `bge-m3` 產生；文件片段、摘要及問題會送至 Ollama Cloud 生成文字。這不是完全離線的系統。
- Ollama 預設位址為 `http://localhost:11434`，可透過 `OLLAMA_BASE_URL` 修改。
- 請從完整原始碼目錄啟動；單獨的 Python wheel 不包含前端資產。

## 使用方式

1. 選擇一份有文字層的 PDF；掃描檔、不合法或無法讀取的 PDF 會回報錯誤。
2. 等待解析、切塊、embedding 與摘要處理完成，再開始提問。第一次處理時間依文件大小與模型服務而異。
3. 輸入問題，例如「用三句話總結這篇論文」、「作者用了哪些資料集？」或追問「其中哪一個結果最好？」。
4. 回答串流時先顯示暫定文字，成功結束後才定稿；引用編號可點擊查看右側來源。
5. 展開「回答過程」查看問題分流、檢索與 token 用量；模型思考內容放在預設收合的技術細節中。

`[C#]` 對應原文 Chunk；`[S#]` 對應摘要、頁碼範圍與涵蓋章節，並非逐句原文對照。不存在的引用編號會標記「未驗證」；沒有引用的句子目前不會自動標記。

系統一次保留一份活動 Document，追問只使用最近兩輪成功對話。重新啟動後，需重新上傳文件；相容的處理快取可重用，回答與對話歷史不快取。上傳期間請保持頁面開啟，重新整理後自動恢復上傳尚未驗證。

## 測試文件

下載固定版本 PDF（需要 bash、curl 與網路）：

```sh
bash scripts/fetch_data.sh
```

| 文件 | 固定版本 | 下載位置 |
|---|---|---|
| LightRAG 論文 | [2410.05779v3](https://arxiv.org/pdf/2410.05779v3) | `data/lightrag.pdf` |
| 工業機器人綜述，109 頁 | [2603.06749v1](https://arxiv.org/pdf/2603.06749v1) | `data/industrial-robotics.pdf` |

下載腳本會檢查 SHA-256；既有檔案不符時會報錯，不靜默覆寫。PDF 不隨 repository 提交。第二份文件用來檢查長文件與不同主題的泛化能力；不宣稱能證明雲端模型從未看過它。

## 資料夾與檔案用途

本 repository 同時保存「可執行網站」和「面試作業的開發、評估證據」。以下的「執行需要」指從完整 checkout 啟動網站，並不代表其他檔案可以從版本庫刪除。

| 路徑 | 功能 | 執行需要？ |
|---|---|---|
| `src/chat_document/` | Python 後端、文件處理、檢索、摘要、模型呼叫與問答流程 | 是 |
| `frontend/dist/` | 已編譯的網頁、CSS 與字型，FastAPI 直接提供 | 是；刻意提交的 build 產物 |
| `frontend/src/` | React/TypeScript 介面原始碼 | 執行已編譯版本不需；修改介面需要 |
| `frontend/src/fonts/` | Noto Serif TC 字型分片、CSS 與授權 | 重建前端需要；大量檔案是字型分片 |
| `frontend/package.json`、`package-lock.json`、`vite.config.ts`、`tsconfig.json`、`index.html` | 前端依賴、建置設定及入口 | 前端開發與 build 需要 |
| `frontend/scripts/` | 來源內容呈現的測試腳本 | 開發驗證用 |
| `frontend/review/` | 設計基準、瀏覽器驗證腳本與截圖證據 | 開發與交付證據 |
| `tests/unit/` | 評估判定、數字關聯等單元測試 | 開發驗證用 |
| `tests/integration/` | 上傳、檢索、摘要、HTTP、串流與失敗處理等整合測試 | 開發驗證用；部分需本地 embedding |
| `eval/` | Golden Facts、Judge、評估執行與報告產生程式 | 回答品質評估用 |
| `eval/reports/` | 原始評估結果、調參比較、通過率與失敗分析 | 交付證據，保留 |
| `scripts/` | 下載文件、同步事件型別、調參與量測工具 | 按需使用，見下表 |
| `spikes/`、`spikes/out/` | 早期 PDF、模型與 embedding 可行性實驗及原始輸出 | 歷史實驗證據，保留 |
| `docs/` | 詳細設計、開發指南、ADR、AI 協作紀錄與驗證證據 | 維護與交付文件 |
| `docs/qa/`、`docs/verification/` | 各階段驗證報告、測試輔助程式、截圖及事件紀錄 | 歷史驗證證據；不是正式伺服器入口 |
| `.scratch/chat-with-document/` | PRD、issues 與執行紀錄 | 已追蹤的需求與工作紀錄；不是可隨手清空的暫存 |
| `pyproject.toml`、`uv.lock` | Python 套件設定與鎖定依賴 | 是；`uv.lock` 用於可重現安裝 |
| `conftest.py` | 註冊 pytest 的評估選項與測試設定 | 測試用 |
| `AGENTS.md`、`CLAUDE.md` | Agent 工作限制與入口；CLAUDE 引用 AGENTS | AI 協作指引 |
| `CONTEXT.md` | Document、Chunk、Citation 等領域術語 | 維護用，避免用詞分歧 |
| `題目：讓 AI 跟文件對話（Chat with Document）.md`、`簡報素材.md` | 作業需求筆記與簡報素材 | 交付準備與背景證據 |
| `data/` | 自行下載的測試 PDF | 使用測試文件時需要；PDF 不提交 |
| `.cache/` | 文件解析、Chunk、向量與 Summary Tree 快取 | 自動建立；刪除會重跑文件處理 |
| `.venv/`、`frontend/node_modules/` | 本機安裝的 Python、前端依賴 | 可重新安裝；不隨 zip 交付 |
| `__pycache__/`、`.pytest_cache/`、`.ruff_cache/` | Python、pytest、ruff 的可再生快取 | 不隨 zip 交付 |
| `.lat/`、`.worktrees/` | 本機協作狀態與隔離工作區 | 不隨 zip 交付；清理前確認沒有未提交工作 |

### 後端主要檔案

| 檔案（位於 `src/chat_document/`） | 負責的功能 |
|---|---|
| `api.py` | FastAPI 路由、SSE 傳輸與前端靜態檔案 |
| `application.py`、`ingestion.py` | 活動 Document、上傳處理與背景工作生命週期 |
| `ask_graph.py` | LangGraph 提問流程：驗證 → 分流 → 準備證據 → 回答 → 定稿 |
| `pdf_parser.py`、`tables.py`、`chunker.py` | PDF 版面與 Section 解析、表格重建、按章節切 Chunk |
| `embedder.py`、`index.py` | 本地 embedding、dense/BM25 檢索、表格連結與相鄰 Chunk |
| `router.py`、`context_packer.py` | 問題分流、追問改寫、Sub-query、證據容量與分批抽取 |
| `summary_tree.py`、`summary_context.py`、`summary_selection.py` | 建立摘要樹、挑選放得下的完整摘要層、表格密集摘要的原文片段選取 |
| `answer_generator.py`、`citation.py` | 回答串流、長度失敗重試、引用編號驗證與來源對應 |
| `llm_adapter.py`、`llm_gateway.py`、`tokens.py` | 原生 Ollama 呼叫、共用 budget guard、token 計數；adapter 也含測試替身 |
| `models.py`、`events.py` | 領域資料模型與前後端共用事件契約 |
| `cache.py`、`policy.py`、`settings.py` | 文件處理快取、共用數值規則、可調參數 |
| `router_regression.py` | Router 回歸題庫，供測試與評估共用；正式提問流程不載入 |

### 前端主要檔案

| 檔案（位於 `frontend/src/`） | 負責的功能 |
|---|---|
| `main.tsx`、`App.tsx` | React 入口、頁面組合與上傳/對話狀態 |
| `DocumentPane.tsx`、`Composer.tsx`、`Shortcuts.tsx` | 文件操作、問題輸入與範例問題 |
| `Answer.tsx`、`SourcePane.tsx`、`SourceContent.tsx` | 回答 Markdown、可點 Citation、來源文字與表格 |
| `AnswerProcess.tsx` | 處理階段、檢索與模型 token Trace |
| `sse.ts`、`events.ts`、`models.ts` | 串流解析、由後端產生的事件型別及前端資料型別 |
| `Shared.tsx`、`styles.css` | 共用介面元件與版面樣式 |

### 工具腳本

| 檔案（位於 `scripts/`） | 功能 |
|---|---|
| `fetch_data.sh` | 下載固定版本 PDF 並驗證雜湊 |
| `generate_event_types.py` | 由後端事件模型產生或檢查 `frontend/src/events.ts` |
| `tune.py` | 檢索參數比較、回答比較與最終多次評估 |
| `measure_summary_concurrency.py` | 量測摘要呼叫的並行能力與延遲 |
| `measure_table_reading.py` | 量測表格閱讀與回答表現 |

**整理原則：** 可再生的安裝環境與快取不放進交付 zip；正式原始碼、前端 dist、測試與實驗證據保留。`frontend/src/` 與 `dist/` 分別是原始碼及可執行產物，不是應刪除的重複；`spikes/` 也不能直接當作死碼。若要精簡正式程式，應另外確認 import、入口與回歸覆蓋，再逐項調整。

## 評估結果與已知限制

- [修正版評估結論](eval/reports/issue11-correction/conclusions.md)：N=3 原始通過率、方法限制與失敗分析；先前 `issue11/` 報告仍保留為歷史。
- [LangGraph 整合驗證](docs/verification/ticket-14/integration.md)：該版本 335 項測試通過、3 項 live eval 未執行；這是當次整合證據，不是每次文件修改後重新跑的結果。
- [A9 診斷結果](docs/verification/ticket-13/d22/probe/final-report.md)：限制題仍可能拒答或漏答；本輪未修復。

目前仍可能漏掉重點、缺少逐論點引用、讀錯比較方向，或未完全遵循繁簡中文。Judge 與數字判定也可能誤判，原始分數和人工比對分開保存。混合字型標題與無法可靠重建的表格仍有解析限制，不能把「編號有效」等同「論點有完整根據」。

範圍為本機單文件、文字 PDF；不支援 OCR、Docker、雲端部署或對話歷史摘要。LangGraph 僅做提問編排，PDF 解析、切塊與檢索仍自行實作，未啟用 checkpoint persistence 或自主 agent loop。

## 繼續開發

- [開發指南](docs/development.md)：測試、前端 build、環境參數、評估與交付。
- [設計規格與實測依據](docs/design.md)：切塊、摘要、檢索、Citation、Context Budget 與重試規則。
- [LangGraph ADR](docs/adr/2026-10-14-langgraph-ask.md)：提問流程的責任邊界與遷移決策。
- [領域術語](CONTEXT.md)、[Agent 工作規則](AGENTS.md)。
