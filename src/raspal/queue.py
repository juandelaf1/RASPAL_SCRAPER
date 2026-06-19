import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from raspal.exceptions import QueueError


@dataclass
class QueueItem:
    url: str
    priority: int = 0
    engine: str = "auto"
    retries: int = 0
    max_retries: int = 3
    error: str | None = None
    metadata: dict = field(default_factory=dict)
    id: int | None = None


class RequestQueue:
    def __init__(self, db_path: str | Path = "raspal_queue.sqlite"):
        self.db_path = str(db_path)
        self.conn: sqlite3.Connection | None = None
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    priority INTEGER DEFAULT 0,
                    engine TEXT DEFAULT 'auto',
                    retries INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    error TEXT,
                    metadata TEXT DEFAULT '{}',
                    status TEXT DEFAULT 'pending'
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            raise QueueError(f"Failed to open queue at {self.db_path}: {e}") from e

    def push(
        self,
        url: str,
        priority: int = 0,
        engine: str = "auto",
        max_retries: int = 3,
        **metadata,
    ):
        if not self.conn:
            raise QueueError("Queue is closed")
        try:
            self.conn.execute(
                "INSERT INTO queue "
                "(url, priority, engine, max_retries, metadata) "
                "VALUES (?, ?, ?, ?, ?)",
                (url, priority, engine, max_retries, json.dumps(metadata)),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise QueueError(f"Failed to push {url}: {e}") from e

    def pop(self) -> QueueItem | None:
        if not self.conn:
            return None
        try:
            row = self.conn.execute(
                "SELECT id, url, priority, engine, retries, "
                "max_retries, error, metadata "
                "FROM queue WHERE status = 'pending' "
                "ORDER BY priority DESC, id ASC LIMIT 1"
            ).fetchone()
            if row is None:
                return None
            item = QueueItem(
                id=row[0],
                url=row[1],
                priority=row[2],
                engine=row[3],
                retries=row[4],
                max_retries=row[5],
                error=row[6],
                metadata=json.loads(row[7]),
            )
            self.conn.execute(
                "UPDATE queue SET status = 'in_progress' WHERE id = ?", (item.id,)
            )
            self.conn.commit()
            return item
        except sqlite3.Error as e:
            raise QueueError(f"Failed to pop from queue: {e}") from e

    def retry(self, item: QueueItem, error: str):
        if not self.conn:
            return
        item.retries += 1
        item.error = error
        try:
            if item.retries >= item.max_retries:
                self.conn.execute(
                    "UPDATE queue SET retries = ?, error = ?, status = 'failed' WHERE id = ?",
                    (item.retries, error, item.id),
                )
            else:
                self.conn.execute(
                    "UPDATE queue SET retries = ?, error = ?, status = 'pending' WHERE id = ?",
                    (item.retries, error, item.id),
                )
            self.conn.commit()
        except sqlite3.Error as e:
            raise QueueError(f"Failed to retry {item.url}: {e}") from e

    def complete(self, item: QueueItem):
        if not self.conn:
            return
        try:
            self.conn.execute(
                "UPDATE queue SET status = 'completed' WHERE id = ?", (item.id,)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise QueueError(f"Failed to complete {item.url}: {e}") from e

    def pending_count(self) -> int:
        if not self.conn:
            return 0
        try:
            row = self.conn.execute(
                "SELECT COUNT(*) FROM queue WHERE status = 'pending'"
            ).fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0

    def failed_count(self) -> int:
        if not self.conn:
            return 0
        try:
            row = self.conn.execute(
                "SELECT COUNT(*) FROM queue WHERE status = 'failed'"
            ).fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0

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
