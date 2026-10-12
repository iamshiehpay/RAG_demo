import { useState } from 'react';
import type { FormEvent } from 'react';
import type { Chunk, Citation, LLMCallTrace, ReadyEvent, RetrievedChunk } from './events';
import { Answer } from './Answer';
import { Trace } from './Trace';
import { consumeEvents } from './sse';

interface Turn {
  id: number; question: string; answer: string; citations: Citation[];
  chunks: RetrievedChunk[]; calls: LLMCallTrace[]; status: string; final: boolean; error: string;
}
const message = (error: unknown) => error instanceof Error ? error.message : 'Request failed. Please retry.';

export function App() {
  const [document, setDocument] = useState<ReadyEvent | null>(null);
  const [question, setQuestion] = useState('');
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('Upload a PDF with a text layer to begin.');
  const [error, setError] = useState('');
  const [source, setSource] = useState<Chunk | null>(null);
  const updateTurn = (id: number, update: (turn: Turn) => Turn) => setTurns(previous => previous.map(
    turn => turn.id === id ? update(turn) : turn,
  ));

  async function upload(file: File) {
    setBusy(true); setError(''); setDocument(null); setTurns([]); setSource(null);
    setUploadStatus('Uploading Document…');
    const form = new FormData(); form.append('document', file);
    try {
      await consumeEvents(await fetch('/api/documents', { method: 'POST', body: form }), event => {
        if (event.type === 'stage') {
          const labels = { parsing: 'Reading PDF', chunking: 'Preparing Chunks', embedding: 'Building the search index' };
          setUploadStatus(`${labels[event.stage]}…`);
        } else if (event.type === 'ready') {
          setDocument(event); setUploadStatus(`${event.name} · ${event.chunk_count} Chunks · Ready`);
        } else if (event.type === 'error') {
          setError(event.message); setUploadStatus('Document could not be processed. Choose another PDF.');
        }
      });
    } catch (error) {
      setError(message(error)); setUploadStatus('Upload failed. Please choose the PDF again.');
    } finally { setBusy(false); }
  }

  async function ask(askedQuestion: string) {
    if (!askedQuestion.trim() || !document || busy) return;
    const id = Date.now();
    setBusy(true); setError(''); setSource(null); setQuestion('');
    setTurns(previous => [...previous, { id, question: askedQuestion, answer: '', citations: [],
      chunks: [], calls: [], status: 'Planning question…', final: false, error: '' }]);
    try {
      await consumeEvents(await fetch('/api/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: askedQuestion }),
      }), event => updateTurn(id, turn => {
        switch (event.type) {
          case 'plan': return { ...turn, status: 'Retrieving evidence…' };
          case 'retrieval': return { ...turn, chunks: event.chunks, status: 'Thinking…' };
          case 'citation_map': return { ...turn, citations: event.citations };
          case 'delta': return { ...turn, answer: turn.answer + event.text, status: 'Provisional answer' };
          case 'retry': return { ...turn, answer: '', status: 'Regenerating…' };
          case 'final': return { ...turn, answer: event.answer, citations: event.citations,
            final: true, status: 'Answer complete' };
          case 'trace': return { ...turn, calls: event.calls };
          case 'error': return { ...turn, answer: '', error: event.message, status: 'Answer failed', final: false };
          default: return turn;
        }
      }));
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
      <input id="document" type="file" accept="application/pdf,.pdf" disabled={busy}
        onChange={event => { const file = event.target.files?.[0]; if (file) void upload(file); event.target.value = ''; }} />
      <p role="status">{uploadStatus}</p>
    </section>
    {error && <p className="error" role="alert">{error}</p>}
    <section className="conversation" aria-label="Conversation">
      {!turns.length && <p className="empty">{document ? 'Your Document is ready. What would you like to know?' : 'Questions will be available when your Document is ready.'}</p>}
      {turns.map(turn => <article key={turn.id}>
        <h2>{turn.question}</h2>
        <p className={turn.final ? 'status' : 'status provisional'} role="status">{turn.status}</p>
        <Answer text={turn.answer} citations={turn.citations} onSource={citation => void showSource(citation)} />
        {turn.error && <div className="error" role="alert"><p>{turn.error}</p>
          <button disabled={busy} onClick={() => void ask(turn.question)}>Retry question</button></div>}
        {(turn.chunks.length > 0 || turn.calls.length > 0) && <Trace chunks={turn.chunks} calls={turn.calls} />}
      </article>)}
    </section>
    {source && <section className="source" aria-label="Citation source">
      <div className="source-heading"><h2>Source · p.{source.page_start} · {source.section}</h2>
        <button onClick={() => setSource(null)}>Close source</button></div>
      <pre>{source.text}</pre>
    </section>}
    <form onSubmit={submit}>
      <label htmlFor="question">Question</label>
      <textarea id="question" rows={3} value={question} onChange={event => setQuestion(event.target.value)}
        disabled={!document || busy} placeholder={document ? 'Ask about your Document…' : 'Upload a Document first'} />
      <button type="submit" disabled={!document || busy || !question.trim()}>{busy && document ? 'Answering…' : 'Ask'}</button>
    </form>
  </main>;
}
