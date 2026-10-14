# AGENTS.md

本機 Chat-with-Document 網站：上傳一份有文字層的 PDF，以文件內容回答並提供 Citation 與 Trace。使用與安裝見 [README](README.md)；領域用語以 [CONTEXT.md](CONTEXT.md) 為準。

## 不可破壞的限制

- LLM 只做 text→text。PDF 解析、切塊、檢索自行實作，不用 LangChain、LlamaIndex 或 LightRAG 套件替代。LangGraph 僅編排提問流程，沿用原生 Ollama `/api/chat` 與同一 LLMGateway；不引入框架 loader、retriever、LLM wrapper。詳見 [ADR](docs/adr/2026-10-14-langgraph-ask.md)。
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
| 修改提問編排、取消與串流生命週期 | [LangGraph ADR](docs/adr/2026-10-14-langgraph-ask.md) 及 `tests/integration/test_ask_stream_lifecycle.py` |
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

驗證產物依 [放置與保留規則](docs/development.md#驗證產物放哪裡) 處理：暫存輸出不提交；回歸案例進 tests，精選模型評估進 eval/results，完成結論更新 docs/validation.md。不要為每輪驗證新增報告目錄。

## 保留與交付

- 使用者於 2026-10-14 核准精簡主分支：正式程式位於 `app/`；保留 `frontend/dist/`、必要測試、`eval/results/` 最終報告及精選 AI 協作證據。歷史 issue、spikes、逐輪驗證已存入 [歸檔標籤](docs/history.md)，不重建 archive 目錄。
- 新實驗輸出寫入已忽略的 `eval/reports/`；只將有持續價值的最終證據納入版本庫。
- 不提交公司內部 PDF、`data/*.pdf`、安裝環境與快取。測試 PDF 用 `scripts/fetch_data.sh` 下載固定版本。
- 用私人 repository 與 zip 交付；邀請協作者、寄信等外部動作仍依使用者授權執行。
