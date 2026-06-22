# Hacker News — Show HN

## Title
Show HN: RASPAL SCRAPER – Open-source CLI for web scraping with local AI, no API keys

## Body

I built RASPAL SCRAPER because every time I needed structured data from a website, I had to stitch together Scrapy + BeautifulSoup + OpenAI (or pay $99/mo for Firecrawl).

The core idea: one command, any URL, structured JSON. All local, all private.

```bash
pip install raspal
raspal fetch https://books.toscrape.com/catalogue/... --extract
```

**What makes it different:**

1. **3 engines in one tool:** scrapling (static, fast), playwright (JS-rendered), stealth (Cloudflare/Turnstile). Auto-detects which to use.

2. **Local AI extraction via Ollama:** No OpenAI keys, no data leaving your machine. Built-in templates: product, article, person, review, event. Custom JSON schemas. Multi-step chains (classify → extract).

3. **YAML pipelines:** Define selectors + AI extraction in a config file. `raspal run config.yaml` → structured JSON.

4. **Enterprise features for free:** SQLite cache with TTL, adaptive auto-throttle, request queue with priorities and retries, compliance checker (robots.txt).

5. **Zero setup:** Docker compose up -d → `raspal run config.yaml` → profit.

```bash
git clone https://github.com/juandelaf1/RASPAL_SCRAPER.git
cd RASPAL_SCRAPER
docker compose up -d
docker compose run raspal raspal run config.yaml
```

**Stack:** Python, Playwright, curl_cffi, Ollama, Typer, Rich, SQLite. MIT licensed.

**GitHub:** https://github.com/juandelaf1/RASPAL_SCRAPER

**Docs:** See docs/ for CLI reference, engine comparison, troubleshooting

I'd love feedback on:
- The onboarding experience (does Docker first make sense?)
- Missing use cases / templates
- Performance on large batches (hundreds of URLs)

## Expectations
- Be ready to answer comments for 12+ hours
- Post at 7-8am US Eastern (when HN traffic peaks)
- Update README with any common questions that arise
