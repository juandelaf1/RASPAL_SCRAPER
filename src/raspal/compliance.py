from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


class ComplianceChecker:
    """Check compliance signals with real robots.txt parsing."""

    def __init__(self, user_agent: str = "RASPAL-SCRAPER/0.6.0 (+https://github.com/juandelaf1/RASPAL_SCRAPER)"):
        self.user_agent = user_agent
        self._robots_cache: dict[str, RobotFileParser] = {}

    def check_url(self, url: str) -> dict:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {
                "valid": False,
                "warnings": ["URL inválida: debe incluir esquema (http:// o https://)"],
            }

        warnings = []
        signals = {
            "valid": True,
            "url": url,
            "domain": parsed.netloc,
            "robots_txt": None,
            "can_fetch": None,
            "crawl_delay": None,
            "is_sensitive_domain": self._is_sensitive_domain(parsed.netloc),
        }

        if signals["is_sensitive_domain"]:
            warnings.append(
                "Dominio potencialmente sensible (redes sociales, salud, finanzas). "
                "Revisa cuidadosamente ToS y regulaciones aplicables."
            )

        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        signals["robots_txt"] = robots_url

        allowed, reason = self.can_fetch(url)
        signals["can_fetch"] = allowed
        if allowed:
            warnings.append(f"✅ {robots_url} permite scraping para '{self.user_agent}'")
        else:
            warnings.append(f"❌ {robots_url} bloquea scraping para '{self.user_agent}'")

        delay = self.get_crawl_delay(url)
        if delay is not None:
            signals["crawl_delay"] = delay
            warnings.append(f"⏱  Crawl-delay: {delay}s — respeta este intervalo")

        return {"signals": signals, "warnings": warnings}

    def can_fetch(self, url: str) -> tuple[bool, str]:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = f"{base_url}/robots.txt"

        if base_url not in self._robots_cache:
            rp = RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self._robots_cache[base_url] = rp
            except Exception:
                return True, f"No se pudo leer {robots_url} — procediendo con precaución"

        rp = self._robots_cache[base_url]
        allowed = rp.can_fetch(self.user_agent, url)
        if allowed:
            return True, f"{url} permite scraping según robots.txt"
        return False, f"{url} está bloqueado en robots.txt para '{self.user_agent}'"

    def get_crawl_delay(self, url: str) -> float | None:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        if base_url in self._robots_cache:
            return self._robots_cache[base_url].crawl_delay(self.user_agent)
        return None

    def _is_sensitive_domain(self, domain: str) -> bool:
        sensitive_patterns = [
            "facebook.com",
            "linkedin.com",
            "instagram.com",
            "twitter.com",
            "x.com",
            "health",
            "hospital",
            "clinic",
            "bank",
            "finance",
            "insurance",
        ]
        domain_lower = domain.lower()
        return any(pattern in domain_lower for pattern in sensitive_patterns)


def check_compliance(url: str) -> dict:
    """Convenience function for quick compliance checks."""
    return ComplianceChecker().check_url(url)


def load_config(config_path: str | Path) -> dict:
    import yaml

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        return {}

    result = {
        "url": config.get("url"),
        "engine": config.get("engine", "auto"),
        "llm_enabled": bool(config.get("llm")),
        "extract_text": config.get("extract", {}).get("text", True),
        "extract_metadata": config.get("extract", {}).get("metadata", True),
    }

    if result["url"]:
        result["compliance"] = check_compliance(result["url"])

    return result
