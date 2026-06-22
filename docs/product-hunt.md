# Product Hunt Launch — RASPAL SCRAPER

## Tagline
URL → structured JSON with local AI. No API keys. No data leaving your machine.

## Hunter pitch
RASPAL SCRAPER is an open-source CLI tool that extracts structured data from any website using local AI. Three engines (scrapling, playwright, stealth) handle everything from static HTML to Cloudflare-protected pages. Built-in YAML pipelines, cache, auto-throttle, and request queue. Docker one-liner or pip install.

## Why now?
Firecrawl costs $99/mo. Browse.ai costs $49/mo. OpenAI charges per token AND your data leaves your machine. RASPAL is free (MIT), runs 100% locally, and needs zero API keys.

## Key features
- 3 engines: static (fast), JS (Playwright), anti-bot (stealth)
- Local AI extraction via Ollama — templates for product, article, person, review, event
- YAML pipelines with CSS selectors + AI fallback
- Built-in: cache (SQLite), auto-throttle, request queue, compliance checker
- Docker + pip install — 30 seconds to first result
- Async batch processing (hundreds of URLs in parallel)

## Target audience
- SaaS founders needing competitor pricing data
- Data journalists extracting articles ethically
- Freelance scrapers with multiple clients
- Developers who want local AI without API costs

## Call to action
```bash
docker compose up -d
docker compose run raspal raspal demo
```

Or: `pip install raspal && raspal fetch https://ejemplo.com`

## First comment (post-launch)
"Hey HN! I built RASPAL because I was tired of stitching together Scrapy + BeautifulSoup + OpenAI and sending all my data to third parties. Everything runs locally via Ollama. MIT licensed. Feedback welcome!"

## Tags
#opensource #webscraping #ai #ollama #python #docker #privacy

## Images to include
- Screenshot of `raspal fetch https://books.toscrape.com` output
- Screenshot of `raspal doctor` diagnostics
- Architecture diagram: URL → Fetcher → Extractor → LLM → JSON
