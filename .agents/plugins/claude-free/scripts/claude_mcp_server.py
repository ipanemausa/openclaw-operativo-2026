"""
=============================================================================
HB.OS — CLAUDE FREE MCP SERVER
=============================================================================
Conecta Claude de Anthropic a Antigravity vía OpenRouter tier gratuito.
Modelos gratuitos disponibles vía OpenRouter:
  - anthropic/claude-3-haiku          (FREE tier, muy rápido)
  - anthropic/claude-3.5-haiku        (FREE tier cuando hay disponibilidad)
  - anthropic/claude-instant-1.2      (legacy FREE)
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

mcp = FastMCP("HB.OS Claude Free — Anthropic via OpenRouter")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _openrouter_chat(model: str, messages: list, max_tokens: int = 1024) -> str:
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "HB.OS Antigravity MCP — Claude Free"
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OPENROUTER_URL, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            choices = body.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "Sin respuesta.")
            return "Sin respuesta de Claude."
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        return f"HTTP {e.code}: {err}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def query_claude_haiku(prompt: str, system_prompt: str = "Eres Claude 3 Haiku, un asistente rápido y preciso de Anthropic.") -> str:
    """Invoca Claude 3 Haiku (tier gratuito vía OpenRouter). Ideal para tareas rápidas de texto, código y análisis sin coste."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return _openrouter_chat("anthropic/claude-3-haiku", messages)


@mcp.tool()
def query_claude_haiku_35(prompt: str, system_prompt: str = "Eres Claude 3.5 Haiku, asistente de alta capacidad de Anthropic.") -> str:
    """Invoca Claude 3.5 Haiku (disponible en tier gratuito/bajo costo vía OpenRouter). Mejor rendimiento que Haiku 3."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return _openrouter_chat("anthropic/claude-3.5-haiku", messages)


@mcp.tool()
def query_claude_instant(prompt: str, system_prompt: str = "Eres Claude Instant, el modelo de Anthropic optimizado para velocidad.") -> str:
    """Invoca Claude Instant 1.2 (legacy, tier gratuito vía OpenRouter). Excelente para Q&A y resúmenes ligeros."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return _openrouter_chat("anthropic/claude-instant-1.2", messages)


if __name__ == "__main__":
    mcp.run()
