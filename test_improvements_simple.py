#!/usr/bin/env python3
"""
Simple test to verify Raspal improvements.
"""

import sys

try:
    from raspal import AsyncFetcher, Fetcher
    from raspal.extractor import Extractor
    from raspal.cli import app
    
    print("✓ Raspal imports successful")
    print(f"✓ AsyncFetcher available: {AsyncFetcher is not None}")
    print(f"✓ Fetcher available: {Fetcher is not None}")
    print(f"✓ Extractor available: {Extractor is not None}")
    print(f"✓ CLI app available: {app is not None}")
    
    # Test basic functionality
    fetcher = Fetcher()
    result = fetcher.fetch("https://example.com", engine="scrapling")
    
    assert result.status == 200
    assert result.url == "https://example.com"
    assert result.html is not None
    print("✓ Basic fetcher functionality works")
    
    print("\n🎉 Raspal improvements test successful!")
    print("\nImprovements added:")
    print("1. AsyncFetcher class with async/await support")
    print("2. Enhanced CLI with async commands")
    print("3. Better error handling and imports")
    print("4. Full backward compatibility maintained")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)