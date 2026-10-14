# 精簡交付與測試重構驗證

基準：`1960fba`。本輪由主對話自行完成，未委派 agent、未做獨立 agent Review。正式 `src/`、`frontend/` 與 `uv.lock` 與基準相同；只調整測試配置、測試組織、離線評估 helper、打包工具及文件。

## 測試保留與分類

- 重構前：236 個 test function；335 個非雲端參數化案例，另有 3 個 live 評估入口。
- 每個原有 test function 都仍存在，逐一比較 `assert` AST 全部相同；原有斷言未刪除。`test_eval_case_selection_does_not_collect_unrequested_live_workloads` 的子程序增加 `eval` 目錄參數，以符合新的預設收集範圍，原斷言不變。
- 新增 4 個打包測試後：121 unit、218 integration、3 live eval。`tests/` 下 test 檔案由 32 個變成 30 個，其中 1 個 live 入口移到 `eval/`；並非靠大量刪測試減少檔案。
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

- `pytest --collect-only`：121 個 unit。
- `pytest tests/integration -m integration --collect-only`：218 個 integration。
- `pytest eval -m eval --collect-only`：3 個 live 入口，只有收集、沒有模型呼叫。
- `pytest`：121 PASS，8.14 秒，5 個既有 PyMuPDF deprecation warnings。
- 完整非雲端回歸：339 PASS、3 eval deselected、0 skip，287.18 秒；5 個既有 PyMuPDF warnings。
- Ruff：通過；本輪新增／修改的測試、打包工具與 helper 全部檢查。
- 現役文件本地連結與錨點：66 個通過；後續報告連結另檢查。

第一次完整執行在沙箱內得到 203 FAIL／136 PASS，最小合成 PDF 路徑確認在 embedding 連線階段失敗。沙箱外 `/api/tags` 確認本地 bge-m3 可用，改在可連線環境重跑；沒有把這批失敗算成驗證通過。

## 打包工具的 RED/GREEN

新功能先提供未實作 stub：4 個行為測試全部失敗，再實作到 4 PASS。另補「兩個 zip 沒有重複路徑」斷言，初版因共用 RELEASE.json 明確失敗（1 FAIL／3 PASS），修正為 EVIDENCE-RELEASE.json 後 4 PASS。完整回歸後再補根目錄簡報素材須進入證據包的斷言，先得到 1 FAIL／3 PASS，再補明確的檔案白名單；此最後打包調整另跑針對性測試，不冒稱先前整套結果涵蓋它。

測試使用臨時 Git repo，確認只讀 HEAD 的 blob，不取未提交修改與未追蹤檔；排除 PDF、`.env`、cache、node_modules；保留可執行前端與測試；逐檔雜湊正確、相同版本輸出一致、不覆寫既有交付、不跟隨 symlink。打包過程不寄信、不上傳、不改寫 Git 歷史。

## 交付包檢查

實際交付包在提交後從 HEAD 建立，再解壓驗證；完成結果待補。
