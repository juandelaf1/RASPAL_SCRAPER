# Getting Started

## Requisitos

- Python 3.10+
- Ollama (con llama3.2 descargado)
- Playwright browsers (`playwright install chromium`)

## Instalacion

```bash
pip install raspal[all]
raspal setup
```

O via Docker (recomendado):

```bash
git clone https://github.com/juandelaf1/RASPAL_SCRAPER.git
cd RASPAL_SCRAPER
docker compose up -d
docker compose run raspal raspal demo
```

## Primeros pasos

1. **Prueba el demo:** `raspal demo`
2. **Scrapea tu primer sitio:** `raspal fetch https://ejemplo.com`
3. **Extrae con IA:** `raspal fetch https://ejemplo.com --extract`
4. **Usa un pipeline:** `raspal run examples/ecommerce-products.yaml`

## Verifica instalacion

```bash
raspal setup        # verifica browsers y Ollama
raspal status       # muestra estado del sistema
raspal version      # version instalada
```
