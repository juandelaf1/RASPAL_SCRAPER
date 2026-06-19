import json
import typer
from rich.console import Console
from rich.json import JSON
from raspal.fetcher import Fetcher
from raspal.extractor import Extractor
from raspal.router import Router

app = typer.Typer(name="raspal")
console = Console()


@app.command()
def fetch(
    url: str,
    engine: str = typer.Option("auto", "--engine", "-e", help="scrapling | playwright | auto"),
    text: bool = typer.Option(True, "--text", "-t", help="Extract text content"),
    pretty: bool = typer.Option(True, "--pretty", "-p", help="Pretty print output"),
):
    """Fetch a URL and extract content."""
    fetcher = Fetcher()
    result = fetcher.fetch(url, engine=engine)

    output = {"url": url, "status": result.status, "engine": result.engine, "cached": result.cached}

    if text and result.html:
        ext = Extractor()
        output["text"] = ext.extract_text(result.html)
        output["metadata"] = ext.extract_metadata(result.html)

    if pretty:
        console.print(JSON(json.dumps(output, indent=2, default=str)))
    else:
        console.print(json.dumps(output, indent=2, default=str))


@app.command()
def run(
    config: str = typer.Argument(..., help="Path to YAML config file"),
    pretty: bool = typer.Option(True, "--pretty", "-p"),
):
    """Run a scraping pipeline from a YAML config."""
    router = Router()
    result = router.run(config)
    if pretty:
        console.print(JSON(json.dumps(result, indent=2, default=str)))
    else:
        console.print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    app()
