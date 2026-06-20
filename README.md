# **RΛSPΛL**

> Scraping inteligente. Extracción potente. Sin servidores, sin nubes, sin límites.

**RΛSPΛL** es un toolkit Python todo-en-uno para web scraping y extracción de datos potenciado por IA local. Combina **Scrapling**, **Playwright** y **Ollama** para ofrecerte un pipeline completo: fetch, extrae y estructura datos con un solo comando.

```bash
pip install raspal
raspal fetch https://ejemplo.com
```

---

## ¿Por qué RΛSPΛL?

| Problema | Solución RΛSPΛL |
|----------|----------------|
| Páginas estáticas lentas | Scrapling con curl_cffi |
| JavaScript pesado | Playwright headless con bloqueo de anuncios |
| Cloudflare / Turnstile | Stealth bypass automático |
| Datos no estructurados | LLM local con Ollama (privado, sin API keys) |
| Rate limiting | AutoThrottle adaptativo |
| Múltiples URLs | AsyncFetcher concurrente |
| Repetir requests | Caché SQLite con TTL |

---

## ⚡ Uso rápido

### CLI

```bash
# Fetch básico
raspal fetch https://ejemplo.com

# Con motor específico
raspal fetch https://ejemplo.com --engine playwright
raspal fetch https://ejemplo.com --engine stealth

# Fetch asíncrono (más rápido)
raspal async_fetch https://ejemplo.com

# Múltiples URLs en paralelo
raspal async_batch https://ejemplo.com https://httpbin.org/json

# Pipeline desde YAML
raspal run config.yaml

# Cola de URLs con prioridades
raspal queue config.yaml --db queue.sqlite -o results.json

# Estado del throttle
raspal status

# Limpiar caché
raspal clear_cache
```

### Python API

```python
from raspal import Fetcher, Extractor, LLMExtractor

# 1. Fetch
f = Fetcher()
result = f.fetch("https://ejemplo.com", engine="auto")
html = result.html

# 2. Extraer texto y metadata
ext = Extractor()
texto = ext.extract_text(html)
metadata = ext.extract_metadata(html)

# 3. Extracción selectores CSS
data = ext.extract_selectors(html, {
    "titulo": "h1",
    "precio": ".price",
    "descripcion": ".description"
})

# 4. Extracción con IA local (Ollama)
llm = LLMExtractor()
producto = llm.extract(texto, template="product")
# → {"name": "...", "brand": "...", "price": "...", "availability": "..."}
```

### Pipelines YAML

```yaml
# config.yaml
url: "https://ejemplo.com/productos"
engine: auto
extract:
  text: true
  metadata: true
  selectors:
    title: "h1.product-title"
    price: "span.price"
llm:
  template: "product"
  prompt: "Extrae nombre, precio y disponibilidad como JSON"
```

```bash
raspal run config.yaml
```

---

## 🧠 Extracción con IA (Ollama)

Sin API keys. Sin costos. Sin enviar datos a terceros.

```python
# Templates predefinidos
llm.extract(texto, template="product")   # nombre, marca, precio...
llm.extract(texto, template="article")   # título, autor, fecha...
llm.extract(texto, template="person")    # nombre, rol, contacto...
llm.extract(texto, template="review")    # rating, pros, contras...
llm.extract(texto, template="event")     # fecha, lugar, organizador...

# Esquema JSON personalizado
llm.extract(texto, template="product", output_schema={
    "name": "",
    "price": 0.0,
    "rating": 0.0,
    "in_stock": False
})

# Cadenas multi-paso (classify → extract)
chain = [
    ChainStep(name="categoria", prompt="¿Esto es un producto o un artículo?"),
    ChainStep(name="detalles", prompt="Extrae información clave",
              output_schema={"title": "", "price": ""}),
]
llm.extract_chain(texto, chain)
```

---

## 🚀 Async para alta escalabilidad

```python
from raspal import AsyncFetcher

async with AsyncFetcher(max_workers=8) as fetcher:
    results = await fetcher.fetch_batch([
        "https://ejemplo.com/pagina1",
        "https://ejemplo.com/pagina2",
        "https://ejemplo.com/pagina3",
    ])
```

Procesa cientos de URLs en paralelo con aislamiento por proceso para Playwright.

---

## 🎛️ Motores

| Motor | Librería | Ideal para |
|-------|----------|-----------|
| `scrapling` | curl_cffi | HTML estático, rápida |
| `playwright` | Playwright | JS pesado, SPAs |
| `stealth` | Playwright + anti-detect | Cloudflare, Turnstile |
| `auto` | — | Selección automática |

---

## 📦 Componentes

| Componente | Descripción |
|-----------|-------------|
| `Fetcher` | Fetch multi-motor con caché y throttle |
| `AsyncFetcher` | Versión asíncrona con ProcessPoolExecutor |
| `Extractor` | Extracción de texto, metadata y selectores |
| `LLMExtractor` | Extracción estructurada con Ollama |
| `Cache` | Caché SQLite con TTL configurable |
| `AutoThrottle` | Control adaptativo de velocidad |
| `RequestQueue` | Cola persistente con prioridades y reintentos |
| `Pipeline` | Pipeline de recolección con salida JSON/CSV |
| `Router` | Orquestador completo desde YAML |

---

## 📊 Salida

```python
pipeline = Pipeline()
pipeline.add(url="https://...", data={...})
pipeline.to_json("resultados.json")
pipeline.to_csv("resultados.csv")
```

---

## ⚙️ Instalación

```bash
pip install raspal           # base
pip install raspal[fast]     # + selectolax (CSS más rápido)
pip install raspal[all]      # todo
```

Requiere Python ≥ 3.11 y [Ollama](https://ollama.com) para extracción con IA.

---

## 📄 Licencia

MIT — haz lo que quieras.
