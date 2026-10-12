"""Versioned ingestion-only cache. Publish complete records with an atomic rename."""

import hashlib
import json
import logging
import os
import tempfile
from pathlib import Path

import numpy as np
from pydantic import BaseModel, ValidationError

from .models import Document

PIPELINE_SOURCES = (
    "pdf_parser.py",
    "tables.py",
    "embedder.py",
    "chunker.py",
    "models.py",
    "cache.py",
    "tokens.py",
    "policy.py",
)


def _pipeline_version() -> str:
    """Invalidate records when parsing, Chunking, token rules or their format changes."""
    fingerprint = hashlib.sha256()
    for name in PIPELINE_SOURCES:
        fingerprint.update(name.encode())
        fingerprint.update(Path(__file__).with_name(name).read_bytes())
    return f"ingest-v2-{fingerprint.hexdigest()}"


PIPELINE_VERSION = _pipeline_version()
logger = logging.getLogger(__name__)


class CacheRecord(BaseModel):
    """Document serialization preserves new fields; source identity invalidates prior formats."""

    content_hash: str
    pipeline_version: str
    processing_config: dict[str, int | str]
    document: Document
    embeddings: list[list[float]]


class ProcessingCache:
    def __init__(self, directory: Path, *, pipeline_version: str = PIPELINE_VERSION):
        self.directory = directory
        self.pipeline_version = pipeline_version

    def _path(self, content: bytes, config: dict[str, int | str]) -> Path:
        identity = json.dumps(
            [hashlib.sha256(content).hexdigest(), self.pipeline_version, config], sort_keys=True
        )
        return self.directory / f"{hashlib.sha256(identity.encode()).hexdigest()}.json"

    def load(self, content: bytes, config: dict[str, int | str]) -> CacheRecord | None:
        path = self._path(content, config)
        try:
            record = CacheRecord.model_validate_json(path.read_bytes())
            if (
                record.content_hash != hashlib.sha256(content).hexdigest()
                or record.pipeline_version != self.pipeline_version
                or record.processing_config != config
            ):
                raise ValueError("Cache identity does not match the uploaded Document.")
            vectors = np.asarray(record.embeddings, dtype=np.float32)
            if (
                not record.document.chunks
                or vectors.ndim != 2
                or vectors.shape[0] != len(record.document.chunks)
                or vectors.shape[1] == 0
                or not np.isfinite(vectors).all()
                or np.any(np.linalg.norm(vectors, axis=1) == 0)
            ):
                raise ValueError("Invalid cached embeddings.")
            return record
        except FileNotFoundError:
            return None
        except (OSError, ValidationError, ValueError):
            logger.warning("Ignoring unreadable ingestion cache entry: %s", path)
            return None

    def store(
        self, content: bytes, config: dict[str, int | str], document: Document, vectors: np.ndarray
    ):
        record = CacheRecord(
            content_hash=hashlib.sha256(content).hexdigest(),
            pipeline_version=self.pipeline_version,
            processing_config=config,
            document=document,
            embeddings=vectors.tolist(),
        )
        # Serialize before creating a temporary entry; no partial record is ever readable.
        serialized = record.model_dump_json().encode()
        self.directory.mkdir(parents=True, exist_ok=True)
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=self.directory, suffix=".tmp", delete=False
            ) as out:
                temporary = Path(out.name)
                out.write(serialized)
                out.flush()
                os.fsync(out.fileno())
            os.replace(temporary, self._path(content, config))
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
