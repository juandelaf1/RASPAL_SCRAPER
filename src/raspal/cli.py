import json

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from raspal.extractor import Extractor
from raspal.fetcher import Fetcher
from raspal.router import Router

app = typer.Typer(name="raspal")
console = Console()


@app.command()
def fetch(
    url: str,
    engine: str = typer.Option(
        "auto", "--engine", "-e",
        help="scrapling | playwright | stealth | auto",
    ),
    text: bool = typer.Option(True, "--text", "-t", help="Extract text content"),
    pretty: bool = typer.Option(True, "--pretty", "-p", help="Pretty print output"),
):
    """Fetch a URL and extract content."""
    fetcher = Fetcher()
    result = fetcher.fetch(url, engine=engine)

    output = {
        "url": url,
        "status": result.status,
        "engine": result.engine,
        "cached": result.cached,
    }

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


@app.command()
def queue(
    config: str = typer.Argument(..., help="Path to YAML config file"),
    db: str = typer.Option("raspal_queue.sqlite", "--db", help="Queue database path"),
    output: str = typer.Option("results.json", "--output", "-o", help="Output file"),
):
    """Process URLs from a queue using a YAML config."""
    router = Router()
    pipeline = router.run_queue(config, db)
    pipeline.to_json(output)
    console.print(f"[green]Processed {len(pipeline)} items -> {output}[/green]")


@app.command()
def status():
    """Show current throttle delays and cache info."""
    from raspal.throttle import AutoThrottle

    throttle = AutoThrottle()
    table = Table(title="AutoThrottle Delays")
    table.add_column("Engine", style="cyan")
    table.add_column("Current delay (s)", style="magenta")

    for engine, delay in throttle.current_delays.items():
        table.add_row(engine, f"{delay:.2f}")

    console.print(table)


if __name__ == "__main__":
    app()
