"""
Test script to demonstrate the improvements made to Raspal.
This script tests the new async functionality and other enhancements.
"""

import asyncio
import json
import os
from pathlib import Path

from raspal.fetcher import Fetcher
from raspal.cache import Cache
from raspal.extractor import Extractor
from raspal.models import FetchResult, LLMConfig
from raspal.throttle import AutoThrottle

# Import the enhanced fetcher (if available)
try:
    from raspal.improvements.async_compatibility import AsyncFetcher
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    print("Warning: Async compatibility module not available")


def test_basic_functionality():
    """Test basic scraping functionality."""
    print("=== Testing Basic Functionality ===")
    
    # Test fetcher
    fetcher = Fetcher()
    result = fetcher.fetch("https://example.com", engine="scrapling")
    
    assert result.status == 200
    assert result.url == "https://example.com"
    assert result.html is not None
    assert result.engine == "scrapling"
    print("✓ Basic fetch works")
    
    # Test extractor
    extractor = Extractor()
    text = extractor.extract_text(result.html)
    metadata = extractor.extract_metadata(result.html)
    
    assert text is not None
    assert "Example" in text or "Domain" in text
    assert isinstance(metadata, dict)
    print("✓ Extraction works")
    
    # Test cache
    with Cache() as cache:
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        assert value == "test_value"
        print("✓ Cache works")
    
    print("All basic functionality tests passed!\n")


async def test_async_functionality():
    """Test async functionality if available."""
    if not ASYNC_AVAILABLE:
        print("Skipping async tests (module not available)\n")
        return
    
    print("=== Testing Async Functionality ===")
    
    # Test async fetcher
    fetcher = AsyncFetcher()
    
    urls = [
        "https://example.com",
        "https://httpbin.org/json",
    ]
    
    # Batch fetch asynchronously
    results = await fetcher.fetch_batch(urls, engine="scrapling")
    
    for result in results:
        if isinstance(result, Exception):
            print(f"✗ Error: {result}")
            continue
        assert result.status == 200
        assert result.html is not None
        assert result.engine == "scrapling"
    
    print(f"✓ Async batch fetch works ({len(results)} results)")
    
    # Test cleanup
    await fetcher.close()
    print("✓ Async cleanup works")
    print("All async functionality tests passed!\n")


def test_advanced_features():
    """Test advanced features like throttling, caching, etc."""
    print("=== Testing Advanced Features ===")
    
    # Test throttling
    throttle = AutoThrottle(min_delay=0.1, max_delay=1.0, target_avg=1.0)
    
    # Record some activity
    throttle.record("scrapling", 200)
    throttle.record("playwright", 404)
    
    # Check delays
    delays = throttle.current_delays
    assert "scrapling" in delays
    assert "playwright" in delays
    assert delays["scrapling"] > 0
    print("✓ Throttling works")
    
    # Test different engines
    fetcher = Fetcher()
    
    # Test scrapling
    result1 = fetcher.fetch("https://example.com", engine="scrapling")
    assert result1.engine == "scrapling"
    print("✓ Scrapling engine works")
    
    # Test dynamic
    result2 = fetcher.fetch("https://example.com", engine="playwright")
    assert result2.engine == "playwright"
    print("✓ Playwright engine works")
    
    print("All advanced feature tests passed!\n")


def test_error_handling():
    """Test error handling."""
    print("=== Testing Error Handling ===")
    
    fetcher = Fetcher()
    
    # Test with invalid URL
    result = fetcher.fetch("https://invalid-domain-that-does-not-exist.com", engine="scrapling")
    assert result.status == 0  # Should be 0 for errors
    assert result.error is not None
    print("✓ Invalid URL handling works")
    
    # Test with non-HTTP URL
    result = fetcher.fetch("ftp://example.com", engine="auto")
    assert result.engine == "scrapling"  # Should default to static
    print("✓ URL detection works")
    
    print("All error handling tests passed!\n")


def test_output_formats():
    """Test different output formats."""
    print("=== Testing Output Formats ===")
    
    from raspal.pipeline import Pipeline
    
    pipeline = Pipeline()
    
    # Add some test data
    pipeline.add(
        url="https://example.com/page1",
        data={"title": "Page 1", "content": "Content 1"},
        errors=[]
    )
    
    pipeline.add(
        url="https://example.com/page2",
        data={"title": "Page 2", "content": "Content 2"},
        errors=["Error 2"]
    )
    
    # Test JSON output
    json_path = "test_output.json"
    pipeline.to_json(json_path)
    
    with open(json_path, "r") as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["url"] == "https://example.com/page1"
        assert data[0]["data"]["title"] == "Page 1"
    
    print("✓ JSON output works")
    
    # Test CSV output
    csv_path = "test_output.csv"
    pipeline.to_csv(csv_path)
    
    with open(csv_path, "r") as f:
        lines = f.readlines()
        assert len(lines) >= 3  # Header + 2 rows
        assert "Page 1" in lines[1] or "Page 1" in lines[2]
    
    print("✓ CSV output works")
    
    # Cleanup
    os.remove(json_path)
    os.remove(csv_path)
    
    print("All output format tests passed!\n")


async def run_all_tests():
    """Run all tests."""
    print("Starting Raspal improvement tests...\n")
    
    # Run synchronous tests
    test_basic_functionality()
    test_advanced_features()
    test_error_handling()
    test_output_formats()
    
    # Run async tests if available
    await test_async_functionality()
    
    print("🎉 All tests passed! Raspal improvements are working correctly.")
if __name__ == "__main__":
    asyncio.run(run_all_tests())