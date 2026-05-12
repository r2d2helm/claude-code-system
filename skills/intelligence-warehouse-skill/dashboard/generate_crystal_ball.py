"""
Boule de Cristal — Dashboard Mike
Génère un fichier HTML statique depuis les deux warehouses
Ouvrir dans n'importe quel navigateur
"""
import sqlite3, json, datetime, os, math

PHI = (1 + math.sqrt(5)) / 2
NOW = datetime.datetime.now()
OUTPUT = r'C:\Users\r2d2\Documents\Knowledge\_Daily\crystal-ball.html'

# Connect to both DBs
geo = sqlite3.connect(r'C:\Users\r2d2\.claude\skills\intelligence-warehouse-skill\data\warehouse-geo.db')
geo.row_factory = sqlite3.Row
main = sqlite3.connect(r'C:\Users\r2d2\.claude\skills\intelligence-warehouse-skill\data\warehouse.db')
main.row_factory = sqlite3.Row

g = geo.cursor()
m = main.cursor()

# ============================================================
# DATA COLLECTION
# ============================================================

# Fractal patterns
fractals = g.execute("SELECT * FROM fractal_patterns ORDER BY fractal_depth DESC, urgency DESC").fetchall()

# Predictions
predictions = g.execute("SELECT * FROM predictions WHERE status='pending' ORDER BY probability DESC").fetchall()

# Temporal chains + nodes
chains = g.execute("SELECT * FROM temporal_chains WHERE status='active'").fetchall()
chain_nodes = {}
for ch in chains:
    nodes = g.execute("SELECT * FROM temporal_nodes WHERE chain_id=? ORDER BY t_position", (ch['id'],)).fetchall()
    chain_nodes[ch['id']] = nodes

# Golden indicators with phi breach
phi_breached = g.execute("SELECT * FROM golden_indicators WHERE phi_threshold_breached=1 ORDER BY change_ratio DESC").fetchall()
phi_approaching = g.execute("SELECT * FROM golden_indicators WHERE phi_threshold_breached=0 AND change_ratio > 1.3 ORDER BY change_ratio DESC").fetchall()
all_golden = g.execute("SELECT * FROM golden_indicators ORDER BY atelier_code").fetchall()

# Butterflies
butterflies = g.execute("SELECT * FROM butterflies WHERE status != 'dead' ORDER BY current_magnitude DESC").fetchall()

# Amplifiers top
amplifiers = g.execute("SELECT * FROM amplifiers ORDER BY amplification_factor DESC LIMIT 8").fetchall()

# Events
events = g.execute("SELECT * FROM events ORDER BY impact_score DESC").fetchall()

# Opportunities (main warehouse)
opportunities = m.execute("SELECT * FROM opportunities WHERE status='detected' ORDER BY urgency DESC LIMIT 8").fetchall()

# Threats (main warehouse)
threats = m.execute("SELECT * FROM threats WHERE status='active' ORDER BY severity DESC").fetchall()

# Stats
stats = {
    'findings': m.execute("SELECT COUNT(*) FROM findings").fetchone()[0],
    'opportunities': m.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0],
    'threats': m.execute("SELECT COUNT(*) FROM threats").fetchone()[0],
    'geo_events': g.execute("SELECT COUNT(*) FROM events").fetchone()[0],
    'geo_sources': g.execute("SELECT COUNT(*) FROM sources").fetchone()[0],
    'geo_analyses': g.execute("SELECT COUNT(*) FROM analyses").fetchone()[0],
    'geo_predictions': g.execute("SELECT COUNT(*) FROM predictions").fetchone()[0],
    'geo_fractals': g.execute("SELECT COUNT(*) FROM fractal_patterns").fetchone()[0],
    'geo_butterflies': g.execute("SELECT COUNT(*) FROM butterflies").fetchone()[0],
    'geo_amplifiers': g.execute("SELECT COUNT(*) FROM amplifiers").fetchone()[0],
    'geo_golden': g.execute("SELECT COUNT(*) FROM golden_indicators").fetchone()[0],
    'geo_nodes': g.execute("SELECT COUNT(*) FROM temporal_nodes").fetchone()[0],
}

# ============================================================
# HTML GENERATION
# ============================================================

def urgency_color(u):
    if u >= 5: return '#ff4444'
    if u >= 4: return '#ff8800'
    if u >= 3: return '#ffcc00'
    return '#44aa44'

def depth_bar(d, mx=5):
    filled = '█' * d
    empty = '░' * (mx - d)
    return filled + empty

def phi_badge(ratio):
    if ratio and ratio > PHI:
        return f'<span class="badge phi-breach">φ {ratio:.3f}</span>'
    elif ratio and ratio > 1.3:
        return f'<span class="badge phi-near">~φ {ratio:.3f}</span>'
    return ''

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Boule de Cristal — Departement Trevize</title>
<style>
:root {{
    --bg: #0a0a1a;
    --card: #12122a;
    --border: #2a2a4a;
    --text: #e0e0f0;
    --dim: #8888aa;
    --accent: #6644ff;
    --gold: #ffd700;
    --red: #ff4444;
    --orange: #ff8800;
    --green: #44cc44;
    --blue: #4488ff;
    --cyan: #00cccc;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; padding: 20px; }}
h1 {{ text-align: center; color: var(--gold); font-size: 2em; margin-bottom: 5px; }}
.subtitle {{ text-align: center; color: var(--dim); margin-bottom: 20px; font-style: italic; }}
.timestamp {{ text-align: center; color: var(--dim); font-size: 0.85em; margin-bottom: 25px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 15px; margin-bottom: 20px; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 15px; }}
.card h2 {{ color: var(--accent); font-size: 1.1em; margin-bottom: 10px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
.card h3 {{ color: var(--cyan); font-size: 0.95em; margin: 10px 0 5px; }}
.stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }}
.stat {{ text-align: center; padding: 8px; background: rgba(100,68,255,0.1); border-radius: 6px; }}
.stat .num {{ font-size: 1.5em; font-weight: bold; color: var(--gold); }}
.stat .label {{ font-size: 0.75em; color: var(--dim); }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.85em; }}
th {{ text-align: left; color: var(--dim); padding: 4px 6px; border-bottom: 1px solid var(--border); }}
td {{ padding: 4px 6px; border-bottom: 1px solid rgba(42,42,74,0.5); }}
.badge {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; }}
.phi-breach {{ background: var(--red); color: white; }}
.phi-near {{ background: var(--orange); color: white; }}
.badge-green {{ background: var(--green); color: black; }}
.badge-red {{ background: var(--red); color: white; }}
.badge-orange {{ background: var(--orange); color: white; }}
.badge-blue {{ background: var(--blue); color: white; }}
.badge-gold {{ background: var(--gold); color: black; }}
.depth {{ font-family: monospace; letter-spacing: 2px; }}
.timeline {{ position: relative; padding-left: 20px; }}
.t-node {{ position: relative; padding: 6px 0 6px 15px; border-left: 2px solid var(--border); }}
.t-node.current {{ border-left-color: var(--gold); }}
.t-node .t-marker {{ position: absolute; left: -7px; top: 8px; width: 12px; height: 12px; border-radius: 50%; }}
.t-node.historical .t-marker {{ background: var(--green); }}
.t-node.current .t-marker {{ background: var(--gold); box-shadow: 0 0 10px var(--gold); }}
.t-node.predicted .t-marker {{ background: var(--border); border: 2px solid var(--dim); }}
.t-label {{ font-size: 0.75em; color: var(--dim); }}
.t-title {{ font-size: 0.85em; }}
.progress-bar {{ height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; margin: 3px 0; }}
.progress-fill {{ height: 100%; border-radius: 3px; }}
.alert-box {{ background: rgba(255,68,68,0.15); border: 1px solid var(--red); border-radius: 8px; padding: 12px; margin-bottom: 15px; }}
.alert-box h2 {{ color: var(--red); }}
.fullwidth {{ grid-column: 1 / -1; }}
</style>
</head>
<body>

<h1>&#x1F52E; Boule de Cristal</h1>
<div class="subtitle">Departement Trevize — Systeme nerveux R2D2</div>
<div class="timestamp">Genere le {NOW.strftime('%d/%m/%Y a %H:%M')} | φ = {PHI:.6f}</div>
"""

# ALERTS SECTION
html += '<div class="alert-box"><h2>ALERTES IMMEDIATES</h2><table>'
# NIS2 deadline
html += '<tr><td><span class="badge badge-red">14 JOURS</span></td><td><strong>NIS2 Belgique deadline 18 avril 2026</strong> — 2.410 entites, resp. personnelle directeurs</td></tr>'
# Ban LNG
html += '<tr><td><span class="badge badge-orange">21 JOURS</span></td><td><strong>Ban LNG russe EU 25 avril</strong> — stockage EU a 28%, double coupure</td></tr>'
# Phi breaches
for gi in phi_breached:
    html += f'<tr><td><span class="badge phi-breach">φ FRANCHI</span></td><td><strong>{gi["name"]}</strong> — ratio {gi["change_ratio"]:.3f} (seuil φ={PHI:.3f}), trend: {gi["variance_trend"]}</td></tr>'
html += '</table></div>'

# STATS ROW
html += '<div class="grid"><div class="card fullwidth"><div class="stat-grid">'
for key, label in [('findings','Findings'),('opportunities','Opportunites'),('threats','Menaces'),
                     ('geo_events','Events GEO'),('geo_sources','Sources'),('geo_predictions','Predictions'),
                     ('geo_fractals','Fractals'),('geo_butterflies','Papillons'),('geo_amplifiers','Amplificateurs'),
                     ('geo_golden','Indicateurs φ'),('geo_nodes','Noeuds T'),('geo_analyses','Analyses')]:
    html += f'<div class="stat"><div class="num">{stats[key]}</div><div class="label">{label}</div></div>'
html += '</div></div></div>'

# MAIN GRID
html += '<div class="grid">'

# FRACTAL PATTERNS
html += '<div class="card"><h2>Patterns Fractals</h2><table>'
html += '<tr><th>Profondeur</th><th>Pattern</th><th>Urgence</th></tr>'
for f in fractals:
    color = urgency_color(f['urgency'])
    html += f'<tr><td class="depth">{depth_bar(f["fractal_depth"])}</td>'
    html += f'<td><strong>{f["title"]}</strong></td>'
    html += f'<td><span class="badge" style="background:{color}">{f["urgency"]}/5</span></td></tr>'
html += '</table></div>'

# PREDICTIONS
html += '<div class="card"><h2>Predictions Trevize</h2><table>'
html += '<tr><th>Prob.</th><th>Prediction</th><th>Horizon</th></tr>'
for p in predictions:
    color = '#ff4444' if p['probability'] >= 70 else '#ff8800' if p['probability'] >= 60 else '#ffcc00'
    html += f'<tr><td><span class="badge" style="background:{color}">{p["probability"]}%</span></td>'
    html += f'<td>{p["title"][:70]}</td>'
    html += f'<td style="color:var(--dim)">{p["timeframe"]}</td></tr>'
html += '</table></div>'

# BUTTERFLIES
html += '<div class="card"><h2>Effet Papillon</h2><table>'
html += '<tr><th>Status</th><th>Papillon</th><th>Mag.</th><th>Fib</th></tr>'
for b in butterflies:
    status_color = {'hurricane':'#ff4444','cascading':'#ff8800','amplifying':'#ffcc00','detected':'#44aa44'}.get(b['status'],'#888')
    fib = f'{b["fibonacci_match"]:.0%}' if b['fibonacci_match'] else '-'
    html += f'<tr><td><span class="badge" style="background:{status_color}">{b["status"]}</span></td>'
    html += f'<td>{b["title"][:45]}</td>'
    html += f'<td>x{b["current_magnitude"]:.0f}</td>'
    html += f'<td>{fib}</td></tr>'
html += '</table></div>'

# GOLDEN INDICATORS
html += '<div class="card"><h2>Indicateurs Dores (φ = {:.3f})</h2><table>'.format(PHI)
html += '<tr><th>Atelier</th><th>Indicateur</th><th>Ratio</th><th>Fib</th><th>Trend</th></tr>'
for gi in all_golden:
    ratio = gi['change_ratio'] or 0
    phi_badge_html = ''
    if gi['phi_threshold_breached']:
        phi_badge_html = '<span class="badge phi-breach">φ!</span>'
    elif ratio > 1.3:
        phi_badge_html = '<span class="badge phi-near">~φ</span>'
    trend_color = {'critical':'#ff4444','increasing':'#ff8800','stable':'#44aa44','chaotic':'#ff00ff'}.get(gi['variance_trend'],'#888')
    html += f'<tr><td><span class="badge badge-blue">{gi["atelier_code"]}</span></td>'
    html += f'<td>{gi["name"][:30]}</td>'
    html += f'<td>{ratio:.3f} {phi_badge_html}</td>'
    html += f'<td>{gi["fibonacci_level"]}</td>'
    html += f'<td style="color:{trend_color}">{gi["variance_trend"]}</td></tr>'
html += '</table></div>'

# AMPLIFIERS
html += '<div class="card"><h2>Top Amplificateurs</h2><table>'
html += '<tr><th>x</th><th>Nom</th><th>Type</th><th>Ctrl</th></tr>'
for a in amplifiers:
    html += f'<tr><td><strong>x{a["amplification_factor"]:.0f}</strong></td>'
    html += f'<td>{a["name"][:30]}</td>'
    html += f'<td style="color:var(--dim)">{a["amplifier_type"]}</td>'
    html += f'<td>{a["controller"] or "-"}</td></tr>'
html += '</table></div>'

# OPPORTUNITIES
html += '<div class="card"><h2>Top Opportunites</h2><table>'
html += '<tr><th>Urg.</th><th>Opportunite</th></tr>'
for o in opportunities:
    color = urgency_color(o['urgency'])
    html += f'<tr><td><span class="badge" style="background:{color}">{o["urgency"]}/5</span></td>'
    html += f'<td>{o["title"][:65]}</td></tr>'
html += '</table></div>'

# THREATS
html += '<div class="card"><h2>Menaces Actives</h2><table>'
html += '<tr><th>Sev.</th><th>Menace</th></tr>'
for t in threats:
    color = urgency_color(t['severity'])
    html += f'<tr><td><span class="badge" style="background:{color}">{t["severity"]}/5</span></td>'
    html += f'<td>{t["title"][:65]}</td></tr>'
html += '</table></div>'

# EVENTS
html += '<div class="card"><h2>Evenements Geopolitiques</h2><table>'
html += '<tr><th>Impact</th><th>Evenement</th><th>Status</th></tr>'
for e in events:
    color = urgency_color(e['impact_score'])
    status_color = {'escalating':'#ff4444','active':'#ff8800','resolved':'#44aa44'}.get(e['status'],'#888')
    html += f'<tr><td><span class="badge" style="background:{color}">{e["impact_score"]}/5</span></td>'
    html += f'<td>{e["title"][:55]}</td>'
    html += f'<td style="color:{status_color}">{e["status"]}</td></tr>'
html += '</table></div>'

html += '</div>'  # end main grid

# TEMPORAL CHAINS (full width)
for ch in chains:
    nodes = chain_nodes[ch['id']]
    html += f'<div class="card" style="margin-bottom:15px"><h2>Timeline: {ch["title"]}</h2>'
    html += f'<div style="color:var(--dim);font-size:0.8em;margin-bottom:10px">Echelle: {ch["scale"]} | Status: {ch["status"]}</div>'
    html += '<div class="timeline">'
    for n in nodes:
        status_class = n['status']
        date_display = n['date_actual'] or n['date_estimated'] or '?'
        if len(date_display) > 10:
            date_display = date_display[:10]
        status_icon = {'historical':'✓','current':'★','predicted':'?'}[n['status']]
        atelier_colors = {'NRJ':'#ff6600','MON':'#ffd700','TECH':'#4488ff','TERRAIN':'#44cc44','CHAIN':'#cc44cc'}
        ac = atelier_colors.get(n['atelier_code'], '#888')
        html += f'<div class="t-node {status_class}">'
        html += f'<div class="t-marker"></div>'
        html += f'<div class="t-label">T{n["t_position"]:+d} | <span style="color:{ac}">{n["atelier_code"]}</span> | {date_display} {status_icon}</div>'
        html += f'<div class="t-title">{n["title"]}</div>'
        html += '</div>'
    html += '</div></div>'

# FOOTER
html += f"""
<div style="text-align:center;color:var(--dim);margin-top:30px;padding:15px;border-top:1px solid var(--border)">
    <div style="color:var(--gold);font-style:italic;margin-bottom:5px">"Les patterns emergent AVANT que la realite les confirme."</div>
    <div>Departement Trevize — R2D2 | φ = {PHI:.10f} | δ = 4.6692016091</div>
    <div style="font-size:0.8em;margin-top:5px">Genere depuis warehouse.db ({stats['findings']} findings) + warehouse-geo.db ({stats['geo_events']} events, {stats['geo_sources']} sources)</div>
</div>
</body></html>"""

# Write
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

geo.close()
main.close()
print(f"Dashboard genere: {OUTPUT}")
print(f"Ouvrir dans le navigateur: file:///{OUTPUT.replace(os.sep, '/')}")
