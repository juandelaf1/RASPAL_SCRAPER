from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich import box

console = Console()


def run_init():
    console.print(Panel.fit(
        "[bold]RΛSPΛL SCRAPER[/bold] — Init\n"
        "Crea un proyecto de scraping configurado.",
        box=box.ROUNDED,
    ))

    project_dir = Prompt.ask("[bold]Nombre del proyecto[/bold]", default="mi-scraper")
    project_path = Path.cwd() / project_dir

    if project_path.exists():
        if not Confirm.ask(f"[yellow]La carpeta '{project_dir}' ya existe. ¿Sobrescribir?[/yellow]", default=False):
            console.print("[red]Cancelado[/red]")
            return
    else:
        project_path.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[bold]Configuración del scraper[/bold]")

    url = Prompt.ask("[bold]URL a scrapear[/bold]")
    engine = Prompt.ask(
        "[bold]Motor[/bold]",
        choices=["auto", "scrapling", "playwright", "stealth"],
        default="auto",
    )
    use_llm = Confirm.ask("[bold]¿Usar extracción con IA (Ollama)?[/bold]", default=True)

    config = {
        "url": url,
        "engine": engine,
        "cache_ttl": 3600,
        "timeout": 30,
        "extract": {
            "text": True,
            "metadata": True,
            "use_selectolax": True,
            "selectors": {},
        },
    }

    use_selectors = Confirm.ask("[bold]¿Añadir selectores CSS?[/bold]", default=False)
    if use_selectors:
        console.print("  [dim]Define selectores (deja vacío para terminar):[/dim]")
        selectors = {}
        while True:
            name = Prompt.ask("    Nombre del campo", default="")
            if not name:
                break
            selector = Prompt.ask(f"    Selector CSS para '{name}'")
            if selector:
                selectors[name] = selector
        if selectors:
            config["extract"]["selectors"] = selectors

    if use_llm:
        console.print("\n[bold]Configuración de IA (Ollama)[/bold]")
        model = Prompt.ask("[bold]Modelo[/bold]", default="llama3.2")
        template = Prompt.ask(
            "[bold]Template[/bold]",
            choices=["product", "article", "person", "review", "event", "generic", ""],
            default="",
        )
        prompt = Prompt.ask("[bold]Prompt personalizado[/bold] (opcional)", default="")

        llm_config = {"model": model}
        if template:
            llm_config["template"] = template
        if prompt:
            llm_config["prompt"] = prompt

        use_schema = Confirm.ask("[bold]¿Definir schema JSON de salida?[/bold]", default=False)
        if use_schema:
            console.print("  [dim]Define campos del schema (deja vacío para terminar):[/dim]")
            schema = {}
            while True:
                field = Prompt.ask("    Nombre del campo", default="")
                if not field:
                    break
                field_type = Prompt.ask(
                    "    Tipo",
                    choices=["string", "number", "boolean"],
                    default="string",
                )
                schema[field] = field_type
            if schema:
                llm_config["output_schema"] = schema

        config["llm"] = llm_config

    config_file = project_path / "config.yaml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    (project_path / "results").mkdir(exist_ok=True)
    (project_path / "results" / ".gitkeep").touch()

    readme_file = project_path / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(f"""# {project_dir}

Scraper generado con RΛSPΛL SCRAPER.

## Uso

```bash
# Ejecutar scraper
raspal run config.yaml

# Modo cola
raspal queue config.yaml --db queue.sqlite -o results/results.json
```
""")

    console.print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    console.print("[bold green]✓ Proyecto creado[/bold green]")
    console.print(f"  [bold]{project_path}[/bold]")
    console.print(f"  ├── [bold]config.yaml[/bold]")
    console.print(f"  ├── [bold]results/[/bold]")
    console.print(f"  └── [bold]README.md[/bold]")
    console.print(f"\n  Para ejecutar: [bold]cd {project_dir} && raspal run config.yaml[/bold]")
