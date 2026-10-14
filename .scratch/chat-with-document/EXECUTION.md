# 執行清單（LAT）

Status: in-progress

依據：`PRD.md`（ready-for-agent）、`issues/01`～`13`、`AGENTS.md`（數值的唯一來源）、`CONTEXT.md`（術語）。
需求與 Spec 已由使用者確認，本輪略過討論與重寫 Spec，只依既有 issues 推進。

**現行驗收／流程：D05（2026-10-13 15:43 真人核准，Main直接核對原對話）。** #10品質調整到17:45；#11調參＋最終eval時限為18:33:01–21:33:01（已正式開工）。Q1–Q3與第二份文件每題N=3、報告每fact通過率與失敗原因，含forbidden的品質缺陷不阻擋交付。10K、Citation、固定拒答、確定性測試、獨立Review維持。剩餘QA只在#10合併後及交付前；改查commit與測試，不逐檔byte/hash比對；新證據保留結論與最終run，既有歷史保留。下方歷史嚴格品質gate／每trial保存／byte比對要求均以D05覆蓋。


**D06 收斂（16:46 真人核准，Main直接核對原對話）：** #10本輪必要修正限generic頁碼污染、upload_error成功判斷、ai-log與freshN3；numeric檢查器不擋合併，附原始率／原因／來源與答案人工核對及已知誤判。下一輪只審這些修正與回歸；新發現僅10K／有根據Citation／固定拒答／確定性測試失敗擋合併，其他列已知缺陷。D05時間與QA點不變。

## 分工

| 角色 | 設定 |
|---|---|
| Orchestrator | Codex `gpt-6-astra` high（HCOM `nova`）；本 session turn_context 已核對 workspace-write / on-request |
| Implementer | D21現行：Codex `gpt-6.1-sol` medium，透過HCOM、workspace-write/on-request；歷史各票保留原設定 |
| Reviewer | D21現行：Codex `gpt-6.1-sol` medium，獨立context，workspace-write/on-request；禁止Claude，歷史Review保留原設定 |
| QA | D09現行：最終網站驗收由使用者依清單操作；不另派Codex QA |

整合分支：`main`。每票在 `.worktrees/<NN>-<slug>/`、分支 `lat/<NN>-<slug>` 開發；合併前 rebase 到最新 `main`，以 `--ff-only` 合併。

## 逐票狀態

| # | 票 | 依賴 | 波次 | 預計修改範圍（衝突協調） | 狀態 |
|---|---|---|---|---|---|
| 01 | Walking skeleton | — | W1 | 建立整個骨架（後端、前端、測試、README） | done（9ba4327；Review APPROVE；QA 7/7 PASS）|
| 02 | 依結構解析與切塊 | 01 | W2 | Parser、Chunker、ingest 測試；前端只動 Citation 旁註文字 | done（e59e096；Review APPROVE；獨立 QA 6/6 AC、213 tests、browser PASS） |
| 06 | Router 與 Synthesis | 01 | W2 | Router、Context Packer、提問流程；前端 Trace 的 plan 與階段指示 | done（5799106；Review APPROVE；QA PASS，AC7 報告隨 #08）|
| 08 | Eval harness | 01 | W2 | `eval/`、pytest marker 設定 | done（11968fd；Review APPROVE；QA 0 FAIL）|
| 09 | Tufte 設計（需人確認初稿） | 01 | W2 初稿 → 使用者確認 → 定稿 | `frontend/`（樣式與共用元件） | done（d48fbf6／Main3432aa09；Review APPROVE；独立QA四項AC通過、21情境PASS；reload-resume限制明列）|
| 04 | 上傳進度與快取 | 01（實際排在 02 之後：共用 ingest 流程） | W3 | Ingestion Jobs、快取、上傳 API、前端上傳進度 | done（4eee3d2；Review APPROVE；獨立 QA 5/5 AC PASS，192 tests PASS） |
| 03 | 表格重建（Q3） | 02（實際排在 06 之後：共用 Context Packer） | W3 | Parser 表格、Table Chunk 連結、Lookup 檢索、Citation 彈窗表格 | done（5d6204c；Review APPROVE；QA structural/UI PASS、238 tests；Q3 品質仍 #11 FAIL）|
| 07 | 失敗處理與串流狀態 | 01（實際排在 06 之後：共用提問流程） | W3 | Gateway 重試、Citation Validator、錯誤事件、前端暫定／重試／錯誤狀態 | done（9538b88；Review APPROVE；QA 16 PASS）|
| 05 | Summary Tree 與 Global（Q1） | 02、04、06 | W4 | Summary Tree Builder、Global 路徑、文件概覽、`[S#]` | done（ca66429＋#09整合3432aa09；Review APPROVE；QA265tests／R01–R06複驗PASS；品質仍#11）|
| 10 | 第二份文件 | 03、05、08 | W5 | 下載腳本、Golden Facts、泛化修正、ai-log | done（3bb0c64／Main7cf9185；限定Review兩軸PASS／整合316PASS／獨立QA功能PASS；N3品質FAIL與已知限制按D05/D06保留） |
| 11 | 調參與最終驗收 | 全部 | W6 | eval 實驗、AGENTS.md 設定、README、最終 build | ready-for-human（Main db64d84；已審 f089cae＋D10 A限制；整合327PASS、兩份快取0-call Ready；D09回報其餘正常／Q3已接受，A9拒答／警告誤歸因FAIL；D14 B交#13有界修正） |
| 12 | 對話排版與中文回答過程 | #11已整合基準 | W7 | 前端／dist／前端驗證；不改後端與事件 | ready-for-human（D21已審7d3794a整合；Main fd1034f完整327PASS、8101提供新UI；D9／D12–D14待人工，既有窄螢幕停滯FAIL保留） |
| 13 | 人工A9最小修正 | #11已整合基準 | W7 | backend最小修正／tests／證據；不改前端與事件 | wontfix（D23使用者核准本輪凍結目前後端、A9保留已知缺陷；D21/D22證據與舊9715538未採用狀態保留） |

共用檔案依序修改：同一波內，後合併的票先 rebase 到已整合的 `main` 再送最終審查。

## 每票完成條件

實作 + 必要測試 → 獨立 Reviewer（/code-review；D04 後 GPT6-sol high）→ GPT 修正 → 複查 → rebase 並合併到 `main` → 在整合後版本跑驗收條件 → QA 驗證（UI 用真實瀏覽器並保存證據）→ 更新本表與 issue 的 `Status:` → 收尾 Agent 與 worktree。

驗收逐項標記 `PASS`／`FAIL`／`UNPROVEN`／`NOT_EXECUTED`，附證據。

## 待使用者決策

D01–D23的現行處置均已由真人答覆。D23凍結目前部署後端、A9列已知缺陷，停止本輪修復；D18結束為舊9715538保留不採用，不接受其中新增錯誤。快捷題已換成資料集題並重新產生dist，本次tests／live／browser／HTTP／Review均依使用者明確要求不執行，由使用者操作。D22窄螢幕問題先擱置，歷史FAIL保留。LangGraph只進入討論，未核准引入或重構。

- D02 已由使用者在新 Main session 直接核准「同意，照此方向定稿」；紀錄於 `.lat/decisions/D02-tufte-draft-direction.md`。

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
| #05 D04 Review | Q1 中文回答宣稱四個領域／指標全面勝過含 GraphRAG 的基線，與 Mix Overall 相反；Q1/中文 cases 缺少既有 not_all_datasets fact，尚未證明同一 fact 的 Judge 誤判；原摘要未保存，來源位置未定 | #11（補既有 fact 覆蓋與 meaningful regression；保留逐字證據要求及失敗原文） |

## 主控狀態快照（2026-10-13 08:55，levi 暫停排程）

- main：`d56e092`（含 #01、#02、#04、#06、#07、#08 的程式碼）。
- done：#01、#06、#07、#08。
- #02：已合併；QA 抓到 CJK 長段落斷句 FAIL → 修正後 Review 抓到 N1（中文表格數字被黏在一起）→ vida 修正（含跨頁段落合併），複審請求 head `7d209b7`（base `d56e092`），尚未複審。
- #04：已合併（`4eee3d2`）；QA 因 Sonnet 額度中斷，部分證據在 `docs/verification/ticket-04/qa/`（未提交），需重跑或續跑。
- #03：第一輪 Review CHANGES_REQUESTED（Table 4 誤判已重建、caption 在下方與雙欄誤配對）→ mulo 修正並 rebase 到 `d56e092`，複審請求 head `f7268f9`，尚未複審。Q3 數值兩題 0/3 移交 #11。
- #05：實作完成，初次 Review 請求 head `14e783d`（base `d56e092`），尚未審查。
- #09：初稿完成，等使用者回覆 D02（`.lat/decisions/D02-tufte-draft-direction.md`）。
- 未開始：#10、#11。
- Codex agents vida／mulo／kano／gala／dune 於 08:54 由系統結束（process_exit），工作樹與提交都保留，可用 `hcom r <name>` 接回。
- 簡報、審查與修正紀錄：`.lat/briefs/`；任務卡：`.lat/tasks/`；決策：`.lat/decisions/`。

## 接手檢查點（2026-10-13，nova）

- 直接使用者授權新 Main 接手全部既有 Issues；levi HCOM #5404 已確認停止所有排程。五位舊 workers process_exit；保留其 worktrees、commits 及未提交 QA 證據。
- LAT recovery active：session `01a132c0-2f33-7e72-9a63-74731d18d08c`，沿用本索引與共用 decisions。Main model/effort/permissions 已從本輪 turn_context 核對。
- 整合順序沿用依賴：先 #02 修正複審與整合，再 #03／#05 rebase 複查；#04 補完整 QA；#09 已解除 D02；#10、#11 維持既有依賴。
- 新角色設定只套用後續工作；歷史 Review／QA 證據保留原角色與版本，不改寫成新驗證。

- 接手 audit：QA nova-qa04-kilo 核對五個 worktree 皆乾淨，candidate heads 與任務卡相符；8110–8189 無 listener；無關的 8201 與既有 browser daemons 保留。#02 Reviewer nova-r02-mige（Opus5.5 medium，terminal 確認）；#04 QA nova-qa04-kilo（GPT6.1 medium，turn_context 確認）；#09 Implementer nova-i09-romi（GPT6.1 high，turn_context 確認）。Codex 均 workspace-write/on-request。

- #02 nova-r02-mige 複審 CHANGES_REQUESTED（2026-10-13）：R1 跨頁接續混入 Table/Figure caption／running header；R2 中文標籤+數值列仍會黏合。F1 原 CJK 分句形狀已通過；42 ingestion tests 通過仍不足以排除這兩項。證據 `.lat/briefs/nova-r02-review.md`；指派新 Implementer 修正後交回同一獨立 Reviewer。
- git-track sync：本機 checkpoint `cd3e303`；`git push` 回報 No configured push destination。無 remote，不自行指定遠端；不阻擋本機實作與驗收。

- #04 完成：獨立 QA `docs/verification/ticket-04/qa/takeover-report.md`（5/5 AC PASS）；Main 核对原 Review、commit ancestry、source unchanged 與 screenshot。#05 合併後摘要快取／概覽，#09 合併後上傳 UI 回歸仍按原依賴驗證。#03 Reviewer nova-r03-hazu、#05 Reviewer nova-r05-guru 均 Opus5.5 medium（terminal 已核對），正在既有 candidate 上獨立審查。

- #05 nova-r05-guru 初審 CHANGES_REQUESTED：H1 Global prompt 偏向 LightRAG/Q1、M1 以來源文字內 [S#] 猜 source mode、M2 upload/cache 測試過濾 summary calls 而削弱斷言；另有 Group/Document 進度、遞迴/取消測試、標題與 cache identity 缺口。完整 `.lat/briefs/nova-r05-review.md`；交給獨立 Implementer 修正，Q1 真實品質仍於 #11 驗收。

- #03 nova-r03-hazu 複審：既有七項 findings 已修正，208 tests PASS；新增 CHANGES_REQUESTED：表格後的 heading/list 被吞入 table region（Section 消失）、段落中 Table/Figure 開頭行誤認 caption。完整 `.lat/briefs/nova-r03-review.md`；新 Implementer 修正後，待 #02 整合再 rebase 複審。

- #02 複審 2：R1 caption/header 與 R2 labelled rows 已修正；full210 PASS 但獨立右欄/非對稱 margin probe 發現新 M3（flow width 假設對稱），仍不得整合。
- #09 獨立 Review CHANGES_REQUESTED：M1 Markdown source/value offset 導致 Unverified 標錯句；另修復 backend restart404 的舊 Document 狀態及 source fetch race。依 PRD 使用 browser harness 回歸、不新增前端 unit-test 要求；原設計證據保留，D02 核准在新報告說明。Reviewer與兩個 child contexts 實際 Opus5.5 medium 已核對。
- #03 新修正 e9deece 的 formed-grid stop 又暴露 internal group-divider 後數值列可能截掉，已由 Reviewer/Implementer 直接協作補回歸；原始數字完整性不放寬。

- #10 獨立選文 preflight：nova-i10-fimo（GPT6.1 high / workspace-write/on-request 已核對），只讀 primary sources、下載 ignored candidate PDF、記錄 fixed version/頁數/雙欄與摘要長度估計。不得改 tracked script/GoldenFacts/source，正式實作與 eval 仍按 #03/#05 依賴放行。

- #02 e59e096 已 ff-only 整合；Main 比對 #04 application/cache/events/frontend 未改，source2ee613b 與 final evidence head 相同。獨立 QA nova-qa02-zeme（GPT6.1 medium，terminal+turn_context 核對）接續六項 AC、原 PA-02 與 Review adversarial cases，main 保持 source 穩定至 QA 放行。
- #05 修正複審 APPROVE（8433e9f）：H1/M1/M2/L1–L6 關閉，Reviewer targeted148 PASS。非阻擋觀察：長問題 Group 過度合併與 prompt cache identity，交 #10/#11 檢查；正式整合與 QA 仍未完成。
- #10 preflight 選定 arXiv2603.06749v1（2026-03-06，109頁雙欄非RAG）；真實 Section 目標長度估計6844/6582 tokens，尚非實際生成證據；正式處理須證明 >6K 與 Group layer。模型原始發行早於論文，opaque cloud exact weights 的限制保留於 provenance。

- #09 修正複審 APPROVE（71925e2）：M1/m1/m2 關閉；獨立18/19 adversarial rendering probes、build/dist parity 通過。殘留 CRLF 邊界 fallback 指派 romi 在其獨占 frontend 分支先補 browser RED/GREEN 後由 kobe 複審，rebase 仍等 #03/#05；現階段不標 done。

- QA02 設定 audit：zeme 曾依一般 AGENTS 路徑探索規則誤派 repo-scout（role metadata GPT6-luna low），不符本輪 exact-model 要求。已停用其結論、禁止再委派，由已核對 GPT6.1 medium 的 zeme 自行重新讀取流程並核對 fixture hash；實際驗收只採其獨立執行證據，QA 報告須明記修正。

- #09 CRLF 修正 e8b266c / source3292629 獨立複審 APPROVE：Reviewer27/27 adversarial probes、typecheck/dist parity PASS；browser RED6→GREEN6，原148 assertions 回歸通過。保留原始 draft/字型，無 backend 變更；尚待整合再審與獨立 QA。

- #02 QA source-freeze released（HCOM7664）：六項 AC PASS、213 tests PASS、24 個獨立 PDF scenarios 與真實 browser/error/cache/citation PASS，無新增 production bug。完整報告整理中，Main 尚未提前勾 done。
- #03 5d6204c ff-only 整合，source/tests/assets 與已審 d7d77e8 位元組一致；獨立 QA nova-qa03-tiki（session01a132f2-a494-73d1-b0cb-04a7899bcd93，GPT6.1 medium/workspace-write/on-request，terminal+turn_context 核對）凍結 main source 進行驗收。#05 只在自己的 worktree 接續 rebase。

- #02 Main 已核對完整 `docs/verification/ticket-02/qa/takeover-report.md`、環境與跨頁 screenshot，六項 AC 全通過，issue 標 done。原160-fact/CJK、24 independent scenarios +2 typography、cache0/0 與 source404 均有獨立證據；角色偏差與自主複核已明記。收尾自己的 implementer/reviewer/QA，不觸碰既有 port8201。

- #11 唯讀盤點已派 nova-i11-meme（GPT6.1 high/workspace-write/on-request，terminal+turn_context 核對，session01a132fb-ce96-78d2-8c04-4cd08fb37bd2），獨立 worktree ca8a02c；只沿用既有實驗與 deferred findings，不改規格/清單、不跑模型或改程式。正式實作仍等全部依賴。

- #03 獨立 QA source-freeze released（HCOM8043）：256 labelled PDF numerical cells、421 tokens、10 independent layouts、CJK/page provenance、browser Table2/uncertain-source PASS，238 tests PASS。fresh real Q3 N=3 仍 FAIL：兩項 numeric exceptions0/3、forbidden pass2/3、baseline1/3、ablation meaning0/3，部分 judge evidence 非逐字遭拒。報告 `docs/verification/ticket-03/qa/takeover-q3-live-n3.md`；AC6 如實報告與最終品質通過分開，#11 不豁免。正式 QA 報告核對後才標 #03 done。

- #03 Main 已核對完整獨立 QA 報告與 uncertain-source screenshot；AC1–5 PASS、AC6 如實報告 PASS，正式標 done。Reviewer 兩個 child transcripts 各13次 assistant actualmodel Opus5.5 / effort+perTurnEffort medium 已核對。收尾自己的三個角色及 merged worktree，最終 Q3 品質不豁免。

- 使用者直接指示 Reviewer 改成 GPT6-sol high（D04，原文與 session 已記錄）。未完成 #05/#09 review 轉交新的獨立 context；既有完成證據保留模型/版本。Implementer/QA/Main 設定不變；所有 Codex sandbox/approval 與實際模型須核對。

- D04 生效核對：nova-r05sol-zero（session01a13305-1d9b-77a2-ac89-6e579549025b）terminal + actual turn_context 確認 gpt-6-sol/high/workspace-write/on-request。guru/kobe 已停止、保留完整/partial handoff、清理並關閉；#09 下次整合審查另派同設定新 context。

- D04 Review 分流核對：原生 inherited children effort 曾重設 medium，已在審查前停止且不採結果；新 explicit GPT6-sol/high Standards與Spec contexts 的全部現有 turn_context 已核對 high/workspace-write/on-request，設定阻塞解除。

- #05 D04 Reviewer 的獨立 probe 找到長 Section 摘要以字元切開 Table Chunk、後批次遺失表頭的 deterministic defect（HCOM8563）；Implementer 以真實12頁 PDF＋本地 bge-m3＋guarded ScriptedLLM 的 public upload 路徑重現 RED，改為完整 Chunk 邊界批次，targeted27 PASS，待 full suite／獨立複查。原 Q1／中文回答品質失敗及 forbidden coverage 缺口仍歸 #11，不以本次修正宣稱解決。

- 流程更新：已完整重讀現行 LAT/hcom-spawn 與 Main AGENTS 自查要求；複審改派 fresh context、以上次 reviewed head 為 base，QA 先備情境批次、最多3個同時實作、文件隨下次合併提交。#05 修正 ca66429 自0663db0起由 nova-r05fix-nano 獨立複審（session01a13317-a4ed-7a20-8d96-93b4dcc78014；actual GPT6-sol/high/workspace-write/on-request 已核對）。#09 nova-r09sol-duma 同設定已核對，僅待整合版本；原 Review 證據保留。接續資訊 `/private/tmp/rag-lat-main-handoff.md`；既有清單與授權不變。

- #05 ca66429 ff-only 整合：Main 已核對完整 full Review＋fresh correction Review（Standards0／Spec0 findings）；兩個 Review child actualmodel/effort/permissions 均符合。15個受保護來源檔與原 main d371b79 位元組相同；整合後全部 source/tests/frontend/scripts/eval-config 檔與 candidate 相同，證據 `docs/verification/ticket-05/integration-source-identity.json`。QA05 已先備20項情境，整合後依固定 SHA 執行；#09 僅在自身 worktree rebase，#10 仍等 QA05。

- #05 QA on0718466：265 deterministic PASS；public10TableChunks/820rows/2batches、48Sections10→2Group、fail/cancel/cache identity PASS。fresh real Q1=5/8、中文=6/10 FAIL（保留原文，#11）。Browser啟動的 auto-review 授權前提拒絕經 Main 核對實際SHA/情境/本機服務後，以同一指令獲核准，非繞過。實際 UI 發現 UP-03 概覽只留在 DOM，會被對話捲出視窗（HCOM9591）；共享 frontend 指派 romi/#09 修正，#05 不標 done，等整合後獨立 QA 複驗，#10 仍等候。

- QA05 最終 batch（HCOM9778）已完成並解除 Main source freeze：0718466／75檔未變，AC2–5 PASS，AC6 如實報告 PASS／品質 FAIL，AC1 UP-03 viewport FAIL。完整報告 `docs/verification/ticket-05/qa/takeover-report.md`；QA own browser/server/temp 已清理，保留 context 待 #09 reviewed integration 後複驗。#05 保持未完成；#09 修正由單一 owner 繼續。

- #10 bounded read-only refresh on0718466（HCOM9911）：固定PDFhash未變；最新版解析仍未保留真正附錄，保留26個 genuine body intervals，15個 TableChunks/123總Chunks，Table9數值正確但 Section 歸屬落在假 Appendix 標題。genuine retained-body target5399；原全文PDF6844/HTML6582只是估計，尚無生成>6K證據。已更新原 preflight，不改程式或重新選文；正式 #10 仍等 #05 UI 複驗。

- #09 frozen cb4f1c9/sourceee383e5（base0718466）：實作者265backend、29real-endpoint、6viewport、148adjacent、10source/restart、6CRLF PASS；107dist重建一致。Main 自行比對89個 backend/test/eval/script/config、129 draft/font 與原已審 Answer.tsx 位元組未變；duma 已開始完整獨立 Review。QA05 AC1與QA09仍待整合後驗證，未提前關票。

- #09 full Review（HCOM10213）：未發現產品程式缺陷；Spec APPROVE，Standards 要求最終 Markdown/Citation renderer 真實 gpt-oss smoke 及 docs/ai-log correction 紀錄。Main 放行 romi 獨占小型 generic PDF 真實模型測試，產品 source 固定不改，Main 提供 ai-log 文字供 branch 追加；完成 evidence/docs delta 後派 fresh GPT6-sol high Reviewer 以cb4f1c9為base複查。

- #09 correction d48fbf6：真實 gpt-oss／bge 的4次呼叫全stop，最高預估3892/10K；最終browser renderer條列／S1／Unicode空白／Source／Trace證據已核對，未觀察的rareformats明列限制。Main逐一比對345產品檔與cb4f1c9相同，29docs/evidence差異；nova-r09fix-gigi fresh correction Review進行中。#10獨立QA nova-qa10-pita（session01a1335c-6805-7941-af57-973873f1caa6，actualGPT6.1medium/workspace-write/on-request核對）僅先備既有需求情境；不提前執行或解除#05依賴。

- #09 d48fbf6 ff-only 整合：Main 核對 full＋fresh correction 兩軸 APPROVE 與 child runtime，345檔實際工作區hash與candidate一致；89backend/config、129draft/font與原已審Answer保留證據合併於 docs/verification/ticket-09/integration-source-identity.json。完整Review、原QA05 FAIL/live品質報告及QA09預備22情境隨本次合併checkpoint；QA05/QA09依最終MainSHA獨立批次驗收，未標done。

- QA05/QA09 released onMain3432aa09（HCOM10547），獨立context與port8270/8290；Main source frozen。QA05重現browser approval前提拒絕（10598）後，Main直接核对SHA／完整Review／345hashes／R01–R06／本機PID49927，以相同command核准exit0解除，僅開browser、不代做驗收。QA10 requirements-only19情境已備妥，仍全NOT_EXECUTED；其正式執行維持依賴。

- #05正式done：Main已核對完整獨立QA原報告＋3432aa09 R01–R06 PASS、桌面六輪geometry/截圖及手機换檔source。原品質FAIL保留#11，非豁免。QA05/QA09 UI均完成後，Main依序以各自session close兩個browser，均exit0；未知tab reset不推論產品bug，受影響cases已獨占重驗。#10正式實作依賴解除，Main仍凍結3432aa09供QA09最後hash/report；#10僅在獨立worktree修改。

- #09正式done：Main完整核對QA09報告、runtime、source345hash/build107parity、真實Citation/Table2/Trace/localfont畫面；四項AC全通過。T09-08處理中整頁reload自動續接job是額外恢復探查，既有PRD/Issue09未要求持久化job身份，仍標UNPROVEN並交#11 README如實說明，不新增需求/endpoint、不宣称resume成功。真實Q3模型比較遺漏仍#11 FAIL。QA09全部source-sensitive工作與cloudwindow已release，測試資源清理完成。Main source freeze解除，#10沿3432aa09獨立實作；#11依賴#10。

- 收尾：#05/#09的本輪實作者與QA已關閉，worktree與merged分支安全移除；D02原核准draftf15f792保留tag lat-approved-tufte-draft。QA11 nova-qa11-zoru（actualGPT6.1medium/workspace-write/on-request，session01a13377-7204-77e2-aba2-34ffbf1a7651）完成18個requirements-only情境，全NOT_EXECUTED，待#11實作/審查/整合。#10 fresh Reviewer nova-r10-lubo（session01a1337c-ba34-7263-ad04-0a473242f2b1，actualGPT6-solhigh/permissions已核對）只讀需求待固定candidate；正式sourceReview未開始。

- #10 實作中：六個 generic parser/table public-upload RED→GREEN 已保存；checkpoint448b719尚非送審版本。首次真實長文件試驗 issue10-trial1 在 Section Summary 1200輸出上限遇到 done_reason=length，Gateway正確拒絕發布Document，尚未執行問答；22calls最高預估6107。保留原始失敗證據，Implementer接續摘要長度控制／回歸，不調高額度、不降低實際>6K與Golden Facts門檻。Reviewer與QA維持待固定版本放行。

- #10 trial4中間實測（未送審448b719＋dirty）：真實public upload完成，31Sections/154Chunks，實際Section Summary7390tokens、1層Group；此為初步證據，仍須固定候選與Review核對合理Section／完整性。SECOND_NUMBER與SECOND_SUMMARY judge皆FAIL；原始數字回答已呈現447/304、0.966→0.951與F1不變，但完整fact/Judge證據仍待診斷，不自行改判。2次length後重試stop完整保留，最終#11全call無截斷門檻不豁免。

- #10 trial5：數字contextual judge與forbidden PASS；全文summary judge仍FAIL。擴充後數字題同時要求expert子集辨識與比較，實際Synthesis與既有保守分流規則相容；Main要求依完整題意／來源跨度核對測試預期，不調production Router硬逼Lookup，保留歷史FAIL與期望修正理由交獨立Review。仍未送審／完成。

- #10 checkpoint11450：277 deterministic PASS／259.94s正常結束，非stalled。trial7真實Section tokens7641／1Group，數字與分流PASS，summary judge仍FAIL。新public-upload RED顯示Ref/Model表內換行模型版本號可能誤判成scores；fimo接續generic geometric reference-row reconstruction與missing-cells raw fallback，候選尚未凍結，需修正後重跑完整測試／真實facts。

- #10 trial8固定source後仍FAIL：numeric judge摘錄缺少完整expert-subset脈絡，summary覆蓋仍不足。Main依既有Issue10裁定新數字題可由Lookup（表格＋連結段落）或Synthesis（子集說明＋表格）完成；驗收未指定唯一route，故使用明記理由的允許集合，但仍必須真實Router／無fallback、來源與完整facts通過，不逐輪切換單一期望值。原12題Router回歸不變，歷史FAIL保留供Review。

- #10新source checkpoint1286357仍非final：source audit報告AppendixD324rows／3888數值保留與LightRAGTable2相同，待Review核對關聯。trial9實際7120Section tokens／1Group但FAIL，3次length重試可見；Main讀到「沒有外部專家驗證」與三篇論文驗證資料矛盾，要求追溯Section/Group來源。fimo已補generic局部未提及不等於全文件缺失、system warning非作者主張、eval允許route集合仍拒fallback的修正／回歸。獨立Review/QA尚未放行，#11仍hold。

- #10 Main11718改進下一步：trial10仍有summary實質FAIL與numeric分號句關聯檢查FAIL，先完成bounded診斷／現有測試，整理乾淨固定checkpoint、完整suite與path inventory，停止新prompt迭代；交尚未開始的freshReviewer lubo作完整獨立Review協助定位，再由fimo修正、另派fresh correction Review。這是既有Review→修正循環，未降低驗收、不合併／不標done；Main仍待exact head才正式放行。

- #10 frozen597db375（Main查證clean、base3432ancestor、16tested-source hashes與252frontend保留PASS）已正式放行lubo完整獨立Review；fimo source hold、cloud已釋出。287tests PASS不覆蓋實際summary矛盾／numeric分號binder／3個Section不足80tokens。Review需補實際入口分支與失敗恢復路徑，原path-inventory只是檔名；修正後另派freshReviewer，QA10與#11仍依賴未放行。

- #10 Review runtime audit：lubo本輪01a133fc-19cf-7d43-bba3-99d529bb223b與獨立children01a133fc-a562-7f23-9735-8c239736006f／01a133fc-cf52-7483-9942-679809294fa1，Main逐一讀取actualturn_context均gpt-6-sol/high/workspace-write/on-request；無模型替換。

- #10 fullReview12023兩軸CHANGES_REQUESTED：獨立probe確認Abstract被前言略過、3個Summary不足80、AppendixD缺乏驗證主張傳至Global、numeric分號false-negative與互換All/InfoFound值false-positive。Main完整讀報告及pathcoverage後放行fimo獨占修正／cloud；保留所有FAIL，不合併。以597db375為下一輪freshReviewer基準；lubo不複審自己提出的修正。

- #10 correction中：Abstract／80tokens四項RED→GREEN，numeric adversarial與既有checks28PASS（尚非finalsuite）。兩次bounded真實probe保留FAIL：局部未見驗證仍可能上推、partial表格範圍泛化、Total誤稱summed、無關材料部分factual bullets缺Citation；Main已讀原輸出並交回fimo，原文Total為fulfilled criteria比例。QA10原19情境補齊這些路徑，仍全NOT_EXECUTED。

- #10 fresh correction Reviewer nova-r10fix-halo已備妥（session01a13416-3f3e-7ac0-bc93-38bcd3831f85／turn01a13417-36bb-7420-bcfc-0abdaf704f03，Main actualaudit gpt-6-sol/high/workspace-write/on-request），base597db375；僅requirements/priorReview prep，sourceReview待固定head。

- #10 Main裁決12244：三次prompt-only bounded試驗仍產生來源未明言的absence評論，改採generic表格主導Section/partial的source-anchored extractive selection；既有low1200 guard／SummaryNode／80-500／>6K／Group／原文provenance與真實Global要求不變，不增加獨立auditor階段。不另問使用者，屬既有grounded摘要的內部實作；先用原FAIL與無關table/prose實測，保留真正作者限制與完整數字關聯，再全流程驗證／fresh複審。

- #10 source-selection適用邊界裁決12280：以table-dominant且足夠distinct原文atomic units可保留caption/header/rows並達80-500為条件；極短／非表格Section仍可走忠實敘述摘要，同限額同長度，不因選文失敗而偷偷fallback逃過驗證。真實來源若無法忠實滿足契約須具體回報，不padding／重複／放寬。

- #10 Main12308依D01裁決：真實Global無關材料S1/S2主體主張有引用，短開場「文件報告兩項研究」作為立即接續來源段落的導讀，不新增無引用句validator／重試／Unverified政策；先前四個未引用methodological bullets仍屬實質FAIL。保留原probe觀察與JSON誤覆寫後從完整raw log還原的紀錄，優先完成source-selection及完整fresh驗證，不為導讀句擴充scope。

- D05已直接核對Claude原始proposal UUID86f304f7-2b2b-4c37-8a9e-ef51d3b17048與真人UUID7cff15e1-c83f-4c2f-91a7-0a2a8d8bbd20（07:43:33Z）；完整定位寫回decision。Main07:46:35Z廣播fimo/halo/pita/meme/zoru，立即停逐檔比對與每次trial歸檔，按17:45／#11三小時與N3報告門檻推進。levi修改AGENTS／10／11未提交隨下次merge保存；nova仍唯一調度者。LangChain追問不代表核准重寫，原硬限制不變。

- #10 correction fullsuite298PASS／4FAIL（249.68s）；已定位source-selection單一sourceunit超過guarded capacity使ingest失敗，需修正功能回歸。fimo指定gpt-6.1-sol/high當前出現Selected model is at capacity，Main已通知同session同設定重試一次，禁止換模型；若重現保存交接並回報外部阻塞。D05品質timebox不免除功能測試。

- #10 modelcapacity已以原session一次續作恢復，Main新turn_context核對仍gpt-6.1-sol/high/workspace-write/on-request；無替換。4FAIL分為2個舊測試adapter與2個selector容量問題，fimo接續修正後finalN3。

- #10 correction確定性重跑302PASS／3eval deselected／243.12s，ruffPASS。真實finalN3已完成六次問答：sourcecitation／route／numeric forbidden3/3，expert_agreement與whole_document_coverage0/3；最後test把upload_error空字串誤當None才exit1，非上傳失敗。Main要求修正sentinel並驗證現有report，不為純harnessassert修正重跑未變production的昂貴模型。依D05報告品質缺陷；尚待fimo固定提交／halo複審／整合QA。

- #10 指定GPT6.1 high再次capacity停工，Main保存302PASS與finalN3原始結果，凍結現有worker成果供fresh halo複審。已知upload_error空字串assert與最終失敗原因報告尚未修正；非完成／不合併、不換模型。獨立Review繼續，QA10與#11仍hold。

- #10容量冷卻後以原session恢復report-only；Main核對新turn01a13463-a32a-7bb1-b80b-d83a0fa4bd73仍指定GPT6.1 high/permissions，source維持588638d供halo審查。Main已讀完整finalN3：numeric失敗可能包含檢查器關聯誤判；Global三次均寫28expertjudgments，原因待查，不改判。levi另交既有使用者簡報素材.md，保留並隨下次merge納入。

- #10 freshReview12806／12850初步發現：p28footer進入Chunk74並被Section→Group→Global當28expertjudgments；numeric比較欄互換false-positive及後置標籤／共用F1false-negative；成功upload_error空字串assert。Main已讀fimo完整report-only draft，兩個length草稿均丟棄、重試完整且所有110calls守10K。原0/3與exit1不改判，等待完整Review後由fimo集中修正。

- #10 588638d freshReview12894完整CHANGES_REQUESTED已讀；兩軸actualGPT6-solhigh皆Main核對。fimo放行generic頁碼／numeric關聯／success-sentinel修正、ai-log與最後一次freshN3；PRD補充eval工具公開check_fact可獨立測試，應用upload/ask主seam不變。先前Section重試call誤記31已由Reviewer核對修正34，原結論不變。下一輪另派fresh Reviewer，QA10／#11仍hold。

- Main重讀#11原文：無截斷實驗明指正式Router600／Answer3000；一般摘要length可依既有規格丟棄並重試，不另創所有summary嘗試必須stop門檻。每次call仍守10K、記錄length與禁止發布截斷稿。meme／zoru已收到澄清；#11正式三小時計時尚未開始。

- D06套用後#10目前genericfolio回歸2PASS、numeric新增關聯11PASS，成果未提交；fimo再次Selected model is at capacity（第三次），未替換模型。完整suite／freshN3／sentinel與ai-log尚待續作。Main保留source與資源，待同設定恢復；數字檢查器已完成部分保留，不再擴大調整。

- D07真人核准已從freshClaude transcript直接核對：#10合併＋整合QA後，#11正式開工前，以handoff換新Main session，沿用nova唯一調度身份，精確GPTastra high／permissions，啟用新session recovery；移交D01–D07／原清單／已知缺陷。舊Main先停止調度；#11三小時計時於新Main正式放行才開始。

- D06修正fullsuite310PASS／3eval deselected／293.86s、ruffPASS；freshN3先因額外note格式失敗，Main允許同source一次恢復後又因selection pool僅74tokens失敗。兩次均無Ready/cache/答案，不能宣稱N3完成。D08已先記pending並向使用者詢問最小selector修正或明確接受N3未完成限制；fimo停模型／新增source修改，整理固定checkpoint供sumi對既有三項限定複審，其他依賴不提前放行。

- D08使用者直接回覆「允許最小修正並重驗（建議）」已記answered（Main原session／call_ca06b004f6bc4fe4b110f885ae7db1c9）。sumi scoped Review暫停以供fimo獨占兩項selector修正；其public-upload探查發現top-margin章節編號1/2被folio規則誤刪，屬D06明定整數保留的必要回歸，同批修正。待固定head／完整測試／freshN3再限定複審，QA與#11依賴維持。

- D08三項限定回歸已RED→GREEN（commentary丟棄／strictIDs、74-token收斂失敗、D06分離章節整數）；freshN3已實際完成6答案、指令PASS133.72s。Main讀報告初核：數字主fact1/3、summary0/3，Citation／route／forbidden3/3；32Sections／149Chunks、SectionSummary7777tokens／1Group，107calls最高估算9729/10K、2個summary length待finalreport對照丟棄重試。完整suite仍進行，尚未固定head／複審／QA，不提前關票。

- Main已核對3bb0c64ae464ccbe411bbec28bf4490a8fd87354 tracked clean、588638d祖先、完整FINAL-REPORT／316PASS348.69s／29targeted／ruff，以及完成freshN3。sumi原79d0報告僅provisional、未finalize；放行同一待完成限定複審到3bb0c64（D06＋D08），不重做完整Review。兩個summary length為29→33／39→44成功重試，沒有answer/judge length；raw數字1/3與summary0/3照實報告，不繼續品質調整。

- #10 Main已完整核對final scoped Review（13679，兩軸PASS）與actual子context設定；mixed-font標題配對於588638d/3bb0c64完全相同，保留既有provenance限制，第三次數字回答缺逐項Citation亦明列knownFAIL。3bb0c64已公告後ff-only整合，無衝突；Main原tracker／05、09QA證據／使用者AGENTS與簡報素材隨本次checkpoint保存。接續由fimo在Main跑一次整合fullsuite，再放行pita原19情境QA；#10未提前done，#11時計未開始。

- #10整合checkpoint7cf91851f9f86527d69c95910f9eadd58cf7b357；Main git確認source/tests/eval/scripts/frontend/config與3bb0c64 diff為空、工作樹乾淨。fimo已放行Main工作區一次fullsuite，pita只先對照最終source／Review與原19情境，測試／UI仍待整合結果正式放行。

- #10 Main完整整合suite7cf9185：316PASS／3eval deselected／zeroSKIP／257.29s／exit0，主工作區import正確。補入同一固定ignoredPDF後74-token replay實際執行，未重跑整套。pita已正式放行原19情境的一次獨立QA，source凍結／cloud專用；保留rawN3品質FAIL與兩項已知限制。#10待QA最終證據、#11依D07仍未開工。

- #10正式done：Main完整讀取獨立QA報告與19情境，核對Table9／Group／Trace／固定拒答截圖、source未變、8300無listener與QA暫存已清理。實際UI6calls全stop最高9575/10K；完整N3與316整合測試沿用已核對同版本證據。品質1/3、0/3與既有mixed-font／逐項Citation限制仍明列FAIL；opaque training與完整D5關聯UNPROVEN，中文加分NOT_EXECUTED。依D05/D06准予結案，接續10資源收尾、D07新Main session接管，再由其正式放行#11（計時尚未開始）。

- D07 actual transfer 2026-10-13T10:28:16.746985+00:00: #10五個本輪角色均停止、merged worktree/branch安全移除，既有diagnostics/cache保留於ignored .lat/retained/issue10/fimo/manifest.md。新Main獨立session01a134c5-10b4-7c21-96b3-7c682d9f8738 bootstrap已完成，舊Main直接核對actualturn為GPT6-astra/high/workspace-write/on-request。舊Main自此停止調度，recovery取消只表示舊session退休、非專案取消；新Main接管nova後啟用自身recovery，沿用meme實作者與zoru QA。#11正式計時仍待新Main放行。新QA10證據與tracker dirty留待#11 merge提交；test-list既有D2/SM02列已更新，未重建清單。

- D07新Main接管完成：native01a134c5-10b4-7c21-96b3-7c682d9f8738，actualturn01a134ce-b204-7482-a9ea-779817114c77為gpt-6-astra/high/workspace-write/on-request。barehcomstart建立nami後正式rebindnova，新nativebinding核對成功；自身LATrecoveryactive。meme/zoru新turn分別01a134d0-2243-75a1-b20e-a7cbeeaf1c3f／01a134d0-223a-7c33-a16a-a204b4e8085f，Main實際讀取確認GPT6.1high／medium及permissions。沿用原角色/worktree/P01–P18，無重建清單。

- #11正式放行：2026-10-13T18:33:01.455279+08:00（UTC2026-10-13T10:33:01.455279+00:00），調參＋最終eval最晚2026-10-13T21:33:01.455279+08:00（UTC2026-10-13T13:33:01.455279+00:00）。meme獨占自身worktree/source/cloud，自7cf9185rebase接續原Issue11；port8320–8329/browsernova-i11。Main保留dirtyQA10/tracker至下一merge；zoru最終QA仍待獨立Review＋整合放行。N3量測報告／已知FAIL／硬限制／freshReviewer規則保持，無模型替換。

- #11實驗檢查點：36組真實檢索比較完成，初選Chunk800／dense／top-k5-3-2；實作者回報實際Router contexts涵蓋Table2／成本／增量更新，尚待獨立Review核對。low/medium回答與summary concurrency實測進行中；finalN3／完整suite／固定candidate／Review／整合QA尚未完成，不提前勾選驗收。新worker turn01a134d2-a177-74d3-a226-49a9db4dfbe5的actual GPT6.1high/workspace-write/on-request已由Main直接核對，原deadline21:33:01不變。

- #11受控實驗修正（HCOM14380）：原比較各Chunk大小的Router子問題不同；第一版control又意外重產生plan，已標INVALIDCONTROL。最後36組使用同一份凍結的真實Q2/Q3plan、沿用未變Chunks/vectors，選定500／dense／5-3-2。原800的low/medium比較標exploratory，維持medium；最終N3／defaults／cache須一致。修正相關18PASS，完整suite重跑中；尚未固定candidate／獨立Review，不提前結案。

- #11最終N3已完成27答案／277calls，最高估算9847／10K，正式Router/Answer無length；LightRAG原始品質FAIL、second數字0/3／global1/3，325完整確定性測試PASS。HCOM14590回報secondNUMBERrep2有效C9重建對應Table10而非所述Table9，C4支援§8.1；重建並非原始SSE。Main依D05/D06保留為潛在引用硬限制問題，未豁免／未准合併；先完成既有固定candidate與fresh獨立Review，明確核對引述支持／原始證據限制／回歸與最小處置選項。其他文件與證據工作繼續。

- #11固定候選0c320a8（source25afd0b）Main已核對Git存在／7cf9185祖先／clean／docs-only尾提交，完整implementation/conclusions/cachemanifest/cleanPythonclone證據已讀。Reviewer meme-review-riko native01a1351e-49a4-7b43-ab6f-3d81af3f91e8，actualturn01a1351e-4a6f-7e53-b02b-4589b1f2d974直接核對gpt-6-sol/high/workspace-write/on-request；正式完整Review放行，兩軸child同設定核對要求維持。Citation待判定，未合併／未放行QA。

- #11 fullReview14900兩軸完成：secondNUMBERrep2原始FinalEvent缺Table9來源，正確數字未被所引用來源完整支持；C9→Table10是重建佐證，非原始SSE。Main不豁免，放行meme最小通用表格引用修正、原始事件N3與無關表格實測；另修controlled報告連結與rank-matrix public seam。既有FAIL保留，修正後fresh獨立Reviewer從0c320a8複審。QA／整合維持hold，21:33:01時限不變。

- D09真人答覆已直接核對：proposal4cf10004／usera0ea4307，20:11:49核准最終網站QA由使用者照清單操作，取消zoru、不另派CodexQA。保留原P01–P18為未執行草稿；獨立Review、確定性與整合後完整測試維持。manual-qa-checklist隨下次merge提交，合併後通知levi與使用者固定SHA；人工結果未回前不宣稱最終QA完成。此答覆沒有核准另一個Citation豁免選項，既有最小修正繼續。

- #11 bounded修正f089cae（base0c320a8）已核對Git／clean／完整correction報告。327testsPASS；修正N3共27答案／272calls，最高9667/10K，正式Router/Answer無length，1Section草稿length後成功重試；Table9原始事件來源3/3，numeric1/3／global1/3。仍有錯誤單位、缺逐項引用與相鄰Chunk時間敘述支持限制，保留供限定複審，不宣稱全groundingPASS。meme-recheck-bela native01a1353d-66e3-79d2-8243-f84434af4eaf／turn01a1353d-6791-7262-ba61-c42ed021014b actualGPT6-solhigh/wswrite/onrequest由Main直接核對；新獨立correctionReview接續，整合尚未放行。

- #11 fresh scopedReview15271完成：Standards0，Spec保留逐項grounding硬finding（評估數量稱papers、時間細節引用相鄰Chunk、結論缺引用）；特定Table9錯表關聯本輪3/3已無再現。Global表格提示對[S#]路徑有未觀察風險。Main已完成最小修正／全327tests／27freshN3後，先記D10v1 pending並向真人提問：接受明列限制的本版驗收例外，或再一輪bounded修正。未答不合併／不新增模型調整，證據交接仍繼續；D09人工QA等待最終版本。

- D10 A 已直接核對 Claude proposal f6033630／human1fc94f9d（12:55:59Z），停止品質修正，明列限制不改判PASS。50eab20（reviewed source f089cae＋docs tail）已 ff-only 整合，保留Main ai-log追加、簡報素材、QA10/QA11與原清單。接續固定Main checkpoint後一套完整測試及兩份快取實際命中；人工QA尚未執行。

- #11 Main db64d84 整合驗證：327 passed／3 eval deselected／zero skipped／263.68s；Main Python與imports、500/dense/5-3-2/medium/4及58005fcc pipeline已核對。兩份named current cache已移交Main `.cache/`，公開上傳均Ready、0 LLM/embedding/guarded calls。已核對完整log及環境／cache證據；不重跑N3、不把D10缺陷改判PASS。D09人工網站QA尚未執行，接續HTTP readiness與已合併資源收尾。

- #11 資源收尾完成：meme/Bela recorded tags 已停止，已合併50eab20 worktree及分支安全移除；8份歷史cache與9份工作context保留在ignored archive，開發暫存已移至Trash。Main兩份current cache、使用者8101服務、Ollama及無關8201保留。首頁／JS／CSS／字型HTTP200僅證明可載入，最終人工QA仍待D09回覆，#11維持ready-for-human；D11未派工。

- Main同session恢復：native01a134c5，latestturn01a135a6-f96a-76a2-91d3-87c771720414 actualgpt-6-astra/high/workspace-write/on-request已核對。#11整合與清理checkpoint b956247，無remote故push未成功。D11/D12已直接核對真人原文，#12正式建票；獨立前端實作由levi協調，Main不重複派工。D13未答，僅擋未核准Reviewer替代。D09原版人工回饋已直接核對user msg_01a13599及msg_01a1359e：Q3短表格接受、其餘正常；A9回答不出來尚無症狀細節，不自行歸因或改判全PASS。

- #12中間候選d7fd1d7（7441dbb／0e3619d／d7fd1d7）已由Main從Git核對存在且worktree clean，前端驗證證據已保存；levi尚未正式交付。native14:30顯示已啟動opus別名Reviewer，D13尚無直接真人答覆，Main已請levi核對／取得核准；不採未核准Review合併。既有Sonnet實作不阻擋，actual child metadata及最終修正待回。原版A9症狀仍待答，不重複提問或重跑品質eval。

- A9真人補充msg_01a135ba（14:46:13Z）直接核對為「回答找不到文件」，非已確認固定拒答；依既有diagnosing-bugs流程放行獨立nova-a9-dino在b956247分支做有界分類／重現，actualGPT6.1high/wswrite/onrequest已核對。不更動Main／8101、不重開N3或消融品質調整；#12／D13獨立推進。

- A9有界診斷完成：真人精確回答「文件中未提及」與9段Trace已核對；p.8 §4.3原文雜訊警語可支持回答，原拒答FAIL、原因UNPROVEN。一次獨立無歷史重跑未重現拒答，另發現系統重建警告被當成論文限制，grounding FAIL；2calls守10K、無source改動。報告已保存在docs/verification/ticket-11/manual-a9/；8330已關、工作樹clean。D14已先記pending並向真人詢問接受兩項明列限制或一輪有界修正；#12獨立推進，D13仍待答。

- D14 B真人「好，改」（msg_01a135cc／15:06:09Z）已直接核對preceding單一提案，核准一輪有界A9修正與回歸／真實模型／獨立Review；#13建票，不改消融、不寫死答案、不擴大調參。D13仍pending，不由本次答覆推定Reviewer替代同意。

- #12 D13/D15真人已直接核對，Main讀完整兩輪Review／paths並核對actualSonnet5.5high、Opus5.5medium及parentauto。af6b9f3已公告後ff-only整合、production與已審1c274e4不變；Main文件與A9診斷隨此checkpoint保存，接續一次Main完整suite及D09新版人工QA。#13freshsoho actual01a135d1-74a6 GPT6.1high/wswrite/onrequest已核對並放行local工作，provider暫候。

- #12 Main單次整合fullsuite327PASS／3eval deselected／zeroSKIP／252.49s／exit0已核對，Mainimports／設定／兩PDF正確；未重跑eval。8101新前端assets200、既有server保留；D1–D7已放行使用者，#12ready-for-human。soho已解除providerhold，接續#13boundedlive驗證／兩份新快取；A9尚未宣稱修好。

- #13固定候選eac9b07（sourceb236b10，baseMainabd7fc7）已核對clean／完整335PASS、3eval deselected、zeroSKIP；兩次fresh上傳均429，沒有Ready、新快取或新回答，實際語意／快取驗證仍blocked。唯一同source恢復已用完，provider停止。freshsoho-review-zeno/mima actualGPT6-solhigh/wswrite/onrequest兩軸已Main直接核對並放行完整#13diff審查；不宣稱smokePASS或提前合併。

- #13最終交接cd3c8aa已Main核對clean／abd7fc7祖先／相對已審eac9b07僅四份文件；完整Standards與Spec均無actionable code findings，兩軸各8targetedPASS。完整335PASS證據沿用同source。429阻擋的A9／無關支持與缺失題／兩份新快取維持NOT_EXECUTED，未合併、不宣稱已修好；原FAIL及原因UNPROVEN保留。soho與worktree保留供服務恢復後接續，子Reviewer已停止，8330無listener。

- D16新版人工回饋已直接核對msg_01a1379a及快捷題選擇msg_01a1379c，#12重開有界UI2–6；第1/7/8由原root對话討論，不先改prompt／文件外回答政策。原levi背景session idle、HCOMinactive，一次resume因背景session已運作而失敗；保留原使用者session，續接協調context使用同設定並開fresh實作／Review children。#13cd3c8aa仍獨立429blocked。

- D17直接真人核准文件限定政策＋自適應回答結構（msg_01a137a1）已核對完整precedingproposal；扩充未合併#13由soho順序接續，舊cd3c8aa Review／335PASS保留，新delta需fresh scopedReview／真实模型。有界provider確認不假定隔夜恢復；#12獨立進行。概覽警告中文化未核准，不混入。

- D17 c3b47fb已Main核對完整345PASS、一次preflight及5個完整Application答案／來源、兩份新快取；129calls最高9873/10K，1個摘要length丟棄後既有重試完成。完整獨立Review仍指出A9未支持的完整方法限制、Q2未逐項引用／未揭露不確定表格、Q3整張抄表未比較reference例外。Main放行D17必要的一輪通用指令呈現／回答契約修正，非新檢索／Overview調參；保留rawFAIL，新source必須fresh scopedReview與final boundedlive。前端f8abe50完整327PASS、browser65/0，兩軸Opus5.5medium actual已核對，Review進行中。

- #12 D16修正版ac1be36已ff-only整合；Main直接核對完整327PASS／3eval deselected／zeroSKIP／265.71s／exit0，Python與imports均Main工作區，兩份固定PDF存在，設定與58005fcc快取版本不變。fresh雙軸Review、75項browser結果已核對。原8101已無listener，Main以原已合併後端重新啟動，首頁／JS／CSS／字型HTTP200；D8–D11正式放行人工驗收，不標PASS。#13候選9715538未合併、D18仍待答；不追加品質迴圈。

- D21直接核對真人與原提案，已解除全GPTmedium角色待決；kune原前端實際提交8e15852移除Overview／label、相關來源中文警告，fresh兩軸GPTmedium runtime已核對。gera新隔離13-a9-routing actualGPT6.1medium/wswrite/onrequest已核對並正式放行，舊soho已停止且9715538原樣保留；前後端分離所有權，UI優先整合，沒有再要求使用者確認。

- D21介面7d3794a已ff-only整合，兩軸GPT6.1 medium限定Review零finding。Main讀完整報告／來源diff／桌面與窄螢幕圖片，獨立新舊版均發生來源Escape後Chromium停滯，保留FAIL與D14人工情境，不當成本delta回歸或全UI通過。A9純證據b0b7710一併保存，14calls最高7741，沒有任何實驗產品改動。Main完整測試接續；尚不宣告最終人工QA完成。

- D21整合驗證完成：Main fd1034f，完整327PASS／3eval deselected／zeroSKIP／269.93s／exit0。Main完整核對log、正確Python/import及固定PDF；原8101提供同版index／JS／CSS／字型HTTP200，沒有重啟後端。D9、D12–D14人工複驗放行，A9與窄螢幕既有FAIL仍保留。自有測試目錄與程序清理，角色收尾，worktree因明列未完人工／A9追查保留。

- D22真人已直接核對（msg_01a13850，02:48:51Z）：要求快速並行驗證A9主體／原文觀察／限定條件，先忽略窄螢幕。新gina真實實驗與muko獨立判讀，actualGPT6.1 medium/wswrite/onrequest已Main核對並放行；最多8次產品模型呼叫，來源／順序／題目／設定凍結，不改產品或部署。既有D21FAIL保留。

- D22診斷完成：1f0fd2d純證據已核對並整合，7次新gpt-oss呼叫均stop、零retry，最高預估7262／provider6610。完整／局部的中立抽取與原回答對照、支持／缺失控制均由獨立muko按原文判讀；局部抽取語意恢復不等於回答正確。沒有通過完整抽取的候選門檻，沒有產品改動／部署。結果見ticket-13/d22/probe/final-report.md與assessment/report.md。窄螢幕依真人D22先擱置；A9仍未解。兩個角色工作結束、無自有服務／暫存，原worktree與快取由Main保管。

- D23真人msg_01a13862明確核准最小快捷題替換，並說「不用驗證，我自己驗證」。委派已核對GPT6.1 medium rose，只改Shortcuts與Vite重建dist；tests／live／browser／HTTP／獨立Review／整合suite本次明確不執行，不再套舊流程攔阻。A9凍結列已知缺陷，#13本輪wontfix；D18結束為舊候選不採用。LangGraph只討論，尚未引入或實作。

- D23最小修改完成：rose將快捷題改成「這篇論文使用哪些資料集進行實驗？」；Vite build成功（690ms），重建dist。Main本機缺react-markdown，依原lockfile npm ci恢復依賴後完成artifact生成，沒有依賴檔改動。所有驗證按真人要求NOT_EXECUTED，不宣稱新題回答或引用PASS；既有服務讀取更新的dist，未做HTTP／瀏覽器檢查。
