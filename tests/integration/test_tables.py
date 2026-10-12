"""Table Chunk behavior through upload/ask, with real local bge-m3."""

from pathlib import Path

from chat_document.application import Application
from chat_document.embedder import OllamaEmbedder
from chat_document.llm_adapter import ScriptedLLM
from chat_document.llm_gateway import LLMGateway

# Transcribed from the fixed LightRAG Table 2, in printed row/column order.
TABLE2_VALUES = [
    ["32.4", "67.6", "38.4", "61.6", "16.4", "83.6", "38.8", "61.2"],
    ["23.6", "76.4", "38.0", "62.0", "13.6", "86.4", "32.4", "67.6"],
    ["32.4", "67.6", "38.8", "61.2", "16.4", "83.6", "42.8", "57.2"],
    ["32.4", "67.6", "38.8", "61.2", "15.2", "84.8", "40.0", "60.0"],
    ["34.8", "65.2", "42.8", "57.2", "23.6", "76.4", "40.4", "59.6"],
    ["27.2", "72.8", "36.8", "63.2", "16.8", "83.2", "36.0", "64.0"],
    ["36.0", "64.0", "42.4", "57.6", "22.8", "77.2", "47.6", "52.4"],
    ["35.2", "64.8", "44.0", "56.0", "22.0", "78.0", "42.4", "57.6"],
    ["36.0", "64.0", "43.2", "56.8", "19.2", "80.8", "36.0", "64.0"],
    ["28.0", "72.0", "39.6", "60.4", "13.6", "86.4", "33.2", "66.8"],
    ["34.8", "65.2", "42.8", "57.2", "16.4", "83.6", "35.2", "64.8"],
    ["34.8", "65.2", "43.6", "56.4", "18.8", "81.2", "35.2", "64.8"],
    ["24.8", "75.2", "39.2", "60.8", "16.4", "83.6", "44.4", "55.6"],
    ["26.4", "73.6", "44.8", "55.2", "14.4", "85.6", "25.6", "74.4"],
    ["32.0", "68.0", "43.2", "56.8", "17.2", "82.8", "45.2", "54.8"],
    ["25.6", "74.4", "39.2", "60.8", "15.6", "84.4", "44.4", "55.6"],
]


async def test_table2_preserves_every_cell_with_dataset_metric_and_comparison_headers():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "LightRAG.pdf")
    ]
    assert events[-1].type == "ready"
    tables = [
        c
        for c in app.document.chunks
        if getattr(c, "kind", None) == "table" and c.table_label == "Table 2"
    ]
    assert len(tables) == 1
    table = tables[0]
    assert table.page_start == table.page_end == 8
    assert table.section.startswith("4.3")
    assert table.table_reconstructed
    assert "每格是 NaiveRAG 勝率 / 變體勝率" in table.text
    assert all(
        dataset in " ".join(table.table_headers)
        for dataset in ["Agriculture", "CS", "Legal", "Mix"]
    )
    rows = table.table_rows
    assert len(rows) == 16
    metrics = ["Comprehensiveness", "Diversity", "Empowerment", "Overall"]
    for i, (row, expected) in enumerate(zip(rows, TABLE2_VALUES, strict=True)):
        variant = ["LightRAG", "-High", "-Low", "-Origin"][i // 4]
        assert row[:2] == [f"NaiveRAG / {variant}", metrics[i % 4]]
        assert row[2:] == [f"{expected[j]}% / {expected[j + 1]}%" for j in range(0, 8, 2)]
    assert not any(
        "64.8%" in c.text
        for c in app.document.chunks
        if c.kind == "text" and c.section.startswith("4.3")
    )


# Transcribed Table 1 baseline / LightRAG pairs, including all four metrics.
TABLE1_VALUES = TABLE2_VALUES[:4] + [
    ["31.6", "68.4", "38.8", "61.2", "15.2", "84.8", "39.2", "60.8"],
    ["29.2", "70.8", "39.2", "60.8", "11.6", "88.4", "30.8", "69.2"],
    ["31.6", "68.4", "36.4", "63.6", "15.2", "84.8", "42.4", "57.6"],
    ["32.4", "67.6", "38.0", "62.0", "14.4", "85.6", "40.0", "60.0"],
    ["26.0", "74.0", "41.6", "58.4", "26.8", "73.2", "40.4", "59.6"],
    ["24.0", "76.0", "38.8", "61.2", "20.0", "80.0", "32.4", "67.6"],
    ["25.2", "74.8", "40.8", "59.2", "26.0", "74.0", "46.0", "54.0"],
    ["24.8", "75.2", "41.6", "58.4", "26.4", "73.6", "42.4", "57.6"],
    ["45.6", "54.4", "48.4", "51.6", "48.4", "51.6", "50.4", "49.6"],
    ["22.8", "77.2", "40.8", "59.2", "26.4", "73.6", "36.0", "64.0"],
    ["41.2", "58.8", "45.2", "54.8", "43.6", "56.4", "50.8", "49.2"],
    ["45.2", "54.8", "48.0", "52.0", "47.2", "52.8", "50.4", "49.6"],
]


async def test_table1_preserves_every_labelled_cell_and_cost_grid_removes_noise():
    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e async for e in app.upload_document(Path("data/lightrag.pdf").read_bytes(), "LightRAG.pdf")
    ]
    assert events[-1].type == "ready"
    rows = [row for c in app.document.chunks if c.table_label == "Table 1" for row in c.table_rows]
    assert len(rows) == 16
    for i, (row, expected) in enumerate(zip(rows, TABLE1_VALUES, strict=True)):
        assert row[:2] == [
            f"{['NaiveRAG', 'RQ-RAG', 'HyDE', 'GraphRAG'][i // 4]} / LightRAG",
            ["Comprehensiveness", "Diversity", "Empowerment", "Overall"][i % 4],
        ]
        assert row[2:] == [f"{expected[j]}% / {expected[j + 1]}%" for j in range(0, 8, 2)]
    cost = [
        c
        for c in app.document.chunks
        if c.kind == "table" and c.page_start == 9 and "Retrieval Phase" in c.text
    ]
    assert cost
    assert all("_" not in c.text for c in cost)
    assert all(
        value in "\n".join(c.text for c in cost)
        for value in ["610", "1,000", "< 100", "1,399", "Textract", "Cextract"]
    )


def authored_table_pdf(*, rows=3, broken=False, heading=True):
    import pymupdf

    with pymupdf.open() as pdf:
        page = pdf.new_page(width=600, height=max(800, rows * 14 + 250))
        if heading:
            page.insert_text((50, 50), "1 Results", fontsize=14)
        page.insert_text((50, 85), "Table 7: Measured values.", fontsize=10)
        for x, text in [(50, "Experiment"), (250, "Accuracy"), (400, "Cost")]:
            page.insert_text((x, 110), text, fontsize=10)
        for i in range(rows):
            for x, text in [(50, f"experiment_{i}"), (250, f"{i}.25%"), (400, f"{i}.75")]:
                if broken and i == 1 and x == 250:
                    continue
                page.insert_text((x, 130 + i * 14), text, fontsize=10)
        page.insert_text(
            (50, 170 + rows * 14), "The results in Table 7 document every measurement.", fontsize=10
        )
        return pdf.tobytes()


async def test_uncertain_table_retains_source_text_and_answer_limitation_rule():
    llm = ScriptedLLM(["not JSON", "The table structure is uncertain. [C1]"])
    app = Application(OllamaEmbedder(), LLMGateway(llm))
    events = [
        e async for e in app.upload_document(authored_table_pdf(broken=True), "uncertain.pdf")
    ]
    assert events[-1].type == "ready"
    tables = [c for c in app.document.chunks if c.kind == "table"]
    assert len(tables) == 1 and not tables[0].table_reconstructed
    assert "結構未能可靠重建" in tables[0].text
    assert all(
        value in tables[0].text
        for value in [
            "experiment_0",
            "0.25%",
            "0.75",
            "experiment_1",
            "1.75",
            "experiment_2",
            "2.25%",
            "2.75",
        ]
    )
    asked = [e async for e in app.ask("What does Table 7 show?")]
    assert asked[-1].type == "trace"
    assert "結構未能可靠重建" in llm.calls[-1].messages[0]["content"]


async def test_large_table_splits_only_between_rows_and_repeats_caption_and_headers():
    from chat_document.tokens import count_tokens

    app = Application(OllamaEmbedder(), LLMGateway(ScriptedLLM([])))
    events = [
        e
        async for e in app.upload_document(authored_table_pdf(rows=230, heading=False), "large.pdf")
    ]
    assert events[-1].type == "ready"
    tables = [c for c in app.document.chunks if c.kind == "table"]
    assert len(tables) > 1
    assert all(c.table_reconstructed and count_tokens(c.text) <= 2000 for c in tables)
    assert all(
        c.table_headers == ["Experiment", "Accuracy", "Cost"]
        and "Table 7: Measured values." in c.text
        for c in tables
    )
    assert [row for c in tables for row in c.table_rows] == [
        [f"experiment_{i}", f"{i}.25%", f"{i}.75"] for i in range(230)
    ]
    assert not any("experiment_" in c.text for c in app.document.chunks if c.kind == "text")
