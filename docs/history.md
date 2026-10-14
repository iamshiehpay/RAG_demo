# 歷史與證據索引

使用者於 2026-10-14 要求復原 docs 與 ticket 紀錄：`docs/verification/`、`docs/qa/`、`docs/agents/`、`.scratch/chat-with-document/` 及完整 AI log 已恢復到主分支。ADR 從未移除；現行設計、開發指南與精選入口保留新版。

歷史報告與診斷腳本保留當時內容，可能引用舊程式路徑、未復原的實驗輸出或當時環境；不作為目前版本的啟動入口。需要完整當時環境時，使用下列標籤。2026-10-14 整理前的全部內容仍保存在 Git annotated tag：

```text
archive/before-main-cleanup-20261014
commit 906044d0736ebf294e9c84ed452aa2e06c841ad4
```

不切換或修改目前工作目錄，也能閱讀任一歷史檔：

```sh
git show archive/before-main-cleanup-20261014:docs/ai-log.md
git show archive/before-main-cleanup-20261014:eval/reports/issue11-correction/conclusions.md
```

| 要追查的內容 | 標籤內原始路徑 |
|---|---|
| 完整人與 AI 決策／修正 | `docs/ai-log.md` |
| 需求、16 個工作項目與執行紀錄 | `.scratch/chat-with-document/` |
| Ollama budget、think 與 embedding 探索 | `spikes/`（含 `out/`） |
| 最終評估的完整失敗分析 | `eval/reports/issue11-correction/conclusions.md` |
| 受控檢索方法與結果 | `eval/reports/issue11-correction/retrieval-controlled.md` |
| A9 七次診斷 | `docs/verification/ticket-13/d22/probe/final-report.md` |
| LangGraph 獨立審查與整合 | `docs/verification/ticket-14/` |
| 前一輪測試／交付整理 | `docs/verification/release-refactor.md` |
| 介面歷次設計與瀏覽器證據 | `frontend/review/`、`docs/verification/ticket-12/` |
| 早期評估、調參、中間截圖 | `eval/reports/`、`docs/qa/`、`docs/verification/` |
| 題目與簡報筆記 | 根目錄的題目筆記與 `簡報素材.md` |

`git ls-tree -r --name-only archive/before-main-cleanup-20261014` 可列出全部歷史檔案。需要完整獨立副本時可對該標籤使用 `git archive`。主分支的移除不會抹除 Git 歷史，也沒有清空 `.cache/`、下載 PDF 或既有 worktree。

zip 不含 Git 歷史；完整證據需要 repository 與此標籤。設定遠端後，請連同 annotated tag 推送；目前是否已推送以實際 Git 狀態為準。
