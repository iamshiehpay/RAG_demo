import { useCallback, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import type { Chunk, Citation, LLMCallTrace, PlanEvent, ReadyEvent, RetrievedChunk, StageEvent, UnverifiedSpan } from './events';
import { Answer } from './Answer';
import { Trace } from './Trace';
import { consumeEvents } from './sse';
import { ErrorState, StageIndicator, UploadProgress } from './Shared';
import type { AskStage } from './Shared';
import { SourceDialog } from './SourceDialog';
import type { SummarySource } from './SourceDialog';

interface Turn {
  id: number; question: string; answer: string; citations: Citation[];
  chunks: RetrievedChunk[]; calls: LLMCallTrace[]; stage: AskStage; final: boolean; error: string;
  plan: PlanEvent | null; rejected: boolean;
  thinking: string; unverified: UnverifiedSpan[]; invalidCitationCount: number; retrying: boolean;
  droppedChunkCount: number; summaryLevel: string | null;
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
  const [source, setSource] = useState<Chunk | SummarySource | null>(null);
  const [sourceOpen, setSourceOpen] = useState(false);
  const [sourceLoading, setSourceLoading] = useState(false);
  const [sourceError, setSourceError] = useState('');
  const [sourceKind, setSourceKind] = useState<'Chunk' | 'Section Summary'>('Chunk');
  const sourceRequest = useRef(0);
  const closeSource = useCallback(() => {
    sourceRequest.current++;
    setSourceOpen(false); setSourceLoading(false);
  }, []);
  const updateTurn = (id: number, update: (turn: Turn) => Turn) => setTurns(previous => previous.map(
    turn => turn.id === id ? update(turn) : turn,
  ));

  async function upload(file: File) {
    closeSource(); setBusy(true); setUploading(true); setUploadStage(null); setUploadEventsUrl(''); setError('');
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
      if (response.status === 404) {
        setDocument(null); setTurns([]); setQuestion(''); setSource(null); closeSource();
      }
      throw new Error(`${await responseMessage(response, 'Upload progress is unavailable.')} Choose the PDF again.`);
    }
    await consumeEvents(response, event => {
      if (event.type === 'stage') setUploadStage(event);
      else if (event.type === 'ready') {
        setDocument(event); setTurns([]); setSource(null); closeSource(); setQuestion(''); setError('');
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
    setBusy(true); setError(''); closeSource(); setSource(null); setQuestion('');
    const freshTurn: Turn = { id, question: askedQuestion, answer: '', citations: [],
      chunks: [], calls: [], plan: null, rejected: false,
      thinking: '', unverified: [], invalidCitationCount: 0, retrying: false,
      droppedChunkCount: 0, summaryLevel: null,
      stage: 'planning', final: false, error: '' };
    setTurns(previous => retryId === undefined ? [...previous, freshTurn] :
      previous.map(turn => turn.id === retryId ? freshTurn : turn));
    try {
      await consumeEvents(await fetch('/api/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: askedQuestion }),
      }), event => {
        if (event.type === 'rejected') setQuestion(askedQuestion);
        updateTurn(id, turn => {
          switch (event.type) {
            case 'plan': return { ...turn, plan: event, stage: 'retrieval' };
            case 'retrieval': return { ...turn, chunks: event.chunks,
              droppedChunkCount: event.dropped_chunk_count ?? 0, stage: 'thinking' };
            case 'citation_map': return { ...turn, citations: event.citations };
            case 'thinking': return { ...turn, thinking: turn.thinking + event.text };
            case 'delta': return { ...turn, answer: turn.answer + event.text,
              stage: 'answering' };
            case 'retry': return { ...turn, answer: '', thinking: '', unverified: [],
              retrying: true, final: false, stage: 'retry' };
            case 'final': return { ...turn, answer: event.answer, citations: event.citations,
              unverified: event.unverified, retrying: false, final: true, stage: 'complete' };
            case 'trace': return { ...turn, calls: event.calls,
              invalidCitationCount: event.invalid_citation_count,
              droppedChunkCount: event.dropped_chunk_count ?? 0, summaryLevel: event.summary_level ?? null };
            case 'rejected': return { ...turn, answer: '', error: event.message,
              rejected: true, stage: 'rejected', final: false };
            case 'error': return { ...turn, answer: '', error: event.message, stage: 'error', final: false };
            default: return turn;
          }
        });
      });
    } catch (error) {
      updateTurn(id, turn => ({ ...turn, answer: turn.final ? turn.answer : '', error: message(error), stage: 'error' }));
    } finally { setBusy(false); }
  }

  const showSource = useCallback(async (citation: Citation) => {
    const request = ++sourceRequest.current;
    setSource(null); setSourceError(''); setSourceLoading(true); setSourceOpen(true);
    setSourceKind(citation.id.startsWith('S') ? 'Section Summary' : 'Chunk');
    try {
      const response = await fetch(`/api/sources/${encodeURIComponent(citation.source_id)}`);
      if (!response.ok) throw new Error(response.status === 404 ? 'Source not found.' : 'Could not load source.');
      const content = await response.json() as Chunk | SummarySource;
      if (request === sourceRequest.current) setSource(content);
    } catch (error) {
      if (request === sourceRequest.current) setSourceError(message(error));
    } finally {
      if (request === sourceRequest.current) setSourceLoading(false);
    }
  }, []);

  function submit(event: FormEvent) { event.preventDefault(); void ask(question); }

  const unavailableReason = uploading ? '文件處理中，完成後即可提問。' : !document ? '請先上傳有文字層的 PDF，完成後即可提問。' : busy ? '回答產生中，請稍候。' : '';

  return <main>
    <header className="page-header"><div><p className="eyebrow">Chat with Document</p><h1>與文件對話</h1></div>
      <p className="header-note">讓每個回答，<br />都有出處可循。</p></header>
    <div className="page-layout">
      <aside className="document-sidebar">
        <section className="upload" aria-label="Upload Document">
          <p className="eyebrow">01 / Document</p><h2>閱讀的起點</h2>
          <p className="muted">上傳一份 PDF，從文件內容開始提問。</p>
          <label className="upload-label" htmlFor="document">選擇 PDF Document</label>
          <input id="document" type="file" accept="application/pdf,.pdf" disabled={busy || uploading}
            onChange={event => { const file = event.target.files?.[0]; if (file) void upload(file); event.target.value = ''; }} />
          <p className="file-help">支援有文字層的 PDF</p>
          <UploadProgress stage={uploadStage} busy={uploading} ready={!!document} name={document?.name} />
          {document && !uploading && <p className="document-meta">{document.chunk_count} Chunks · 可提問</p>}
          {uploading && !busy && uploadEventsUrl && <button className="secondary-button" onClick={() => void reconnectUpload()}>Reconnect upload progress</button>}
          {error && <ErrorState message={error} />}
        </section>
        <section className="document-overview" aria-label="Document Summary" tabIndex={0}>
          <p className="eyebrow">Document Summary</p><h2>文件概覽</h2>
          {document?.document_summary ? <Answer text={document.document_summary} citations={[]} onSource={() => {}} /> :
            <p className="muted">{document ? '此版本尚未提供文件概覽。' : '處理完成後，文件概覽會顯示在這裡。'}</p>}
        </section>
      </aside>
      <div className="reading-workspace">
        <section className="conversation" aria-label="Conversation">
          <div className="section-heading"><p className="eyebrow">02 / Conversation</p><span className="margin-heading">Citation / 來源旁註</span></div>
          {!turns.length && <div className="empty"><h2>{document ? '想從哪個問題開始？' : '先讀文件，再循證據。'}</h2>
            <p>{document ? '提問後，回答與來源會並列呈現。點一下 Citation，即可核對原文。' : '完成上傳後即可提問。回答的 Citation 會放在頁邊，方便一邊閱讀、一邊查證。'}</p></div>}
          {turns.map((turn, i) => <article key={turn.id}>
            <p className="turn-number">Question {String(i + 1).padStart(2, '0')}</p><h2 className="question-heading">{turn.rejected ? '問題過長' : turn.question}</h2>
            <StageIndicator stage={turn.stage} />
            <Answer text={turn.answer} citations={turn.citations} provisional={!turn.final && !turn.error && !turn.rejected}
              unverified={turn.unverified} onSource={showSource} />
            {turn.error && <ErrorState message={turn.error} disabled={busy || uploading}
              onRetry={!turn.rejected && turn.id === turns.at(-1)?.id ? () => void ask(turn.question, turn.id) : undefined} />}
            {(turn.plan || turn.chunks.length > 0 || turn.calls.length > 0 || turn.thinking) && <Trace chunks={turn.chunks}
              calls={turn.calls} plan={turn.plan} thinking={turn.thinking} invalidCitationCount={turn.invalidCitationCount}
              droppedChunkCount={turn.droppedChunkCount} summaryLevel={turn.summaryLevel} />}
          </article>)}
        </section>
        <form className="composer" onSubmit={submit}>
          <label htmlFor="question">你的問題 <span className="label-note">Question</span></label>
          <textarea id="question" rows={3} value={question} onChange={event => setQuestion(event.target.value)}
            aria-describedby={unavailableReason ? 'question-help' : undefined} disabled={!document || busy || uploading}
            placeholder={document ? 'Ask about your Document…' : 'Upload a Document first'} />
          <div className="composer-footer"><p id="question-help" className="muted">{unavailableReason || '回答以文件為依據；點 Citation 查看原文。'}</p>
            <button type="submit" disabled={!document || busy || uploading || !question.trim()}>{busy && document && !uploading ? '回答中…' : '提問 · Ask'}</button></div>
        </form>
      </div>
    </div>
    {sourceOpen && <SourceDialog source={source} kind={sourceKind} loading={sourceLoading}
      error={sourceError} onClose={closeSource} />}
  </main>;
}
