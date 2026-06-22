from raspal.improvements.async_compatibility import AsyncFetcher


def test_async_fetcher_imports():
    assert AsyncFetcher is not None


def test_async_fetcher_instantiates():
    fetcher = AsyncFetcher(max_workers=2)
    assert fetcher is not None
