# Changelog

## [0.5.0] — 2026-06-21

### Added
- Docker support (Dockerfile, docker-compose.yml, docker-compose.dev.yml)
- `raspal compliance` — check robots.txt and sensitive domains
- `raspal validate` — validate YAML config files
- Compliance module (`raspal.compliance`)
- Legal and ethics documentation (`docs/legal-and-ethics.md`)
- Docker quickstart guide (`docs/quickstart-docker.md`)
- KNOWN_ISSUES.md documenting limitations
- Example YAML pipelines (e-commerce, news, real estate)
- Multi-arch Docker CI (GitHub Actions for amd64 + arm64)
- requirements.txt for reproducible installs

### Changed
- README reorganized with Docker as primary installation path
- Updated AGENTS.md with new commands

## [0.4.0] — 2026-06-19

### Added
- `raspal setup` — installs Playwright browsers, verifies Ollama
- `raspal init` — interactive project scaffolding
- `raspal report` — HTML report generation
- `raspal serve` — web dashboard (FastAPI + uvicorn)
- AsyncFetcher improvements
- Web dashboard with real-time scraping

### Changed
- Project renamed to RASPAL SCRAPER
- Complete README rewrite

## [0.3.0] — 2026-06-19

### Added
- YAML pipeline support
- LLM extraction chain (multi-step)
- Output schema validation
- Request queue with priorities and retries

## [0.2.0] — 2026-06-19

### Added
- AsyncFetcher for concurrent scraping
- CLI commands (async_fetch, async_batch, status, clear_cache)
- Enhanced documentation

## [0.1.0] — 2026-06-19

### Added
- Initial release
- Fetcher with multiple engines (scrapling, playwright, stealth)
- Cache with TTL
- AutoThrottle for rate limiting
- Extractor with text and metadata extraction
- LLM extraction via Ollama
- Basic CLI (fetch, run, queue)
