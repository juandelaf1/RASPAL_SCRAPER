import time
from pathlib import Path

import pytest

from raspal.cache import Cache
from raspal.exceptions import CacheError


def test_cache_set_get(tmp_path: Path):
    db = tmp_path / "test_cache.sqlite"
    cache = Cache(db)
    cache.set("https://a.com", "<html>hello</html>")
    result = cache.get("https://a.com", ttl=3600)
    assert result == "<html>hello</html>"
    cache.close()


def test_cache_expiry(tmp_path: Path):
    db = tmp_path / "test_expiry.sqlite"
    cache = Cache(db)
    cache.set("https://a.com", "<html>hello</html>")
    result = cache.get("https://a.com", ttl=-1)
    assert result is None
    cache.close()


def test_cache_miss(tmp_path: Path):
    db = tmp_path / "test_miss.sqlite"
    cache = Cache(db)
    result = cache.get("https://unknown.com")
    assert result is None
    cache.close()


def test_cache_clear_single(tmp_path: Path):
    db = tmp_path / "test_clear.sqlite"
    cache = Cache(db)
    cache.set("https://a.com", "aaa")
    cache.set("https://b.com", "bbb")
    cache.clear("https://a.com")
    assert cache.get("https://a.com") is None
    assert cache.get("https://b.com") is not None
    cache.close()


def test_cache_clear_all(tmp_path: Path):
    db = tmp_path / "test_clear_all.sqlite"
    cache = Cache(db)
    cache.set("https://a.com", "aaa")
    cache.set("https://b.com", "bbb")
    cache.clear()
    assert cache.get("https://a.com") is None
    assert cache.get("https://b.com") is None
    cache.close()


def test_cache_context_manager(tmp_path: Path):
    db = tmp_path / "test_ctx.sqlite"
    with Cache(db) as cache:
        cache.set("https://a.com", "hello")
        assert cache.get("https://a.com") == "hello"
    # After context exit, should be closed
    assert cache.conn is None


def test_cache_invalid_path():
    with pytest.raises(CacheError):
        # Invalid path chars might raise on some OS
        Cache("/nonexistent/deep/dir/cache.sqlite")
