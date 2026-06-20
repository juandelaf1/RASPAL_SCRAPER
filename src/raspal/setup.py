import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

console = Console()

OLLAMA_MODELS = [
    "llama3.2:latest",
    "llama3.2:1b",
    "llama3.1:8b",
    "mistral:7b",
    "qwen2.5:7b",
]

RECOMMENDED_MODEL = "llama3.2"


def _step(msg: str):
    console.print(f"  [dim]├[/dim] {msg}")


def _ok(msg: str):
    console.print(f"  [green]├[/green] [bold green]✓[/bold green] {msg}")


def _fail(msg: str):
    console.print(f"  [red]├[/red] [bold red]✗[/bold red] {msg}")


def _skip(msg: str):
    console.print(f"  [yellow]├[/yellow] [bold yellow]→[/bold yellow] {msg}")


def _check_playwright():
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False


def _playwright_browsers_installed():
    try:
        from playwright._repo_impl import Browser
        browsers_dir = Path.home() / ".cache" / "ms-playwright"
        if not browsers_dir.exists():
            return False
        chromium_dir = list(browsers_dir.glob("chromium-*"))
        return len(chromium_dir) > 0
    except Exception:
        return False


def _install_playwright():
    _step("Instalando browsers de Playwright...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            _ok("Playwright browsers instalados")
            return True
        _fail(f"Error instalando browsers: {result.stderr.strip()}")
        return False
    except subprocess.TimeoutExpired:
        _fail("Timeout instalando browsers")
        return False
    except Exception as e:
        _fail(f"Error: {e}")
        return False


def _check_ollama_binary():
    return shutil.which("ollama") is not None


def _ollama_running():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def _ollama_has_model(model: str) -> bool:
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=10,
        )
        return model.split(":")[0] in result.stdout
    except Exception:
        return False


def _pull_ollama_model(model: str):
    _step(f"Descargando modelo {model} (esto puede tomar varios minutos)...")
    try:
        process = subprocess.Popen(
            ["ollama", "pull", model],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True,
        )
        for line in process.stdout:
            line = line.strip()
            if line:
                console.print(f"    [dim]{line}[/dim]")
        process.wait()
        if process.returncode == 0:
            _ok(f"Modelo {model} descargado")
            return True
        _fail(f"Error descargando {model}")
        return False
    except Exception as e:
        _fail(f"Error: {e}")
        return False


def run_setup():
    console.print(Panel.fit(
        "[bold]RΛSPΛL SCRAPER[/bold] — Setup\n"
        "Vamos a preparar tu entorno para scraping con IA local.\n"
        "Esto instalará los browsers necesarios y configurará Ollama.",
        box=box.ROUNDED,
    ))

    console.print("\n[bold]1. Playwright[/bold]")
    if not _playwright_browsers_installed():
        if not _install_playwright():
            _skip("Puedes instalarlo después con: playwright install chromium")
    else:
        _ok("Playwright browsers ya instalados")

    console.print("\n[bold]2. Ollama[/bold]")
    if _check_ollama_binary():
        _ok("Ollama instalado")
        if _ollama_running():
            _ok("Servidor Ollama corriendo")
            has_recommended = _ollama_has_model(RECOMMENDED_MODEL)
            if has_recommended:
                _ok(f"Modelo {RECOMMENDED_MODEL} disponible")
            else:
                _skip(f"Modelo {RECOMMENDED_MODEL} no encontrado")
                console.print(f"    [dim]Descargando modelo recomendado ({RECOMMENDED_MODEL})...[/dim]")
                _pull_ollama_model(RECOMMENDED_MODEL)
        else:
            _fail("Servidor Ollama no está corriendo")
            _step("Inícialo con: ollama serve")
    else:
        _fail("Ollama no está instalado")
        _step("Descárgalo desde: https://ollama.com")

    console.print("\n[bold]3. Dependencias Python[/bold]")
    try:
        import scrapling  # noqa: F401
        _ok("scrapling instalado")
    except ImportError:
        _fail("scrapling no instalado — ejecuta: pip install scrapling")

    try:
        import playwright  # noqa: F401
        _ok("playwright instalado")
    except ImportError:
        _fail("playwright no instalado")

    console.print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    console.print("[bold green]✓ Setup completado[/bold green]")
    console.print("  Prueba con: [bold]raspal fetch https://example.com[/bold]")
    console.print("  Con IA:    [bold]raspal run config.yaml[/bold]")
