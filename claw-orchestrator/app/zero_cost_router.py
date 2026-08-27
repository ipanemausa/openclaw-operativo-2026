"""
=============================================================================
OPENCLAW 2026 — ZERO-COST EDGE ROUTER
=============================================================================
Enrutador de baja latencia que maximiza el Free-Tier "EdgeCut" de los modelos
americanos (Google, OpenAI, Anthropic, Meta).

Estrategia de Enrutamiento:
- 'chat' o 'resumen'  -> Groq (Llama 3.3 70B) - Maxima velocidad (<1s)
- 'multimodal'        -> Gemini 2.0 Flash - Mejor vision/audio gratuito
- 'parsing' / 'json'  -> Claude 3.5 Haiku - Formateo estructural veloz
- 'edge' / 'rapido'   -> GPT-4o-Mini - Utilidad general rápida
=============================================================================
"""

import os
import json
import urllib.request
from pathlib import Path

# Cargar master env
_MASTER_ENV = Path(r"C:\Users\ipane\.openclaw-master.env")
if _MASTER_ENV.exists():
    for _line in _MASTER_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in _line and not _line.strip().startswith("#"):
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            _v = _v.strip().strip('"').strip("'")
            if _v and not _v.startswith("tu_"):
                os.environ[_k] = _v

GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def _http_post(url: str, headers: dict, payload: dict, timeout: int = 30) -> dict:
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body)
    except Exception as e:
        return {"error": str(e)}

def _openai_compat_call(base_url: str, api_key: str, model: str, prompt: str, system: str) -> str:
    if not api_key:
        return f"Error: API Key no configurada para {model}."
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.cloud",
        "X-Title": "OpenClaw Edge Router"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error [{model}]: {res['error']}"
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return f"Sin respuesta de {model}."


class ZeroCostEdgeRouter:
    @staticmethod
    def route_task(task_type: str, prompt: str, system: str = "Eres un agente veloz de OpenClaw.") -> str:
        """
        Enruta dinámicamente la tarea al modelo gratuito más óptimo.
        """
        task_type = task_type.lower()
        
        if task_type in ['chat', 'resumen', 'traduccion']:
            # Groq (Llama 3.3 70B)
            return _openai_compat_call(
                "https://api.groq.com/openai/v1",
                GROQ_API_KEY,
                "llama-3.3-70b-versatile",
                prompt, system
            )
            
        elif task_type in ['multimodal', 'vision', 'firebase']:
            # Gemini 2.0 Flash via OpenRouter
            return _openai_compat_call(
                "https://openrouter.ai/api/v1",
                OPENROUTER_API_KEY,
                "google/gemini-2.0-flash-001",
                prompt, system
            )
            
        elif task_type in ['parsing', 'json', 'extracción']:
            # Claude 3.5 Haiku via OpenRouter
            return _openai_compat_call(
                "https://openrouter.ai/api/v1",
                OPENROUTER_API_KEY,
                "anthropic/claude-3-5-haiku",
                prompt, system
            )
            
        else:
            # Por defecto: GPT-4o-Mini via OpenRouter
            return _openai_compat_call(
                "https://openrouter.ai/api/v1",
                OPENROUTER_API_KEY,
                "openai/gpt-4o-mini",
                prompt, system
            )

if __name__ == "__main__":
    print("Zero-Cost Edge Router Inicializado.")
    print("Probando ruteo por defecto...")
    res = ZeroCostEdgeRouter.route_task("rapido", "Di 'Hola desde el Edge Router'.", "System")
    print(res)
