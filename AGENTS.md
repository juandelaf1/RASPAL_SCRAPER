# Raspal — Reference for AI Agents

Raspal is a Python scraping toolkit. Installed in this environment.

## Install

```bash
pip install raspal          # base
pip install raspal[fast]    # + selectolax (faster CSS parsing)
pip install raspal[all]     # everything
```

## CLI

```bash
# Fetch a URL
raspal fetch https://ejemplo.com
raspal fetch https://ejemplo.com --engine playwright
raspal fetch https://ejemplo.com --engine stealth

# Run YAML pipeline
raspal run config.yaml

# Process a URL queue
raspal queue config.yaml --db queue.sqlite -o results.json

# Show throttle status
raspal status
```

## Engines

| Engine | Scrapling class | When to use |
|--------|----------------|-------------|
| `scrapling` | `Fetcher` | Static HTML, curl_cffi fast requests |
| `playwright` | `DynamicFetcher` | JS-rendered, blocks ads/resources |
| `stealth` | `StealthyFetcher` | Cloudflare/Turnstile, anti-bot pages |
| `auto` | — | Defaults to scrapling |

## Python API

```python
from raspal import Fetcher, Cache, Extractor, LLMExtractor
from raspal import AutoThrottle, RequestQueue, Pipeline

# === FETCH ===
f = Fetcher()
result = f.fetch("https://example.com", engine="auto", cache_ttl=3600)
# result.html, result.text, result.status, result.cached, result.engine

# === EXTRACT ===
ext = Extractor()
text = ext.extract_text(result.html)
meta = ext.extract_metadata(result.html)
data = ext.extract_selectors(html, {"title": "h1", "price": ".price"})
data = ext.extract_selectors_fast(html, {"title": "h1"})  # uses selectolax

# === LLM EXTRACTION (Ollama) ===
from raspal.models import LLMConfig
llm = LLMExtractor()
data = llm.extract(text, LLMConfig(model="llama3.2", prompt="Extract product name and price"))

# === CACHE ===
cache = Cache("my_cache.sqlite")
cache.get(url, ttl=3600)
cache.set(url, html)

# === AUTOTHROTTLE ===
t = AutoThrottle(min_delay=0.5, max_delay=60.0)
t.wait("scrapling")   # blocks if needed
t.record("scrapling", 200)  # auto-adjusts delay
t.record("scrapling", 429)  # doubles delay on rate limit

# === REQUEST QUEUE ===
q = RequestQueue("queue.sqlite")
q.push("https://example.com/page1", priority=1)
q.push("https://example.com/page2", priority=2)
item = q.pop()           # returns highest-priority item
q.complete(item)         # marks done
q.retry(item, "timeout") # retries up to max_retries
q.pending_count()

# === PIPELINE (collect results) ===
p = Pipeline()
p.add(url="https://x.com", data={"title": "Example"})
p.to_json("results.json")
p.to_csv("results.csv")
```

## YAML Pipeline (`config.yaml`)

```yaml
url: "https://ejemplo.com/productos"
engine: auto
cache_ttl: 3600
extract:
  text: true
  metadata: true
  use_selectolax: true
  selectors:
    title: "h1.product-title"
    price: "span.price"
llm:
  model: "llama3.2"
  prompt: "Extract product name, price, and availability as JSON"
throttle:
  min_delay: 0.5
  max_delay: 60.0
```

Run: `raspal run config.yaml`
