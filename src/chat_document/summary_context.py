"""Select the most detailed complete Summary Tree level within the answer budget."""

from .answer_generator import answer_messages
from .llm_gateway import BUDGET_TABLE, LLMFailure
from .models import Citation, Summary, SummaryTree
from .policy import CONTEXT_EVIDENCE_TOKEN_LIMIT
from .tokens import count_tokens


def summary_context(summaries: list[Summary]) -> str:
    return "\n\n".join(
        f"[S{i}] {s.section} (p.{s.page_start}–{s.page_end})\n{s.text}"
        for i, s in enumerate(summaries, 1)
    )


def select_summary_context(
    tree: SummaryTree, question: str, *, current_question: str
) -> tuple[str, list[Citation], str]:
    levels = [("section", tree.section_summaries)]
    levels.extend((f"group:{i}", level) for i, level in enumerate(tree.group_levels, 1))
    levels.append(("document", [tree.document_summary]))
    for label, summaries in levels:
        context = summary_context(summaries)
        prompt_tokens = sum(
            count_tokens(m["content"])
            for m in answer_messages(question, context, current_question=current_question)
        )
        if (
            count_tokens(context) <= CONTEXT_EVIDENCE_TOKEN_LIMIT
            and prompt_tokens <= BUDGET_TABLE["answer"].prompt_limit
        ):
            return (
                context,
                [
                    Citation(
                        id=f"S{i}",
                        source_id=s.id,
                        section=s.section,
                        page_start=s.page_start,
                        page_end=s.page_end,
                    )
                    for i, s in enumerate(summaries, 1)
                ],
                label,
            )
    raise LLMFailure("No complete Summary Tree level fits the answer Context Budget.")
