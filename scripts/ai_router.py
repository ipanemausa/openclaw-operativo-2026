"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — AI ROUTER MULTI-MODELO REAL
==============================================================================
Router inteligente que selecciona y despacha al modelo óptimo según tarea.
Ecosistema: DeepSeek (directo) + Qwen/Kimi (OpenRouter) + Gemini + Claude

Fuente de verdad de keys: C:\\Users\\ipane\\.openclaw-master.env
==============================================================================
"""

import os
import json
import time
import requests
from typing import Optional
from dotenv import load_dotenv

# Cargar keys desde el archivo maestro
load_dotenv(r"C:\Users\ipane\.openclaw-master.env", override=True)

# ─── CONFIGURACIÓN DE MODELOS ───────────────────────────────────────────────

MODELS = {
    # Ecosistema chino — código, matemáticas, RAG técnico
    "deepseek": {
        "id": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1",
        "key_env": "DEEPSEEK_API_KEY",
        "max_tokens": 2048,
        "tags": ["code", "math", "structured_output"],
    },
    # Qwen vía OpenRouter — multilingüe, joyería, mercado latinoamericano
    "qwen": {
        "id": "qwen/qwen-2.5-72b-instruct",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 2048,
        "tags": ["multilingual", "rag", "jewelry", "latam"],
    },
    # Kimi K3 vía OpenRouter — razonamiento largo, documentos extensos
    "kimi": {
        "id": "moonshotai/kimi-k2",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 4096,
        "tags": ["long_context", "reasoning", "documents"],
    },
    # Gemini — razonamiento general, multimodal, Firebase nativo
    "gemini": {
        "id": "google/gemini-2.0-flash-001",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 2048,
        "tags": ["reasoning", "general", "firebase"],
    },
    # Claude — fallback de alta calidad, análisis de negocio
    "claude": {
        "id": "anthropic/claude-sonnet-4-5",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 2048,
        "tags": ["business", "analysis", "fallback"],
    },
}

# ─── TABLA DE DESPACHO POR TIPO DE TAREA ────────────────────────────────────

DISPATCH_TABLE = {
    "code":              "deepseek",
    "math":              "deepseek",
    "structured_output": "deepseek",
    "rag":               "qwen",
    "multilingual":      "qwen",
    "jewelry":           "qwen",
    "latam":             "qwen",
    "long_context":      "kimi",
    "documents":         "kimi",
    "reasoning":         "gemini",
    "general":           "gemini",
    "business":          "claude",
    "fallback":          "claude",
}

# ─── ROUTER PRINCIPAL ────────────────────────────────────────────────────────

class AIRouter:
    """Router multi-modelo OpenClaw — despacha al modelo óptimo por tarea."""

    def __init__(self):
        self.session_id = f"ROUTER-{int(time.time())}"
        self._verify_keys()

    def _verify_keys(self):
        """Verifica que las keys necesarias estén disponibles."""
        missing = []
        checked = set()
        for model_cfg in MODELS.values():
            env_var = model_cfg["key_env"]
            if env_var not in checked:
                checked.add(env_var)
                if not os.getenv(env_var):
                    missing.append(env_var)
        if missing:
            print(f"[ROUTER WARNING] Keys no encontradas: {missing}")
            print(f"  -> Verificar C:\\Users\\ipane\\.openclaw-master.env")
        else:
            print(f"[ROUTER OK] Todas las API keys cargadas correctamente.")

    def select_model(self, task_type: str) -> str:
        """Selecciona el modelo óptimo para el tipo de tarea."""
        model_key = DISPATCH_TABLE.get(task_type, "claude")
        model_cfg = MODELS[model_key]
        print(f"[ROUTER] Tarea '{task_type}' → Modelo: {model_cfg['id']}")
        return model_key

    def call(
        self,
        prompt: str,
        task_type: str = "general",
        system: Optional[str] = None,
        model_override: Optional[str] = None,
    ) -> dict:
        """
        Llama al modelo seleccionado y retorna respuesta estructurada.

        Args:
            prompt: Pregunta o instrucción
            task_type: Tipo de tarea para selección automática de modelo
            system: System prompt opcional
            model_override: Forzar un modelo específico

        Returns:
            dict con keys: model, response, tokens, latency_ms, success
        """
        t0 = time.time()
        model_key = model_override if model_override else self.select_model(task_type)
        cfg = MODELS[model_key]
        api_key = os.getenv(cfg["key_env"], "")

        if not api_key:
            return {
                "model": cfg["id"],
                "response": f"ERROR: Key '{cfg['key_env']}' no encontrada en master env.",
                "tokens": 0,
                "latency_ms": 0,
                "success": False,
            }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        # OpenRouter requiere header adicional
        if "openrouter" in cfg["base_url"]:
            headers["HTTP-Referer"] = "https://openclaw.cloud"
            headers["X-Title"] = "OpenClaw Core Matrix 2026"

        payload = {
            "model": cfg["id"],
            "messages": messages,
            "max_tokens": cfg["max_tokens"],
            "temperature": 0.3,
        }

        try:
            resp = requests.post(
                f"{cfg['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            latency = int((time.time() - t0) * 1000)

            return {
                "model": cfg["id"],
                "response": content,
                "tokens": tokens,
                "latency_ms": latency,
                "success": True,
            }

        except requests.exceptions.HTTPError as e:
            return {
                "model": cfg["id"],
                "response": f"HTTP ERROR {e.response.status_code}: {e.response.text[:300]}",
                "tokens": 0,
                "latency_ms": int((time.time() - t0) * 1000),
                "success": False,
            }
        except Exception as e:
            return {
                "model": cfg["id"],
                "response": f"ERROR: {str(e)}",
                "tokens": 0,
                "latency_ms": int((time.time() - t0) * 1000),
                "success": False,
            }

    def print_result(self, result: dict):
        """Imprime el resultado de forma legible."""
        status = "[OK]" if result["success"] else "[FAIL]"
        print(f"\n{'─'*60}")
        print(f"{status} Modelo:    {result['model']}")
        print(f"   Tokens:    {result['tokens']}")
        print(f"   Latencia:  {result['latency_ms']}ms")
        print(f"   Respuesta:")
        print(f"   {result['response'][:800]}")
        print(f"{'─'*60}")


# ─── INSTANCIA GLOBAL ────────────────────────────────────────────────────────

router = AIRouter()


if __name__ == "__main__":
    # Test rápido de conectividad
    print("\n[AI ROUTER] Test de conectividad rápido...\n")
    result = router.call(
        prompt="Responde en una sola línea: ¿Estás conectado y funcionando?",
        task_type="general",
    )
    router.print_result(result)
