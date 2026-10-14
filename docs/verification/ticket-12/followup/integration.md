# D16 前端修正版整合驗證

Main整合候選：`ac1be368cb0c7c7751d0a9eb2d3e4d7fd4260261`；產品程式`9a0715e`。後续文件checkpoint不改程式。

- Main直接核對完整兩輪獨立Review與最終75項browser檢查，fresh限定Spec／Standards均APPROVE。見[review/completion.md](review/completion.md)；保留初次空白／拖曳回歸及測試量測時機失敗，不覆寫历史結果。
- 唯一一次Main完整測試：`PYTHONPATH=src:. .venv/bin/python -m pytest -q`，327 passed、3 eval deselected、0 skipped、exit0、265.71s。6項dependency deprecation warnings不影響結果。見[完整輸出](integration-full-suite.txt)、[環境](integration-environment.json)、[結果](integration-result.json)。未重跑模型eval。
- Python及application import來自Main；LightRAG16頁、第二份PDF109頁存在；500-token dense／5-3-2／medium／summary concurrency4與58005fcc pipeline維持。Main再次確認src/tests/frontend/eval/scripts/config無未提交產品差異。
- 本機8101最初connection refused且無listener；Main啟動已合併版本供人工QA。首頁、JS、CSS、本地字型均HTTP200，見[readiness](integration-http-readiness.json)。僅證明可載入，不替代UI驗收。重新開啟頁面並上傳PDF以重建session。
- [人工清單D8–D11](../../final-acceptance/manual-qa-checklist.md)已放行，結果仍NOT_EXECUTED。原D1–D7與既有答案品質觀察保留，不宣稱新版人工全通過。
- #13候選9715538未合併；D18待真人處置。現有後端及原始FAIL保留，前端通過不代表A9／Q3語意已修好。

自有臨時檔已交由原負責者以Trash收尾；乾淨merged工作區暫留供D09人工複驗，Main接管保管，人工後無需修正即可移除。原使用者levi session與不相關服務未清理。
