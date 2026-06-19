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
        from scrapling import Selector

        parser = Selector(html)
        result = {}
        for name, selector in selectors.items():
            els = parser.css(selector)
            result[name] = str(els[0].text) if els else None
        return result

    def extract_selectors_fast(self, html: str, selectors: dict[str, str]) -> dict[str, str | None]:
        try:
            from selectolax.parser import HTMLParser as SelectolaxParser

            parser = SelectolaxParser(html)
            result = {}
            for name, selector in selectors.items():
                node = parser.css_first(selector)
                result[name] = node.text() if node else None
            return result
        except ImportError:
            return self.extract_selectors(html, selectors)
