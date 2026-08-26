"""
=============================================================================
OPENCLAW 2026 — DEDICATED OLLAMA LOCAL MCP SERVER
=============================================================================
Provee integración determinista MCP para Ollama local (localhost:11434):
- Inferencia offline 100% privada (Llama 3, Qwen 2.5, DeepSeek R1 local, Orca)
- Gestión de modelos (list, generate, chat, pull)
=============================================================================
"""

import sys
import os
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OpenClaw Ollama Local Engine")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def _http_request(url: str, method: str = "GET", payload: dict = None) -> dict:
    data = json.dumps(payload).encode('utf-8') if payload else None
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        return {"error": f"HTTP {e.code}: {err_body}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def ollama_generate(prompt: str, model: str = "qwen2.5:latest", system_prompt: str = "") -> str:
    """Genera una respuesta en texto usando un modelo local en Ollama (ej. qwen2.5, llama3, deepseek-r1:8b)."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    if system_prompt:
        payload["system"] = system_prompt
    res = _http_request(url, method="POST", payload=payload)
    if "error" in res:
        return f"Ollama local no disponible en {OLLAMA_BASE_URL}. Error: {res['error']}"
    return res.get("response", "Sin respuesta de Ollama.")

@mcp.tool()
def ollama_chat(prompt: str, model: str = "llama3:latest", system_prompt: str = "Eres un asistente de IA local ejecutándose sin conexión a internet.") -> str:
    """Ejecuta un turno de conversación chat en formato de mensajes usando Ollama local."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    res = _http_request(url, method="POST", payload=payload)
    if "error" in res:
        return f"Ollama local no disponible en {OLLAMA_BASE_URL}. Error: {res['error']}"
    message = res.get("message", {})
    return message.get("content", "Sin respuesta de Ollama Chat.")

@mcp.tool()
def ollama_list_models() -> str:
    """Lista todos los modelos instalados actualmente en la instancia local de Ollama."""
    url = f"{OLLAMA_BASE_URL}/api/tags"
    res = _http_request(url, method="GET")
    if "error" in res:
        return f"Error consultando modelos Ollama en {OLLAMA_BASE_URL}: {res['error']}"
    models = res.get("models", [])
    if not models:
        return "No hay modelos instalados actualmente en Ollama local."
    out = ["### Modelos Ollama Instalados Localmente:"]
    for m in models:
        name = m.get("name", "Desconocido")
        size_gb = round(m.get("size", 0) / (1024**3), 2)
        modified = m.get("modified_at", "")[:10]
        out.append(f"- **{name}** ({size_gb} GB) - Modificado: {modified}")
    return "\n".join(out)

if __name__ == "__main__":
    mcp.run()
