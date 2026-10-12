import json, time, urllib.request

def chat(payload):
    req = urllib.request.Request("http://localhost:11434/api/chat", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    t = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=180))
    return r, time.time() - t

filler = "The quick brown fox jumps over the lazy dog. " * 400  # ~4K tokens
base = {"model": "gpt-oss:120b-cloud", "stream": False}

# 1) normal call: token accounting + thinking
r, dt = chat({**base, "messages": [{"role": "user", "content": "In one sentence, what is RAG?"}], "think": "low"})
print("[1] think=low", f"{dt:.1f}s", "prompt_eval_count=", r.get("prompt_eval_count"), "eval_count=", r.get("eval_count"),
      "thinking_len=", len(r["message"].get("thinking") or ""), "| content:", r["message"]["content"][:150])

# 2) num_predict cap with thinking
r, dt = chat({**base, "messages": [{"role": "user", "content": "Explain retrieval augmented generation in detail."}], "think": "high", "options": {"num_predict": 200}})
print("[2] think=high num_predict=200", f"{dt:.1f}s", "eval_count=", r.get("eval_count"), "done_reason=", r.get("done_reason"),
      "thinking_len=", len(r["message"].get("thinking") or ""), "content_len=", len(r["message"]["content"]))

# 3) does num_ctx truncate on cloud?
r, dt = chat({**base, "messages": [{"role": "user", "content": filler + "\nHow many times does 'fox' appear above? Just a rough guess."}], "think": "low", "options": {"num_ctx": 1024}})
print("[3] ~4K prompt with num_ctx=1024", f"{dt:.1f}s", "prompt_eval_count=", r.get("prompt_eval_count"), "| content:", r["message"]["content"][:120])
