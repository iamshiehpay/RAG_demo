# Chat with Document

讓使用者對一份上傳的文件提問，系統只根據文件內容回答。

## 文件結構

**Document**：
使用者上傳的一份 PDF。系統一次只針對一份 Document 對話。
_Avoid_：file、paper（paper 只用來指測試用的 LightRAG 論文）

**Section**：
Document 依自身標題切出的章節，是摘要和切塊的邊界單位。完全偵測不到標題時，用固定長度切出的虛擬 Section 代替。
_Avoid_：part、segment

**Chunk**：
檢索的最小單位，屬於某個 Section，並帶有頁碼。
_Avoid_：passage、node、segment

**Table Chunk**：
由一張表格重建而成的 Chunk，包含 caption 和寫明數字意義的表頭，不跟內文混在一起切。它和內文中提到這張表的段落互相連結。結構無法可靠重建時，保留原始文字，並標記為「結構未能可靠重建」。

## 摘要

**Section Summary**：
一個 Section 的摘要，要保留其中的數字和具體結論。

**Group Summary**：
把相鄰的幾個 Section Summary 合併成的摘要。只有長文件需要，用來讓 Summary Tree 的某一層放得進 Context Budget。

**Document Summary**：
Summary Tree 的最頂層，是全文摘要。上傳完成後，會在介面上顯示為文件概覽。

**Summary Tree**：
由 Section Summary 往上合併而成的階層：Section Summary → Group Summary（視需要，可以有多層）→ Document Summary。
_Avoid_：summary index、RAPTOR tree

## 問答

**Question Type**：
決定一個問題要走哪條回答路徑的分類，只有三種：Global（需要全文）、Synthesis（需要彙整多個 Section，比較題是其中一種）、Lookup（從單一處就能回答的事實、數字或表格）。
_Avoid_：intent、route、Comparison（範圍太窄，「有什麼限制」這類問題不是比較，卻同樣需要跨 Section）

**Standalone Question**：
把追問依對話歷史改寫成的完整問題，不看前文也能理解；後續的檢索和回答都以它為準。
_Avoid_：rewritten query、condensed question

**Sub-query**：
Synthesis 問題拆出來的子問題，每個各自檢索。
_Avoid_：sub-question、facet

**Context Budget**：
單次 LLM 呼叫可用的 10,000 tokens，涵蓋 prompt、思考過程和回答。
_Avoid_：context window（指模型本身的上限，比 Context Budget 大）

**Citation**：
回答中指向來源的引用，來源可以是 Chunk 或 Section Summary，會標示 Section 與頁碼。引用了不存在的編號時，移除該編號，並把那句話標記為 Unverified；沒有附 Citation 的句子不標記（使用者決策，2026-10-12）。
_Avoid_：reference（會跟論文的 References 章節混淆）

**Trace**：
一次回答的處理紀錄，內容包括 Question Type、取回的 Chunk，以及每次 LLM 呼叫的 token 用量。

**Golden Facts**：
驗收問題的標準答案檢查點，用來判斷一個回答是否正確且完整。分成兩種：必須出現的事實，以及不得出現的錯誤結論（forbidden claim）。
