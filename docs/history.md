# 歷史與證據索引

主分支保留開發規劃（`.scratch/chat-with-document/`）、設計與 ADR、維護指南、完整 AI log、精選評估與最新驗證摘要。使用者於 2026-10-14 核准從工作目錄移除 `docs/verification/` 和 `docs/qa/` 的 1,449 個逐輪產物；移除前逐檔核對，內容與下列歸檔標籤完全一致。

歷史報告與診斷腳本保留當時路徑及環境假設，不作為目前啟動入口。AI log、EXECUTION 與 ticket 中的純文字舊路徑也以歸檔版本為準；可點擊的驗證證據連結已改為 GitHub 固定 commit。2026-10-14 整理前完整版本：

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

zip 不含 Git 歷史；完整證據需要 repository 與此標籤。遠端為 `git@github.com:iamshiehpay/RAG_demo.git`；完整交付需連同上述 annotated tag 推送。GitHub 歷史連結需要此私人 repository 的存取權。
