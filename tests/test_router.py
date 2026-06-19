from pathlib import Path

import pytest

from raspal.router import Router
from raspal.exceptions import ConfigError


def test_load_config_invalid_path():
    router = Router()
    with pytest.raises(ConfigError):
        router._load_config("/nonexistent/path.yaml")


def test_load_config_invalid_yaml(tmp_path: Path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("{{{invalid yaml")
    router = Router()
    with pytest.raises(ConfigError):
        router._load_config(str(bad))


def test_load_config_valid(tmp_path: Path):
    cfg = tmp_path / "test.yaml"
    cfg.write_text("""
        url: "https://example.com"
        engine: auto
    """)
    router = Router()
    config = router._load_config(str(cfg))
    assert config.url == "https://example.com"
    assert config.engine == "auto"


def test_load_config_with_all_options(tmp_path: Path):
    cfg = tmp_path / "full.yaml"
    cfg.write_text("""
        url: "https://example.com"
        engine: stealth
        cache_ttl: 7200
        timeout: 60
        proxy:
            http: "http://proxy:8080"
        extract:
            text: true
            metadata: false
            selectors:
                title: h1
        llm:
            model: llama3.2
            template: product
        throttle:
            min_delay: 1.0
            max_delay: 30.0
    """)
    router = Router()
    config = router._load_config(str(cfg))
    assert config.url == "https://example.com"
    assert config.engine == "stealth"
    assert config.cache_ttl == 7200
    assert config.timeout == 60
    assert config.proxy is not None
    assert config.proxy.http == "http://proxy:8080"
    assert config.extract.text is True
    assert config.extract.metadata is False
    assert config.llm is not None
    assert config.llm.model == "llama3.2"
    assert config.throttle is not None
    assert config.throttle.min_delay == 1.0
    assert config.throttle.max_delay == 30.0
