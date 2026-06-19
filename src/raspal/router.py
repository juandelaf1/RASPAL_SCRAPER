from pathlib import Path
from raspal.fetcher import Fetcher
from raspal.extractor import Extractor
from raspal.llm import LLMExtractor
from raspal.models import PipelineConfig, LLMConfig
import yaml


class Router:
    def __init__(self, fetcher: Fetcher | None = None):
        self.fetcher = fetcher or Fetcher()
        self.extractor = Extractor()
        self.llm = LLMExtractor()

    def run(self, config_path: str | Path) -> dict:
        with open(config_path) as f:
            raw = yaml.safe_load(f)

        config = PipelineConfig(**raw)

        fetch_result = self.fetcher.fetch(config.url, engine=config.engine, cache_ttl=config.cache_ttl)

        result = {"url": config.url, "status": fetch_result.status, "cached": fetch_result.cached}

        if config.extract.text and fetch_result.html:
            result["text"] = self.extractor.extract_text(fetch_result.html)

        if config.extract.metadata and fetch_result.html:
            result["metadata"] = self.extractor.extract_metadata(fetch_result.html)

        if config.extract.selectors and fetch_result.html:
            result["selectors"] = self.extractor.extract_selectors(
                fetch_result.html, config.extract.selectors
            )

        if config.llm and result.get("text"):
            result["llm_extraction"] = self.llm.extract(result["text"], config.llm)

        return result
