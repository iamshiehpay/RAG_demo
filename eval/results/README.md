# 最終評估與已知限制

此處保留 2026-10-13 修正版 N=3 的原始測量，來自歸檔版本的 `eval/reports/issue11-correction/`。四份原始檔逐位元保留，未重新評分；其中版本、dirty 狀態、舊路徑及 pipeline 指紋均描述當時執行，不代表本次重構又呼叫了模型。

| 文件 | 報告與原始資料 | 當次觀察 |
|---|---|---|
| LightRAG | [報告](final-lightrag.md)、[JSON](final-lightrag.json) | 21 次回答完成、170 次模型呼叫；固定拒答 9/9，品質仍為 FAIL |
| 工業機器人綜述 | [報告](final-second.md)、[JSON](final-second.json) | 6 次回答完成、102 次模型呼叫；數字題與摘要 Golden Facts 各 1/3，品質仍為 FAIL |

所有呼叫均未超過 10K。第二文件有一次 Section Summary 截斷後重試成功；這不是零失敗嘗試。JSON 包含當次公開事件、回答、來源映射、逐項分數及呼叫資訊，可核對 Markdown 摘要。

## 主要失敗

- **Q1**：問題動機、graph indexing、dual-level retrieval、實驗各 3/3；增量更新原始判分 0/3，其中有 Judge 未逐字摘錄的問題。
- **Q2**：檢索比較、成本與增量更新均 0/3；有真實遺漏，也有 Judge 證據限制。一次回答將 Agriculture 的勝率錯配為 Mix 數值。
- **Q3**：Table 2 來源 Citation 3/3；兩個必要的變體／完整版比較均 0/3，且部分回答顛倒 High／Low 的移除元件意義。
- **第二文件**：Table 9 的來源 Citation 3/3，但一次回答把「準則×論文的評估次數」寫成論文數；另有缺少逐論點引用的推論。
- **Judge**：非逐字摘錄、表格列／欄綁定及術語 anchors 會造成額外失敗。人工分析與原始判分分開，不重標成通過。

此外，A9 限制題仍可能拒答或漏答；七次有界診斷後由人決定凍結為已知缺陷。本次結構整理不改 prompt、模型或品質結論。

完整分析、受控檢索比較、A9 診斷及中間實驗的取得方式見 [歷史索引](../../docs/history.md)。當次功能 PASS 不等於每句回答都有充分根據。
