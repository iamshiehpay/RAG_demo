# #09 Tufte 視覺設計與共用元件（需要人參與）

Status: ready-for-agent

## Parent

`.scratch/chat-with-document/PRD.md`

## What to build

先載入 `web-design-engineer` skill，採用 `tufte-dataink` recipe，把介面做成「附證據的研究筆記」。這個切片採用方案 A：**早點定好版面和共用元件，讓其他切片直接使用。**

- **版面：** 文件概覽、對話區（Citation 以頁邊旁註呈現）、Trace 面板。
- **共用元件：**
  - 旁註形式的 Citation。
  - Citation 的彈出視窗，要能顯示 Chunk 原文、Section 摘要和表格。
  - 以 10K 為滿格的 token 迷你長條。
  - 階段指示。
  - 暫定文字的樣式。
  - 「重新產生中」和錯誤狀態，含重試按鈕。
  - Unverified 標記。
  - 可以收合的思考內容。
  - 上傳進度。
- **規格：**
  - 內文 15～16px。
  - Noto Serif TC 字型檔放在 repo 裡，不從網路載入。
  - 不加裝飾性動畫。
- **流程：**
  1. 先做一版初稿，給人看過。**這是需要人參與的步驟**：等方向確認後才繼續。
  2. 定稿。
  3. 重新 build 前端，並 commit。

## Acceptance criteria

- [x] 初稿經過使用者確認，方向也已同意。
- [ ] 共用元件都已完成，目前的介面也已改用這些元件。
- [ ] 瀏覽器驗收：上傳 → 問 Q3 → 能看到頁邊旁註和 Trace 的 token 長條；離線時字型也能正常顯示。
- [ ] 重新 build 前端，並 commit。

## Blocked by

- #01（`01-walking-skeleton.md`）

## Comments

- 2026-10-13 nova：使用者於 Main session `01a132c0-2f33-7e72-9a63-74731d18d08c` 對 D02 v1 直接回覆「同意，照此方向定稿」。初稿基準 `f15f792`；定稿、重新 build、獨立 Review、整合驗證與獨立 QA 仍待完成。

- 2026-10-13 nova：d48fbf6 已 ff-only 整合，完整與 fresh correction Review 兩軸通過。產品345檔 byte identity、實作者265tests／browser回歸／dist107parity及真實4call渲染證據已保存；仍待最終Main獨立QA與#05概覽複驗，不提前標done。
