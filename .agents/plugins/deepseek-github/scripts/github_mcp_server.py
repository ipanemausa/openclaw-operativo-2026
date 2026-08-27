"""
=============================================================================
OPENCLAW 2026 — GITHUB MCP SERVER (API REST nativa, cero dependencias extra)
=============================================================================
MCP Server para Antigravity IDE que provee acceso a GitHub vía API REST.

TOOLS DISPONIBLES:
  github_repo_info      → Info de cualquier repo (stars, forks, descripción)
  github_list_commits   → Últimos commits de un repo
  github_list_branches  → Ramas de un repo
  github_read_file      → Leer contenido de un archivo en GitHub
  github_list_issues    → Issues abiertos/cerrados de un repo
  github_create_issue   → Crear un nuevo issue
  github_search_code    → Buscar código en GitHub
  github_repo_status    → Estado de CI/CD y último push del repo propio
  git_local_status      → Estado del repo local (git status)
  git_local_commit_push → Commit + push del repo local con mensaje (GUARDRAIL)

SEGURIDAD:
  - git_local_commit_push requiere confirmacion=True explícito para ejecutar
  - Nunca expone el token en output
  - Logs de todas las operaciones de escritura

Key requerida: GITHUB_TOKEN en .openclaw-master.env
Repo propio:   ipanemausa/openclaw-operativo-2026
=============================================================================
"""

import sys
import os
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ─── AUTO-CARGA del master env (fuente única de verdad) ──────────────────────
_MASTER_ENV = Path(r"C:\Users\ipane\.openclaw-master.env")
if _MASTER_ENV.exists():
    for _line in _MASTER_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in _line and not _line.strip().startswith("#"):
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            _v = _v.strip().strip('"').strip("'")
            if _v and not _v.startswith("tu_"):
                os.environ.setdefault(_k, _v)  # no sobreescribe si ya existe

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OpenClaw GitHub MCP — Trazabilidad + Git Local")

# ─── CONFIG ──────────────────────────────────────────────────────────────────
GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN", "")
GITHUB_API     = "https://api.github.com"
WORKSPACE_ROOT = Path(r"C:\Users\ipane\openclaw-operativo-2026")
DEFAULT_REPO   = "ipanemausa/openclaw-operativo-2026"

# ─── HELPER HTTP → GitHub API ────────────────────────────────────────────────
def _gh_get(path: str, params: dict = None) -> dict:
    """GET a GitHub API endpoint. path = '/repos/owner/repo/...'"""
    url = f"{GITHUB_API}{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{qs}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {err[:300]}"}
    except Exception as e:
        return {"error": str(e)}

def _gh_post(path: str, payload: dict) -> dict:
    """POST a GitHub API endpoint."""
    url = f"{GITHUB_API}{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {err[:300]}"}
    except Exception as e:
        return {"error": str(e)}

def _no_token_msg():
    return "⚠️ GITHUB_TOKEN no configurado. Agregar en C:\\Users\\ipane\\.openclaw-master.env"

# ─────────────────────────────────────────────────────────────────────────────
# TOOLS: INFORMACIÓN DE REPOS
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def github_repo_info(repo: str = DEFAULT_REPO) -> str:
    """Info completa de un repo GitHub: descripción, stars, forks, lenguaje, última actualización.
    Ejemplo: repo='ipanemausa/openclaw-operativo-2026'
    """
    data = _gh_get(f"/repos/{repo}")
    if "error" in data:
        return f"Error: {data['error']}"
    return (
        f"📦 {data.get('full_name')}\n"
        f"   Descripción: {data.get('description', 'N/A')}\n"
        f"   Stars: ⭐ {data.get('stargazers_count', 0)} | Forks: 🍴 {data.get('forks_count', 0)}\n"
        f"   Lenguaje: {data.get('language', 'N/A')}\n"
        f"   Rama default: {data.get('default_branch', 'main')}\n"
        f"   Privado: {'🔒 Sí' if data.get('private') else '🌐 No'}\n"
        f"   Último push: {data.get('pushed_at', 'N/A')}\n"
        f"   URL: {data.get('html_url')}"
    )

@mcp.tool()
def github_list_commits(repo: str = DEFAULT_REPO, branch: str = "main", limit: int = 10) -> str:
    """Lista los últimos commits de un repo GitHub.
    Proporciona trazabilidad completa de cambios.
    """
    data = _gh_get(f"/repos/{repo}/commits", {"sha": branch, "per_page": str(limit)})
    if isinstance(data, dict) and "error" in data:
        return f"Error: {data['error']}"
    if not isinstance(data, list):
        return f"Respuesta inesperada: {str(data)[:200]}"
    lines = [f"📋 Últimos {limit} commits en {repo}/{branch}:\n"]
    for c in data:
        sha = c.get("sha", "")[:7]
        msg = c.get("commit", {}).get("message", "").split("\n")[0][:80]
        author = c.get("commit", {}).get("author", {}).get("name", "?")
        date = c.get("commit", {}).get("author", {}).get("date", "")[:10]
        lines.append(f"  [{sha}] {date} — {author}: {msg}")
    return "\n".join(lines)

@mcp.tool()
def github_list_branches(repo: str = DEFAULT_REPO) -> str:
    """Lista todas las ramas de un repo GitHub."""
    data = _gh_get(f"/repos/{repo}/branches")
    if isinstance(data, dict) and "error" in data:
        return f"Error: {data['error']}"
    if not isinstance(data, list):
        return f"Respuesta inesperada: {str(data)[:200]}"
    lines = [f"🌿 Ramas en {repo}:"]
    for b in data:
        protected = " 🔒" if b.get("protected") else ""
        lines.append(f"  ├─ {b.get('name')}{protected}")
    return "\n".join(lines)

@mcp.tool()
def github_read_file(repo: str = DEFAULT_REPO, file_path: str = "README.md", branch: str = "main") -> str:
    """Lee el contenido de un archivo en un repo GitHub.
    Útil para ver SKILL.md, configs, scripts directamente desde GitHub.
    """
    import base64
    data = _gh_get(f"/repos/{repo}/contents/{file_path}", {"ref": branch})
    if isinstance(data, dict) and "error" in data:
        return f"Error: {data['error']}"
    content_b64 = data.get("content", "")
    if not content_b64:
        return f"Archivo '{file_path}' no encontrado o vacío."
    try:
        decoded = base64.b64decode(content_b64).decode("utf-8", errors="replace")
        # Limitar a 3000 chars para no saturar el contexto
        if len(decoded) > 3000:
            decoded = decoded[:3000] + "\n\n... [TRUNCADO — archivo más largo]"
        return f"📄 {repo}/{file_path} ({branch}):\n\n{decoded}"
    except Exception as e:
        return f"Error decodificando: {e}"

@mcp.tool()
def github_list_issues(repo: str = DEFAULT_REPO, state: str = "open", limit: int = 10) -> str:
    """Lista issues de un repo GitHub. state = 'open' | 'closed' | 'all'"""
    data = _gh_get(f"/repos/{repo}/issues", {"state": state, "per_page": str(limit)})
    if isinstance(data, dict) and "error" in data:
        return f"Error: {data['error']}"
    if not isinstance(data, list):
        return f"Sin issues o respuesta inesperada."
    lines = [f"🐛 Issues ({state}) en {repo}:"]
    for issue in data:
        if issue.get("pull_request"):
            continue  # skip PRs
        num = issue.get("number")
        title = issue.get("title", "")[:70]
        labels = ", ".join(l["name"] for l in issue.get("labels", []))
        lines.append(f"  #{num} — {title}" + (f" [{labels}]" if labels else ""))
    return "\n".join(lines) if len(lines) > 1 else f"No hay issues {state} en {repo}."

@mcp.tool()
def github_create_issue(title: str, body: str, repo: str = DEFAULT_REPO, labels: str = "") -> str:
    """Crea un nuevo issue en un repo GitHub.
    labels: string separado por comas. Ej: 'bug,enhancement'
    """
    if not GITHUB_TOKEN:
        return _no_token_msg()
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = [l.strip() for l in labels.split(",")]
    data = _gh_post(f"/repos/{repo}/issues", payload)
    if "error" in data:
        return f"Error creando issue: {data['error']}"
    return f"✅ Issue creado: #{data.get('number')} — {data.get('title')}\n   URL: {data.get('html_url')}"

@mcp.tool()
def github_search_code(query: str, repo: str = DEFAULT_REPO) -> str:
    """Busca código en GitHub. query = término de búsqueda."""
    full_query = f"{query}+repo:{repo}" if repo else query
    data = _gh_get("/search/code", {"q": full_query, "per_page": "8"})
    if "error" in data:
        return f"Error: {data['error']}"
    items = data.get("items", [])
    if not items:
        return f"No se encontraron resultados para '{query}' en {repo}."
    lines = [f"🔍 Resultados para '{query}' en {repo}:"]
    for item in items:
        name = item.get("name")
        path = item.get("path")
        url = item.get("html_url")
        lines.append(f"  📄 {path} → {url}")
    return "\n".join(lines)

@mcp.tool()
def github_repo_status(repo: str = DEFAULT_REPO) -> str:
    """Estado completo del repo propio: último commit, ramas, open issues, tags."""
    if not GITHUB_TOKEN:
        return _no_token_msg()
    repo_data = _gh_get(f"/repos/{repo}")
    commits_data = _gh_get(f"/repos/{repo}/commits", {"per_page": "1"})
    if "error" in repo_data:
        return f"Error: {repo_data['error']}"
    last_commit = ""
    if isinstance(commits_data, list) and commits_data:
        c = commits_data[0]
        sha = c.get("sha", "")[:7]
        msg = c.get("commit", {}).get("message", "").split("\n")[0][:60]
        date = c.get("commit", {}).get("author", {}).get("date", "")[:10]
        last_commit = f"{sha} — {date}: {msg}"
    return (
        f"📊 Estado de {repo}:\n"
        f"   Rama default:  {repo_data.get('default_branch', 'main')}\n"
        f"   Último commit: {last_commit}\n"
        f"   Open issues:   {repo_data.get('open_issues_count', 0)}\n"
        f"   Forks:         {repo_data.get('forks_count', 0)}\n"
        f"   Último push:   {repo_data.get('pushed_at', 'N/A')}"
    )

# ─────────────────────────────────────────────────────────────────────────────
# TOOLS: GIT LOCAL (con guardrails)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def git_local_status() -> str:
    """Estado del repo local: archivos modificados, branch actual, último commit.
    Operación de SOLO LECTURA — segura en todo momento.
    """
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=str(WORKSPACE_ROOT), text=True, encoding="utf-8"
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=str(WORKSPACE_ROOT), text=True, encoding="utf-8"
        ).strip()
        last = subprocess.check_output(
            ["git", "log", "--oneline", "-5"],
            cwd=str(WORKSPACE_ROOT), text=True, encoding="utf-8"
        ).strip()
        status_display = status if status else "✅ Nada por commitear"
        return (
            f"🌿 Rama actual: {branch}\n\n"
            f"📝 Cambios pendientes:\n{status_display}\n\n"
            f"📋 Últimos 5 commits:\n{last}"
        )
    except Exception as e:
        return f"Error leyendo estado local: {e}"

@mcp.tool()
def git_local_commit_push(
    mensaje: str,
    confirmacion: bool = False,
    rama: str = "main"
) -> str:
    """[GUARDRAIL] Hace git add . + commit + push al repo local.

    REQUIERE confirmacion=True para ejecutar. Sin confirmación solo simula.
    Usar ÚNICAMENTE para cambios ya verificados y aprobados.
    El mensaje debe ser descriptivo: 'feat: agrega tool Groq al MCP server'
    """
    if not confirmacion:
        # Modo simulación — muestra qué haría sin ejecutar
        try:
            status = subprocess.check_output(
                ["git", "status", "--short"],
                cwd=str(WORKSPACE_ROOT), text=True, encoding="utf-8"
            ).strip()
        except Exception:
            status = "Error leyendo status"
        return (
            f"⚠️  SIMULACIÓN (confirmacion=False):\n"
            f"   Ejecutaría: git add . && git commit -m '{mensaje}' && git push origin {rama}\n\n"
            f"   Archivos que se commitearían:\n{status or '(ninguno)'}\n\n"
            f"   Para ejecutar de verdad: confirmacion=True"
        )

    # Ejecución real con guardrail
    try:
        subprocess.check_call(["git", "add", "."], cwd=str(WORKSPACE_ROOT))
        result = subprocess.run(
            ["git", "commit", "-m", mensaje],
            cwd=str(WORKSPACE_ROOT), capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode != 0:
            if "nothing to commit" in result.stdout:
                return "ℹ️ No hay cambios para commitear."
            return f"Error en commit: {result.stderr}"
        push = subprocess.run(
            ["git", "push", "origin", rama],
            cwd=str(WORKSPACE_ROOT), capture_output=True, text=True, encoding="utf-8"
        )
        if push.returncode != 0:
            return f"Commit OK pero push falló: {push.stderr}"
        # Log de auditoría
        log_path = WORKSPACE_ROOT / "ANTIGRAVITY_WORK_LOG.txt"
        with open(log_path, "a", encoding="utf-8") as f:
            import datetime
            f.write(f"\n[{datetime.datetime.now().isoformat()}] GIT COMMIT+PUSH: {mensaje}\n")
        return f"✅ Commit y push exitosos.\n   Mensaje: '{mensaje}'\n   Rama: {rama}"
    except Exception as e:
        return f"Error ejecutando git: {e}"


if __name__ == "__main__":
    mcp.run()
