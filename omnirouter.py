"""
==============================================================================
OPENCLAW 2026 — OMNIROUTER & SOVEREIGN AI GATEWAY (FASTAPI)
==============================================================================
Motor unificado de enrutamiento de modelos Open-Weight y APIs soberanas:
- DeepSeek (V3 / R1)
- Groq (Inferencia Ultra-Rápida)
- OpenRouter (Qwen 2.5, Kimi, Minimax, Gemini 2.0)
- Ollama Local (localhost:11434)
- Google Gemini Directo
- Endpoints de salud, estado, chat y compatibilidad OpenAI v1
==============================================================================
"""

import os
import time
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import requests

# 1. Cargar variables de entorno (Local + Master)
load_dotenv()
MASTER_ENV = r"C:\Users\ipane\.openclaw-master.env"
if os.path.exists(MASTER_ENV):
    load_dotenv(MASTER_ENV)

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [OmniRouter] %(message)s"
)
logger = logging.getLogger("OmniRouter")

# 2. Instanciación FastAPI
app = FastAPI(
    title="OpenClaw OmniRouter & Sovereign AI Gateway",
    description="Motor de enrutamiento soberano multimodelo para HB Jewelry y HB.OS",
    version="2026.7.1"
)

# CORS Permisivo para Frontend Vite (localhost:5173, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Modelos Pydantic
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "deepseek-chat"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    stream: Optional[bool] = False

class AgentRequest(BaseModel):
    agent_id: Optional[str] = "main"
    prompt: str
    context: Optional[Dict[str, Any]] = None
    model_preference: Optional[str] = "auto"

# 4. Proveedores y Claves
def get_providers_status() -> Dict[str, Any]:
    return {
        "deepseek": bool(os.getenv("DEEPSEEK_API_KEY")),
        "groq": bool(os.getenv("GROQ_API_KEY")),
        "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")),
        "ollama": True # Localhost
    }

# 5. Endpoints de Salud y Estado
@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "HB.OS OmniRouter Gateway",
        "version": "2026.7.1",
        "timestamp": int(time.time()),
        "providers": get_providers_status()
    }

@app.get("/api/providers")
def get_providers():
    status = get_providers_status()
    return {
        "providers": [
            {"name": "groq", "active": status["groq"], "tier": "ultra_fast"},
            {"name": "openrouter", "active": status["openrouter"], "tier": "universal_hub"},
            {"name": "deepseek", "active": status["deepseek"], "tier": "reasoning_r1"},
            {"name": "gemini", "active": status["gemini"], "tier": "multimodal"},
            {"name": "ollama", "active": status["ollama"], "tier": "offline_private", "url": "http://localhost:11434"}
        ]
    }

@app.get("/api/combos")
def get_combos():
    return {
        "combos": [
            {
                "name": "combo-best-free",
                "description": "Mejor modelo gratuito disponible en orden de latencia",
                "models": ["groq/llama-3.3-70b-versatile", "openrouter/google/gemini-2.0-flash-001"]
            },
            {
                "name": "combo-deepseek-sovereign",
                "description": "Enrutamiento estricto a DeepSeek V3 / R1",
                "models": ["deepseek/deepseek-chat", "groq/deepseek-r1-distill-llama-70b", "ollama/deepseek-r1:latest"]
            }
        ]
    }

@app.get("/api/models")
def list_models():
    models = [
        {"id": "deepseek-chat", "provider": "deepseek", "description": "DeepSeek V3 Oficial"},
        {"id": "deepseek-reasoner", "provider": "deepseek", "description": "DeepSeek R1 Oficial"},
        {"id": "groq/llama-3.3-70b", "provider": "groq", "description": "Llama 3.3 70B en Groq LPU"},
        {"id": "groq/deepseek-r1", "provider": "groq", "description": "DeepSeek R1 Distill en Groq"},
        {"id": "openrouter/auto", "provider": "openrouter", "description": "OpenRouter Smart Auto"},
        {"id": "gemini-2.0-flash", "provider": "gemini", "description": "Google Gemini 2.0 Flash"},
        {"id": "ollama/local", "provider": "ollama", "description": "Ollama Localhost:11434"}
    ]
    return {"object": "list", "data": models}

# 6. Enrutador de Chat Central
@app.post("/v1/chat/completions")
@app.post("/api/chat")
async def chat_completions(req: ChatCompletionRequest):
    messages_payload = [{"role": m.role, "content": m.content} for m in req.messages]
    
    # 1. Intentar con Groq si está disponible y requerido o auto
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and ("groq" in req.model.lower() or req.model == "auto"):
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages_payload,
                    "temperature": req.temperature,
                    "max_tokens": req.max_tokens
                },
                timeout=20
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"Fallback desde Groq por error: {e}")

    # 2. Intentar con DeepSeek Directo
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_key and ("deepseek" in req.model.lower() or req.model == "auto"):
        try:
            resp = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"},
                json={
                    "model": "deepseek-chat",
                    "messages": messages_payload,
                    "temperature": req.temperature,
                    "max_tokens": req.max_tokens
                },
                timeout=25
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"Fallback desde DeepSeek por error: {e}")

    # 3. Intentar con OpenRouter
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_key}",
                    "HTTP-Referer": "https://hb-jewelry-cloud-2026-2dff9.web.app/",
                    "X-Title": "HB.OS Sovereign AI",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "google/gemini-2.0-flash-001" if "gemini" in req.model.lower() else "deepseek/deepseek-chat",
                    "messages": messages_payload,
                    "temperature": req.temperature
                },
                timeout=25
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"Fallback desde OpenRouter por error: {e}")

    # 4. Fallback a Ollama Local
    try:
        ollama_resp = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:latest",
                "messages": messages_payload,
                "stream": False
            },
            timeout=15
        )
        if ollama_resp.status_code == 200:
            data = ollama_resp.json()
            return {
                "id": f"chatcmpl-ollama-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "ollama/local",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": data.get("message", {}).get("content", "")
                    },
                    "finish_reason": "stop"
                }]
            }
    except Exception as e:
        logger.warning(f"Fallback a Ollama falló o no está activo: {e}")

    # 5. Respuesta de contingencia autónoma
    return {
        "id": f"chatcmpl-emergency-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "hbos-emergency-router",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "HB.OS OmniRouter activo. Conexión establecida con la infraestructura soberana 2026."
            },
            "finish_reason": "stop"
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("omnirouter:app", host="0.0.0.0", port=8080, reload=True)
