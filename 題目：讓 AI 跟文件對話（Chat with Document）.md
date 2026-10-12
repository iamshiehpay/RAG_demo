# 題目：讓 AI 跟文件對話（Chat with Document）

Oct 12, 2026 · @Thank Family

## 任務概述

做一個可在本機執行的網站，提供聊天介面：使用者上傳一份文件後，可以針對文件內容提問，LLM 只根據系統從文件中提供的資料回答。

整個專案要以 **AI Native** 方式開發，也就是以 Claude Code、Antigravity、Codex 等 AI 編程工具為主要開發方式。開發過程本身也是評分重點。

## 技術限制

| # | 限制 | 意義 |
| --- | --- | --- |
| 1 | 不能使用現成的 GPT / Gemini API 解析文件，LLM 只做 text-to-text | 不能把 PDF 直接丟給 LLM API 的檔案上傳或多模態功能。文件解析（PDF → 文字）、切塊、檢索都要自己實作，LLM 只接收純文字 prompt、回傳純文字 |
| 2 | 假設 LLM 最大 context size 為 10K tokens | 整份文件不能一次塞進 prompt。必須設計分段處理、檢索或階層式摘要機制，每次呼叫的輸入加輸出都要控制在 10K 以內 |

## 測試文件

預設文件為 [arXiv 2410.05779](https://arxiv.org/pdf/2410.05779)，即論文 **LightRAG: Simple and Fast Retrieval-Augmented Generation**（HKU，2024）。內容包含方法說明、與 GraphRAG 等 baseline 的比較實驗，以及消融實驗（ablation study）表格。完整論文的 token 數明顯超過 10K。

## 功能需求與驗收問題

核心功能：網頁聊天介面、文件上傳、根據上傳文件內容回答問題（RAG）。

系統必須能回答以下三個問題：

| 問題 | 內容 | 考驗的能力 |
| --- | --- | --- |
| Q1 | Summary this document. | 全文摘要：需涵蓋整份文件，無法只靠檢索少數片段 |
| Q2 | Compare LightRAG with GraphRAG. | 跨段落比較：相關內容散布在方法、實驗、討論等多個章節 |
| Q3 | Performance of ablated versions of LightRAG. | 精準檢索：需找到消融實驗章節與表格，並正確解讀數據 |

## 必須說明的設計問題

1. 文件 token 數超過 LLM max context size 時，你怎麼處理？
2. 你怎麼處理 summary？

## 交付內容

1. **程式碼**：壓縮成 zip 寄到指定 email，或提供可存取的連結（例如 GitHub repo）。
2. **簡報（PPT）**，需包含：
   - 專案架構與成果（Describe project architecture and result）
   - 如何與 AI 協作完成作業（How did you cowork with AI）
   - 與 AI 協作的心得與洞察（What's your learn/insight when cowork with AI）
3. **Demo**：另約時間線上 demo，在本機執行即可，不需要部署。

## 解讀與待討論事項

以下是題目沒有明講、但會影響實作方向的地方。

- **「不能用 API 解析文件」的範圍**：解讀為可以呼叫 LLM API 做文字生成，但 PDF 轉文字要用自己的程式處理（例如 PyMuPDF、pdfplumber）。需確認是否也禁止使用 LLM 廠商的 embedding API。
- **10K 限制要真的執行**：在程式裡實際計算 token 並強制截斷或分批，而不只是口頭聲稱。Demo 時能展示這一點會加分。
- **三個問題適合不同策略**：Q1 適合 map-reduce 或階層式摘要，Q2、Q3 適合檢索。系統可能需要判斷問題類型（query routing）。
- **表格處理**：Q3 的答案主要在消融實驗表格裡，PDF 表格的擷取品質直接影響答案準確度。
- **簡報有三分之二在講 AI 協作**：從現在開始記錄與 AI 工具的互動，例如關鍵 prompt、AI 做錯的地方、如何修正，作為簡報素材。
