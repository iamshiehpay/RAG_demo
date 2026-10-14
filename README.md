# Chat with Document｜與 PDF 對話

本機執行的文件問答網站：上傳一份 PDF，使用中文或英文提問，點擊回答中的 Citation 查看來源章節與頁碼，並透過 Trace 檢查檢索結果、模型呼叫與 token 用量。

支援有文字層的 PDF、串流回答和多輪追問。全文問題使用上傳時建立的 Summary Tree；細節與比較問題檢索原文 Chunk。每次 LLM 呼叫的 prompt、思考與回答合計限制在 **10,000 tokens**。

> 功能與回答品質分開驗證：網站可正常操作，不代表所有回答都完整或正確；已知失敗與實測結果保留在評估報告中。

先依本頁啟動網站，再閱讀 [AI 協作摘要](docs/ai-collaboration.md) 與 [評估結果](eval/results/README.md)。主分支只保留持續使用的程式、測試與文件；完整開發歷史由 [Git 歸檔標籤](docs/history.md) 保存。

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
.venv/bin/python -m uvicorn app.api:create_app --factory --host 127.0.0.1 --port 8101
```

開啟 **http://127.0.0.1:8101**。Windows 請把 `.venv/bin/python` 換成 `.venv\Scripts\python.exe`。

若已安裝 [uv](https://docs.astral.sh/uv/)，可改用鎖定依賴的啟動方式：

```sh
uv run --frozen --no-dev uvicorn app.api:create_app --factory --host 127.0.0.1 --port 8101
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

## 資料儲存

目前不需要另外安裝資料庫。活動 Document、檢索索引與對話歷史放在記憶體；文件處理結果以 JSON 存在 `.cache/`，供相容版本重用。重啟後不會保留活動對話。若未來需要對話歷史永久保存、多文件管理或多使用者權限，再評估加入資料庫。

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

| 路徑 | 用途 |
|---|---|
| `app/` | 正式 Python 程式；API、上傳、PDF 處理、檢索、摘要與問答 |
| `frontend/src/` | React/TypeScript 介面與 Noto Serif TC Regular 字型 |
| `frontend/dist/` | 已編譯網頁與字型；刻意提交，讓執行者不必安裝 Node.js |
| `frontend/scripts/` | 來源文字與表格呈現測試；前端設定位於 `frontend/` 根目錄 |
| `tests/unit/`、`tests/integration/` | 離線邏輯測試、需本地 embedding 的整合測試 |
| `tests/support.py`、`tests/data/` | 共用合成 PDF、測試 helper 與必要回歸 fixture |
| `eval/` | Golden Facts、Judge、真實模型評估、調參；[執行方式](eval/README.md) |
| `eval/results/` | 精選最終評估，含原始回答、事件與逐項分數 |
| `scripts/` | `fetch_data.sh` 下載 PDF；`generate_event_types.py` 同步前後端事件型別 |
| `docs/` | 設計、開發指南、AI 協作、架構決策與歷史查詢方式 |
| `pyproject.toml`、`uv.lock` | Python 套件、測試設定與鎖定依賴 |
| `conftest.py` | pytest 分層標記與評估選項註冊 |
| `AGENTS.md`、`CLAUDE.md`、`CONTEXT.md` | Agent 工作規則、共用入口與領域術語 |
| `data/`、`.cache/` | 下載的 PDF、處理快取；不提交 |
| `.venv/`、`frontend/node_modules/` | 本機依賴；不提交 |

後端各模組的責任與兩條執行路徑見 [程式導覽](docs/development.md#程式導覽)。原始碼與前端 build 都需要保留；本地字型保留動態文件內容需要的字元。過時的 issue、spikes、中間報告與截圖已移至 Git 歷史，不另建立 archive 目錄。

## 評估結果與已知限制

[最終評估摘要](eval/results/README.md) 保留 N=3 的原始通過率、回答錯誤與 Judge 限制；這些是當時版本的測量，本次結構重構沒有重新評分。功能回歸另見 [驗證摘要](docs/validation.md)。

目前仍可能漏答、缺少逐論點引用、讀錯比較方向或未完全遵循繁簡中文。A9 限制題的拒答／漏答仍列為已知缺陷。Judge 也可能誤判；不能把「引用編號有效」等同「論點有完整根據」。

範圍為本機單文件、文字 PDF，不支援 OCR、多使用者或對話歷史持久化。LangGraph 僅做提問編排，PDF 解析、切塊與檢索自行實作，未啟用 checkpoint persistence。

## 繼續開發

- [開發指南](docs/development.md)：測試、前端 build、環境參數、評估與交付。
- [設計規格與實測依據](docs/design.md)：切塊、摘要、檢索、Citation、Context Budget 與重試規則。
- [LangGraph ADR](docs/adr/2026-10-14-langgraph-ask.md)：提問流程的責任邊界與遷移決策。
- [AI 協作摘要](docs/ai-collaboration.md)、[領域術語](CONTEXT.md)、[Agent 工作規則](AGENTS.md)。
