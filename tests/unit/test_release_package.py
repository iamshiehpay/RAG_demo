"""Delivery must contain committed, runnable code without local/private artifacts."""

import hashlib
import json
import subprocess
import zipfile

import pytest

from scripts.package_release import build_release


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


@pytest.fixture
def repository(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "Release test")
    files = {
        "README.md": "Usage\n",
        "pyproject.toml": "[project]\nname='example'\n",
        "uv.lock": "version = 1\n",
        "src/chat_document/api.py": "# committed API\n",
        "frontend/dist/index.html": "<html>working build</html>\n",
        "frontend/src/App.tsx": "// original frontend\n",
        "tests/unit/test_example.py": "def test_example(): assert True\n",
        "docs/ai-collaboration.md": "Evidence overview\n",
        "docs/verification/ticket-old/raw.json": '{"result":"FAIL"}\n',
        "spikes/out/probe.json": '{"observed":123}\n',
        ".scratch/chat-with-document/PRD.md": "Requirements\n",
        "簡報素材.md": "Presentation evidence\n",
        ".env": "SECRET=do-not-export\n",
        ".cache/private.json": "private cache\n",
        "data/paper.pdf": "private PDF\n",
        "frontend/node_modules/package/index.js": "installed dependency\n",
    }
    for name, content in files.items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "Initial delivery fixture")
    return repo


def contents(path):
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def test_release_uses_committed_allowlist_and_separates_historical_evidence(repository, tmp_path):
    (repository / "src/chat_document/api.py").write_text("# uncommitted replacement")
    (repository / "src/chat_document/untracked.py").write_text("secret")
    result = build_release(repository, tmp_path / "delivery")
    code = contents(result["code"])
    evidence = contents(result["evidence"])
    assert code.keys().isdisjoint(evidence), "Extracting evidence must not overwrite code metadata"
    prefix = "chat-with-document/"
    assert code[prefix + "src/chat_document/api.py"] == b"# committed API\n"
    assert prefix + "frontend/dist/index.html" in code
    assert prefix + "tests/unit/test_example.py" in code
    assert prefix + "docs/ai-collaboration.md" in code
    assert prefix + "docs/verification/ticket-old/raw.json" not in code
    assert prefix + "docs/verification/ticket-old/raw.json" in evidence
    assert prefix + "spikes/out/probe.json" in evidence
    assert prefix + ".scratch/chat-with-document/PRD.md" in evidence
    assert prefix + "簡報素材.md" in evidence
    forbidden = [".env", ".cache/", ".pdf", "node_modules/", "untracked.py", ".git/"]
    assert not any(term in name for name in [*code, *evidence] for term in forbidden)
    manifest = json.loads(code[prefix + "RELEASE.json"])
    assert manifest["commit"] == git(repository, "rev-parse", "HEAD")
    for name, digest in manifest["sha256"].items():
        assert hashlib.sha256(code[prefix + name]).hexdigest() == digest
    assert git(repository, "rev-parse", "HEAD").encode() in code[prefix + "CHANGELOG.txt"]


def test_release_is_reproducible_and_does_not_overwrite(repository, tmp_path):
    first = build_release(repository, tmp_path / "first")
    second = build_release(repository, tmp_path / "second")
    for kind in ("code", "evidence"):
        assert first[kind].read_bytes() == second[kind].read_bytes()
    before = first["code"].read_bytes()
    with pytest.raises(FileExistsError):
        build_release(repository, tmp_path / "first")
    assert first["code"].read_bytes() == before


def test_release_rejects_missing_frontend_before_writing(repository, tmp_path):
    git(repository, "rm", "frontend/dist/index.html")
    git(repository, "commit", "-qm", "Missing production build")
    output = tmp_path / "delivery"
    with pytest.raises(ValueError, match="frontend/dist/index.html"):
        build_release(repository, output)
    assert not output.exists()


def test_release_never_exports_selected_symlinks(repository, tmp_path):
    link = repository / "src/chat_document/external.py"
    link.symlink_to(tmp_path / "outside-secret")
    git(repository, "add", str(link))
    git(repository, "commit", "-qm", "A symlink must not enter delivery")
    with pytest.raises(ValueError, match="symlink"):
        build_release(repository, tmp_path / "delivery")
