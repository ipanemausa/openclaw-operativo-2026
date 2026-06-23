from flask import Flask, jsonify, request
import os, urllib.request, json

app = Flask(__name__)

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="10">
<title>LAMAUTONOMIA — Control</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0a; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 24px; }
  h1 { color: #00ff88; font-size: 1.4rem; margin-bottom: 4px; }
  .sub { color: #555; font-size: 0.8rem; margin-bottom: 24px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 16px; }
  .card h2 { color: #00aaff; font-size: 0.85rem; margin-bottom: 12px; letter-spacing: 2px; }
  .item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #1a1a1a; font-size: 0.82rem; }
  .item:last-child { border-bottom: none; }
  .ok { color: #00ff88; }
  .fail { color: #ff4444; }
  .pending { color: #ffaa00; }
  .en_cola { color: #00aaff; }
  .completada { color: #555; text-decoration: line-through; }
  .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
  .dot-ok { background: #00ff88; }
  .dot-fail { background: #ff4444; }
  .dot-pending { background: #ffaa00; }
  .tag { font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; }
  .tag-ok { background: #00ff8820; color: #00ff88; border: 1px solid #00ff8840; }
  .tag-pending { background: #ffaa0020; color: #ffaa00; border: 1px solid #ffaa0040; }
  .tag-completada { background: #33333320; color: #555; border: 1px solid #33333340; }
  .tag-en_cola { background: #00aaff20; color: #00aaff; border: 1px solid #00aaff40; }
  .version { color: #333; font-size: 0.7rem; margin-top: 24px; }
</style>
</head>
<body>
<h1>⬡ LAMAUTONOMIA</h1>
<div class="sub">Dashboard — auto-refresh 10s</div>
<div class="grid" id="grid">CARGANDO...</div>
<div class="version">openclaw-cloud-2026 · {version}</div>
<script>
async function load() {
  const [stack, tareas] = await Promise.all([
    fetch('/api/stack').then(r=>r.json()),
    fetch('/api/tareas').then(r=>r.json())
  ]);
  const tagClass = s => s === 'completada' ? 'tag-completada' : s === 'pendiente' ? 'tag-pending' : s === 'en_cola' ? 'tag-en_cola' : 'tag-ok';
  const dotClass = s => s.includes('Up') ? 'dot-ok' : 'dot-fail';

  document.getElementById('grid').innerHTML = `
    <div class="card">
      <h2>CONTENEDORES</h2>
      ${stack.containers.map(c => `
        <div class="item">
          <span><span class="dot ${dotClass(c.status)}"></span>${c.name}</span>
          <span class="${c.status.includes('Up') ? 'ok' : 'fail'}">${c.status.split(' ').slice(0,2).join(' ')}</span>
        </div>`).join('')}
    </div>
    <div class="card">
      <h2>DAG — TAREAS</h2>
      ${Object.entries(tareas.tareas).map(([k,v]) => `
        <div class="item">
          <span class="${v.estado}">${k.replace(/_/g,' ')}</span>
          <span class="tag ${tagClass(v.estado)}">${v.estado}</span>
        </div>`).join('')}
    </div>`;
}
load();
</script>
</body>
</html>""".replace("{version}", os.getenv("VERSION", "2026.5.27"))

ORCHESTRATOR = "http://claw-orchestrator:8090"

def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            return json.loads(r.read())
    except:
        return {}

@app.route("/")
def dashboard():
    return DASHBOARD_HTML

@app.route("/healthz")
def health():
    return jsonify({"status": "healthy", "service": "openclaw-app", "version": os.getenv("VERSION", "2026.5.27")}), 200

@app.route("/api/status")
def status():
    return jsonify({"status": "running", "service": "openclaw-app"}), 200

@app.route("/api/stack")
def stack():
    data = fetch_json(f"{ORCHESTRATOR}/stack")
    return jsonify(data)

@app.route("/api/tareas")
def tareas():
    data = fetch_json(f"{ORCHESTRATOR}/api/tareas")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
