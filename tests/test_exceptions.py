import pytest
from raspal.exceptions import (
    RaspalError,
    FetchError,
    TimeoutError,
    HTTPError,
    ConnectionError,
    ProxyError,
    ExtractError,
    LLMError,
    CacheError,
    QueueError,
    ConfigError,
)


def test_hierarchy():
    assert issubclass(FetchError, RaspalError)
    assert issubclass(TimeoutError, FetchError)
    assert issubclass(HTTPError, FetchError)
    assert issubclass(ConnectionError, FetchError)
    assert issubclass(ProxyError, FetchError)
    assert issubclass(ExtractError, RaspalError)
    assert issubclass(LLMError, RaspalError)
    assert issubclass(CacheError, RaspalError)
    assert issubclass(QueueError, RaspalError)
    assert issubclass(ConfigError, RaspalError)


def test_http_error():
    err = HTTPError(404, "https://example.com/404")
    assert err.status == 404
    assert err.url == "https://example.com/404"
    assert "HTTP 404" in str(err)


def test_timeout_error():
    err = TimeoutError("Timed out after 30s")
    assert "Timed out" in str(err)


def test_raspal_error_is_base():
    assert RaspalError.__name__ == "RaspalError"
