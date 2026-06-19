import sqlite3
import time
from pathlib import Path
from typing import Self

from raspal.exceptions import CacheError


class Cache:
    def __init__(self, db_path: str | Path = "raspal_cache.sqlite"):
        self.db_path = str(db_path)
        self.conn: sqlite3.Connection | None = None
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS cache "
                "(url TEXT PRIMARY KEY, html TEXT, fetched_at REAL)"
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise CacheError(f"Failed to open cache at {self.db_path}: {e}") from e

    def get(self, url: str, ttl: int = 3600) -> str | None:
        if not self.conn:
            return None
        try:
            row = self.conn.execute(
                "SELECT html, fetched_at FROM cache WHERE url = ?", (url,)
            ).fetchone()
            if row is None:
                return None
            html, fetched_at = row
            if time.time() - fetched_at > ttl:
                self.conn.execute("DELETE FROM cache WHERE url = ?", (url,))
                self.conn.commit()
                return None
            return html
        except sqlite3.Error as e:
            raise CacheError(f"Failed to read cache for {url}: {e}") from e

    def set(self, url: str, html: str):
        if not self.conn:
            return
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO cache (url, html, fetched_at) VALUES (?, ?, ?)",
                (url, html, time.time()),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise CacheError(f"Failed to write cache for {url}: {e}") from e

    def clear(self, url: str | None = None):
        if not self.conn:
            return
        try:
            if url:
                self.conn.execute("DELETE FROM cache WHERE url = ?", (url,))
            else:
                self.conn.execute("DELETE FROM cache")
            self.conn.commit()
        except sqlite3.Error as e:
            raise CacheError(f"Failed to clear cache: {e}") from e

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
            finally:
                self.conn = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.close()
