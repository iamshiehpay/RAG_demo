"""Retrieval settings: AGENTS.md defaults, configurable for eval experiments."""

import os

from pydantic import BaseModel, ConfigDict, Field

from .policy import LOOKUP_TOP_K, SUB_QUERY_TOP_K, SYNTHESIS_TOP_K


class RetrievalSettings(BaseModel):
    model_config = ConfigDict(frozen=True)
    lookup_top_k: int = Field(default=LOOKUP_TOP_K, gt=0)
    synthesis_top_k: int = Field(default=SYNTHESIS_TOP_K, gt=0)
    sub_query_top_k: int = Field(default=SUB_QUERY_TOP_K, gt=0)

    @classmethod
    def from_env(cls) -> "RetrievalSettings":
        return cls(
            **{
                key: os.environ[key.upper()]
                for key in cls.model_fields
                if key.upper() in os.environ
            }
        )
