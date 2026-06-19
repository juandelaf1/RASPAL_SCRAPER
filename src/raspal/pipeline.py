import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field


class Item(BaseModel):
    url: str
    scraped_at: datetime = Field(default_factory=datetime.now)
    data: dict = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)


class Pipeline:
    def __init__(self):
        self.items: list[Item] = []

    def add(self, url: str, data: dict, errors: list[str] | None = None):
        self.items.append(Item(url=url, data=data, errors=errors or []))

    def to_json(self, path: str | Path, indent: int = 2):
        with open(path, "w", encoding="utf-8") as f:
            data = [i.model_dump(mode="json") for i in self.items]
            json.dump(data, f, indent=indent, default=str)

    def to_csv(self, path: str | Path):
        if not self.items:
            return
        fieldnames: list[str] = sorted(
            {k for item in self.items for k in item.data.keys()}
        )
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["url", *fieldnames])
            writer.writeheader()
            for item in self.items:
                row = {"url": item.url, **item.data}
                writer.writerow(row)

    def __len__(self):
        return len(self.items)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.items.clear()
