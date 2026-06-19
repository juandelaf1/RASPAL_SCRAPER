from raspal.extractor import Extractor


SIMPLE_HTML = """
<html><head><title>Test Page</title>
<meta name="description" content="A test page">
</head>
<body>
<h1>Main Title</h1>
<p class="content">Hello world</p>
<span class="price">$10.99</span>
</body></html>
"""


def test_extract_text():
    ext = Extractor()
    text = ext.extract_text(SIMPLE_HTML)
    assert text is not None
    assert "Main Title" in text
    assert "Hello world" in text


def test_extract_metadata():
    ext = Extractor()
    meta = ext.extract_metadata(SIMPLE_HTML)
    # trafilatura may pick h1 as title, not the <title> tag
    assert "title" in meta
    assert meta["title"] is not None


def test_extract_selectors():
    ext = Extractor()
    result = ext.extract_selectors(
        SIMPLE_HTML, {"title": "h1", "price": ".price"}
    )
    assert result["title"] == "Main Title"
    assert result["price"] == "$10.99"


def test_extract_selectors_missing():
    ext = Extractor()
    result = ext.extract_selectors(SIMPLE_HTML, {"missing": ".does-not-exist"})
    assert result["missing"] is None


def test_extract_selectors_fast():
    ext = Extractor()
    result = ext.extract_selectors_fast(
        SIMPLE_HTML, {"title": "h1", "price": ".price"}
    )
    assert result["title"] == "Main Title"
    assert result["price"] == "$10.99"


def test_extract_selectors_fast_fallback():
    """If selectolax not installed, falls back to scrapling parser."""
    ext = Extractor()
    result = ext.extract_selectors_fast(SIMPLE_HTML, {"h1": "h1"})
    assert result["h1"] is not None


def test_empty_html():
    ext = Extractor()
    text = ext.extract_text("<html></html>")
    # trafilatura might return None or empty string for no content
    assert text is None or text.strip() == ""
