import asyncio
import json
import shutil
import signal
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.json import JSON
from rich.table import Table

from raspal.cache import Cache
from raspal.extractor import Extractor
from raspal.fetcher import Fetcher
from raspal.improvements.async_compatibility import AsyncFetcher
from raspal.llm import LLMExtractor
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
def async_fetch(
    url: str,
    engine: str = typer.Option("auto", "--engine", "-e", help="scrapling | playwright | stealth | auto"),
    text: bool = typer.Option(True, "--text", "-t", help="Extract text content"),
    timeout: int = typer.Option(30, "--timeout", help="Request timeout in seconds"),
    pretty: bool = typer.Option(True, "--pretty", "-p", help="Pretty print output"),
):
    """Fetch a URL asynchronously."""
    async def run():
        async with AsyncFetcher() as fetcher:
            result = await fetcher.fetch_async(url, engine=engine, timeout=timeout)

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

            return output

    try:
        output = asyncio.run(run())
        if pretty:
            console.print(JSON(json.dumps(output, indent=2, default=str)))
        else:
            console.print(json.dumps(output, indent=2, default=str))
    except Exception as e:
        msg = str(e)
        if "connect" in msg.lower() or "connection" in msg.lower():
            console.print("[red]Error de conexion:[/red] No se pudo conectar con el servidor. Verifica la URL, tu conexion a internet, o prueba con otro motor (--engine playwright o --engine stealth).")
        elif "timeout" in msg.lower():
            console.print(f"[red]Timeout:[/red] La solicitud tardó demasiado. Aumenta el timeout con --timeout 60 o prueba con --engine scrapling (mas rapido).")
        elif "ollama" in msg.lower():
            console.print("[red]Error de Ollama:[/red] Asegurate de que Ollama este corriendo (ollama serve) y que el modelo este descargado (ollama pull llama3.2).")
        else:
            console.print(f"[red]Error:[/red] {msg}")
        sys.exit(1)


@app.command()
def async_batch(
    urls: list[str] = typer.Argument(..., help="List of URLs to fetch asynchronously"),
    engine: str = typer.Option("auto", "--engine", "-e", help="scrapling | playwright | stealth | auto"),
    text: bool = typer.Option(True, "--text", "-t", help="Extract text content"),
    timeout: int = typer.Option(30, "--timeout", help="Request timeout in seconds"),
    pretty: bool = typer.Option(True, "--pretty", "-p", help="Pretty print output"),
):
    """Fetch multiple URLs asynchronously."""
    async def run():
        async with AsyncFetcher() as fetcher:
            results = await fetcher.fetch_batch(urls, engine=engine, timeout=timeout)

            output = []
            for result in results:
                entry = {
                    "url": getattr(result, "url", "unknown"),
                    "status": getattr(result, "status", 0),
                    "engine": getattr(result, "engine", "unknown"),
                    "cached": getattr(result, "cached", False),
                }

                if hasattr(result, "error") and result.error:
                    entry["error"] = result.error
                elif text and hasattr(result, "html") and result.html:
                    ext = Extractor()
                    entry["text"] = ext.extract_text(result.html)
                    entry["metadata"] = ext.extract_metadata(result.html)

                output.append(entry)

            return output

    try:
        output = asyncio.run(run())
        if pretty:
            console.print(JSON(json.dumps(output, indent=2, default=str)))
        else:
            console.print(json.dumps(output, indent=2, default=str))
    except Exception as e:
        msg = str(e)
        if "connect" in msg.lower() or "connection" in msg.lower():
            console.print("[red]Error de conexion:[/red] No se pudo conectar con el servidor. Verifica la URL y tu conexion a internet.")
        elif "timeout" in msg.lower():
            console.print(f"[red]Timeout:[/red] Aumenta el timeout con --timeout 60 o prueba con --engine scrapling.")
        else:
            console.print(f"[red]Error:[/red] {msg}")
        sys.exit(1)


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


@app.command()
def validate(
    config: str = typer.Argument(..., help="Path to YAML config file"),
):
    """Validate a YAML config file."""
    from raspal.router import Router
    from raspal.exceptions import ConfigError

    try:
        router = Router()
        router._load_config(config)
        console.print(f"[green]v Config válido:[/green] {config}")
    except ConfigError as e:
        console.print(f"[red]x Config inválido:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def compliance(
    url: str = typer.Argument(..., help="URL a verificar"),
):
    """Check robots.txt compliance before scraping."""
    from raspal.compliance import ComplianceChecker

    checker = ComplianceChecker()
    result = checker.check_url(url)
    signals = result.get("signals", {})
    warnings = result.get("warnings", [])

    console.print(f"[bold]URL:[/bold] {url}")
    console.print(f"[bold]Dominio:[/bold] {signals.get('domain', 'N/A')}")
    console.print(f"[bold]robots.txt:[/bold] {signals.get('robots_txt', 'N/A')}")
    can_fetch = signals.get("can_fetch")
    if can_fetch is True:
        console.print(f"[bold]Scraping permitido:[/bold] [green]Sí[/green]")
    elif can_fetch is False:
        console.print(f"[bold]Scraping permitido:[/bold] [red]No (bloqueado por robots.txt)[/red]")
    else:
        console.print(f"[bold]Scraping permitido:[/bold] [yellow]No se pudo verificar[/yellow]")
    delay = signals.get("crawl_delay")
    if delay is not None:
        console.print(f"[bold]Crawl-delay:[/bold] {delay}s")

    if signals.get("is_sensitive_domain"):
        console.print("[yellow]⚠️  Dominio potencialmente sensible (redes sociales, salud, finanzas)[/yellow]")

    if warnings:
        console.print("\n[yellow]Advertencias:[/yellow]")
        for w in warnings:
            console.print(f"  • {w}")
    else:
        console.print("\n[green]✔ Sin advertencias.[/green]")


@app.command()
def doctor():
    """Verify that the RASPAL environment is correctly configured."""
    import shutil
    import sys

    console.print("\n[bold]🩺 RASPAL Doctor[/bold]\n")
    all_ok = True

    py_ver = sys.version_info
    if py_ver >= (3, 11):
        console.print(f"  ✅ Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    else:
        console.print(f"  ❌ Python {py_ver.major}.{py_ver.minor} — se necesita Python ≥ 3.11")
        all_ok = False

    ollama_bin = shutil.which("ollama")
    if ollama_bin:
        console.print(f"  ✅ Ollama instalado ({ollama_bin})")
        try:
            import httpx
            r = httpx.get("http://localhost:11434/api/tags", timeout=3)
            models = r.json().get("models", [])
            if models:
                console.print(f"  ✅ Ollama activo — {len(models)} modelo(s)")
                for m in models[:3]:
                    console.print(f"     • {m.get('name', 'unknown')}")
            else:
                console.print("  ⚠️  Ollama activo sin modelos. Ejecuta: ollama pull llama3.2:3b")
        except Exception:
            console.print("  ⚠️  Ollama instalado pero no corriendo. Ejecuta: ollama serve")
            all_ok = False
    else:
        console.print("  ❌ Ollama no encontrado — instálalo en https://ollama.com")
        all_ok = False

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                console.print("  ✅ Playwright browsers instalados")
            except Exception:
                console.print("  ⚠️  Playwright sin browsers. Ejecuta: raspal setup")
    except ImportError:
        console.print("  ❌ Playwright no instalado. Ejecuta: pip install raspal[all]")

    from raspal.cache import Cache
    import os
    if os.access(".", os.W_OK):
        console.print("  ✅ Permisos de escritura en directorio actual")
    else:
        console.print("  ❌ Sin permisos de escritura")
        all_ok = False

    console.print()
    if all_ok:
        console.print("[bold green]✅ RASPAL está listo.[/bold green]")
        console.print("   Siguiente paso: [bold]raspal demo[/bold]\n")
    else:
        console.print("[bold yellow]⚠️  RASPAL tiene problemas de configuración.[/bold yellow]")
        console.print("   Revisa los puntos marcados con ❌ arriba.\n")


@app.command()
def setup():
    """Prepare the environment: install browsers, check Ollama."""
    from raspal.setup import run_setup
    run_setup()


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", help="Host del dashboard"),
    port: int = typer.Option(8462, "--port", "-p", help="Puerto del dashboard"),
):
    """Start the web dashboard."""
    from raspal.web.dashboard import serve as web_serve
    web_serve(host=host, port=port)


@app.command()
def init():
    """Scaffold a new scraping project interactively."""
    from raspal.scaffold import run_init
    run_init()


@app.command()
def report(
    input: str = typer.Option("results.json", "--input", "-i", help="Pipeline results JSON"),
    output: str = typer.Option("report.html", "--output", "-o", help="HTML report path"),
):
    """Generate an HTML report from pipeline results."""
    from raspal.reporter import generate_html, print_summary

    try:
        with open(input, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        console.print(f"[red]No se encontró {input}[/red]")
        raise typer.Exit(1)

    print_summary(data)
    generate_html(data, output)


@app.command()
def demo(
    pretty: bool = typer.Option(True, "--pretty", "-p", help="Pretty print output"),
):
    """Run a demo with data from the web. No configuration needed."""
    import time

    DEMO_URL = "https://books.toscrape.com"

    console.print("\n[bold cyan]🔍 RASPAL DEMO[/bold cyan]")
    console.print("─" * 50)

    console.print(f"\n[bold]1. Fetching[/bold] {DEMO_URL}...")
    start = time.time()
    try:
        with Fetcher() as fetcher:
            result = fetcher.fetch(DEMO_URL, engine="scrapling")
        fetch_time = time.time() - start
        console.print(f"   ✅ {result.status} OK en {fetch_time:.1f}s (motor: scrapling)")
    except Exception as e:
        console.print(f"   ❌ Error de fetch: {e}")
        console.print("   Verifica tu conexión y ejecuta [bold]raspal doctor[/bold]")
        raise typer.Exit(1)

    console.print("\n[bold]2. Extrayendo contenido...[/bold]")
    ext = Extractor()
    data = ext.extract_selectors(result.html, {
        "titles": "article.product_pod h3 a",
        "prices": "article.product_pod p.price_color",
    })
    titles = data.get("titles", [])
    prices = data.get("prices", [])
    console.print(f"   ✅ {len(titles)} productos detectados")
    for t, p in list(zip(titles, prices))[:5]:
        console.print(f"     • {t} — {p}")

    import shutil
    ai_result = None
    if shutil.which("ollama"):
        console.print("\n[bold]3. Estructurando con IA local (Ollama)...[/bold]")
        try:
            llm = LLMExtractor()
            text_sample = ext.extract_text(result.html)[:1500]
            ai_result = llm.extract(text_sample, template="product")
            console.print("   ✅ Extracción con IA completada")
        except Exception as e:
            console.print(f"   ⚠️  IA no disponible ({e})")
    else:
        console.print("\n[bold]3. IA local[/bold] ⚠️  Ollama no detectado")
        console.print("   Instala Ollama en https://ollama.com para activarlo")

    total_time = time.time() - start
    console.print(f"\n[bold]📦 Resultado:[/bold]")
    output = {
        "url": DEMO_URL,
        "products_found": len(titles),
        "sample": [{"title": t, "price": p} for t, p in list(zip(titles, prices))[:5]],
        "ai_extraction": ai_result,
    }
    if pretty:
        console.print(JSON(json.dumps(output, indent=2, ensure_ascii=False, default=str)))
    else:
        console.print(json.dumps(output, indent=2, ensure_ascii=False, default=str))

    console.print(f"\n[dim]⏱  Total: {total_time:.1f}s | Sin API keys | Datos en tu máquina[/dim]")
    console.print("\n[bold]Siguiente paso:[/bold] raspal fetch <tu-url> --engine auto")
    console.print("[bold]Docs:[/bold] https://github.com/juandelaf1/RASPAL_SCRAPER\n")


@app.command()
def version():
    """Show the installed version."""
    from importlib.metadata import version as get_version
    try:
        ver = get_version("raspal")
    except Exception:
        ver = "unknown"
    console.print(f"RASPAL SCRAPER v{ver}")
    console.print("Web scraping toolkit with local LLM extraction via Ollama.")


if __name__ == "__main__":
    app()
