# 最終驗收：人工 QA 清單

依 D09，交付前的最終驗收改由使用者親自操作網站，取代 Codex 的 QA。在 #11 合併後的 `main` 上執行，約 20～30 分鐘。

每一步在「結果」欄填 ✅、❌ 或「已知缺陷」。出現 ❌ 時寫一句看到什麼，或附截圖，交給 levi 判斷嚴重程度。

## 目前可驗收版本

程式驗證基準：`db64d844a58ee854f855848c90dd599e69b8a34c`（已審 source `f089cae`）。主工作區327項測試通過、3項雲端eval未選入、沒有跳過測試；兩份最新快取已移交，公開上傳確認0 LLM／0 embedding呼叫。後續文件提交不改程式；詳見[整合證據](../ticket-11/integration.md)。

使用者已回報原版人工QA結果：消融題找到正確表格並明確接受簡短回答，其餘操作正常；A9限制題已補充「回答找不到文件」，正區分文件狀態／API錯誤與語意拒答。D10已知缺陷與raw評分保留；D11/D12改版另由#12處理，目前網站仍是原版。目前 [8101網站](http://127.0.0.1:8101) 已開啟，HTTP首頁／JS／CSS／本地字型均200；這只是可用性檢查，不代替人工QA。可直接從A1開始，無須再次啟動伺服器。

## 0. 準備（約 2 分鐘）

```sh
cd /Users/shiehpay/Desktop/resume/rag
git log --oneline -1          # 確認是 #11 合併後的 commit
bash scripts/fetch_data.sh    # 下載兩份測試 PDF（已存在就只做核對）
uv run uvicorn chat_document.api:create_app --factory --host 127.0.0.1 --port 8101
```

用瀏覽器打開 http://127.0.0.1:8101 。終端機不要關，伺服器會一直在前景執行。

## A. LightRAG 論文（主要驗收）

| # | 操作 | 通過的樣子 | 結果 |
|---|---|---|---|
| A1 | 上傳 `data/lightrag.pdf` | 依序顯示解析 → 切塊 → embedding n/N → 摘要 n/N → 完成，約 30～60 秒；完成後出現「文件概覽」；完成前提問框不能用。若 `.cache/` 已有這份文件，會直接跳到完成，看不到中間階段，這也算通過 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A2 | 問 `Summary this document.` | 回答涵蓋：問題動機、graph-based indexing、dual-level retrieval、增量更新、實驗設定與結果、結論；附 `[S#]` | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A3 | 點一個 `[S#]` | 顯示該 Section 的頁碼範圍和摘要內容 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A4 | 問 `Compare LightRAG with GraphRAG.` | 提到檢索方式（community 對 dual-level keyword）、成本（GraphRAG 約 610×1,000 tokens，LightRAG < 100 tokens、1 次 API call）、增量更新（GraphRAG 要重建 community）、Table 1 勝率 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A5 | 檢查 A4 有沒有寫錯 | **不能**說「LightRAG 在所有資料集都勝過 GraphRAG」（Mix 資料集的 Overall 是 GraphRAG 50.4%、LightRAG 49.6%） | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A6 | 問 `Performance of ablated versions of LightRAG.`，點引用 Table 2 的 `[C#]` | 原文以表格呈現；回答先說明比較基準（每格是對 NaiveRAG 的勝率） | ✅ 使用者確認找到正確table；回答較短，以表格為主 |
| A7 | 檢查 A6 的兩個反直覺結果 | Mix 資料集 `-Low` 64.8% > 完整版 60.0%；Agriculture 資料集 `-Origin` 74.4% > 67.6%。**不能**說「完整版在所有資料集、所有指標都最好」 | 使用者明確接受簡短表格結果；不宣稱完整比較通過，原N3品質FAIL保留 |
| A8 | 接著問 `那成本呢？` | 用繁體中文回答 LightRAG 和 GraphRAG 的成本差異；展開 Trace，Standalone Question 是一句完整的問題 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A9 | 問 `這篇論文有什麼限制？` | 繁體中文、附 Citation，內容來自論文 | ❌ 精確回答「文件中未提及」，但p.8 §4.3有原文雜訊的限制證據；原因未證實。獨立重跑另見系統警告誤歸因，見下方診斷 |
| A10 | 問 `LightRAG 在 HotpotQA 上的分數是多少？` | 只回固定句「文件中未提及」，沒有補任何編造的內容 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A11 | 問 `What are LightRAG's license terms?` | 只回「Not mentioned in the document.」 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| A12 | 展開任一回答的 Trace | 看得到問題類型、檢索到的 Chunk 與相似度；每次 LLM 呼叫的長條都 ≤ 10K；模型的思考內容預設收合 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |

## B. 錯誤處理（約 2 分鐘）

| # | 操作 | 通過的樣子 | 結果 |
|---|---|---|---|
| B1 | 上傳任意一個非 PDF 檔（例如 `.txt` 或 `.png`） | 顯示「不是有效的 PDF」這類錯誤；原本的文件和對話都還在 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| B2 | 重新上傳 `data/lightrag.pdf` | 幾乎立刻完成（取用快取），對話被清空，可以提問 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |

## C. 第二份文件（泛化）

處理約 100 次 LLM 呼叫，第一次上傳可能要好幾分鐘；有快取的話會立刻完成。

| # | 操作 | 通過的樣子 | 結果 |
|---|---|---|---|
| C1 | 上傳 `data/industrial-robotics.pdf` | 完成，出現「文件概覽」 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| C2 | 問 `How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.` | 3 篇論文；All：N=447 個 criterion-paper evaluations（不是論文篇數）、Accuracy 0.966；InfoFound：N=304、Accuracy 0.951；兩者的 F1 都是 0.762（InfoFound 的準確率較低，F1 不變） | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| C3 | 點 C2 引用 Table 9 的 `[C#]` | 原文是 p.31 的 Table 9，數字和回答一致 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |
| C4 | 問 `Summarize this document in three sentences.` | 剛好三句、附 `[S#]`；Trace 顯示用的是 Group 層摘要 | ✅ 使用者回報其餘測試正常；未提供逐项截圖 |

## 已知缺陷（看到時填「已知缺陷／FAIL」，照實記錄，不改成通過）

- 全文摘要（A2、C4）偶爾會漏掉某一項內容。
- D10 A 核准保留：第二份文件447/304筆評估被誤稱論文篇數；時間細節引用到只支持部分敘述的相鄰片段；最後推導結論未附自己的Citation。數字或來源ID正確不代表整句有根據。
- Q2成本／增量更新、Q3變體比較、中文與全文摘要仍可能遺漏或寫錯；依D05照實記錄。
- Global的通用Table Chunk提示存在未觀察回歸的措辭風險，詳見限定複審。
- 某些字型組合下，標題會掛錯 Section。

## 結論

- 執行者：使用者（原版人工操作回饋）
- 時間：2026-10-13 22:10、22:15 Asia/Taipei
- `main` commit：db64d84程式基準；後續b956247只補文件與驗證紀錄
- ❌ 的項目與處理方式：A9已補充「回答找不到文件」；先分類並做有界診斷，不調整已接受的Q3回答、不改判所有項目PASS。

## 使用者原始回饋與判定邊界

2026-10-13 22:10：「這篇論文有什麼限制？」回答不出來；「Performance of ablated versions of LightRAG.」雖然回答比較短，只有貼回表格，但有找到正確的table；「其他都測試正常」。22:15補充：「Performance of ablated versions of LightRAG.」雖然回答比較短，只有貼回表格，但有找到正確的table，「但這樣應該可以」。

Main直接核對nativeCodex原使用者訊息 `msg_01a13599-b59c-7e21-a9da-c4de08d06a64`（14:10:28Z）與 `msg_01a1359e-856b-77f1-a32c-73f474946366`（14:15:43Z）。結果表是使用者整體回報，不虛構逐項影片／截圖，也不覆寫既有Golden Facts分數。A9目前唯一回報失敗，後續症狀補充與診斷記於下方；未核准擴大品質調參。#12合併後仍須驗受影響的新介面。

2026-10-13 22:46 補充原文：「"這篇論文有什麼限制？" 回答找不到文件
- 消融題 你覺得要改嗎？」（native msg_01a135ba-717a-76a0-95cf-27bed7e974a6）。這不是精確固定拒答的確認；區分文件狀態／API錯誤與語意拒答前不歸因。消融題維持先前接受的結果。

2026-10-13 22:54 精確補充：回答為「文件中未提及」。Trace 為 Synthesis、plan_source=router，Standalone Question「這篇論文的限制是什麼？」；9段來源涵蓋§4.1、§4.3、§4.4、§5.1與Appendix；invalid citations=0、budget dropped=0、最高相似度0.4857。Main直接核對診斷session01a135bc的真人回答msg_01a135c1-b8ce-76d3-87d6-5bc469f06ac7（request_user_input_async call_a72b01fa50fb43cc9d434fb33289e520），可排除這次是文件未載入／來源404的症狀；拒答是否適當仍需原文核對。

有界診斷結論：[A9報告](../ticket-11/manual-a9/report.md)。原拒答FAIL、來源支持存在（p.8 §4.3），檢索漏段或模型解讀的原因UNPROVEN。一次獨立無歷史重跑未重現拒答，另出現把系統重建警告當成論文限制的grounding FAIL；兩者分開記錄，D14待真人決定處置，不調整已接受的消融題。

## D. #12 三欄介面改版（整合後複驗）

基準：af6b9f3 的已審前端（後續Main文件checkpoint不改程式）。舊版A/B/C結果保留；本表只記新介面受影響流程。Main完整測試通過後再通知可驗收版本。A9後端修正另屬#13，不能把介面通過當成A9已修好。

| # | 來源／操作 | 預期可見結果 | 結果 |
|---|---|---|---|
| D1 | D11三欄；重新整理8101、上傳LightRAG、收合左右欄 | 文件／對話／來源三欄；收合後中欄變寬，輸入框固定在底部，對話可獨立捲動 | NOT_EXECUTED |
| D2 | D11 Citation；問比較題，點句內C引用 | 右欄自動顯示對應原文；長表格可左右捲動，數字不拆行，也不把整頁撐寬 | NOT_EXECUTED |
| D3 | AnswerProcess；展開「回答過程」 | 問題理解、每一步模型／思考量／送入＋預留／時間、找到的段落三段清楚；技術細節預設收合，模型名保留原文 | NOT_EXECUTED |
| D4 | Global路徑；問全文摘要，點S引用 | 來源欄顯示摘要及Section頁碼；回答過程標示實際摘要層，不捏造檢索步驟 | NOT_EXECUTED |
| D5 | Composer；實際中文輸入法選字按Enter、Shift+Enter與送出 | 組字選字不誤送出；Shift+Enter換行；完成組字後Enter可送出；串流保留暫定狀態 | NOT_EXECUTED |
| D6 | 窄螢幕；縮窄瀏覽器，交替開文件／來源，按Escape，再拉寬 | 側欄不互相遮蓋；能關閉回對話；跨寬度不遺留遮罩，整頁無橫向溢出 | NOT_EXECUTED |
| D7 | DocumentPane失敗與重置；選非PDF，再換回PDF | 錯誤清楚且原文件／對話保留；成功換文件才清空對話，檔案按鈕中文 | NOT_EXECUTED |

少見串流重試／拒絕、404、未驗證、抽取分批、safe Markdown由已審劇本與原回歸支援，證據見[review.md](../ticket-12/review.md)；此處不宣稱使用者已親手觸發。
