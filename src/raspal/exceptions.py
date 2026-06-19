class RaspalError(Exception):
    """Base exception for all raspal errors."""


class FetchError(RaspalError):
    """Error during URL fetching."""


class TimeoutError(FetchError):
    """Request timed out."""


class HTTPError(FetchError):
    """HTTP error response."""

    def __init__(self, status: int, url: str, body: str = ""):
        self.status = status
        self.url = url
        self.body = body
        super().__init__(f"HTTP {status} for {url}")


class ConnectionError(FetchError):
    """Connection failed."""


class ProxyError(FetchError):
    """Proxy connection failed."""


class ExtractError(RaspalError):
    """Error during extraction."""


class LLMError(RaspalError):
    """Error during LLM extraction."""


class CacheError(RaspalError):
    """Error during cache operations."""


class QueueError(RaspalError):
    """Error during queue operations."""


class ConfigError(RaspalError):
    """Error in configuration."""
