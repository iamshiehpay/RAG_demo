import json

import numpy as np
import pytest

from chat_document.application import Application
from chat_document.context_packer import ContextPacker
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.models import Chunk, ConversationTurn
from chat_document.router import Router
from chat_document.settings import RetrievalSettings

from .fixtures import text_pdf


@pytest.mark.parametrize(
    "question,rewrite",
    [
        ("How do the ablated versions perform?", "消融版本的性能如何？"),
        ("消融版本的表現如何？", "How do the ablated versions perform?"),
    ],
)
async def test_cross_language_rewrite_keeps_type_and_records_original_without_reasking(
    question, rewrite
):
    llm = ScriptedLLM(
        [json.dumps(dict(question_type="Synthesis", standalone_question=rewrite, sub_queries=[]))]
    )
    calls = []
    plan = await Router(LLMGateway(llm)).plan(
        question, [ConversationTurn(question="成本如何？", answer="文件中未提及")], calls
    )
    assert plan.question_type == "Synthesis" and plan.plan_source == "router"
    assert plan.standalone_question == question
    assert plan.rewrite_language_mismatch is True
    assert plan.router_standalone_question == rewrite
    assert calls[0].rewrite_language_mismatch is True
    assert calls[0].router_standalone_question == rewrite
    assert len(llm.calls) == 1


class FixedEmbedder:
    async def embed(self, texts):
        return np.ones((len(texts), 2), dtype=np.float32) / np.sqrt(2)


async def test_english_current_question_after_chinese_history_controls_answer_language():
    question = "Performance of ablated versions of LightRAG"
    llm = ScriptedLLM(
        [
            json.dumps(
                dict(
                    question_type="Synthesis",
                    standalone_question="LightRAG 的消融版本的性能如何？",
                    sub_queries=["LightRAG ablation"],
                )
            ),
            "Not mentioned in the document.",
        ]
    )
    app = Application(FixedEmbedder(), LLMGateway(llm))
    assert [e async for e in app.upload_document(text_pdf(), "sample.pdf")][-1].type == "ready"
    events = [
        e
        async for e in app.ask(
            question, history=[ConversationTurn(question="它的成本呢？", answer="文件中未提及")]
        )
    ]
    assert events[0].standalone_question == question
    assert events[0].rewrite_language_mismatch
    messages = llm.calls[-1].messages
    assert "CURRENT USER QUESTION controls the answer language" in messages[0]["content"]
    assert f"Current user question (language reference): {question}" in messages[-1]["content"]
    assert len(llm.calls) == 2
    assert events[-1].calls[0].rewrite_language_mismatch
    assert any(e.type == "final" for e in events)


def test_context_capacity_counts_current_question_language_reference():
    packer = ContextPacker(LLMGateway(ScriptedLLM([])), RetrievalSettings())
    chunk = Chunk(
        id="c",
        section_id="s",
        section="Results",
        page_start=1,
        page_end=1,
        text="evidence " * 5800,
        order=0,
    )
    assert packer.fits("Short rewritten question", [chunk])
    assert not packer.fits("Short rewritten question", [chunk], current_question="question " * 950)
