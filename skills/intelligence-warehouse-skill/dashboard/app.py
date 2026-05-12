"""
Prime Radiant — Le Plan Seldon en temps reel
Departement Trevize — R2D2

Usage: python app.py
Accessible: http://localhost:8842 (port Trevize)
Auth: login/password (configure dans config.json)
"""
import sqlite3, json, os, math, secrets, hashlib
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import requests as http_requests
from bs4 import BeautifulSoup

try:
    from ddgs import DDGS
    HAS_WEBSEARCH = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        HAS_WEBSEARCH = True
    except ImportError:
        HAS_WEBSEARCH = False

# ============================================================
# CONFIG
# ============================================================
APP_DIR = Path(__file__).parent
CONFIG_PATH = APP_DIR / "config.json"
GEO_DB = APP_DIR.parent / "data" / "warehouse-geo.db"
MAIN_DB = APP_DIR.parent / "data" / "warehouse.db"
TEMPLATE_DIR = APP_DIR / "templates"
PHI = (1 + math.sqrt(5)) / 2
FEIGENBAUM = 4.6692016091

# Load or create config
def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    # First run: create default config
    default_password = "trevize2026"
    salt = secrets.token_hex(16)
    pw_hash = hashlib.sha256((default_password + salt).encode()).hexdigest()
    config = {
        "username": "mike",
        "password_hash": pw_hash,
        "salt": salt,
        "secret_key": secrets.token_hex(32),
        "port": 8842,
        "host": "127.0.0.1",
        "first_run": True,
        "note": "Change password on first login! Default: trevize2026"
    }
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    return config

config = load_config()

# ============================================================
# APP
# ============================================================
app = FastAPI(title="Prime Radiant", docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key=config["secret_key"])

os.makedirs(TEMPLATE_DIR, exist_ok=True)

# ============================================================
# AUTH
# ============================================================
def verify_password(password: str) -> bool:
    pw_hash = hashlib.sha256((password + config["salt"]).encode()).hexdigest()
    return pw_hash == config["password_hash"]

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user

# ============================================================
# DB HELPERS
# ============================================================
@contextmanager
def get_geo():
    db = sqlite3.connect(str(GEO_DB))
    db.row_factory = sqlite3.Row
    try:
        yield db.cursor()
    finally:
        db.close()

@contextmanager
def get_main():
    db = sqlite3.connect(str(MAIN_DB))
    db.row_factory = sqlite3.Row
    try:
        yield db.cursor()
    finally:
        db.close()

def query_all(cursor, sql, params=()):
    cursor.execute(sql, params)
    return [dict(r) for r in cursor.fetchall()]

# ============================================================
# DATA FUNCTIONS
# ============================================================
def get_dashboard_data():
    data = {"generated": datetime.now().strftime("%d/%m/%Y %H:%M"), "phi": PHI}

    with get_geo() as g:
        data["fractals"] = query_all(g, "SELECT * FROM fractal_patterns ORDER BY fractal_depth DESC, urgency DESC")
        data["predictions"] = query_all(g, "SELECT * FROM predictions WHERE status='pending' ORDER BY probability DESC")
        data["butterflies"] = query_all(g, "SELECT * FROM butterflies WHERE status != 'dead' ORDER BY current_magnitude DESC")
        data["amplifiers"] = query_all(g, "SELECT * FROM amplifiers ORDER BY amplification_factor DESC LIMIT 10")
        data["events"] = query_all(g, "SELECT * FROM events ORDER BY impact_score DESC")
        data["golden"] = query_all(g, "SELECT * FROM golden_indicators ORDER BY phi_threshold_breached DESC, change_ratio DESC")
        data["chains"] = query_all(g, "SELECT * FROM temporal_chains WHERE status='active'")
        data["phi_alerts"] = query_all(g, "SELECT * FROM golden_indicators WHERE phi_threshold_breached=1")

        chain_nodes = {}
        for ch in data["chains"]:
            chain_nodes[ch["id"]] = query_all(g, "SELECT * FROM temporal_nodes WHERE chain_id=? ORDER BY t_position", (ch["id"],))
        data["chain_nodes"] = chain_nodes

        # Stats GEO
        geo_stats = {}
        for t in ['events','analyses','sources','predictions','fractal_patterns','butterflies','amplifiers','golden_indicators','temporal_nodes','ateliers']:
            g.execute(f"SELECT COUNT(*) FROM {t}")
            geo_stats[t] = g.fetchone()[0]
        data["geo_stats"] = geo_stats

    with get_main() as m:
        data["opportunities"] = query_all(m, "SELECT * FROM opportunities WHERE status='detected' ORDER BY urgency DESC LIMIT 10")
        data["threats"] = query_all(m, "SELECT * FROM threats WHERE status='active' ORDER BY severity DESC")

        main_stats = {}
        for t in ['findings','opportunities','threats','connections','patterns']:
            m.execute(f"SELECT COUNT(*) FROM {t}")
            main_stats[t] = m.fetchone()[0]
        data["main_stats"] = main_stats

    # Lentille Gravitationnelle: findings tagged matiere-noire + cross-bloc distortions
    with get_main() as m2:
        # Findings avec tag matiere-noire ou lentille
        data["dark_matter"] = query_all(m2, "SELECT * FROM findings WHERE tags LIKE '%matiere-noire%' OR tags LIKE '%lentille%' OR title LIKE '%LENTILLE%' ORDER BY ingested_at DESC LIMIT 10")

        # Cross-bloc: findings press_review recent (WEST vs BRICS)
        data["press_west"] = query_all(m2, "SELECT * FROM findings WHERE source_type='press_review' AND source LIKE '%Reuters%' OR source LIKE '%Bloomberg%' OR source LIKE '%CNBC%' OR source LIKE '%FT%' ORDER BY ingested_at DESC LIMIT 5")
        data["press_brics"] = query_all(m2, "SELECT * FROM findings WHERE source_type='press_review' AND (source LIKE '%Al Jazeera%' OR source LIKE '%CGTN%' OR source LIKE '%Global Times%' OR source LIKE '%SCMP%') ORDER BY ingested_at DESC LIMIT 5")

        # Distorsion pairs: findings du meme jour avec sources differentes
        data["distortions"] = []
        west_recent = query_all(m2, "SELECT id, title, key_points, source FROM findings WHERE source_type='press_review' AND tags LIKE '%geopolitique%' ORDER BY ingested_at DESC LIMIT 3")
        brics_recent = query_all(m2, "SELECT id, title, key_points, source FROM findings WHERE source_type='press_review' AND (source LIKE '%Al Jazeera%' OR source LIKE '%CGTN%' OR source LIKE '%Global Times%') ORDER BY ingested_at DESC LIMIT 3")
        for w in west_recent:
            for b in brics_recent:
                data["distortions"].append({"west": w, "brics": b})

    # Microscope-Lentille-Telescope counts
    with get_geo() as g3:
        data["microscope"] = {"butterflies": len(data.get("butterflies", [])), "label": "Micro-events"}
        data["lentille"] = {"amplifiers": len(data.get("amplifiers", [])), "distortions": len(data.get("distortions", [])), "dark_matter": len(data.get("dark_matter", [])), "label": "Distorsions"}
        data["telescope"] = {"fractals": len(data.get("fractals", [])), "predictions": len(data.get("predictions", [])), "label": "Patterns globaux"}

    # Deadlines
    today = datetime.now().date()
    data["deadlines"] = [
        {"name": "ULTIMATUM ORMUZ (Trump)", "date": "2026-04-06", "days": max(0,(datetime(2026,4,6).date() - today).days), "severity": "critical"},
        {"name": "NIS2 Belgique", "date": "2026-04-18", "days": (datetime(2026,4,18).date() - today).days, "severity": "critical"},
        {"name": "Ban LNG russe EU", "date": "2026-04-25", "days": (datetime(2026,4,25).date() - today).days, "severity": "critical"},
        {"name": "MiCA grandfathering", "date": "2026-07-01", "days": (datetime(2026,7,1).date() - today).days, "severity": "high"},
        {"name": "AI Act haut risque", "date": "2026-08-02", "days": (datetime(2026,8,2).date() - today).days, "severity": "high"},
        {"name": "CRA vulnerabilites 24h", "date": "2026-09-11", "days": (datetime(2026,9,11).date() - today).days, "severity": "medium"},
        {"name": "Data Act design", "date": "2026-09-12", "days": (datetime(2026,9,12).date() - today).days, "severity": "medium"},
        {"name": "Reserves IEA epuisees (est.)", "date": "2026-08-01", "days": (datetime(2026,8,1).date() - today).days, "severity": "critical"},
    ]
    data["deadlines"].sort(key=lambda x: x["days"])

    return data

# ============================================================
# ROUTES
# ============================================================
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    first_run = config.get("first_run", False)
    return HTMLResponse(LOGIN_HTML.replace("{{FIRST_RUN}}", "block" if first_run else "none"))

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == config["username"] and verify_password(password):
        request.session["user"] = username
        if config.get("first_run"):
            config["first_run"] = False
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f, indent=2)
        return RedirectResponse("/", status_code=303)
    return HTMLResponse(LOGIN_HTML.replace("{{FIRST_RUN}}", "none").replace("<!--ERROR-->", '<div class="error">Identifiants incorrects</div>'))

@app.post("/change-password")
async def change_password(request: Request, current_password: str = Form(...), new_password: str = Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    if not verify_password(current_password):
        return RedirectResponse("/settings?error=wrong_password", status_code=303)
    new_salt = secrets.token_hex(16)
    new_hash = hashlib.sha256((new_password + new_salt).encode()).hexdigest()
    config["password_hash"] = new_hash
    config["salt"] = new_salt
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    return RedirectResponse("/settings?success=1", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    data = get_dashboard_data()
    return HTMLResponse(render_dashboard(data))

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, error: str = None, success: str = None):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    return HTMLResponse(SETTINGS_HTML.replace("{{ERROR}}", "block" if error else "none").replace("{{SUCCESS}}", "block" if success else "none"))

@app.get("/api/data")
async def api_data(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401)
    data = get_dashboard_data()
    return {"status": "ok", "generated": data["generated"], "stats": {**data["main_stats"], **data["geo_stats"]}}

# ============================================================
# AGENT TREVIZE — Chat intelligent sur les warehouses
# ============================================================
def agent_search(query: str) -> dict:
    """Recherche intelligente dans les deux warehouses"""
    query_lower = query.lower()
    results = {"findings": [], "events": [], "predictions": [], "fractals": [], "golden": [], "butterflies": [], "summary_parts": []}

    # Keywords mapping
    keywords = query_lower.split()

    with get_main() as m:
        # Search findings
        for kw in keywords:
            if len(kw) < 3:
                continue
            found = query_all(m, "SELECT id, title, summary, seldon_score, source, article_date FROM findings WHERE title LIKE ? OR summary LIKE ? OR tags LIKE ? ORDER BY seldon_score DESC LIMIT 5",
                (f'%{kw}%', f'%{kw}%', f'%{kw}%'))
            for f in found:
                if f not in results["findings"]:
                    results["findings"].append(f)

    with get_geo() as g:
        # Search events
        for kw in keywords:
            if len(kw) < 3:
                continue
            found = query_all(g, "SELECT id, title, summary, impact_score, status, event_type FROM events WHERE title LIKE ? OR summary LIKE ? ORDER BY impact_score DESC LIMIT 5",
                (f'%{kw}%', f'%{kw}%'))
            for e in found:
                if e not in results["events"]:
                    results["events"].append(e)

        # Search predictions
        found = query_all(g, "SELECT title, prediction_text, probability, timeframe, status FROM predictions WHERE status='pending' ORDER BY probability DESC")
        for p in found:
            for kw in keywords:
                if kw in p["title"].lower() or kw in p["prediction_text"].lower():
                    if p not in results["predictions"]:
                        results["predictions"].append(p)

        # Search fractal patterns
        found = query_all(g, "SELECT title, pattern_statement, fractal_depth, prediction, urgency FROM fractal_patterns ORDER BY fractal_depth DESC")
        for f in found:
            for kw in keywords:
                if kw in f["title"].lower() or kw in (f["pattern_statement"] or "").lower():
                    if f not in results["fractals"]:
                        results["fractals"].append(f)

        # Search golden indicators
        found = query_all(g, "SELECT name, atelier_code, current_value, change_ratio, phi_threshold_breached, variance_trend, unit FROM golden_indicators ORDER BY phi_threshold_breached DESC")
        for gi in found:
            for kw in keywords:
                if kw in gi["name"].lower() or kw in gi["atelier_code"].lower():
                    if gi not in results["golden"]:
                        results["golden"].append(gi)

        # Search butterflies
        found = query_all(g, "SELECT title, status, current_magnitude, fibonacci_match, origin_atelier FROM butterflies WHERE status != 'dead' ORDER BY current_magnitude DESC")
        for b in found:
            for kw in keywords:
                if kw in b["title"].lower():
                    if b not in results["butterflies"]:
                        results["butterflies"].append(b)

    # Build summary
    total = sum(len(v) for v in results.values() if isinstance(v, list))
    results["total_hits"] = total
    results["query"] = query

    return results

def format_agent_response(results: dict) -> str:
    """Formate la reponse de l'agent en HTML lisible"""
    q = results["query"]
    total = results["total_hits"]

    html = f'<div style="margin-bottom:15px"><strong>Recherche:</strong> "{q}" — {total} resultats</div>'

    if not total:
        html += '<div style="color:var(--dim);font-style:italic">Aucun resultat. Essayez d autres mots-cles.</div>'
        return html

    # Findings
    if results["findings"]:
        html += '<h3 style="color:var(--accent);margin:15px 0 8px;font-size:1.1em">FINDINGS</h3>'
        for f in results["findings"][:5]:
            html += f'<div style="padding:10px;margin:5px 0;background:rgba(100,68,255,0.08);border-radius:8px;border-left:3px solid var(--accent)">'
            html += f'<div><span class="badge" style="background:var(--gold);color:black">Seldon {f["seldon_score"]}/5</span> <strong>{f["title"][:80]}</strong></div>'
            html += f'<div style="color:var(--dim);font-size:0.9em;margin-top:5px">{(f["summary"] or "")[:200]}...</div>'
            html += '</div>'

    # Events
    if results["events"]:
        html += '<h3 style="color:var(--orange);margin:15px 0 8px;font-size:1.1em">EVENEMENTS GEO</h3>'
        for e in results["events"][:5]:
            sc = e.get("impact_score", 3)
            html += f'<div style="padding:10px;margin:5px 0;background:rgba(255,136,0,0.08);border-radius:8px;border-left:3px solid var(--orange)">'
            html += f'<div><span class="badge" style="background:var(--orange)">{sc}/5</span> <strong>{e["title"][:80]}</strong> <span class="badge" style="background:var(--border)">{e["status"]}</span></div>'
            html += f'<div style="color:var(--dim);font-size:0.9em;margin-top:5px">{(e["summary"] or "")[:200]}...</div>'
            html += '</div>'

    # Predictions
    if results["predictions"]:
        html += '<h3 style="color:var(--red);margin:15px 0 8px;font-size:1.1em">PREDICTIONS</h3>'
        for p in results["predictions"][:5]:
            color = '#ff4444' if p["probability"] >= 70 else '#ff8800' if p["probability"] >= 60 else '#ffcc00'
            html += f'<div style="padding:10px;margin:5px 0;background:rgba(255,68,68,0.08);border-radius:8px;border-left:3px solid var(--red)">'
            html += f'<div><span class="badge" style="background:{color}">{p["probability"]}%</span> <strong>{p["title"][:80]}</strong></div>'
            html += f'<div style="color:var(--dim);font-size:0.9em;margin-top:5px">Horizon: {p["timeframe"]}</div>'
            html += '</div>'

    # Fractals
    if results["fractals"]:
        html += '<h3 style="color:var(--gold);margin:15px 0 8px;font-size:1.1em">PATTERNS FRACTALS</h3>'
        for f in results["fractals"][:3]:
            html += f'<div style="padding:10px;margin:5px 0;background:rgba(255,215,0,0.08);border-radius:8px;border-left:3px solid var(--gold)">'
            html += f'<div><span style="font-family:monospace;color:var(--gold)">{"█" * f["fractal_depth"]}{"░" * (5-f["fractal_depth"])}</span> <strong>{f["title"]}</strong></div>'
            html += f'<div style="color:var(--dim);font-size:0.9em;margin-top:5px">{(f["pattern_statement"] or "")[:200]}</div>'
            html += '</div>'

    # Golden
    if results["golden"]:
        html += '<h3 style="color:var(--cyan);margin:15px 0 8px;font-size:1.1em">INDICATEURS</h3>'
        for gi in results["golden"][:5]:
            phi_alert = ' PHI BREACH!' if gi.get("phi_threshold_breached") else ''
            html += f'<div style="padding:8px;margin:3px 0"><span class="badge" style="background:var(--blue)">{gi["atelier_code"]}</span> <strong>{gi["name"]}</strong>: {gi["current_value"]:.1f} {gi["unit"]} (ratio: {(gi["change_ratio"] or 0):.3f}) <span style="color:var(--red)">{phi_alert}</span></div>'

    # Butterflies
    if results["butterflies"]:
        html += '<h3 style="color:var(--green);margin:15px 0 8px;font-size:1.1em">PAPILLONS</h3>'
        for b in results["butterflies"][:3]:
            html += f'<div style="padding:8px;margin:3px 0"><span class="badge" style="background:var(--green)">{b["status"]}</span> <strong>{b["title"][:60]}</strong> — magnitude x{b["current_magnitude"]:.0f}</div>'

    return html

def web_search(query: str, max_results: int = 21, region: str = "wt-wt", perspective: str = None) -> list:
    """Recherche web live via DuckDuckGo"""
    if not HAS_WEBSEARCH:
        return []

    # Perspective-based search modifications
    perspective_sites = {
        "west": "site:reuters.com OR site:bloomberg.com OR site:ft.com OR site:bbc.com OR site:cnbc.com",
        "brics": "site:cgtn.com OR site:globaltimes.cn OR site:aljazeera.com OR site:scmp.com OR site:rt.com",
        "chine": "site:cgtn.com OR site:globaltimes.cn OR site:scmp.com OR site:chinadaily.com.cn",
        "france": "site:lemonde.fr OR site:lesechos.fr OR site:liberation.fr OR site:france24.com",
        "belgique": "site:lecho.be OR site:lesoir.be OR site:vrt.be OR site:rtbf.be OR site:agoria.be",
        "tech": "site:techcrunch.com OR site:arstechnica.com OR site:theverge.com OR site:wired.com",
        "finance": "site:bloomberg.com OR site:ft.com OR site:cnbc.com OR site:wsj.com",
    }

    search_query = query
    if perspective and perspective.lower() in perspective_sites:
        search_query = f"{query} ({perspective_sites[perspective.lower()]})"

    try:
        raw = DDGS().text(search_query, region=region, max_results=max_results)
        results = []
        for r in raw:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", r.get("url", "")),
                "body": r.get("body", r.get("snippet", "")),
            })
        return results
    except Exception as e:
        return [{"title": f"Erreur recherche: {str(e)}", "url": "", "body": str(e)}]

def format_web_results(results: list, query: str, perspective: str = None) -> str:
    """Formate les resultats web en HTML"""
    if not results:
        return '<div style="color:var(--dim)">Aucun resultat web. Verifiez votre connexion.</div>'

    persp_label = f' <span class="badge" style="background:var(--magenta)">vue: {perspective}</span>' if perspective else ''
    html = f'<div style="margin-bottom:15px;font-size:1.1em"><strong>Recherche web:</strong> "{query}"{persp_label} — {len(results)} resultats</div>'

    for i, r in enumerate(results, 1):
        # Color by rank
        if i <= 3:
            border_color = "var(--gold)"
            rank_color = "var(--gold)"
        elif i <= 7:
            border_color = "var(--accent)"
            rank_color = "var(--accent)"
        elif i <= 13:
            border_color = "var(--blue)"
            rank_color = "var(--blue)"
        else:
            border_color = "var(--border)"
            rank_color = "var(--dim)"

        url = r.get("url", "")
        domain = url.split("/")[2] if url and "/" in url else ""

        # Detect bloc from domain
        west_domains = ['reuters.com','bloomberg.com','ft.com','bbc.com','cnbc.com','nytimes.com','wsj.com','theguardian.com','npr.org']
        brics_domains = ['cgtn.com','globaltimes.cn','aljazeera.com','scmp.com','rt.com','tass.com','xinhua','presstv']
        bloc_badge = ""
        for wd in west_domains:
            if wd in domain:
                bloc_badge = '<span class="badge" style="background:var(--blue);margin-left:5px">WEST</span>'
                break
        for bd in brics_domains:
            if bd in domain:
                bloc_badge = '<span class="badge" style="background:var(--red);margin-left:5px">BRICS</span>'
                break

        html += f'<div style="padding:12px;margin:8px 0;background:var(--card);border-radius:10px;border-left:4px solid {border_color}">'
        html += f'<div style="display:flex;align-items:center;gap:10px">'
        html += f'<span style="color:{rank_color};font-size:1.3em;font-weight:bold;min-width:30px">#{i}</span>'
        html += f'<div style="flex:1">'
        html += f'<div style="font-size:1.05em"><strong>{r["title"][:90]}</strong>{bloc_badge}</div>'
        html += f'<div style="color:var(--dim);font-size:0.85em;margin-top:3px">{domain}</div>'
        html += f'</div></div>'
        html += f'<div style="color:var(--text);font-size:0.95em;margin-top:8px;line-height:1.4">{r["body"][:250]}</div>'
        if url:
            from urllib.parse import quote
            html += f'<div style="margin-top:8px;display:flex;gap:15px">'
            html += f'<a href="{url}" target="_blank" style="color:var(--accent);font-size:0.95em">Ouvrir l article</a>'
            html += f'<a href="/agent/summary?url={quote(url, safe="")}" style="color:var(--gold);font-size:0.95em;font-weight:bold">Resume 15 lignes</a>'
            html += '</div>'
        html += '</div>'

    return html

@app.get("/agent", response_class=HTMLResponse)
async def agent_page(request: Request, q: str = None, mode: str = "auto", perspective: str = None, max_results: str = "21"):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    response_html = ""
    max_r = min(int(max_results), 50)

    if q:
        if mode == "warehouse":
            # Search warehouses only
            results = agent_search(q)
            response_html = format_agent_response(results)
        elif mode == "web":
            # Search web only
            web_results = web_search(q, max_results=max_r, perspective=perspective)
            response_html = format_web_results(web_results, q, perspective)
        else:
            # AUTO: search warehouses first, then web if needed
            wh_results = agent_search(q)
            if wh_results["total_hits"] >= 3:
                response_html = '<div style="margin-bottom:10px"><span class="badge" style="background:var(--accent)">WAREHOUSE</span> Resultats internes</div>'
                response_html += format_agent_response(wh_results)
            # Always add web results in auto mode
            web_results = web_search(q, max_results=max_r, perspective=perspective)
            if web_results:
                response_html += '<div style="margin:25px 0 10px;border-top:2px solid var(--gold);padding-top:15px"><span class="badge" style="background:var(--orange)">WEB LIVE</span> Resultats internet</div>'
                response_html += format_web_results(web_results, q, perspective)

    page = AGENT_HTML.replace("{{QUERY}}", q or "").replace("{{RESPONSE}}", response_html)
    page = page.replace("{{MODE}}", mode or "auto").replace("{{PERSPECTIVE}}", perspective or "")
    return HTMLResponse(page)

def fetch_and_summarize(url: str, num_lines: int = 15) -> dict:
    """Fetch une page web et extrait un resume"""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
        resp = http_requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Remove scripts, styles, nav, footer
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript']):
            tag.decompose()

        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Sans titre"

        # Get meta description
        meta_desc = ""
        meta = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if meta:
            meta_desc = meta.get('content', '')

        # Extract paragraphs
        paragraphs = []
        for p in soup.find_all(['p', 'article']):
            text = p.get_text().strip()
            # Filter: min 40 chars, no cookie/nav junk
            if len(text) > 40 and not any(junk in text.lower() for junk in ['cookie', 'javascript', 'subscribe', 'newsletter', 'sign up', 'log in', 'accept', 'privacy policy']):
                paragraphs.append(text)

        if not paragraphs and meta_desc:
            paragraphs = [meta_desc]

        # Take first N meaningful paragraphs, split into lines
        content_lines = []
        for p in paragraphs:
            # Split long paragraphs into sentences
            sentences = p.replace('. ', '.\n').split('\n')
            for s in sentences:
                s = s.strip()
                if len(s) > 30:
                    content_lines.append(s)
                if len(content_lines) >= num_lines:
                    break
            if len(content_lines) >= num_lines:
                break

        return {
            "title": title_text,
            "url": url,
            "description": meta_desc[:300],
            "lines": content_lines[:num_lines],
            "total_paragraphs": len(paragraphs),
            "success": True
        }
    except Exception as e:
        return {"title": "Erreur", "url": url, "lines": [str(e)], "success": False}

@app.get("/agent/summary", response_class=HTMLResponse)
async def agent_summary(request: Request, url: str = ""):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    if not url:
        return HTMLResponse("<p>URL manquante</p>")

    result = fetch_and_summarize(url, num_lines=15)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Resume — {result['title'][:50]}</title>
<style>
body{{background:#050510;color:#f0f0ff;font-family:'Segoe UI',system-ui;padding:30px;font-size:18px;line-height:1.6;max-width:900px;margin:0 auto}}
h1{{color:#ffd700;font-size:1.6em;line-height:1.3}}
.meta{{color:#aaaacc;font-size:0.9em;margin:10px 0 20px}}
.line{{padding:8px 0;border-bottom:1px solid rgba(42,42,90,0.3);font-size:1.05em}}
.line-num{{color:#ffd700;font-weight:bold;margin-right:10px;min-width:30px;display:inline-block}}
.nav{{margin-bottom:20px}}
.nav a{{color:#8866ff;text-decoration:none;padding:5px 10px;border:1px solid #8866ff;border-radius:5px;font-size:1em}}
.nav a:hover{{background:#8866ff;color:white}}
.source-link{{display:inline-block;margin-top:15px;padding:10px 20px;background:#8866ff;color:white;border-radius:8px;text-decoration:none;font-size:1em}}
.source-link:hover{{background:#9977ff}}
.desc{{background:rgba(100,68,255,0.1);padding:15px;border-radius:8px;margin:15px 0;font-style:italic;color:#aaaacc}}
</style></head><body>
<div class="nav"><a href="javascript:history.back()">Retour aux resultats</a> <a href="/">Dashboard</a> <a href="/agent">Agent</a></div>
<h1>{result['title']}</h1>
<div class="meta">{result['url'][:80]}</div>"""

    if result.get("description"):
        html += f'<div class="desc">{result["description"]}</div>'

    html += '<div style="margin:20px 0">'
    if result["success"] and result["lines"]:
        for i, line in enumerate(result["lines"], 1):
            html += f'<div class="line"><span class="line-num">{i}.</span>{line}</div>'
    else:
        html += '<div style="color:#ff5555">Impossible d extraire le contenu de cette page.</div>'

    html += '</div>'
    html += f'<a class="source-link" href="{url}" target="_blank">Lire l article complet</a>'
    html += '<div style="color:#aaaacc;margin-top:30px;font-size:0.85em;font-style:italic">Resume extractif — 15 lignes. Pour un resume IA, connecter LiteLLM (prochaine etape).</div>'
    html += '</body></html>'

    return HTMLResponse(html)

# ============================================================
# TEMPLATES (inline for portability)
# ============================================================
LOGIN_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Login — Prime Radiant</title>
<style>
body{background:#0a0a1a;color:#e0e0f0;font-family:'Segoe UI',system-ui;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:#12122a;border:1px solid #2a2a4a;border-radius:12px;padding:40px;width:350px;text-align:center}
h1{color:#ffd700;margin-bottom:5px;font-size:2em}
.sub{color:#8888aa;font-style:italic;margin-bottom:25px}
input{width:100%;padding:12px;margin:8px 0;background:#1a1a3a;border:1px solid #2a2a4a;border-radius:6px;color:#e0e0f0;font-size:1em}
input:focus{outline:none;border-color:#6644ff}
button{width:100%;padding:12px;margin-top:15px;background:#6644ff;color:white;border:none;border-radius:6px;font-size:1em;cursor:pointer}
button:hover{background:#7755ff}
.error{background:rgba(255,68,68,0.2);border:1px solid #ff4444;padding:10px;border-radius:6px;margin:10px 0;color:#ff4444}
.first-run{background:rgba(255,215,0,0.15);border:1px solid #ffd700;padding:10px;border-radius:6px;margin:10px 0;color:#ffd700;display:{{FIRST_RUN}};font-size:0.85em}
</style></head><body>
<div class="login-box">
<h1>&#x1F52E;</h1>
<h1>Prime Radiant</h1>
<div class="sub">Departement Trevize</div>
<div class="first-run">Premier lancement! Login: mike / trevize2026<br>Changez le mot de passe apres connexion.</div>
<!--ERROR-->
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Utilisateur" required autofocus>
<input type="password" name="password" placeholder="Mot de passe" required>
<button type="submit">Entrer</button>
</form>
</div></body></html>"""

AGENT_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Agent Trevize — Prime Radiant</title>
<style>
body{background:#050510;color:#f0f0ff;font-family:'Segoe UI',system-ui;padding:25px;font-size:18px;line-height:1.5;max-width:1000px;margin:0 auto}
h1{color:#ffd700;font-size:2em;margin-bottom:5px}
.sub{color:#aaaacc;font-style:italic;margin-bottom:25px}
.nav{margin-bottom:20px}
.nav a{color:#8866ff;text-decoration:none;margin-right:20px;font-size:1.1em;padding:5px 10px;border:1px solid #8866ff;border-radius:5px}
.nav a:hover{background:#8866ff;color:white}
.search-box{display:flex;gap:12px;margin:20px 0}
.search-box input{flex:1;padding:15px 20px;background:#10102a;border:2px solid #2a2a5a;border-radius:10px;color:#f0f0ff;font-size:1.1em}
.search-box input:focus{outline:none;border-color:#ffd700}
.search-box button{padding:15px 30px;background:#8866ff;color:white;border:none;border-radius:10px;font-size:1.1em;cursor:pointer;font-weight:bold}
.search-box button:hover{background:#9977ff}
.suggestions{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 20px}
.sug{padding:8px 15px;background:#10102a;border:1px solid #2a2a5a;border-radius:20px;color:#aaaacc;cursor:pointer;font-size:0.95em;text-decoration:none}
.sug:hover{border-color:#ffd700;color:#ffd700}
.response{margin-top:20px;padding:20px;background:#10102a;border:1px solid #2a2a5a;border-radius:12px;min-height:100px}
h3{margin:0}
.badge{display:inline-block;padding:4px 10px;border-radius:5px;font-size:0.85em;font-weight:bold}
:root{--accent:#8866ff;--gold:#ffd700;--red:#ff5555;--orange:#ffaa22;--green:#55dd55;--blue:#55aaff;--cyan:#00dddd;--dim:#aaaacc;--border:#2a2a5a;--card:#10102a}
</style></head><body>
<div class="nav"><a href="/">Dashboard</a><a href="/settings">Settings</a><a href="/logout">Logout</a></div>
<h1>Agent Trevize</h1>
<div class="sub">Interrogez les warehouses — 257 findings, 12 events, 7 predictions</div>

<form method="GET" action="/agent" class="search-box">
<input type="text" name="q" placeholder="Recherchez n importe quoi... (news tech Paris, cacao Bresil, evenements vus de Chine...)" value="{{QUERY}}" autofocus>
<button type="submit">Chercher</button>
</form>

<div style="display:flex;gap:15px;flex-wrap:wrap;margin:10px 0 5px;align-items:center">
<div style="color:var(--dim);font-size:0.95em">Mode:</div>
<a class="sug" href="/agent?q={{QUERY}}&mode=auto">Auto (warehouse + web)</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=warehouse">Warehouse seul</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web">Web seul</a>
</div>

<div style="display:flex;gap:10px;flex-wrap:wrap;margin:5px 0 15px;align-items:center">
<div style="color:var(--dim);font-size:0.95em">Perspective:</div>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=west">Bloc WEST</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=brics">Bloc BRICS</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=chine">Vue de Chine</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=france">Vue de France</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=belgique">Vue Belgique</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=tech">Tech</a>
<a class="sug" href="/agent?q={{QUERY}}&mode=web&perspective=finance">Finance</a>
</div>

<div style="color:var(--dim);font-size:0.9em;margin-bottom:10px">Exemples de recherches:</div>
<div class="suggestions">
<a class="sug" href="/agent?q=news tech Paris 2026&mode=web">news tech Paris</a>
<a class="sug" href="/agent?q=marche cacao Bresil 2026&mode=web">cacao Bresil</a>
<a class="sug" href="/agent?q=evenements internationaux avril 2026&mode=web&perspective=chine">evenements vus de Chine</a>
<a class="sug" href="/agent?q=Ormuz Iran guerre&mode=auto">Ormuz (warehouse+web)</a>
<a class="sug" href="/agent?q=PME Wallonie digital 2026&mode=web&perspective=belgique">PME Wallonie</a>
<a class="sug" href="/agent?q=AI regulation Europe 2026&mode=web&perspective=tech">AI regulation EU</a>
<a class="sug" href="/agent?q=gold price BRICS central bank 2026&mode=web&perspective=finance">Or + BRICS</a>
<a class="sug" href="/agent?q=semiconductor chip war ASML 2026&mode=web">Guerre des puces</a>
<a class="sug" href="/agent?q=dedollarisation yuan SWIFT 2026&mode=web&perspective=brics">Dedollarisation (vue BRICS)</a>
<a class="sug" href="/agent?q=NIS2 cybersecurity Belgium April 2026&mode=web&perspective=belgique">NIS2 Belgique</a>
</div>

<div class="response">{{RESPONSE}}</div>

<div style="text-align:center;color:#aaaacc;margin-top:30px;font-size:0.9em;font-style:italic">
"La seule source de la verite est LA VERITE" — Loi Foundation
</div>
</body></html>"""

SETTINGS_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Settings — Prime Radiant</title>
<style>
body{background:#0a0a1a;color:#e0e0f0;font-family:'Segoe UI',system-ui;padding:40px;max-width:500px;margin:0 auto}
h1{color:#ffd700}
input{width:100%;padding:10px;margin:8px 0;background:#1a1a3a;border:1px solid #2a2a4a;border-radius:6px;color:#e0e0f0}
button{padding:10px 20px;background:#6644ff;color:white;border:none;border-radius:6px;cursor:pointer;margin-top:10px}
a{color:#6644ff}
.msg-err{background:rgba(255,68,68,0.2);padding:10px;border-radius:6px;color:#ff4444;display:{{ERROR}}}
.msg-ok{background:rgba(68,204,68,0.2);padding:10px;border-radius:6px;color:#44cc44;display:{{SUCCESS}}}
</style></head><body>
<h1>Settings</h1>
<a href="/">← Retour au dashboard</a>
<div class="msg-err">Mot de passe actuel incorrect</div>
<div class="msg-ok">Mot de passe change avec succes!</div>
<h2 style="margin-top:30px">Changer le mot de passe</h2>
<form method="POST" action="/change-password">
<input type="password" name="current_password" placeholder="Mot de passe actuel" required>
<input type="password" name="new_password" placeholder="Nouveau mot de passe" required>
<button type="submit">Changer</button>
</form>
<br><a href="/logout">Se deconnecter</a>
</body></html>"""

# ============================================================
# DASHBOARD RENDERER
# ============================================================
def render_dashboard(data):
    def urgency_color(u):
        if u >= 5: return '#ff4444'
        if u >= 4: return '#ff8800'
        if u >= 3: return '#ffcc00'
        return '#44aa44'

    def depth_bar(d):
        return '<span style="color:#ffd700;font-family:monospace;letter-spacing:2px">' + '█' * d + '<span style="color:#2a2a4a">' + '░' * (5-d) + '</span></span>'

    def deadline_badge(d):
        if d["days"] <= 14: return f'<span class="badge" style="background:#ff4444;animation:pulse 1s infinite">{d["days"]}j</span>'
        if d["days"] <= 30: return f'<span class="badge" style="background:#ff8800">{d["days"]}j</span>'
        if d["days"] <= 90: return f'<span class="badge" style="background:#ffcc00;color:black">{d["days"]}j</span>'
        return f'<span class="badge" style="background:#44aa44">{d["days"]}j</span>'

    # Stats
    gs = data["geo_stats"]
    ms = data["main_stats"]

    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Prime Radiant — Departement Trevize</title>
<style>
:root{{--bg:#050510;--card:#10102a;--border:#2a2a5a;--text:#f0f0ff;--dim:#aaaacc;--accent:#8866ff;--gold:#ffd700;--red:#ff5555;--orange:#ffaa22;--green:#55dd55;--blue:#55aaff;--cyan:#00dddd;--magenta:#ff44ff}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;padding:20px;font-size:18px;line-height:1.5}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
@keyframes glow{{0%,100%{{box-shadow:0 0 8px var(--gold)}}50%{{box-shadow:0 0 20px var(--gold)}}}}
.header{{text-align:center;margin-bottom:25px}}
.header h1{{color:var(--gold);font-size:2.5em;letter-spacing:2px}}
.header .sub{{color:var(--dim);font-style:italic;font-size:1.1em;margin-top:5px}}
.header .meta{{color:var(--dim);font-size:0.95em;margin-top:5px}}
.nav{{text-align:right;margin-bottom:15px}}
.nav a{{color:var(--accent);text-decoration:none;margin-left:20px;font-size:1.1em;padding:5px 10px;border:1px solid var(--accent);border-radius:5px}}
.nav a:hover{{background:var(--accent);color:white}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px;margin-bottom:16px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px}}
.card h2{{color:var(--accent);font-size:1.2em;margin-bottom:12px;border-bottom:2px solid var(--border);padding-bottom:8px;letter-spacing:1px}}
.alert{{background:rgba(255,85,85,0.15);border:2px solid var(--red);border-radius:12px;padding:18px;margin-bottom:16px}}
.alert h2{{color:var(--red);border:none;margin:0 0 12px;font-size:1.3em}}
.stat-row{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}}
.stat{{flex:1;min-width:90px;text-align:center;padding:10px 6px;background:rgba(100,68,255,0.1);border-radius:8px;border:1px solid rgba(100,68,255,0.2)}}
.stat .n{{font-size:1.8em;font-weight:bold;color:var(--gold)}}
.stat .l{{font-size:0.8em;color:var(--dim);margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:1em}}
th{{text-align:left;color:var(--dim);padding:8px 10px;border-bottom:2px solid var(--border);font-size:0.9em;text-transform:uppercase;letter-spacing:1px}}
td{{padding:10px 10px;border-bottom:1px solid rgba(42,42,90,0.5)}}
tr:hover{{background:rgba(100,68,255,0.05)}}
.badge{{display:inline-block;padding:4px 10px;border-radius:5px;font-size:0.85em;font-weight:bold;white-space:nowrap;letter-spacing:0.5px}}
.timeline{{padding-left:25px}}
.t-node{{position:relative;padding:8px 0 8px 18px;border-left:3px solid var(--border);font-size:1em}}
.t-node.current{{border-left-color:var(--gold);border-left-width:4px}}
.t-node .dot{{position:absolute;left:-8px;top:12px;width:13px;height:13px;border-radius:50%}}
.t-node.historical .dot{{background:var(--green)}}
.t-node.current .dot{{background:var(--gold);box-shadow:0 0 12px var(--gold);animation:glow 2s infinite}}
.t-node.predicted .dot{{background:var(--border);border:3px solid var(--dim)}}
.t-meta{{color:var(--dim);font-size:0.9em}}
.fullwidth{{grid-column:1/-1}}
.section-title{{font-size:1.4em;color:var(--gold);border-bottom:3px double var(--gold);padding-bottom:8px;margin:25px 0 15px;letter-spacing:2px;text-transform:uppercase}}
.manchette{{background:linear-gradient(135deg,rgba(255,68,68,0.2),rgba(255,136,0,0.1));border:2px solid var(--red);border-radius:14px;padding:25px;margin-bottom:20px;text-align:center}}
.manchette h2{{font-size:2.2em;color:var(--red);margin-bottom:8px;line-height:1.2}}
.manchette .lead{{font-size:1.2em;color:var(--text);margin-top:10px}}
.manchette .kicker{{font-size:0.9em;color:var(--gold);text-transform:uppercase;letter-spacing:3px;margin-bottom:8px}}
.ticker{{display:flex;gap:15px;overflow-x:auto;padding:12px 0;margin-bottom:20px;border-top:2px solid var(--gold);border-bottom:2px solid var(--gold)}}
.ticker-item{{flex:0 0 auto;padding:8px 15px;background:var(--card);border-radius:8px;border:1px solid var(--border);white-space:nowrap;font-size:1em}}
.ticker-item .val{{font-weight:bold;color:var(--gold);font-size:1.1em}}
.ticker-item .lbl{{color:var(--dim);font-size:0.85em;margin-left:5px}}
.optic-row{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:15px;margin-bottom:20px}}
.optic{{text-align:center;padding:20px;border-radius:12px;border:2px solid var(--border)}}
.optic h3{{font-size:1.3em;margin-bottom:10px;letter-spacing:1px}}
.optic .big-num{{font-size:2.5em;font-weight:bold;color:var(--gold)}}
.optic .desc{{font-size:0.9em;color:var(--dim);margin-top:5px}}
.dark-matter-box{{background:linear-gradient(135deg,rgba(255,136,0,0.1),rgba(255,0,255,0.08));border:2px solid var(--orange);border-radius:12px;padding:20px;margin-bottom:20px}}
.dark-matter-box h2{{color:var(--orange);font-size:1.3em;margin-bottom:12px}}
.distortion-pair{{display:grid;grid-template-columns:1fr 50px 1fr;gap:10px;margin:12px 0;padding:15px;background:rgba(255,0,255,0.06);border-radius:10px;border:1px solid rgba(255,0,255,0.2);font-size:1em}}
.distortion-pair .vs{{text-align:center;color:var(--magenta);font-size:1.8em;align-self:center}}
.deadline-row{{display:flex;align-items:center;gap:15px;padding:10px 0;border-bottom:1px solid rgba(255,85,85,0.2);font-size:1.1em}}
.deadline-row .countdown{{min-width:70px;text-align:center}}
</style></head><body>

<div class="nav"><a href="/agent">Agent Trevize</a><a href="/settings">Settings</a><a href="/logout">Logout</a></div>
"""

    # ============================================================
    # MANCHETTE (headline like a newspaper front page)
    # ============================================================
    top_event = data["events"][0] if data["events"] else None
    top_pred = data["predictions"][0] if data["predictions"] else None
    top_deadline = data["deadlines"][0] if data["deadlines"] else None

    html += '<div style="text-align:center;padding:15px 0;border-bottom:4px double var(--gold);margin-bottom:5px">'
    html += '<div style="font-size:3em;color:var(--gold);font-weight:bold;letter-spacing:4px">PRIME RADIANT</div>'
    html += '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:5px">'
    html += f'<span style="color:var(--dim);font-size:1em">Departement Trevize</span>'
    html += f'<span style="color:var(--text);font-size:1.1em;font-weight:bold">{data["generated"]}</span>'
    html += f'<span style="color:var(--dim);font-size:1em">Edition #{ms["findings"]}</span>'
    html += '</div></div>'

    # MANCHETTE principale
    if top_deadline:
        d = top_deadline
        html += '<div class="manchette">'
        html += f'<div class="kicker">Alerte {d["severity"]}</div>'
        html += f'<h2>{d["name"]}</h2>'
        if d["days"] <= 2:
            html += f'<div class="lead" style="color:var(--red);font-size:1.5em;animation:pulse 1.5s infinite">{d["days"]} JOURS</div>'
        else:
            html += f'<div class="lead">{d["days"]} jours — {d["date"]}</div>'
        html += '</div>'

    # TICKER (bande defilante style bourse)
    html += '<div class="ticker">'
    for gi in data["golden"][:8]:
        r = gi["change_ratio"] or 0
        color = "var(--red)" if gi.get("phi_threshold_breached") else ("var(--orange)" if r > 1.3 else "var(--green)")
        arrow = "+" if r > 1 else ""
        html += f'<div class="ticker-item"><span class="val" style="color:{color}">{gi["current_value"]:.0f}</span><span class="lbl">{gi["name"][:20]}</span></div>'
    html += '</div>'

    # DEADLINES (style journal)
    html += '<div class="section-title">Echeances</div>'
    for d in data["deadlines"]:
        html += f'<div class="deadline-row"><div class="countdown">{deadline_badge(d)}</div><div><strong>{d["name"]}</strong></div><div style="color:var(--dim);margin-left:auto">{d["date"]}</div></div>'
    # Phi alerts inline
    for pa in data["phi_alerts"]:
        html += f'<div class="deadline-row"><div class="countdown"><span class="badge" style="background:var(--red);animation:pulse 1s infinite">φ</span></div><div><strong>{pa["name"]}</strong> — ratio {pa["change_ratio"]:.3f}</div><div style="color:var(--dim);margin-left:auto">{pa["variance_trend"]}</div></div>'

    # OPTIQUE: Microscope — Lentille — Telescope
    micro = data.get("microscope", {})
    lent = data.get("lentille", {})
    tele = data.get("telescope", {})
    html += '<div class="section-title">Optique Trevize</div>'
    html += '<div class="optic-row">'
    html += f'<div class="optic" style="border-color:var(--green)"><h3 style="color:var(--green)">MICROSCOPE</h3><div class="big-num">{micro.get("butterflies",0)}</div><div class="desc">Papillons detectes<br>Zoom IN — micro-events</div></div>'
    html += f'<div class="optic" style="border-color:var(--orange)"><h3 style="color:var(--orange)">LENTILLE</h3><div class="big-num">{lent.get("amplifiers",0)}<span style="font-size:0.4em;color:var(--dim)"> amp</span> {lent.get("dark_matter",0)}<span style="font-size:0.4em;color:var(--dim)"> dark</span></div><div class="desc">Distorsions bi-bloc<br>Ce qui est cache</div></div>'
    html += f'<div class="optic" style="border-color:var(--blue)"><h3 style="color:var(--blue)">TELESCOPE</h3><div class="big-num">{tele.get("fractals",0)}<span style="font-size:0.4em;color:var(--dim)"> frac</span> {tele.get("predictions",0)}<span style="font-size:0.4em;color:var(--dim)"> pred</span></div><div class="desc">Patterns globaux<br>Zoom OUT — Seldon</div></div>'
    html += '</div>'

    # MATIERE NOIRE
    dark = data.get("dark_matter", [])
    if dark:
        html += '<div class="dark-matter-box"><h2>MATIERE NOIRE — Ce que les deux blocs cachent</h2>'
        for dm in dark[:5]:
            sc = dm.get("seldon_score", 3)
            c_color = urgency_color(sc)
            html += f'<div style="padding:10px 0;border-bottom:1px solid rgba(255,136,0,0.2);font-size:1.05em"><span class="badge" style="background:{c_color}">{sc}/5</span> <strong>{dm["title"][:80]}</strong> <span style="color:var(--dim)">— {(dm.get("source") or "")[:40]}</span></div>'
        html += '</div>'

    # DISTORSIONS BI-BLOC
    distortions = data.get("distortions", [])
    if distortions:
        html += '<div class="section-title" style="color:var(--magenta);border-color:var(--magenta)">Lentille Gravitationnelle — Distorsions Bi-Bloc</div>'
        for d in distortions[:3]:
            w = d.get("west", {})
            b = d.get("brics", {})
            html += '<div class="distortion-pair">'
            html += f'<div><span class="badge" style="background:var(--blue)">WEST</span><br><strong>{w.get("title","")[:60]}</strong></div>'
            html += '<div class="vs">&#x21C4;</div>'
            html += f'<div><span class="badge" style="background:var(--red)">BRICS</span><br><strong>{b.get("title","")[:60]}</strong></div>'
            html += '</div>'
        html += '<div style="color:var(--dim);font-size:0.9em;font-style:italic;margin:10px 0 20px;text-align:center">La difference entre les deux recits = la carte de l invisible</div>'

    # STATS TICKER
    html += '<div class="section-title">Tableau de Bord</div>'
    html += '<div class="stat-row">'
    for val, label in [(ms["findings"],"Findings"),(ms["opportunities"],"Opportunites"),(ms["threats"],"Menaces"),
                        (gs["events"],"Events"),(gs["sources"],"Sources"),(gs["predictions"],"Predictions"),
                        (gs["fractal_patterns"],"Fractals"),(gs["butterflies"],"Papillons"),(gs["amplifiers"],"Amplificateurs")]:
        html += f'<div class="stat"><div class="n">{val}</div><div class="l">{label}</div></div>'
    html += '</div>'
    html += '<div style="color:var(--dim);font-size:0.75em;margin-top:5px">Zoom OUT — patterns globaux, Seldon-level</div></div>'
    html += '</div>'

    # MATIERE NOIRE (dark matter findings)
    dark = data.get("dark_matter", [])
    if dark:
        html += '<div class="card" style="margin-bottom:12px;border-left:3px solid var(--orange)"><h2 style="color:var(--orange)">MATIERE NOIRE — Ce que les deux blocs cachent</h2>'
        html += '<table><tr><th>Score</th><th>Decouverte</th><th>Source</th></tr>'
        for dm in dark[:5]:
            sc = dm.get("seldon_score", 3)
            c_color = urgency_color(sc)
            html += f'<tr><td><span class="badge" style="background:{c_color}">{sc}/5</span></td>'
            html += f'<td><strong>{dm["title"][:70]}</strong></td>'
            html += f'<td class="t-meta">{(dm.get("source") or "")[:30]}</td></tr>'
        html += '</table></div>'

    # DISTORSIONS BI-BLOC
    distortions = data.get("distortions", [])
    if distortions:
        html += '<div class="card" style="margin-bottom:12px;border-left:3px solid #ff00ff"><h2 style="color:#ff00ff">LENTILLE — Distorsions Bi-Bloc (WEST vs BRICS)</h2>'
        for i, d in enumerate(distortions[:3]):
            w = d.get("west", {})
            b = d.get("brics", {})
            html += f'<div style="display:grid;grid-template-columns:1fr 40px 1fr;gap:8px;margin:8px 0;padding:8px;background:rgba(255,0,255,0.05);border-radius:6px">'
            html += f'<div style="font-size:0.82em"><span class="badge" style="background:var(--blue)">WEST</span> {w.get("title","")[:50]}</div>'
            html += f'<div style="text-align:center;color:var(--orange);font-size:1.2em">&#x2194;</div>'
            html += f'<div style="font-size:0.82em"><span class="badge" style="background:var(--red)">BRICS</span> {b.get("title","")[:50]}</div>'
            html += '</div>'
        html += '<div style="color:var(--dim);font-size:0.75em;font-style:italic;margin-top:5px">La difference entre les deux recits = la carte de ce qui est invisible (Loi Lentille Gravitationnelle)</div>'
        html += '</div>'

    # MAIN GRID
    html += '<div class="section-title">Analyses</div>'
    html += '<div class="grid">'

    # Fractals
    html += '<div class="card"><h2>Patterns Fractals</h2><table><tr><th>Depth</th><th>Pattern</th><th>Urg.</th></tr>'
    for f in data["fractals"]:
        c = urgency_color(f["urgency"])
        html += f'<tr><td>{depth_bar(f["fractal_depth"])}</td><td><strong>{f["title"]}</strong></td><td><span class="badge" style="background:{c}">{f["urgency"]}/5</span></td></tr>'
    html += '</table></div>'

    # Predictions
    html += '<div class="card"><h2>Predictions Trevize</h2><table><tr><th>%</th><th>Prediction</th><th>Quand</th></tr>'
    for p in data["predictions"]:
        c = '#ff4444' if p["probability"]>=70 else '#ff8800' if p["probability"]>=60 else '#ffcc00'
        html += f'<tr><td><span class="badge" style="background:{c}">{p["probability"]}%</span></td><td>{p["title"][:65]}</td><td class="t-meta">{p["timeframe"]}</td></tr>'
    html += '</table></div>'

    # Butterflies
    html += '<div class="card"><h2>Effet Papillon</h2><table><tr><th>Status</th><th>Papillon</th><th>Mag</th><th>Fib</th></tr>'
    for b in data["butterflies"]:
        sc = {'hurricane':'#ff4444','cascading':'#ff8800','amplifying':'#ffcc00','detected':'#44aa44'}.get(b["status"],'#888')
        fib = f'{b["fibonacci_match"]:.0%}' if b["fibonacci_match"] else '-'
        html += f'<tr><td><span class="badge" style="background:{sc}">{b["status"][:6]}</span></td><td>{b["title"][:40]}</td><td>x{b["current_magnitude"]:.0f}</td><td>{fib}</td></tr>'
    html += '</table></div>'

    # Golden indicators
    html += '<div class="card"><h2>Indicateurs Dores (φ={:.3f})</h2><table><tr><th>At.</th><th>Indicateur</th><th>Ratio</th><th>Trend</th></tr>'.format(PHI)
    for gi in data["golden"]:
        r = gi["change_ratio"] or 0
        phi_html = '<span class="badge" style="background:var(--red)">φ!</span>' if gi["phi_threshold_breached"] else ('<span class="badge" style="background:var(--orange)">~φ</span>' if r > 1.3 else '')
        tc = {'critical':'var(--red)','increasing':'var(--orange)','stable':'var(--green)','chaotic':'#ff00ff'}.get(gi["variance_trend"],'var(--dim)')
        html += f'<tr><td><span class="badge" style="background:var(--blue)">{gi["atelier_code"]}</span></td><td>{gi["name"][:25]}</td><td>{r:.3f} {phi_html}</td><td style="color:{tc}">{gi["variance_trend"]}</td></tr>'
    html += '</table></div>'

    # Amplifiers
    html += '<div class="card"><h2>Amplificateurs</h2><table><tr><th>x</th><th>Nom</th><th>Type</th><th>Ctrl</th></tr>'
    for a in data["amplifiers"]:
        html += f'<tr><td><strong>x{a["amplification_factor"]:.0f}</strong></td><td>{a["name"][:28]}</td><td class="t-meta">{a["amplifier_type"][:12]}</td><td>{a["controller"] or "-"}</td></tr>'
    html += '</table></div>'

    # Opportunities
    html += '<div class="card"><h2>Opportunites</h2><table><tr><th>Urg</th><th>Opportunite</th></tr>'
    for o in data["opportunities"]:
        c = urgency_color(o["urgency"])
        html += f'<tr><td><span class="badge" style="background:{c}">{o["urgency"]}/5</span></td><td>{o["title"][:60]}</td></tr>'
    html += '</table></div>'

    # Threats
    html += '<div class="card"><h2>Menaces</h2><table><tr><th>Sev</th><th>Menace</th></tr>'
    for t in data["threats"]:
        c = urgency_color(t["severity"])
        html += f'<tr><td><span class="badge" style="background:{c}">{t["severity"]}/5</span></td><td>{t["title"][:60]}</td></tr>'
    html += '</table></div>'

    # Events
    html += '<div class="card"><h2>Evenements GEO</h2><table><tr><th>Imp</th><th>Evenement</th><th>Status</th></tr>'
    for e in data["events"]:
        c = urgency_color(e["impact_score"])
        sc = {'escalating':'var(--red)','active':'var(--orange)','resolved':'var(--green)'}.get(e["status"],'var(--dim)')
        html += f'<tr><td><span class="badge" style="background:{c}">{e["impact_score"]}/5</span></td><td>{e["title"][:50]}</td><td style="color:{sc}">{e["status"]}</td></tr>'
    html += '</table></div>'

    html += '</div>'  # end grid

    # TEMPORAL CHAINS
    for ch in data["chains"]:
        nodes = data["chain_nodes"].get(ch["id"], [])
        html += f'<div class="card" style="margin-bottom:12px"><h2>Timeline: {ch["title"][:60]}</h2>'
        html += f'<div class="t-meta">Echelle: {ch["scale"]}</div><div class="timeline">'
        atelier_colors = {'NRJ':'#ff6600','MON':'#ffd700','TECH':'#4488ff','TERRAIN':'#44cc44','CHAIN':'#cc44cc'}
        for n in nodes:
            st = n["status"]
            date_d = (n["date_actual"] or n["date_estimated"] or "?")[:10]
            icon = {'historical':'✓','current':'★','predicted':'?'}.get(st,'')
            ac = atelier_colors.get(n["atelier_code"],'#888')
            html += f'<div class="t-node {st}"><div class="dot"></div>'
            html += f'<div class="t-meta">T{n["t_position"]:+d} <span style="color:{ac}">{n["atelier_code"]}</span> {date_d} {icon}</div>'
            html += f'<div>{n["title"]}</div></div>'
        html += '</div></div>'

    # FOOTER
    html += f"""
<div style="text-align:center;color:var(--dim);margin-top:20px;padding:12px;border-top:1px solid var(--border);font-size:0.8em">
<div style="color:var(--gold);font-style:italic">"Les patterns emergent AVANT que la realite les confirme."</div>
<div>Departement Trevize — R2D2 | Warehouse: {ms['findings']} findings + {gs['events']} events GEO</div>
</div></body></html>"""

    return html

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print(f"\n  Prime Radiant - Departement Trevize")
    print(f"  http://localhost:{config['port']}")
    print(f"  Login: {config['username']} / (voir config.json)")
    print(f"  Ctrl+C pour arreter\n")
    uvicorn.run(app, host=config["host"], port=config["port"], log_level="warning")
