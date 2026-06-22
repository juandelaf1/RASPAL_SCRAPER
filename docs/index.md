# RASPAL SCRAPER

**Scraping + IA local. Sin API keys. Sin salir de tu maquina.**

RASPAL SCRAPER extrae datos estructurados de cualquier web usando IA local.
Sin enviar datos a terceros. Sin pagar APIs. Un solo comando.

```bash
pip install raspal
raspal fetch https://ejemplo.com
```

## Por qué RASPAL?

| Necesitas... | Firecrawl | Apify | Browse.ai | Scrapy | **RASPAL** |
|---|---|---|---|---|---|
| Sin enviar datos a terceros | ❌ | ❌ | ❌ | ✅ | **✅** |
| Sin pagar por API | ❌ | ❌ | ❌ | ✅ | **✅** |
| Un solo comando | ❌ | ❌ | ❌ | ❌ | **✅** |
| IA local (Ollama) | ❌ | ❌ | ❌ | ❌ | **✅** |
| Modo stealth | ❌ | ❌ | ❌ | ❌ | **✅** |
| Docker listo | ❌ | ✅ | ❌ | ❌ | **✅** |
| Open source (MIT) | ❌ | ❌ | ❌ | ✅ | **✅** |
| Precio | $10+/mes | $49+/mes | $49+/mes | Gratis | **Gratis** |

## Inicio rápido

=== "Docker (recomendado)"

    ```bash
    git clone https://github.com/juandelaf1/RASPAL_SCRAPER.git
    cd RASPAL_SCRAPER
    docker compose up -d
    docker compose run raspal raspal demo
    ```

=== "pip"

    ```bash
    pip install raspal
    raspal setup
    raspal fetch https://ejemplo.com
    ```

=== "YAML Pipeline"

    ```yaml
    # config.yaml
    url: "https://ejemplo.com/productos"
    engine: auto
    extract:
      text: true
      selectors:
        title: "h1.product-title"
        price: "span.price"
    llm:
      template: "product"
    ```

    ```bash
    raspal run config.yaml
    ```

## 3 motores

| Motor | Librería | Ideal para |
|-------|----------|-----------|
| `scrapling` | curl_cffi | HTML estático, rápida |
| `playwright` | Playwright | JS pesado, SPAs |
| `stealth` | Playwright + anti-detect | Cloudflare, Turnstile |
| `auto` | — | Selección automática |

## Componentes

| Componente | Descripción |
|-----------|-------------|
| `Fetcher` | Fetch multi-motor con caché y throttle |
| `AsyncFetcher` | Versión asíncrona |
| `Extractor` | Texto, metadata y selectores CSS |
| `LLMExtractor` | Extracción estructurada con Ollama |
| `Cache` | Caché SQLite con TTL |
| `AutoThrottle` | Control adaptativo de velocidad |
| `RequestQueue` | Cola persistente con prioridades |
| `Pipeline` | Pipeline con salida JSON/CSV |
| `Router` | Orquestador desde YAML |

## Licencia

MIT — haz lo que quieras.
