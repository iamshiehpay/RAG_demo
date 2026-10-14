"""The 12 labeled Router cases from spikes/think_level_probe.py, for eval reuse."""

CASES: list[tuple[list[tuple[str, str]], str, str]] = [
    ([], "Summary this document.", "Global"),
    ([], "這篇在講什麼？", "Global"),
    ([], "Give me the key takeaways of this paper.", "Global"),
    ([], "Compare LightRAG with GraphRAG.", "Synthesis"),
    ([], "LightRAG 有什麼限制？", "Synthesis"),
    ([], "How do the experiments support the paper's claims?", "Synthesis"),
    ([], "Performance of ablated versions of LightRAG.", "Lookup"),
    ([], "What datasets were used?", "Lookup"),
    ([], "Table 2 裡 -Origin 在 Mix 的 Overall 是多少？", "Lookup"),
    ([], "How many API calls does LightRAG need for retrieval?", "Lookup"),
    (
        [
            ("user", "What is GraphRAG's retrieval cost in the paper?"),
            (
                "assistant",
                "GraphRAG needs about 610 x 1,000 tokens per retrieval "
                "because it traverses communities.",
            ),
        ],
        "那 LightRAG 呢？",
        "Lookup",
    ),
    (
        [
            ("user", "Summary this document."),
            (
                "assistant",
                "LightRAG is a graph-based RAG system with dual-level retrieval "
                "and incremental updates...",
            ),
        ],
        "那它跟 GraphRAG 比呢？",
        "Synthesis",
    ),
]

# One-based CASES indexes. All groups must occur in a changed Standalone
# Question; terms within each group are alternatives. These are evaluation
# expectations, separate from the Router's implementation.
FOLLOW_UP_STANDALONE_TERMS: dict[int, tuple[tuple[str, ...], ...]] = {
    11: (("LightRAG",), ("retrieval cost", "retrieval costs", "cost of retrieval", "成本")),
    12: (
        ("LightRAG",),
        ("GraphRAG",),
        (
            "compare",
            "comparison",
            "compared",
            "versus",
            "vs",
            "differ",
            "difference",
            "differences",
            "比較",
            "比较",
            "對比",
            "对比",
            "差異",
            "差异",
            "相比",
            "比",
        ),
    ),
}
