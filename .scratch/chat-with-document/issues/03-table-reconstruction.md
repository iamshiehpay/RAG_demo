# #03 表格重建與 Lookup 品質（Q3）

Status: done

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

讓 Q3 這類查表格的問題能正確回答。

- **重建表格：** 用文字座標把無框線的表格重建成 Table Chunk。內容包含 caption、多層的欄標題和列標題，讓每個數字的意義都看得出來。例如 Table 2 的每一格，都要能對應到「資料集 × NaiveRAG / 變體」。
- **重建失敗時：** 保留原始文字，並標記為「結構未能可靠重建」。回答引用它時必須說明這個限制，介面也要顯示提示。
- **清除雜訊：** 去掉數學斜體留下的 `_` 等字元，例如 p9 的成本表。
- **互相連結：** Table Chunk 和內文中提到「Table N」的段落互相連結。Lookup 檢索時，照規則帶出這些連結的段落，以及相鄰的 Chunk。
- **大表格：** 超過 2,000 tokens 的表格依列分段，每段都重複表頭。
- **回答的 prompt 規則：** 引用表格時，先說明比較基準，再下結論。
- **介面：** Citation 的彈出視窗以表格形式顯示 Table Chunk。

**介面的部分：** 如果 #09 已經合併，就使用它提供的共用元件；如果還沒合併，先用最簡單的樣式，等合併時再換成共用元件。

## Acceptance criteria

- [x] 確定性測試：Table 1 和 Table 2 重建後，每一格的數字都和論文一致。
- [x] 確定性測試：p9 的成本表裡沒有 `_` 雜訊。
- [x] 確定性測試：問 Q3 時，假 LLM 記錄到的回答 prompt 裡，同時有 Table 2，以及 §4.3 中討論它的段落。
- [x] 確定性測試：重建失敗的表格會保留原始文字並帶有標記；介面引用它時會顯示限制的提示。
- [x] 確定性測試：在測試中產生一張超過 2,000 tokens 的表格，它會被依列分段，而且每段都有表頭。
- [x] 如果 #08 已經合併：Q3 的 Golden Facts（包括 forbidden claim）寫進 eval 報告。

## Blocked by

- #02（`02-structure-aware-chunking.md`）

## Verification

- Final5d6204c integrated; independent Opus5.5 medium Review APPROVE including #02 rebase conflicts, numeric/Section preservation and adversarial layouts. Evidence `docs/verification/ticket-03/takeover-independent-review.md`.
- Independent GPT6.1 medium integrated QA: AC1–5 PASS, AC6 honest reporting PASS;238 deterministic tests,256 labelled PDF numeric values,421 numeric-token preservation,10 independent layouts and actual table/uncertain-source browser PASS. Report `docs/verification/ticket-03/qa/takeover-report.md`.
- Fresh real Q3 N=3 remains FAIL (both numerical exceptions0/3; forbidden pass2/3), recorded at `docs/verification/ticket-03/qa/takeover-q3-live-n3.md`. This ticket requires reporting; #11 still requires Golden Facts to pass and is not waived.
