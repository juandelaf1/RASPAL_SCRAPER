# Configuration

## YAML Pipeline

```yaml
url: "https://ejemplo.com"
engine: auto            # scrapling, playwright, stealth, auto
cache_ttl: 3600         # segundos (0 para desactivar)
timeout: 30             # segundos

extract:
  text: true            # extraer texto plano
  metadata: true        # extraer meta tags
  use_selectolax: true  # faster CSS parsing (requiere raspal[fast])
  selectors:
    title: "h1.title"
    price: "span.price"

llm:
  model: "llama3.2:3b"
  template: "product"   # product, article, person, review, event
  prompt: "Extrae datos como JSON"
  output_schema:
    name: ""
    price: 0.0
  strict: true          # validar schema

llm_chain:
  - name: classify
    prompt: "Clasifica como producto o articulo"
    output_schema: {"category": ""}
  - name: details
    prompt: "Extrae informacion principal"
    output_schema: {"title": "", "price": ""}

throttle:
  min_delay: 0.5
  max_delay: 60.0

queue:
  concurrency: 3
  max_retries: 3
```

## Variables de entorno

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | URL del servidor Ollama |
| `RASPAL_CACHE_DIR` | `~/.raspal/cache` | Directorio de cache |
| `RASPAL_DB_DIR` | `~/.raspal/db` | Directorio de bases de datos |
| `PLAYWRIGHT_BROWSERS_PATH` | `auto` | Ruta a browsers Playwright |
