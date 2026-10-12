"""Opt-in real gpt-oss Router smoke; saves raw outputs and token traces before asserting."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import pytest

from chat_document.llm_adapter import OllamaLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.models import ConversationTurn
from chat_document.router import Router
from chat_document.router_regression import CASES


class RecordingOllama(OllamaLLM):
    async def stream(self, request):
        self.raw = ""
        async for frame in super().stream(request):
            self.raw += frame.content
            yield frame


@pytest.mark.eval
async def test_live_router_twelve_labelled_cases():
    adapter = RecordingOllama()
    router = Router(LLMGateway(adapter))
    results = []
    for history, question, expected in CASES:
        turns = [
            ConversationTurn(question=history[i][1], answer=history[i + 1][1])
            for i in range(0, len(history), 2)
        ]
        calls = []
        plan = await router.plan(question, turns, calls)
        results.append(
            {
                "question": question,
                "history": history,
                "expected": expected,
                "correct": plan.plan_source == "router" and plan.question_type == expected,
                "plan": plan.model_dump(),
                "raw": adapter.raw,
                "calls": [call.model_dump() for call in calls],
            }
        )
    correct = sum(result["correct"] for result in results)
    parse_fallbacks = [
        result
        for result in results
        if result["plan"]["fallback_reason"] in {"invalid_json", "invalid_plan", "missing_rewrite"}
    ]
    report = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "model": adapter.model,
        "correct": correct,
        "total": len(results),
        "parse_fallbacks": len(parse_fallbacks),
        "results": results,
    }
    target = Path("docs/qa/t06/live-router-smoke.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    assert not parse_fallbacks, f"Parse fallbacks: {parse_fallbacks}"
    assert correct >= 10, f"Router accuracy {correct}/{len(results)}; see {target}"
    assert all(result["plan"]["plan_source"] == "router" for result in results), results

    def has_chinese(text):
        return bool(re.search(r"[\u4e00-\u9fff]", text))

    for result in results:
        assert has_chinese(result["question"]) == has_chinese(
            result["plan"]["standalone_question"]
        ), result
        if result["history"]:
            rewritten = result["plan"]["standalone_question"]
            assert "LightRAG" in rewritten and "它" not in rewritten, result
