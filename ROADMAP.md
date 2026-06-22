# RASPAL SCRAPER — ROADMAP

> Este documento refleja la dirección del proyecto. Las fechas son orientativas,
> no compromisos. El orden de prioridad cambia según el feedback de usuarios reales.

---

## ✅ v0.5.4 — Estado actual (Jun 2026)

- CLI completo con 15 comandos
- 3 motores de scraping: scrapling, playwright, stealth
- Extracción con IA local via Ollama (6 templates, chains multi-paso)
- Cache SQLite con TTL + AutoThrottle adaptativo
- Cola de requests con prioridades y reintentos
- Pipelines YAML configurables
- Dashboard web (FastAPI + HTMX)
- Docker multi-arch + docker-compose con Ollama integrado
- CI/CD para PyPI y Docker Hub
- 10 templates YAML de ejemplo
- Documentación completa (10 docs + AGENTS.md)
- Compliance checker + docs de ética y legalidad

---

## 🔄 v0.6.0 — Blindaje y estabilidad (próximas 2-4 semanas)

> Objetivo: que el producto funcione de forma impecable en cualquier máquina
> antes de mostrárselo a ningún usuario externo.

- [ ] Tests con mocks — ningún test requiere Ollama ni red para ejecutarse
- [ ] CI ejecuta pytest + ruff en cada push a main
- [ ] CI como requisito para publicar a PyPI y Docker Hub
- [ ] `raspal doctor` — diagnóstico completo del entorno
- [ ] `raspal demo` — demostración sin configuración previa
- [ ] Compliance checker real con parseo de robots.txt (urllib.robotparser)
- [ ] Refactorizar Router — eliminar duplicación de código (~70%)
- [ ] `PUBLIC_API.md` — contrato de API pública estable
- [ ] `CONTRIBUTING.md` + `SECURITY.md`
- [ ] Badges de CI en README
- [ ] Metadata del repositorio GitHub (description + topics)

---

## 🎯 v0.7.0 — Primeros usuarios reales (1-2 meses)

> Objetivo: conseguir 10 usuarios externos que usen RASPAL en producción
> y den feedback real. Nada de esta fase se construye sin ese feedback.

- [ ] Lanzamiento en r/webscraping y r/Python
- [ ] Show HN en Hacker News
- [ ] Soporte activo de issues en < 24h
- [ ] CHANGELOG actualizado semanalmente
- [ ] Iteraciones basadas en feedback real (sin roadmap predefinido aquí)

---

## 💰 v1.0.0 — Producto comercial (3-6 meses)

> Objetivo: primera versión con modelo de negocio funcionando.
> Solo se construye después de tener 50+ usuarios activos.

- [ ] Sistema de licencias (open core: Free + Pro)
- [ ] Tier Pro: workers concurrentes, soporte prioritario, SLA
- [ ] Billing integrado (LemonSqueezy)
- [ ] Template marketplace — pipelines YAML de la comunidad
- [ ] API REST pública
- [ ] Landing page con pricing

---

## 🧠 v1.5.0 — RASPAL Dataset Studio (PREMIUM)

> **Por qué existe esta feature:**
> El 90% de los datos disponibles en la web no están etiquetados.
> Etiquetar datos manualmente es caro (Scale AI cobra $0.05-2.00 por item).
> RASPAL puede automatizar el etiquetado usando IA local, generando datasets
> listos para entrenar modelos a una fracción del coste.
>
> **Para quién:**
> Equipos de ML y data science que necesitan datasets de entrenamiento
> a partir de fuentes web, sin depender de servicios externos ni exponer sus datos.
>
> **Cuándo se construye:**
> Cuando al menos 5 usuarios actuales lo pidan explícitamente o lo estén
> haciendo manualmente con el output actual de RASPAL.

### Funcionalidades planificadas

**Exportación a formatos ML nativos:**
- JSONL para fine-tuning de LLMs (formato OpenAI, Hugging Face)
- CSV con columnas `text`, `label`, `confidence` para clasificación clásica
- Parquet para datasets grandes (compatible con pandas, polars, spark)
- Formato Hugging Face Datasets directo (`datasets.Dataset`)
- CoNLL para NER (Named Entity Recognition)

**Esquemas de etiquetado configurables en YAML:**
```yaml
url: "https://reviews.example.com"
engine: auto
ml_labeling:
  task: classification
  labels:
    - positive
    - negative
    - neutral
  confidence_threshold: 0.85
  output_format: jsonl
  include_raw_text: true
  validation_split: 0.2
```

**Tareas de etiquetado soportadas:**
- Clasificación de texto (categorías personalizadas)
- Análisis de sentimiento (positivo / negativo / neutro)
- NER — extracción de entidades (personas, lugares, organizaciones, productos)
- Q&A — generación de pares pregunta-respuesta para fine-tuning
- Resumen — pares texto-resumen para modelos de summarization
- Clasificación de intención (para chatbots y asistentes)

**Control de calidad:**
- Score de confianza por etiqueta
- Filtro automático de items con baja confianza
- Estadísticas del dataset: distribución de clases, balance, outliers
- Deduplicación automática antes de exportar
- Reporte HTML de calidad del dataset

**Integración con el ecosistema ML:**
- Push directo a Hugging Face Hub (datasets privados o públicos)
- Compatible con LabelStudio para revisión humana posterior
- Export a Argilla para anotación colaborativa
- Webhook al terminar (para pipelines de entrenamiento automatizados)

**Precio sugerido (a validar con usuarios):**
- Incluido en tier Pro: hasta 10.000 items etiquetados/mes
- Tier Dataset (nuevo): $149/mes — items ilimitados, todos los formatos,
  push a Hugging Face Hub, soporte prioritario
- Enterprise: precio negociado — SLA, modelos de etiquetado personalizados,
  integración con infraestructura ML del cliente

---

## 🌐 v2.0.0 — RASPAL Cloud (futuro lejano)

> Solo si hay demanda validada de usuarios que no quieren self-host.
> Managed infrastructure con Ollama preinstalado.
> Pago por uso: $0.01-0.05 por request procesado.

---

## ❌ Fuera del scope (no se construirá)

- **Modelo propio de scraping**: Ollama + modelos existentes son suficientes
- **Bypass activo de CAPTCHAs**: fuera de los límites legales y éticos del proyecto
- **Almacenamiento en la nube de datos scrapeados**: contradice la filosofía de privacidad
- **Integración con APIs de LLMs externos** (OpenAI, Anthropic): contradice el core value de "100% local"

---

## 📬 Sugerir funcionalidades

¿Tienes una idea que no está aquí?
Abre un issue con el label `feature-request` en GitHub.

---

*Última actualización: Jun 2026 — v0.5.4*
*Próxima revisión del roadmap: cuando se alcance v0.6.0*
