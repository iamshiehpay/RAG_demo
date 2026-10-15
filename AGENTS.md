# AGENTS.md

本機 Chat-with-Document 網站：上傳一份有文字層的 PDF，以文件內容回答並提供 Citation 與 Trace。使用與安裝見 [README](README.md)；領域用語以 [CONTEXT.md](CONTEXT.md) 為準。

## 不可破壞的限制

- LLM 只做 text→text。PDF 解析、切塊、檢索自行實作，不用 LangChain、LlamaIndex 或 LightRAG 套件替代。LangGraph 僅編排提問流程，沿用原生 Ollama `/api/chat` 與同一 LLMGateway；不引入框架 loader、retriever、LLM wrapper。執行路徑見 [開發指南](docs/development.md#程式導覽)；本機若有 `docs/adr/2026-10-14-langgraph-ask.md`，可查閱遷移決策。
- 每次 LLM 呼叫都經 budget guard：prompt 估算 + 300-token 安全邊際 + 輸出預留 ≤ 10,000。思考也算輸出；超額 raise，由上游安排容量，不靜默截斷。不使用 `think="high"`。
- 回答應逐論點附 Citation（Section、頁碼）；文件無答案時按提問語言固定拒答，中文為「文件中未提及」。引用不存在的編號須標「未驗證」；沒有附引用的句子目前不自動標記，不能宣稱已全面驗證。
- 串流文字成功結束前是暫定；`done_reason=length` 視為失敗，回答以 low 重試一次並取代暫定文字，再失敗不得保留截斷答案。
- 保持單文件、本機、文字 PDF 範圍。多輪僅改寫追問；不擴充 OCR、Docker、Graph RAG、雲端部署或對話歷史摘要。
- 不把測試文件名稱、Golden Facts 數字或回歸題標籤寫進產品 prompt。評估失敗如實記錄，不能靠改標籤當成通過。

## 依任務讀取

不要每次載入全部歷史報告；開始修改對應功能前，讀下列相關段落。

| 任務 | 必讀來源 |
|---|---|
| 修改解析、表格、切塊、摘要、檢索、引用、budget、重試或快取 | [設計規格](docs/design.md) 的對應章節；數值實作見 `policy.py`、`settings.py`、`llm_gateway.py` |
| 修改提問編排、取消與串流生命週期 | [程式導覽](docs/development.md#程式導覽) 及 `tests/integration/test_ask_stream_lifecycle.py` |
| 修改前端 | 先載入 `web-design-engineer` skill，再讀 [設計基準](docs/frontend.md) 與 [前端開發](docs/development.md#前端開發)；修改後 build 並提交 `frontend/dist/` |
| 修改測試、prompt 或評估 | [開發與評估指南](docs/development.md)、[eval 說明](eval/README.md)；Golden Facts 以 `eval/golden_facts.py`、`eval/second_document.py` 為準 |
| 準備交付或清理檔案 | [README 的檔案用途與保留原則](README.md#資料夾與檔案用途)、[交付](docs/development.md#交付) |
| 術語、架構決策或歷史證據 | [CONTEXT.md](CONTEXT.md)、`docs/adr/`、[歷史索引](docs/history.md) |

## 修改與驗證

- 新增或修正模組先寫會失敗的測試，再實作到通過；文件修改只驗證連結、命令及敘述一致性。
- 測試與啟動指令見 [開發指南](docs/development.md)。預設 pytest 只跑 tests/unit，不需 Ollama；tests/integration 使用本地 bge-m3，eval 的雲端評估明確指定後另跑。測試重構須核對案例數與完整非雲端回歸。
- 涉及模型輸出格式的功能，除替身測試外，至少用真實 gpt-oss 做一次最小 smoke；泛化題不得出自既有測試集。
- 送審時逐項說明相關風險與驗證：模型替身是否掩蓋真實行為、prompt 是否教到測試題、中文斷句與數字、雙欄/圖標籤/caption/框內標題、共用檔案及快取版本。無關項目註明不適用。
- rebase 或整合共用程式後，重跑受影響的其他模組測試；快取版本必須涵蓋處理流程變更。
- 設計決策寫入 [設計規格](docs/design.md)，難逆轉的架構決策寫 `docs/adr/`；不要再把完整規格或實驗數據堆回本檔。
- AI 建議被實測推翻、AI 錯誤被修正或使用者改變方向時，追加 `docs/ai-log.md`；里程碑完成後 commit。

## 驗證紀錄偏好

驗證要充分，產物要精選；位置與保留方式以 [開發指南](docs/development.md#驗證產物放哪裡) 為準。

- 一般測試輸出留在終端或 CI；需要暫存時使用忽略目錄，不為每輪修正新增報告。
- 新發現的 bug 優先補進既有正式測試；一次性診斷腳本完成任務後清理，已提交的舊版由 Git 歷史保存。
- 實驗原始輸出預設忽略，只挑選最終結果與重要失敗納入版本庫。
- 同一結果只保留一份來源；issue、審查與交付摘要使用連結。AI log 只記重要決策、AI 錯誤與修正原因，連到 commit 或測試。
- 每個里程碑結束前，清理本輪暫存與已被取代的產物並修正連結；保留需求、tickets、決策與重要失敗證據。完成結論更新既有驗證摘要，舊版交給 Git。

## 保留與交付

- 主分支保留 `app/`、`frontend/dist/`、必要測試、`eval/results/`、`.scratch/` 規劃與工作項目，AGENTS.md、CONTEXT.md，以及 docs 的設計、指南、完整 AI log 與精選成果。LangGraph ADR 與 AI 協作摘要僅保留本機。使用者於 2026-10-14 核准將 `docs/verification/`、`docs/qa/` 逐輪產物移出工作目錄；完整歷史由 [歸檔標籤](docs/history.md) 保存。新驗證產物按上方規則處理。
- 新實驗輸出寫入已忽略的 `eval/reports/`；只將有持續價值的最終證據納入版本庫。
- 不提交公司內部 PDF、`data/*.pdf`、安裝環境與快取。測試 PDF 用 `scripts/fetch_data.sh` 下載固定版本。
- 用私人 repository 與 zip 交付；邀請協作者、寄信等外部動作仍依使用者授權執行。
