# Troubleshooting

## Error: "No module named 'raspal'"

```bash
pip install raspal[all]
```

Si usas Docker, asegurate de ejecutar dentro del contenedor:
```bash
docker compose run raspal raspal fetch https://ejemplo.com
```

## Error: "Connection refused" con Ollama

1. Verifica que Ollama este corriendo: `ollama serve`
2. Revisa `OLLAMA_HOST` (default: `http://localhost:11434`)
3. En Docker, espera que el servicio `ollama` termine de iniciar (~10s)

## Error: "Browser not found" con Playwright

```bash
raspal setup
# o manual:
playwright install chromium
```

## Error Unicode en Windows

Si ves caracteres extranos en la terminal, asegurate de usar:
- PowerShell 7+ (no Windows PowerShell)
- Fuente compatible con Unicode (Cascadia Code, Consolas)
- `[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()`

## Error: "timeout" en fetch

Aumenta el timeout en el YAML:
```yaml
timeout: 60
```

Sitios lentos o con mucho JS pueden necesitar 60-120 segundos.

## Error: Cloudflare / Turnstile

Usa `engine: stealth`:
```bash
raspal fetch https://ejemplo.com --engine stealth
```

## La imagen Docker es muy grande

La imagen optimizada pesa ~1.95GB. Es normal dado que incluye Chromium y las dependencias de Playwright. En futuras versiones exploraremos reducir el tamaño.

## Logs y debug

Usa `--verbose` para informacion detallada:
```bash
raspal fetch https://ejemplo.com --verbose
```
