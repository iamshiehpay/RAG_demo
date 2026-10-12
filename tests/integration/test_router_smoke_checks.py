import json

import pytest

from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.models import ConversationTurn
from chat_document.router import Router

from .test_router_smoke_eval import assess_answer_script, assess_rewrite


@pytest.mark.parametrize(
    "rewrite,expected_ok,script_warning",
    [
        ("那 LightRAG 呢？", False, False),
        ("LightRAG 的檢索成本是多少？", True, False),
        ("LightRAG 的检索成本是多少？", False, True),
    ],
)
async def test_smoke_checks_history_topic_and_flags_simplified_script(
    rewrite, expected_ok, script_warning
):
    question = "那 LightRAG 呢？"
    history = [
        ConversationTurn(question="What is GraphRAG's retrieval cost?", answer="610k tokens.")
    ]
    script = json.dumps(
        {"question_type": "Lookup", "standalone_question": rewrite, "sub_queries": []}
    )
    plan = await Router(LLMGateway(ScriptedLLM([script]))).plan(question, history, [])
    checks = assess_rewrite(
        question, True, plan.standalone_question, (("LightRAG",), ("cost", "成本", "API"))
    )
    assert checks["passed"] is expected_ok
    assert bool(checks["script_warning"]) is script_warning


@pytest.mark.parametrize(
    "question,answer,warning",
    [
        ("那它的成本呢？", "检索阶段：610 × 1,000 个 token。", True),
        ("那它的成本呢？", "檢索階段：610 × 1,000 個 token。", False),
        ("检索成本是多少？", "检索阶段：610 × 1,000 个 token。", False),
        ("那它的成本呢？", "社群結構的檢索成本。", False),
    ],
)
def test_live_answer_script_check_flags_simplified_answer_to_traditional_question(
    question, answer, warning
):
    assert bool(assess_answer_script(question, answer)) is warning
