"""Chunk/retrieval settings: AGENTS.md defaults, configurable for eval experiments."""

import os
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .llm_gateway import BUDGET_TABLE
from .policy import (
    BM25_WEIGHT,
    CHUNK_TOKEN_TARGET,
    LOOKUP_TOP_K,
    SUB_QUERY_TOP_K,
    SUMMARY_CONCURRENCY,
    SYNTHESIS_TOP_K,
)


class RetrievalSettings(BaseModel):
    model_config = ConfigDict(frozen=True)
    lookup_top_k: int = Field(default=LOOKUP_TOP_K, gt=0)
    synthesis_top_k: int = Field(default=SYNTHESIS_TOP_K, gt=0)
    sub_query_top_k: int = Field(default=SUB_QUERY_TOP_K, gt=0)
    chunk_token_target: int = Field(default=CHUNK_TOKEN_TARGET, gt=0)
    answer_think: Literal["low", "medium"] = BUDGET_TABLE["answer"].think
    bm25_weight: float = Field(default=BM25_WEIGHT, ge=0, le=1, allow_inf_nan=False)
    summary_concurrency: int = Field(default=SUMMARY_CONCURRENCY, gt=0)

    @classmethod
    def from_env(cls) -> "RetrievalSettings":
        return cls(
            **{
                key: os.environ[key.upper()]
                for key in cls.model_fields
                if key.upper() in os.environ
            }
        )
