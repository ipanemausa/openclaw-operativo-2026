"""
=============================================================================
OPENCLAW 2026 — SOVEREIGN OPEN-WEIGHT MODEL HUB & LOCAL AI ENGINE MCP SERVER
=============================================================================
Provee integración determinista MCP para el ecosistema de IA Local:
- DeepSeek-R1 (deepseek-reasoner)
- DeepSeek-V3 / V4 / V5 (deepseek-chat)
- DeepSeek Developer Studio Chat
- Qwen 2.5 (qwen/qwen-2.5-72b-instruct & qwen-2.5-coder-32b)
- Orca (orca-2-13b / orca-mini)
- Ollama Local (http://localhost:11434)
- LM Studio (http://localhost:1234/v1)
- Jan AI (http://localhost:1337/v1)
- Anything LLM (http://localhost:3001/api/v1)
- ComfyUI (http://localhost:8188)
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

mcp = FastMCP("OpenClaw Sovereign Open-Weight & Local AI Ecosystem Hub")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
JAN_AI_URL = os.getenv("JAN_AI_URL", "http://localhost:1337/v1")
ANYTHING_LLM_URL = os.getenv("ANYTHING_LLM_URL", "http://localhost:3001/api/v1")
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://localhost:8188")

def _http_post(url: str, headers: dict, payload: dict) -> dict:
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
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
def query_deepseek_r1(prompt: str, system_prompt: str = "Eres DeepSeek-R1, experto en razonamiento algorítmico y lógica matemática.") -> str:
    """Invoca DeepSeek-R1 para razonamiento lógico profundo y matemática avanzada."""
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
            return f"### [Pensamiento Razonado R1]\n{reasoning}\n\n### [Respuesta Final]\n{content}"
        return content
    return "Sin respuesta de DeepSeek-R1."

@mcp.tool()
def query_deepseek_v3(prompt: str, system_prompt: str = "Eres DeepSeek-V3, modelo MoE de alta velocidad.") -> str:
    """Invoca DeepSeek-V3 para inferencia conversacional rápida y código."""
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error invocando DeepSeek-V3: {res['error']}"
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de DeepSeek-V3."

@mcp.tool()
def query_deepseek_harness_v4_v5(prompt: str, version: str = "v5", system_prompt: str = "Eres DeepSeek Harness V4/V5, orquestador de desarrollo avanzado.") -> str:
    """Invoca la suite DeepSeek Harness (V4/V5) y DeepSeek Studio Chat para desarrolladores."""
    model_name = "deepseek-reasoner" if version.lower() == "v5" else "deepseek-chat"
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error invocando DeepSeek Harness {version.upper()}: {res['error']}"
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return f"Sin respuesta de DeepSeek Harness {version.upper()}."

@mcp.tool()
def query_qwen_2_5(prompt: str, system_prompt: str = "Eres Qwen 2.5 72B Instruct, especialista en JSON determinista y código multilingüe.") -> str:
    """Invoca Qwen 2.5 72B vía OpenRouter para estructuras JSON y código sofisticado."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "OpenClaw Antigravity MCP"
    }
    payload = {
        "model": "qwen/qwen-2.5-72b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Error invocando Qwen 2.5: {res['error']}"
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de Qwen 2.5."

@mcp.tool()
def query_orca_model(prompt: str, model_variant: str = "orca-2-13b") -> str:
    """Invoca modelos de la familia Orca (Orca 2 / Orca Mini) para razonamiento explicativo paso a paso."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai"
    }
    model_id = "microsoft/orca-2-13b" if "13b" in model_variant else "microsoft/orca-mini-3b"
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "Eres Orca, un modelo optimizado para el razonamiento paso a paso con explicaciones detalladas."},
            {"role": "user", "content": prompt}
        ]
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return query_local_ollama(prompt, model=model_variant)
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de Orca."

@mcp.tool()
def query_local_ollama(prompt: str, model: str = "qwen2.5:latest") -> str:
    """Invoca modelo local 100% offline mediante servidor Ollama local (localhost:11434). Soporta llama3, qwen2.5, deepseek-r1, orca."""
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Ollama local no disponible en http://localhost:11434. Detalles: {res['error']}"
    return res.get("response", "Sin respuesta de Ollama local.")

@mcp.tool()
def query_lm_studio(prompt: str, model: str = "local-model") -> str:
    """Invoca el servidor local de LM Studio (http://localhost:1234/v1)."""
    url = f"{LM_STUDIO_URL}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"LM Studio no detectado en {LM_STUDIO_URL}. Inicia el servidor local en LM Studio."
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de LM Studio."

@mcp.tool()
def query_jan_ai(prompt: str, model: str = "local-model") -> str:
    """Invoca el servidor local de Jan AI (http://localhost:1337/v1)."""
    url = f"{JAN_AI_URL}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Jan AI no detectado en {JAN_AI_URL}. Inicia el servidor local en Jan AI."
    choices = res.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return "Sin respuesta de Jan AI."

@mcp.tool()
def query_anything_llm(prompt: str, workspace_slug: str = "main") -> str:
    """Invoca la base de conocimiento RAG local en Anything LLM (http://localhost:3001/api/v1)."""
    url = f"{ANYTHING_LLM_URL}/workspace/{workspace_slug}/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": prompt,
        "mode": "chat"
    }
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"Anything LLM no detectado en {ANYTHING_LLM_URL}. Verifica que el contenedor o app esté activo."
    return res.get("textResponse", "Sin respuesta de Anything LLM.")

@mcp.tool()
def trigger_comfyui_workflow(prompt_json: str) -> str:
    """Envía un workflow de generación de imagen/video a la API local de ComfyUI (http://localhost:8188/prompt)."""
    url = f"{COMFYUI_URL}/prompt"
    headers = {"Content-Type": "application/json"}
    try:
        workflow_data = json.loads(prompt_json)
    except Exception as e:
        return f"Error en JSON de ComfyUI: {str(e)}"
    payload = {"prompt": workflow_data}
    res = _http_post(url, headers, payload)
    if "error" in res:
        return f"ComfyUI no detectado en {COMFYUI_URL}. Inicia ComfyUI en el puerto 8188."
    prompt_id = res.get("prompt_id", "desconocido")
    return f"Workflow enviado a ComfyUI con éxito. Prompt ID: {prompt_id}"

if __name__ == "__main__":
    mcp.run()
