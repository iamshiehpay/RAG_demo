# AI 協作紀錄

簡報素材。每筆記錄：發生什麼、怎麼發現、學到什麼。

## 2026-10-12：讀題與實測

- **讀原始 PDF，不只讀整理過的 md。** md 已經忠實整理了題目，但 PDF 前面的公司介紹透露了兩件事：團隊 roadmap 寫的是 SDD / TDD / Checkpoint，內部用的模型是 `gpt-oss-120b`。因此開發流程和 LLM 選型都對齊這兩點。
- **AI 的建議被實測推翻：** AI 原本建議「Ollama 設 `num_ctx=10240`，讓 10K 限制在物理上成立」。實測發現 Ollama Cloud 會忽略 `num_ctx`，4K tokens 的 prompt 在 `num_ctx=1024` 下照樣全收。教訓：AI 對 API 行為的說法要先驗證，再寫進設計。
- **實測抓到一個隱藏的坑：** gpt-oss 的思考過程算在 `num_predict` 裡。設 `think="high"`、`num_predict=200` 時，回答是空的。如果沒實測，budget guard 會漏算思考 tokens。
- **AI 預期的工具行為不成立：** AI 預期 `find_tables()` 能抽出論文表格，實測卻漏掉了 Q3 最需要的 Table 1 和 Table 2（無框線表格）。改成用文字座標重建表格。
- **AI 第一版的章節偵測失敗：** 用正則抓編號標題，結果一個都沒抓到，因為編號和標題分在兩行。改成用字體大小（12pt）偵測。
- **人決定範圍：** AI 排了 7 天計畫，人把時程砍成 2 天。
- **Embedding 選型改用數據決定：** 在論文上用 12 個中英文問題做 bake-off，MRR 結果為 `bge-m3` 0.708 > `embeddinggemma` 0.583 > `qwen3-embedding:0.6b` 0.558 > BM25 0.408。公開排行榜上較新的 `qwen3-embedding`，在這份文件上反而輸給 `bge-m3`。另外，「hybrid 一定比較好」的直覺也被推翻：等權重 RRF 讓 MRR 降到 0.658，因為 BM25 對中文問題無效。
- **人的追問逼出實測：** 人問「router 為什麼用 `think=low`？」AI 原本的理由（任務簡單、在每個問題的關鍵路徑上、思考會吃掉輸出額度）都只是推理，沒有數據。於是拿 12 題、4 個等級實測，發現兩件事：
  - `think=false` 關不掉 gpt-oss 的思考，產生的 tokens 甚至比 `low` 多。
  - 各等級的準確率只差 1 題，而 `high` 的 token 用量起伏很大（最多 1,349 tokens）。

  教訓：AI 給的「為什麼」，也要能拿出數據。
- **人的直覺也要實測：** 人提議「產生回答用 `think=high` 比較好吧？」實測結果：在 Q2 規模（prompt 約 5.3K tokens）下，`high` 的思考用掉 3,500～4,400 tokens，一次回答全空，另一次被截斷。教訓：10K 的限制改變了取捨。思考過程和檢索到的內容搶的是同一份額度，所以「多想一點一定比較好」在這裡不成立。
- **人推翻 AI 的技術建議，AI 找出解法：** AI 原本建議前端不用 build 工具，理由是評審要多裝 Node。人認為 React + Vite 比較好維護。AI 重新評估後，提出「把 build 好的 `dist/` 一起 commit」，原本的顧慮就消失了，於是改成支持 React。教訓：AI 的反對理由如果有辦法繞過，就不該堅持原本的立場。
- **AI 自己發現寫死的假設：** 討論第二份測試文件時，AI 注意到自己在 AGENTS.md 記錄的「章節標題是 12pt 字體」只是 LightRAG 這份模板的特徵，改成依字體大小的相對關係判斷標題，偵測不到時用虛擬 Section。
- **用另一個模型當設計審查者：** 設計討論結束後，人把設計交給 GPT 審查。GPT 抓到 5 個缺口，主要模型（Claude）核對後全部同意：
  - PDF 支援範圍沒有定義。
  - 經過摘要之後，Citation 回不到原文。
  - 額度表漏了 Group Summary 和 judge 兩列，也沒寫放不下時怎麼辦。
  - 「回答寫到一半被截斷」這種失敗沒有處理。前面的實測其實已經出現過這種情況，卻沒有補進設計。
  - 用字串比對檢查數字不可靠：`64.8` 在 Table 2 出現 3 次，實測時寫錯變體的回答也被算成答對。

  教訓：同一個模型很難看到自己的盲點，換一個模型審查很有效。

## 2026-10-12：Walking skeleton 的失敗 Trace

- **AI 寫錯並被測試抓到：** 第一版 Gateway 在 `done_reason=length` 時立即 raise，導致失敗的 LLM 呼叫沒有 Trace。透過「上傳 Document／提問」補一個回歸斷言後，測試明確失敗；修正成先保存 token／thinking／done_reason，再發出 error 和 Trace，仍不產生 final。重試策略留給 #07。
- **AI 自行修正前端狀態處理：** 第一版把串流是否定稿的變數修改放在 React state updater 內。Updater 可能延後執行，因此改為在失敗時直接依該 Turn 的 `final` 狀態決定是否保留回答，讓 updater 保持純函式。
- **真實模型推翻了 AI 對格式的假設：** Q3 瀏覽器驗收中，gpt-oss 雖收到 `[C#]` 規則，仍產生 `【C3】`。第一版只辨識 ASCII 方括號，結果 Citation 不能點。補上應用層回歸測試（marker 被切在三個串流 frame），確認先失敗，再於 Citation mapping seam 正規化括號；保留編號、不做無效引用的驗證（#07）。同一次 Q3 也再次顯示原始表格文字會造成錯誤解讀；結構重建仍由 #03 處理。

## 2026-10-12：#01 獨立審查後的修正

- **另一個模型抓到 AI 寫錯的切句規則：** 原本英、中標點都用零寬 split，`64.8`、`60.0` 和 `e.g.` 在長段落裡被插入換行。透過上傳真正的合成 PDF 先重現失敗，再改成英文標點後必須有空白、中文句末標點可以零寬切。超長句的 token slicing 也會產生 U+FFFD，改成完整 Unicode 字元邊界，並補上長段落的約 10% overlap；中文 PDF 回歸先失敗後通過。
- **審查補足實際額度邊界的證據：** 原本只測人為 budget=1，新增 raw prompt 6,701 tokens、正式 10K budget 的 guard 測試，以及應用層 error/no-final/zero-call 的測試。6,700-token prompt 仍能通過，完整保留輸出預留。
- **AI 的 Citation 格式正規化仍不完整：** `[C1, C3]` 和 `【C3†L1-L4】` 仍無法點擊。用分散在多個 frame 的腳本重現，再正規化成 `[C1][C3]` 與 `[C3]`，prompt 也明定多引用寫法。無效編號的驗證仍留給 #07。
- **AI 對資源生命週期與 Trace 集合處理不完整：** 第一版只保留最後一筆 Trace，而且遇到 terminal frame 時 break 不會立即 close adapter。回歸測試重現兩個問題，改成累積全部 calls 並用 `aclosing`；連下一次呼叫被 guard 擋住的情況，也會保留前一次的 Trace。
- **AI 漏掉非預期例外的事件與共用常數：** 原版 RuntimeError 會直接中止 SSE；在審查版本上重現後，兩個操作改成發出通用 error、伺服器記錄例外、LLM 失敗仍有 Trace。問題長度、安全邊際和切塊規則改用 policy 常數，安全邊際由 Trace 欄位提供給前端。

## 2026-10-12：#06 的拒絕事件與前端串流終止

- **AI 寫錯，瀏覽器驗收抓到：** 新增 `rejected` 事件後，後端的「問題超過 1,000 tokens、LLM 呼叫為 0」測試已通過，但 AI 漏改前端 SSE reader 的 terminal 清單。瀏覽器收到拒絕原因後，又被 `Stream ended before completion` 蓋掉。修正 reader，把 `rejected` 視為正常終止；重新 build 並再次在瀏覽器送出超長問題，確認保留原因、提示縮短問題、不顯示重試同一問題的按鈕。教訓：事件模型與生成型別一致，還不能保證串流消費端正確處理新的終止事件。

## 2026-10-12：#06 獨立審查後的修正

- **審查抓到 Router 的過度驗證：** AI 把「Synthesis 應產生 2–5 個 Sub-query」當成硬驗證，連一個 Sub-query 的合法 JSON 都退回 Lookup，並丟掉追問的 Standalone Question。先用 0／1／8 個 Sub-query 與非 Synthesis 帶 Sub-query 的五組測試重現，再改成保留改寫、正規化計畫；只有解析／型別失敗或截斷才走 fallback。
- **AI 忽略已知 Citation 輸出形式：** 分批抽取只認 `[C#]`，沒有沿用早已實測的 `[C1, C3]`、`【C3†L1-L4】` 正規化。回歸測試先失敗，再用 CitationText 處理，保留可追溯事實、丟掉標題／無引用行並在每次呼叫的 Trace 計數。無事實的 sentinel 不再附上 Citation，也不被當成證據。
- **AI 的測試假設不符合真正輸出額度：** 原遞迴合併測試每批腳本超過 3,500 tokens，超出 `num_predict=1000`，所以不能證明真實遞迴路徑。修正 ScriptedLLM，連 thinking 也納入輸出上限；改用較大合成 Document、多批低於 1,000 tokens 的結果，總量仍超過 6K，確認再次合併能保留原始 Citation。
- **審查補上 Question Type 和歷史的隔離：** AI 原本把批次抽取套用到 Lookup，也讓 eval 的顯式歷史污染 session。修正成 Lookup 依排名選擇放得下的完整 Chunk；只在 Synthesis 原始上下文超過 6K 時抽取。顯式傳入歷史不修改 session。Global 的過渡路徑仍是 Synthesis，等 #05 接上 Summary Tree。
- **驗收腳本也有固定數量的假設：** Trace 的瀏覽器腳本先假定 top-k=30 一定只有兩批，但 Sub-query 的聯集多帶出一些 Chunk，實際是三批，腳本因此耗盡。測試依 request 類型逐批供應回應後，UI 順利完成，Trace 顯示三批丟棄行數 2、1、1。這是 fixture 修正，正式程式不需要更動。

## 2026-10-12：#02 損壞 PDF 被誤判成掃描檔

- **AI 的錯誤分類被合成 PDF 抓到：** 沒有文字的 PDF 截掉最後 100 bytes 後，PyMuPDF 仍能修復並開啟；#01 解析器卻回報「沒有文字層」，讓人誤以為需要 OCR。基底 cf49802 的上傳回歸為 1 failed、2 passed，明確重現錯誤原因。
- **第一版修正採取保守拒絕：** 先拒絕非 PDF 與 `Document.is_repaired`，三個案例都通過；正常掃描 PDF 仍回報不同的 no-text 原因。PyMuPDF 說明此欄位代表重大結構修復，並非完整有效性檢查。後續審查要求放行修復後仍可讀的文字，見下方 #02 獨立審查修正。

## 2026-10-12：#02 字型與重疊的回歸

- **實際文件抓到 AI 的標題誤判：** LightRAG 的 Table 4 粗體表頭 `Mix` 被當成 Appendix Section。先加上傳回歸，確認表頭必須留在內容，再依同一基線上的文字座標抑制表格儲存格標題；表格重建仍由 #03 處理。
- **AI 的 overlap 從單字中間開始：** #01 長段落會把 `encyclopediawordnumber103` 切成 `opediawordnumber103`。完整單字的上傳測試先失敗，再把 overlap 起點移到附近句子或完整英文單字；沒有句子的中文仍保留完整 Unicode 字元。
- **修正時又被測試抓到 API 用錯：** AI 把 start/end 傳給模組層級的 `re.finditer`，造成處理錯誤。改用已編譯 pattern 的 `finditer`，五個段落／overlap 回歸通過。
- **測試資料也要確認沒有被裁切：** 固定大小 fixture 的單行文字超過頁面邊界，沒有產生足夠 tokens。改成文字框後，35／60-token 測試能驗證完整段落裝箱與精確頁碼。

## 2026-10-12：Eval harness 的證據驗證

- **AI 修正自己的報告測試：** 第一版以整份 markdown 中的 `judge` 欄位出現次數驗證呼叫數，誤把 fact 的檢查方式欄位也算進去。真實 bge-m3／scripted LLM 的三次操作測試抓到失敗後，改成只比對 LLM 呼叫列，並同時斷言 recording Gateway 的六筆呼叫與 2/3 通過率。教訓：報告文字的斷言要對準使用者要核對的紀錄。

- **真實模型抓到 AI 的 Judge prompt 寫錯：** Lookup-only 第一輪評估裡，中文回答與三個正確固定拒答都被判失敗。檢查報告後發現 prompt 把所有條件都當成「回答必須自行宣稱的事實」，所以不會把中文文字視為「回答用中文」，也不會把拒答本身视為符合格式。先加會失敗的 adaptive fake judge 回歸，修正成區分 factual claim 與 answer property，再重跑真實基準；保留初次報告 `lookup-skeleton-initial.md` 作為錯誤證據。逐字摘錄仍嚴格驗證，包含 Citation 與空白，沒有放寬為近似比對。
- **第二輪量測補上缺少的 Judge 輸入：** answer property 的分類已讓中文答案正確通過，但固定拒答仍被判失敗。Judge 只收到「固定句」的描述，沒有收到 D01 要求的確切句子。先加缺少 expected sentence 就失敗的回歸，再把 `exact_answer` 一起傳給 Judge，並明定拒答本身是格式條件；程式仍先拒絕任何額外內容。中間報告保留為 `lookup-skeleton-property-intermediate.md`，後續基準以完整修正後的報告為準。
- **Judge 也會把拒答當成錯誤結論：** 完整修正的基準中，Judge 對 `Not mentioned in the document.` 摘錄出相同文字，卻宣稱它斷言了 privacy／license／HotpotQA 的錯誤限制。這不是摘錄捏造，而是語意誤判。先以會故意回傳這個錯誤結論的 ScriptedLLM 重現，再在 checker 確認完整回答恰好為 D01 固定拒答時，直接判定沒有 asserted forbidden claim；帶有額外文字仍需 Judge。保留 `lookup-skeleton-refusal-intermediate.md`，不把錯誤 Judge 結論當作系統真的編造限制。

## 2026-10-12：#08 獨立審查後的修正

- **Reviewer 抓到 AI 的評估假陰性：** 基準裡 Q1 experiments 的正確內容因 markdown 的兩個尾隨空格／換行而無法通過 raw substring 驗證。先加會失敗的 hard-break、U+202F 與 U+2011 回歸，再同時正規化回答及摘錄的 typography／空白；保留文字、大小寫、標點、Citation，虛構的字仍拒絕。
- **AI 把 Golden Facts 寫得比需求嚴格：** Table 1 原本把四個資料集塞在同一條數字 fact，要求單一摘錄出現全部 anchors；Table 3 額外要求 MAPK／AUC／engagement，Q1 experiments 也混入負向判準。依審查拆成每個資料集一條 fact，Mix 比較獨立檢查，移除 Table 3 額外要求，Q1 的 universal-best 改成獨立 forbidden。額外加強變體與數值的 clause／row／table column 對應，避免同一摘錄裡 -High 的數字被算成 -Low，以及 LightRAG-High 被算成完整版。
- **Reviewer 修正 AI 把 Judge 當成唯一判準的設計：** 固定拒答改成 deterministic 比對，允許一個句末句號，不再浪費 Judge 呼叫或因 Judge 截斷誤判；拒答文字集中到 policy。報告區分 ask／Judge 時間、把 budget 超額標為 harness/upstream bug、把 live Judge probes 從 Golden Facts 結果分離；Q3 增加可追溯到 p.8／Table 2 Chunk 的 Citation 檢查。先前報告全部標示 superseded，重新量測基準。

- **第二次審查抓到 numeric anchor 修正引入的假陰性：** 單字邊界讓正確的 `LightRAG‑Low`／`LightRAG‑Origin` 無法匹配 `-Low`／`-Origin`。先用完整變體名的兩個數字 fact 重現失敗，再接受獨立、連字號和空白前綴寫法，同時保留完整版不能匹配變體的反向測試。`60%` 與 `60.0%` 的回歸也先失敗再通過。Citation 檢查在 Table Chunk kind／label 可用時優先要求它；沒有該 metadata 時保留明示的 p.8／Table 2 fallback。

- **整合測試抓到舊 fixture 的呼叫次序假設：** #08 rebase 到含 #06 的 main 後，四個應用測試仍只供應 answer／Judge 腳本；真實 Router 先取走腳本，導致耗盡、錯誤的 Citation 和時間斷言。先跑完整測試重現，再為每次 ask 加入 Router JSON，將 Trace／呼叫數與時間驗證納入 Router。新增 canonical 12-case 對應及两個追問的應用層測試，確認 role/content 轉成 ConversationTurn 後實際進入 Router request，獨立題目傳空歷史且不污染 session。

- **第三次審查抓到評估把 fallback 當成 Router 成功：** 整合報告的 Lookup「通過」沒有驗證計畫來源，追問未改寫也因 ask 接受 history 就通過。先用 scripted PlanEvent 重現 fallback Lookup 的假陽性，再要求 plan_source=router，fallback 以 FALLBACK 記錄且分類失敗。與 #06 agent 約定 plan_source／fallback_reason 介面，兩個追問以 canonical case metadata 檢查 Standalone Question 改變及明確的 referent／檢索成本或比較；不再用參數被接受作為品質判準。舊報告標示 superseded。

- **人補上語言改寫的驗收限制：** #06 新增 rewrite_language_mismatch 後，#08 原先只看 plan_source／referent，會讓帶有語言不符旗標的 scripted PlanEvent 通過改寫測試。先重現，再把旗標納入改寫失敗條件，報告保留原始 router_standalone_question，方便追查；Question Type 與改寫品質分開檢查。

- **AI 的 rebase 修復腳本被 TOML conflict 擋住：** 用 uv run 啟動 Python 時，uv 先解析尚未解決的 pyproject.toml 而拒絕執行；AI 未確認該步 exit status 就繼續，讓 marker 留在中間 checkpoint。改用 uv run --no-project 執行修復，明確驗證 TOML 可解析且沒有 conflict markers 後才繼續。最终保留兩邊的 eval exclusion／marker 與兩份 AI log，並以完整測試驗證整合。

- **整合後的測試 fixture 仍假定 Router user message 只有問句：** #06 新增語言提示 wrapper，歷史內容與問句皆正確傳入，但舊斷言比較整個 content 而失敗。改為驗證最後一則仍為 user 且保留原問句，歷史 role/content 仍逐字核對；改写品質另外由新的 provenance／referent／語言旗標斷言負責。

## 2026-10-13：#06 真實 Router QA 推翻腳本驗收

- **測試替身掩蓋 AI 的格式假設：** ScriptedLLM 一直給合法 JSON，確定性測試全過；獨立 QA 卻發現 Ollama Cloud 不執行 `format` schema，Router prompt 又沒列出完整鍵名，12 題僅 1 題有合法計畫。修正 prompt，明列三個鍵、型別和範例；解析容忍實測的 `type` 別名與額外欄位。保留 9 份逐字真實回應作為 fixture，再加入預設排除的 live smoke。最終實測 12/12 正確、零 fallback，輸出 52–179 tokens，沒有把 600-token 額度調大。
- **原本把 fallback 當正常 Lookup，Trace 看不出失敗：** 新增 `plan_source` 和 `fallback_reason`，計畫事件與 Router 呼叫 Trace 都保留來源。帶歷史卻缺少改寫時，明確記錄 `missing_rewrite`，不再宣稱代名詞已解開。#08 同步改為把 fallback 與真正的分類結果分開計分。
- **schema 合法不代表追問改寫成功：** 第一輪修正的 live smoke 雖然類型 12/12，仍有「它」未解開；加上具名主詞規則後，又發現中文短問句被英文歷史帶成英文。把語言提示放進目前問題，live smoke 也斷言語言與具名主詞。最終瀏覽器追問顯示完整中文的 LightRAG／GraphRAG 成本問題。
- **有效 Sub-query 也可能找錯證據：** 瀏覽器 Q2 最初得到 Synthesis，但泛稱 cost 的子查詢只找到 Table 3 caption，沒有 `610 × 1,000` 成本段落。針對檢索系統比較，明列 token／API-call 成本與 incremental updates 的查詢要求；重新跑真實 bge-m3 與雲端 Router，兩種原文證據都進入檢索結果。
- **修正 AI 對 Trace 證據的誤讀：** 舊 Q3 Router 以 low 用完 600 tokens，QA 有保存完整 thinking：`Need to answer synthesis: compare ablated versions. Provide subqueries.`，用 `o200k_harmony` 計數為 14 tokens，因此約 586 tokens 是內容，很可能是過長或失控的 JSON／Sub-queries。AI 曾誤稱 thinking 不完整；審查指出後已更正。未保存部分 JSON，所以無法還原其確切形式。先前修正的瀏覽器 Q3 用 63 tokens 結束；那輪結果的 prompt 另有測試調校偏誤，見下節。

## 2026-10-13：#06 審查抓到評估洩漏

- **AI 把驗收題寫進 prompt：** 前次修正把 Q2 本身與成本／增量更新 Sub-query 當範例，又列出 ablation、dataset 等回歸題線索，12/12 不能證明泛化。審查要求後改成單一表格／圖、比較機制／成本／維護的通用規則，以及其他領域的範例；不再含 LightRAG、RAG 或 Golden Facts 的特定查詢詞。
- **neutral 範例也要檢查是否與 held-out 重疊：** 第一個 neutral 版本用太陽能／風能範例，和八題新測試中的追問主題重疊。改用鐵路／海運貨運範例，保持八題與標籤不變，再重跑並保留分開報告。held-out 題涵蓋中英文、三種 Question Type、天氣感測器和能源的追問；沒有依其答錯結果調整題目或標籤。
- **原本的追問檢查太弱：** 「那 LightRAG 呢？」本來就含 LightRAG，單比名字不會抓到遺失的檢索成本主題。新增成本／API 等歷史主題檢查，也以 dev-only OpenCC s2t 標記簡體轉換；「检索成本」現在會使 smoke 失敗，共用字無法判定字體的限制明載於報告。
- **保留失敗，避免繼續對 Golden Facts 調 prompt：** 第一個 neutral 瀏覽器 Q2 的分類與 incremental-update 證據正確，但沒有檢索到含 `610` 的成本段落；這個失敗已通知協調者，沒有把 token／API-call 等特定驗收詞放回 prompt。最終貨運範例的瀏覽器結果另列於 follow-up 報告。
- **小型 smoke 過關，不代表完整聊天流程過關：** 最終通用貨運範例在 canonical 12/12、held-out 8/8 通過，且歷史主題／繁體檢查都過。但瀏覽器 Q2 沒取回成本與增量更新段落；先聊完兩輪再問英文 Q3 時，模型改判 Synthesis 並改寫成中文。這些案例保留為 FAIL，沒有用 smoke 分數代替實際驗收；後續需改善通用計畫／歷史處理與檢索品質。

## 2026-10-13：#06 回答語言不能由改寫問題決定

- **真人把檢索品質與 #06 bug 分開：** Levi #2066 接受歧義時選 Synthesis，並將 Q2 的成本／增量更新檢索 FAIL 留給 #11，在真實 Section 與 neighbor/table links 整合後調整；不把 Golden Facts 詞彙寫回 Router prompt。
- **AI 的語言契約漏了應用層：** 回答原本只收到 Standalone Question，模型把英文 Q3 改成中文後，回答也跟著中文。補四個先失敗的回歸案例，讓回答收到目前問題作為語言依據，並把同一份提示納入 Context Packer 額度估算。中英 script 不一致時保留 type／queries、使用目前問題並在 Trace 保留警示與原始改寫，不再呼叫一次 Router；依賴歷史的追問可能因此留下未解參照，警示明確暴露此限制。
- **真實聊天再驗證：** Q2 → 中文成本追問 → 英文 Q3，Standalone Question 與回答均為英文，Router 95 tokens 正常結束。這次模型本身沒有輸出跨語言改寫，強制錯誤分支由確定性測試證明。保留原先失敗 tapes，另存新證據；68 項測試通過，前端重新 build。這次只驗收語言，沒有宣稱表格數字或 Golden Facts 已通過。

## 2026-10-13：#06 的中文回答還要保留繁簡體

- **獨立 QA 抓到 AI 的提示仍不完整：** 中文成本追問的 Standalone Question 保持繁體，回答卻出現「检索阶段」「个 token」。原本只指定回答語言，不足以約束中文字體。Levi #2269 要求最小修正：沿用 Router 的中文偵測與規則，在目前問題旁明定保留繁簡體，共用字無法判定時採繁體；數字不變，同一份提示仍由 Context Packer 計入額度。
- **先重現提示缺漏，再補測試：** 繁體、簡體與共用字追問三個提示測試先失敗後通過；英文問題不會被中文改寫帶入中文字體規則。Dev-only OpenCC 檢查能標記 QA 的簡體回答；只檢查保存的文字，不轉換正式回答，也不新增模型呼叫。
- **檢查器的誤報也由實測修正：** 重跑一次瀏覽器追問後，回答已使用「檢索階段」「個 token」「實體與關係」，但 OpenCC s2t 把合法繁體的「群」轉成「羣」。新增先失敗的異體字案例，比較時以 t2tw 正規化繁體異體字，避免把正確繁體計為簡體錯誤；原始回答保持不變。校正後，舊 QA 的簡體回答仍被標記，新回答通過。

## 2026-10-13：#07 的失敗狀態與 Citation Validator

- **AI 寫錯的句子歸屬被回歸測試抓到：** 第一版 Validator 把「結論。 [C99] 下一句」的無效 Citation 歸給下一句，違反 D01 只標記引用無效編號的句子。透過 Application.ask 先重現，再把句末後的 Citation 連回前一句；數值 64.8／60.0 不切開，中英文句末與重複無效編號也補了檢查。
- **延後項目有具體失敗證據：** 字元逐個串流的 `[C1 C3]`、`[C1–C3]` 與 alternate bracket range 測試先失敗；補正規化後通過。範圍只有在每個編號都存在於 Citation map 時才展開，巨大、反向或跨 C/S 範圍保留成無效 Citation 交給 Validator，避免把不可信範圍偷換成有效來源。

## 2026-10-13：#07 審查後的 Unverified 與失敗細節

- **獨立 reviewer 抓到 AI 把 UI 標記混入回答文字：** 第一版在句尾加「未驗證」，前端再按字串找標記，導致「論文中的假設仍未驗證[C1]。」也被標成 Unverified，history 也混入 UI 文字。先用 Application.ask 重現，再改成 FinalEvent 的 UnverifiedSpan（Unicode code-point start/end），前端用 Array.from(text) 對齊位置；自然語句和 history 保持原文，只有無效 Citation 句子有 badge。
- **相同正規化程式也要帶對資料：** 分批抽取事實的 CitationText 沒有 map，合法 `[C1–C3]` 因此被丟掉。新增真實 bge-m3、oversized Synthesis 的回歸測試先重現，再傳該 batch 的 allowed Citations；句子切分也補 vs.、e.g.、i.e.、et al.，移除無效編號後收斂多餘空格。
- **錯誤與重試狀態仍有小缺漏：** 審查指出 Router／query embedding 共用 answer_failed，重試第一個 delta 蓋掉「重新產生中」，較早的失敗 Turn 可在後續成功 Turn 前被原地替換。改為 stage-specific connection error、維持 retrying 狀態，且只讓最後一個 Turn 提供 Retry。半有效範圍整段拒絕的 fail-closed 規則經 reviewer 確認接受，保留 README 原有「全部編號都存在才展開」規則。
- **整合測試也要反映一次 low 重試：** rebase 到含 #08 的 main 後，eval runner 的失敗 fixture 只供應第一次截斷，低思考重試因此耗盡腳本。補第二次截斷並驗證 Router／answer／answer 三次呼叫、最後一次 low、無 Judge；AI 初次漏刪相鄰的舊兩次呼叫斷言，targeted test 抓到後修正。最終完整測試 138 passed、2 deselected，eval 正式程式沒有更動。

## 2026-10-13：#02 與 #06 整合

- **保留兩張票的介面與紀錄：** 依指示從 cf49802 rebase 到 main b005721，保留 Application 的兩個 keyword-only 設定、Router／history 與兩張票的 AI log。HTTP factory 當時同時讀取 `CHUNK_TOKEN_TARGET` 與 RetrievalSettings。
- **真實 Section 改變批次數量，揭露 fixture 假設：** 分批抽取從兩批變成三批，#06 的腳本佇列耗盡；固定 C20 也依賴舊 Chunk 排序。改成每批從實際 evidence 選 Citation ID，仍驗證多批、來源追溯、有效引用、過濾與 Context Budget。
- **Q2 的固定排名假設太脆弱：** 真實 Section 可能讓成本段落進入前三名，因此不再要求 baseline 一定沒有 `610`。保留 Synthesis 擴充且包含 baseline、成本／增量更新／community、去重、原文順序與 prompt 來源檢查；獨立審查另要求每個 Sub-query 自己的 top-2 證據，見下節。
- **追問測試補上正式 Router 路徑：** heading-free fixture 加入 #06 所需的 Router 腳本回應；PDF 解析、切塊與本機 bge-m3 都維持真實執行。

## 2026-10-13：#02 獨立審查補足解析邊界

- **另一個模型抓到單份文件驗收的盲點：** 原版遺失換行標題、References 後沒有 Appendix 字樣的附錄，以及雙欄的閱讀順序；本文大小的 small-caps 小節也沒有成為 Section。11 個合成 PDF 上傳案例先重現 10 failed、1 passed，再修正相鄰同樣式標題合併、字母／補充附錄、依欄與座標排序，以及帶編號的小節樣式判斷；沒有寫死字體大小。
- **表格與圖內文字不能一起刪：** PyMuPDF 的 drawing rectangle 也可能代表表格。只依 Figure caption 找圖形候選區域，再移除其中短標籤；合成圖表同頁案例保留真實短句、Table caption、表頭和數值，LightRAG 的 `Beekeeper`、`Query + LLM` 與控制字元碎片不再進入段落。
- **修復不代表不可讀：** 審查推翻第一版一律拒絕 `is_repaired` 的策略。修復後有文字的 PDF 會記錄 warning 並正常上傳；修復後仍沒有可讀文字，回報損壞 PDF 原因，正常掃描檔仍回報沒有文字層。
- **測試與設定改用明確來源：** 分批抽取替身依 Gateway 提供的 `call_type` 判斷，不再用輸出額度猜用途；`CHUNK_TOKEN_TARGET` 由 RetrievalSettings 驗證，虛擬 Section 與 Chunk 共用同一目標。Q2 加上每個 Sub-query 自己的 top-2 成本／增量更新證據檢查。

## 2026-10-13：#02 第二次審查抓到圖形區域過度過濾

- **AI 把「靠近 Figure caption」誤當成足夠證據：** 第一版圖內文字過濾會把陰影框裡的換行段落當成圖形標籤，也會讓頁框裡的標題消失。陰影框與頁框的上傳測試分別先失敗；改成先取得全文的內文字體與標題樣式，再排除包含段落句子流或標題的候選區域。逐行過濾也明確保留標題與章節編號，LightRAG Figure 1 的短標籤仍被過濾，表格數字仍保留。
- **句點不一定代表內文：** `7.2 CASE EXAMPLE … IN LIGHTRAG.` 與 `7.4 CASE STUDY: … NAIVERAG.` 被句尾規則擋掉，內容掛到前一節。合成 PDF 的同列與拆開編號案例先失敗，再允許帶編號且全大寫／small-caps 的標題以句點結尾，並以真實 LightRAG 檢查這兩節。
- **空 Section 的用途要寫成契約：** 主節標題若緊接小節，會保留零段落／零 Chunk 的 metadata；Summary Tree 輸入排除這些 Section，#05 builder 必須跳過，只摘要有來源 Chunk 的 Section。契約記在 Section docstring 與驗證報告，不在 #02 新增摘要行為。

## 2026-10-13：#02 保護標題的修正反而讓圖內標籤變成 Section

- **審查抓到 AI 修正引入的回歸：** 為了保護陰影框與頁框，AI 讓任何像標題的文字都保護整個圖形區域。結果粗體 `LLM`、本文大小的 `LLM AGENT` 留在內容，較大字的 `Dual-level Retrieval` 更把 caption 與後面的 Introduction 段落搶成新 Section。合成 PDF 上傳先失敗，再將保護限於頁框大小的區域、真正帶編號的 Section 與段落句子流；確定是圖內的短標籤則先過濾，不因粗體或大字保留。
- **全大寫加句點仍不足以辨識標題：** `2 GPU HOURS.` 和 `3. THE SOFTWARE IS PROVIDED AS IS.` 會搶走後續段落；同列與拆開編號兩個回歸先失敗。現在句點例外還要有粗體、small-caps、字體變化或較大字級。LightRAG §7.2／§7.4 的 mixed-size small-caps 保留；標題的句末句點去除。正向合成案例分別使用粗體與不同字體，與真正內文樣式的反向案例分開。
- **減少重複的判斷規則：** 句末標點共用一個 regex，短標籤字數與寬行比例改成具名常數，逐行圖形標籤判斷集中到 helper。陰影框、帶／不帶編號的頁框與 LightRAG Figure 1 回歸持續保留。

## 2026-10-13：#02 最終 rebase 保留 #07 失敗行為

- **整合方向由人確認：** 第四次獨立審查批准 #02，要求 rebase 到含 #07 的 `79c82a8`；編號步驟圖內標籤與頁框內無編號標題的邊界案例移交 #10，不在 #02 擴充。
- **衝突要保留兩邊的契約：** Citation 旁註包住 #07 的 structured UnverifiedSpan renderer，保留 Unicode code-point 位移、暫定樣式、C/S inline 引用；Gateway 同時保留 low retry 的 effective think 與腳本辨識用的 call_type。抽取失敗測試用真正 Section 的可變批次數，並維持 trace → error 的終止次序。AI log 去除 rebase 產生的重複區塊，保留 #06／#07／#08／#02 內容並依日期排列；前端 dist 由合併後 source 重建。

## 2026-10-13：#04 背景上傳的關閉時序

- **AI 漏掉尚未開始執行的 Task：** 第一版只在 ingestion worker 捕捉 CancelledError；若剛拿到 job id 就關閉 Application，Task 還沒執行到 try 區塊，close() 會直接拋出取消例外，progress 也沒有終止事件。先以 Application.start_upload → close → upload_events 的公開操作測試重現失敗，再讓 close() 等待取消並補送唯一的 ingestion_cancelled error；已進入 embedding 的取消案例也維持通過，不留下半成品快取。

## 2026-10-13：#04 審查與 #02 整合

- **Reviewer 抓到 AI 的快取身分漏了調參設定：** 原本只記內容 hash、ingest-v1 與 embedding_model；#02 的 Section 新欄位有預設值，舊資料仍可能驗證通過，調 Chunk 大小也會吃到舊結果。先以 effective chunk_token_target 改變及 legacy pipeline 的兩個 Application 測試重現，再把有效設定加入 key，並用 parser／chunker／models／cache format／token／policy 原始碼的 digest 產生 ingest-v2 身分。新 Section metadata 的快取往返與失敗替換保留狀態也重新驗證。
- **Reviewer 修正 AI 把快取失敗當成文件失敗：** 第一版已完成 parsing、Chunking、embedding，卻因快取寫入失敗丟掉可用 Document；測試也鎖住了這個行為。依審查先改成會失敗的 ready 驗收，再把 cache write 改為記 warning 並繼續發布；atomic replace 的 temp cleanup 及既有快取保留仍受測試保護。
- **進度與錯誤也補上可觀察的界線：** 真實 bge-m3 的進度測試先重現只停在 0/N，再改成每批 8 個 Chunk 並逐批發 n/N；invalid／zero-vector 的 ValueError 測試先重現 generic ingestion_failed，修成 embedding_failed。404 reconnect 解除上傳 pending，409 顯示後端 detail；快取目錄固定到 repo root。
- **Rebase 保留兩邊的意圖：** #02 與 #04 都新增 test_ingestion.py；將 #04 工作測試移到 test_ingestion_jobs.py，完整保留 #02 測試、設定驗證和 parser/chunker 呼叫，同時保留 #04 背景處理與 swap-on-success。由源碼重新產生 event types 與 dist，沒有手合併 build 產物。

- **瀏覽器 QA 編排也曾漏等背景命令：** 一次 exec_command 回傳 session_id 後，AI 提前執行下一個快取比較，導致 before 檔案尚未建立及額外的 409。改為等外部 ingestion 的 ready、命令完成與 UI ready 後才比較；正式證據使用完整 before/after call counts，並另外以新 server 的零呼叫 cache hit 確認，不把等待腳本的錯誤當成產品失敗。
## 2026-10-13：#02 QA 抓到中文句尾與數字斷行

- **通過既有測試仍漏了等號邊界：** 獨立 QA 以換行中文 PDF 重現，句尾剛好落在 token 上限時，AI 把 `end == hard_end` 當成沒有句界，退回 PDF 行尾空白而切斷句子。相同 160 句玄武岩資料的 upload 測試先失敗，再用明確的「找到句界／未找到」分支，保留剛好等於上限的句尾。
- **約 10% overlap 不能犧牲完整短句：** 舊邏輯要求 sentence overlap 至少占一半額度，會跳過窗口內只有 3 tokens 的「完成1！」，讓下一塊從前一句中間開始。獨立短句 upload 回歸先失敗，再讓 。！？ 後的句首優先，即使重疊較短；窗口內沒有句首時，中文維持完整字元備援，英文維持完整單字。
- **PDF 排版換行不該拆開中文數字：** `區域1\n4` 與 `4\n9` 的 source／Chunk 測試先失敗。只在包含 CJK 的同一段落內，將 CJK／數字字元之間的排版 newline 移除；`Sample 14\nstayed stable.` 與 `Sample\n14` 保留英文分隔，不修改純英文表格數字。#04 已確認 source-derived processing identity 會使這次 parser／chunker 修改自動失效舊快取。

## 2026-10-13：#02 中文斷行修正把數值欄合併

- **Reviewer 抓到 AI 修正的資料毀損：** 含中文表頭的同一 block 只要碰到 digit-to-digit newline 就移除，讓 `1.2`、`3.4`、`2023`、`2024` 變成一串數字。stacked-value upload 測試先重現完整錯誤，再保留每行所屬 block 的 bbox，只有前一行占 block 寬度至少 90% 且下一行往下延續時才當作排版換行；純數值行即使滿寬也保留分隔。正向數字斷行 fixture 改成真正靠近 block 右緣的長行，保留英文分隔檢查。
- **數字分組空格也屬於數值行：** 新增 `1 234`／`2 345` 的 upload 案例後，仍重現兩行被接起來；AI 的數值行判斷漏了空格。補上空白字元後，帶分組空格的滿寬數值行也保留原始換行。
- **跨頁不是段落邊界：** 中英文兩頁 upload 測試先在未完成句子的案例失敗；改成上一頁最後一行沒有句尾標點、下一頁第一段樣式與左緣一致且仍在同一 Section 時接續同一段落，保留 `(1, 2)` 的 paragraph／Chunk 頁碼。已結束的句子維持兩個段落；原有 whole-paragraph packing fixture 加上本來就意圖結束段落的句點，不放寬測試斷言。

## 2026-10-13: #02 re-review found caption/header joins and labelled numeric rows

- The independent reviewer found that matching typography and left alignment joined LightRAG Table 1/3 captions to the preceding page's body, extending its provenance incorrectly. Four public-upload regressions failed first (real LightRAG plus generated Table, Figure and CJK running-header cases). Continuation now excludes captions and requires sentence or text-flow evidence; an unsupported page-leading label stays separate from both adjacent body paragraphs. Source text is retained. Existing English/CJK and real LightRAG continuations remain covered.
- Equal-width CJK label/value rows still satisfied the old block-width guard. Two public-upload cases failed first; requiring a shorter final block line preserves those rows while keeping actual wraps. An additional shorter-final-value regression then failed, demonstrating that raggedness alone is insufficient. Consecutive CJK labels with whitespace-delimited numeric cells supply evidence against prose wrapping, preserving their separators without a blanket rule against numeric content.
- An initial new test incorrectly forbade two small independent paragraphs from sharing a Chunk. The assertion was corrected to require their double-newline separator, consistent with the existing paragraph-packing requirement; exact paragraph content and page provenance checks remain. No existing assertion or fixture was weakened. Final ingestion verification: 49 passed, including all 160 facts and the short-sentence overlap checks.
- Replaying the original QA PDF exposed another boundary: its completed paragraph has a nearly full-width final line, so requiring raggedness alone preserved 50 layout newlines. The replay still retained 160 facts and sentence-ending Chunks, but used 12 Chunks instead of 11. A new public-upload regression for genuine prose with a full final line failed first. Page/column-width evidence plus a completed final sentence now also establishes text flow; labelled numeric-row guards remain. The replay returns to 11 Chunks (maximum 498 tokens), and a stronger assertion checks all 160 source measurement phrases without removing newlines first. The initially added exact-whole-sentence source assertion was corrected because punctuation-adjacent layout newlines remain intentionally retained; the measurement check specifically protects CJK text and numbers, while the existing complete-sentence Chunk coverage assertion remains.

## 2026-10-13: #02 independent review found the symmetric-margin assumption

- Reviewer nova-r02-mige confirmed R1/R2 closed but found M3: the AI's calculated page/column width assumed symmetric margins. Nearly full final CJK lines in an asymmetric text area or the right column failed the normalization gate. Public-upload regressions first failed for both layouts; the left-column control passed.
- Width now comes from measured, aligned text of matching typography on the page, bounded by the block's right extent to avoid borrowing a spanning band's width. Page-leading continuation uses a separate reference that also considers the measured preceding body flow, so a short running header cannot count its own width as proof of continuation. Caption and numeric-row guards and all previous assertions remain.
- Exact-source regressions cover 172 characters in an asymmetric single column and 96/120 characters in both columns, along with paragraph page provenance and Chunk text. Ingestion tests: 53 passed. Original QA/cache replay still gives 11 sentence-ending Chunks, maximum 498 tokens and all 160 facts and source measurement phrases, with embedding calls 2/0 and no LLM call. Full final checks and independent M3 re-review are recorded in the separate verification report.

## 2026-10-13 — #03 Table 2 Golden Facts fixture corrected

AI initially transcribed three -Origin rows incorrectly in the deterministic fixture. The coordinate-extracted source cells disagreed; the fixture was corrected against the fixed PDF before treating its test as evidence. Numeric acceptance must compare every labelled cell, not infer values from the overall result.

## 2026-10-13 — #03 Q2 retrieval assertion aligned with the requirement

After table text was removed from prose, the §4.5 cost and GraphRAG update paragraphs packed into a valid 494-token Chunk. The incremental Sub-query top two then ranked the §3.1 incremental-update paragraph and Abstract. The previous assertion required all cost/update/community terms in one particular Sub-query's top two. Levi clarified (#4395) that AGENTS requires coverage from the Sub-queries collectively. The regression now proves that their top-two union covers 610 costs, incremental updates, and GraphRAG community regeneration, that the Standalone Question top three lacks the 610 paragraph, and that the final Synthesis prompt includes all three. Chunk size and retrieval counts remain unchanged.

## 2026-10-13 — #03 Table reconstruction did not by itself solve Q3

The first clean N=3 live run at fef26f5 preserved typed Table 2 Citations and comparison-baseline explanations in 3/3 answers, but both numeric exceptions scored 0/3 and one answer asserted every ablation was worse. The model omitted full-model rows and sometimes used a Comprehensiveness value as Overall despite correctly labelled source rows. A richer table and baseline wording alone were insufficient; the report is retained honestly at `eval/reports/table-reconstruction-q3-n3.md`. Some ablation-meaning Judge failures were also non-verbatim multi-excerpt evidence, so those failures are distinguished from the missing numeric claims.

## 2026-10-13 — #03 generic table-reading correction authorized

Levi #4532 authorized one follow-up measurement and a held-out non-Golden-Fact table question. The correction adds generic instructions to identify/include the supplied reference/full-system row, compare the same metric and dataset/column, and mention cells contradicting the trend. Source table text repeats the dataset/metric on each numeric pair and identifies a source-derived unmodified named row when other rows use shortened '-' variant labels. Added rules contain no model names or Golden Fact numbers and are not restricted to an ablation question. The previous failed report remains intact.

The authorized follow-up at clean d6a075e did not improve the Q3 Golden Fact rates: Table 2 citation/baseline/type/terms remain 3/3; both numeric exceptions remain 0/3; forbidden passes 2/3. One answer still claimed the full system wins every metric/dataset. The held-out Table 1 Legal HyDE/LightRAG question was answered correctly (Diversity 20.0% / 80.0%, Empowerment 26.0% / 74.0%) with a real Table 1 Citation. Neither run truncated or exceeded budget. Per Levi #4532, no further tuning was attempted; Q3 answer-quality failures are handed to #11. The follow-up and held-out answers/traces are committed separately, preserving the baseline.

## 2026-10-13 — #03 independent review exposed table-region assumptions

The independent Claude review (#4830) found that caption-left bounds dropped Table 4's row labels, equal cell counts falsely reconstructed prose columns, and caption-below layouts swallowed body text. Authored-PDF upload regressions reproduced those failures before the fixes. Table candidates now use the caption's page/text column, stop at prose boundaries, and scan above a below-table caption; rectangular reconstruction requires coordinate alignment, numeric cells and nonnumeric row labels. Existing Table 3 case-study prose cells and the Figure 2 cost grid remain source evidence, while plain prose after captions stays in Sections.

The same review caught a system-prompt-only limitation assertion, mismatched candidate/variant headers, caption-specific underscore cleanup and an oversized raw-line split gap. The regression now checks the actual uncertain Table Chunk in the answer's user message; a frontend static-render check verifies its limitation note and raw text. Math-italic artifact cleanup preserves identifier underscores, oversized raw lines split with the limitation repeated, and virtual Sections rebuild from their own Chunk fields instead of looking up duplicate labels. Early column inference also mistook isolated table cells for an opposite prose column; the targeted upload tests exposed that and the detection now requires opposite prose or a caption. No Q3 quality prompt tuning or additional cloud evaluation was performed.

Rebased #03 onto main d56e092 including #04. Resolutions preserve embedding batches plus the table token limit, both AI logs, background upload lifecycle/ask guards plus request-local retrieval drop counts, and both README scopes. Frontend dist was rebuilt from the combined source. The cache-source regression failed until tables.py and embedder.py joined PIPELINE_SOURCES, then verifies source changes cause upload reprocessing and table metadata round-trips. An additional two-column upload case showed the physical page midpoint can clip an edge cell; the region now follows the opposite text gutter. The earlier rebased suite passed 207 tests; the final suite and final-backend Table 2 source UI acceptance are recorded in docs/verification/ticket-03/review-corrections/.

### 2026-10-13 — #03 independent re-review catches table boundary regressions

Independent reviewer nova-r03-hazu found that a close 10pt numbered heading below
9pt table rows disappeared into raw Table evidence, while a wrapped prose line
starting `Table 1.` stole its entire paragraph as the caption. Authored PDFs
through public upload reproduced both findings; a stolen paragraph above 2K
combined with a damaged numeric row ended upload in Error instead of Ready.
The parser now supplies its own heading indices to table reconstruction. A
formed grid stops at unrelated nonnumeric list/equation lines, but malformed
numeric rows remain uncertain source evidence. Captions require block-leading
or distinct typography and consume only lines from the actual caption onward.
New RED→GREEN logs and the 421-token LightRAG preservation comparison are in
`docs/verification/ticket-03/review-round2/`. Independent re-review and #02
integration verification remain required; no cloud quality/prompt tuning ran.

### 2026-10-13 — #03 grid-stop correction retains internal group dividers

Independent round-2 review of e9deece found that the new grid-stop rule treated an
internal nonnumeric group divider as the table's end, leaving later numeric rows
in prose while claiming reconstruction succeeded. Authored caption-above and
caption-below public-upload tests both failed on an isolated exact e9deece source
snapshot. Coordinate collection now looks ahead within the same font, gap and
heading boundaries: if aligned numeric rows resume, the divider stays inside the
region and the whole table retains raw uncertain evidence. The list/equation
boundary and caption/Section fixes stay covered. This corrects an AI-written rule
that was too broad; re-review is still separate and required.

### 2026-10-13 — #03 rebase preserves #02 measured flow alongside tables

Main confirmed integrated #02 e59e096 and authorized the #03 rebase. The parser
conflict combined #02's body-continuation/wrapping helpers and typed `_Line`
paragraph handling with #03's table-aware `_sections` signature/anchors; all
existing #02 measured-width, caption, numeric-row and CJK chunk rules remained.
Both logs were preserved. Application/cache/events/frontend are byte-identical
to pre-rebase #03 1d21023; no shared lifecycle/UI behavior was replaced.
All 78 existing ingestion/table uploads passed after rebase. A new combined PDF
checks a CJK number continuing across pages before a Table Chunk, followed by a
close same-size heading: exact number 14 and p.1–2 prose provenance, p.2 table
cells, and the following Section are retained together. Its pre-rebase source
failure and integrated pass are recorded under ticket-03/post-issue02.

## 2026-10-13：#05 Summary Tree 與 Global

- **AI 初版的長度基準會被 Chunk overlap 放大：** Section Summary 的 15% 最初用全部 Chunk 文字計數；改成原始 Section 段落加 Table Chunk 文字計算，摘要依據仍包含所有 Chunk，來源記錄不變。單一超長段落的 500-token 上限、分段摘要後合併與零 Chunk parent 排除，都由公開 upload 操作驗證。
- **既有假 LLM 不能把 Router 腳本吃成上傳摘要：** 加入 Summary Tree 後，所有上傳都會先呼叫摘要；舊測試只有 ask 腳本。測試 adapter 明確提供摘要回應、完整記錄 calls，並用 ask_calls 分開斷言提問；客製抽取 adapter 的 summary 分支先回到相同 seam，避免留下多餘腳本。正式 ScriptedLLM 不改動。
- **實測推翻「列出機制名稱就足以覆蓋三句摘要」：** 初次 Global eval 的中文與恰三句通過，但 graph indexing／dual-level／incremental update 的具體語意未通過；Q1 另有 judge 摘錄含省略號而非逐字引用。保留初次 FAIL 報告，僅加強 Global prompt：短摘要也說明機制，以第一句動機與 indexing、第二句 retrieval 與更新、第三句實驗與結論安排，不改 Router 或 checker。
- **Ollama Cloud 同時呼叫實測：** 8 次 Section Summary 分別以 concurrency=1/2/4/8 執行，全部 8/8 成功；wall time 8.82/4.31/2.64/2.10 秒，所有呼叫經原 Gateway、low、num_predict=1200，沒有 length 或超 10K。只能說這組短輸入在 8 個 in-flight 內沒有觀察到限制，不能證明服務完全沒上限；遵守已定 default=4，保留可配置選项與原始 JSON。
- **短格式也不能把檢索成本挪到更新成本：** 後續三句摘要把「單次 API 呼叫」接到增量更新上；這是回答壓縮時的錯誤，加入 Global-only 的 operation distinction，要求 retrieval／indexing／incremental update 的 token 與 API 數據不得互換。保留前後報告，不改 checker、分類或數值規則。

## 2026-10-13: Issue05 independent review corrections

- **Independent review rejected a topic-fitted Global prompt:** The earlier three-sentence instructions explicitly required graph indexing, retrieval levels and incremental updates. Replaced them with Document-agnostic whole-Document, language/format, comparison-baseline, qualifier and operation-metric instructions. A non-RAG rainfall Document reproduces the old prompt defect. Existing failed/successful live evaluation artifacts remain untouched; #11 must measure quality again with this generic prompt rather than restoring the fitted instructions.
- **Source text accidentally controlled Citation mode:** A literal supplementary `[S1]` inside a Chunk switched Lookup/Synthesis to summary instructions. Public upload/ask regressions fail at the original candidate and pass with an explicit source kind carried from the Global branch through prompt selection and answer generation.
- **Filtered call assertions hid upload regressions:** Restored complete LLM-call assertions on upload/failure paths and unchanged total call count on cache replay. A temporary cache-hit mutation that recomputes summaries is missed by the original cache test and detected by the new total-call assertion. Shared fixture ask dispatch removes duplicated summary passthrough branches.
- **Long supported questions lost detailed evidence:** Main accepted building conservative Group levels at upload time, reserving both question fields and the actual Global prompt overhead under the unchanged budget policies. An exactly-1,000-token question selects a complete Group level, while a short question retains Section Summaries. This can add upload calls near the capacity boundary; no answer-time tree generation or silent truncation was introduced. Adapter semantics and answer prompt changes now invalidate upload cache identity.
- **Recursive and failure coverage clarified scheduling:** Tests now exercise multiple Section merge rounds, multiple Group levels, all-source provenance, pathological nonreducing responses, and cancellation during concurrent Section work. A freed semaphore slot can admit one queued sibling before the failure reaches the parent; assertions verify all started siblings are canceled and awaited, with prior Document/cache preserved. Real bge-m3 is used for acceptance success paths; fake embeddings are limited to the very large recursive and pathological-provider probes; sibling failure/cancellation uses real bge-m3.
- **Implementation corrections during this work:** An overly broad text replacement temporarily inserted policy constants into a `min()` expression; corrected before candidate submission and reran the focused suite. The original HTTP test counted old progress events, so its assertion now checks stage order and the actual Section/Document progress values. An initial isolated-baseline test lacked pytest's asyncio configuration; rerun with `--asyncio-mode=auto` supplied valid mutation evidence.


### 2026-10-13 — Issue05 integration after Issue02/03

- **Uncertain table warnings were lost across summaries:** A real-bge public upload/Global/cache regression with table-only Sections showed that the model can omit the reconstruction warning. Summary generation now preserves that exact warning deterministically at split, merge, Group and Document levels, while keeping full source Chunk IDs and Section provenance. The answer still receives the shared table limitation rule.
- **Conflict-resolution automation required repair:** An overbroad multiline conflict regex truncated unstaged files. Recovered each file from unmerged index stages, then used a line-bounded pattern and rebuilt generated frontend output. Preserved integrated parser/table/cache dependencies, retrieval budget-drop fields and SourceContent while retaining Global summary dispatch.
- **Evidence wording corrected:** Earlier report incorrectly listed sibling cancellation among fake-embedding tests. Its actual Application uses real bge-m3; only the very large recursive and pathological-provider probes use fixed vectors.
- **Generic integrated live evidence remains mixed:** One fresh Q1/Chinese-three-sentence run on aa50859 reports 5/8 and 7/10. Q1 Judge omitted verbatim text or inserted ellipses; Chinese answer lacks several required semantic details. The report retains raw answers and all 49 calls, with no truncation/budget failure. No fact/checker relaxation or topic fitting was used. Final N=3 quality gate stays in Issue11.


### 2026-10-13 — Issue05 independent integration correction

- **AI reused a character splitter where table boundaries mattered:** The independent reviewer found that oversized Section summarization flattened Table Chunks and then split inside rows/cells, dropping repeated table context from some requests. A public upload test with a real 12-page table-only Section and bge-m3 reproduced an incomplete source Table Chunk in the guarded Section requests. Section inputs now pack whole original Chunks, keeping Table captions/headers/rows together; recursive summary merging and the shared guard remain unchanged.
- **A passed forbidden check did not validate all comparative claims:** The recorded three-sentence Chinese answer overstated LightRAG win rates over all baselines/datasets, including the known Mix Overall GraphRAG exception. Q1/Chinese facts omit Q2's specific GraphRAG all-datasets prohibition; the live NOT_ALL_BEST check has a different target. This is a confirmed coverage gap, distinct from proving a same-fact judge false negative. Summary text was not recorded in that report, so the semantic failure cannot be localized to upload versus answer. Exact answer and original checker outcome are retained and handed to Issue11; no topic-fitted prompt or relaxed checker was added.
- **README lagged the implemented contract:** Updated the opening C/S Citation description, upload summary n/N progress and stale claim that Summary Tree was a later ticket.

### 2026-10-13 — Issue09 rendering and integrated overview corrections

- **Rendered Markdown positions differ from raw answer positions:** Independent review caught Unverified markers attaching to the wrong sentence after Markdown decoding, Unicode and newline transformations. The renderer now maps decoded text back to raw offsets and preserves CR/CRLF boundaries. Source-request races and backend-restart stale state were also corrected. Historical RED/GREEN evidence remains in `docs/verification/ticket-09/review-corrections/` and `crlf/`; the integrated rerun records 10 source/restart/marker checks and 6 newline checks, alongside 148 broader assertions.
- **Mounted content was not persistent visible context:** QA05 reproduced an entirely off-screen overview after six ordinary Global turns at1280×720. The approved Tufte sidebar plus bounded internal overview scrolling keeps the desktop panel visible while chat grows, including long summaries. The implementation's measured RED/GREEN evidence is in `docs/verification/ticket-09/integration/`; independent integrated QA must still confirm the fix before Issues05/09 close. Phone page flow and intentional modal occlusion are recorded separately rather than mislabeled as desktop viewport persistence.
- **A fixture assumption was mistaken for a source-kind expectation:** Long scripted summaries made the real backend correctly select a Group level while a browser check expected Section. Separate short and long documents now exercise both routes; the failed ledger is preserved and production routing was not changed to fit the test.
- **Final model-output rendering needed real evidence:** The new pre-review self-check applies to the Markdown/Citation/Unicode consumer as well as the model-output producer. Independent review identified that post-annotation checks were scripted; one real gpt-oss browser smoke is required on the final renderer. Its output only proves the formats actually observed, and does not replace the final Issue11 Golden Facts gate or deterministic rare-marker regressions.

- **Observed real final-renderer smoke:** On frozen `cb4f1c9a164a40243a38358e59f2ed5c126bcf7c`, actual bge-m3/OllamaLLM produced a completed Traditional Chinese three-item Markdown list with three `[S1]` Citations, U+202F/U+3000 spacing, working Section source and actual Trace. All four real gpt-oss calls ended `stop`; maximum estimated prompt plus reservation was 3,892/10,000 (actual prompt plus reservation 3,667). No Unverified or CR/CRLF was emitted, so their rare-case coverage remains deterministic. [Real smoke evidence](verification/ticket-09/real-smoke/REPORT.md). Independent real LightRAG Q3/QA09 and semantic/N=3 Issue11 gates remain open.

## 2026-10-13 — Issue10: typography/table assumptions failed on the second Document

The fixed industrial robotics Document (arXiv2603.06749v1) exposed assumptions
that LightRAG did not: same-baseline split Appendix headings were rejected as
shared table rows; a bold prose mention of Appendix activated appendix mode;
indented headings split; an ordinary numeric table cell combined with the next
row's label into a false Section. Author lines and body emphasis created false
summary boundaries. Read-only preflight at3432aa09's integrated predecessor
0718466 recorded64 detected Sections and no real appendices after References.

Public upload regressions first failed for each behavior, then passed after
generic relative-typography/geometry corrections. A repeated numbered hierarchy
now distinguishes body emphasis, the title is metadata, and explicit Appendix
openers resume after References. Wrapped titles and spatially adjacent Section
number/title fragments are merged without fixed fonts, coordinates or paper
names. The selected Document now has30 source-bearing Sections and four real
appendices; target lengths remain estimates until live ingestion.

Appendix captions with letter-prefixed numbers and repeated geometric table
headers also required fixes. Continuations retain page-specific Table Chunks;
uncertain grids keep raw rows and the reconstruction limitation. Sorting arrows
may disappear from repeated headers; header comparison ignores the arrows while
retaining source text. One synthetic fixture initially joined adjacent header
cells because their text boxes overlapped; spacing was corrected before claiming
the header-variation regression passed. RED/GREEN and retained primary PDF
evidence: `docs/verification/ticket-10/`, `.lat/briefs/nova-i10-preflight.md`.


### Issue10 actual failures and subsequent corrections

- Trials1/2 failed upload because gpt-oss interpreted nominal summary lengths loosely and exhausted the unchanged1,200-token reservation. Trials3/6 failed bounded length correction. No failed draft was published or cached. Complete Section Summaries are now regenerated when above500 tokens; overlong intermediate parts still feed recursive merges. Truncated calls retry once from complete evidence at low, with every returned Trace retained; corrections never slice text. #05 stress fixtures now use450-token ordinary Section outputs while preserving long Group/partial failure injections, recursion, cancellation, progress and provenance assertions.
- Trials4/5/7 successfully built30 genuine Section Summaries and one Group layer (7,390/7,588/7,641 actual tokens), but whole-Document semantic checks failed. Group source prompts now expose actual covered Section titles; generic instructions preserve supplementary contributions, reporting limitations and the distinction between missing evidence and absent capability. Extraction warnings describe the system, not the authors. No test names, paper names or expected numbers were added to production instructions.
- Unreconstructed reference tables let model-version1.5 drift into invented score claims. Generic original-word coordinates separate wrapped label/version text from numeric columns, returning raw fallback on missing/ambiguous cells. All324 Table D5 rows now reconstruct;3,888 metric values match an independent PDF-word census, and the first two rows are spot-checked. This does not independently validate every row/column association. Closed single-cell query tables and fragmented rule borders retain raw text with visible caveats.
- An affirmative numeric judge excerpt omitted the already-required count of expert-annotated papers. Added structural evidence terms and RED/GREEN checker tests so this cannot silently pass. Earlier report outcomes remain unchanged historical model judgments; their full subset guarantee is insufficient. The finalized numeric question spans expert-subset prose and a floating table, so Synthesis is legitimate (Main11360); corrected only the eval expectation, never the Router.
- A first numeric census counted a caption's Section3.2 reference as a table value. Restricting the audit to below the printed header corrected the census, without modifying product data. LightRAG Table2 source/rendered bytes, every labelled row and page/Section match the3432aa09 baseline; measured raw/rendered lengths are790/1,392 tokens with the installed tokenizer. The earlier421-token figure is not reproduced by this unchanged baseline representation; no invented count is reported. Full source/live evidence: docs/verification/ticket-10 and eval/reports/issue10-trial*.

### Issue10 frozen checkpoint: persistent semantic failures

- Trial8 treated a processor caution about inferring a Total formula as an author claim that the methodology was hidden. The claim originated in Appendix D, propagated through Group1.2, and contradicted the actual global-maturity definition and three-paper expert-validation description in §8.1. Removed the generic formula caution from source meaning; saved the complete propagation trace. Trials9/10 still generalize missing validation within an appendix excerpt into absent validation across the Document. Generic scope instructions have not resolved this contradiction; original FAILs remain.
- Length correction regenerated from a previously generated draft, allowing that draft's mistakes to become new evidence. A public upload RED/GREEN now verifies that each correction receives the original complete source, while preserving its targets, reservations and trace records. The current full deterministic suite passes287 tests; this does not establish live semantic correctness.
- Main11593 approved a fixed Lookup/Synthesis accepted set for the mixed numeric query, always requiring a valid real Router and no fallback. Trial10 correctly answers the three-paper counts, accuracy/F1 and comparison, but the inherited numeric clause binder rejects the InfoFound accuracy after a semicolon. The reported FAIL is preserved pending independent Review, without changing the binder or weakening the requirement.
- One separately labeled diagnostic judge incorrectly required verbatim PDF quotations although only the answer and criterion were supplied. Its output is retained as an unreliable diagnostic, never substituted for acceptance. Whole-answer factual coverage remains an answer property with verbatim answer evidence and unchanged content requirements.
- Main11718 changed the next step to a frozen committed checkpoint and independent full Review before further prompt iterations. Latest ingestion has30 genuine Section Summaries totaling7,693 tokens and a Group layer; all53 traced calls stay below10K. Three truncated attempts were visibly discarded/retried. Numeric binding and unsupported validation-scope claims still fail; no Issue10 completion, acceptance waiver or self-review is claimed.

### Issue10 independent-review corrections and D06 convergence

- Independent Reviews of597db375/588638d found substantive Abstract content skipped as front matter, published Section Summaries below80tokens, ungrounded local-absence/validation claims, numeric clause-association errors, and missing correction records. Abstract is now conserved without author metadata;80–500 bounds regenerate from original evidence and fail closed instead of slicing/padding. Table-dominant summaries select validated original source-span IDs through the existing native Gateway; selected text retains original caption/header/Chunk provenance. A processing-scope caution was initially misattributed to authors in a real diagnostic, so it moved into trusted system instructions. Scripted contract-sized fixtures verify functional state/provenance, not real summary fidelity. One diagnostic JSON was accidentally overwritten and restored from its complete original output; neither result was promoted to acceptance.
- The saved original finalN3 run completed six answers but pytest exited1 because an AI-written upload assertion expectedNone although success is an empty string. The gate now accepts empty string/None and still rejects a nonempty upload failure. Its original exit1 and all raw fact outcomes remain unchanged. D05/D06 change delivery to report per-questionN3 rates and causes, with scoped Review and two QApoints; they retain the10K, grounded Citation, fixed-refusal and deterministic-test contracts.
- All three original Global answers cited “28 expert judgments.” Independent Review and source tracing established that28 was the physicalp28 footer between “against” and p29's “expert judgements,” not an author-reported count. It first entered Section8's generated summary, then Group1.1/Document overview/Global answers;§8.1 separately preserved the actual three expert-annotated papers. The90%-height integer rule was wrong for this template. Generic recurring sequential margin geometry now removes corroborated folios, including offsets and top/bottom placements, while public upload/ask/source regressions preserve body99, table23, Section2 and a legitimate margin41. No28/paper/font expectation is embedded in production parsing.
- Original numeric answers visibly match Table9: AllN447/accuracy0.966 and InfoFoundN304/accuracy0.951 (lower), F1 unchanged0.762 in both, validation on three papers. Raw expert_agreement0/3 is retained: judge excerpts1/3 omit the correct three-paper sentence; excerpt2 includes it but the binder rejects postpositive setting labels/shared-F1 prose. The old table checker also falsely accepted reversed values when the other setting appeared in a “Compared with” column. Already-produced generic row-owner/postpositive/shared-metric fixes pass adversarial tests and are retained underD06; no further optional checker tuning or silent regrading. Main owns the PRD eval check_fact seam exception.
- The ONE authorized fresh D06 run after parser/cache invalidation failed upload in53.70s: the native model ignored the exact private JSON schema and added note/uncertainty fields on four AppendixC selections. Strict validation exhausted its bounded corrections, cancelled siblings, and published no Ready/tree/cache or question answers. Its0/3 rows represent application failure, not six measured answer-quality misses. The corrected nonempty-error gate correctly exited1. Saved final evidence is issue10-d06-final-n3 with raw companions; Main was notified for bounded recovery, with no unapproved retry or prompt loop. Previous successful7334-token/Group run and two discarded/retried length attempts remain historical evidence.
- Final changed-source deterministic suite:310passed/3eval deselected/6warnings in293.86s, exit0; targeted19passed and ruffPASS. These passing checks establish source/lifecycle/budget regression behavior, not final real-model fact coverage. Main13138 authorized exactly one recovery freshN3 on identical fixed source/provider/settings/questions, preserving the failed upload and making no prompt/protocol tolerance changes; that recovery is separately labeled issue10-d06-recovery-n3.
- Main-authorized single same-source recovery also failed closed,106.59s: after recursive narrowing, an AppendixC batch contained only three original spans E633/E634/E635. All available source plus caption totals74tokens (92with system warning); the80-original-token minimum is impossible in that narrowed batch, so four corrections fail. This is a later-pool feasibility defect, distinct from the first run's extra-key provider behavior.93completed calls stay within10K(maxestimated9850/reported9583),1length; noReady/tree/cache/answers. New0/3 rows are application failure placeholders, not measured quality. Stopped after the authorized recovery, notified Main with the exact blocker, preserved passing source fixes and all historical outcomes; no lowering minimum, padding, protocol change or third cloud run. Fresh completedN3 remains explicitly unmet pending Main's further release.

### Issue10 D08 authorized minimal selector recovery

- Direct humanD08A permits discarding extra provider commentary while strictly validating span_ids, preserving feasible80–500distinct original candidate pools, and finishingD06 genuine heading-number preservation. No application-failure/zero-answer N3 waiver was approved. Source changes are limited to these functional corrections; numeric fixes and all historical reports remain unchanged, with no prompt/model/API/budget tuning.
- The native schema failure now consumes only span_ids and ignores every other provider field. A public upload RED→GREEN verifies an injected note never appears in the published summary; unknown/duplicate/missing/wrong-type/nonJSON ID output still fails closed. The selector never uses generated commentary as evidence.
- Sumi's scoped public-upload reproduction exposed another AI-written heuristic error: sequential isolated top-margin headings1/2 with separated titles were treated as page folios. New public RED→GREENs cover both y68/y80 titles below y32 numerals, retain numbered Sections/Chunk source context, and remove true bottom folios28/29. Relative title typography/alignment protects genuine numerals and combines the separated pair without a document-specific font/number rule.
- The74-token dead end was reproduced through fresh public upload with deterministic replay of recorded native IDs, using current PDF/source validation; recorded model prose is never used as source. Narrowing now restores distinct original spans for thin retained source units before repacking, then checks80–500feasibility on every returned batch and can move contiguous whole units between neighbors within guarded capacity. It never duplicates/pads evidence, counts warning tokens toward80, lowers the minimum, slices rows/context, or feeds generated drafts back as evidence. Impossible/nonreducing pools still fail. The replay changes from the exact74/92ingestion error to Ready with valid original source IDs.
- Final targeted regression result29PASS5.38s and ruffPASS. One final deterministic suite and one fresh same-PDF/questions/criteria N3 are running on stable D08production code; actual final results will follow. D05quality/forbidden failures remain reported and do not cause an all-quality-PASS exit gate; application success and hard contracts remain required. No optional numeric or prompt loop follows the measurement.
- Final freshD08N3 completed all SIX actual answers: functionalpytest1PASS/exit0 in133.72s, while the raw Golden Facts report remainsFAIL. Numeric Citation/Router/forbidden3/3, expert_agreement1/3; GlobalRouter3/3, coverage0/3. ManualTable9/§8.1 values/counts/subset match all three numeric answers; rep1judge omits the three-paper sentence, rep2passes, rep3binder cannot associate sharedF1 across separate bullets. No silent regrade or further numeric tuning. All Global answers now preserve THREE expert papers and do not claim28judgments. Broad judge failures give no excerpt; observed limits include compressed hardware coverage, corpus works mislabelled as RFMs in reps1/2, compressed appendix roles and some uncited numeric-rep3claims. These remain reported model/evaluator defects underD05/D06, no new validator/prompt loop.
- Fresh ingestion7777Section Summary tokens/31summaries(min81,max497),149Chunks, oneGroup/twoNodes, allfourtrueAppendices and completeReady/cache.107completedcalls, maxestimated9729/reported9462 including reservation; two Sectionlengths29→33 and39→44visiblydiscarded/retried, no failed draft in published tree, no answer/judge truncation. Every original Summary Chunk reference resolves. Saved final evidence issue10-d08-final-n3 and d08-final-n3-run; metadata truthfully records79d0f55+dirty source before its checkpoint commit. Earlier failures remain unchanged history.
- Final changed-source deterministic316PASS/3eval deselected/6warnings348.69s exit0, targeted29PASS5.38s, ruffPASS. Production code was stable before these checks and freshN3; later edits only complete final conclusions/flow inventory/ai-log. Freeze exact checkpoint for Main verification and Sumi's boundedD06+D08 Review, with no self-review/merge/push/optional tuning or acceptance claim.

### Issue11 effective tuning and honest final measurements

- Main14083 formal-release implementation makes environment/injected Chunk, retrieval k, BM25 weight, answer think and Summary concurrency reach the real Application/eval rather than a settings label. Pure-Python BM25 weighted RRF retains cosine separately; native answerlow/medium keeps the unchanged3000 reservation. Public upload/ask RED→GREENs cover these seams, actual HTTP status/query-embedding stage labels, and duplicate-question overhead. Existing contains boundary tests already pass; no unnecessary rewrite.
- The first real retrieval matrix was confounded because Router Sub-queries changed between Chunk sizes. It suggested800dense. An AI edit for the first attempted control silently failed to match its target, so plans still regenerated; that result is explicitly INVALID CONTROL. The corrected36-row matrix uses the same frozen actual Q2/Q3 plans for every setting and selects500dense5/3/2 (MRR1, measured Table2/cost/update context coverage). Unchanged original Chunks/vectors are transparently reused from older ingestion records; their trees are not final-cache proof. No historical report is replaced or regraded.
- Actual low/medium Q2/Q3 N1 comparison remains labelled800dense:6/20 versus8/20 fact passes, both functional with no formal Router/Answer length. Medium retained provisionally; no claim that the tiny comparison proves optimality at500. Final effective defaults remain500/dense5/3/2/medium/4 and finalN3 measures those settings independently.32short native Summary calls succeeded at client in-flight1/2/4/8; timings overlap some of this worker's own ingestion and do not establish production throughput or a universal service ceiling. Conservative4 retained.
- Adding Chinese script measurement exposed scripted eval fixtures that answered English to Chinese questions; the fixtures now provide actual Chinese evidence while keeping their original lifecycle/history assertions. The first full suite had320PASS/5FAIL: test adapter lacked settings, duplicate-question label changed a public expectation, and removing duplicate input freed enough budget to invalidate an old too-small evidence fixture. Corrected expectations/fixture size preserve the tested language/reference/budget behavior. Final325PASS/3eval deselected,258.19s; frontendtypecheck/build/eventparity/ruffPASS.
- Judge now requests a reason plus a single continuous answer excerpt with exact capitalization; real outputs still violate that contract. Q1/ChineseQ1 share the already-existing forbidden GraphRAG universal-superiority criterion, exposing prior coverage gaps. Chinese property checks preserve opposing-script misses separately; facts and numeric binder are not softened. Native finalLightRAG21answers completed with170calls, maxestimated9617/reported9392 including reservation, no length or budget violation, fixed refusals9/9. The raw GoldenFacts report remainsFAIL; final per-fact/failure analysis is preserved in eval/reports/issue11/final-lightrag.*.
- FinalLightRAG Q2 actualRouterplans ask for broad mechanisms/performance/limitations, and the answers omit retrieval cost/update despite the controlled frozen-plan coverage. Q1 overclaims and Q3 missing explicit comparisons remain true answer defects; Q3rep3 says fullLightRAGbeats every variant despite its own74.4/67.6 table, while the raw forbidden Judge reportsPASS (known false accept, not regraded). Some Q1 increment/update and Q2 numeric row failures are Judge excerpt/binder limitations; individual causes are recorded separately. D05/D06 allow measured semantic defects, not an invented allPASS.
- Final second-document N3 completes allsixanswers,107callsmaxestimated9847/reported9580; two discarded/retriedSection lengths and one Judge length, no formalRouter/Answerlength. Numeric raw0/3, targetCitation2/3, global1/3. ManualTable9/§8.1 matches all answers (3papers;All447/.966/.762;InfoFound304/.951/.762), with binder shared-F1/owner failures and a Judge excerpt omitting the paper-count sentence. Saved-plan no-LLM diagnostic mapsrep2's validC9 toTable10 insteadTable9; Main notified, no grounded-referencePASS claimed. Globalrep2requiresanexplicitdenial notpresent;rep3Judgelengthfails.324works mislabelledRFMs and some scope inference remain true generatedanswer/tree defects.
- Two REAL currentpipeline caches built after the final source/settings change:LightRAG42Chunks/4383Sectiontokens, second149Chunks/7705tokens, eachGroup layer, observedzero-model-callReadyreuploads. Manifest/actualpayloadpaths in eval/reports/issue11/cache-manifest.json; caches/PDFs remainignored for Main/demo transfer. Final27actualanswers preserve FAILrates. No extra qualityloop, summaryminimum/budget weakening or expectation fitting.
- Held-out native calibration smoke exposed an AI fixture mistake: single-line text_pdf placed most source off-page, so missing-duration refusals were correctly grounded in clipped input. Preserved that invalidcomplete-sourcefixture result. Corrected fit-checked one-page textbox and fixed PDFbytes through publicreuploads. Four novel questions: Englishsixsensors/seventeenminutes and traditionalChinese durationcorrect[C1], absentmanufacturerfixedrefusal; simplifiedChinese stillmixedtraditionalforms.10nativecalls allstop,maxestimated3868/reported3643. No productionpromptfitting or hidden regrade; source layout matters to test validity.
- Independent exactGPT6-sol/high two-axis Review0c320a8 identified a hard Table9 Citation failure (validIDwrongsource), an internal rank-matrix seam deviation and a wrong controlled report locator; low-priority ranking-expression duplication left unchanged. Full report/nativeaxisIDs preserved in docs/verification/ticket-11/review-0c320a8.md. Main14912/14950 released only generic exact-table Citation instruction, public-event evidence/driver adaptation and bounded real verification; no semanticvalidator/newfeature/Citationwaiver or test-specific prompt. Three generic prompt lines make original27answers and2source-versionedcacheproofs stale, so one fresh correctedfinalN3/cache run preserves originals separately.
- Missing original event capture was reproducedRED then fixed at public upload/ask.11targetedPASS proves persistent CitationMap/Final/source relationship and external-adapter replay with actual embeddings; scripted checks do not establish semantic grounding. New36-row public-event matrix retains500dense5/3/2, stores actual source-order hits separately from score-sorted returned-hitRR, expressly not full-indexMRR/native answerquality. Prior internal-seam results remain historical limitations. Controlled locator corrected; no raw fact regrade.
- D09 direct user decision moves finalwebsiteQA to user/manual checklist after reviewed integration; cancels zoru workload. Worker correction/fullsuite/fresh independentReview and Mainintegratedtests continue unchanged. D09 is not a Citation waiver; worker does not edit the levi/Main checklist.
- CorrectedboundedfinalN3 completes27actualanswers onstable58005fccpipeline; LightRAG170callsmax9667/9442allstop,second102max9630/9363oneSectionlengthdiscard/retry, noformalRouter/Answerlength or10Kviolation. Current42/149Chunkcaches/4135/7763Sectiontokens eachGroup layer andzero-callReadyhits retained with currentmanifest. Originalevents now showTable9sourceCitation3/3; original2/3wrongtablefailureunchangedhistory. Numericraw1/3/global1/3 remainFAIL; rep2mislabels evaluationcounts as“papers”, rep3arithmeticconclusionuncited, and knownbinder/excerpt/coverage errors persist. Correctvalues/sourceidentity are not allsemanticgroundingPASS; Main/freshReviewassess exactsupport withoutautomaticwaiver.
- UnrelatednumericadjacentTable native smoke N1 answers37samples/meanresidual.42mm withC1actualTable7shoreline row; adjacentinland59/.73 notcited.4callsallstop,maxestimated3914/reported3689. This is bounded actualsource-support evidence, notuniversalstochasticguarantee. Correctedfullsuite327PASS/289.90s,11targeted/ruffPASS. No morequalityloops, defaults/GoldenFacts/model/budgetsunchanged; originalbuild/startup reused because thosepathsunchanged. FreshscopedindependentReviewfrom0c320a8required; D09manualwebsiteacceptancestillpendingMainmerge.
- Exactsourcecapture also exposes partialprose-supportlimits: numericrep1/3citeC4p30for3papersandtwo-before/one-afterchronology; thatChunkstates3papersbuttimingdetailisinadjacentprovidedp29context. This is not silently counted asallclaimsgroundedbyTable9source3/3. Preserve per-claimsupportlimits for freshReview/Main classification alongsideuniterror/uncitedderivedconclusion; no Citationwaiver or further stochasticqualityloop.
- Freshindependent scopedBelaReviewf089cae:Standards0;Specobservedhardunsupportedper-claimpopulation/unit/chronology/uncitedconclusionlimits, plusnonobservedGlobalTableChunkinstructionrisk. Specificwrongtableassociationnotobserved3/3correctedoriginalmaps,butnotfullgroundingPASS/waiver. Fullreport/runtimeaxislocatorssavedreview-f089cae.md. Oneboundedcorrectioncomplete; MainD10v1humanchoicepending, nofurtherquality/source/providerwork/merge. D01markerpolicyandD09manualQAdo notwaiveCitationhardlimit. Main15292permitsdocs-onlyretentioncheckpointwithsourcef089unchanged; no extra tests for this documentary save.

### 題目解讀被當成題目原文（levi，2026-10-13）

- levi（Claude）說明 10K 限制時，把題目筆記 `題目：讓 AI 跟文件對話（Chat with Document）.md` 裡「意義」欄的解讀（「必須設計分段處理、檢索或階層式摘要機制」「輸入加輸出都要控制在 10K 以內」），當成題目原文引用，還拿來回答「預先建摘要算不算作弊」。使用者貼出題目原圖指正：原文只有「假定 LLM max context size 為 10K」，以及兩個要說明的設計問題。
- 同一個錯誤先前也發生在 LangChain：筆記的「意義」欄寫了「不引入 LangChain」，被誤當成題目禁止。
- 修正：`簡報素材.md` 改寫成「題目原文」和「我們的解讀」分開（輸入加輸出合計是較嚴格的解讀），作弊疑慮的理由改用原文「說明你怎麼處理 summary?」。教訓：引用題目時，只引用原圖或「技術限制」表的第 2 欄，「意義」欄一律標示為解讀。

### D10 最終驗收例外（2026-10-13）

使用者明確選 A：將已列明的評估單位錯誤、相鄰片段時間细節引用與結論缺引用列為本版已知缺陷，停止品質修正，整合後人工 QA。原始 FAIL、獨立 Review 與未觀察到回歸的 Global 提示風險保留；這不是所有 Citation 通過的宣稱。10K、固定拒答、無效 ID 標記及確定性測試仍維持。

### D11 對話介面方向調整（2026-10-13）

使用者實際操作後指出：逐題編號與頁邊旁註不利於持續提問，表格會跑版，Trace 的英文術語難以理解。原 Tufte 初稿雖已通過設計審查，仍未充分符合對話流程。D11 改採可收合的文件／對話／來源三欄、底部輸入框與句內引用；保留米白、襯線與 10K 用量長條。Trace 改稱中文「回答過程」，原始計數與模型思考收進「技術細節（開發用）」。這是使用者改變介面方向，後端檢索、模型與事件契約不變；改版驗收由 #12 另外記錄。
