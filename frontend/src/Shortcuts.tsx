/** Click-to-send example questions shown under the composer. Static text: nothing here is generated or sent to a model. */
export const LIGHTRAG_QUESTIONS = [
  'Summary this document.',
  'Compare LightRAG with GraphRAG.',
  'Performance of ablated versions of LightRAG.',
  '這篇論文使用哪些資料集進行實驗？',
  'LightRAG 在 HotpotQA 上的分數是多少？',
] as const;
const GENERAL_QUESTIONS = [LIGHTRAG_QUESTIONS[0]] as const;

/** The examples are written for the LightRAG paper; decide by filename only (no backend field exists for this). */
export const isLightRagDocument = (name: string | undefined) => !!name && /lightrag/i.test(name);

export function QuestionShortcuts({ documentName, disabled, onPick }: {
  documentName: string | undefined; disabled: boolean; onPick: (question: string) => void;
}) {
  // Other Documents never see LightRAG-specific questions, and the group is not labelled as tailored to them.
  const tailored = !documentName || isLightRagDocument(documentName);
  const questions = tailored ? LIGHTRAG_QUESTIONS : GENERAL_QUESTIONS;
  // The group name is accessible-only (no visible heading); aria-label keeps it out of the visible text.
  return <div className="shortcuts" role="group" aria-label={tailored ? 'LightRAG 論文範例問題' : '範例問題'}>
    <div className="shortcut-list">
      {/* aria-disabled instead of disabled: a disabled button drops keyboard focus while an answer is generating. */}
      {questions.map(question => <button type="button" key={question} className="shortcut" aria-disabled={disabled}
        onClick={() => { if (!disabled) onPick(question); }}>{question}</button>)}
    </div>
  </div>;
}
