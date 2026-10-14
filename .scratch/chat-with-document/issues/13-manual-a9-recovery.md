# #13 來源警告、限制題與通用回答結構

Status: needs-info

## Parent

[Chat with Document PRD](../PRD.md)、#11人工A9。使用者D14 B核准一輪有界診斷與最小通用修正；D13僅屬#12，分開處理。

## What to build

文件有明確支持的限制／取捨時，能依據原文提出有條件的回答；系統新增的解析／表格重建警告不能被當成作者的研究主張或方法限制。保持來源對應、固定拒答與10K guard。原版A9精確拒答原因未證實；不得把另一次重跑的警告誤歸因冒充相同重現。

## Acceptance criteria

- [ ] 用已保存的公開事件／來源與最小回饋，分開驗證原拒答與警告誤歸因；清楚記錄能重現與不能重現的項目。
- [x] 最小通用修正不包含測試論文名稱、Golden Facts數字或回歸標籤；不改消融題、檢索調參、模型／額度、事件契約或前端。
- [ ] 先有有效RED，再有GREEN的必要回歸：文件主張与系統警告區分；真實作者限制保留；來源沒有答案時仍固定拒答。測試替身不取代真實模型。
- [ ] 真實gpt-oss驗證A9與無關材料的支持／缺失情境，保存原始答案、來源與Trace；不以有效Citation ID取代語意核對。保留原始FAIL與因果不確定性。
- [x] 必要檢查與完整確定性測試通過，獨立GPT6-sol high限定Review覆蓋完整本票diff、實作路徑與既有接口回歸；修正後fresh scoped複審。
- [ ] 若修改處理流程則更新快取版本並移交最新版；若只改回答流程，驗證原快取仍適用，不為文件改動重跑N3。
- [ ] Main整合後一次完整測試，D09使用者複驗受影響問題；如有剩餘FAIL如實回報，不自動豁免或無限調整。

## Ownership and dependencies

實作者獨占backend必要最小模組、相關tests與docs/verification/ticket-13/，既有診斷基準b956247與docs/verification/ticket-11/manual-a9/由Main保存。Frontend和事件契約屬#12且不可改。Main擁有tracker、AGENTS及integration。工作區沿用.worktrees/a9-document-diagnosis的乾淨分支，新的實作context接手；不動8101、8201或其他agent資源。D14 B解除本票修正阻塞，D13不限制本票指定GPT Review。

## Evidence

[有界診斷報告](../../../docs/verification/ticket-11/manual-a9/report.md)。真人核准：原Main native msg_01a135cc-b284-7333-9fd9-d4266343c55a（2026-10-13T15:06:09Z），對應D14 B提案。原拒答與警告誤歸因均保留FAIL，修正前未宣稱原因已找到。

## Current candidate and blocker

候選cd3c8aa（sourceb236b10；已審eac9b07後僅文件更新）保留在`.worktrees/a9-document-diagnosis`／`lat/a9-document-diagnosis`。Main已核對clean、祖先關係與完整兩軸Review；335確定性測試通過／zeroSKIP，兩個獨立GPT6-sol high Reviewer各8項回歸通過，無actionable code findings。這不等於實際語意驗收通過。

兩次fresh公開上傳在摘要0/25遇Ollama429，沒有新快取或驗證答案；唯一同source恢復已用完，停止provider呼叫。真實A9與無關材料支持／缺失檢查、兩份最新版快取仍NOT_EXECUTED。Main不提前合併；原拒答與警告誤歸因FAIL保留，原拒答原因UNPROVEN，限流解除時間未知。needs-info表示外部環境恢復條件未明，不是等待已核准修正的再次許可。

服務恢復後沿用固定候選與`docs/verification/ticket-13/live_probe.py`完成既定有界驗證，不改模型、額度、並行數或快取版本來繞過。通過必要關卡後才整合、跑一次Main完整測試，再依D09由使用者複驗。完整報告與兩軸Review目前在候選worktree的`docs/verification/ticket-13/`；未冒充已存在Main。

## 2026-10-14 D17：文件政策與回答結構

使用者直接核准保留文件限定回答，並加入通用、自適應的回答結構（proposal msg_0e228c9f1f8aeb20016acebfd5b80c819194cd86bbdd32c02a；human msg_01a137a1）。原cd3c8aa完整Review與335PASS保留作為基準，不冒充新delta已審。由同一實作者順序修改，避免共用answer prompt衝突；本票未合併前擴充同一有界交付。

- [ ] 依問題長短安排「先給結論、分點解讀、必要數據與反例、比較限制」；簡單事實題、明確格式題與固定拒答不硬塞全套標題，不預設逐格抄表。
- [ ] 通用規則分清作者解釋／表格觀察、共同基準的分開比較／直接對決；每條事實有Citation，數字關聯不改寫。不含LightRAG名稱、Golden Facts數字或回歸標籤。
- [ ] 不使用文件外知識；不支持時仍依提問語言固定拒答。已有來源警告區分／有條件作者限制／壓縮警告保留與10K不回歸。
- [ ] 先建立必要RED→GREEN；最終source完整測試一次；新delta以cd3c8aa為base由fresh GPT6-sol high雙軸限定Review，原Review與本輪合起來覆蓋完整交付。
- [ ] 真實gpt-oss有界檢查Q2/Q3結構及引用支持、A9、无關材料支持與缺失題；明確記錄品質FAIL，不以結構好看當成事實正確，不重跑完整N3。
- [ ] 正常fingerprint處理／兩份新快取及Main整合測試、D09受影響人工QA；若429仍在，保持真實gate NOT_EXECUTED，不假造cache或提前宣稱完成。

上方兩項已勾選的本輪前基準測試／通用性只證明cd3c8aa；新結構delta待本段驗證。第一次新provider檢查先以最終prompt做一個小型guarded held-out支持題；429即停，成功才進行既定fresh上傳／有界答案驗證。無額外模型、帳號、並行數或規則替代。第1項概覽警告中文化仍只討論，不在本次核准中。

### D17 first scoped Review and correction

c3b47fb完整345PASS；預檢＋既定五題與三份處理共129次真實呼叫守住10K，最新快取已完成。原始結果仍有A9範圍／推論、Q2逐項引用／系統警告揭露、Q3選擇性解讀及限定語缺失，完整兩軸Review未給整體通過。Main已讀原始答案與相關來源，授權D17範圍內一輪必要的通用prompt呈現／回答契約修正，保留原FAIL；不調檢索／Overview或模型。以c3b47fb為下一輪fresh scopedReview基準，完成必要測試與同組有界實測後才裁決整合。

### Final bounded candidate and D18

最終9715538（已審79507a9、production4e647b0）已固定，Main核對clean及文件尾提交。347完整測試PASS、130真實呼叫守10K、兩份示範文件新快取與重傳完成。fresh獨立兩軸Review無新程式finding，仍有A9/Q3錯誤變體定義與來源範圍、Q3錯誤全面最佳結論／整表抄寫、作者推測被強化、Q2引用／涵蓋不足；正面警告揭露未被本輪實際引用觸發。支持／缺失題各PASS一次。

完整原始結果與四份Review在候選worktree `docs/verification/ticket-13/d17/correction/`。不追加品質迴圈，不自動套用D10的舊版例外。D18待真人决定先只合併介面並保留後端候選，或接受明列限制後整合候選；未答前不合併#13。#12與其驗證不受阻。
