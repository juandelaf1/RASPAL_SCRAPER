import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path


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
        self.conn = sqlite3.connect(str(db_path))
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

    def push(
        self, url: str, priority: int = 0, engine: str = "auto",
        max_retries: int = 3, **metadata,
    ):
        self.conn.execute(
            "INSERT INTO queue "
            "(url, priority, engine, max_retries, metadata) "
            "VALUES (?, ?, ?, ?, ?)",
            (url, priority, engine, max_retries, json.dumps(metadata)),
        )
        self.conn.commit()

    def pop(self) -> QueueItem | None:
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
        self.conn.execute("UPDATE queue SET status = 'in_progress' WHERE id = ?", (item.id,))
        self.conn.commit()
        return item

    def retry(self, item: QueueItem, error: str):
        item.retries += 1
        item.error = error
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

    def complete(self, item: QueueItem):
        self.conn.execute("UPDATE queue SET status = 'completed' WHERE id = ?", (item.id,))
        self.conn.commit()

    def pending_count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) FROM queue WHERE status = 'pending'").fetchone()
        return row[0]

    def failed_count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) FROM queue WHERE status = 'failed'").fetchone()
        return row[0]

    def close(self):
        self.conn.close()
