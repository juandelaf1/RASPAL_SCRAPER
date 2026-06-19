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
    error: str | None = None
    fetched_at: datetime = Field(default_factory=datetime.now)


class ExtractionConfig(BaseModel):
    text: bool = True
    metadata: bool = True
    selectors: dict[str, str] = Field(default_factory=dict)
    use_selectolax: bool = True


class LLMConfig(BaseModel):
    model: str = "llama3.2"
    prompt: str = ""
    output_schema: dict[str, Any] | None = None
    template: str = ""
    temperature: float = 0.0
    strict: bool = False
    timeout: int = 60


class ChainStep(BaseModel):
    name: str
    prompt: str
    output_schema: dict[str, Any] | None = None
    template: str = ""
    model: str = ""
    temperature: float = 0.0
    output_key: str | None = None


class ThrottleConfig(BaseModel):
    min_delay: float = 0.5
    max_delay: float = 60.0
    target_avg: float = 1.0


class ProxyConfig(BaseModel):
    http: str = ""
    https: str = ""
    rotate: bool = False


class PipelineConfig(BaseModel):
    url: str
    engine: str = "auto"
    cache_ttl: int = 3600
    timeout: int = 30
    proxy: ProxyConfig | None = None
    extract: ExtractionConfig = Field(default_factory=lambda: ExtractionConfig())
    llm: LLMConfig | None = None
    llm_chain: list[ChainStep] | None = None
    throttle: ThrottleConfig | None = None
