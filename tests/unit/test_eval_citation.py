from chat_document.application import Application
from chat_document.events import FinalEvent
from chat_document.models import Chunk, Citation, Document
from eval.models import EvaluationCase
from eval.runner import check_source_citation


def test_citation_prefers_a_labeled_table_chunk_when_available():
    class TableChunk(Chunk):
        kind: str = "table"
        table_label: str = "Table 2"

    common = dict(section_id="s", section="Results", page_start=8, page_end=8)
    paragraph = Chunk(id="paragraph", text="The discussion of Table 2.", order=0, **common)
    table = TableChunk(id="table", text="Ablation win rates", order=1, **common)
    application = Application(None, None)
    application.document = Document(id="d", name="test", sections=[], chunks=[paragraph, table])
    case = EvaluationCase(
        "Q3", "question", (), required_citation_page=8, required_citation_term="Table 2"
    )

    def final(source):
        citation = Citation(
            id="C1", source_id=source.id, section="Results", page_start=8, page_end=8
        )
        return [FinalEvent(answer="Evidence [C1]", citations=[citation])]

    assert not check_source_citation(application, final(paragraph), case).passed
    assert check_source_citation(application, final(table), case).passed
    application.document.chunks = [paragraph]
    assert check_source_citation(application, final(paragraph), case).passed
