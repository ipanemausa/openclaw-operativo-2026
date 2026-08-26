"""
=============================================================================
HB.OS — OPENAI FREE MCP SERVER
=============================================================================
Conecta modelos de OpenAI a Antigravity vía OpenRouter tier gratuito.
Modelos gratuitos / bajo costo disponibles vía OpenRouter:
  - openai/gpt-4o-mini         (FREE tier — mejor relación calidad/precio)
  - openai/gpt-3.5-turbo       (legacy FREE / muy económico)
  - openai/gpt-4o-mini-2024-07-18  (pinned free version)
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

mcp = FastMCP("HB.OS OpenAI Free — GPT via OpenRouter")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _openrouter_chat(model: str, messages: list, max_tokens: int = 1024) -> str:
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "HB.OS Antigravity MCP — OpenAI Free"
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
            return "Sin respuesta de OpenAI."
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        return f"HTTP {e.code}: {err}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def query_gpt4o_mini(prompt: str, system_prompt: str = "Eres GPT-4o Mini, un asistente inteligente de OpenAI, eficiente y preciso.") -> str:
    """Invoca GPT-4o Mini (tier gratuito vía OpenRouter). La mejor opción gratuita de OpenAI: rápido, multimodal y de alta calidad."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return _openrouter_chat("openai/gpt-4o-mini", messages)


@mcp.tool()
def query_gpt35_turbo(prompt: str, system_prompt: str = "Eres GPT-3.5 Turbo de OpenAI, un asistente rápido y versátil.") -> str:
    """Invoca GPT-3.5 Turbo (legacy free tier vía OpenRouter). Ideal para tareas de texto, resúmenes y código ligero."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return _openrouter_chat("openai/gpt-3.5-turbo", messages)


@mcp.tool()
def query_gpt4o_mini_pinned(prompt: str, system_prompt: str = "Eres GPT-4o Mini, versión estable y gratuita de OpenAI.") -> str:
    """Invoca GPT-4o Mini pinned (2024-07-18), versión fija con disponibilidad garantizada en el tier gratuito de OpenRouter."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return _openrouter_chat("openai/gpt-4o-mini-2024-07-18", messages)


if __name__ == "__main__":
    mcp.run()
