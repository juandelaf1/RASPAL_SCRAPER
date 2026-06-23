# RASPAL SCRAPER — Reference for AI Agents

RASPAL SCRAPER v0.6.1 is a production-grade web scraping tool with local AI extraction.
PyPI: `pip install raspal` | GitHub: `juandelaf1/RASPAL_SCRAPER`
Docs site: `https://juandelaf1.github.io/RASPAL_SCRAPER/` (pending GitHub Pages activation)

## Install

```bash
# Docker (recommended)
git clone https://github.com/juandelaf1/RASPAL_SCRAPER.git
cd RASPAL_SCRAPER
docker compose up -d
docker compose run raspal raspal demo

# pip
pip install raspal              # base
pip install raspal[fast]        # + selectolax (faster CSS parsing)
pip install raspal[web]         # + web dashboard
pip install raspal[all]         # everything
raspal setup                    # install browsers, verify Ollama
```

## CLI (17 commands)

```bash
# Setup
raspal setup                    # install browsers, verify Ollama
raspal init                     # scaffold project
raspal doctor                   # system diagnostics (Python, Ollama, Playwright)
raspal version                  # show version

# Compliance
raspal compliance https://ejemplo.com  # real robots.txt parsing
raspal validate config.yaml     # validate YAML pipeline

# Fetch
raspal fetch https://ejemplo.com
raspal fetch https://ejemplo.com --engine playwright
raspal fetch https://ejemplo.com --engine stealth

# Async
raspal async-fetch https://ejemplo.com
raspal async-batch https://ejemplo.com https://httpbin.org/json

# Pipeline
raspal run config.yaml

# Queue
raspal queue config.yaml --db queue.sqlite -o results.json

# Reports & Dashboard
raspal report --input results.json --output report.html
raspal serve                    # http://localhost:8462

# Status
raspal status
raspal clear-cache

# Demo
raspal demo                     # scrape books.toscrape.com with real CSS selectors
```

## CI/CD (4 workflows)

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `ci.yml` | push/PR to master | pytest (3.11 + 3.12), ruff lint+format |
| `publish.yml` | tag `v*` | tests → build → PyPI (trusted publishing) |
| `docker-publish.yml` | tag `v*` | tests → build → Docker Hub (`juandelaf/raspal`) |
| `integration.yml` | weekly Mon / manual | Ollama service + Playwright + real HTTP tests |
| `docs.yml` | push master / manual | mkdocs build → deploy to GitHub Pages |

## Trusted Publishing

Configured on PyPI: `juandelaf1/RASPAL_SCRAPER` + `publish.yml`.
Next `v*` tag publishes automatically — no token needed.

## Engines

| Engine | Class | When to use |
|--------|-------|-------------|
| `scrapling` | `Fetcher` | Static HTML, curl_cffi fast requests |
| `playwright` | `DynamicFetcher` | JS-rendered, blocks ads/resources |
| `stealth` | `StealthyFetcher` | Cloudflare/Turnstile, anti-bot pages |
| `auto` | — | Defaults to scrapling |

## Python API

```python
from raspal import Fetcher, Cache, Extractor, LLMExtractor
from raspal import AutoThrottle, RequestQueue, Pipeline

f = Fetcher()
result = f.fetch("https://example.com", engine="auto", cache_ttl=3600)

ext = Extractor()
text = ext.extract_text(result.html)
meta = ext.extract_metadata(result.html)
data = ext.extract_selectors(html, {"title": "h1", "price": ".price"})
data = ext.extract_selectors_fast(html, {"title": "h1"})

from raspal.models import LLMConfig, ChainStep
llm = LLMExtractor()
data = llm.extract(text, LLMConfig(template="product"))
data = llm.extract(text, LLMConfig(output_schema={"name": "", "price": ""}, strict=True))
result = llm.extract_chain(text, [
    ChainStep(name="classify", prompt="Product or article?"),
    ChainStep(name="details", prompt="Extract info",
              output_schema={"title": "", "price": ""}),
])
results = llm.extract_batch([text1, text2], LLMConfig(template="article"))

cache = Cache("cache.sqlite")
cache.get(url, ttl=3600)
cache.set(url, html)

t = AutoThrottle(min_delay=0.5, max_delay=60.0)
t.wait("scrapling")
t.record("scrapling", 200)

q = RequestQueue("queue.sqlite")
q.push("https://example.com", priority=1)
q.pop()
q.complete(item)
q.retry(item, "timeout")

p = Pipeline()
p.add(url="https://x.com", data={"title": "Example"})
p.to_json("results.json")
p.to_csv("results.csv")
```

## YAML Pipeline

```yaml
url: "https://ejemplo.com/productos"
engine: auto
cache_ttl: 3600
extract:
  text: true
  metadata: true
  selectors:
    title: "h1.product-title"
    price: "span.price"
llm:
  model: "llama3.2"
  template: "product"
  prompt: "Extract product name, price, and availability as JSON"
throttle:
  min_delay: 0.5
  max_delay: 60.0
```

## Project Status

### PyPI versions published
`0.1.0` → `0.2.0` → `0.3.0` → `0.4.0` → **`0.6.0`** → **`0.6.1`** (latest)

### What exists
- 6-phase blindaje complete (tests, CI/CD, router refactor, compliance, doctor/demo, docs)
- 81 unit tests (no external deps needed)
- Trusted publishing + Docker Hub publishing
- mkdocs site config (Material theme, bilingual)
- Promotion drafts: Reddit (EN+ES), Product Hunt, Hacker News
- Full doc set: index, getting-started, quickstart-docker, cli-reference, engines, configuration, legal-and-ethics, troubleshooting, brand-identity, reddit-post, product-hunt, hacker-news

### Next steps
1. Activate GitHub Pages (Settings → Pages → "GitHub Actions")
2. Publish promotion drafts: Reddit → HN → Product Hunt
3. Iterate on feedback, plan v0.7.0 features
4. Add integration tests if community contributions grow
