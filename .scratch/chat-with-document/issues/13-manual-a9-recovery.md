# #13 人工限制題的拒答與系統警告誤歸因

Status: ready-for-agent

## Parent

[Chat with Document PRD](../PRD.md)、#11人工A9。使用者D14 B核准一輪有界診斷與最小通用修正；D13僅屬#12，分開處理。

## What to build

文件有明確支持的限制／取捨時，能依據原文提出有條件的回答；系統新增的解析／表格重建警告不能被當成作者的研究主張或方法限制。保持來源對應、固定拒答與10K guard。原版A9精確拒答原因未證實；不得把另一次重跑的警告誤歸因冒充相同重現。

## Acceptance criteria

- [ ] 用已保存的公開事件／來源與最小回饋，分開驗證原拒答與警告誤歸因；清楚記錄能重現與不能重現的項目。
- [ ] 最小通用修正不包含測試論文名稱、Golden Facts數字或回歸標籤；不改消融題、檢索調參、模型／額度、事件契約或前端。
- [ ] 先有有效RED，再有GREEN的必要回歸：文件主張与系統警告區分；真實作者限制保留；來源沒有答案時仍固定拒答。測試替身不取代真實模型。
- [ ] 真實gpt-oss驗證A9與無關材料的支持／缺失情境，保存原始答案、來源與Trace；不以有效Citation ID取代語意核對。保留原始FAIL與因果不確定性。
- [ ] 必要檢查與完整確定性測試通過，獨立GPT6-sol high限定Review覆蓋完整本票diff、實作路徑與既有接口回歸；修正後fresh scoped複審。
- [ ] 若修改處理流程則更新快取版本並移交最新版；若只改回答流程，驗證原快取仍適用，不為文件改動重跑N3。
- [ ] Main整合後一次完整測試，D09使用者複驗受影響問題；如有剩餘FAIL如實回報，不自動豁免或無限調整。

## Ownership and dependencies

實作者獨占backend必要最小模組、相關tests與docs/verification/ticket-13/，既有診斷基準b956247與docs/verification/ticket-11/manual-a9/由Main保存。Frontend和事件契約屬#12且不可改。Main擁有tracker、AGENTS及integration。工作區沿用.worktrees/a9-document-diagnosis的乾淨分支，新的實作context接手；不動8101、8201或其他agent資源。D14 B解除本票修正阻塞，D13不限制本票指定GPT Review。

## Evidence

[有界診斷報告](../../../docs/verification/ticket-11/manual-a9/report.md)。真人核准：原Main native msg_01a135cc-b284-7333-9fd9-d4266343c55a（2026-10-13T15:06:09Z），對應D14 B提案。原拒答與警告誤歸因均保留FAIL，修正前未宣稱原因已找到。
