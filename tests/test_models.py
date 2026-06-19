from raspal.models import (
    FetchResult,
    ExtractionConfig,
    LLMConfig,
    ChainStep,
    ThrottleConfig,
    ProxyConfig,
    PipelineConfig,
)


def test_fetch_result_defaults():
    r = FetchResult(url="https://x.com", status=200)
    assert r.url == "https://x.com"
    assert r.status == 200
    assert r.html is None
    assert r.cached is False
    assert r.engine == "scrapling"
    assert r.error is None
    assert r.fetched_at is not None


def test_extraction_config_defaults():
    c = ExtractionConfig()
    assert c.text is True
    assert c.metadata is True
    assert c.selectors == {}
    assert c.use_selectolax is True


def test_llm_config():
    c = LLMConfig(model="llama3.2", template="product", strict=True, timeout=120)
    assert c.model == "llama3.2"
    assert c.template == "product"
    assert c.strict is True
    assert c.timeout == 120


def test_chain_step():
    step = ChainStep(
        name="classify",
        prompt="Classify this",
        output_schema={"type": ""},
        temperature=0.5,
    )
    assert step.name == "classify"
    assert step.output_schema == {"type": ""}
    assert step.temperature == 0.5


def test_proxy_config():
    p = ProxyConfig(http="http://user:pass@proxy:8080")
    assert p.http == "http://user:pass@proxy:8080"
    assert p.https == ""
    assert p.rotate is False


def test_pipeline_config_defaults():
    c = PipelineConfig(url="https://x.com")
    assert c.url == "https://x.com"
    assert c.engine == "auto"
    assert c.cache_ttl == 3600
    assert c.timeout == 30
    assert c.proxy is None
    assert c.llm is None
    assert c.llm_chain is None
