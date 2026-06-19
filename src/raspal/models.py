from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class FetchResult(BaseModel):
    url: str
    status: int
    html: str | None = None
    text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    engine: str = "scrapling"
    cached: bool = False
    fetched_at: datetime = Field(default_factory=datetime.now)


class ExtractionConfig(BaseModel):
    text: bool = True
    metadata: bool = True
    selectors: dict[str, str] = Field(default_factory=dict)


class LLMConfig(BaseModel):
    model: str = "llama3.2"
    prompt: str = ""
    output_schema: dict[str, Any] | None = None


class PipelineConfig(BaseModel):
    url: str
    engine: str = "auto"
    cache_ttl: int = 3600
    extract: ExtractionConfig = Field(default_factory=lambda: ExtractionConfig())
    llm: LLMConfig | None = None
