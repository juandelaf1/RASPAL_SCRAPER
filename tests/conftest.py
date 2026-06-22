import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


SAMPLE_HTML = """<!DOCTYPE html>
<html><head><title>Test Page</title><meta name="description" content="Test description">
</head><body>
<h1 class="title">Test Product</h1>
<span class="price">$29.99</span>
<p class="description">A great product for testing</p>
<div class="rating">4.5</div>
</body></html>"""


@pytest.fixture
def sample_html():
    return SAMPLE_HTML


@pytest.fixture
def sample_url():
    return "https://example.com"


@pytest.fixture
def sample_yaml_config(tmp_path: Path):
    config = tmp_path / "test_config.yaml"
    config.write_text("""
url: "https://example.com"
engine: scrapling
extract:
  text: true
  metadata: true
""")
    return config


@pytest.fixture
def tmp_db(tmp_path: Path):
    return tmp_path / "test.sqlite"
