import sqlite3
import json
import time
from pathlib import Path


class Cache:
    def __init__(self, db_path: str | Path = "raspal_cache.sqlite"):
        self.conn = sqlite3.connect(str(db_path))
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (url TEXT PRIMARY KEY, html TEXT, fetched_at REAL)"
        )

    def get(self, url: str, ttl: int = 3600) -> str | None:
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

    def set(self, url: str, html: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (url, html, fetched_at) VALUES (?, ?, ?)",
            (url, html, time.time()),
        )
        self.conn.commit()

    def clear(self, url: str | None = None):
        if url:
            self.conn.execute("DELETE FROM cache WHERE url = ?", (url,))
        else:
            self.conn.execute("DELETE FROM cache")
        self.conn.commit()

    def close(self):
        self.conn.close()
