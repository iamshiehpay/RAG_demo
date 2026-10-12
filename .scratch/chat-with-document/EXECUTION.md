# 執行清單（LAT）

Status: in-progress

依據：`PRD.md`（ready-for-agent）、`issues/01`～`11`、`AGENTS.md`（數值的唯一來源）、`CONTEXT.md`（術語）。
需求與 Spec 已由使用者確認，本輪略過討論與重寫 Spec，只依既有 issues 推進。

## 分工

| 角色 | 設定 |
|---|---|
| Orchestrator | Claude Opus 5.5 high（HCOM 名稱 `levi`） |
| Implementer | Codex `gpt-6.1-sol`、`model_reasoning_effort=high`，透過 HCOM；每票新 context，依 /implement |
| Reviewer | Claude 原生 subagent `claude-opus-5-5` high，每票新 context，依 /code-review；內部再委派同為 Opus 5.5 high |
| QA | Claude 原生 subagent Sonnet 5.5 high；複雜情境用 Opus 5.5 high |

整合分支：`main`。每票在 `.worktrees/<NN>-<slug>/`、分支 `lat/<NN>-<slug>` 開發；合併前 rebase 到最新 `main`，以 `--ff-only` 合併。

## 逐票狀態

| # | 票 | 依賴 | 波次 | 預計修改範圍（衝突協調） | 狀態 |
|---|---|---|---|---|---|
| 01 | Walking skeleton | — | W1 | 建立整個骨架（後端、前端、測試、README） | done（9ba4327；Review APPROVE；QA 7/7 PASS）|
| 02 | 依結構解析與切塊 | 01 | W2 | Parser、Chunker、ingest 測試；前端只動 Citation 旁註文字 | merged 3a15958；QA 6/6 AC PASS，但 CJK 長段落斷句 FAIL → 修正中 |
| 06 | Router 與 Synthesis | 01 | W2 | Router、Context Packer、提問流程；前端 Trace 的 plan 與階段指示 | done（5799106；Review APPROVE；QA PASS，AC7 報告隨 #08）|
| 08 | Eval harness | 01 | W2 | `eval/`、pytest marker 設定 | done（11968fd；Review APPROVE；QA 0 FAIL）|
| 09 | Tufte 設計（需人確認初稿） | 01 | W2 初稿 → 使用者確認 → 定稿 | `frontend/`（樣式與共用元件） | dispatched 初稿（levi-t09-dune）|
| 04 | 上傳進度與快取 | 01（實際排在 02 之後：共用 ingest 流程） | W3 | Ingestion Jobs、快取、上傳 API、前端上傳進度 | dispatched（levi-t04-kano）|
| 03 | 表格重建（Q3） | 02（實際排在 06 之後：共用 Context Packer） | W3 | Parser 表格、Table Chunk 連結、Lookup 檢索、Citation 彈窗表格 | dispatched（levi-t03-mulo）|
| 07 | 失敗處理與串流狀態 | 01（實際排在 06 之後：共用提問流程） | W3 | Gateway 重試、Citation Validator、錯誤事件、前端暫定／重試／錯誤狀態 | done（9538b88；Review APPROVE；QA 16 PASS）|
| 05 | Summary Tree 與 Global（Q1） | 02、04、06 | W4 | Summary Tree Builder、Global 路徑、文件概覽、`[S#]` | todo |
| 10 | 第二份文件 | 03、05、08 | W5 | 下載腳本、Golden Facts、泛化修正、ai-log | todo |
| 11 | 調參與最終驗收 | 全部 | W6 | eval 實驗、AGENTS.md 設定、README、最終 build | todo |

共用檔案依序修改：同一波內，後合併的票先 rebase 到已整合的 `main` 再送最終審查。

## 每票完成條件

實作 + 必要測試 → Claude Reviewer（/code-review）→ GPT 修正 → 複查 → rebase 並合併到 `main` → 在整合後版本跑驗收條件 → QA 驗證（UI 用真實瀏覽器並保存證據）→ 更新本表與 issue 的 `Status:` → 收尾 Agent 與 worktree。

驗收逐項標記 `PASS`／`FAIL`／`UNPROVEN`／`NOT_EXECUTED`，附證據。

## 待使用者決策

- #09 初稿方向確認（issue 明定需要人參與），初稿完成後提出，紀錄於 `.lat/decisions/`。

## QA 草稿缺口的歸屬（`test-list.md` 附錄）

已確認需求的補足，直接併入對應票的驗收，不另開票：

| 缺口 | 歸屬 |
|---|---|
| 1. 未 `ready` 就送出提問時後端拒絕；上傳新文件時重置狀態 | #04 |
| 2. 壞檔或非 PDF 上傳回報錯誤 | #02；處理到一半失敗時不留半成品快取、回答不快取 → #04 |
| 3. Section 超過 8,500 tokens 時，先切開再摘要 | #05 |
| 4. `thinking` 事件（思考內容放 Trace、預設收合） | #07（後端事件）、#09（收合元件） |
| 5. 問題過長的拒絕事件寫進事件契約 | #06 |
| 7. 中文提問（user story 20）、「有什麼限制」（user story 10）的 eval 題 | #08 |
| 8. top-k 與 think 等級可設定（user story 47） | #06（top-k）、#11（think 實驗） |
| 9. eval 防呆：數字不得用 `contains`、forbidden 對否定句不誤判、預設 `pytest` 排除 eval | #08 |
| 10. 來源查詢遇到不存在的編號 | #01 |

需要使用者決定：缺口 6，紀錄於 `.lat/decisions/D01-unverified-and-fixed-reply.md`。

## Review 延後項目（從前一票的 Review 移交）

| 來源 | 項目 | 歸屬 |
|---|---|---|
| #01 Review | 截斷的 PDF 被報成「沒有文字層」 | #02 |
| #01 Review | 過長段落切開時，重疊的起點對齊到字詞／句子邊界 | #02 |
| #01 Review | 上傳失敗時不應已清掉目前的 Document | #04 |
| #01 Review | `[C1 C3]`（空白分隔）與 `[C1–C3]`（範圍）引用的正規化 | #07 |
| #01 QA | 回答中的 Markdown（`**粗體**`）原樣顯示；10K 長條沒有明確刻度 | #09 |
| #01 QA | Q3 回答只引用一次、把 NaiveRAG 比較誤當成消融結果 | #03（表格重建與回答 prompt） |
| #01 QA | 乾淨 clone 啟動（ST-01）、`fetch_data.sh`（ST-02） | #11 |
| #06 Review | Lookup／Synthesis 因額度放不下而略去的 Chunk 數量，沒有記在 Trace | #03（同一段檢索流程） |
| #06 QA 修正 | 真實 gpt-oss 下，Q2 的 Sub-queries 沒檢索到 610 成本段落與增量更新段落（確定性劇本測試通過） | #11（調整 Chunk 大小／top-k／BM25；在 #02 真實 Section 與 #03 相鄰／表格連結之後） |
| #06 Review | 沒有對話歷史時，回答 prompt 仍重複附上目前的問題（佔用證據額度，計算正確） | #11 |
| #06 Review | 文字系統不一致時保留 `plan_source=router`；#08 要讀 `rewrite_language_mismatch` | #08 |
| #06 Review | 回答把「610 × 1,000 tokens」寫成「610,000 個 token」；Golden Facts 判定要接受等值寫法 | #08 |
| #06 QA | 簡體中文提問時，Router 的 Standalone Question 變成繁體（回答仍是簡體，不影響結果） | #11（觀察，不阻擋） |
| #08 QA | 「用三句話、中文總結」沒有 eval 題（QA-02） | #05 |
| #08 QA | Ollama 停止時的錯誤訊息（EV-05） | #07（連線失敗事件） |
| #08 QA | `-m eval` 會一併跑 router smoke、忽略 `--eval-cases`；`contains` 讓 "NaiveRAG-High" 算成 "-High"；judge 判 matched=false 時沒有記錄理由；最高相似度分數在 Trace 的呈現（TR-04） | #11 |
| #02 Review | 沒有段落的 Section（如 LightRAG 的 §3、§5、§7.3）不送進 Section Summary | #05 |
| #07 Review | 上傳時 Ollama 失敗只顯示通用的 `ingestion_failed`（EV-05 上傳段） | #04 |
| #07 Review | `HTTPStatusError`（如模型不存在 404）被報成連線失敗；embedding 階段的 `ValueError` 報成 `answer_failed`；分批抽取失敗也標 `stage="answer"` | #11 |
| #02 Review | 圖中帶編號的步驟標籤（粗體「1 Extract Entities」、較大字「2 Build Graph」）會開出假 Section | #10（第二份文件驗證時觀察） |
| #02 Review | 框線內、沒有編號的標題（陰影底上的「Conclusion」、緊貼 teaser caption 的「Abstract」）可能被濾掉 | #10 |
| #07 QA | 錯誤後狀態列仍是暫定的斜體；句子間沒空白時 Unverified 標籤緊貼下一句 | #09 |
| #02 QA | Citation 原文面板標題寫「p.7」，旁註寫「p.7–8」 | #09 |

## 中斷點（2026-10-13，Orchestrator 額度用盡）

- main：`11968fd`（含 #01、#06、#08）。#01、#06 done；#08 QA 進行中（報告將寫到 `docs/verification/ticket-08/qa/`）。
- #07：實作完成（`f26b09e`），獨立 Review 進行中。
- #02：Review 修正中／已送複審（見 `.lat/briefs/pending-request.md`）。
- #09：初稿完成，等使用者回覆 D02（`.lat/decisions/D02-tufte-draft-direction.md`）。
- 未開始：#03、#04、#05、#10、#11。
- 恢復：主控以 `hcom start --as levi` 重新連線，讀 `.lat/tasks/`、`.lat/decisions/`、`.lat/briefs/` 與本檔。
