# 2026-10-14：LangGraph只編排提問流程

狀態：已接受。使用者於2026-10-14核准直接重構；範圍與驗收見歸檔標籤中的 Issue14（[查詢方式](../history.md)）。

將Application.ask的手寫流程改為LangGraph StateGraph，讓問題檢查、Router、Global或檢索證據、回答串流與定稿各階段有清楚的節點及轉移。Document與服務依賴放在請求context或closure；graph state只承載這次提問的暫態資料，不新增持久化或checkpoint。

Parser、Chunker、Retriever、ContextPacker、AnswerGenerator與原生Ollama LLMGateway保留核心行為。分批抽取仍由ContextPacker處理，截斷後low重試仍由AnswerGenerator處理。所有LLM呼叫繼續經過既有10K budget guard，模型與prompt不改。

遷移必須保留公開SSE事件及其順序、逐字串流、Citation、Trace、成功後才寫入歷史，以及取消／失敗時的清理。上傳與Summary Tree建置不遷移，A9已知缺陷與先前品質報告不改判。

允許LangGraph及必要轉依賴；不使用LangChain的LLM、loader、切塊或retriever wrappers。這是舊框架限制的受限例外。代價是新增依賴及graph串流生命週期，需鎖定版本、確認Python3.12安裝，並以真正執行graph的公開入口回歸測試和真實Ollama smoke驗證。實際選定版本、獨立Review與整合證據隨Issue14保存。

實作鎖定LangGraph 1.2.15（Python 3.12.10乾淨安裝已驗證），以request-scoped AskWorkflow closure提供依賴，compile(checkpointer=False)。透過有界事件佇列和逐事件確認維持公開串流時機；取消時等待自有graph工作與原生串流關閉。就緒狀態與index／Document於請求開始同步捕捉。版本與審查證據見[歷史驗證索引](../history.md)。
