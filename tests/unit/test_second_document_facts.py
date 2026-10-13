"""The subset context cannot disappear from an affirmative judge excerpt."""

import json

from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway
from eval.checks import check_fact
from eval.second_document import SECOND_DOCUMENT_CASES


async def test_numeric_expert_fact_rejects_an_excerpt_without_the_declared_paper_subset():
    answer = (
        "All accuracy is 0.966, N=447, and positive-class F1 is 0.762. "
        "InfoFound accuracy is 0.951 (lower), N=304, and F1 remains 0.762."
    )
    judged = json.dumps({"matched": True, "asserted": True, "evidence": answer})
    fact = SECOND_DOCUMENT_CASES[0].facts[0]
    gateway = LLMGateway(ScriptedLLM([judged]))
    assert not (await check_fact(answer, fact, gateway)).passed


async def test_numeric_expert_fact_accepts_complete_verbatim_context_with_correct_bindings():
    answer = (
        "Three expert-annotated papers supplied the criterion-level evaluations. "
        "All accuracy is 0.966, N=447, and positive-class F1 is 0.762. "
        "InfoFound accuracy is 0.951 (lower), N=304, and F1 remains 0.762."
    )
    judged = json.dumps({"matched": True, "asserted": True, "evidence": answer})
    fact = SECOND_DOCUMENT_CASES[0].facts[0]
    gateway = LLMGateway(ScriptedLLM([judged]))
    assert (await check_fact(answer, fact, gateway)).passed
