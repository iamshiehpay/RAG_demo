"""Focused regressions grouped by feature; helpers remain outside test modules."""

import json
from pathlib import Path

import pytest

from app.llm_gateway import LLMGateway
from app.models import ConversationTurn
from app.router import Router
from eval.fakes import ScriptedLLM
from eval.router_checks import assess_answer_script, assess_rewrite

RAW_PROBES = json.loads((Path(__file__).parents[1] / "data/router_qa_raw.json").read_text())


@pytest.mark.parametrize("case", RAW_PROBES, ids=lambda case: f"{case['source']}:{case['line']}")
async def test_exact_live_qa_raw_outputs_preserve_classification(case):
    calls = []
    plan = await Router(LLMGateway(ScriptedLLM([case["raw"]]))).plan(case["question"], [], calls)
    assert plan.question_type == case["expected"]
    assert plan.standalone_question == case["question"]
    assert plan.plan_source == "router" and plan.fallback_reason is None
    assert calls[0].plan_source == "router"


async def test_known_extra_key_with_valid_follow_up_rewrite_is_ignored():
    raw = json.dumps(
        {
            "question_type": "Synthesis",
            "standalone_question": "Compare LightRAG with GraphRAG.",
            "sub_queries": ["cost", "updates"],
            "answer_format": "Chinese",
            "answer": None,
        }
    )
    history = [ConversationTurn(question="Summarize LightRAG.", answer="LightRAG is a RAG system.")]
    plan = await Router(LLMGateway(ScriptedLLM([raw]))).plan("那它跟 GraphRAG 比呢？", history, [])
    assert plan.plan_source == "router"
    assert plan.standalone_question == "那它跟 GraphRAG 比呢？"
    assert plan.rewrite_language_mismatch
    assert plan.router_standalone_question == "Compare LightRAG with GraphRAG."


@pytest.mark.parametrize(
    "raw,history,expected_source,reason",
    [
        ('{"type":"Synthesis","sub_queries":["cost","updates"],"answer":null}', [], "router", None),
        ('{"question_type":"Lookup","sub_queries":[]}', [], "router", None),
        ('{"type":"Global","sub_queries":[]}', [], "router", None),
        ('{"question_type":"Lookup","sub_queries":[],"answer":null}', [], "router", None),
        (
            '{"type":"Lookup","sub_queries":[]}',
            [ConversationTurn(question="What is GraphRAG?", answer="A retrieval system.")],
            "fallback",
            "missing_rewrite",
        ),
        ('{"answer":"unknown","sub_queries":[]}', [], "fallback", "invalid_plan"),
        (
            '{"question_type":"Synthesis","sub_queries":[],"answer_format":"Chinese"}',
            [ConversationTurn(question="Summarize LightRAG.", answer="LightRAG is a RAG system.")],
            "fallback",
            "missing_rewrite",
        ),
        ("not JSON", [], "fallback", "invalid_json"),
    ],
)
async def test_near_miss_router_shapes_record_plan_origin(raw, history, expected_source, reason):
    llm = ScriptedLLM([raw])
    calls = []
    plan = await Router(LLMGateway(llm)).plan("Compare costs.", history, calls)
    assert plan.plan_source == expected_source
    assert plan.fallback_reason == reason
    assert calls[0].plan_source == expected_source
    assert calls[0].fallback_reason == reason
    assert plan.standalone_question == "Compare costs."
    assert llm.calls[0].think == "low" and llm.calls[0].num_predict == 600
    prompt = llm.calls[0].messages[0]["content"]
    assert '"question_type"' in prompt and '"standalone_question"' in prompt
    assert '"sub_queries"' in prompt


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
