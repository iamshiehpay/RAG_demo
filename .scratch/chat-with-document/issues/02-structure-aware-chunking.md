# #02 依結構解析與切塊：Section、References、附錄、掃描檔

Status: done

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

把 #01 用的「每頁一個虛擬 Section」，換成真正的 Section，並照 AGENTS.md 的切塊規則切塊。

- **章節標題：** 用字體大小的相對關係判斷。出現最多的字體大小視為內文，比內文大或是粗體的行才是標題；編號和標題分在兩行時要合併。完全偵測不到標題時，退回用固定長度切出的虛擬 Section。
- 移除 References；附錄保留，並標示為 Appendix。
- **切塊：**
  - Chunk 不跨越 Section。
  - 把整段段落裝進 Chunk，裝到約 500 tokens 就換下一塊（這個數字可以設定）。
  - 只有單一段落過長時，才在句子邊界切開，並重疊約 10%。句子邊界同時支援中文和英文的標點。
  - 每個 Chunk 前面加上 Section 標題。
- **掃描檔：** 抽不出文字層的 PDF，上傳時就發出錯誤，介面顯示原因。
- **Citation 旁註：** 顯示「頁碼 + Section 標題」。

**介面的部分：** 如果 #09 已經合併，就使用它提供的共用元件；如果還沒合併，先用最簡單的樣式，等合併時再換成共用元件。

## Acceptance criteria

- [x] 處理 LightRAG 論文時，偵測得到全部主章節（Introduction 到 Conclusion，以及 Appendix）。
- [x] 任何 Chunk 都不含 References 的內容；附錄的 Chunk 都標示為 Appendix。
- [x] 確定性測試：沒有 Chunk 跨越 Section；除了單一長段落之外，每個 Chunk 都不超過設定的大小。
- [x] 確定性測試：在測試中產生一份只有圖片、沒有文字層的 PDF，上傳時會收到錯誤事件。
- [x] 確定性測試：在測試中產生一份完全沒有標題的 PDF，系統用虛擬 Section 照常處理，並且可以提問。
- [x] Citation 的旁註顯示頁碼和 Section 標題。

## Blocked by

- #01（`01-walking-skeleton.md`）

## Verification

- Final source e59e096 integrated after independent Opus5.5 medium APPROVE; report `docs/verification/ticket-02/takeover-independent-review.md`.
- Independent GPT6.1 medium QA on integrated e59e096: all six AC PASS, 213 tests PASS, 24 independent PDF scenarios plus two typography/packing probes, actual browser/error/citation/cache checks PASS. Evidence: `docs/verification/ticket-02/qa/takeover-report.md`. Main inspected report, environment, source ancestry and cross-page screenshot.
- Source panel heading page-range display remains assigned to #09; full source metadata/text and Citation side-note ranges passed.
