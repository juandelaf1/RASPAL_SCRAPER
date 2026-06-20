import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def generate_html(pipeline_data: list[dict], output: str | Path):
    items = pipeline_data if isinstance(pipeline_data, list) else []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows_html = ""
    for item in items:
        url = item.get("url", "unknown")
        status = item.get("data", {}).get("status", "N/A")
        text = item.get("data", {}).get("text", "")
        metadata = item.get("data", {}).get("metadata", {})
        llm = item.get("data", {}).get("llm_extraction", {})

        text_preview = (text[:500] + "...") if text and len(text) > 500 else (text or "")

        meta_html = ""
        if metadata:
            meta_html = "<dl class='meta'>"
            for k, v in metadata.items():
                if v:
                    meta_html += f"<dt>{k}</dt><dd>{v}</dd>"
            meta_html += "</dl>"

        llm_html = ""
        if llm:
            llm_html = f"<pre class='llm'>{json.dumps(llm, indent=2, ensure_ascii=False)}</pre>"

        rows_html += f"""
        <tr>
            <td><a href="{url}" target="_blank">{url[:80]}{'...' if len(url) > 80 else ''}</a></td>
            <td>{status}</td>
            <td>{meta_html}</td>
            <td><div class="text-preview">{text_preview}</div></td>
            <td>{llm_html}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RΛSPΛL SCRAPER — Reporte</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }}
  h1 {{ color: #58a6ff; margin-bottom: 0.5rem; font-size: 1.5rem; }}
  .meta {{ color: #8b949e; margin-bottom: 2rem; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ text-align: left; padding: 0.75rem; background: #161b22; color: #58a6ff; border-bottom: 2px solid #30363d; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  td {{ padding: 0.75rem; border-bottom: 1px solid #21262d; font-size: 0.9rem; vertical-align: top; }}
  tr:hover {{ background: #161b22; }}
  a {{ color: #58a6ff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  dl.meta {{ margin: 0; }}
  dl.meta dt {{ color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }}
  dl.meta dd {{ margin: 0 0 0.5rem 0; color: #c9d1d9; }}
  .text-preview {{ max-height: 150px; overflow-y: auto; font-size: 0.85rem; line-height: 1.4; color: #8b949e; }}
  .llm {{ background: #161b22; padding: 0.5rem; border-radius: 6px; font-size: 0.8rem; max-height: 200px; overflow: auto; color: #7ee787; }}
  .status-badge {{ display: inline-block; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }}
  .status-ok {{ background: #1b4721; color: #7ee787; }}
  .status-err {{ background: #49211b; color: #ff7b72; }}
</style>
</head>
<body>
    <h1>RΛSPΛL SCRAPER</h1>
    <div class="meta">Reporte generado el {timestamp} | {len(items)} items procesados</div>
    <table>
        <thead>
            <tr>
                <th>URL</th>
                <th>Status</th>
                <th>Metadata</th>
                <th>Texto extraído</th>
                <th>IA (LLM)</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</body>
</html>"""

    output_path = Path(output)
    output_path.write_text(html, encoding="utf-8")
    console.print(f"[green]Reporte generado: {output_path.resolve()}[/green]")


def print_summary(pipeline_data: list[dict]):
    if not pipeline_data:
        console.print("[yellow]No hay datos para mostrar[/yellow]")
        return

    total = len(pipeline_data)
    ok = sum(1 for i in pipeline_data if i.get("data", {}).get("status") == 200)
    errors = total - ok
    with_llm = sum(
        1 for i in pipeline_data
        if i.get("data", {}).get("llm_extraction") or i.get("data", {}).get("llm_chain")
    )

    table = Table(box=box.ROUNDED, title="Resumen")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="bold")
    table.add_row("Total URLs", str(total))
    table.add_row("Exitosas", f"[green]{ok}[/green]")
    if errors:
        table.add_row("Fallos", f"[red]{errors}[/red]")
    if with_llm:
        table.add_row("Extracciones con IA", str(with_llm))
    console.print(table)
