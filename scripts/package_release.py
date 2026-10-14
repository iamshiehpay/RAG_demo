"""Package committed code plus curated evidence; keep bulk history in a second zip.

Standard library only. Nothing is sent anywhere, and untracked/working-tree files
are never read into an archive. Both zips extract into the same project directory.
"""

import argparse
import hashlib
import io
import json
import posixpath
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

ROOT_FILES = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTEXT.md",
    ".gitignore",
    "pyproject.toml",
    "uv.lock",
    "conftest.py",
}
CODE_PREFIXES = ("src/", "tests/", "scripts/", "frontend/", "eval/")
DOC_FILES = {
    "docs/design.md",
    "docs/development.md",
    "docs/ai-collaboration.md",
    "docs/ai-log.md",
    "frontend/review/DESIGN.md",
}
DOC_PREFIXES = ("docs/adr/", "docs/agents/")
HISTORY_PREFIXES = (
    "docs/qa/",
    "docs/verification/",
    "eval/reports/",
    "spikes/",
    ".scratch/",
    "frontend/review/",
)
HISTORY_FILES = {"簡報素材.md", "題目：讓 AI 跟文件對話（Chat with Document）.md"}
REQUIRED = {
    "README.md",
    "pyproject.toml",
    "uv.lock",
    "src/chat_document/api.py",
    "frontend/dist/index.html",
}
BLOCKED_PARTS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".cache",
    ".pytest_cache",
    ".ruff_cache",
    ".lat",
    ".worktrees",
    "data",
}
PREFIX = "chat-with-document/"


def _git(repository: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repository), *args])


def _permitted(path: str) -> bool:
    parts = PurePosixPath(path).parts
    # tests/data contains public regression fixtures, not downloaded Documents.
    blocked = BLOCKED_PARTS - {"data"} if path.startswith("tests/data/") else BLOCKED_PARTS
    return (
        not any(part in blocked or part.startswith(".env") for part in parts)
        and not path.lower().endswith((".pdf", ".pyc"))
        and not path.startswith("/")
        and ".." not in parts
    )


def _code_file(path: str) -> bool:
    if path in ROOT_FILES or path in DOC_FILES or path.startswith(DOC_PREFIXES):
        return True
    return path.startswith(CODE_PREFIXES) and not path.startswith(HISTORY_PREFIXES)


def _zip_payload(
    files: dict[str, bytes], modes: dict[str, str], commit: str, *, manifest="RELEASE.json"
) -> bytes:
    payload = dict(files)
    payload[manifest] = (
        json.dumps(
            {
                "commit": commit,
                "sha256": {
                    p: hashlib.sha256(data).hexdigest() for p, data in sorted(files.items())
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    ).encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(PREFIX + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (0o100755 if modes.get(name) == "100755" else 0o100644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return output.getvalue()


def build_release(repository: Path, output_dir: Path) -> dict[str, Path]:
    repository, output_dir = Path(repository), Path(output_dir)
    commit = _git(repository, "rev-parse", "HEAD").decode().strip()
    entries = _git(repository, "ls-tree", "-rz", "--full-tree", commit).split(b"\0")
    tree = {}
    for entry in filter(None, entries):
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = raw_path.decode()
        if _permitted(path):
            tree[path] = (mode, kind, oid)
    missing = REQUIRED - tree.keys()
    if missing:
        raise ValueError(f"Missing release files: {', '.join(sorted(missing))}")

    blobs = {}

    def read(path):
        mode, kind, oid = tree[path]
        if mode == "120000" or kind != "blob":
            raise ValueError(f"Cannot export symlink/submodule: {path}")
        if path not in blobs:
            blobs[path] = _git(repository, "cat-file", "blob", oid)
        return blobs[path]

    code = {p for p in tree if _code_file(p)}
    # Include local Markdown-link targets so the concise reading path is usable
    # without downloading the bulk evidence zip. Inline historical paths are not
    # recursively expanded; their full records remain in the companion archive.
    pending = list(code)
    while pending:
        path = pending.pop()
        if not path.endswith(".md"):
            continue
        for raw in re.findall(r"\]\(([^\s]+?)\)", read(path).decode("utf-8")):
            if "://" in raw or raw.startswith(("#", "/", "mailto:")):
                continue
            target = posixpath.normpath(
                posixpath.join(posixpath.dirname(path), unquote(raw.split("#", 1)[0]).strip("<>"))
            )
            if target in tree and target not in code:
                code.add(target)
                pending.append(target)

    evidence = {p for p in tree if p.startswith(HISTORY_PREFIXES) or p in HISTORY_FILES} - code
    code_files = {p: read(p) for p in sorted(code)}
    evidence_files = {p: read(p) for p in sorted(evidence)}
    code_files["CHANGELOG.txt"] = _git(
        repository, "log", "--date=iso-strict", "--format=%H %ad %s", commit
    )
    evidence_files["EVIDENCE.txt"] = (
        f"Historical evidence for commit {commit}.\n"
        "Extract this zip alongside the code zip; both use chat-with-document/.\n"
        "These are prior observations, including failed runs, not a new verification.\n"
    ).encode()
    modes = {p: value[0] for p, value in tree.items()}
    archives = {
        "code": ("chat-with-document.zip", _zip_payload(code_files, modes, commit)),
        "evidence": (
            "chat-with-document-evidence.zip",
            _zip_payload(evidence_files, modes, commit, manifest="EVIDENCE-RELEASE.json"),
        ),
    }
    # All validation and reads complete before output is created. Never overwrite
    # an earlier delivery, even if only one of its archives remains.
    if output_dir.exists():
        raise FileExistsError(f"Choose a new output directory: {output_dir}")
    output_dir.mkdir(parents=True)
    result = {}
    for kind, (name, data) in archives.items():
        target = output_dir / name
        with target.open("xb") as output:
            output.write(data)
        result[kind] = target
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, required=True, help="New directory for the two zip files"
    )
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    for kind, path in build_release(repository, args.output).items():
        print(f"{kind}: {path} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
