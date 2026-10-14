# AI 協作：決策、驗證與修正

本專案以 AI 協助設計、實作與審查，由人決定範圍、技術取捨及可接受的限制。以下挑選能追溯到程式或實測的案例；完整開發紀錄見 [AI log](ai-log.md)，架構決策見 [LangGraph ADR](adr/2026-10-14-langgraph-ask.md)。

## 三個值得先看的案例

| 問題 | 人與 AI 如何協作 | 最後採取的做法 | 可核對的證據 |
|---|---|---|---|
| 10K 限制不能只靠模型參數 | AI 建議用 Ollama `num_ctx` 限制容量；實測發現雲端會忽略它，而且 thinking 也會占輸出額度 | 所有文字生成呼叫統一經過 budget guard；把思考與回答一起預留，超額立即拒絕 | [當時的觀測與條件](design.md#早期實測與設計依據)、[guard 實作](../src/chat_document/llm_gateway.py)、[邊界測試](../tests/unit/test_budget.py) |
| 測試替身讓 Router 看起來比真實模型可靠 | 劇本模型固定回傳合格 JSON，但真實模型沒有照 schema 回覆；保留逐字模型輸出，補回歸並修正提示與解析 | 區分真正 Router 計畫與 fallback，不把 fallback 的 Lookup 算成分類成功；另外保留真實模型評估入口 | [逐字回應 fixture](../tests/data/router_qa_raw.json)、[解析回歸](../tests/unit/test_router_parsing.py)、[live 評估入口](../eval/test_router_live.py) |
| 引入 LangGraph 仍須維持原有行為 | 人要求限制在提問流程；獨立審查發現上傳替換時可能混用舊文件與新就緒狀態 | 同一時點捕捉請求狀態；加入取消、串流與文件替換測試後整合，保留原模型、檢索和 prompt | [ADR](adr/2026-10-14-langgraph-ask.md)、[整合證據](verification/ticket-14/integration.md)、[生命週期測試](../tests/integration/test_ask_stream_lifecycle.py) |

這三個案例分別呈現「AI 的建議被實測推翻」、「測試方法本身被修正」和「審查找到遷移回歸」，比列出使用了哪些模型更能說明協作方式。

## 失敗與未完成事項也保留

- 最終多次回答評估並非全數通過；[評估結論](../eval/reports/issue11-correction/conclusions.md) 保留 Golden Facts 原始分數、Judge 限制和人工比對。
- A9 的限制題經七次有界診斷仍未解決，人決定凍結為已知缺陷；沒有把「某次有回答」當成問題已修復。[診斷報告](verification/ticket-13/d22/probe/final-report.md)
- LangGraph 當次整合的 335 PASS 是該版本的功能測試結果，不代表回答品質全面正確，也不是未執行的人工 QA 已通過。

## 版本追溯

| 提交 | 可查看的變更 |
|---|---|
| `d455f50` | 將提問編排改為 request-scoped LangGraph |
| `24fba26` | 修正替換文件時的請求開始狀態，補回歸 |
| `a5b70a0` | 核准範圍、ADR 與整合檢查點 |
| `52e18c9` | 保存整合驗證與本機部署紀錄 |

完整 Git repository 可用 `git show <commit>` 查閱差異。程式交付 zip 另附 `CHANGELOG.txt`（commit、時間與訊息）及 `RELEASE.json`（交付版本與逐檔 SHA-256）；zip 不含 `.git`，需要完整 diff 時使用 repository。

本次交付整理另有 [驗證摘要](verification/release-refactor.md)，記錄測試保留、分層與打包檢查。

## 交付閱讀順序

1. [README](../README.md)：啟動、使用方式與檔案責任。
2. 本頁：人如何作決策、AI 如何協助，以及如何驗證。
3. 上表連結的幾份證據；只有需要追查時，再看完整 AI log 與歷史紀錄。

`chat-with-document.zip` 已包含這條閱讀路徑及其 Markdown 連結到的檔案。`chat-with-document-evidence.zip` 保存其餘歷史實驗、截圖與原始輸出；需要深入核對時，將兩個 zip 解壓到同一個父目錄即可合併為完整資料夾。歷史報告中的行內路徑可能只存在於證據包，並保留當時的檔案名稱與版本，不改寫成目前狀態。
