# Chat with Document：需求導向測試清單（實作前草稿）

Status: in-progress (existing requirement checklist; evidence updated incrementally)

> 產生方式：先只依 `PRD.md`（50 條 user story、事件契約、測試決策）、`AGENTS.md`（硬數字、失敗處理、Golden Facts、交付）、`CONTEXT.md`（術語）與題目原文獨立列出情境，之後才對照 `issues/01..11` 填「對應票」欄。原始需求草稿保留；已實作範圍與目前驗證見 EXECUTION.md 及各列證據。
>
> 驗證方式縮寫：**DET** = deterministic pytest（假 LLM + 真 bge-m3，不呼叫雲端 LLM）；**EVAL** = `pytest -m eval`（真 gpt-oss，語意判定，不降低 AGENTS.md 已確認的驗收條件）；**UI** = 真實瀏覽器（web-design-engineer 驗收）；**HTTP** = HTTP / SSE 契約測試。
>
> 「對應票」中的 `GAP` 表示沒有任何票明確負責交付或驗證該需求（詳見文末）。

## A. 啟動與交付

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| ST-01 | Story 37；AGENTS「交付」「已定決策：後端/前端」；PRD 驗收 | 乾淨 clone；只裝 Python 與 uv；Ollama 開著並已有 `bge-m3`、已登入 gpt-oss cloud；機器上沒有 node／npm | 照 README 逐字執行安裝與啟動指令（一行指令啟動），瀏覽器開 localhost | 網站載入、可上傳；全程不需要 npm／vite；`frontend/dist/` 已在 git 內且與原始碼同步（重新 build 後 `git diff` 為空） | UI + DET（`git ls-files frontend/dist` 非空） | #01、#09、#11 | NOT_EXECUTED（實作前草稿） |
| ST-02 | Story 49；AGENTS「交付」 | 乾淨 clone，`data/` 無 PDF | 執行 `scripts/fetch_data.sh` 兩次 | 下載固定版本的 LightRAG（arXiv 2410.05779）與第二份文件；內容雜湊每次一致；`data/*.pdf`、`AI_Engineer_Job_intro_assignment_v4.pdf`、`.cache/` 不被 git 追蹤；README 寫明 Ollama 前置與資料外送 Ollama Cloud 的說明 | DET（雜湊／`git check-ignore`）+ 人工讀 README | #01、#10、#11 | NOT_EXECUTED（實作前草稿） |
| ST-03 | Story 15、「視覺設計」決策；PRD Frontend | 斷網（或封鎖外部網域）的瀏覽器 | 載入網站，檢視內文與中文字 | Noto Serif TC 從 repo 內字型檔載入（Network 面板無外部字型請求）；內文計算字級 15～16px；無裝飾性動畫（無 CSS transition／animation 於非必要元素） | UI | #09 | NOT_EXECUTED（實作前草稿） |

## B. 上傳、進度、概覽、快取

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| UP-01 | Story 1、2；PRD 事件契約「上傳」；AGENTS「上傳處理與快取」 | 服務已啟動，LightRAG 未被快取 | POST 上傳 PDF 並訂閱進度 SSE | 上傳請求立刻回應（不等處理完，數秒內）；`stage` 事件依序為 解析 → 切塊 → embedding → 摘要 n/N（n 單調遞增到 N）→ 完成；串流一定以 `ready`（附文件概覽）或 `error` 結束，且之後不再有事件 | HTTP + DET | #04、#05 | #04 PASS；#05 摘要/概覽 NOT_EXECUTED。 [QA #04](../../../docs/verification/ticket-04/qa/takeover-report.md)（d56e092 source / cd3e303；2026-10-13） |
| UP-02 | Story 2、4；AGENTS「上傳處理」 | 瀏覽器開啟首頁 | 選擇 LightRAG PDF 上傳，處理中觀察畫面 | 即時看到目前階段與 n/N 進度；提問框為停用狀態且旁邊有文字說明原因（例如「文件處理中」）；`ready` 之後提問框才啟用、原因文字消失 | UI | #04、#09 | PASS：真實 UI 0/41→8/41→ready，提問停用與原因。 [QA #04](../../../docs/verification/ticket-04/qa/takeover-report.md)（d56e092 source / cd3e303；2026-10-13） |
| UP-03 | Story 3、30 | UP-02 完成 | 看畫面，並連續提問數輪、捲動對話 | 完成時立即顯示「文件概覽」（Document Summary，內容非空且為全文層級）；整個對話期間仍看得到，不被對話擠掉 | UI | #05 | NOT_EXECUTED（實作前草稿） |
| UP-04 | Story 5；AGENTS「支援範圍」；PRD Parser | 測試中以程式產生「只有圖片、無文字層」的 PDF；另備一個損毀／非 PDF 檔 | 上傳該檔 | 上傳階段（非等到提問）就收到 `error` 事件，訊息說明「掃描檔／無文字層，不支援」；UI 顯示該原因、不卡在進度條；提問框仍停用；之後可立即重新上傳正常 PDF 成功。損毀檔同樣得到明確錯誤而非 500 空白頁 | DET + UI | #02（掃描檔）；損毀／非 PDF：GAP | PASS（#02 QA e59e096：scan/non-PDF/corrupt distinct errors + browser recovery；ticket-02/qa/takeover-report.md） |
| UP-05 | AGENTS「失敗處理」；PRD `error` 事件 | 以假 LLM／假 Embedder 注入：第 k 個 Section Summary 呼叫失敗、或 Embedder 連線失敗 | 上傳 PDF | 以 `error` 結束，不發 `ready`；UI 顯示錯誤並可重新上傳；不留下半成品快取（再次上傳會完整重跑） | DET + UI | #04（只有文字描述，無驗收項）；快取不留半成品：GAP | #04 embedding失敗/無半成品快取/重試 PASS；#05 summary失敗 NOT_EXECUTED。 [QA #04](../../../docs/verification/ticket-04/qa/takeover-report.md)（d56e092 source / cd3e303；2026-10-13） |
| UP-06 | Story 6、46；AGENTS「處理結果依雜湊值存到 .cache/」；PRD Ingestion Jobs | 假 LLM／假 Embedder 會計數；LightRAG 已處理過一次 | (a) 同一檔案再上傳；(b) 改一個位元組再上傳；(c) 把「處理流程版本」常數改掉再上傳同一檔 | (a) Embedder 與 LLM 呼叫次數皆為 0，直接進 `ready`，概覽與首次相同，UI 幾乎立刻完成；(b)(c) 重新處理；`.cache/` 內含 Chunk、embedding、Summary Tree，鍵含內容雜湊與流程版本 | DET + UI | #04、#05 | #04 cache/hash/version/config PASS；#05 Summary Tree NOT_EXECUTED。 [QA #04](../../../docs/verification/ticket-04/qa/takeover-report.md)（d56e092 source / cd3e303；2026-10-13） |
| UP-07 | AGENTS「只快取上傳時的處理結果，不快取回答」；Story 25 的前提 | 文件已 `ready`（含快取） | 對同一份文件連續問同一題兩次 | 兩次都真的呼叫 LLM（假 LLM 紀錄兩組呼叫）、兩次 Trace 各自獨立；`.cache/` 內沒有任何回答內容 | DET | GAP（無票涵蓋） | PASS：重問兩次真的呼叫 LLM，快取 bytes 不變。 [QA #04](../../../docs/verification/ticket-04/qa/takeover-report.md)（d56e092 source / cd3e303；2026-10-13） |
| UP-08 | PRD 流程步驟 1「完成後開放提問」；CONTEXT「一次只針對一份 Document」 | (a) 文件處理中；(b) 已有文件 A 的對話 | (a) 繞過 UI 直接 POST 提問；(b) 上傳文件 B | (a) 伺服器端拒絕（4xx／`error`），不進入檢索也不呼叫 LLM；(b) 對話區、概覽、Trace、引用彈窗全部切到文件 B，不殘留 A 的引用或歷史 | HTTP + UI | GAP（#04 只管 UI 停用） | #04 readiness/backend拒絕/切換重置 PASS；#05概覽 NOT_EXECUTED。 [QA #04](../../../docs/verification/ticket-04/qa/takeover-report.md)（d56e092 source / cd3e303；2026-10-13） |

## C. 解析與切塊

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| PA-01 | AGENTS「已驗證事實：章節標題」；「切塊規則」1、5、6 | LightRAG 已 `ready` | 檢視 Document 的 Section 清單與全部 Chunk | 偵測到 Introduction 到 Conclusion 的全部主章節（編號與標題分兩行也合併，如 `3` / `THE LIGHTRAG ARCHITECTURE`）與 Appendix；每個 Chunk 屬於且不跨越單一 Section，文字開頭帶 Section 標題，帶頁碼；沒有任何 Chunk 含 References 書目內容；附錄 Chunk 皆標 Appendix | DET | #02 | PASS（#02 QA e59e096：28 Sections/41 Chunks、References/Appendix/provenance；ticket-02/qa/takeover-report.md） |
| PA-02 | 切塊規則 2、3；Story 38；AGENTS「程式不能寫死字體大小」 | 測試中程式產生：(a) 不同字體大小／粗體標題的 PDF；(b) 含超過 500 tokens 單一長段落的 PDF；(c) 中英混合標點長段落；(d) 設定改為其他 Chunk 大小 | 上傳並檢視 Chunk | (a) 依「最常見字級為內文、較大或粗體為標題」偵測，不依賴 12pt 或 NimbusRomNo9L；(b) 只有該長段落在句子邊界切開，相鄰片段重疊約 10%，其餘 Chunk 以整段段落裝到約設定大小、段落間不重疊、且不超過設定大小；(c) 在 。！？ 與英文標點邊界切；(d) 設定值改變會改變切塊結果（可配置） | DET | #02、#10、#11（設定值）；可配置性：#02 一句話帶過 | PASS（#02 QA：160/160 facts、11 Chunks max498、256/500/800、相對字級與整段裝填；同報告） |
| PA-03 | 範圍「完全偵測不到標題」；CONTEXT「Section」 | 程式產生完全沒有標題的 PDF | 上傳後提問 | 以固定長度切出虛擬 Section，處理成功、可提問、有回答與引用（頁碼仍正確） | DET | #02 | PASS（#02 QA：6 virtual Sections、App + browser ask/source；同報告） |
| PA-04 | AGENTS「Section 超過 8,500 tokens 先切開，各自摘要，再合併」 | 程式產生單一 Section 超過 8,500 tokens 的 PDF | 上傳 | 該 Section 的摘要呼叫被拆成多次，每次 prompt ≤ 8,500、合計後再合併成一個 Section Summary；沒有 guard raise | DET | GAP（#05 未寫） | NOT_EXECUTED（實作前草稿） |

## D. 表格

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| TB-01 | 切塊規則 4；Story 11、12；Golden Facts Q3 | LightRAG 已 `ready` | 取出 Table 1、Table 2 的 Table Chunk | 每一格數字與論文一致（含 Table 2 中 Mix 的 `-Low` Overall 64.8、完整版 60.0；Agriculture `-Origin` 74.4、完整版 67.6；Table 1 Mix Overall 50.4 / 49.6）；內容含 caption，且多層欄標題寫明「資料集 × NaiveRAG／變體」「每格是 NaiveRAG 勝率／變體勝率」；p9 成本表沒有數學斜體殘留的 `_` | DET | #03 | NOT_EXECUTED（實作前草稿） |
| TB-02 | 切塊規則 4、7；Story 11；AGENTS「Q3 的前 5 名一定有 Table 2」 | 假 LLM 記錄 prompt；真 bge-m3 | 問 Q3 | 檢索前 5 名含 Table 2 的 Table Chunk；回答 prompt 同時含 Table 2 與 §4.3 討論它的段落（以 Table 2 與「Table 2」提及處互相連結帶出）；Chunk 依原文順序、各標 `[C#]` 與頁碼、Section；Table Chunk 與 Table 內文鄰居未使額度超過 | DET | #03（連結）、#01（Lookup 前 5） | NOT_EXECUTED（實作前草稿） |
| TB-03 | 切塊規則 4（失敗保留）；Story 29 | 程式產生結構不規則、無法可靠重建的表格 PDF；假 LLM 腳本讓回答引用該 Table Chunk | 上傳 → 提問該表格 | Table Chunk 保留原始文字並帶「結構未能可靠重建」標記；回答（prompt 規則）說明此限制；UI 點開引用時顯示限制提示；不發生 LLM 重排表格的呼叫 | DET + UI | #03 | NOT_EXECUTED（實作前草稿） |
| TB-04 | 切塊規則 4（>2,000 tokens）；「放不下時怎麼辦」 | 程式產生超過 2,000 tokens 的表格 PDF | 上傳 | 依列分段，每段都重複表頭與 caption，每段 ≤ 2,000 tokens，各段都可被檢索與引用 | DET | #03 | NOT_EXECUTED（實作前草稿） |

## E. Summary Tree

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| SM-01 | AGENTS「摘要規則」；Story 3 | LightRAG 上傳；假 LLM 記錄呼叫；另以真 LLM 跑一次 | 檢視 Summary Tree 與每次摘要呼叫 | 假 LLM：每個 Section Summary 呼叫的長度要求為原文 15%，夾在 80～500 tokens（短章節取 80、長章節取 500）、`think=low`、預留 1,200；真 LLM（EVAL）：實際輸出長度落在合理範圍且保留數字；總和約 3K，因此不產生 Group Summary，Document Summary 為最頂層 | DET + EVAL | #05 | NOT_EXECUTED（實作前草稿） |
| SM-02 | Story 39；摘要規則「Group Summary」；「Section Summary 加起來超過 6,000 tokens 時建立 Group Summary」 | 程式產生很多 Section、Section Summary 合計 > 6,000 tokens 的 PDF（及第二份真實長文件） | 上傳並提問 Global 題 | 建出至少 1 層 Group Summary（相鄰 Section 分組、逐層合併到放得下）；Group／Document Summary 呼叫為 `low`、預留 2,500、prompt ≤ 7,200；Global 回答使用「放得進額度的最詳細那一層」；所有呼叫 ≤ 10,000；進度顯示「摘要 n/N」含各層 | DET | #05、#10 | NOT_EXECUTED（實作前草稿） |
| SM-03 | AGENTS「來源要能一路追溯回原文」 | 同 SM-01／SM-02 | 檢查節點 metadata | Section Summary 記錄所屬 Section 的全部 Chunk 編號；Group Summary 記錄涵蓋的 Section；沿 Document → Group → Section 可一路追回 Chunk | DET | #05 | NOT_EXECUTED（實作前草稿） |
| SM-04 | AGENTS「Section Summary 平行產生，同時呼叫數預設 4，可調整」 | 假 LLM 對每次呼叫延遲並記錄同時進行數 | 上傳多 Section 文件；再把設定改為 2 | 最大同時呼叫數 ≤ 4（改設定後 ≤ 2）；進度 n/N 隨完成遞增；結果順序與 Section 順序一致、與完成順序無關 | DET | #05（只有文字描述，無驗收項） | NOT_EXECUTED（實作前草稿） |

## F. Router 與檢索

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| RT-01 | Story 31；AGENTS「問題分流」；PRD Router | 文件 `ready` | 問任一題，檢查 `plan` 事件與假 LLM 紀錄 | 恰一次 router 呼叫：`think=low`、輸出預留 600、prompt ≤ 9,100、JSON schema 輸出；`plan` 含 Question Type（只有 Global／Synthesis／Lookup 三種）、Standalone Question、Sub-queries（只有 Synthesis 非空）；Router prompt 含「不確定時選 Synthesis」規則 | DET + HTTP | #06；#01 的 `plan` 固定 Lookup | NOT_EXECUTED（實作前草稿） |
| RT-02 | AGENTS「Router 在不同 think 等級」；Testing Decisions | 真 gpt-oss；`spikes/think_level_probe.py` 的 12 題轉成回歸資料 | `pytest -m eval` router 回歸 | 12 題各自的 Question Type 與標準答案比對，正確率不低於實測基準 11/12；出錯題只能是「Lookup 誤判為 Synthesis」方向（反向為不合格）；報告列出每題判定與 token／延遲 | EVAL | #06、#08 | NOT_EXECUTED（實作前草稿） |
| RT-03 | AGENTS「Router 失敗」；Testing Decisions | 假 LLM router 回傳壞掉的 JSON（含缺欄位、非 JSON、類型不在三者之內） | 提問 | 不報錯，退回 Lookup：`plan` 顯示 Lookup，用原問題檢索前 5 名，仍產出回答與 `final` | DET | #06 | NOT_EXECUTED（實作前草稿） |
| RT-04 | Story 21；AGENTS「對話歷史只帶最近 2 輪，每輪截到 500 tokens」 | 已進行 5 輪對話，其中前幾輪回答很長 | 第 6 輪提問，檢查 router prompt | 歷史只含最近 2 輪，每輪 ≤ 500 tokens；router 呼叫仍 ≤ 9,100 prompt；不引入對話歷史摘要的 LLM 呼叫 | DET | #06 | NOT_EXECUTED（實作前草稿） |
| RT-05 | AGENTS「問題超過 1,000 tokens」；Story 28 | 文件 `ready`；問題 1,001 tokens 與恰好 1,000 tokens 各一 | 送出問題 | 1,001 tokens：不呼叫任何 LLM／Embedder（呼叫數 0），收到拒絕事件，UI 顯示原因（問題太長、上限 1,000 tokens），輸入內容保留讓使用者縮短；1,000 tokens：正常處理 | DET + UI | #06（拒絕事件型別未列入 PRD 事件契約，見 GAP） | NOT_EXECUTED（實作前草稿） |
| RV-01 | AGENTS「檢索規則」Synthesis；Golden Facts Q2 | 真 bge-m3；假 LLM 照劇本給 Q2 的 Standalone Question 與 Sub-queries（成本、增量更新、檢索方式、勝率、case study） | 問 Q2 | 檢索 = Standalone Question 前 3 + 每個 Sub-query 前 2，合併去重；結果涵蓋成本分析段落（GraphRAG 約 610×1,000 tokens、LightRAG < 100 tokens／1 次 call）與增量更新段落；不含 Section Summary；Chunk 依原文順序 | DET | #06 | NOT_EXECUTED（實作前草稿） |
| RV-02 | AGENTS「檢索規則」Global；Story 7 | 文件 `ready`；假 LLM router 回 Global | 問 Q1 | 不做 Chunk 檢索（`retrieval` 無 Chunk 或為摘要層清單）；回答 prompt 以 `[S#]` 標示的 Summary Tree 層（LightRAG 為 Section Summary 層）組成，prompt ≤ 6,700；呼叫為 `medium`、預留 3,000 | DET | #05（#06 合併前 Global 暫走 Synthesis） | NOT_EXECUTED（實作前草稿） |
| RV-03 | AGENTS「Synthesis 超過 6,000 tokens 時改用分批抽取」；「抽取出來的事實超過 6,000 tokens → 再合併一次」 | 把 top-k 設大或使用長文件，使檢索內容 > 6,000 tokens；再構造抽取結果也 > 6,000 | 提問 | 先分批抽取（`low`、預留 1,000、prompt ≤ 8,700），每條事實保留 `[C#]`；事實仍放不下則再分批合併一次；最終回答呼叫 ≤ 6,700 prompt；最後回答中的每個 `[C#]` 都能對回原始 Chunk（頁碼／Section 正確） | DET | #06 | NOT_EXECUTED（實作前草稿） |
| RV-04 | Story 47；AGENTS「前 5／3／2 是起始值」 | 修改設定：Lookup top-k、Synthesis 的 3／2、Chunk 大小、各呼叫 think 等級 | 重新處理並提問 | 設定改變即反映在檢索筆數、Trace 與呼叫紀錄（think 等級）上，不需改程式碼 | DET | #02（Chunk 大小）、#11（實驗）；top-k／think 可配置：GAP | NOT_EXECUTED（實作前草稿） |

## G. Context Budget 與 LLM Gateway

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| BG-01 | 硬限制 2；Story 32、45；PRD 假 LLM 紀錄 | 假 LLM 記錄所有呼叫；跑完整流程：上傳 LightRAG + 長文件 + Q1／Q2／Q3 + 追問 + 重試路徑 + eval judge | 檢查紀錄 | 每次呼叫：估算 prompt tokens（含 `o200k_harmony` 計數、300 邊際、模板開銷）+ `num_predict` ≤ 10,000；且各呼叫類型的 think／預留／prompt 上限完全等於 AGENTS 預算表（Router 600／9,100；Section 1,200／8,500；Group 與 Document 2,500／7,200；分批抽取 1,000／8,700；回答 medium 3,000／6,700；Judge 1,000／8,700） | DET | #01（通用）、#05、#06；Judge：#08 未明列 | NOT_EXECUTED（實作前草稿） |
| BG-02 | AGENTS「budget guard 超過就 raise，不靜默截斷」；「guard 一旦 raise 就代表上游有 bug」 | 將某類呼叫額度設到必超（或餵超長 prompt） | (a) 直接透過 Gateway 呼叫；(b) 透過提問操作 | (a) raise，prompt 未被截斷也未送出網路請求；(b) 發出 `error` 事件、不發 `final`、UI 顯示錯誤（不是半截答案）；錯誤訊息可辨識為預算超限 | DET + HTTP | #01 | NOT_EXECUTED（實作前草稿） |
| BG-03 | Story 33、34、50；AGENTS「對話模板有額外開銷」 | 真 gpt-oss 跑 Q1～Q3 | 讀每次呼叫的 Trace 紀錄 | 每筆含：呼叫類型、think 等級、輸出預留、估算 tokens、模型回報 `prompt_eval_count`、`eval_count`、思考內容（若有）、延遲、`done_reason`；估算值 ≥ `prompt_eval_count`（保守）；兩者並列顯示 | EVAL + DET（欄位齊全） | #01 | NOT_EXECUTED（實作前草稿） |
| BG-04 | Story 48；PRD LLM Gateway | 以「假 LLM adapter」整套替換真 adapter | 跑上傳與 Q1～Q3 | 只替換一個 adapter 即可完整運作，事件契約與使用真 LLM 時相同；假 LLM 能照劇本回應並記錄呼叫 | DET | #01 | NOT_EXECUTED（實作前草稿） |

## H. 失敗處理與事件契約

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| FL-01 | Story 25；AGENTS「done_reason=length 就算失敗，即使已有內容」 | 假 LLM：第一次回答先吐部分內容再 `done_reason=length`，第二次成功 | 提問 | 事件：`delta`… → `retry` → `delta`… → `final`；重試呼叫為 `think=low`；`final` 只含第二次內容；UI 收到 `retry` 後清掉原暫定文字並顯示「重新產生中」，最後以重試結果取代；Trace 記錄兩次呼叫 | DET + UI | #07 | NOT_EXECUTED（實作前草稿） |
| FL-02 | Story 26 | 假 LLM：兩次皆 `done_reason=length`（其中一次有內容） | 提問 | 最後事件為 `error`，沒有 `final`；UI 顯示錯誤訊息，畫面上不殘留任何半截答案或暫定文字 | DET + UI | #07 | NOT_EXECUTED（實作前草稿） |
| FL-03 | Story 24；AGENTS「串流文字先標示為暫定」 | 真 LLM 或慢速假 LLM | 提問並於串流中途截圖，再等到完成 | 串流中文字有明顯「暫定」樣式；收到 `final` 後樣式變為定稿，文字與 `final` 內容一致；中途不得有定稿樣式 | UI | #07、#09 | NOT_EXECUTED（實作前草稿） |
| FL-04 | Story 18；AGENTS「引用 prompt 裡沒有的編號」 | 假 LLM 回答含 `[C99]`（以及同時含有效 `[C1]` 的另一句） | 提問 | `final` 中含 `[C99]` 的句子被標 Unverified、該編號被移除、有效引用保留且對應正確頁碼；UI 在該句顯示 Unverified 標記；Trace 的無效引用數 = 1；沒有靜默刪句 | DET + UI | #07 | NOT_EXECUTED（實作前草稿） |
| FL-05 | CONTEXT「Citation：找不到有效來源的句子標記為 Unverified」；Story 14 | 假 LLM 回答含一句完全沒有 `[C#]`／`[S#]` 的事實句，以及固定的「文件中未提及」句 | 提問 | D01 已核准：只有引用不存在編號的句子標 Unverified；完全未附編號與固定拒答不標，prompt 要求論點附引用 | DET + UI | GAP（#07 只覆蓋「不存在的編號」） | NOT_EXECUTED（實作前草稿） |
| FL-06 | Story 27；AGENTS「Router 失敗：連線失敗或逾時不繼續檢索」 | 分別讓 Router、Embedder（查詢時）、回答 LLM（串流中途）連線失敗或逾時 | 提問；之後恢復服務並按重試鈕 | 三種都發出 `error`：Router／Embedder 失敗時不進入檢索或回答，沒有 `final`；UI 顯示錯誤訊息與重試按鈕；按鈕重新送出同一題並成功完成，畫面不殘留舊的錯誤與暫定文字；JSON 壞掉不屬此類（見 RT-03） | DET + UI | #07 | NOT_EXECUTED（實作前草稿） |
| FL-07 | PRD 事件契約；Story 22、23、35 | 真 LLM 與假 LLM 各跑一次 | 對提問 SSE 做契約檢查；比對前端 TypeScript 型別與後端事件模型 | 事件順序為 `plan` → `retrieval` → `citation_map` → [`thinking`] → `delta`… → [`retry`…] → `final` → `trace`，任一步可改發 `error` 並終止；`thinking` 沒有時前端不出錯；`citation_map` 在第一個 `delta` 之前；前端 TS 型別與後端模型一致（由後端模型產生或 CI 型別檢查）；`retry` 後的 `delta` 重新開始 | HTTP + DET | #01（順序、型別）、#07（retry）；`thinking` 事件：GAP | NOT_EXECUTED（實作前草稿） |

## I. Citation 與來源檢視

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| CT-01 | Story 14、15、16；AGENTS「用短編號引用」 | Q3 回答完成 | 看頁邊；點 `[C#]`；用 PyMuPDF 在原 PDF 該頁搜尋彈窗文字；另對不存在編號呼叫來源查詢端點 | 每個引用在頁邊旁註顯示「p.N §Section」；點擊彈出該 Chunk 原文（Table Chunk 以表格形式顯示）；彈窗文字確實出現在其標示的頁碼；模型只寫編號，位置字串由後端對照表產生（假 LLM 寫出錯誤的「p.9」字樣也不影響對照結果）；未知編號回 404 而非崩潰 | UI + HTTP + DET | #01（彈窗）、#02（旁註含頁碼與 Section）、#03（表格形式）、#09；404：GAP | PASS（#02 範圍：旁註頁碼/Section、原文/provenance/source404；ticket-02/qa/takeover-report.md）；表格格式仍待 #03 QA、彈窗完整頁碼標題待 #09 |
| CT-02 | Story 17；AGENTS「`[S#]` 點下去顯示該 Section 的頁碼範圍和摘要」 | Q1 回答完成 | 點 `[S#]` | 顯示該 Section 的頁碼範圍與其 Section Summary；Group 層則顯示涵蓋的 Section 清單；不做逐句追溯 | UI | #05 | NOT_EXECUTED（實作前草稿） |
| CT-03 | Story 22；AGENTS「開始產生回答前先傳對照表」 | 串流進行中 | 在第一個 `delta` 剛出現、尚未 `final` 時點 `[C3]` | `[C3]` 已是可點的引用並能開啟正確來源，不必等 `final` | UI | #01 | NOT_EXECUTED（實作前草稿） |

## J. 端到端問答（含 Golden Facts）

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| QA-01 | 題目 Q1；Story 7；Golden Facts Q1 | LightRAG `ready` | 問「Summary this document.」 | Question Type = Global；回答語意涵蓋：問題動機、graph-based indexing、dual-level retrieval、增量更新、實驗設定與結果、結論（judge 必須逐字摘錄證據句）；以 `[S#]` 引用；`done_reason` 非 length；所有呼叫 ≤ 10K | EVAL + UI | #05、#08 | NOT_EXECUTED（實作前草稿） |
| QA-02 | Story 8 | 同上 | 問「用三句話、中文總結這份文件」 | 回答為中文、恰三句、仍涵蓋全文要點並附 `[S#]`；證明回答是依問題格式即時生成而非直接回傳預存摘要 | EVAL | #05、#08 | NOT_EXECUTED（實作前草稿） |
| QA-03 | 題目 Q2；Story 9；Golden Facts Q2 | 同上 | 問「Compare LightRAG with GraphRAG.」 | Question Type = Synthesis；涵蓋：檢索方式（GraphRAG community 遍歷 vs LightRAG dual-level keyword）、成本（610×1,000 tokens vs < 100 tokens 且 1 次 call）、增量更新（GraphRAG 需重建 community）、Table 1 勝率、Table 3 case study；forbidden：「LightRAG 在所有資料集都勝過 GraphRAG」（Mix Overall 實為 GraphRAG 50.4% / LightRAG 49.6%）；數字帶上下文判定；引用 `[C#]` 皆有效 | EVAL + UI | #06、#08（forbidden 寫入 #08） | NOT_EXECUTED（實作前草稿） |
| QA-04 | 題目 Q3；Story 11–13；Golden Facts Q3 | 同上 | 問「Performance of ablated versions of LightRAG.」 | 引用 Table 2 並先說明比較基準（各變體對 NaiveRAG 的勝率）再下結論；點出 Mix 上 `-Low` Overall 64.8% 高於完整版 60.0%、Agriculture 上 `-Origin` 74.4% 高於完整版 67.6%（變體、資料集、指標、數值、方向都對得上）；forbidden：「完整版 LightRAG 在所有資料集、所有指標都最好」；連字號 U+2011 已正規化後才比對 | EVAL + UI | #03、#08 | NOT_EXECUTED（實作前草稿） |
| QA-05 | Story 19；AGENTS「文件中沒有答案的問題：準備 3 題」 | LightRAG `ready` | 問「LightRAG 在 HotpotQA 上的分數」「LightRAG 的授權條款」與第三題（文件外事實） | 回答為固定的「文件中未提及」，不補任何編造的數字或內容、無無根據引用；Trace 記錄最高相似度分數；英文問題時的固定句語言依產品決定（見 GAP） | EVAL + UI | #08（題目）；#01 的 prompt 規則；語言：GAP | NOT_EXECUTED（實作前草稿） |
| QA-06 | Story 20；AGENTS「用提問的語言回答，引用的數字保持原樣」 | LightRAG `ready` | 以中文問「LightRAG 和 GraphRAG 的成本差異」 | 回答為中文，檢索到英文內文；引用的數字（如 610、1,000、< 100）與標點／單位保持原樣；`[C#]` 有效 | EVAL + UI | #01（prompt 規則）；評估題：GAP | NOT_EXECUTED（實作前草稿） |
| QA-07 | Story 10；CONTEXT「Question Type：有什麼限制不是比較卻需要跨 Section」 | LightRAG `ready` | 問「這篇論文有什麼限制？」 | Question Type = Synthesis（非 Lookup 亦非 Global）；回答彙整多個 Section 的資訊並附跨 Section 的引用；文件未寫的限制不得編造 | EVAL + UI | #06；Golden Facts：GAP | NOT_EXECUTED（實作前草稿） |
| QA-08 | Story 21；AGENTS「多輪對話只做追問改寫」 | 已問過 Q2 或「LightRAG 如何做增量更新？」 | 追問「那 GraphRAG 呢？」 | `plan` 的 Standalone Question 為不看前文也能理解的完整問題（含 GraphRAG 與增量更新）；回答依此檢索，且不是只重複上一輪內容；回答 LLM 的 prompt 不含對話歷史摘要 | EVAL + DET（假 router 驗證改寫被採用） | #06 | NOT_EXECUTED（實作前草稿） |
| QA-09 | 全部主流程；Story 1–3、7、9、11、14–16、31–32 | 乾淨啟動，瀏覽器 | 上傳 LightRAG → 看進度 → 概覽 → 依序問 Q1、Q2、Q3 → 點引用 → 開 Trace → 追問 | 一條龍無卡關、無 console error、無失敗的網路請求；每題先顯示階段（判斷問題類型 → 檢索 → 思考中）再逐字出現回答；回答開始前不是空白等待；全程截圖留存供 demo | UI | 全部票（#11 最終驗收） | NOT_EXECUTED（實作前草稿） |

## K. Trace 面板與介面狀態

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| TR-01 | Story 31、34、36；PRD 目標 4 | Q2 回答完成 | 開 Trace | 顯示 Question Type、Standalone Question、Sub-queries、檢索到的 Chunk 與相似度分數（順序與去重後一致）、每次 LLM 呼叫（Router、必要時分批抽取、回答）的 think、輸出預留、估算 tokens、`prompt_eval_count`；Q3 時（Lookup）無 Sub-queries | UI | #01、#06 | NOT_EXECUTED（實作前草稿） |
| TR-02 | Story 32；AGENTS「Trace 用迷你長條，以 10K 為滿格」 | 已有多筆呼叫（含接近滿額的呼叫） | 檢視長條 | 長條寬度 = (prompt + 輸出預留) / 10,000 的比例（DOM 寬度可量測），任何呼叫不超過滿格；有可辨識的 10K 刻度 | UI | #01、#09 | NOT_EXECUTED（實作前草稿） |
| TR-03 | Story 35；AGENTS「思考內容放在 Trace，預設收合」 | 回答含思考內容的一題；另一題無 `thinking` 事件 | 看 Trace、展開思考 | 預設收合；點開可見思考內容；無思考時不顯示空面板且不報錯 | UI | #09（元件）；`thinking` 事件由誰發出：GAP | NOT_EXECUTED（實作前草稿） |
| TR-04 | AGENTS「Trace 同時記錄無效引用數與最高相似度」 | FL-04 與 QA-05 的情境 | 看 Trace | 無效引用數、最高相似度分數都可見 | UI + DET | #07（引用數）；最高相似度：#01 的 retrieval 分數間接涵蓋 | NOT_EXECUTED（實作前草稿） |
| UX-01 | Story 22、23；AGENTS「串流」 | 慢速回答 | 提問後逐秒觀察 | 階段依序顯示 判斷問題類型 → 檢索 → 思考中 → 回答逐字出現；階段指示在 1 秒內出現；`delta` 為增量而非一次吐出全文 | UI | #06（階段）、#01（逐字） | NOT_EXECUTED（實作前草稿） |
| UX-02 | AGENTS「因為要分享螢幕 demo」；「視覺設計」決策 | 1440×900 與 1280×720 視窗；Q2 長回答與多旁註 | 檢視版面 | 頁邊旁註不與內文重疊、無橫向捲軸、Trace 不遮住對話；樣式為 Tufte 風格（非深色聊天介面）；長回答時引用旁註與所屬句子對齊 | UI | #09 | NOT_EXECUTED（實作前草稿） |
| UX-03 | #09 的人工流程；AGENTS「設計前先載入 web-design-engineer」 | 設計初稿 | 給使用者檢視 | 使用者確認方向後才定稿；共用元件（旁註、彈窗、10K 長條、階段、暫定、重試／錯誤、Unverified、收合思考、上傳進度）全數存在且被實際使用 | 人工 + UI | #09 | 人工方向確認 PASS（D02 v1，使用者「同意，照此方向定稿」）；定稿共用元件/UI 待 #09。 |

## L. Eval harness 本身

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| EV-01 | AGENTS「驗收：contains」；已驗證事實 U+2011 | 固定回答 + 假 judge | 跑 `contains` 檢查邏輯 | `‑High`（U+2011）、全形／半形百分比、`67.6 %` 與 `67.6%`、空白差異都被正規化後匹配；`contains` 規格若用來檢查數字，harness 拒絕或警告（數字只能走 judge） | DET | #08（U+2011、`67.6 %`）；「數字不得用 contains」的防呆：GAP | NOT_EXECUTED（實作前草稿） |
| EV-02 | AGENTS「judge 必須逐字摘錄證據句」「數字須同時對上變體、資料集、指標、數值、比較方向」 | 固定回答 + 假 judge | (a) judge 回傳不在回答中的證據句；(b) 回答只寫「`-High` 的 64.8」，fact 為「Mix 上 `-Low` 是 64.8」；(c) 正確回答 | (a)(b) 判定失敗；(c) 通過；judge 呼叫 `think=low`、預留 1,000、prompt ≤ 8,700（回答與 fact 清單放得進） | DET | #08 | NOT_EXECUTED（實作前草稿） |
| EV-03 | AGENTS「反向檢查 forbidden」 | 固定回答 + 假 judge；真 judge 的語意樣本 | (a) 回答含「完整版在所有資料集、所有指標都最好」；(b) 回答明確否定該說法（例如指出 Mix 上 `-Low` 較高） | (a) judge 能摘錄該錯誤結論 → fail；(b) 不應誤判為出現 forbidden claim（語意判定，不靠關鍵字） | DET（假 judge）+ EVAL（語意樣本） | #08（forbidden 邏輯）；否定句誤判樣本：GAP | NOT_EXECUTED（實作前草稿） |
| EV-04 | Story 40、42、43；AGENTS「每次跑完把報告寫到 eval/reports/」 | 真 gpt-oss | 一個指令跑 `pytest -m eval`，再以 N=3 重跑 | `eval/reports/` 產生 markdown 報告：每條 fact 通過與否、每次呼叫 token 用量與延遲、Question Type、`done_reason`；預設每題 1 次，N=3 顯示每條 fact 通過率；基準報告 commit，通過狀況如實記錄（不要求全過）；所有 eval 執行中正式額度（router 600、回答 3,000）無截斷 | EVAL | #08、#11 | NOT_EXECUTED（實作前草稿） |
| EV-05 | Story 41；AGENTS「確定性測試……幾秒內跑完」 | 無雲端連線、僅本機 Ollama（bge-m3） | 執行預設 `pytest` | 不選到 eval 測試、不呼叫任何雲端 LLM；以 `-m eval` 才跑 eval；整體在數秒～數十秒內完成；Ollama 沒開時錯誤訊息明確指出缺 bge-m3／daemon | DET | #01、#08（marker 與預設排除未明列：GAP） | NOT_EXECUTED（實作前草稿） |
| EV-06 | Story 47；PRD「調參實驗也透過 eval」；AGENTS「BM25 是否加入由 eval 決定」 | eval 可跑 | 依 #11 的實驗項目跑 Chunk 大小 256／500／800、top-k、加權 BM25 hybrid vs 純 dense、回答 `low` vs `medium`、Ollama Cloud 同時呼叫數 | 實驗結果表寫入 eval 報告；採用的設定寫回 AGENTS.md；過程觀察寫進 `docs/ai-log.md`（建議被推翻、AI 寫錯、人改方向各一筆以上則如實記錄） | EVAL + 人工審閱 | #11 | NOT_EXECUTED（實作前草稿） |

## M. 第二份文件與泛化

| ID | 來源 | 前置條件 | 操作／觸發 | 預期可見結果 | 驗證方式 | 對應票 | 證據與判定 |
|---|---|---|---|---|---|---|---|
| D2-01 | Story 38、39、49；AGENTS「第二份測試文件」 | 下載腳本已加入第二份文件 | 取得文件並檢查條件 | 為 2026 年 arXiv 論文、雙欄、含附錄 ≥ 40 頁、主題非 RAG；版本固定可重現；選擇理由記錄在文件中 | DET + 人工 | #10 | NOT_EXECUTED（實作前草稿） |
| D2-02 | Story 38、39；#10 驗證四件事 | 第二份文件上傳 | 看進度、報告與 Trace | 章節偵測合理（報告記錄偵測到的 Section 數）；Group Summary 至少 1 層（Section Summary 合計 > 6,000 tokens）；進度顯示摘要 n/N；所有呼叫 ≤ 10K；Global 題使用 Group 層，Trace 可見使用的層級；問題與修正記錄進 ai-log | EVAL + UI | #10 | NOT_EXECUTED（實作前草稿） |
| D2-03 | AGENTS「為它寫 2～3 條 Golden Facts：一個數字題、一個摘要題」 | 第二份文件 `ready` | 跑其 Golden Facts | 數字題（含上下文，judge）與摘要題通過；無編造；引用頁碼對得上該文件 | EVAL | #10、#08 | NOT_EXECUTED（實作前草稿） |
| D2-04 | AGENTS「中文 PDF 是加分項」；Story 38 | 一份有文字層的中文 PDF | 上傳後用中文提問 | 斷句在 。！？ 處；Section 偵測合理；回答為中文並附有效引用；若通不過，限制被如實記錄而不影響必做項 | UI + EVAL | #10（加分項） | NOT_EXECUTED（實作前草稿） |
| D2-05 | 交付；#11 驗收 | 乾淨 clone，照 README | 啟動後上傳兩份文件各一次 | 兩份文件的 `.cache/` 已預先建好，demo 時重新上傳秒開；Q1～Q3 於 N=3 的通過率（含 forbidden）已列在最終報告 | UI + EVAL | #11 | NOT_EXECUTED（實作前草稿） |

---

**列數：** 73 列（ST 3、UP 8、PA 4、TB 4、SM 4、RT 5、RV 4、BG 4、FL 7、CT 3、QA 9、TR 4、UX 3、EV 6、D2 5；TR 與 UX 同屬 K 節）。

## 附錄：對照票面後的 GAPs 與落差

### 需求沒有任何票負責（GAP）

1. **伺服器端狀態防呆**（UP-08）：處理中直接 POST 提問、換新文件時清掉舊文件的對話狀態，票只管 UI 停用。
2. **損毀／非 PDF 檔**的錯誤（UP-04）、**上傳中途失敗**不留半成品快取（UP-05）：#04 只一句話提到 `error`，無驗收項。
3. **回答不快取**的測試（UP-07）。
4. **Section > 8,500 tokens 先切開再摘要**（PA-04）：AGENTS 有規則，#05 沒寫。
5. **`thinking` 事件**（FL-07、TR-03）：PRD 契約有，#01 發出的事件清單沒有，#09 只做收合元件；沒有票負責實際發出思考內容。
6. **問題過長的拒絕事件型別**（RT-05）：#06 說「拒絕事件」，但 PRD 事件契約沒定義這個事件，前後端型別對齊（FL-07）會有缺口。
7. **無引用的事實句是否標 Unverified**（FL-05）：CONTEXT 與 #07 的範圍不一致，需決策。
8. **「文件中未提及」固定句在英文問題下的語言**（QA-05）：AGENTS 規定固定句，同時規定用提問語言回答，兩者衝突，需決策。
9. **中文問題對英文文件的 eval 題**（QA-06）、**「有什麼限制」的 Golden Facts**（QA-07）：Story 10、20 無評估題。
10. **top-k 與 think 等級可配置**（RV-04）：Story 47 要求，只有 Chunk 大小在 #02 明列。
11. **`contains` 不可檢查數字的防呆**、**forbidden 對否定句不誤判**、**Judge 預算納入 guard**（EV-01～03）。
12. **eval 預設排除（marker）與 `pytest` 速度**（EV-05）：#08 只要求一個指令跑 eval。
13. **來源查詢端點對未知編號的行為**（CT-01）。

### 票面有、獨立草稿原先未列出的項目（已併入上表或需補強）

- #08「第一份基準報告 commit，通過情況如實記錄」（已併 EV-04）。
- #11 的實驗結果表、Ollama Cloud 同時呼叫數實測、「無截斷」確認（已併 EV-04／EV-06）。
- #09「初稿須經使用者確認」的人工關卡與 ai-log 紀錄要求（已併 UX-03、D2-02、EV-06）。
- #02「Citation 旁註顯示頁碼與 Section」（CT-01 已涵蓋）；#02 對無標題 PDF「並且可以提問」（PA-03 已涵蓋）。
- #05 Group Summary 情境下「假 LLM 每次呼叫 ≤ 10,000」與 #06 合併前 Global 暫走 Synthesis 的過渡行為（RV-02 備註）：票之間的暫時行為，整合後須再跑一次 QA-01。
