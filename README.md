# Raspal

A reusable Python scraping toolkit combining **Scrapling**, **Playwright**, and **LLM extraction via Ollama**.

## Install

```bash
pip install raspal
```

## Quickstart

```bash
# Fetch and extract text from a URL
raspal fetch https://example.com

# Run a scraping pipeline from a YAML config
raspal run config.yaml
```

## Features

- Adaptive engine: auto-detects between Scrapling (fast) and Playwright (JS-heavy)
- SQLite-based request cache with TTL
- Layered text extraction (trafilatura-style)
- LLM-powered structured extraction via Ollama
- YAML-configured pipelines

## License

MIT
