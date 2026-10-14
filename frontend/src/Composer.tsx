import type { FormEvent, KeyboardEvent } from 'react';
import { QuestionShortcuts } from './Shortcuts';

/** Bottom input. Enter submits, Shift+Enter inserts a newline, and IME composition never submits. */
export function Composer({ value, onChange, onSubmit, disabled, canSubmit, busy, help, placeholder, documentName, onShortcut }: {
  value: string; onChange: (value: string) => void; onSubmit: () => void;
  disabled: boolean; canSubmit: boolean; busy: boolean; help: string; placeholder: string;
  documentName: string | undefined; onShortcut: (question: string) => void;
}) {
  function keyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key !== 'Enter' || event.shiftKey) return;
    // keyCode 229 covers browsers that report Enter after composition has already ended.
    if (event.nativeEvent.isComposing || event.keyCode === 229) return;
    event.preventDefault();
    if (canSubmit) onSubmit();
  }
  return <div className="composer">
    <div className="composer-inner">
      <form onSubmit={(event: FormEvent) => { event.preventDefault(); if (canSubmit) onSubmit(); }}>
        <div className="composer-box">
          <textarea id="question" aria-label="問這份文件" rows={2} value={value} onChange={event => onChange(event.target.value)}
            onKeyDown={keyDown} aria-describedby="question-help" disabled={disabled} placeholder={placeholder} />
          <button type="submit" className="send-button" disabled={disabled || !canSubmit}>{busy && !disabled ? '回答中…' : '送出'}</button>
        </div>
        <p id="question-help" className="muted composer-help">{help}</p>
      </form>
      <QuestionShortcuts documentName={documentName} disabled={disabled} onPick={onShortcut} />
    </div>
  </div>;
}
