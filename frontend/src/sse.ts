import type { Event } from './events';

/** POST-based SSE; the backend event models define the payload union. */
export async function consumeEvents(response: Response, onEvent: (event: Event) => void) {
  if (!response.ok) throw new Error(`Request failed (${response.status}). Please retry.`);
  if (!response.body) throw new Error('Streaming response is unavailable.');
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let terminal = false;
  const dispatch = (frame: string) => {
    const lines = frame.split('\n');
    const data = lines.filter(line => line.startsWith('data:')).map(line => line.slice(5).trimStart()).join('\n');
    if (!data) return;
    const event = JSON.parse(data) as Event;
    const name = lines.find(line => line.startsWith('event:'))?.slice(6).trim();
    if (name && name !== event.type) throw new Error('Inconsistent event response.');
    if (['final', 'ready', 'error'].includes(event.type)) terminal = true;
    onEvent(event);
  };
  try {
    while (true) {
      const { done, value } = await reader.read();
      buffer += done ? decoder.decode() : decoder.decode(value, { stream: true });
      let boundary: number;
      while ((boundary = buffer.indexOf('\n\n')) !== -1) {
        dispatch(buffer.slice(0, boundary));
        buffer = buffer.slice(boundary + 2);
      }
      if (done) break;
    }
    if (buffer.trim() || !terminal) throw new Error('Stream ended before completion. Please retry.');
  } catch (error) {
    await reader.cancel().catch(() => {});
    throw error;
  } finally {
    reader.releaseLock();
  }
}
