"""Opt-in real Router evaluation with separate canonical and held-out results."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import opencc
import pytest

from chat_document.llm_adapter import OllamaLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.models import ConversationTurn
from chat_document.router import SYSTEM_PROMPT, Router
from chat_document.router_regression import CASES

ROOT = Path(__file__).resolve().parents[2]
TRADITIONAL = opencc.OpenCC("s2t.json")

# Frozen before the first neutral-prompt run. None occur in CASES or the Router prompt.
HELD_OUT = [
    ([], "用一段話說明作者研究的主題、做法與主要結論。", "Global"),
    ([], "I need the big picture of this document before reading it in detail.", "Global"),
    ([], "文中的證據是否足以支持作者的結論？請整合不同章節的發現。", "Synthesis"),
    (
        [],
        "What are the benefits and drawbacks of the approach, based on the evidence presented?",
        "Synthesis",
    ),
    ([], "What value is reported for the measurement shown in Figure 4?", "Lookup"),
    ([], "作者在實驗中設定的樣本總數是多少？", "Lookup"),
    (
        [
            ("user", "How often is Aurora's weather sensor recalibrated?"),
            ("assistant", "Aurora's weather sensor is recalibrated every six months."),
        ],
        "那另一款 Boreal 呢？",
        "Lookup",
    ),
    (
        [
            ("user", "Outline the findings about solar panels."),
            ("assistant", "The document discusses solar-panel performance and maintenance."),
        ],
        "And how does that compare with wind turbines?",
        "Synthesis",
    ),
]
REFERENTS = {
    "R11": (("LightRAG",), ("cost", "成本", "費用", "API", "token", "呼叫")),
    "R12": (("LightRAG",), ("GraphRAG",), ("compar", "versus", "vs", "比較", "比")),
    "H07": (("Boreal",), ("calibrat", "校準", "校正", "標定")),
    "H08": (("solar",), ("wind",), ("compar", "versus", "vs", "differ")),
}


def assess_rewrite(question, has_history, rewritten, referents=()):
    def chinese(text):
        return bool(re.search(r"[\u4e00-\u9fff]", text))

    missing = [
        group
        for group in referents
        if not any(term.casefold() in rewritten.casefold() for term in group)
    ]
    traditional = TRADITIONAL.convert(rewritten)
    script_warning = (
        {"observed": rewritten, "traditional_candidate": traditional}
        if chinese(question) and traditional != rewritten
        else None
    )
    language_preserved = chinese(question) == chinese(rewritten)
    changed = not has_history or rewritten.strip() != question.strip()
    return {
        "passed": not missing and not script_warning and language_preserved and changed,
        "missing_referent_terms": missing,
        "language_preserved": language_preserved,
        "history_rewrite_changed": changed,
        "script_warning": script_warning,
    }


class RecordingOllama(OllamaLLM):
    async def stream(self, request):
        self.raw = ""
        async for frame in super().stream(request):
            self.raw += frame.content
            yield frame


@pytest.mark.eval
async def test_live_router_canonical_and_held_out_cases():
    adapter = RecordingOllama()
    router = Router(LLMGateway(adapter))
    sets = {}
    for name, prefix, cases in (("canonical", "R", CASES), ("held_out", "H", HELD_OUT)):
        results = []
        for index, (history, question, expected) in enumerate(cases, 1):
            case_id = f"{prefix}{index:02}"
            turns = [
                ConversationTurn(question=history[i][1], answer=history[i + 1][1])
                for i in range(0, len(history), 2)
            ]
            calls = []
            plan = await router.plan(question, turns, calls)
            checks = assess_rewrite(
                question, bool(history), plan.standalone_question, REFERENTS.get(case_id, ())
            )
            results.append(
                {
                    "id": case_id,
                    "question": question,
                    "history": history,
                    "expected": expected,
                    "correct": plan.plan_source == "router" and plan.question_type == expected,
                    "rewrite_checks": checks,
                    "plan": plan.model_dump(),
                    "raw": adapter.raw,
                    "calls": [call.model_dump() for call in calls],
                }
            )
        sets[name] = {
            "correct": sum(result["correct"] for result in results),
            "total": len(results),
            "fallbacks": sum(result["plan"]["plan_source"] == "fallback" for result in results),
            "rewrite_failures": sum(not result["rewrite_checks"]["passed"] for result in results),
            "results": results,
        }
    recorded = datetime.now(UTC)
    report = {
        "recorded_at": recorded.isoformat(),
        "model": adapter.model,
        "system_prompt": SYSTEM_PROMPT,
        "sets": sets,
        "script_check": "OpenCC s2t flags conversions; unchanged text is inconclusive.",
    }
    target = ROOT / "eval/reports" / f"router-smoke-{recorded.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x") as output:
        output.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Router smoke report: {target}")
    print(
        {
            name: {key: value for key, value in data.items() if key != "results"}
            for name, data in sets.items()
        }
    )
    assert sets["canonical"]["correct"] >= 10, target
    assert sets["held_out"]["correct"] >= 7, target
    assert all(data["fallbacks"] == 0 for data in sets.values()), target
    assert all(data["rewrite_failures"] == 0 for data in sets.values()), target
