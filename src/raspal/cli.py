import json
import signal
import sys

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from raspal.cache import Cache
from raspal.extractor import Extractor
from raspal.fetcher import Fetcher
from raspal.router import Router

app = typer.Typer(name="raspal")
console = Console()


def _handle_interrupt(sig, frame):
    console.print("\n[yellow]Interrupted. Exiting...[/yellow]")
    sys.exit(0)


signal.signal(signal.SIGINT, _handle_interrupt)


@app.command()
def fetch(
    url: str,
    engine: str = typer.Option(
        "auto", "--engine", "-e",
        help="scrapling | playwright | stealth | auto",
    ),
    text: bool = typer.Option(True, "--text", "-t", help="Extract text content"),
    timeout: int = typer.Option(30, "--timeout", help="Request timeout in seconds"),
    pretty: bool = typer.Option(True, "--pretty", "-p", help="Pretty print output"),
):
    """Fetch a URL and extract content."""
    with Fetcher() as fetcher:
        result = fetcher.fetch(url, engine=engine, timeout=timeout)

    output = {
        "url": url,
        "status": result.status,
        "engine": result.engine,
        "cached": result.cached,
    }

    if result.error:
        output["error"] = result.error
    elif text and result.html:
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


@app.command()
def clear_cache(
    url: str | None = typer.Argument(None, help="URL to clear (clears all if omitted)"),
):
    """Clear the cache."""
    with Cache() as cache:
        if url:
            cache.clear(url)
            console.print(f"[green]Cleared cache for {url}[/green]")
        else:
            cache.clear()
            console.print("[green]Cleared entire cache[/green]")


if __name__ == "__main__":
    app()
