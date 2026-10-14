# 前端設計

現行介面以紙張底色、襯線中文字與可查閱的原文呈現文件問答。內文約 16px；使用本地 Noto Serif TC 字型，不加入裝飾動畫。

- 左欄：上傳／替換 Document、處理進度、Chunk 數與文件概覽。
- 中欄：對話、句中 Citation、小螢幕可橫向捲動的 Markdown 表格；輸入框固定於下方。
- 右欄：點擊 Citation 後的原文／摘要與頁碼；兩側欄可收合，窄版改以 overlay 開啟。
- 「回答過程」先呈現問題理解、模型 token 用量和檢索片段；原始計數及思考文字放在預設收合的技術細節。
- token 長條以 10,000 為滿格，同時區分 prompt 與輸出預留。
- Enter 送出、Shift+Enter 換行；輸入法組字期間 Enter 不送出。
- 串流內容先標暫定；重新產生時取代舊文字，成功才定稿。

| `frontend/src/` 檔案 | 功能 |
|---|---|
| `main.tsx`、`App.tsx` | React 入口、版面與互動狀態 |
| `DocumentPane.tsx`、`Composer.tsx`、`Shortcuts.tsx` | 文件操作、輸入與範例問題 |
| `Answer.tsx`、`SourcePane.tsx`、`SourceContent.tsx` | 回答 Markdown、Citation 與來源表格 |
| `AnswerProcess.tsx` | 階段、檢索與 token Trace |
| `sse.ts`、`events.ts`、`models.ts` | SSE 解析、生成的事件型別及前端模型 |
| `Shared.tsx`、`styles.css`、`fonts/` | 共用元件、樣式與單一 Regular 字型／授權 |

前端的模型名稱是顯示常數，修改後端模型時需同步。build 與事件核對命令見 [開發指南](development.md#前端開發)。歷史設計稿與瀏覽器驗證保存於 [歸檔標籤](history.md)，不將過時的 modal／margin-note 決策列為現行規則。

## 本地字型

只保留 `frontend/src/fonts/` 的 Regular WOFF2、CSS 與 OFL 授權；`frontend/dist/` 是其建置產物，兩者各有用途。

- 原本 108 個 400 字重分片合併為 1 個：3,035,932 → 2,473,812 bytes（減少 18.5%）。
- 字型版本維持 2.003，保留原先 cmap 的全部 12,377 個 Unicode 字元；沒有只依目前畫面文字裁切，因此動態回答的既有字元覆蓋不變。
- [官方來源](https://github.com/notofonts/noto-cjk/blob/985fa52c81c1d6692ccdd82bc3656e8fb932fd89/google-fonts/NotoSerifTC%5Bwght%5D.ttf) 固定於 commit `985fa52c81c1d6692ccdd82bc3656e8fb932fd89`。以 fonttools 4.66.1 保留舊分片字元聯集、釘選 `wght=400`，輸出靜態 WOFF2；原分片仍可在 Git `6a618ef` 查閱。
- WOFF2 SHA-256：`3154709ea75f60d7cfad29edf6feac38e262dbb4d52ea0d9c9d9a6e16774014f`。
- 單一檔案讓 repo 更簡潔；首次載入會讀取整個約 2.47 MB 字型，之後由瀏覽器快取，不再依字元分片下載。

只修改字型資產，版面、文字大小、Regular／合成強調與互動規則沿用現行設計。字型工具只用於這次離線轉換，不加入產品依賴。
