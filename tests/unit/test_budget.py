from chat_document.llm_gateway import LLMGateway
from chat_document.tokens import count_tokens
from tests.support import SummaryScriptedLLM as ScriptedLLM


async def test_real_10k_budget_rejects_prompt_one_token_over_answer_cap():
    import pytest

    from chat_document.llm_gateway import BUDGET_TABLE, BudgetExceeded

    llm = ScriptedLLM(["Must not run"])
    gateway = LLMGateway(llm)
    cap = BUDGET_TABLE["answer"].prompt_limit
    prompt = "x " * cap
    assert count_tokens(prompt) == cap + 1
    observed = []
    with pytest.raises(BudgetExceeded):
        async for event in gateway.generate("answer", [{"role": "user", "content": prompt}]):
            observed.append(event)
    assert observed == []  # No delta, final or Trace: the adapter was never called.
    assert llm.ask_calls == []
    # The exact cap remains legal: reserved usage reaches, but never exceeds, 10K.
    accepted = [
        e async for e in gateway.generate("answer", [{"role": "user", "content": prompt.rstrip()}])
    ]
    assert count_tokens(prompt.rstrip()) == cap
    trace = accepted[-1].calls[0]
    assert trace.estimated_prompt_tokens + trace.num_predict == trace.context_budget
