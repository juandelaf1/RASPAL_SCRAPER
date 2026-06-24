import csv
import io
import json
import subprocess
import sys
from pathlib import Path

from raspal.cache import Cache
from raspal.router import Router

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
    import uvicorn
except ImportError:
    FastAPI = None
    HTTPException = None
    UploadFile = None
    File = None
    HTMLResponse = None
    JSONResponse = None
    PlainTextResponse = None
    uvicorn = None

app = FastAPI(title="RASPAL SCRAPER Dashboard")

RECENT = []
RECENT_MAX = 20


TEMPLATES = {
    "": "Sin template",
    "product": {
        "label": "Producto (precio, nombre, disponibilidad)",
        "selectors": {"title": "h1", "price": ".price", "description": ".description"},
        "llm": {"template": "product"},
    },
    "article": {
        "label": "Artículo (titular, autor, fecha)",
        "selectors": {"title": "h1", "author": ".author", "date": ".date"},
        "llm": {"template": "article"},
    },
    "person": {
        "label": "Persona (nombre, rol, contacto)",
        "selectors": {"name": "h1", "role": ".role", "contact": ".contact"},
        "llm": {"template": "person"},
    },
    "review": {
        "label": "Reseña (rating, pros, contras)",
        "selectors": {"rating": ".rating", "title": "h2"},
        "llm": {"template": "review"},
    },
    "event": {
        "label": "Evento (fecha, lugar, organizador)",
        "selectors": {"title": "h1", "date": ".date", "location": ".location"},
        "llm": {"template": "event"},
    },
}


@app.get("/", response_class=HTMLResponse)
async def index():
    return PAGE_HTML


@app.get("/api/stats")
async def stats():
    router = Router()
    cache = Cache()
    return {
        "Cache activa": "✅",
        "Ollama": "✅" if _check_ollama() else "❌",
        "Playwright": "✅" if _check_playwright() else "⚠️",
        "Scrapers recientes": str(len(RECENT)),
    }


@app.post("/api/scrape")
async def scrape(url: str, engine: str = "auto", template: str = "", prompt: str = ""):
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
            text = ext.extract_text(result.html)
            meta = ext.extract_metadata(result.html)
            output["text"] = text[:2000] if text else ""
            output["metadata"] = meta

            if template:
                tpl = TEMPLATES.get(template)
                if tpl and isinstance(tpl, dict):
                    selectors = tpl.get("selectors", {})
                    if selectors:
                        try:
                            output["selectors"] = ext.extract_selectors_fast(result.html, selectors)
                        except Exception:
                            output["selectors"] = ext.extract_selectors(result.html, selectors)

                    try:
                        from raspal.models import LLMConfig
                        from raspal.llm import LLMExtractor

                        llm = LLMExtractor()
                        cfg = LLMConfig(template=template)
                        if prompt:
                            cfg.prompt = prompt
                        llm_result = llm.extract(text, cfg)
                        output["llm"] = llm_result
                    except Exception as e:
                        output["llm"] = {"error": str(e)}

        entry = {"url": url, "status": result.status, "engine": result.engine}
        if output.get("metadata"):
            entry["title"] = output["metadata"].get("title", "")
        RECENT.insert(0, entry)
        if len(RECENT) > RECENT_MAX:
            RECENT.pop()

        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/queue")
async def queue_urls(urls: list[str]):
    from raspal.queue import RequestQueue

    q = RequestQueue("raspal_queue.sqlite")
    for u in urls:
        q.push(u)
    q.close()
    return {"added": len(urls), "urls": urls}


@app.get("/api/queue/status")
async def queue_status():
    from raspal.queue import RequestQueue

    q = RequestQueue("raspal_queue.sqlite")
    pending = q.pending_count()
    q.close()
    return {"pending": pending}


@app.get("/api/recent")
async def recent():
    return RECENT


@app.post("/api/export")
async def export(data: dict):
    fmt = data.get("format", "json")
    items = data.get("data", [])
    if fmt == "csv":
        if not items:
            return PlainTextResponse("", media_type="text/csv")
        output = io.StringIO()
        fieldnames = set()
        for item in items:
            fieldnames.update(item.keys())
        fieldnames = sorted(fieldnames)
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)
        return PlainTextResponse(output.getvalue(), media_type="text/csv")
    else:
        return JSONResponse(items)


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


PAGE_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RASPAL SCRAPER — Dashboard</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#0d1117; color:#c9d1d9; }
  .header { background:#161b22; border-bottom:1px solid #30363d; padding:1rem 2rem; display:flex; align-items:center; gap:1rem; }
  .header h1 { color:#58a6ff; font-size:1.25rem; }
  .header .sub { color:#8b949e; font-size:0.8rem; }
  .container { max-width:1200px; margin:0 auto; padding:2rem; }
  .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:0.75rem; margin-bottom:1.5rem; }
  .stat-card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:1rem; display:flex; align-items:center; gap:0.75rem; }
  .stat-icon { font-size:1.5rem; }
  .stat-label { color:#8b949e; font-size:0.75rem; }
  .stat-value { font-size:1rem; font-weight:600; }
  .card { background:#161b22; border:1px solid #30363d; border-radius:8px; padding:1.5rem; margin-bottom:1rem; }
  .card h2 { color:#f0f6fc; font-size:1rem; margin-bottom:1rem; display:flex; align-items:center; gap:0.5rem; }
  .card h2 .badge { background:#238636; color:#fff; font-size:0.65rem; padding:2px 8px; border-radius:99px; font-weight:500; }
  .form-row { display:flex; gap:0.5rem; flex-wrap:wrap; }
  .form-row > * { flex:1; min-width:120px; }
  input,select,textarea,button { padding:0.6rem 0.75rem; border-radius:6px; border:1px solid #30363d; background:#0d1117; color:#c9d1d9; font-size:0.875rem; }
  input:focus,select:focus,textarea:focus { outline:none; border-color:#58a6ff; }
  button { background:#238636; border:none; cursor:pointer; font-weight:600; white-space:nowrap; }
  button:hover { background:#2ea043; }
  button:disabled { opacity:0.5; cursor:default; }
  button.danger { background:#da3633; }
  button.danger:hover { background:#f85149; }
  button.secondary { background:#21262d; border:1px solid #30363d; }
  button.secondary:hover { background:#30363d; }
  .result-card { background:#0d1117; border:1px solid #21262d; border-radius:6px; padding:1rem; margin-top:0.75rem; display:none; }
  .result-card.show { display:block; }
  .result-card.ok { border-left:3px solid #3fb950; }
  .result-card.err { border-left:3px solid #f85149; }
  .result-meta { display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:0.75rem; font-size:0.8rem; color:#8b949e; }
  .result-meta span { display:flex; align-items:center; gap:0.25rem; }
  .result-section { margin-top:0.75rem; }
  .result-section h3 { color:#58a6ff; font-size:0.8rem; margin-bottom:0.25rem; }
  .result-section .content { color:#c9d1d9; font-size:0.875rem; line-height:1.5; white-space:pre-wrap; word-break:break-word; max-height:200px; overflow-y:auto; background:#0d1117; padding:0.5rem; border-radius:4px; border:1px solid #21262d; }
  .result-actions { display:flex; gap:0.5rem; margin-top:0.75rem; }
  table { width:100%; border-collapse:collapse; font-size:0.875rem; }
  th { text-align:left; padding:0.6rem 0.75rem; background:#0d1117; color:#8b949e; border-bottom:1px solid #21262d; font-weight:500; }
  td { padding:0.6rem 0.75rem; border-bottom:1px solid #21262d; }
  tr:hover td { background:#161b22; }
  .status-badge { display:inline-block; padding:2px 8px; border-radius:99px; font-size:0.7rem; font-weight:600; }
  .status-badge.ok { background:#3fb95022; color:#3fb950; }
  .status-badge.err { background:#f8514922; color:#f85149; }
  .engine-badge { display:inline-block; padding:2px 8px; border-radius:99px; font-size:0.7rem; background:#1f6feb22; color:#58a6ff; }
  .empty { color:#8b949e; text-align:center; padding:2rem; }
  .spinner { display:inline-block; width:16px; height:16px; border:2px solid #30363d; border-top-color:#58a6ff; border-radius:50%; animation:spin .6s linear infinite; margin-right:0.5rem; vertical-align:middle; }
  @keyframes spin { to { transform:rotate(360deg); } }
  .toast { position:fixed; bottom:2rem; right:2rem; background:#238636; color:#fff; padding:0.75rem 1.5rem; border-radius:8px; font-size:0.875rem; transform:translateY(100px); opacity:0; transition:all .3s; }
  .toast.show { transform:translateY(0); opacity:1; }
  .toast.err { background:#da3633; }
  @media(max-width:768px) {
    .container { padding:1rem; }
    .form-row > * { min-width:100%; }
    .result-meta { flex-direction:column; gap:0.25rem; }
  }
</style>
</head>
<body>
<div class="header">
  <h1>RASPAL SCRAPER</h1>
  <span class="sub">Dashboard</span>
</div>
<div class="container">
  <div class="stats" id="stats"></div>

  <div class="card">
    <h2>🔍 Extraer datos de una URL</h2>
    <form id="scrape-form">
      <div class="form-row">
        <input type="url" name="url" placeholder="https://ejemplo.com/pagina" required style="flex:3">
        <select name="engine">
          <option value="auto">Motor: Auto</option>
          <option value="scrapling">Scrapling (rápido)</option>
          <option value="playwright">Playwright (JS)</option>
          <option value="stealth">Stealth (anti-bot)</option>
        </select>
        <select name="template">
          <option value="">Sin IA (solo texto)</option>
          <option value="product">Producto</option>
          <option value="article">Artículo</option>
          <option value="person">Persona</option>
          <option value="review">Reseña</option>
          <option value="event">Evento</option>
        </select>
        <button type="submit" id="scrape-btn">Extraer</button>
      </div>
    </form>
    <div id="result" class="result-card"></div>
  </div>

  <div class="card">
    <h2>📋 Historial <span class="badge" id="recent-count">0</span></h2>
    <div id="recent">
      <div class="empty">Aún no has extraído ninguna URL</div>
    </div>
  </div>
</div>

<div id="toast" class="toast"></div>

<script>
let resultsCache = [];

async function loadStats() {
  const res = await fetch('/api/stats');
  const s = await res.json();
  const icons = {'Cache activa':'💾','Ollama':'🤖','Playwright':'🎭','Scrapers recientes':'📋'};
  document.getElementById('stats').innerHTML = Object.entries(s).map(([k,v]) =>
    `<div class="stat-card"><div class="stat-icon">${icons[k]||'📊'}</div><div><div class="stat-label">${k}</div><div class="stat-value">${v}</div></div></div>`
  ).join('');
}

function showToast(msg, isErr) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast' + (isErr ? ' err' : '') + ' show';
  setTimeout(() => t.classList.remove('show'), 3000);
}

function escapeHtml(v) {
  if (v===null||v===undefined) return '';
  return String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function displayResult(data, isErr) {
  const div = document.getElementById('result');
  div.className = 'result-card show ' + (isErr ? 'err' : 'ok');
  if (isErr) {
    div.innerHTML = `<div style="color:#f85149;font-weight:600;">Error: ${escapeHtml(data)}</div>`;
    return;
  }
  const meta = data.metadata || {};
  const title = meta.title || data.url;
  const statusClass = data.status >= 200 && data.status < 400 ? 'ok' : 'err';
  let html = `
    <div class="result-meta">
      <span>🔗 ${escapeHtml(data.url)}</span>
      <span class="status-badge ${statusClass}">${data.status}</span>
      <span class="engine-badge">${escapeHtml(data.engine)}${data.cached ? ' (cache)' : ''}</span>
      ${meta.title ? `<span>📄 ${escapeHtml(meta.title)}</span>` : ''}
      ${meta.author ? `<span>✍️ ${escapeHtml(meta.author)}</span>` : ''}
      ${meta.date ? `<span>📅 ${escapeHtml(meta.date)}</span>` : ''}
    </div>`;

  if (data.selectors) {
    html += `<div class="result-section"><h3>📌 Datos extraídos (CSS selectors)</h3><div class="content">`;
    for (const [k,v] of Object.entries(data.selectors)) {
      html += `<b>${escapeHtml(k)}:</b> ${escapeHtml(JSON.stringify(v))}<br>`;
    }
    html += `</div></div>`;
  }

  if (data.llm) {
    html += `<div class="result-section"><h3>🤖 IA local (Ollama)</h3><div class="content">`;
    if (data.llm.error) {
      html += `<span style="color:#f85149;">${escapeHtml(data.llm.error)}</span>`;
    } else {
      html += `<pre style="margin:0;font-size:0.8rem;">${escapeHtml(JSON.stringify(data.llm, null, 2))}</pre>`;
    }
    html += `</div></div>`;
  }

  if (data.text) {
    const preview = data.text.length > 500 ? data.text.substring(0,500) + '...' : data.text;
    html += `<div class="result-section"><h3>📝 Texto extraído</h3><div class="content">${escapeHtml(preview)}</div></div>`;
  }

  html += `<div class="result-actions">
    <button class="secondary" onclick='copyResult(${JSON.stringify(JSON.stringify(data,null,2))})'>📋 Copiar JSON</button>
    <button class="secondary" onclick='downloadResult(${JSON.stringify(JSON.stringify(data,null,2))},"json")'>💾 Descargar JSON</button>
  </div>`;
  div.innerHTML = html;
}

function copyResult(str) {
  navigator.clipboard.writeText(JSON.parse(str)).then(() => showToast('Copiado al portapapeles'));
}

function downloadResult(str, fmt) {
  const data = JSON.parse(str);
  const blob = new Blob([JSON.stringify(data,null,2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'raspal-result.json';
  a.click();
  URL.revokeObjectURL(a.href);
}

async function loadRecent() {
  const res = await fetch('/api/recent');
  const items = await res.json();
  resultsCache = items;
  document.getElementById('recent-count').textContent = items.length;
  const container = document.getElementById('recent');
  if (!items.length) {
    container.innerHTML = '<div class="empty">Aún no has extraído ninguna URL</div>';
    return;
  }
  let html = `<table><thead><tr><th>URL</th><th>Estado</th><th>Motor</th><th>Título</th></tr></thead><tbody>`;
  for (const item of items) {
    const statusClass = item.status >= 200 && item.status < 400 ? 'ok' : 'err';
    html += `<tr><td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(item.url)}</td>
      <td><span class="status-badge ${statusClass}">${item.status}</span></td>
      <td><span class="engine-badge">${escapeHtml(item.engine)}</span></td>
      <td>${escapeHtml(item.title||'')}</td></tr>`;
  }
  html += '</tbody></table>';
  container.innerHTML = html;
}

document.getElementById('scrape-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = document.getElementById('scrape-btn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Extrayendo...';
  const form = e.target;
  try {
    const res = await fetch('/api/scrape', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({url: form.url.value, engine: form.engine.value, template: form.template.value}),
    });
    const data = await res.json();
    if (!res.ok) {
      displayResult(data.detail || 'Error desconocido', true);
      showToast('Error al extraer', true);
    } else {
      displayResult(data, false);
      showToast('✅ Datos extraídos correctamente');
      loadRecent();
      loadStats();
    }
  } catch(err) {
    displayResult('No se pudo conectar con el servidor', true);
    showToast('Error de conexión', true);
  }
  btn.disabled = false;
  btn.innerHTML = 'Extraer';
});

loadStats();
loadRecent();
</script>
</body>
</html>"""
