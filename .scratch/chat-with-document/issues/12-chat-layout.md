# #12 對話排版與中文回答過程

Status: ready-for-human

## Parent

[Chat with Document PRD](../PRD.md)。使用者於2026-10-13核准D11版型A及D12今晚由levi主控的前端實作；本票完整保存新增範圍，其他#11品質缺陷與驗收結果維持。

## What to build

把網站改成適合持續提問的三欄對話介面。左欄顯示Document、上傳狀態與Document Summary；中欄顯示問題與回答，底部固定輸入框；右欄顯示點選Citation的原文。左右欄可收合，中欄隨之變寬，對話區可上下捲動。

使用者問題靠右，不再用Question編號；回答表格在自己的橫向捲動區內，不撐寬整頁。Citation改為句內小編號，點選後展開右欄，保留Chunk、Table Chunk、Section Summary及Group來源的既有內容與警告。

介面預設中文，Trace在畫面上稱「回答過程」。收合時概述Question Type、來源數／Summary Tree層、模型呼叫數、單次最大用量／10,000；展開後呈現系統理解的問題、每一步的模型／思考量／額度／時間、找到的原文段落。模型名稱保持原名：回答與判斷問題類型使用gpt-oss:120b-cloud，檢索使用本機bge-m3。不要把embedding誤列為受10K限制的LLM呼叫；Global未檢索时不製造檢索步驟。

移除頁首標語與預設介面的模型思考區；思考原文、原始token欄位及完成原因放進預設收合的「技術細節（開發用）」。回答內容仍依提問語言。保留Tufte米白／襯線／少裝飾、16px內文、本地字型、暫定／重新產生／未驗證／錯誤重試／上傳進度與換文件重置。

## Acceptance criteria

- [ ] Document →提問→串流回答→點Citation→右欄原文可完整操作；左右欄可收合，輸入框固定，對話獨立捲動。
- [ ] 問題靠右且無Question編號；桌面與390px窄螢幕不產生整頁橫向溢出，長表格可在自身框內捲動；中文組字Enter不誤送出。
- [ ] C/S引用、表格結構警告、來源loading/error/404、換文件重置及既有安全Markdown/未驗證定位行為保留。
- [ ] 「回答過程」三段及收合摘要顯示真實事件資料、正確中文與模型；Global層級／非檢索情況、fallback、重試／錯誤與空thinking均合理呈現。10K長條及送入＋預留的語義不變。
- [ ] 原始思考只在收合的技術細節中，移除指定標語；字型不向外部CDN載入。
- [ ] 型別檢查、前端來源與事件契約檢查、重新build並提交dist、受影響HTTP回歸通過。桌面／窄螢幕劇本UI及至少一次真實gpt-oss公開流程有證據；不以scriptedLLM代替真實模型smoke。
- [ ] 獨立Review完整覆蓋候選diff與實際路徑；實際模型／effort／權限可核對，D13未解前不替換指定Reviewer。
- [ ] nova核對候選、整合後完整測試及跨票限制；使用者在整合網站完成受影響介面人工QA。舊版通過不代替改版驗收。

## Blocked by

- #11的已整合程式基準db64d84（已滿足；最新文件checkpoint b956247程式相同）。原版人工A9症狀確認不阻擋獨立前端實作，但整體交付不靜默豁免。
- Review階段：D13已由使用者明確接受Opus5.5審查結果，解除替代阻塞。Main直接核對兩輪實際模型與medium effort、Sonnet5.5 high實作。

## Ownership and integration constraints

D12限定例外：levi負責設計／實作協調，程式由Sonnet5.5 high subagent撰寫。nova維持整合及tracker所有權；levi不改Main、不merge。工作分支lat/12-chat-layout基於db64d84；交付前接上最新Main文件checkpoint並核對衝突。只改前端、重新build產物與必要前端驗證證據；不得改後端、事件契約、模型呼叫、prompt、Golden Facts或快取政策。8101由使用者操作，測試使用獨立8121並清理自己的資源。

使用者在nativeClaude b9ac5768的proposal f732b249／human4b233eaa、a1068057核准今晚執行與上述分工；D11版型選擇human87568787。D13真人72ef3e0c已接受Opus5.5審查；D15真人5e4e0e03允許只同步AGENTS兩格。

## Integration progress

候選af6b9f3已ff-only整合；reviewed production1c274e4不變。完整兩輪Review、實作路徑與Main核對見[review.md](../../../docs/verification/ticket-12/review.md)。前端型別／build／source／event契約、36次UI劇本、真實模型smoke及6項HTTP測試已核對；Main完整測試接續執行，D09新版人工介面驗收尚未執行，不先關票。

Main完整測試：abd7fc7上327PASS、3eval deselected、zeroSKIP、252.49s、exit0；新assets由8101正常提供。詳見[integration.md](../../../docs/verification/ticket-12/integration.md)。D1–D7人工QA已放行，等待使用者結果；尚未標done。

## 2026-10-14 人工回饋：UI 後續修正（D16）

原abd7fc7整合／327PASS證據保留。本輪重新開啟受影響介面項目，沿用本票清單，不把原版人工回饋當成新版全PASS。真人原文與來源見D16（msg_01a1379a；快捷題選擇msg_01a1379c）。

- [ ] 來源收合欄可讀；桌面可拖曳調整來源面板寬度，文字隨宽度重排。保留鍵盤可操作、可見焦點、窄螢幕來源開關／Escape／焦點恢復；不讓對話或來源撐破畫面。
- [ ] 整理輸入框層次、留白與送出按鈕，保持既有米白、Noto Serif TC、少裝飾及底部固定；IME、送出／產生中／錯誤狀態不回歸。
- [ ] 輸入框下方五個可點即送出的快捷題：三個題目原文（Summary this document.／Compare LightRAG with GraphRAG.／Performance of ablated versions of LightRAG.），以及「這篇論文有什麼限制？」與「LightRAG 在 HotpotQA 上的分數是多少？」。只在Document Ready且未產生回答時可送出；一次點擊只送一次；與手動提問共用流程。其他Document不能默默顯示為其量身打造的LightRAG問題，使用明確範例標示或合適的文件限定展示。
- [ ] 移除指定兩句可見文字與回答中的裝飾底線，Citation保持可辨認且可點、鍵盤焦點可見、Unverified語意保留；無障礙表單label保留但不必可見。
- [ ] 修正heading／paragraph／list間距及句內Citation排版，重播使用者所貼GraphRAG／LightRAG成本與更新段落、長Q3列表與表格；不重寫回答事實或掩蓋原始錯誤。
- [ ] 本輪必要前端／HTTP檢查、dist重建、獨立Review與整合後完整測試通過；補充原D1–D7人工清單的受影響情境供使用者再驗。

依賴：Mainabd7fc7。與#13獨立，不能混入其未驗證backend；此輪純呈現／互動，可用保存的真實輸出做渲染回歸，明記重播不是新模型驗證。無新的provider呼叫，429阻塞不以改模型／帳號／額度繞過。第1/7/8項只討論，未授權prompt或文件外回答政策修改。

### D16修正版整合結果

ac1be36（production9a0715e）已ff-only整合；fresh兩軸限定Review APPROVE、最終browser75PASS／0FAIL。Main同版本完整測試327PASS／3eval deselected／zeroSKIP／265.71s／exit0，來源與前端保持已審版本。首頁、JS、CSS與本地字型HTTP200。詳見[followup integration](../../../docs/verification/ticket-12/followup/integration.md)。D8–D11已放行，由使用者重新整理8101操作；未回報前不勾人工驗收或標done。暫留乾淨worktree供這次人工複驗，其他自有測試暫存清理，協作角色收尾。
