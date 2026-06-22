# Contributing to RASPAL SCRAPER

Thanks for your interest in contributing!

## Development setup

```bash
git clone https://github.com/juandelaf1/RASPAL_SCRAPER
cd RASPAL_SCRAPER
pip install -e ".[dev]"
pip install pytest ruff
```

## Running tests

```bash
pytest tests/ -v
```

All tests must pass without Ollama installed or internet access.

## Linting

```bash
ruff check src/
ruff format src/
```

## Versioning

See [PUBLIC_API.md](PUBLIC_API.md) for what constitutes the public API.
RASPAL follows [SemVer](https://semver.org/).

## Reporting bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).
Always include: OS, Python version, RASPAL version, and output of `raspal doctor`.

## What we accept

- 🐛 Bug fixes (always welcome)
- 📝 Documentation improvements (always welcome)
- ✨ Features (open an issue first to discuss)
- 🧪 Additional tests (always welcome)
- 🌐 YAML templates for new use cases (always welcome)
