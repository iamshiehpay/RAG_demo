# 回答品質評估

這裡量測真實模型回答，與 `tests/` 的程式回歸分開。入口統一使用 pytest；需要本地 Ollama、bge-m3、雲端模型權限，以及 `bash scripts/fetch_data.sh` 下載的文件。

## 怎麼跑

```sh
# LightRAG 的 Q1–Q3，每題三次
uv run --frozen pytest eval -m eval -s --eval-cases Q1,Q2,Q3 --eval-repeats 3

# 第二份長文件：數字題與摘要題
uv run --frozen pytest eval -m eval -s --eval-cases SECOND_NUMBER,SECOND_SUMMARY --eval-repeats 3

# Router 的既有與泛化題
uv run --frozen pytest eval/test_router_live.py -m eval -s
```

不指定 `--eval-cases` 時，`pytest eval -m eval` 執行全部三個 live 入口。預設 `pytest` 只跑離線 unit；不會默默呼叫雲端。

| 選項 | 用途 |
|---|---|
| `--eval-cases` | 逗號分隔的 case ID；未知 ID 直接報錯 |
| `--eval-repeats` | 每題次數，預設 1 |
| `--eval-document` | 第一份評估 PDF 的替代路徑；第二文件入口仍使用固定版本 |
| `--eval-report` | 輸出報告路徑；同時跑多個入口時勿共用這個選項，以免覆寫 |
| `--eval-label` | 實驗名稱 |
| `--eval-record-only` | 功能失敗仍保存報告、不以 assert 阻止測量；報告中的 FAIL 不改判 |

新結果預設寫到已忽略的 `eval/reports/`，確認有保留價值後再挑選到 `eval/results/`。不要覆寫既有最終報告。

## 檔案分工

| 檔案 | 功能 |
|---|---|
| `golden_facts.py`、`second_document.py`、`router_cases.py` | 評估問題、Golden Facts 與 Router 回歸題 |
| `models.py`、`checks.py`、`router_checks.py` | 評分資料、Judge／逐字證據／數字關聯／繁簡檢查 |
| `runner.py` | 上傳、提問、評分及逐次 LLM Trace；共用 `run_evaluation()` |
| `report.py`、`provenance.py` | 報告格式與 Git 來源版本；zip 無 Git 時標 unknown |
| `test_live.py`、`test_second_document_live.py`、`test_router_live.py` | 三個明確選用的真實模型入口 |
| `pytest_plugin.py` | CLI 選項與案例篩選 |
| `tune.py` | 共用的檢索參數、回答 think 與最終評估比較 |
| `fakes.py` | 非產品用的劇本模型，供 tests 與受控檢索實驗使用 |
| `results/` | 精選最後測量及失敗分析；[先讀摘要](results/README.md) |

## 評分契約與限制

- `contains` 只查專有名詞，不能拿來檢查數字；統一連字號與空白後比對。
- `judge` 必須摘錄回答中實際存在的證據。數字另核對變體、資料集、指標、數值及關聯；無逐字證據不給分。
- `forbidden` 只將明確斷言錯誤結論判為失敗，否定或引用不算。固定拒答用確定性檢查，不呼叫 Judge。
- Router 只有 `plan_source=router` 才能通過；fallback Lookup 不算分類成功。追問須改寫並解決指涉。
- 只評估成功 FinalEvent，截斷的暫定內容不評分。token、延遲、重試與 Judge 呼叫都保留。
- 功能通過與 Golden Facts 品質分開報告。Judge 仍可能因非逐字摘錄或嚴格數字綁定而誤判；人工比對不覆寫原始分數。
- 成本題的確定性 anchors 仍要求 `610` 與 `API`；`610k`、`61萬` 或只寫「一次呼叫」可能被判失敗。

## 調參（按需）

```sh
uv run --frozen python -m eval.tune retrieval --output eval/reports/experiment
uv run --frozen python -m eval.tune retrieval-controlled --output eval/reports/experiment
uv run --frozen python -m eval.tune answers --output eval/reports/experiment
uv run --frozen python -m eval.tune final --output eval/reports/experiment
```

為每次實驗使用新的目錄；controlled 階段讀取同目錄 retrieval 階段記錄的 Router 計畫與相容的真實摘要快取。檢索重播的答案是替身，回傳結果排名不代表真實回答品質；answers／final 才呼叫真實模型。歷史並行量測與單次表格實驗已歸檔，不維護第二套入口。
