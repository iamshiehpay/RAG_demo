"""Public-path presentation regressions; scripted output does not prove semantics.

Actual refusal/claim support is checked by the retained D21 live feedback loop.
"""

import json

import numpy as np

from chat_document.application import Application
from chat_document.index import Index
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from chat_document.models import Chunk, Document


class LocalEmbedder:
    async def embed(self, texts):
        return np.asarray([[1.0] for _ in texts], dtype=np.float32)


async def test_public_ask_keeps_distinct_paragraphs_with_same_citation_and_verbatim_table():
    question = "What constraints are stated?"
    llm = ScriptedLLM([
        json.dumps({"question_type": "Synthesis", "standalone_question": question,
                    "sub_queries": []}),
        "The input component may introduce noise under the stated condition. [C1]",
    ])
    chunks = [
        Chunk(id="prose", section_id="s", section="Analysis", page_start=2, page_end=3,
              text="A removed component was studied.\n\nThe input component may introduce noise.",
              order=0),
        Chunk(id="table", section_id="s", section="Analysis", page_start=3, page_end=3,
              text="Table caption\n\nHeader | Value\nControl | 7", order=1, kind="table"),
    ]
    app = Application(LocalEmbedder(), LLMGateway(llm))
    app.document = Document(id="d", name="authored fixture", sections=[], chunks=chunks)
    app.index = Index(chunks, np.ones((2, 1), dtype=np.float32), app.embedder)
    events = [e async for e in app.ask(question)]
    final = next(e for e in events if e.type == "final")
    assert final.answer.endswith("[C1]") and final.unverified == []
    assert app.source(final.citations[0].source_id).text == chunks[0].text
    answer_context = llm.calls[-1].messages[-1]["content"]
    assert (
        "[C1] Analysis (p.2)\nA removed component was studied.\n\n"
        "[C1] Analysis (p.2)\nThe input component may introduce noise."
    ) in answer_context
    assert "[C2] Analysis (p.3)\nTable caption\n\nHeader | Value\nControl | 7" in answer_context
    assert answer_context.count("[C2]") == 1
    assert [c.call_type for c in events[-1].calls] == ["router", "answer"]
    assert all(c.estimated_prompt_tokens + c.num_predict <= 10000 for c in events[-1].calls)
