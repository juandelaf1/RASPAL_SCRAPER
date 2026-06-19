from pathlib import Path

from raspal.queue import RequestQueue, QueueItem


def test_push_pop(tmp_path: Path):
    db = tmp_path / "test_queue.sqlite"
    q = RequestQueue(db)
    q.push("https://a.com", priority=1)
    assert q.pending_count() == 1
    item = q.pop()
    assert item is not None
    assert item.url == "https://a.com"
    assert item.priority == 1
    q.close()


def test_pop_empty(tmp_path: Path):
    db = tmp_path / "test_empty.sqlite"
    q = RequestQueue(db)
    assert q.pop() is None
    q.close()


def test_priority_ordering(tmp_path: Path):
    db = tmp_path / "test_priority.sqlite"
    q = RequestQueue(db)
    q.push("https://low.com", priority=1)
    q.push("https://high.com", priority=10)
    item1 = q.pop()
    assert item1 is not None
    assert item1.url == "https://high.com"
    q.close()


def test_complete(tmp_path: Path):
    db = tmp_path / "test_complete.sqlite"
    q = RequestQueue(db)
    q.push("https://a.com")
    item = q.pop()
    assert item is not None
    q.complete(item)
    assert q.pending_count() == 0
    q.close()


def test_retry(tmp_path: Path):
    db = tmp_path / "test_retry.sqlite"
    q = RequestQueue(db)
    q.push("https://a.com", max_retries=2)
    item = q.pop()
    assert item is not None
    # First retry: retries goes 0 -> 1 (< max_retries=2, stays pending)
    q.retry(item, "HTTP 500")
    assert q.pending_count() == 1
    assert q.failed_count() == 0
    item2 = q.pop()
    assert item2 is not None
    assert item2.retries == 1
    # Second retry: retries goes 1 -> 2 (>= max_retries=2, marked failed)
    q.retry(item2, "HTTP 500")
    assert q.pending_count() == 0  # now pending is 0 since it failed
    assert q.failed_count() == 1
    q.close()


def test_failed_count(tmp_path: Path):
    db = tmp_path / "test_failed.sqlite"
    q = RequestQueue(db)
    q.push("https://a.com", max_retries=1)
    item = q.pop()
    assert item is not None
    # retries goes 0 -> 1 (>= max_retries=1, immediately failed)
    q.retry(item, "error")
    assert q.failed_count() == 1
    assert q.pending_count() == 0
    q.close()


def test_context_manager(tmp_path: Path):
    db = tmp_path / "test_ctx.sqlite"
    with RequestQueue(db) as q:
        q.push("https://a.com")
        assert q.pending_count() == 1
    assert q.conn is None


def test_pending_count(tmp_path: Path):
    db = tmp_path / "test_count.sqlite"
    q = RequestQueue(db)
    assert q.pending_count() == 0
    q.push("https://a.com")
    q.push("https://b.com")
    assert q.pending_count() == 2
    q.close()


def test_failed_count(tmp_path: Path):
    db = tmp_path / "test_failed.sqlite"
    q = RequestQueue(db)
    q.push("https://a.com", max_retries=1)
    item = q.pop()
    assert item is not None
    q.retry(item, "error")
    # With max_retries=1, one retry moves it straight to failed
    assert q.failed_count() == 1
    assert q.pending_count() == 0
    q.close()
