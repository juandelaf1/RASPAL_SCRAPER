# RASPAL_SCRAPER — Technical Case Study

## Problem
Extracting structured data from websites often requires brittle scripts, paid APIs, or sending data to third-party services. The goal is to provide a **local-first, practical scraping toolkit** that can fetch pages with appropriate engines, extract content/fields, and optionally structure results with local AI workflows.

## Decisions
- **Multi-engine fetching:** support different fetching strategies (e.g. fast/static, browser/JS, stealth/anti-bot modes) with an `auto` selection path to match site characteristics.
- **Local-first processing:** prioritize running extraction and AI-assisted structuring locally (e.g. Ollama integration) to avoid mandatory third-party data transfer and API keys.
- **Composable toolkit:** expose building blocks (fetchers, extractors, LLM extraction, cache, throttle, queue, pipelines/router, CLI) usable via CLI, Python API, and YAML pipelines.
- **Pragmatic automation:** include templates/examples, async/batch capabilities, reporting/dashboard utilities, and Docker-based setup to reduce onboarding friction.
- **Operational safeguards:** encourage/implement responsible usage practices (compliance checks, throttling, caching) and provide diagnostics (`doctor`, validation commands).

## Trade-offs
- **Convenience vs site variability:** automated/stealth strategies improve reach but cannot guarantee success on every protected or highly dynamic site.
- **Local AI benefits vs setup cost:** local inference improves privacy/control but depends on local model/runtime availability and hardware performance.
- **Toolkit breadth vs simplicity:** many components increase flexibility but require clear documentation and conventions to avoid misuse.
- **Scraping utility vs legal/ethical constraints:** technical capability must be balanced with robots/ToS/legal considerations; the tool cannot make scraping compliant by itself.

## Evidence
- **Repository assets:** CLI commands, Python API modules, YAML pipeline support, examples/templates, Docker configuration, and documentation site/content in `docs/`.
- **Quality/tooling:** automated test suites/workflows configured in `.github/workflows/` (CI, integration/docs/publish flows as present) and project tooling (`ruff`, pytest config).
- **Packaging/distribution signals:** PyPI/Docker-oriented metadata and release/versioning conventions documented in project files (e.g. README, `PUBLIC_API.md`, changelog/roadmap docs where applicable).

## Limits & learnings
- **Limits:** effectiveness depends on target-site behavior, anti-bot measures, selectors/prompts quality, and local environment (browsers/Ollama/resources). Not a drop-in replacement for large-scale distributed crawling frameworks in all cases.
- **Learnings:** clear engine abstractions, reproducible pipelines (YAML/CLI), and local-first defaults make scraping workflows easier to iterate and review; explicit compliance/throttling guidance is essential for responsible use.
