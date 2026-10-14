# 精簡交付與測試重構驗證

基準：`1960fba`。本輪由主對話自行完成，未委派 agent、未做獨立 agent Review。正式 `src/`、`frontend/` 與 `uv.lock` 與基準相同；只調整測試配置、測試組織、離線評估 helper、打包工具及文件。

## 測試保留與分類

- 重構前：236 個 test function；335 個非雲端參數化案例，另有 3 個 live 評估入口。
- 每個原有 test function 都仍存在，逐一比較 `assert` AST 全部相同；原有斷言未刪除。`test_eval_case_selection_does_not_collect_unrequested_live_workloads` 的子程序增加 `eval` 目錄參數，以符合新的預設收集範圍，原斷言不變。
- 新增 4 個打包測試並完成解壓驗證修正後：120 unit、219 integration、3 live eval。`tests/` 下 test 檔案由 32 個變成 30 個，其中 1 個 live 入口移到 `eval/`；並非靠大量刪測試減少檔案。
- 共用 PDF／替身 helper 移至 `tests/support.py`，真實 embedding helper 移至 `tests/integration/support.py`；已確認 test module 不再互相 import。

| 舊位置 | 現在位置 |
|---|---|
| `test_router_review.py` | 合併到 `tests/integration/test_router_synthesis.py` |
| `test_review_regressions.py` | 依行為分到 ingestion、failure_handling、unit/budget |
| `test_issue10_review_corrections.py`、`test_second_document.py` | 依行為分到 unit/document_layout、unit/summaries |
| `test_summary_corrections.py` | `tests/integration/test_summary_limits.py` |
| `test_summary_selection.py` | `tests/unit/test_summaries.py` |
| `test_router_live_qa.py`、`test_router_smoke_checks.py` | unit/router_parsing、unit/router_checks |
| `test_router_smoke_eval.py` | `eval/test_router_live.py`，helper 抽到 `eval/router_checks.py` |
| question_language、eval_allowed_routes、event_types | 移至 unit，檢查行為不變 |

歷史報告保留舊名稱與當時版本；上表是導覽，不把舊報告改寫成新測量。

## 執行結果

- `pytest --collect-only`：最初 121 個 unit；解壓驗證發現一個依賴下載 PDF 的案例，移至整合層後為 120。
- `pytest tests/integration -m integration --collect-only`：最初 218 個，PDF 回歸移入後為 219。
- `pytest eval -m eval --collect-only`：3 個 live 入口，只有收集、沒有模型呼叫。
- `pytest`：初版 121 PASS（8.14 秒）；最後重新分類後 120 PASS、0 SKIP（3.08 秒）。均有 5 個既有 PyMuPDF deprecation warnings。
- 完整非雲端回歸：339 PASS、3 eval deselected、0 skip，287.18 秒；5 個既有 PyMuPDF warnings。此結果在最後的 PDF 案例歸類及 fixture 抽取前，該項修正另行執行原案例得到 1 PASS（3.81 秒），並重跑預設測試。
- Ruff：通過；本輪新增／修改的測試、打包工具與 helper 全部檢查。
- 現役文件本地連結與錨點：66 個通過；後續報告連結另檢查。

第一次完整執行在沙箱內得到 203 FAIL／136 PASS，最小合成 PDF 路徑確認在 embedding 連線階段失敗。沙箱外 `/api/tags` 確認本地 bge-m3 可用，改在可連線環境重跑；沒有把這批失敗算成驗證通過。

## 打包工具的 RED/GREEN

新功能先提供未實作 stub：4 個行為測試全部失敗，再實作到 4 PASS。另補「兩個 zip 沒有重複路徑」斷言，初版因共用 RELEASE.json 明確失敗（1 FAIL／3 PASS），修正為 EVIDENCE-RELEASE.json 後 4 PASS。完整回歸後再補根目錄簡報素材須進入證據包的斷言，先得到 1 FAIL／3 PASS，再補明確的檔案白名單；此最後打包調整另跑針對性測試，不冒稱先前整套結果涵蓋它。

測試使用臨時 Git repo，確認只讀 HEAD 的 blob，不取未提交修改與未追蹤檔；排除 PDF、`.env`、cache、node_modules；保留可執行前端與測試；逐檔雜湊正確、相同版本輸出一致、不覆寫既有交付、不跟隨 symlink。打包過程不寄信、不上傳、不改寫 Git 歷史。

## 交付包檢查

初版 `9302a45` 交付包已實際建立與解壓：程式包 384 個檔案、10,507,219 bytes；補充證據包 1,567 個檔案、117,056,868 bytes。逐檔 SHA-256、兩包互不覆寫、排除私有/安裝資料、主要文件連結均通過；解壓後 API 確認載入解壓目錄，首頁與兩個引用的 JS/CSS 資產 HTTP 200 且位元組相同。沒有重新安裝依賴；此檢查使用既有 Python 環境與解壓後的原始碼。

初版解壓後預設測試為 120 PASS／1 SKIP。原因是被歸入 unit 的一個合成 embedding 測試其實仍讀取下載的 109 頁 PDF；不能把有替身直接等同於獨立於外部文件。已移到 integration，並把它從 971,862-byte 歷史模型輸出中讀取的 14 組決策，抽成 15,102-byte 固定 fixture，保留來源雜湊與原順序。此後整合回歸只需 pinned PDF 與程式包內的小 fixture，不再依賴補充證據包。原 test function 及斷言保留。

最終交付將重新從修正後 HEAD 建立；實際 zip 版本、檔案数與解壓檢查結果另附於交付目錄 `VERIFICATION.json`，避免用初版數值冒充最終產物。
