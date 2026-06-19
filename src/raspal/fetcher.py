from raspal.cache import Cache
from raspal.models import FetchResult


class Fetcher:
    def __init__(self, cache: Cache | None = None):
        self.cache = cache or Cache()
        self._playwright = None

    def fetch(self, url: str, engine: str = "auto", cache_ttl: int = 3600) -> FetchResult:
        if engine == "auto":
            engine = self._detect_engine(url)

        if self.cache:
            cached = self.cache.get(url, ttl=cache_ttl)
            if cached is not None:
                return FetchResult(url=url, status=200, html=cached, cached=True, engine=engine)

        result = self._fetch_scrapling(url) if engine == "scrapling" else self._fetch_playwright(url)

        if self.cache and result.html:
            self.cache.set(url, result.html)

        return result

    def _detect_engine(self, url: str) -> str:
        return "scrapling"

    def _fetch_scrapling(self, url: str) -> FetchResult:
        try:
            from scrapling import Fetcher as ScraplingFetcher

            f = ScraplingFetcher()
            resp = f.get(url)
            return FetchResult(
                url=url,
                status=resp.status,
                html=resp.text,
                engine="scrapling",
                metadata={"headers": dict(resp.headers)},
            )
        except Exception as e:
            return FetchResult(url=url, status=0, text=str(e), engine="scrapling")

    def _fetch_playwright(self, url: str) -> FetchResult:
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="networkidle")
                html = page.content()
                browser.close()
            return FetchResult(url=url, status=200, html=html, engine="playwright")
        except Exception as e:
            return FetchResult(url=url, status=0, text=str(e), engine="playwright")
