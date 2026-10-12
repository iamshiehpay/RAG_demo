/** Minimal state components; #09 supplies the final design. */
export function UnverifiedMark() {
  return <span className="unverified-mark" role="note">未驗證 · Unverified</span>;
}

export function ThinkingContent({ text }: { text: string }) {
  if (!text) return null;
  return <details className="thinking-content"><summary>Model thinking</summary><pre>{text}</pre></details>;
}
