"""
Asyncio compatibility improvements for Raspal.
This module enhances the core Fetcher class to support both synchronous and asynchronous operations.
"""

import asyncio
from typing import Self
from concurrent.futures import ThreadPoolExecutor

from raspal.cache import Cache
from raspal.fetcher import Fetcher
from raspal.models import FetchResult
class AsyncFetcher(Fetcher):
    """Enhanced fetcher with async support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._async_executor = ThreadPoolExecutor(max_workers=4)
        self._semaphore = asyncio.Semaphore(100)  # Limit concurrent requests

    async def fetch_async(
        self,
        url: str,
        engine: str = "auto",
        cache_ttl: int = 3600,
        timeout: int = 30,
        **kwargs,
    ) -> FetchResult:
        """Fetch a URL asynchronously."""
        async with self._semaphore:
            # Check cache in async-friendly way
            if self.cache:
                try:
                    cached = await self._async_cache_get(url, ttl=cache_ttl)
                    if cached is not None:
                        return FetchResult(
                            url=url, status=200, html=cached, cached=True, engine=engine
                        )
                except Exception:
                    pass

            # Perform async fetch
            result = await self._dispatch_async(url, engine, timeout, kwargs)

            # Cache result
            if self.cache and result.html and result.status == 200:
                try:
                    await self._async_cache_set(url, result.html)
                except Exception:
                    pass

            # Record in throttle
            self.throttle.record(engine, result.status)
            return result

    async def _async_cache_get(self, url: str, ttl: int):
        """Asynchronously get from cache."""
        if isinstance(self.cache, Cache):
            return self.cache.get(url, ttl=ttl)
        return None

    async def _async_cache_set(self, url: str, html: str):
        """Asynchronously set to cache."""
        if isinstance(self.cache, Cache):
            self.cache.set(url, html)

    async def _dispatch_async(self, url: str, engine: str, timeout: int, kwargs: dict) -> FetchResult:
        """Dispatch request asynchronously."""
        # Run the synchronous _dispatch in a thread
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._async_executor,
            lambda: self._dispatch(url, engine, timeout, kwargs)
        )

    async def fetch_batch(self, urls: list[str], engine: str = "auto", cache_ttl: int = 3600, timeout: int = 30, **kwargs) -> list[FetchResult]:
        """Fetch multiple URLs asynchronously."""
        tasks = [self.fetch_async(url, engine, cache_ttl, timeout, **kwargs) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def close(self):
        """Close async resources."""
        self._async_executor.shutdown(wait=True)
        await super().close()

    def __aiter__(self) -> Self:
        return self

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args):
        await self.close()
async def enhance_fetcher(fetcher: Fetcher) -> FetchResult:
    """
    Enhance a synchronous Fetcher with async capabilities.
    This function is primarily for backward compatibility.
    """
    if isinstance(fetcher, Fetcher):
        return fetcher
    raise ValueError(f"Unsupported fetcher type: {type(fetcher)}")


def run_async_example():
    """Example showing how to use the enhanced async fetcher."""
    import asyncio

    async def main():
        from raspal.fetcher import Fetcher

        # Create fetcher
        fetcher = AsyncFetcher()

        # Example: fetch multiple URLs concurrently
        urls = [
            "https://example.com",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/json",
        ]

        results = await fetcher.fetch_batch(urls)

        for result in results:
            if isinstance(result, Exception):
                print(f"Error: {result}")
            else:
                print(f"URL: {result.url}, Status: {result.status}, Cached: {result.cached}")

    asyncio.run(main())
if __name__ == "__main__":
    run_async_example()
