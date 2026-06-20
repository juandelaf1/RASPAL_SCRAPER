import json
import subprocess
import sys
from pathlib import Path

from raspal.cache import Cache
from raspal.router import Router

try:
    from fastapi import FastAPI, HTTPException, UploadFile, File
    from fastapi.responses import HTMLResponse, JSONResponse
    import uvicorn
except ImportError:
    FastAPI = None
    HTTPException = None
    UploadFile = None
    File = None
    HTMLResponse = None
    JSONResponse = None
    uvicorn = None

app = FastAPI(title="RΛSPΛL SCRAPER Dashboard")


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RΛSPΛL SCRAPER — Dashboard</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }
  h1 { color: #58a6ff; margin-bottom: 2rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
  .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.5rem; }
  .card h2 { color: #58a6ff; font-size: 1rem; margin-bottom: 1rem; }
  .card .value { font-size: 2rem; font-weight: bold; }
  .card .label { color: #8b949e; font-size: 0.85rem; }
  table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
  th { text-align: left; padding: 0.75rem; background: #161b22; color: #58a6ff; border-bottom: 2px solid #30363d; font-size: 0.85rem; }
  td { padding: 0.75rem; border-bottom: 1px solid #21262d; }
  .ok { color: #7ee787; }
  .err { color: #ff7b72; }
  form { margin-top: 1rem; }
  input, select, button { padding: 0.5rem; margin: 0.25rem 0; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; width: 100%; }
  button { background: #238636; border: none; cursor: pointer; font-weight: 600; }
  button:hover { background: #2ea043; }
  .flex { display: flex; gap: 1rem; }
  .flex > * { flex: 1; }
  pre { background: #0d1117; padding: 1rem; border-radius: 6px; overflow: auto; max-height: 400px; }
</style>
</head>
<body>
  <h1>RΛSPΛL SCRAPER</h1>
  <div class="grid" id="stats"></div>
  <div class="card">
    <h2>Ejecutar scraper</h2>
    <form id="scrape-form">
      <div class="flex">
        <input type="url" name="url" placeholder="URL a scrapear" required>
        <select name="engine">
          <option value="auto">Auto</option>
          <option value="scrapling">Scrapling</option>
          <option value="playwright">Playwright</option>
          <option value="stealth">Stealth</option>
        </select>
        <button type="submit">Scrapear</button>
      </div>
    </form>
    <div id="result"></div>
  </div>
  <div class="card">
    <h2>Cola de URLs</h2>
    <form id="queue-form">
      <div class="flex">
        <input type="text" name="urls" placeholder="URLs separadas por coma" required>
        <button type="submit">Añadir a cola</button>
      </div>
    </form>
    <div id="queue-result"></div>
  </div>
  <div class="card">
    <h2>Scrapers recientes</h2>
    <div id="recent"></div>
  </div>
  <script>
    async function loadStats() {
      const res = await fetch('/api/stats');
      const stats = await res.json();
      document.getElementById('stats').innerHTML = Object.entries(stats).map(([k, v]) =>
        `<div class="card"><div class="label">${k}</div><div class="value">${v}</div></div>`
      ).join('');
    }
    document.getElementById('scrape-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = e.target;
      const res = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: form.url.value, engine: form.engine.value }),
      });
      const data = await res.json();
      document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
      loadStats();
    });
    document.getElementById('queue-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = e.target;
      const urls = form.urls.value.split(',').map(u => u.trim()).filter(Boolean);
      const res = await fetch('/api/queue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urls }),
      });
      const data = await res.json();
      document.getElementById('queue-result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
      loadStats();
    });
    loadStats();
  </script>
</body>
</html>
"""


@app.get("/api/stats")
async def stats():
    router = Router()
    cache = Cache()

    # Basic stats
    return {
        "Cache activa": "✅",
        "Ollama": "✅" if _check_ollama() else "❌",
        "Playwright": "✅" if _check_playwright() else "⚠️",
    }


@app.post("/api/scrape")
async def scrape(url: str, engine: str = "auto"):
    router = Router()
    try:
        result = router.fetcher.fetch(url, engine=engine)
        output = {
            "url": url,
            "status": result.status,
            "engine": result.engine,
            "cached": result.cached,
        }
        if result.html:
            from raspal.extractor import Extractor
            ext = Extractor()
            output["text"] = ext.extract_text(result.html)
            output["metadata"] = ext.extract_metadata(result.html)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/queue")
async def queue_urls(urls: list[str]):
    from raspal.queue import RequestQueue

    q = RequestQueue("raspal_queue.sqlite")
    for url in urls:
        q.push(url)
    q.close()
    return {"added": len(urls), "urls": urls}


@app.get("/api/queue/status")
async def queue_status():
    from raspal.queue import RequestQueue

    q = RequestQueue("raspal_queue.sqlite")
    pending = q.pending_count()
    q.close()
    return {"pending": pending}


def _check_ollama():
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def _check_playwright():
    try:
        from playwright._repo_impl import Browser
        return True
    except Exception:
        return False


def serve(host: str = "127.0.0.1", port: int = 8462):
    if uvicorn is None:
        print("Error: instala 'pip install fastapi uvicorn' para el dashboard web")
        return
    print(f"  Dashboard: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
