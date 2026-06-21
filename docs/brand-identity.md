# RASPAL SCRAPER — Identidad de Marca

## Tagline

**Primario:** "Scraping + IA local. Sin API keys. Sin salir de tu maquina."
**Secundario:** "URL -> JSON estructurado. Un comando. Cero dependencias cloud."
**Terciario:** "El scraper que respeta tu privacidad."

## Propuesta de Valor

> De una URL a JSON estructurado con IA local, sin enviar datos a terceros, sin API keys, en un solo comando.

## Los 3 Casos de Uso Ancla

### 1. Monitor de Precios de E-commerce

**Problema:** Un SaaS necesita trackear precios de 50+ productos de la competencia semanalmente. Soluciones existentes: caras (Firecrawl $99/mes) o requieren enviar datos a terceros.

**Comando:**
```bash
raspal run pipelines/ecommerce-products.yaml
```

**Output:**
```json
{
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "producto": "A Light in the Attic",
  "precio": "£51.77",
  "disponibilidad": "In stock",
  "categoria": "Books",
  "timestamp": "2026-06-21T12:00:00Z"
}
```

**Para quién:** Fundadores de SaaS B2B, analistas de pricing, equipos de producto.

### 2. Extracción de Noticias con Resumen IA

**Problema:** Una periodista de datos necesita procesar 20+ artículos al dia. Quiere extraer titular, fecha, autor y un resumen automatico sin leer cada uno.

**Comando:**
```bash
raspal run pipelines/news-article.yaml
```

**Output:**
```json
{
  "url": "https://example.com/article",
  "titular": "Example Article Title",
  "autor": "Author Name",
  "fecha": "2026-06-21",
  "resumen_ia": "Este articulo trata sobre...",
  "categoria": "technology"
}
```

**Para quién:** Periodistas de datos, investigadores academicos, analistas de medios.

### 3. Agregación de Listados Inmobiliarios

**Problema:** Un agente inmobiliario necesita consolidar listados de 3 portales diferentes para analizar precios de mercado.

**Comando:**
```bash
raspal run pipelines/real-estate-listings.yaml
```

**Output:**
```json
{
  "url": "https://example.com/propiedad/123",
  "direccion": "Calle Example 123",
  "precio": "$250,000",
  "habitaciones": 3,
  "metros_cuadrados": 120,
  "agente": "Inmobiliaria Example"
}
```

**Para quién:** Agentes inmobiliarios, analistas de mercado, inversores.

## Personas Objetivo

### 1. Marcos — Fundador de SaaS B2B
- **Edad:** 30-45
- **Pain point:** Necesita datos de competidores pero las APIs de scraping cuestan $99-500/mes
- **Por que RASPAL:** Gratuito (OS), self-hosted, sin costes recurrentes
- **Donde encontrarlo:** r/SaaS, r/Entrepreneur, Hacker News, Twitter
- **Cuanto pagaria:** $0 (OS) o $79/mes si necesita workers extra

### 2. Ana — Periodista de Datos
- **Edad:** 25-40
- **Pain point:** Necesita extraer datos de sitios de noticias pero le preocupan aspectos legales
- **Por que RASPAL:** Compliance checks integrados, IA local mantiene confidencialidad de fuentes
- **Donde encontrarla:** Twitter/LinkedIn (periodismo de datos), NICAR, IRE
- **Cuanto pagaria:** $0 (OS), donacion si el proyecto le es util

### 3. Carlos — Freelance Web Scraper
- **Edad:** 22-35
- **Pain point:** Tiene multiples clientes con distintos niveles de complejidad (estatico, JS, Cloudflare)
- **Por que RASPAL:** 3 motores (scrapling/playwright/stealth), pipelines YAML reutilizables, Ollama integration
- **Donde encontrarlo:** r/webscraping, Upwork, Fiverr, Discord de scraping
- **Cuanto pagaria:** $0 para proyectos personales, $79/mes si ahorra horas de trabajo

## Jerarquia de Mensajes

### Nivel 1 (10 segundos) — Tagline
"Scraping + IA local. Sin API keys. Sin salir de tu maquina."

### Nivel 2 (60 segundos) — 3 Beneficios Clave
1. **Sin dependencias cloud:** No envias tus datos a nadie. Todo corre en tu maquina con Ollama.
2. **Sin API keys:** No necesitas pagar a OpenAI, Firecrawl ni ningun tercero.
3. **Un solo comando:** Docker + raspal y tienes tu primer JSON estructurado en segundos.

### Nivel 3 (5 minutos) — Demo Funcional
```bash
git clone https://github.com/juandelaf1/RASPAL_SCRAPER.git
cd RASPAL_SCRAPER
docker compose up -d
docker compose run raspal raspal demo
```

## Voz y Tono

- **Idioma:** Español e Ingles (el codigo y CLI en ingles, docs bilingues)
- **Tono:** Directo, honesto, técnico pero accesible
- **Que NO decir:** "revolucionario", "disruptivo", "empoderamos"
- **Que SI decir:** "extrae", "estructura", "automatiza", "en local"
