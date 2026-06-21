# Engines

## Comparativa

| Engine | Clase | Ideal para | Velocidad | JS | Anti-bot |
|--------|-------|-----------|-----------|-----|----------|
| `scrapling` | `Fetcher` | HTML estatico, APIs REST | Alta | No | Baja |
| `playwright` | `DynamicFetcher` | SPAs, JS pesado, paginas modernas | Media | Si | Media |
| `stealth` | `StealthyFetcher` | Cloudflare, Turnstile, sites con proteccion | Baja | Si | Alta |
| `auto` | — | Uso general (scrapling por defecto) | Variable | No | Baja |

## Cuando usar cada uno

- **scrapling:** Ideal para paginas HTML simples, documentacion, blogs, directorios sin JS. Mas rapido y con menos recursos.
- **playwright:** Necesario cuando el contenido se carga via JavaScript (SPAs como React, Vue, Angular). Bloquea anuncios y recursos innecesarios.
- **stealth:** Para sitios protegidos por Cloudflare, Turnstile o sistemas anti-bot. Usa patrones de navegacion realista.

## Seleccion automatica

Con `engine: auto`, RASPAL intenta `scrapling` primero. Si falla, no hace fallback automatico. Configura manualmente el engine si encuentras errores.

## Performance

scrapling es ~10x mas rapido que playwright/stealth para paginas estaticas. playwright y stealth tienen overhead por el navegador headless (~200ms adicionales por request).
