#!/usr/bin/env python3
"""
Benchmark Raspal sync vs async fetch performance.
"""

import asyncio
import time

from raspal import AsyncFetcher, Fetcher


URLS = [
    "https://example.com",
    "https://httpbin.org/json",
    "https://httpbin.org/uuid",
    "https://httpbin.org/ip",
]


def benchmark_sync():
    """Benchmark synchronous fetching."""
    print("\n=== Synchronous Fetch Benchmark ===")
    fetcher = Fetcher()

    start = time.perf_counter()
    results = []
    for url in URLS:
        result = fetcher.fetch(url, engine="scrapling")
        results.append(result.status)
    elapsed = time.perf_counter() - start

    print(f"  URLs: {len(URLS)}")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Statuses: {results}")
    return elapsed


async def benchmark_async():
    """Benchmark asynchronous fetching."""
    print("\n=== Async Fetch Benchmark ===")
    async with AsyncFetcher() as fetcher:
        start = time.perf_counter()
        results = await fetcher.fetch_batch(URLS)
        elapsed = time.perf_counter() - start

        statuses = [
            getattr(result, "status", 0)
            if not isinstance(result, Exception)
            else "ERROR"
            for result in results
        ]

        print(f"  URLs: {len(URLS)}")
        print(f"  Time: {elapsed:.2f}s")
        print(f"  Statuses: {statuses}")
        return elapsed


def main():
    """Run benchmarks."""
    sync_time = benchmark_sync()
    async_time = asyncio.run(benchmark_async())

    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Synchronous: {sync_time:.2f}s")
    print(f"Async:       {async_time:.2f}s")
    print(f"Speedup:     {sync_time / async_time:.2f}x" if async_time > 0 else "N/A")
    print("=" * 60)


if __name__ == "__main__":
    main()
