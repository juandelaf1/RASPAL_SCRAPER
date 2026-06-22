from unittest.mock import patch

from raspal.fetcher import Fetcher
from raspal.models import ProxyConfig, FetchResult


def test_resolve_engine_auto():
    f = Fetcher()
    assert f._resolve_engine("https://example.com", "auto") == "scrapling"
    assert f._resolve_engine("http://example.com", "auto") == "scrapling"
    assert f._resolve_engine("https://example.com", "scrapling") == "scrapling"
    assert f._resolve_engine("https://example.com", "playwright") == "playwright"
    assert f._resolve_engine("https://example.com", "stealth") == "stealth"


def test_proxy_kwargs_none():
    f = Fetcher()
    assert f._get_proxy_kwargs() == {}


def test_proxy_kwargs_with_proxy():
    f = Fetcher(proxy=ProxyConfig(http="http://user:pass@proxy:8080"))
    kwargs = f._get_proxy_kwargs()
    assert "proxies" in kwargs
    assert kwargs["proxies"]["http"] == "http://user:pass@proxy:8080"


def test_proxy_kwargs_https_fallback():
    f = Fetcher(proxy=ProxyConfig(http="http://proxy:8080"))
    kwargs = f._get_proxy_kwargs()
    assert kwargs["proxies"]["https"] == "http://proxy:8080"


def test_context_manager():
    with Fetcher() as f:
        assert f.cache is not None
        assert f.throttle is not None


def test_fetch_returns_result_on_error():
    with patch.object(Fetcher, '_dispatch') as mock_dispatch:
        mock_dispatch.return_value = FetchResult(
            url="https://error.test", status=0, error="Simulated error", engine="scrapling"
        )
        f = Fetcher()
        result = f.fetch("https://error.test", timeout=5)
        assert result.status == 0
        assert result.error is not None
