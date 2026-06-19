from pathlib import Path

import yaml

from raspal.exceptions import ConfigError, RaspalError
from raspal.extractor import Extractor
from raspal.fetcher import Fetcher
from raspal.llm import LLMExtractor
from raspal.models import PipelineConfig
from raspal.pipeline import Pipeline
from raspal.queue import RequestQueue
from raspal.throttle import AutoThrottle


class Router:
    def __init__(self):
        self.throttle = AutoThrottle()
        self.fetcher = Fetcher(throttle=self.throttle)
        self.extractor = Extractor()
        self.llm = LLMExtractor()

    def _load_config(self, config_path: str | Path) -> PipelineConfig:
        try:
            with open(config_path) as f:
                raw = yaml.safe_load(f)
            return PipelineConfig(**raw)
        except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
            raise ConfigError(f"Invalid config at {config_path}: {e}") from e

    def _apply_config(self, config: PipelineConfig):
        if config.throttle:
            self.throttle = AutoThrottle(
                min_delay=config.throttle.min_delay,
                max_delay=config.throttle.max_delay,
                target_avg=config.throttle.target_avg,
            )
        self.fetcher = Fetcher(
            throttle=self.throttle,
            proxy=config.proxy,
        )

    def run(self, config_path: str | Path) -> dict:
        config = self._load_config(config_path)
        self._apply_config(config)

        fetch_result = self.fetcher.fetch(
            config.url,
            engine=config.engine,
            cache_ttl=config.cache_ttl,
            timeout=config.timeout,
        )

        result = {
            "url": config.url,
            "status": fetch_result.status,
            "engine": fetch_result.engine,
            "cached": fetch_result.cached,
        }

        if fetch_result.error:
            result["error"] = fetch_result.error
            return result

        if config.extract.text and fetch_result.html:
            try:
                result["text"] = self.extractor.extract_text(fetch_result.html)
            except Exception as e:
                result["text_error"] = str(e)

        if config.extract.metadata and fetch_result.html:
            try:
                result["metadata"] = self.extractor.extract_metadata(fetch_result.html)
            except Exception as e:
                result["metadata_error"] = str(e)

        if config.extract.selectors and fetch_result.html:
            try:
                if config.extract.use_selectolax:
                    result["selectors"] = self.extractor.extract_selectors_fast(
                        fetch_result.html, config.extract.selectors
                    )
                else:
                    result["selectors"] = self.extractor.extract_selectors(
                        fetch_result.html, config.extract.selectors
                    )
            except Exception as e:
                result["selectors_error"] = str(e)

        text = result.get("text")
        text_str = str(text) if text else ""
        if config.llm and text_str:
            try:
                result["llm_extraction"] = self.llm.extract(text_str, config.llm)
            except Exception as e:
                result["llm_extraction_error"] = str(e)

        if config.llm_chain and text_str:
            try:
                result["llm_chain"] = self.llm.extract_chain(text_str, config.llm_chain)
            except Exception as e:
                result["llm_chain_error"] = str(e)

        return result

    def run_queue(
        self,
        config_path: str | Path,
        queue_path: str | Path = "raspal_queue.sqlite",
    ) -> Pipeline:
        config = self._load_config(config_path)
        self._apply_config(config)

        queue = RequestQueue(queue_path)
        pipeline = Pipeline()

        try:
            while queue.pending_count() > 0:
                item = queue.pop()
                if item is None:
                    break

                try:
                    result = self.fetcher.fetch(
                        item.url,
                        engine=item.engine,
                        timeout=config.timeout,
                    )

                    if result.status != 200:
                        queue.retry(item, f"HTTP {result.status}")
                        continue

                    data: dict = {"status": result.status, "engine": result.engine}

                    if result.error:
                        queue.retry(item, result.error)
                        continue

                    if config.extract.text and result.html:
                        try:
                            data["text"] = self.extractor.extract_text(result.html)
                        except Exception as e:
                            data["text_error"] = str(e)

                    if config.extract.metadata and result.html:
                        try:
                            data["metadata"] = self.extractor.extract_metadata(
                                result.html
                            )
                        except Exception as e:
                            data["metadata_error"] = str(e)

                    if config.extract.selectors and result.html:
                        try:
                            if config.extract.use_selectolax:
                                data["selectors"] = (
                                    self.extractor.extract_selectors_fast(
                                        result.html, config.extract.selectors
                                    )
                                )
                            else:
                                data["selectors"] = self.extractor.extract_selectors(
                                    result.html, config.extract.selectors
                                )
                        except Exception as e:
                            data["selectors_error"] = str(e)

                    text = data.get("text")
                    text_str = str(text) if text else ""
                    if config.llm and text_str:
                        try:
                            data["llm_extraction"] = self.llm.extract(
                                text_str, config.llm
                            )
                        except Exception as e:
                            data["llm_extraction_error"] = str(e)

                    if config.llm_chain and text_str:
                        try:
                            data["llm_chain"] = self.llm.extract_chain(
                                text_str, config.llm_chain
                            )
                        except Exception as e:
                            data["llm_chain_error"] = str(e)

                    pipeline.add(url=item.url, data=data)
                    queue.complete(item)

                except RaspalError as e:
                    queue.retry(item, str(e))
                except Exception as e:
                    queue.retry(item, str(e))
        finally:
            queue.close()

        return pipeline
