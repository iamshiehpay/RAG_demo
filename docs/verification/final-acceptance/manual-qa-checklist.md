# 最終驗收：人工 QA 清單

依 D09，交付前的最終驗收改由使用者親自操作網站，取代 Codex 的 QA。在 #11 合併後的 `main` 上執行，約 20～30 分鐘。

每一步在「結果」欄填 ✅、❌ 或「已知缺陷」。出現 ❌ 時寫一句看到什麼，或附截圖，交給 levi 判斷嚴重程度。

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
| A1 | 上傳 `data/lightrag.pdf` | 依序顯示解析 → 切塊 → embedding n/N → 摘要 n/N → 完成，約 30～60 秒；完成後出現「文件概覽」；完成前提問框不能用。若 `.cache/` 已有這份文件，會直接跳到完成，看不到中間階段，這也算通過 | |
| A2 | 問 `Summary this document.` | 回答涵蓋：問題動機、graph-based indexing、dual-level retrieval、增量更新、實驗設定與結果、結論；附 `[S#]` | |
| A3 | 點一個 `[S#]` | 顯示該 Section 的頁碼範圍和摘要內容 | |
| A4 | 問 `Compare LightRAG with GraphRAG.` | 提到檢索方式（community 對 dual-level keyword）、成本（GraphRAG 約 610×1,000 tokens，LightRAG < 100 tokens、1 次 API call）、增量更新（GraphRAG 要重建 community）、Table 1 勝率 | |
| A5 | 檢查 A4 有沒有寫錯 | **不能**說「LightRAG 在所有資料集都勝過 GraphRAG」（Mix 資料集的 Overall 是 GraphRAG 50.4%、LightRAG 49.6%） | |
| A6 | 問 `Performance of ablated versions of LightRAG.`，點引用 Table 2 的 `[C#]` | 原文以表格呈現；回答先說明比較基準（每格是對 NaiveRAG 的勝率） | |
| A7 | 檢查 A6 的兩個反直覺結果 | Mix 資料集 `-Low` 64.8% > 完整版 60.0%；Agriculture 資料集 `-Origin` 74.4% > 67.6%。**不能**說「完整版在所有資料集、所有指標都最好」 | |
| A8 | 接著問 `那成本呢？` | 用繁體中文回答 LightRAG 和 GraphRAG 的成本差異；展開 Trace，Standalone Question 是一句完整的問題 | |
| A9 | 問 `這篇論文有什麼限制？` | 繁體中文、附 Citation，內容來自論文 | |
| A10 | 問 `LightRAG 在 HotpotQA 上的分數是多少？` | 只回固定句「文件中未提及」，沒有補任何編造的內容 | |
| A11 | 問 `What are LightRAG's license terms?` | 只回「Not mentioned in the document.」 | |
| A12 | 展開任一回答的 Trace | 看得到問題類型、檢索到的 Chunk 與相似度；每次 LLM 呼叫的長條都 ≤ 10K；模型的思考內容預設收合 | |

## B. 錯誤處理（約 2 分鐘）

| # | 操作 | 通過的樣子 | 結果 |
|---|---|---|---|
| B1 | 上傳任意一個非 PDF 檔（例如 `.txt` 或 `.png`） | 顯示「不是有效的 PDF」這類錯誤；原本的文件和對話都還在 | |
| B2 | 重新上傳 `data/lightrag.pdf` | 幾乎立刻完成（取用快取），對話被清空，可以提問 | |

## C. 第二份文件（泛化）

處理約 100 次 LLM 呼叫，第一次上傳可能要好幾分鐘；有快取的話會立刻完成。

| # | 操作 | 通過的樣子 | 結果 |
|---|---|---|---|
| C1 | 上傳 `data/industrial-robotics.pdf` | 完成，出現「文件概覽」 | |
| C2 | 問 `How many model papers were manually annotated for expert validation? In that comparison, how does InfoFound affect overall accuracy and positive-class F1 relative to All? Include the evaluation counts for both settings.` | 3 篇論文；All：N=447 個 criterion-paper evaluations（不是論文篇數）、Accuracy 0.966；InfoFound：N=304、Accuracy 0.951；兩者的 F1 都是 0.762（InfoFound 的準確率較低，F1 不變） | |
| C3 | 點 C2 引用 Table 9 的 `[C#]` | 原文是 p.31 的 Table 9，數字和回答一致 | |
| C4 | 問 `Summarize this document in three sentences.` | 剛好三句、附 `[S#]`；Trace 顯示用的是 Group 層摘要 | |

## 已知缺陷（看到時填「已知缺陷／FAIL」，照實記錄，不改成通過）

- 全文摘要（A2、C4）偶爾會漏掉某一項內容。
- D10 A 核准保留：第二份文件447/304筆評估被誤稱論文篇數；時間細節引用到只支持部分敘述的相鄰片段；最後推導結論未附自己的Citation。數字或來源ID正確不代表整句有根據。
- Q2成本／增量更新、Q3變體比較、中文與全文摘要仍可能遺漏或寫錯；依D05照實記錄。
- Global的通用Table Chunk提示存在未觀察回歸的措辭風險，詳見限定複審。
- 某些字型組合下，標題會掛錯 Section。

## 結論

- 執行者：
- 時間：
- `main` commit：
- ❌ 的項目與處理方式：
