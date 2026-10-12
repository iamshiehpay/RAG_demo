"""LightRAG Golden Facts from AGENTS.md and the fixed test Document.

Numbers use judge checks with model/variant, dataset, metric, value and direction.
Source locations are requirements context, not substring acceptance criteria.
"""

from chat_document.policy import FIXED_REFUSALS

from .models import EvaluationCase, GoldenFact, NumericBinding


def semantic(id: str, requirement: str) -> GoldenFact:
    return GoldenFact(id, "judge", requirement)


MIX_LOW = GoldenFact(
    "mix_low_overall",
    "judge",
    "Table 2 (p.8): on Mix, -Low Overall win rate against NaiveRAG is 64.8%, "
    "higher than full LightRAG's 60.0%; correctly assigns values and comparison direction.",
    (
        ("Mix", "混合"),
        ("-Low",),
        ("Overall", "整體", "總體"),
        ("64.8%",),
        ("LightRAG", "完整版"),
        ("60.0%",),
    ),
    value_bindings=(
        NumericBinding(("-Low",), "64.8%"),
        NumericBinding(("LightRAG", "完整版"), "60.0%"),
    ),
)
AGRICULTURE_ORIGIN = GoldenFact(
    "agriculture_origin_overall",
    "judge",
    "Table 2 (p.8): on Agriculture, -Origin Overall win rate against NaiveRAG is 74.4%, "
    "higher than full LightRAG's 67.6%; correctly assigns values and comparison direction.",
    (
        ("Agriculture", "農業"),
        ("-Origin",),
        ("Overall", "整體", "總體"),
        ("74.4%",),
        ("LightRAG", "完整版"),
        ("67.6%",),
    ),
    value_bindings=(
        NumericBinding(("-Origin",), "74.4%"),
        NumericBinding(("LightRAG", "完整版"), "67.6%"),
    ),
)
NOT_ALL_BEST = GoldenFact(
    "not_all_best",
    "forbidden",
    "Full LightRAG is best on every dataset and every metric (not merely balanced or often "
    "better).",
)
COST = GoldenFact(
    "retrieval_cost",
    "judge",
    "Section 4.5 (p.9-10), Legal retrieval: GraphRAG uses about 610 x 1,000 tokens "
    "(610,000 tokens), whereas LightRAG uses fewer than 100 tokens and only one API call. "
    "This concerns retrieval, not total indexing cost; LightRAG's retrieval cost is lower.",
    (("GraphRAG",), ("LightRAG",), ("610",), ("100",), ("API",)),
)


def table1_fact(dataset: str, aliases: tuple[str, ...], light: str, graph: str) -> GoldenFact:
    direction = "lower" if dataset == "Mix" else "higher"
    return GoldenFact(
        f"table1_{dataset.lower()}_overall",
        "judge",
        f"Table 1 (p.7): on {dataset}, Overall win rate for LightRAG is {light}, "
        f"{direction} than GraphRAG's {graph}. "
        "Values, comparison baseline and direction are correct.",
        (aliases, ("Overall", "整體", "總體"), ("LightRAG",), (light,), ("GraphRAG",), (graph,)),
        value_bindings=(NumericBinding(("LightRAG",), light), NumericBinding(("GraphRAG",), graph)),
    )


TABLE1_FACTS = (
    table1_fact("Agriculture", ("Agriculture", "農業"), "54.8%", "45.2%"),
    table1_fact("CS", ("CS", "電腦", "計算機"), "52.0%", "48.0%"),
    table1_fact("Legal", ("Legal", "法律"), "52.8%", "47.2%"),
    table1_fact("Mix", ("Mix", "混合"), "49.6%", "50.4%"),
)

LIGHTRAG_CASES = (
    EvaluationCase(
        "Q1",
        "Summary this document.",
        (
            semantic(
                "motivation",
                "p.1-2: flat RAG loses contextual interdependencies, motivating LightRAG.",
            ),
            semantic(
                "graph_indexing",
                "Section 3.1: graph-based indexing extracts entities and relationships.",
            ),
            semantic(
                "dual_level",
                "Section 3.2: dual-level retrieval combines specific entities and broader topics.",
            ),
            semantic(
                "incremental_update",
                "Section 3.1/4.5: incremental updates integrate new graph data without "
                "rebuilding the entire index.",
            ),
            semantic(
                "experiments",
                "Section 4: evaluation on Agriculture, CS, Legal and Mix compares baselines "
                "and shows stronger answer quality, especially diversity.",
            ),
            NOT_ALL_BEST,
            semantic(
                "conclusion",
                "Section 6: conclusion combines effective, efficient graph-based retrieval "
                "with adaptability.",
            ),
        ),
        "Global",
    ),
    EvaluationCase(
        "Q2",
        "Compare LightRAG with GraphRAG.",
        (
            semantic(
                "retrieval_methods",
                "Section 3.2/4.1: GraphRAG traverses communities, LightRAG retrieves with "
                "dual-level keywords (entities and topics).",
            ),
            COST,
            semantic(
                "incremental_update",
                "Section 4.5: GraphRAG rebuilds communities on new text; LightRAG "
                "incrementally updates its graph without rebuilding everything.",
            ),
            *TABLE1_FACTS,
            semantic(
                "table3_case_study",
                "Table 3 / Section 4.4 (p.8-9): case study LLM judge favors LightRAG on "
                "comprehensiveness, diversity, empowerment and overall.",
            ),
            GoldenFact(
                "not_all_datasets",
                "forbidden",
                "LightRAG beats GraphRAG on all datasets (a universal assertion, not a "
                "negation or a qualified often-better statement).",
            ),
        ),
        "Synthesis",
    ),
    EvaluationCase(
        "Q3",
        "Performance of ablated versions of LightRAG.",
        (
            GoldenFact("high_term", "contains", "-High"),
            GoldenFact("low_term", "contains", "-Low"),
            GoldenFact("origin_term", "contains", "-Origin"),
            semantic(
                "table2_baseline",
                "Table 2 (p.8): establishes NaiveRAG versus each variant win rates, not "
                "win/loss or full-LightRAG-versus-variant scores.",
            ),
            semantic(
                "ablation_meaning",
                "Section 4.3: -High removes high-level retrieval, -Low removes low-level "
                "retrieval, -Origin removes original text; full LightRAG combines both "
                "retrieval levels.",
            ),
            MIX_LOW,
            AGRICULTURE_ORIGIN,
            NOT_ALL_BEST,
        ),
        "Lookup",
        required_citation_page=8,
        required_citation_term="Table 2",
    ),
    EvaluationCase(
        "ZH_COST",
        "LightRAG 和 GraphRAG 的檢索成本差異是什麼？",
        (
            GoldenFact(
                "chinese_answer",
                "judge",
                "Answer is in Chinese (English proper nouns, units and Citations may "
                "remain), not primarily English.",
                answer_property=True,
            ),
            COST,
            semantic(
                "numbers_unchanged",
                "The Chinese answer preserves source numeric quantities: GraphRAG 610 × "
                "1,000 tokens (610,000 also acceptable), LightRAG < 100 tokens, one API "
                "call. Does not rescale, round away, swap models or change the units.",
            ),
        ),
        "Synthesis",
    ),
    EvaluationCase(
        "LIMITATIONS",
        "這篇論文有什麼限制？",
        (
            semantic(
                "evaluation_limit",
                "Section 4.1 (p.6): reliable ground truth for complex high-level RAG "
                "questions is difficult; evaluation uses LLM-based multi-dimensional "
                "comparisons instead.",
            ),
            semantic(
                "retrieval_tradeoff",
                "Section 4.3 (p.8): low-level-only (-High) struggles with broad complex "
                "context; high-level-only (-Low) loses entity detail. Identifies these as "
                "ablation trade-offs, not measured failure of full LightRAG.",
            ),
            semantic(
                "not_universally_best",
                "Sections 4.2/4.3: results do not show universal superiority; recognizes a "
                "specific measured exception to full-LightRAG or GraphRAG comparisons.",
            ),
            GoldenFact(
                "no_invented_limit",
                "forbidden",
                "The document explicitly reports LightRAG's privacy violations, proprietary "
                "license restrictions or a measured HotpotQA failure (none is in this "
                "document).",
            ),
        ),
        "Synthesis",
        minimum_citation_sections=2,
    ),
    EvaluationCase(
        "ABSENT_HOTPOT",
        "LightRAG 在 HotpotQA 上的分數是多少？",
        (
            GoldenFact(
                "fixed_reply",
                "judge",
                "Only the Chinese fixed refusal, with no invented content.",
                exact_answer=FIXED_REFUSALS["zh"],
            ),
        ),
        "Lookup",
    ),
    EvaluationCase(
        "ABSENT_LICENSE",
        "What are LightRAG's license terms?",
        (
            GoldenFact(
                "fixed_reply",
                "judge",
                "Only the English fixed refusal, with no invented content.",
                exact_answer=FIXED_REFUSALS["en"],
            ),
        ),
        "Lookup",
    ),
    EvaluationCase(
        "ABSENT_GPU",
        "訓練 LightRAG 使用了多少 GPU 小時？",
        (
            GoldenFact(
                "fixed_reply",
                "judge",
                "Only the Chinese fixed refusal, with no invented content.",
                exact_answer=FIXED_REFUSALS["zh"],
            ),
        ),
        "Lookup",
    ),
)


LIGHTRAG_CASES += (
    EvaluationCase(
        "Q1_ZH_THREE_SENTENCES",
        "用三句話、中文總結這份文件",
        LIGHTRAG_CASES[0].facts
        + (
            GoldenFact(
                "chinese_summary",
                "judge",
                "The entire answer is in Chinese, allowing English proper nouns and Citations.",
                answer_property=True,
            ),
            GoldenFact(
                "three_sentences",
                "judge",
                "The answer contains exactly three complete sentences, no extra headings, "
                "introductory sentence or closing sentence. Citation markers are not sentences.",
                answer_property=True,
            ),
        ),
        "Global",
    ),
)


def router_cases() -> tuple[EvaluationCase, ...]:
    from chat_document.router_regression import CASES, FOLLOW_UP_STANDALONE_TERMS

    return tuple(
        EvaluationCase(
            f"ROUTER_{index:02}",
            question,
            expected_question_type=expected,
            history=tuple(history),
            standalone_terms=FOLLOW_UP_STANDALONE_TERMS.get(index, ()),
        )
        for index, (history, question, expected) in enumerate(CASES, 1)
    )
