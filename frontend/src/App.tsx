import { useState } from 'react';
import type { FormEvent } from 'react';
import type { Chunk, Citation, LLMCallTrace, PlanEvent, ReadyEvent, RetrievedChunk, StageEvent, UnverifiedSpan } from './events';
import { Answer } from './Answer';
import { Trace } from './Trace';
import { SourceContent } from './SourceContent';
import { consumeEvents } from './sse';
import { UploadProgress } from './Shared';

interface Turn {
  id: number; question: string; answer: string; citations: Citation[];
  chunks: RetrievedChunk[]; calls: LLMCallTrace[]; status: string; final: boolean; error: string;
  plan: PlanEvent | null; rejected: boolean;
  thinking: string; unverified: UnverifiedSpan[]; invalidCitationCount: number; droppedChunkCount: number; retrying: boolean;
}
const message = (error: unknown) => error instanceof Error ? error.message : 'Request failed. Please retry.';
async function responseMessage(response: Response, fallback: string) {
  const payload = await response.json().catch(() => null) as { detail?: unknown } | null;
  return typeof payload?.detail === 'string' ? payload.detail : fallback;
}

export function App() {
  const [document, setDocument] = useState<ReadyEvent | null>(null);
  const [question, setQuestion] = useState('');
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStage, setUploadStage] = useState<StageEvent | null>(null);
  const [uploadEventsUrl, setUploadEventsUrl] = useState('');
  const [error, setError] = useState('');
  const [source, setSource] = useState<Chunk | null>(null);
  const updateTurn = (id: number, update: (turn: Turn) => Turn) => setTurns(previous => previous.map(
    turn => turn.id === id ? update(turn) : turn,
  ));

  async function upload(file: File) {
    setBusy(true); setUploading(true); setUploadStage(null); setUploadEventsUrl(''); setError('');
    const form = new FormData(); form.append('document', file);
    let eventsUrl = '';
    try {
      const response = await fetch('/api/documents', { method: 'POST', body: form });
      if (!response.ok) throw new Error(await responseMessage(response,
        `Upload failed (${response.status}). Please retry.`));
      const accepted = await response.json() as { job_id: string; events_url: string };
      eventsUrl = accepted.events_url;
      setUploadEventsUrl(eventsUrl);
      await followUpload(eventsUrl);
    } catch (error) {
      setError(message(error));
      if (!eventsUrl) setUploading(false);
    } finally { setBusy(false); }
  }

  async function followUpload(eventsUrl: string) {
    const response = await fetch(eventsUrl);
    if (!response.ok) {
      setUploading(false); setUploadEventsUrl(''); setUploadStage(null);
      throw new Error(`${await responseMessage(response, 'Upload progress is unavailable.')} Choose the PDF again.`);
    }
    await consumeEvents(response, event => {
      if (event.type === 'stage') setUploadStage(event);
      else if (event.type === 'ready') {
        setDocument(event); setTurns([]); setSource(null); setQuestion(''); setError('');
        setUploading(false); setUploadEventsUrl('');
      } else if (event.type === 'error') {
        setError(event.message); setUploading(false); setUploadEventsUrl('');
      }
    });
  }

  async function reconnectUpload() {
    setBusy(true); setError('');
    try { await followUpload(uploadEventsUrl); }
    catch (error) { setError(message(error)); }
    finally { setBusy(false); }
  }

  async function ask(askedQuestion: string, retryId?: number) {
    if (!askedQuestion.trim() || !document || busy || uploading) return;
    if (retryId !== undefined && turns.at(-1)?.id !== retryId) return;
    const id = retryId ?? Date.now();
    setBusy(true); setError(''); setSource(null); setQuestion('');
    const freshTurn: Turn = { id, question: askedQuestion, answer: '', citations: [],
      chunks: [], calls: [], plan: null, rejected: false,
      thinking: '', unverified: [], invalidCitationCount: 0, droppedChunkCount: 0, retrying: false,
      status: '判斷問題類型', final: false, error: '' };
    setTurns(previous => retryId === undefined ? [...previous, freshTurn] :
      previous.map(turn => turn.id === retryId ? freshTurn : turn));
    try {
      await consumeEvents(await fetch('/api/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: askedQuestion }),
      }), event => {
        if (event.type === 'rejected') setQuestion(askedQuestion);
        updateTurn(id, turn => {
          switch (event.type) {
            case 'plan': return { ...turn, plan: event, status: '檢索' };
            case 'retrieval': return { ...turn, chunks: event.chunks, droppedChunkCount: event.dropped_chunk_count, status: '思考中' };
            case 'citation_map': return { ...turn, citations: event.citations };
            case 'thinking': return { ...turn, thinking: turn.thinking + event.text };
            case 'delta': return { ...turn, answer: turn.answer + event.text,
              status: turn.retrying ? '重新產生中 · 暫定' : '回答中 · 暫定' };
            case 'retry': return { ...turn, answer: '', thinking: '', unverified: [],
              retrying: true, final: false, status: '重新產生中' };
            case 'final': return { ...turn, answer: event.answer, citations: event.citations,
              unverified: event.unverified, retrying: false, final: true, status: 'Answer complete' };
            case 'trace': return { ...turn, calls: event.calls,
              invalidCitationCount: event.invalid_citation_count, droppedChunkCount: event.dropped_chunk_count };
            case 'rejected': return { ...turn, answer: '', error: event.message,
              rejected: true, status: '問題過長，請縮短問題', final: false };
            case 'error': return { ...turn, answer: '', error: event.message, status: 'Answer failed', final: false };
            default: return turn;
          }
        });
      });
    } catch (error) {
      updateTurn(id, turn => ({ ...turn, answer: turn.final ? turn.answer : '', error: message(error), status: 'Connection interrupted' }));
    } finally { setBusy(false); }
  }

  async function showSource(citation: Citation) {
    try {
      const response = await fetch(`/api/sources/${encodeURIComponent(citation.source_id)}`);
      if (!response.ok) throw new Error(response.status === 404 ? 'Source not found.' : 'Could not load source.');
      setSource(await response.json() as Chunk);
    } catch (error) { setError(message(error)); }
  }

  function submit(event: FormEvent) { event.preventDefault(); void ask(question); }

  return <main>
    <header><h1>Chat with Document</h1><p>Ask a question. Follow the evidence back to your Document.</p></header>
    <section className="upload" aria-label="Upload Document">
      <label htmlFor="document">PDF Document</label>
      <input id="document" type="file" accept="application/pdf,.pdf" disabled={busy || uploading}
        onChange={event => { const file = event.target.files?.[0]; if (file) void upload(file); event.target.value = ''; }} />
      <UploadProgress stage={uploadStage} busy={uploading} ready={!!document} name={document?.name} />
      {uploading && !busy && uploadEventsUrl &&
        <button onClick={() => void reconnectUpload()}>Reconnect upload progress</button>}
    </section>
    {error && <p className="error" role="alert">{error}</p>}
    <section className="conversation" aria-label="Conversation">
      {!turns.length && <p className="empty">{document ? 'Your Document is ready. What would you like to know?' : 'Questions will be available when your Document is ready.'}</p>}
      {turns.map(turn => <article key={turn.id}>
        <h2>{turn.rejected ? '問題過長' : turn.question}</h2>
        <p className={turn.final ? 'status' : 'status provisional'} role="status">{turn.status}</p>
        <Answer text={turn.answer} citations={turn.citations} provisional={!turn.final}
          unverified={turn.unverified} onSource={citation => void showSource(citation)} />
        {turn.error && <div className="error" role="alert"><p>{turn.error}</p>
          {!turn.rejected && turn.id === turns.at(-1)?.id &&
            <button disabled={busy || uploading} onClick={() => void ask(turn.question, turn.id)}>Retry question</button>}</div>}
        {(turn.plan || turn.chunks.length > 0 || turn.calls.length > 0) &&
          <Trace plan={turn.plan} chunks={turn.chunks} calls={turn.calls}
            thinking={turn.thinking} invalidCitationCount={turn.invalidCitationCount} droppedChunkCount={turn.droppedChunkCount} />}
      </article>)}
    </section>
    {source && <section className="source" aria-label="Citation source">
      <div className="source-heading"><h2>Source · p.{source.page_start} · {source.section}</h2>
        <button onClick={() => setSource(null)}>Close source</button></div>
      <SourceContent source={source} />
    </section>}
    <form onSubmit={submit}>
      <label htmlFor="question">Question</label>
      <textarea id="question" rows={3} value={question} onChange={event => setQuestion(event.target.value)}
        disabled={!document || busy || uploading} aria-describedby={!document || uploading ? 'question-disabled-reason' : undefined}
        placeholder={document ? 'Ask about your Document…' : 'Upload a Document first'} />
      {(!document || uploading) && <p id="question-disabled-reason" role="status">
        {uploading ? '文件處理中，完成後才能提問。' : '請先上傳 PDF，文件準備完成後才能提問。'}
      </p>}
      <button type="submit" disabled={!document || busy || uploading || !question.trim()}>{busy && document && !uploading ? 'Answering…' : 'Ask'}</button>
    </form>
  </main>;
}
