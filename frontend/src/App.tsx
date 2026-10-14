import { useCallback, useEffect, useLayoutEffect, useRef, useState, useSyncExternalStore } from 'react';
import type { KeyboardEvent as ReactKeyboardEvent, PointerEvent as ReactPointerEvent } from 'react';
import type { Citation, LLMCallTrace, PlanEvent, ReadyEvent, RetrievedChunk, StageEvent, UnverifiedSpan } from './events';
import { Answer } from './Answer';
import { AnswerProcess } from './AnswerProcess';
import { Composer } from './Composer';
import { DocumentPane } from './DocumentPane';
import { EMBEDDING_MODEL, LLM_MODEL } from './models';
import { consumeEvents } from './sse';
import { ErrorState, StageIndicator } from './Shared';
import type { AskStage } from './Shared';
import { SourcePane } from './SourcePane';
import type { SourceContentData } from './SourcePane';

interface Turn {
  id: number; question: string; answer: string; citations: Citation[];
  chunks: RetrievedChunk[]; calls: LLMCallTrace[]; stage: AskStage; final: boolean; error: string;
  plan: PlanEvent | null; rejected: boolean;
  thinking: string; unverified: UnverifiedSpan[]; invalidCitationCount: number; retrying: boolean;
  droppedChunkCount: number; summaryLevel: string | null;
}
const message = (error: unknown) => error instanceof Error ? error.message : '請求失敗，請重試。';
async function responseMessage(response: Response, fallback: string) {
  const payload = await response.json().catch(() => null) as { detail?: unknown } | null;
  return typeof payload?.detail === 'string' ? payload.detail : fallback;
}

function useMediaQuery(query: string) {
  return useSyncExternalStore(
    notify => { const list = window.matchMedia(query); list.addEventListener('change', notify); return () => list.removeEventListener('change', notify); },
    () => window.matchMedia(query).matches,
    () => false,
  );
}

function useViewportWidth() {
  return useSyncExternalStore(
    notify => { window.addEventListener('resize', notify); return () => window.removeEventListener('resize', notify); },
    () => window.innerWidth,
    () => 1280,
  );
}

// Source pane width (desktop only). The conversation column always keeps at least CHAT_MIN.
const SOURCE_MIN = 260, SOURCE_MAX = 720, SOURCE_DEFAULT = 400, CHAT_MIN = 360, SEPARATOR_WIDTH = 8, RAIL_WIDTH = 64;
const SOURCE_WIDTH_KEY = 'chat-document.source-width';
const leftColumnWidth = (viewport: number, open: boolean) => open ? (viewport >= 1200 ? 280 : 250) : RAIL_WIDTH;
function sourceBounds(viewport: number, leftOpen: boolean) {
  const room = viewport - leftColumnWidth(viewport, leftOpen) - SEPARATOR_WIDTH - CHAT_MIN;
  return { min: SOURCE_MIN, max: Math.max(SOURCE_MIN, Math.min(SOURCE_MAX, room)) };
}
function storedSourceWidth(): number | null {
  try {
    const value = Number(window.localStorage.getItem(SOURCE_WIDTH_KEY));
    return Number.isFinite(value) && value > 0 ? value : null;
  } catch { return null; }
}
function storeSourceWidth(width: number) {
  try { window.localStorage.setItem(SOURCE_WIDTH_KEY, String(Math.round(width))); } catch { /* storage is optional */ }
}

function PaneIcon({ side, open }: { side: 'left' | 'right'; open: boolean }) {
  // The chevron points toward where the pane will go: an open pane collapses toward its own edge.
  const chevron = side === 'left' ? (open ? 'M15 10l-2 2 2 2' : 'M13 10l2 2-2 2') : (open ? 'M9 10l2 2-2 2' : 'M11 10l-2 2 2 2');
  return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
    <rect x="3" y="4" width="18" height="16" rx="2" /><path d={side === 'left' ? 'M9 4v16' : 'M15 4v16'} /><path d={chevron} />
  </svg>;
}

export function App() {
  const [document, setDocument] = useState<ReadyEvent | null>(null);
  const [question, setQuestion] = useState('');
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadName, setUploadName] = useState('');
  const [uploadStage, setUploadStage] = useState<StageEvent | null>(null);
  const [uploadEventsUrl, setUploadEventsUrl] = useState('');
  const [error, setError] = useState('');
  const [source, setSource] = useState<SourceContentData | null>(null);
  const [sourceLoading, setSourceLoading] = useState(false);
  const [sourceError, setSourceError] = useState('');
  const [sourceCitation, setSourceCitation] = useState('');
  const sourceRequest = useRef(0);
  // Wide screens: columns are open or collapsed (null = follow the screen-size default).
  const [leftPref, setLeftPref] = useState<boolean | null>(null);
  const [rightPref, setRightPref] = useState<boolean | null>(null);
  // Narrow screens: at most one overlay at a time, kept apart from the wide-screen choice so a
  // citation click at narrow width never changes the layout the person gets back on a wide screen.
  // undefined = default (Document overlay only while no Document is loaded).
  const [overlay, setOverlay] = useState<'left' | 'right' | null | undefined>(undefined);
  // Preferred source width; the width actually used is always re-clamped to the current window and left column.
  const [sourcePref, setSourcePref] = useState<number | null>(storedSourceWidth);
  const [dragging, setDragging] = useState(false);
  const dragStart = useRef<{ x: number; width: number; last: number } | null>(null);
  const viewport = useViewportWidth();
  const narrow = useMediaQuery('(max-width: 900px)');
  const roomy = useMediaQuery('(min-width: 1200px)');
  const leftOpen = narrow ? (overlay === undefined ? !document : overlay === 'left') : leftPref ?? true;
  const rightOpen = narrow ? overlay === 'right' : rightPref ?? roomy;
  useEffect(() => setOverlay(undefined), [narrow]);
  const bounds = sourceBounds(viewport, leftOpen);
  const sourceWidth = Math.min(bounds.max, Math.max(bounds.min, sourcePref ?? SOURCE_DEFAULT));
  const resizeSource = (width: number) => setSourcePref(Math.min(bounds.max, Math.max(bounds.min, Math.round(width))));
  function startDrag(event: ReactPointerEvent<HTMLDivElement>) {
    if (event.button !== 0) return;
    event.currentTarget.setPointerCapture(event.pointerId);
    dragStart.current = { x: event.clientX, width: sourceWidth, last: sourceWidth };
    setDragging(true);
    event.preventDefault();
  }
  function moveDrag(event: ReactPointerEvent<HTMLDivElement>) {
    const start = dragStart.current;
    if (!start) return;
    start.last = Math.min(bounds.max, Math.max(bounds.min, Math.round(start.width + (start.x - event.clientX))));
    setSourcePref(start.last);
  }
  // Pointer release, pointercancel and losing capture (released outside the window) all end the drag the same way.
  function endDrag() {
    const start = dragStart.current;
    if (!start) return;
    dragStart.current = null;
    setDragging(false);
    storeSourceWidth(start.last);
  }
  function separatorKey(event: ReactKeyboardEvent<HTMLDivElement>) {
    const step = event.shiftKey ? 64 : 16;
    const next = event.key === 'ArrowLeft' ? sourceWidth + step : event.key === 'ArrowRight' ? sourceWidth - step
      : event.key === 'Home' ? bounds.min : event.key === 'End' ? bounds.max : null;
    if (next === null) return;
    event.preventDefault();
    resizeSource(next);
    storeSourceWidth(Math.min(bounds.max, Math.max(bounds.min, next)));
  }
  const setLeft = (open: boolean) => narrow ? setOverlay(open ? 'left' : null) : setLeftPref(open);
  const setRight = (open: boolean) => narrow ? setOverlay(open ? 'right' : null) : setRightPref(open);
  // Focus handling for the Source overlay: heading on open, the clicked Citation on close.
  const returnFocus = useRef<HTMLElement | null>(null);
  const sourceHeading = useRef<HTMLDivElement>(null);
  const leftToggle = useRef<HTMLButtonElement>(null);
  const [sourceOpenTick, setSourceOpenTick] = useState(0);
  useEffect(() => { if (sourceOpenTick && narrow) sourceHeading.current?.focus(); }, [sourceOpenTick, narrow]);
  function closeRight() {
    setRight(false);
    if (narrow) { const target = returnFocus.current; if (target?.isConnected) target.focus(); }
  }
  function closeLeft() { setLeft(false); if (narrow) leftToggle.current?.focus(); }
  // Escape closes whichever overlay is open (narrow screens only).
  useEffect(() => {
    if (!narrow) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      if (rightOpen) closeRight(); else if (leftOpen && overlay !== undefined) closeLeft();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const clearSource = useCallback(() => {
    sourceRequest.current++;
    setSource(null); setSourceError(''); setSourceLoading(false); setSourceCitation('');
  }, []);
  const updateTurn = (id: number, update: (turn: Turn) => Turn) => setTurns(previous => previous.map(
    turn => turn.id === id ? update(turn) : turn,
  ));

  // The conversation scrolls on its own; follow new content unless the person scrolled up.
  const scroller = useRef<HTMLDivElement>(null);
  const following = useRef(true);
  const onScroll = () => {
    const element = scroller.current;
    if (element) following.current = element.scrollHeight - element.scrollTop - element.clientHeight < 120;
  };
  useLayoutEffect(() => {
    const element = scroller.current;
    if (element && following.current) element.scrollTop = element.scrollHeight;
  }, [turns]);

  async function upload(file: File) {
    clearSource(); setUploadName(file.name); setBusy(true); setUploading(true); setUploadStage(null); setUploadEventsUrl(''); setError('');
    const form = new FormData(); form.append('document', file);
    let eventsUrl = '';
    try {
      const response = await fetch('/api/documents', { method: 'POST', body: form });
      if (!response.ok) throw new Error(await responseMessage(response,
        `上傳失敗（${response.status}），請重試。`));
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
        setDocument(null); setTurns([]); setQuestion(''); clearSource();
      }
      throw new Error(`${await responseMessage(response, '無法取得上傳進度。')} 請重新選擇 PDF。`);
    }
    await consumeEvents(response, event => {
      if (event.type === 'stage') setUploadStage(event);
      else if (event.type === 'ready') {
        setDocument(event); setTurns([]); clearSource(); setQuestion(''); setError('');
        setUploading(false); setUploadEventsUrl(''); setOverlay(undefined);
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

  // Set synchronously so a fast double click (or Enter plus a click) can never send the same ask twice.
  const asking = useRef(false);
  async function ask(askedQuestion: string, retryId?: number, keepDraft = false) {
    if (!askedQuestion.trim() || !document || busy || uploading || asking.current) return;
    if (retryId !== undefined && turns.at(-1)?.id !== retryId) return;
    asking.current = true;
    const id = retryId ?? Date.now();
    following.current = true;
    setBusy(true); setError(''); if (!keepDraft) setQuestion('');
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
    } finally { asking.current = false; setBusy(false); }
  }

  const showSource = useCallback(async (citation: Citation) => {
    const request = ++sourceRequest.current;
    setSource(null); setSourceError(''); setSourceLoading(true); setSourceCitation(citation.id);
    if (narrow) setOverlay('right'); else setRightPref(true);
    returnFocus.current = globalThis.document.activeElement instanceof HTMLElement ? globalThis.document.activeElement : null;
    setSourceOpenTick(tick => tick + 1);
    try {
      const response = await fetch(`/api/sources/${encodeURIComponent(citation.source_id)}`);
      if (!response.ok) throw new Error(response.status === 404 ? '找不到這段來源。' : '無法載入來源，請再點一次。');
      const content = await response.json() as SourceContentData;
      if (request === sourceRequest.current) setSource(content);
    } catch (error) {
      if (request === sourceRequest.current) setSourceError(message(error));
    } finally {
      if (request === sourceRequest.current) setSourceLoading(false);
    }
  }, [narrow]);

  const unavailableReason = uploading ? '文件處理中，完成後即可提問。' : !document ? '請先在「文件」欄上傳有文字層的 PDF，完成後即可提問。' : busy ? '回答產生中，請稍候。' : 'Enter 送出，Shift+Enter 換行';
  const placeholder = uploading ? '文件處理中…' : !document ? '上傳文件後即可提問' : busy ? '回答產生中…' : '輸入問題';
  const disabled = !document || busy || uploading;
  const status = uploading ? '處理中' : document ? '可提問' : '尚未上傳';

  return <div className="app">
    <header className="app-header">
      <div className="header-title">
        <h1>與文件對話</h1>
        <span className="eyebrow">Chat with Document</span>
        <span className="header-status" role="status">{document ? `${document.name} · ${status}` : status}</span>
      </div>
      <div className="header-right">
        <span className="header-models">回答模型 {LLM_MODEL} · 檢索模型 {EMBEDDING_MODEL}</span>
        <div className="header-toggles">
          <button className="secondary-button" aria-expanded={leftOpen} ref={leftToggle} onClick={() => setLeft(!leftOpen)}>文件</button>
          <button className="secondary-button" aria-expanded={rightOpen} onClick={() => rightOpen ? closeRight() : setRight(true)}>來源</button>
        </div>
      </div>
    </header>
    <div className={`workspace${dragging ? ' resizing' : ''}`} style={{ '--source-width': `${sourceWidth}px` } as React.CSSProperties}>
      {leftOpen ? <aside className="pane pane-left" aria-label="文件" data-open="true">
        <div className="pane-head"><span className="label">文件</span>
          <button className="icon-button" aria-label="收合文件欄" onClick={closeLeft}><PaneIcon side="left" open /></button></div>
        <DocumentPane document={document} uploadName={uploadName} uploading={uploading} busy={busy} uploadStage={uploadStage}
          canReconnect={uploading && !busy && !!uploadEventsUrl} error={error}
          onUpload={file => void upload(file)} onReconnect={() => void reconnectUpload()} />
      </aside> : <aside className="rail rail-left" aria-label="文件（已收合）" data-open="false">
        <button className="rail-button" aria-label="展開文件欄" onClick={() => setLeft(true)}><PaneIcon side="left" open={false} /><span className="rail-label" aria-hidden="true">文件</span></button>
      </aside>}

      <main className="chat">
        <div className="messages" ref={scroller} onScroll={onScroll} role="region" aria-label="對話">
          <div className="messages-inner">
            {!turns.length && <div className="empty"><h2>{document ? '想從哪個問題開始？' : '先上傳文件，再提問。'}</h2>
              <p>{document ? '提問後，回答裡的來源編號可以點開，在右側核對原文。' : '在左側「文件」欄選擇一份有文字層的 PDF，處理完成後即可提問。'}</p>
              {!document && !leftOpen && <button className="secondary-button" onClick={() => setLeft(true)}>開啟「文件」欄</button>}</div>}
            {turns.map(turn => <article className="turn" key={turn.id}>
              <div className="user-bubble">{turn.rejected ? '問題過長（未送出）' : turn.question}</div>
              <div className="assistant">
                <StageIndicator stage={turn.stage} />
                <Answer text={turn.answer} citations={turn.citations} provisional={!turn.final && !turn.error && !turn.rejected}
                  unverified={turn.unverified} onSource={showSource} />
                {turn.error && <ErrorState message={turn.error} disabled={busy || uploading}
                  onRetry={!turn.rejected && turn.id === turns.at(-1)?.id ? () => void ask(turn.question, turn.id) : undefined} />}
                {(turn.plan || turn.chunks.length > 0 || turn.calls.length > 0 || turn.thinking) && <AnswerProcess chunks={turn.chunks}
                  calls={turn.calls} plan={turn.plan} thinking={turn.thinking} invalidCitationCount={turn.invalidCitationCount}
                  droppedChunkCount={turn.droppedChunkCount} summaryLevel={turn.summaryLevel} />}
              </div>
            </article>)}
          </div>
        </div>
        <Composer value={question} onChange={setQuestion} onSubmit={() => void ask(question)} disabled={disabled}
          canSubmit={!disabled && !!question.trim()} busy={busy} help={unavailableReason} placeholder={placeholder}
          documentName={document?.name} onShortcut={text => void ask(text, undefined, true)} />
      </main>

      {rightOpen && !narrow && <div className="pane-resizer" role="separator" aria-orientation="vertical" aria-label="調整來源欄寬度"
        aria-valuenow={sourceWidth} aria-valuemin={bounds.min} aria-valuemax={bounds.max} tabIndex={0}
        data-dragging={dragging || undefined} onPointerDown={startDrag} onPointerMove={moveDrag}
        onPointerUp={endDrag} onPointerCancel={endDrag} onLostPointerCapture={endDrag} onKeyDown={separatorKey} />}
      {rightOpen ? <aside className="pane pane-right" aria-label="來源" data-open="true">
        <div className="pane-head"><span className="label">來源</span>
          <button className="icon-button" aria-label="收合來源欄" onClick={closeRight}><PaneIcon side="right" open /></button></div>
        <SourcePane source={source} citationId={sourceCitation} loading={sourceLoading} error={sourceError} headingRef={sourceHeading} />
      </aside> : <aside className="rail rail-right" aria-label="來源（已收合）" data-open="false">
        <button className="rail-button" aria-label="展開來源欄" onClick={() => setRight(true)}><PaneIcon side="right" open={false} /><span className="rail-label" aria-hidden="true">來源</span></button>
      </aside>}
    </div>
  </div>;
}
