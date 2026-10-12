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
