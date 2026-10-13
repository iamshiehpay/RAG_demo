"""Options for one-command live evaluation; default pytest never calls gpt-oss."""

from pathlib import Path

import pytest


def positive_int(value: str) -> int:
    try:
        number = int(value)
        if number > 0:
            return number
    except ValueError:
        pass
    raise pytest.UsageError("--eval-repeats must be a positive integer")


def pytest_addoption(parser):
    group = parser.getgroup("Golden Facts evaluation")
    group.addoption("--eval-repeats", type=positive_int, default=1, help="Runs per question")
    group.addoption("--eval-document", type=Path, default=Path("data/lightrag.pdf"))
    group.addoption("--eval-report", type=Path, default=None, help="Markdown output path")
    group.addoption("--eval-label", default="evaluation", help="Report experiment label")
    group.addoption("--eval-cases", default="", help="Comma-separated case ids; default all")
    group.addoption(
        "--eval-record-only",
        action="store_true",
        help="Record failures without asserting all Golden Facts pass (baseline only)",
    )


def pytest_collection_modifyitems(config, items):
    selection = config.getoption("--eval-cases")
    if not selection:
        return
    from .golden_facts import LIGHTRAG_CASES, router_cases
    from .second_document import SECOND_DOCUMENT_CASES

    chosen = {value.strip() for value in selection.split(",")}
    primary = {c.id for c in LIGHTRAG_CASES + router_cases()}
    second = {c.id for c in SECOND_DOCUMENT_CASES}
    if chosen - primary - second:
        raise pytest.UsageError(f"Unknown --eval-cases ids: {sorted(chosen - primary - second)}")
    retained, removed = [], []
    for item in items:
        skip = (
            item.name == "test_live_router_canonical_and_held_out_cases"
            or item.name == "test_golden_facts_live"
            and not chosen & primary
            or item.name == "test_second_document_real_ingestion_and_golden_facts"
            and not chosen & second
        )
        (removed if skip else retained).append(item)
    items[:] = retained
    config.hook.pytest_deselected(items=removed)
