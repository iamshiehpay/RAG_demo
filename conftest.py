"""Evaluation options and dependency-tier markers for explicit test selection."""

from pathlib import Path

import pytest

pytest_plugins = ("eval.pytest_plugin",)
TESTS = Path(__file__).parent / "tests"


def pytest_collection_modifyitems(items):
    for item in items:
        for tier in ("unit", "integration"):
            if TESTS / tier in item.path.parents:
                item.add_marker(getattr(pytest.mark, tier))
