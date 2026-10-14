# #14 LangGraph提問流程編排

Status: ready-for-agent

## Scope

D24使用者已確認直接遷移，不做比較prototype。基準Main5f5e35f；只將Application.ask的手寫提問編排替換為明確StateGraph，保留既有模組的核心行為。上傳、PDF解析、Chunker、檢索策略、prompt、模型、LLMGateway/10K、前端及新資料集快捷題維持。

可採 validate → plan → evidence → generate → finalize 的可讀節點；Global使用Summary Tree，其餘走現有ContextPacker。ContextPacker分批抽取與AnswerGenerator的截斷重試先維持原位置。Document／service依賴以請求context或closure提供，避免塞入可序列化graph state；本次不引入持久化/checkpointer、新工作流能力或另一套網站。

## Acceptance

- [x] Application公開ask入口由真實LangGraph編排，不只新增未使用graph或外包一個包住舊大函式的node；三種Question Type路徑可讀，原手寫重複編排移除。
- [x] 公開SSE事件名稱／結構／順序不變：plan/stages、Global空retrieved、citation map先於delta、thinking/暫定／重試reset、final經驗證Citation與Trace；仍逐token串流，不變成等整個graph結束才一次吐出。
- [x] 所有LLM呼叫沿用同一guard、額度與model/think；不新增LLM呼叫、prompt教題或A9品質調整。Synthesis抽取、low retry、invalid引用／拒答保持。
- [x] 歷史只在成功後追加，顯式history不污染內建history；預檢問題長度、未Ready／不存在Document、並發_asking、取消與所有stage-specific錯誤／finally cleanup保持。
- [x] 依官方LangGraph文件選定兼容Python3.12的版本，更新pyproject與uv.lock，從乾淨依賴安裝可啟動；不使用其LLM/loader/retriever wrappers，不改上傳核心或任意快取政策。
- [x] 既有回歸及必要public-seam測試、一次完整普通suite通過；含真正執行graph的取消/錯誤/SSE分支覆蓋。以真實gpt-oss/bge做小型公開上傳／提問smoke；標明劇本與真實證據，不重跑N3調參。
- [ ] 完整diff由獨立gpt-6-luna max/Fast兩軸Review，actual設定可核對；必要修正後fresh scoped複審。Main整合後完整suite、在原8101提供新版，保留全部既有已知FAIL。

## Ownership / verification

唯一實作者owns application orchestration/newgraph module、AnswerGenerator必要iterator關閉接線、必要tests、pyproject/uv.lock、README流程說明與docs/verification/ticket-14。Main owns AGENTS/CONTEXT/ADR/tracker/ai-log/manualQA與整合。只讀API研究角色在指定scratch交結論，不能與實作者同寫source。現有31569a2/D22/D23證據維持原樣；前端/dist從5f5e35f原樣保留。

使用者確認來源：真人msg_01a13877（03:32:23Z），preceding限定scope proposal msg_0f4efa0ee05e245f016acef605a3d08191821e0639a8a201b1。D24提供AGENTS舊規則的受限LangGraph例外，D23跳過驗證不延伸至重構。

## Reviewed candidate

初版d455f50完成333項測試；Luna max/Fast雙軸審查指出換文件完成與graph validate的就緒競態。修正版24fba26以同步snapshot修正，公開Lookup／Global回歸原版2PASS、初版2RED，修正後targeted59PASS、完整335PASS／3eval deselected／zeroSKIP。Fresh限定Standards與Spec均無阻擋finding；非阻擋的私有欄位耦合觀察保留。完整報告見[驗證](../../../docs/verification/ticket-14/verification.md)與其review目錄。

兩次小型真實上傳／三種提問共20次呼叫均stop、10K內；最後取消／就緒修正使用真正graph的確定性回歸，沒有把較早的smoke說成最終source實測。prompt／模型／前端與原有品質FAIL保持。Main整合／完整測試／8101更新仍待完成，最終網站操作依D09由使用者執行。
