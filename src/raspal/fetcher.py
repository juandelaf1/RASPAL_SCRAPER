from raspal.cache import Cache
from raspal.models import FetchResult
from raspal.throttle import AutoThrottle


class Fetcher:
    STATIC = "scrapling"
    DYNAMIC = "playwright"
    STEALTH = "stealth"

    def __init__(self, cache: Cache | None = None, throttle: AutoThrottle | None = None):
        self.cache = cache or Cache()
        self.throttle = throttle or AutoThrottle()
        self._configure_scrapling()

    @staticmethod
    def _configure_scrapling():
        from scrapling import Fetcher as ScraplingFetcher

        ScraplingFetcher.configure(
            huge_tree=True,
            adaptive=True,
        )

    def fetch(
        self,
        url: str,
        engine: str = "auto",
        cache_ttl: int = 3600,
        **kwargs,
    ) -> FetchResult:
        engine = self._resolve_engine(url, engine)
        self.throttle.wait(engine)

        if self.cache:
            cached = self.cache.get(url, ttl=cache_ttl)
            if cached is not None:
                return FetchResult(url=url, status=200, html=cached, cached=True, engine=engine)

        result = self._dispatch(url, engine, kwargs)

        if self.cache and result.html:
            self.cache.set(url, result.html)

        self.throttle.record(engine, result.status)
        return result

    def _resolve_engine(self, url: str, preferred: str) -> str:
        if preferred != "auto":
            return preferred
        if url.startswith("https://") or url.startswith("http://"):
            return self.STATIC
        return self.STATIC

    def _dispatch(self, url: str, engine: str, kwargs: dict) -> FetchResult:
        dispatch = {
            self.STATIC: self._fetch_static,
            self.DYNAMIC: self._fetch_dynamic,
            self.STEALTH: self._fetch_stealth,
        }
        handler = dispatch.get(engine, self._fetch_static)
        try:
            return handler(url, kwargs)
        except Exception as e:
            return FetchResult(url=url, status=0, text=str(e), engine=engine)

    def _fetch_static(self, url: str, kwargs: dict) -> FetchResult:
        from scrapling import Fetcher as ScraplingFetcher

        resp = ScraplingFetcher.get(url, **kwargs)
        html = resp.html_content or (resp.body.decode() if hasattr(resp, "body") else None)
        return FetchResult(
            url=url,
            status=resp.status,
            html=html,
            engine=self.STATIC,
            metadata={"headers": dict(resp.headers)},
        )

    def _fetch_dynamic(self, url: str, kwargs: dict) -> FetchResult:
        from scrapling.fetchers import DynamicFetcher

        opts = {
            "headless": True,
            "disable_resources": True,
            "network_idle": True,
            "load_dom": True,
            "block_ads": True,
            **kwargs,
        }
        resp = DynamicFetcher.fetch(url, **opts)
        html = resp.html_content or (resp.body.decode() if hasattr(resp, "body") else None)
        return FetchResult(
            url=url,
            status=resp.status,
            html=html,
            engine=self.DYNAMIC,
            metadata={"headers": dict(resp.headers)},
        )

    def _fetch_stealth(self, url: str, kwargs: dict) -> FetchResult:
        from scrapling.fetchers import StealthyFetcher

        opts = {
            "headless": True,
            "disable_resources": True,
            "network_idle": True,
            "load_dom": True,
            "block_ads": True,
            "solve_cloudflare": True,
            **kwargs,
        }
        resp = StealthyFetcher.fetch(url, **opts)
        html = resp.html_content or (resp.body.decode() if hasattr(resp, "body") else None)
        return FetchResult(
            url=url,
            status=resp.status,
            html=html,
            engine=self.STEALTH,
            metadata={"headers": dict(resp.headers)},
        )
