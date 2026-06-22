# Reddit Posts — RASPAL SCRAPER

---

## 🇬🇧 English — r/webscraping

**Title:**
I built a CLI that scrapes any URL and extracts structured data with local AI — no API keys, no data leaving your machine (Docker, open source)

**Body:**
```
TL;DR: pip install raspal → raspal fetch URL → structured JSON. All local, all private.

I was tired of stitching together Scrapy + BeautifulSoup + OpenAI (or paying $99/mo for Firecrawl). Built RASPAL SCRAPER instead:

• 3 engines: Scrapling (fast), Playwright (JS), Stealth (anti-bot/Cloudflare)
• Local AI extraction via Ollama — templates: product, article, person, review, event
• YAML pipelines with CSS selectors + AI fallback
• SQLite cache, auto-throttle, request queue with priorities
• Compliance checker (robots.txt + sensitive domains)
• `raspal doctor` — full system diagnostics

The pitch in one command:
  docker compose up -d
  docker compose run raspal raspal run config.yaml
  → structured JSON

MIT licensed. Would love feedback on:
• Onboarding experience (Docker vs pip install)
• What use cases I'm missing
• How it compares to your current stack

Repo: https://github.com/juandelaf1/RASPAL_SCRAPER
PyPI: pip install raspal
```

---

## 🇪🇸 Español — r/devsarg / r/programacion

**Título:**
Hice una CLI que extrae datos estructurados de cualquier web con IA local — sin API keys, sin que tus datos salgan de tu maquina

**Cuerpo:**
```
TL;DR: pip install raspal → raspal fetch URL → JSON estructurado. Todo local, todo privado.

Me canse de estar usando Scrapy + BeautifulSoup + OpenAI (o pagando $99/mes por Firecrawl) cada vez que necesitaba datos de una web. Construi RASPAL SCRAPER:

• 3 motores: Scrapling (rapido), Playwright (JS), Stealth (anti-bot/Cloudflare)
• Extraccion con IA local via Ollama — templates: producto, articulo, persona, resena, evento
• Pipelines YAML con selectores CSS + IA
• Cache SQLite, auto-throttle, cola de requests con prioridades
• Verificador de compliance (robots.txt + dominios sensibles)
• `raspal doctor` — diagnostico completo del sistema

El pitch en un comando:
  docker compose up -d
  docker compose run raspal raspal run config.yaml
  → JSON estructurado

Licencia MIT. Me encantaria feedback sobre:
• La experiencia de onboarding (Docker vs pip install)
• Que casos de uso me faltan
• Como se compara con tu stack actual

Repo: https://github.com/juandelaf1/RASPAL_SCRAPER
PyPI: pip install raspal
```

---

## Reglas de publicación

- Publicar un lunes, martes o miércoles por la mañana (US time)
- Responder TODOS los comentarios en las primeras 6 horas
- Si alguien reporta un bug, agradecer públicamente y decir qué vas a hacer
- No borrar comentarios negativos
- Publicar en r/webscraping y r/selfhosted primero (ingles), luego r/devsarg (español)
