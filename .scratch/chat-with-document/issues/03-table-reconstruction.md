# #03 表格重建與 Lookup 品質（Q3）

Status: ready-for-agent

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

- [ ] 確定性測試：Table 1 和 Table 2 重建後，每一格的數字都和論文一致。
- [ ] 確定性測試：p9 的成本表裡沒有 `_` 雜訊。
- [ ] 確定性測試：問 Q3 時，假 LLM 記錄到的回答 prompt 裡，同時有 Table 2，以及 §4.3 中討論它的段落。
- [ ] 確定性測試：重建失敗的表格會保留原始文字並帶有標記；介面引用它時會顯示限制的提示。
- [ ] 確定性測試：在測試中產生一張超過 2,000 tokens 的表格，它會被依列分段，而且每段都有表頭。
- [ ] 如果 #08 已經合併：Q3 的 Golden Facts（包括 forbidden claim）寫進 eval 報告。

## Blocked by

- #02（`02-structure-aware-chunking.md`）
