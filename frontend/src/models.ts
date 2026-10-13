// 模型名稱的單一來源。
// 事件契約（LLMCallTrace）沒有 model 欄位，所以這裡用常數表達；
// 數值必須與後端設定一致（src/chat_document/llm_adapter.py 的 gpt-oss:120b-cloud、
// embedder.py 的 bge-m3）。後端若改模型，這個檔案要同步修改。
export const LLM_MODEL = 'gpt-oss:120b-cloud';
export const EMBEDDING_MODEL = 'bge-m3（本機）';
