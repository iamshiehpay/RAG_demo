# 開發、驗證與交付

網站安裝與操作見 [README](../README.md)；功能規格見 [設計文件](design.md)。以下命令都從 repository 根目錄執行。僅執行網站不需要安裝前端工具或開發依賴。

## Python 測試

```sh
uv sync --frozen
uv run --frozen pytest
```

預設只收集 `tests/unit/`，不需要 Ollama 或雲端模型。測試會在本機建立合成 PDF、使用模型與 embedding 替身；這些結果驗證程式契約，不代表真實模型回答品質。

| 要驗證的內容 | 命令 | 前置條件 |
|---|---|---|
| 快速邏輯與替身測試 | `uv run --frozen pytest` | Python 開發依賴；打包測試另外使用 Git |
| 真實本地 embedding 與模組整合 | `uv run --frozen pytest tests/integration` | Ollama 執行中，已下載 bge-m3；部分測試需先執行 `bash scripts/fetch_data.sh` |
| 完整非雲端回歸 | `uv run --frozen pytest tests eval` | 同整合測試；預設排除 eval marker |
| 雲端回答品質 | `uv run --frozen pytest eval -m eval` | 另需雲端模型權限；見下方評估說明 |

`unit`、`integration` 標記由根目錄 `conftest.py` 依位置加入；雲端入口保留 `eval` marker。沒有把外部服務換成替身後，宣称真實服務驗證通過。

測試依功能命名：`test_router_synthesis.py` 收納分流/抽取/追問；`test_ingestion.py` 與 `test_document_layout.py` 區分真實 embedding 路徑及合成版面回歸；`test_summary_tree.py`、`test_summary_limits.py` 與 `test_summaries.py` 分別涵蓋摘要樹、容量/失敗邊界、離線來源契約。先前 review/issue 編號的檔案已依責任合併，不刪除回歸斷言。

共用合成 PDF 與模型替身放在 `tests/support.py`；需要真實服務的 helper 放在 `tests/integration/support.py`。測試檔不互相 import；Router live 檢查函式放在 `eval/router_checks.py`，不為取得 helper 而載入 live test module。

不使用 uv 時，先按 README 建立環境，再於該環境安裝 `pytest pytest-asyncio opencc ruff`；這條替代路徑不提供與 `uv.lock` 相同的鎖定保證。

只改文件時核對連結、命令與現行行為即可；修改測試結構時，比較案例收集清單並跑完整非雲端回歸，避免因搬檔而漏跑。功能驗證與模型回答品質分開報告。

## 前端開發

需要 Node.js 20.19 以上；正式網站仍由 FastAPI 提供已編譯資產。

```sh
npm ci --prefix frontend
npm run dev --prefix frontend
npm run typecheck --prefix frontend
npm run test:source --prefix frontend
npm run build --prefix frontend
PYTHONPATH=src:. uv run --frozen python scripts/generate_event_types.py --check
```

Vite 使用 5101，將 `/api` 代理至 8101。前端修改後必須重新 build 並提交 `frontend/dist/`。`src/chat_document/events.py` 是 SSE 型別來源；變更契約後先執行 `generate_event_types.py`（不帶 `--check`）更新 `frontend/src/events.ts`，再核對前後端。

保留已選定的紙張/襯線字體/Citation 側欄設計。設計原始基準見 [DESIGN](../frontend/review/DESIGN.md)，後續使用者核准的調整以現行介面與驗證紀錄為準。

## 可調參數

HTTP factory、Application 與 eval 讀取同一套 `RetrievalSettings`；也可明確注入設定。預設值實作於 [policy.py](../src/chat_document/policy.py)、[settings.py](../src/chat_document/settings.py) 與 [llm_gateway.py](../src/chat_document/llm_gateway.py)。

| 環境變數 | 預設值與用途 |
|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434`，Ollama 位址 |
| `CHUNK_TOKEN_TARGET` | 500，同 Section 的段落切塊目標 |
| `LOOKUP_TOP_K` | 5，Lookup 主要命中數 |
| `SYNTHESIS_TOP_K`、`SUB_QUERY_TOP_K` | 3、2，主問題與各 Sub-query 命中數 |
| `BM25_WEIGHT` | 0，預設 dense；0–1 為 BM25 的加權 RRF 比重 |
| `ANSWER_THINK` | `medium`；可用 `low`，輸出預留維持 3,000 |
| `SUMMARY_CONCURRENCY` | 4，上傳摘要並行呼叫數，須為正整數 |

BM25 使用基本 Unicode 詞彙斷詞；中文問題缺少英文詞彙重疊時保留 dense 排名。Trace 區分 cosine 與加權 RRF 分數，不把兩者當成同尺度。

## 回答品質評估

下列命令會呼叫真實雲端 LLM/Judge；需 Ollama 登入、雲端模型權限、本地 embedding 與已下載 PDF。

```sh
PYTHONPATH=src:. uv run --frozen pytest eval -m eval -s --eval-cases Q1,Q2,Q3 --eval-repeats 3
PYTHONPATH=src:. uv run --frozen pytest eval -m eval -s --eval-cases SECOND_NUMBER,SECOND_SUMMARY --eval-repeats 3
```

`--eval-cases` 用來排除不相關的 live 案例；Router smoke 另見 `eval/test_router_live.py`。評分方式、CLI 選項和逐字證據檢查見 [eval 說明](../eval/README.md)。目前案例定義在 `eval/golden_facts.py`、`eval/second_document.py`，不要在設計文件維護第二份可執行題庫。

調參工具：

```sh
PYTHONPATH=src:. uv run --frozen python -m scripts.tune retrieval --output eval/reports/my-retrieval-run
PYTHONPATH=src:. uv run --frozen python -m scripts.tune retrieval-controlled --output eval/reports/my-retrieval-run
PYTHONPATH=src:. uv run --frozen python -m scripts.tune answers --output eval/reports/my-answer-run
PYTHONPATH=src:. uv run --frozen python -m scripts.measure_summary_concurrency --output eval/reports/my-concurrency-run.json
PYTHONPATH=src:. uv run --frozen python -m scripts.tune final --output eval/reports/my-final-run
```

為新實驗使用新的輸出位置，保留既有報告。執行 `final` 前，確認設定與正式環境一致。受控檢索比較重播已記錄的真實 Router plan，以真實 Chunk/向量/embedding 搭配非評估回答的替身；回傳結果排名指標不是完整索引 MRR，也不是原生回答品質證明。正式回答評估仍呼叫真實模型。

交付評估每題 N=3，列出每條 fact 通過率、失敗原因、token、延遲及截斷嘗試。品質失敗如實列為已知缺陷，不改成 PASS；功能失敗亦須明確保留。早期實驗曾有時間上限，那是當次開發決策，不代表未來每次重跑自動取得相同時間或模型額度。

## 證據與快取

- [issue11-correction 結論](../eval/reports/issue11-correction/conclusions.md) 是修正版 N=3 評估與方法限制入口；`issue11/` 是先前測量，不能覆寫或混稱同一次實驗。
- 該批最終評估完成 27 次真實回答，功能通過、原始 Golden Facts 未全通過；九次無答案題固定拒答檢查通過。第二文件數字來源 Citation 修正後 N=3 為 3/3，數字與摘要 Golden Facts 仍各 1/3；不能宣稱全面 grounding 已解決。
- [A9 診斷](verification/ticket-13/d22/probe/final-report.md) 保留限制題的失敗觀察；目前凍結為已知缺陷。
- [LangGraph 整合紀錄](verification/ticket-14/integration.md) 記錄該版本 335 PASS、3 eval deselected、0 skip；其中人工驗證的未執行情境不算 PASS。
- `.cache/` 只保存上傳處理結果：Document、Chunk、embedding、Summary Tree；不保存回答或對話歷史。鍵值包含 PDF 雜湊、來源導出的 pipeline 版本、模型與有效切塊設定。
- 舊報告中的 `cache-manifest.json` 只證明當時的快取命中。後續來源或處理設定改變可能讓它失效，不保證目前重新上傳是零模型呼叫；demo 前保留且確認相容快取。

## 交付

完整 repository 保留歷史；交付包將日常程式與大量原始證據分開。先完成提交，再執行：

```sh
python3 scripts/package_release.py --output dist/release-$(git rev-parse --short HEAD)
```

此命令只讀 **Git HEAD** 的檔案內容，不包含未提交或未追蹤資料；輸出目錄必須不存在，避免覆寫前一次交付。產生：

- `chat-with-document.zip`：可執行網站、原始碼、測試、文件及 [AI 協作摘要](ai-collaboration.md) 連到的精選證據。
- `chat-with-document-evidence.zip`：剩餘歷史實驗與 QA 證據；與程式包不重複覆寫檔案，兩包可解壓到同一父目錄。

每包附版本與逐檔 SHA-256，程式包另附 commit 紀錄。精選文件的本地 Markdown 連結會一併收錄；歷史報告的行內路徑仍可能指向補充證據包。zip 不附 Git 資料庫；需要逐次 diff 時查看完整 repository。

打包不會寄信、上傳或邀請任何人。

保留原始碼、鎖定依賴、`frontend/dist/`、測試、`spikes/`（含輸出）、`eval/reports/`、題目筆記與協作證據。完整用途見 [README](../README.md#資料夾與檔案用途)。不包含公司內部 PDF、下載的 arXiv PDF、`.venv/`、`node_modules/`、本機快取與隔離工作區。

repo 的 `.gitignore` 已排除多數本機資料；打包前仍要核對是否含私密或未追蹤資料。`.scratch/` 的規格與 issue 是已追蹤證據，不能因名稱像暫存就清空。清理 `.worktrees/` 或其他工作目錄前，先確認未提交變更與使用狀態；本文件不提供整批刪除命令。
