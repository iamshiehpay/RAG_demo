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


## 2026-10-12：Eval harness 的證據驗證

- **AI 修正自己的報告測試：** 第一版以整份 markdown 中的 `judge` 欄位出現次數驗證呼叫數，誤把 fact 的檢查方式欄位也算進去。真實 bge-m3／scripted LLM 的三次操作測試抓到失敗後，改成只比對 LLM 呼叫列，並同時斷言 recording Gateway 的六筆呼叫與 2/3 通過率。教訓：報告文字的斷言要對準使用者要核對的紀錄。
