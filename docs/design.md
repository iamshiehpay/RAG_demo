# 設計規格與實測依據

這份文件承接原 AGENTS.md 的詳細設計規則，供修改對應功能時查閱；常駐限制仍見 [AGENTS.md](../AGENTS.md)，術語見 [CONTEXT.md](../CONTEXT.md)。路徑寫在行內程式碼時，以 repository 根目錄為起點。

規格描述預期行為，**不代表所有模型回答都已達標**。未附引用的句子目前不自動標記，A9 的限制題仍是已知缺陷。正式數值由 [policy.py](../src/chat_document/policy.py)、[settings.py](../src/chat_document/settings.py) 與 [llm_gateway.py](../src/chat_document/llm_gateway.py) 實作；變更決策時同步更新相關文件與測試。

提問編排已改用 LangGraph，僅限 request-scoped StateGraph，不增加 checkpoint persistence、agent loop 或框架檢索器。責任與取消契約見 [LangGraph ADR](adr/2026-10-14-langgraph-ask.md)。

## 已定決策

| 項目 | 決定 | 原因 |
|---|---|---|
| LLM | `gpt-oss:120b-cloud`，透過本機 Ollama daemon 的原生 `/api/chat` | 本機已登入 Ollama，不需要 API key；原生 API 才能控制 `think` 和拿到 token 計數 |
| Tokenizer | tiktoken `o200k_harmony` | 跟 gpt-oss 一致 |
| Embedding | 本地 Ollama 的 `bge-m3` | bake-off 中 MRR 最高（見下方早期實測）；跑在本地，避開「embedding 算不算用 API 解析文件」的灰色地帶；不需要 PyTorch；中文問題能檢索到英文內文 |
| 檢索 | 以 dense（bge-m3）為主；BM25 是否加入，由 eval 結果決定 | 等權重的 RRF hybrid 實測反而讓 MRR 下降，因為 BM25 對中文問題無效 |
| Summary | 上傳時就建好 Summary Tree；Global 問題依其中一層產生回答，細節見下方的「摘要規則」 | Q1 必須涵蓋全文 |
| 問題分流 | 用一次 LLM 呼叫（router）同時產出三樣東西：Question Type（Global / Synthesis / Lookup）、Standalone Question、Sub-queries（只有 Synthesis 需要）。Router 用 `think="low"`；prompt 規定「不確定是 Lookup 還是 Synthesis 時，選 Synthesis」；JSON 輸出壞掉時退回 Lookup。早期 12 題已整理為 `src/chat_document/router_regression.py` 的回歸資料 | 關鍵字規則判斷不了換句話說的問句（例如「這篇在講什麼？」）；把追問改寫合併在同一次呼叫，多輪對話不必多花一次呼叫；`low` 最快、token 用量最穩定，而把 Lookup 誤判成 Synthesis 只是多檢索一些，反方向誤判則會漏掉散在其他 Section 的內容 |
| 後端 / 前端 | Python + FastAPI；前端用 React + Vite + TypeScript。build 好的 `frontend/dist/` 一起 commit，由 FastAPI 直接提供；開發時由 Vite 開發伺服器把 `/api` 轉送給 FastAPI。設計前先載入 `web-design-engineer` skill | React 的元件寫法讓多狀態的介面（串流、引用、Trace、上傳進度）比較好維護，AI 寫 React 也最熟練；TypeScript 能抓出前後端資料格式對不上的問題。commit `dist/` 是為了讓評審只裝 Python 就能跑，**所以前端改完要重新 build** |
| 視覺設計 | `web-design-engineer` skill 的 `tufte-dataink` recipe：三欄可收合：句中引用編號，點了在右欄顯示原文；Trace 用迷你長條顯示每次 LLM 呼叫的 token 用量，以 10K 為滿格。因為要分享螢幕 demo，內文放大到 15～16px；中文字型用 Noto Serif TC，字型檔放進 repo；互動只保留功能必要的部分，不加裝飾性動畫 | 這個產品的核心是「拿得出證據的回答」，Tufte 的風格就是為了呈現證據而設計；而且跟常見的深色 AI 聊天介面有明顯區隔。這個 recipe 本身不建議用在互動介面，所以把互動壓到最少 |
| 串流 | 回答用 SSE 串流，依序顯示：判斷問題類型 → 檢索 → 思考中 → 回答逐字出現。開始產生回答前，先傳「編號 → 頁碼與 Section」對照表，讓 `[C3]` 能即時變成可點的引用；回答結束後再送出驗證過的引用清單。模型的思考內容放在「回答過程」的技術細節（開發用）裡，預設收合 | 不串流的話，每個問題要對著空白畫面等 5～10 秒 |

## 切塊規則

1. 以 Section 為單位切，Chunk 不會跨越 Section。
2. 在同一個 Section 內，把整段的段落裝進 Chunk，裝到約 500 tokens 就換下一塊。段落和段落之間不重疊。
3. 只有單一段落超過 500 tokens 時，才在句子邊界切開，切開處重疊約 10%。
4. 表格保持完整，成為一個 Table Chunk，內容包含 caption 和寫明數字意義的表頭，並記下內文中哪些段落提到它（例如「Table 2」）。
   - 用文字座標重建失敗時，保留原始文字，並把這個 Table Chunk 標記為「結構未能可靠重建」。回答引用它時，必須說明這個限制。
   - 表格超過 2,000 tokens 時，依列分段，每段都重複表頭。
5. 每個 Chunk 前面加上它的 Section 標題，並帶有頁碼。標題同時用在 embedding 和 prompt 裡。
6. 移除 References；附錄保留，並標示為 Appendix。
7. 檢索時，視需要帶出相鄰的 Chunk，以及和 Table Chunk 互相連結的段落。前後文靠這一步補足，所以段落之間不需要重疊。

500 tokens 是 #11 以真實處理／Router 的 256 / 500 / 800 與 top-k／加權 BM25 比較後選定的值。dense、Lookup 5／Synthesis 3／Sub-query 2 在此設定下涵蓋 Table 2、成本與增量更新，三個目標來源在該實驗的回傳結果中排名第一；這不是完整索引的 MRR，也不是回答品質證明。修正版方法與限制見 [評估結論](../eval/reports/issue11-correction/conclusions.md)；`eval/reports/issue11/` 保留為歷史證據。回答 medium 保留 3,000、summary concurrency=4；low/medium 的 N=1 比較使用 800-token dense，僅作探索觀察，不是最終設定的顯著性證明。最終 N=3 使用選定的 500-token dense。

不用固定長度加重疊，原因有兩個：

- 結構解析得出來（見下方早期實測）。
- 在 10K 限制下，重疊的文字會佔用 Chunk 能用的額度。

## 摘要規則

上傳時就建好 Summary Tree：

- **Section Summary：** 長度約為該 Section 原文的 15%，最短 80、最長 500 tokens。長度跟著原文走，短章節才不會在全文摘要中佔太多比例。
- **Group Summary：** 只有在所有 Section Summary 加起來放不進回答的額度時才需要。做法是把相鄰的 Section Summary 分組再摘要，一層層往上合併，直到某一層放得進去。
- **Document Summary：** 最頂層，仍在上傳時建立；目前介面已移除上傳後直接顯示的概覽區塊，不代表移除 Summary Tree。

Global 問題一樣要呼叫 LLM 產生回答（`medium`），依據是「放得進額度的最詳細那一層」。這篇論文的 Section Summary 加起來約 3K tokens，可以直接用。不直接回傳算好的摘要，是因為它無法配合問題的格式和語言，例如「用三句話、中文總結」。

## 檢索規則

| Question Type | 檢索方式 |
|---|---|
| Lookup | 用 Standalone Question 取前 5 名 → 加上連結的表格或段落 → 剩下的額度依名次補上相鄰的 Chunk |
| Synthesis | Standalone Question 取前 3 名，每個 Sub-query 各取前 2 名 → 合併、去除重複 → 加上連結的表格或段落；超過 6,000 tokens 時改用分批抽取 |
| Global | 不檢索 Chunk，用 Summary Tree（見摘要規則） |

- **Prompt 裡的 Chunk 依原文順序排**，不依相似度分數排；每個 Chunk 都標上頁碼和 Section。照原文順序讀起來比較連貫，也比較不會遇到「中間的內容被忽略」的問題（lost in the middle）。
- **Synthesis 不放 Section Summary**，把空間留給原文 Chunk。如果 Golden Facts 顯示 Q2 缺少整體觀點，再加回來。
- **前 5、前 3、前 2 是目前選定的預設值**；再調整時要用評估報告記錄結果。

## Citation 與「文件中未提及」

- **用短編號引用。** Prompt 裡每個 Chunk 標上 `[C1]`、`[C2]`…，Global 問題的 Section Summary 則標上 `[S1]`、`[S2]`…。LLM 只寫編號，後端再把編號轉成「p.8 §4.3」，介面上點一下就能看到原文。照抄完整的位置字串容易出錯，例如把 p.8 寫成 p.9；短編號則能確實對回來源。
- **來源要能一路追溯回原文。** 不論回答經過幾層摘要或抽取，Citation 都能點回原文：
  - Section Summary 記錄它所屬 Section 的全部 Chunk 編號；Group Summary 記錄它涵蓋的 Section。
  - 分批抽取時，LLM 必須在每條事實後面標上 `[C#]`；合成回答時，這些標記要保留下來。
  - `[S#]` 點下去，顯示該 Section 的頁碼範圍和摘要內容。摘要只追溯到 Section 層級，不做逐句追溯，否則摘要會被大量標記弄亂。
- **引用了 prompt 裡沒有的編號時，不會靜默刪掉。** 移除該編號，並在那句話標上「未驗證」，同時在 Trace 記錄數量。只刪編號會讓沒有根據的句子看起來像有根據。
- **文件裡找不到答案時，回答一句固定的話。** 目前只靠 prompt 規則判定，不用相似度分數設門檻，因為中文問題對英文段落的相似度本來就偏低，門檻很難設準。Trace 會記錄最高的相似度分數；之後如果能回答和不能回答的問題，分數明顯分得開，再加門檻。
- **用提問的語言回答**，但引用的數字保持原樣。

## 上傳處理與快取

- **上傳後立刻回應，處理在背景進行。** 用 SSE 即時推送目前階段（解析 → 切塊 → embedding → 摘要 n/N → 完成），全部完成後才開放提問。處理時間取決於文件長度、模型服務與快取，不保證固定秒數。
- **Embedding 每批 8 個 Chunk**，每批完成後推送已完成的 Chunk 數 n/N；全部完成後才發布 Document。
- **Section Summary 平行產生**，同時呼叫數預設 4，可以調整。並行實測見 `eval/reports/issue11/concurrency.json`；測過的並行數不等於服務的固定上限。
- **處理結果依檔案內容的雜湊值存到 `.cache/`**，內容包括 Chunk、embedding、Summary Tree。快取的鍵值同時包含「處理流程的版本」，所以改了切塊或摘要規則之後，舊快取會自動失效。同一份檔案重新上傳時直接取用快取。
- **只快取上傳時的處理結果，不快取回答。** 調整 prompt 和 think 等級時，要看到每次真實的回答。

## Context Budget 分配

每種 LLM 呼叫的額度都是固定的，budget guard 依這張表檢查。表中的 prompt 上限已經扣掉 300 tokens 的安全邊際。

| 呼叫 | think | 輸出預留（思考 + 回答） | prompt 上限 |
|---|---|---|---|
| Router | low | 600 | 9,100（對話歷史只帶最近 2 輪） |
| Section Summary | low | 1,200 | 8,500（Section 超過上限就先切開） |
| Group Summary | low | 2,500 | 7,200 |
| Document Summary | low | 2,500 | 7,200 |
| 分批抽取事實（Synthesis 的 Chunk 超過 6,000 tokens 時才用） | low | 1,000 | 8,700 |
| 產生回答 | medium | 3,000 | 6,700（扣掉系統提示和問題後，約 6,000 可以放 Chunk） |
| Judge（eval 用） | low | 1,000 | 8,700 |

- **不用 `high`。** 在 Q2 規模下，`high` 的思考會把回答擠掉（見下方早期實測）。
- **讀錯表格的對策：**
  - Table Chunk 的表頭要寫明每個數字的意義，例如「每格是 NaiveRAG 勝率 / 變體勝率」。
  - 產生回答的 prompt 規定：引用表格時，先說明比較基準，再下結論。

  這兩項的效果都用 Golden Facts 驗證，不靠調高 think 等級。

### 放不下時怎麼辦

Budget guard 只負責攔截超額。把內容安排到放得下，是上游的責任。所以 guard 一旦 raise，就代表上游有 bug，不是正常的處理流程。

| 情況 | 處理 |
|---|---|
| 使用者的問題超過 1,000 tokens | 不呼叫 LLM，直接拒絕並說明原因 |
| 對話歷史 | 只帶最近 2 輪，每輪截到 500 tokens |
| Section 超過 8,500 tokens | 先切開，各自摘要，再合併 |
| 表格超過 2,000 tokens | 依列分段，每段重複表頭（見切塊規則第 4 條） |
| 檢索到的 Chunk 超過 6,000 tokens | 分批抽取事實，每條事實標上 `[C#]` |
| 抽取出來的事實超過 6,000 tokens | 分批再合併一次，直到放得下 |
| Section Summary 加起來超過 6,000 tokens | 建立 Group Summary（見摘要規則） |

## 失敗處理與串流狀態

- **串流出來的文字一律先標示為「暫定」**，收到成功結束的事件才定稿。
- **只要 `done_reason=length` 就算失敗**，即使已經有內容也一樣。前面的實測裡，`high` 有一次寫到 918 tokens 才被截斷。
  - 失敗後，改用 `low` 重試一次，畫面顯示「重新產生中」，並取代原本的暫定文字。
  - 再失敗的話，顯示錯誤訊息，不留下被截斷的答案。
- **無效的引用**：在那句話標上「未驗證」，不靜默刪除（見 Citation 一節）。
- **Router 失敗：**
  - JSON 輸出壞掉時，退回 Lookup。
  - 連線失敗或逾時時，不繼續檢索；顯示錯誤訊息和重試按鈕。
  - 查詢時 embedding 失敗，也照同樣方式處理。

## 早期實測與設計依據

以下保留開發時的觀測與腳本，條件與樣本數都只適用於當次實驗，不視為服務永久保證。腳本在根目錄 `spikes/`、原始輸出在 `spikes/out/`；較新的整合與評估證據由 [開發指南](development.md) 導覽。若實測推翻設計假設，須修正假設並記錄證據。

- **Ollama Cloud 會忽略 `num_ctx`。** 送 4K tokens 的 prompt、設 `num_ctx=1024`，結果 4,083 tokens 全部照收。10K 限制只能靠我們的程式守住。
- **`num_predict` 包含思考過程。** 設 `think="high"`、`num_predict=200`，200 tokens 全被思考用掉，content 是空的，`done_reason="length"`。預設改用 `think="low"`；只要 `done_reason="length"`，就視為失敗（見「失敗處理與串流狀態」）。
- **`think=false` 關不掉 gpt-oss 的思考。** 實測平均仍產生 220 tokens，比 `think="low"` 的 115 還多。要壓低思考量，只能用 `"low"`。
- **Router 在不同 `think` 等級的表現**（`spikes/think_level_probe.py`；12 個標好答案的問題、各跑一次）：
  - `low`：11/12 正確，平均 0.9s，平均產生 115 tokens（最多 185）。
  - `medium`：11/12 正確，平均 1.1s，平均 172 tokens。
  - `high`：12/12 正確，平均 1.9s（最慢 5.6s），平均 394 tokens（最多 1,349）。

  各等級只差 1 題，在雜訊範圍內。`high` 的思考量起伏很大，即使是簡單任務也可能用到上千 tokens。
- **產生回答時，各 `think` 等級實際思考多少**（`spikes/answer_think_probe.py`，每個等級跑 2 次；完整輸出在 `spikes/out/`）：
  - **Q2 規模**（prompt 約 5.3K tokens，輸出額度約 4.4K）：`low` 思考約 8 tokens；`medium` 約 440；`high` 用了 3,500～4,400，結果一次回答全空，另一次回答被截斷、漏掉成本數據。**在 10K 限制下，`high` 處理不了 Q2 規模的 prompt。**
  - **Q3 規模**（prompt 約 1.8K tokens）：`high` 思考約 1,200～1,300 tokens，能完成回答。
  - **品質：** `high` 提到 `-Origin` 改善比較穩定，但沒有任何等級穩定指出 Mix 資料集上 `-Low` 勝過完整版。`low` 有一次把 NaiveRAG / variant 的勝率誤讀成「勝 / 負」，還說完整版各方面最好，這跟表格不符。Q3 的主要問題是表格讀錯，靠調高思考等級解決不了。
- **gpt-oss 輸出的連字號常是 U+2011（不斷行連字號）**，例如 `‑High`。用字串比對檢查 Golden Facts 之前，要先把各種連字號統一成 `-`。
- **Token 估算偏差：** 估算值（tiktoken 計數 + 300）比模型回報的 `prompt_eval_count` 多 225，代表實際的模板開銷約 75 tokens。保留 300 的安全邊際是偏保守、安全的做法。
- **對話模板有額外開銷。** 一句話的 prompt，模型回報 `prompt_eval_count=76`。Budget guard 要把模板開銷算進去；Trace 同時記錄我們的估算值和模型回報的 `prompt_eval_count`，兩者可以互相核對。
- **測試文件規模：** LightRAG 論文共 16 頁、13,610 tokens；References 之前的正文約 10.4K tokens。
- **章節標題：** LightRAG 論文的章節標題是 12pt `NimbusRomNo9L-Regu`，編號和標題分在兩行（`3` / `THE LIGHTRAG ARCHITECTURE`），所以用正則抓不到。這只是這份模板的特徵，**程式不能寫死字體大小**，做法如下：
  - 出現最多的字體大小視為內文；比內文大或是粗體的行，才當作標題。
  - 完全偵測不到標題時，用固定長度切出虛擬 Section。
  - 句子切分同時支援中文（。！？）和英文的標點。
- **表格：** `page.find_tables()` 抓不到 Table 1 和 Table 2（無框線表格）。`get_text()` 會依閱讀順序一格一行輸出，數字完整但結構遺失。做法是用文字座標重建列與欄，不另做 LLM 重排備援；重建失敗時的處理見切塊規則第 4 條。p9 的成本表抽出來會夾帶數學斜體留下的 `_`，需要清掉。
- **Embedding bake-off**（`spikes/embedding_bakeoff.py`；12 個中英文問題、52 個粗切 chunk，指標為 MRR）：
  - `bge-m3` 0.708
  - bge-m3 + BM25 等權 RRF 0.658
  - `embeddinggemma:300m` 0.583
  - `qwen3-embedding:0.6b` 0.558
  - 純 BM25 0.408（中文問題幾乎都檢索失敗）

  `embeddinggemma-2` 需要比 0.21.1 更新的 Ollama，所以沒有測。

## 驗收：Golden Facts

測試分成兩層：

- **非雲端回歸**（`pytest tests eval`，排除 live eval；其中整合測試使用本地 bge-m3。預設 `pytest` 僅跑不需 Ollama 的 unit）：
  - Table 2 重建後，每一格的數字都正確。
  - 沒有 Chunk 跨越 Section；References 不在索引裡。
  - Budget guard 超過額度一定會 raise。
  - Q3 的前 5 名一定有 Table 2；Q2 的 Sub-queries 一定找得到成本和增量更新的段落。
- **回答評估**（`pytest -m eval`，會呼叫 LLM，需要時手動跑）：每條 Golden Fact 都標明用哪種方式檢查。
  - **`contains`**：只用來檢查某個專有名詞有沒有出現，例如 `-Origin`。先統一連字號、空格和百分比的寫法，再做字串比對。**不能用來檢查數字**，因為同一個數字可能在表格中出現好幾次。例如 `64.8` 在 Table 2 出現 3 次，只比對字串會把寫錯變體的回答也算成答對。
  - **`judge`**：用於語意上的涵蓋，以及帶有前後文的數字。由 LLM 判斷（`think=low`），但它必須從回答中逐字摘錄證據句；這句話不在回答裡，就判定失敗，這樣可以避免評分的 LLM 憑空捏造。檢查數字時，證據句必須同時對上變體、資料集、指標、數值和比較方向。
  - **反向檢查（`forbidden`）**：列出不該出現的錯誤結論，由 judge 檢查。只有 judge 從回答中摘錄出明確斷言這個錯誤結論的說法時，才判定失敗；否定或引用該錯誤說法不算。
  - 每次跑完，把報告寫到 `eval/reports/`，內容包含每條 fact 是否通過、每次呼叫的 token 用量和延遲。預設每題跑 1 次，可以用參數改成跑 3 次，看通過率。
  - 交付的驗收報告每題跑 3 次，列出每條 fact 的通過率與失敗原因；forbidden 類錯誤結論列為已知缺陷，不阻擋交付。品質調整有時間上限，到時就照實報告當下結果。

以下是驗收意圖摘要；完整案例與實際檢查定義以 [golden_facts.py](../eval/golden_facts.py)、[second_document.py](../eval/second_document.py) 為準。設計要求不等同於全部已通過；原始通過率及已知判定限制見 [評估結論](../eval/reports/issue11-correction/conclusions.md)。

- **Q1** 摘要要涵蓋：問題動機、graph-based indexing、dual-level retrieval、增量更新、實驗設定與結果、結論。
- **Q2** 比較要涵蓋：檢索方式（GraphRAG 用 community 遍歷，LightRAG 用 dual-level keyword）、成本（GraphRAG 檢索約 610×1,000 tokens，LightRAG < 100 tokens 且只需 1 次 API call）、增量更新（GraphRAG 要重建 community）、Table 1 的勝率、Table 3 的 case study。
  - 不得出現「LightRAG 在所有資料集都勝過 GraphRAG」。Table 1 中，Mix 資料集的 Overall 是 GraphRAG 50.4%、LightRAG 49.6%。
- **Q3** 要正確引用 Table 2（各變體對 NaiveRAG 的勝率），並點出兩個反直覺結果：
  - Mix 資料集上，`-Low` 的 Overall 是 64.8%，高於完整版 LightRAG 的 60.0%。
  - Agriculture 資料集上，`-Origin` 是 74.4%，高於完整版的 67.6%。
  - 不得出現「完整版 LightRAG 在所有資料集、所有指標都最好」。實測時，`low` 真的這樣回答過。

- **文件裡沒有答案的問題：** 準備 3 題，例如「LightRAG 在 HotpotQA 上的分數」「LightRAG 的授權條款」。預期系統回答固定的「文件中未提及」，而且不補上任何編造的內容。

- **第二份測試文件：** 已選定工業機器人綜述（arXiv 2603.06749v1，109 頁）。原選件條件如下：
  - 2026 年發表的 arXiv 論文，晚於原始 gpt-oss 發布；託管模型的權重與訓練來源不透明，不能保證未見過此文。
  - 雙欄排版，模板和 LightRAG 不同。
  - 含附錄 40 頁以上，Section Summary 加起來要超過 6,000 tokens，才會觸發 Group Summary。
  - 主題不是 RAG。

  數字題與摘要題已定義於 `eval/second_document.py`。中文 PDF 是額外泛化測試方向，用來測中文斷句。
