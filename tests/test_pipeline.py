from pathlib import Path
import json

from raspal.pipeline import Pipeline, Item


def test_pipeline_add():
    p = Pipeline()
    p.add(url="https://a.com", data={"title": "Hello"})
    assert len(p) == 1
    assert p.items[0].url == "https://a.com"
    assert p.items[0].data["title"] == "Hello"


def test_pipeline_to_json(tmp_path: Path):
    p = Pipeline()
    p.add(url="https://a.com", data={"title": "Hello"})
    out = tmp_path / "out.json"
    p.to_json(out)
    with open(out) as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["url"] == "https://a.com"
    assert data[0]["data"]["title"] == "Hello"


def test_pipeline_to_csv(tmp_path: Path):
    p = Pipeline()
    p.add(url="https://a.com", data={"title": "Hello", "price": "10"})
    p.add(url="https://b.com", data={"title": "World", "price": "20"})
    out = tmp_path / "out.csv"
    p.to_csv(out)
    with open(out, newline="") as f:
        lines = f.read().strip().split("\n")
    assert "url" in lines[0]
    assert "Hello" in lines[1]
    assert "World" in lines[2]


def test_pipeline_empty_json(tmp_path: Path):
    p = Pipeline()
    out = tmp_path / "empty.json"
    p.to_json(out)
    with open(out) as f:
        data = json.load(f)
    assert data == []


def test_pipeline_empty_csv(tmp_path: Path):
    p = Pipeline()
    out = tmp_path / "empty.csv"
    p.to_csv(out)  # Should not crash
    assert not out.exists() or out.stat().st_size == 0


def test_pipeline_context_manager():
    with Pipeline() as p:
        p.add(url="https://a.com", data={"x": 1})
        assert len(p) == 1
    assert len(p.items) == 0


def test_item_model():
    item = Item(url="https://a.com", data={"title": "Test"}, errors=["err1"])
    assert item.url == "https://a.com"
    assert item.errors == ["err1"]
