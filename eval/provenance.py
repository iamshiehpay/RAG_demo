"""Report source provenance when available, including zip delivery without Git."""

import subprocess
from pathlib import Path


def repository_state(directory: Path | None = None) -> tuple[str, str]:
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=directory, stderr=subprocess.DEVNULL, text=True
        ).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=directory, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown", "unknown"
    return revision, "yes" if dirty else "no"
