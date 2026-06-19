from trafilatura import extract, extract_metadata


class Extractor:
    def extract_text(self, html: str) -> str | None:
        return extract(html, output_format="txt", include_links=False, include_images=False)

    def extract_metadata(self, html: str) -> dict:
        meta = extract_metadata(html)
        if meta is None:
            return {}
        return {
            "title": meta.title,
            "author": meta.author,
            "date": meta.date,
            "description": meta.description,
            "site_name": meta.sitename,
        }

    def extract_selectors(self, html: str, selectors: dict[str, str]) -> dict[str, str | None]:
        from scrapling import HtmlParser

        parser = HtmlParser(html)
        result = {}
        for name, selector in selectors.items():
            el = parser.css(selector)
            result[name] = el.text if el else None
        return result
