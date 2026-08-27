"""
=============================================================================
OPENCLAW 2026 — SOVEREIGN OPEN-WEIGHT MODEL HUB & LOCAL AI ENGINE MCP SERVER v2.1
=============================================================================
MCP Server para Antigravity IDE.

NIVEL 1 — ULTRA-RÁPIDO (Groq):
  - query_groq_fast      → Llama 3.3 70B (chat, resumen, general)
  - query_groq_coder     → Qwen 2.5 Coder 32B (código rápido)
  - query_groq_reason    → DeepSeek R1 Distill 70B (razonamiento rápido)

NIVEL 2 — OPENROUTER HUB (modelos chinos + Gemini):
  - query_qwen3_max      → Qwen 3.8 Max 235B (RAG, multilingüe, código)
  - query_kimi           → Kimi K2 (contexto 1M, documentos)
  - query_minimax        → Minimax-01 (análisis multimedia, guiones)
  - query_gemini_free    → Gemini 2.0 Flash vía OpenRouter
  - query_deepseek_r1    → DeepSeek-R1 nativo (razonamiento profundo)
  - query_deepseek_v3    → DeepSeek-V3 nativo (código MoE rápido)
  - query_deepseek_harness_v4_v5 → Suite DeepSeek Harness

NIVEL 2 — OPENROUTER LEGACY:
  - query_qwen_2_5       → Qwen 2.5 72B (compatibilidad)
  - query_orca_model     → Orca 2 / Orca Mini

LOCAL (Offline Privado):
  - query_local_ollama   → Ollama local (Qwen2.5, Llama3, DeepSeek R1)
  - query_lm_studio      → LM Studio local
  - query_jan_ai         → Jan AI local
  - query_anything_llm   → RAG local AnythingLLM
  - trigger_comfyui_workflow → ComfyUI imagen/video
  - invoke_pinokio_flow  → Ejecutar scripts/apps en Pinokio
  - generate_jam_audio   → Generar música/audio (Jam)
  - query_odysseus_workspace → Integración con Odysseus (Felix Kjellberg)
=============================================================================
"""

import sys
import os
import json
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
                # IMPORTANTE: Forzar sobrescritura. Si el IDE pasa el literal "${VAR}", lo pisamos con la real.
                os.environ[_k] = _v

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OpenClaw Sovereign Model Hub v2.1 — Groq + OpenRouter + Local")

# ─── KEYS ───────────────────────────────────────────────────────────────────
DEEPSEEK_API_KEY   = os.getenv("DEEPSEEK_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")
DASHSCOPE_API_KEY  = os.getenv("DASHSCOPE_API_KEY", "")
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")

# ─── LOCAL ENDPOINTS ────────────────────────────────────────────────────────
LM_STUDIO_URL    = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
JAN_AI_URL       = os.getenv("JAN_AI_URL", "http://localhost:1337/v1")
ANYTHING_LLM_URL = os.getenv("ANYTHING_LLM_URL", "http://localhost:3001/api/v1")
COMFYUI_URL      = os.getenv("COMFYUI_URL", "http://localhost:8188")
PINOKIO_API_URL  = os.getenv("PINOKIO_API_URL", "http://localhost:4200/api")
JAM_AUDIO_URL    = os.getenv("JAM_AUDIO_URL", "http://localhost:5000/api")
ODYSSEUS_URL     = os.getenv("ODYSSEUS_URL", "http://localhost:11435/v1")

# ─── HELPER HTTP ────────────────────────────────────────────────────────────
def _http_post(url: str, headers: dict, payload: dict, timeout: int = 90) -> dict:
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        return {"error": f"HTTP {e.code}: {err_body}"}
    except Exception as e:
        return {"error": str(e)}

def _openai_compat_call(base_url: str, api_key: str, model: str, prompt: str, system: str, extra_headers: dict = None) -> str:
    """Helper genérico para cualquier endpoint compatible con OpenAI."""
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error [{model}]: {res['error']}"
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return f"Sin respuesta de {model}."

_OR_HEADERS = {
    "HTTP-Referer": "https://openclaw.cloud",
    "X-Title": "OpenClaw Core Matrix 2026"
}

# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 1 — GROQ: ULTRA-RÁPIDO
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def query_groq_fast(prompt: str, system_prompt: str = "Eres un asistente experto. Responde de forma clara y concisa.") -> str:
    """Llama 3.3 70B vía Groq — Ultra-rápido (~1800 tok/s), ideal para chat, resumen y tareas generales. Tier gratuito: 600K tokens/día."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY no configurada. Registrar en https://console.groq.com (gratis)."
    return _openai_compat_call(
        "https://api.groq.com/openai/v1",
        GROQ_API_KEY,
        "llama-3.3-70b-versatile",
        prompt, system_prompt
    )

@mcp.tool()
def query_groq_coder(prompt: str, system_prompt: str = "Eres Qwen 2.5 Coder, especialista en código Python, TypeScript y JavaScript.") -> str:
    """Qwen 2.5 Coder 32B vía Groq — Código ultra-rápido. Ideal para completar funciones, revisar errores, generar scripts."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY no configurada. Registrar en https://console.groq.com (gratis)."
    return _openai_compat_call(
        "https://api.groq.com/openai/v1",
        GROQ_API_KEY,
        "qwen-2.5-coder-32b",
        prompt, system_prompt
    )

@mcp.tool()
def query_groq_reason(prompt: str, system_prompt: str = "Eres DeepSeek R1 Distill, experto en razonamiento lógico y matemático.") -> str:
    """DeepSeek R1 Distill 70B vía Groq — Razonamiento rápido sin latencia de la API de DeepSeek. Tier gratuito incluido."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY no configurada. Registrar en https://console.groq.com (gratis)."
    return _openai_compat_call(
        "https://api.groq.com/openai/v1",
        GROQ_API_KEY,
        "deepseek-r1-distill-llama-70b",
        prompt, system_prompt
    )

# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 2 — OPENROUTER: MODELOS CHINOS NUEVOS
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def query_qwen3_max(prompt: str, system_prompt: str = "Eres Qwen 3.8 Max (235B), el modelo de Alibaba #1 en rankings globales. Especialista en RAG, código multilingüe y análisis técnico.") -> str:
    """Qwen 3.8 Max 235B vía OpenRouter — El modelo chino mejor posicionado en benchmarks 2026. Excelente para RAG, multilingüe (español/inglés/chino), código y análisis."""
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    return _openai_compat_call(
        "https://openrouter.ai/api/v1",
        OPENROUTER_API_KEY,
        "qwen/qwen3-235b-a22b",
        prompt, system_prompt, _OR_HEADERS
    )

@mcp.tool()
def query_kimi(prompt: str, system_prompt: str = "Eres Kimi K2, modelo de Moonshot AI con ventana de contexto de 1M tokens. Especialista en documentos extensos y razonamiento multi-paso.") -> str:
    """Kimi K2 vía OpenRouter — Contexto 1M tokens. Ideal para documentos extensos, planes largos, análisis de múltiples archivos."""
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    return _openai_compat_call(
        "https://openrouter.ai/api/v1",
        OPENROUTER_API_KEY,
        "moonshotai/kimi-k2",
        prompt, system_prompt, _OR_HEADERS
    )

@mcp.tool()
def query_minimax(prompt: str, system_prompt: str = "Eres Minimax-01, especialista en análisis multimedia, generación de guiones y contenido audiovisual.") -> str:
    """Minimax-01 vía OpenRouter — Del mismo equipo que Minimax H3 (video). Ideal para guiones de video, análisis de contenido multimedia, storyboards."""
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    return _openai_compat_call(
        "https://openrouter.ai/api/v1",
        OPENROUTER_API_KEY,
        "minimax/minimax-01",
        prompt, system_prompt, _OR_HEADERS
    )

@mcp.tool()
def query_gemini_free(prompt: str, system_prompt: str = "Eres Gemini 2.0 Flash, modelo multimodal de Google. Especialista en razonamiento general, Firebase y análisis visual.") -> str:
    """Gemini 2.0 Flash vía OpenRouter — Gratis, multimodal. Ideal para razonamiento general, integraciones Firebase, análisis visual."""
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    return _openai_compat_call(
        "https://openrouter.ai/api/v1",
        OPENROUTER_API_KEY,
        "google/gemini-2.0-flash-001",
        prompt, system_prompt, _OR_HEADERS
    )

# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 2 — DEEPSEEK DIRECTO (API nativa)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def query_deepseek_r1(prompt: str, system_prompt: str = "Eres DeepSeek-R1, experto en razonamiento algorítmico y lógica matemática.") -> str:
    """Invoca DeepSeek-R1 nativo para razonamiento lógico profundo y matemática avanzada. Incluye chain-of-thought."""
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error invocando DeepSeek-R1: {res['error']}"
    choices = res.get("choices", [])
    if choices:
        msg = choices[0].get("message", {})
        reasoning = msg.get("reasoning_content", "")
        content = msg.get("content", "")
        if reasoning:
            return f"### [Pensamiento R1]\n{reasoning}\n\n### [Respuesta Final]\n{content}"
        return content
    return "Sin respuesta de DeepSeek-R1."

@mcp.tool()
def query_deepseek_v3(prompt: str, system_prompt: str = "Eres DeepSeek-V3, modelo MoE de alta velocidad para código e inferencia rápida.") -> str:
    """Invoca DeepSeek-V3 nativo para código e inferencia rápida."""
    return _openai_compat_call(
        "https://api.deepseek.com/v1",
        DEEPSEEK_API_KEY,
        "deepseek-chat",
        prompt, system_prompt
    )

@mcp.tool()
def query_deepseek_harness_v4_v5(prompt: str, version: str = "v5", system_prompt: str = "Eres DeepSeek Harness V4/V5, orquestador de desarrollo avanzado.") -> str:
    """Suite DeepSeek Harness (V4=chat / V5=reasoner) para orquestación de desarrollo."""
    model_name = "deepseek-reasoner" if version.lower() == "v5" else "deepseek-chat"
    return _openai_compat_call(
        "https://api.deepseek.com/v1",
        DEEPSEEK_API_KEY,
        model_name,
        prompt, system_prompt
    )

# ─────────────────────────────────────────────────────────────────────────────
# LEGACY — OPENROUTER (compatibilidad anterior)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def query_qwen_2_5(prompt: str, system_prompt: str = "Eres Qwen 2.5 72B Instruct, especialista en JSON determinista y código multilingüe.") -> str:
    """Qwen 2.5 72B vía OpenRouter — Versión anterior de Qwen. Usar query_qwen3_max para Qwen 3.8."""
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY no configurada."
    return _openai_compat_call(
        "https://openrouter.ai/api/v1",
        OPENROUTER_API_KEY,
        "qwen/qwen-2.5-72b-instruct",
        prompt, system_prompt, _OR_HEADERS
    )

@mcp.tool()
def query_orca_model(prompt: str, model_variant: str = "orca-2-13b") -> str:
    """Modelos Orca (Microsoft) para razonamiento explicativo paso a paso."""
    model_id = "microsoft/orca-2-13b" if "13b" in model_variant else "microsoft/orca-mini-3b"
    if not OPENROUTER_API_KEY:
        return query_local_ollama(prompt, model="llama3")
    return _openai_compat_call(
        "https://openrouter.ai/api/v1",
        OPENROUTER_API_KEY,
        model_id,
        prompt,
        "Eres Orca, optimizado para razonamiento paso a paso con explicaciones detalladas.",
        _OR_HEADERS
    )

# ─────────────────────────────────────────────────────────────────────────────
# LOCAL — OFFLINE PRIVADO
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def query_local_ollama(prompt: str, model: str = "qwen2.5:latest") -> str:
    """Inferencia 100% offline via Ollama local (localhost:11434). Soporta: qwen2.5, llama3, deepseek-r1, mistral, phi3."""
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "stream": False}
    res = _http_post(url, headers, payload, timeout=120)
    if "error" in res:
        return f"Ollama local no disponible en http://localhost:11434. Detalles: {res['error']}"
    return res.get("response", "Sin respuesta de Ollama local.")

@mcp.tool()
def query_lm_studio(prompt: str, model: str = "local-model") -> str:
    """Servidor local LM Studio (http://localhost:1234/v1)."""
    url = f"{LM_STUDIO_URL}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"LM Studio no detectado en {LM_STUDIO_URL}."
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de LM Studio."

@mcp.tool()
def query_jan_ai(prompt: str, model: str = "local-model") -> str:
    """Servidor local Jan AI (http://localhost:1337/v1)."""
    url = f"{JAN_AI_URL}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Jan AI no detectado en {JAN_AI_URL}."
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de Jan AI."

@mcp.tool()
def query_anything_llm(prompt: str, workspace_slug: str = "main") -> str:
    """RAG local en AnythingLLM (http://localhost:3001/api/v1). Búsqueda vectorial sobre documentos locales."""
    url = f"{ANYTHING_LLM_URL}/workspace/{workspace_slug}/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"message": prompt, "mode": "chat"}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Anything LLM no detectado en {ANYTHING_LLM_URL}."
    return res.get("textResponse", "Sin respuesta de Anything LLM.")

@mcp.tool()
def trigger_comfyui_workflow(prompt_json: str) -> str:
    """Envía workflow de imagen/video a ComfyUI local (http://localhost:8188). prompt_json: JSON del workflow ComfyUI."""
    url = f"{COMFYUI_URL}/prompt"
    headers = {"Content-Type": "application/json"}
    try:
        workflow_data = json.loads(prompt_json)
    except Exception as e:
        return f"Error en JSON de ComfyUI: {str(e)}"
    payload = {"prompt": workflow_data}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"ComfyUI no detectado en {COMFYUI_URL}."
    prompt_id = res.get("prompt_id", "desconocido")
    return f"Workflow enviado a ComfyUI. Prompt ID: {prompt_id}"

@mcp.tool()
def invoke_pinokio_flow(script_path: str, args: dict = None) -> str:
    """Envía un script de ejecución a Pinokio (AI Browser local)."""
    url = f"{PINOKIO_API_URL}/run"
    headers = {"Content-Type": "application/json"}
    payload = {"script": script_path, "args": args or {}}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error conectando con Pinokio en {PINOKIO_API_URL}. Detalles: {res['error']}"
    return res.get("status", "Comando enviado a Pinokio con éxito.")

@mcp.tool()
def generate_jam_audio(prompt: str) -> str:
    """Genera música o audio utilizando el modelo de Jam (local o API)."""
    url = f"{JAM_AUDIO_URL}/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error conectando con generador Jam de audio: {res['error']}"
    return res.get("file_url", "Audio Jam generado y guardado localmente.")

@mcp.tool()
def query_odysseus_workspace(prompt: str) -> str:
    """Envía un prompt a Odysseus (workspace open-source creado por Felix Kjellberg 'PewDiePie')."""
    url = f"{ODYSSEUS_URL}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {"messages": [{"role": "user", "content": prompt}]}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error conectando con Odysseus en {ODYSSEUS_URL}. Asegúrate de tenerlo ejecutando localmente."
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de Odysseus."

if __name__ == "__main__":
    mcp.run()
