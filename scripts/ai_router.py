"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — AI ROUTER MULTI-MODELO REAL v2.1
==============================================================================
Router inteligente que selecciona y despacha al modelo óptimo según tarea.

NIVEL 1 — ULTRA-RÁPIDO: Groq (Llama 3.3 70B, Qwen 2.5 Coder, DeepSeek R1 Distill)
NIVEL 2 — OPENROUTER HUB: Qwen 3.8, Kimi K2, Minimax, Gemini 2.0, Claude
NIVEL 3 — DIRECTO: api.deepseek.com, Ollama local

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

# ─── NIVEL 1: GROQ — ULTRA-RÁPIDO (600K tokens/día gratis) ─────────────────

GROQ_MODELS = {
    "groq-llama": {
        "id": "llama-3.3-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "max_tokens": 8192,
        "tags": ["fast", "chat", "summarize", "general"],
        "tier": 1,
    },
    "groq-qwen-coder": {
        "id": "qwen-2.5-coder-32b",
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "max_tokens": 8192,
        "tags": ["fast_code", "typescript", "python"],
        "tier": 1,
    },
    "groq-deepseek-r1": {
        "id": "deepseek-r1-distill-llama-70b",
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "max_tokens": 8192,
        "tags": ["fast_reasoning", "math", "logic"],
        "tier": 1,
    },
    "groq-mixtral": {
        "id": "mixtral-8x7b-32768",
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "max_tokens": 32768,
        "tags": ["multilingual_fast", "long_chat"],
        "tier": 1,
    },
}

# ─── NIVEL 2: OPENROUTER HUB — MODELOS CHINOS + GEMINI ──────────────────────

OPENROUTER_MODELS = {
    # Qwen 3.8 Max (el mejor modelo actual según rankings)
    "qwen3-max": {
        "id": "qwen/qwen3-235b-a22b",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 4096,
        "tags": ["rag", "multilingual", "jewelry", "latam", "code"],
        "tier": 2,
    },
    # Kimi K2 — contexto largo 1M, documentos extensos
    "kimi": {
        "id": "moonshotai/kimi-k2",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 16384,
        "tags": ["long_context", "documents", "analysis"],
        "tier": 2,
    },
    # Minimax — análisis multimedia y texto largo
    "minimax": {
        "id": "minimax/minimax-01",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 4096,
        "tags": ["multimedia_analysis", "video_scripts"],
        "tier": 2,
    },
    # Gemini 2.0 Flash — multimodal, gratis vía OpenRouter
    "gemini-or": {
        "id": "google/gemini-2.0-flash-001",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 8192,
        "tags": ["reasoning", "firebase", "multimodal"],
        "tier": 2,
    },
    # Claude 4 Sonnet — análisis de negocio B2B
    "claude": {
        "id": "anthropic/claude-sonnet-4-5",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 4096,
        "tags": ["business", "b2b", "legal"],
        "tier": 2,
    },
    # DeepSeek R1 vía OpenRouter (fallback si api.deepseek.com cae)
    "deepseek-or": {
        "id": "deepseek/deepseek-r1",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "max_tokens": 4096,
        "tags": ["or_reasoning", "or_structured"],
        "tier": 2,
    },
}

# ─── NIVEL 3: DIRECTO — DEEPSEEK API + GEMINI NATIVO ────────────────────────

DIRECT_MODELS = {
    # DeepSeek nativo — código, matemáticas, RAG técnico
    "deepseek": {
        "id": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1",
        "key_env": "DEEPSEEK_API_KEY",
        "max_tokens": 4096,
        "tags": ["code", "math", "structured_output"],
        "tier": 3,
    },
    "deepseek-r1": {
        "id": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com/v1",
        "key_env": "DEEPSEEK_API_KEY",
        "max_tokens": 4096,
        "tags": ["deep_reasoning", "complex_math"],
        "tier": 3,
    },
    # Gemini nativo Google
    "gemini": {
        "id": "gemini-2.0-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "key_env": "GEMINI_API_KEY",
        "max_tokens": 4096,
        "tags": ["gemini_native", "vision"],
        "tier": 3,
    },
}

# ─── TABLA MAESTRA DE MODELOS ────────────────────────────────────────────────

MODELS = {**GROQ_MODELS, **OPENROUTER_MODELS, **DIRECT_MODELS}

# ─── TABLA DE DESPACHO POR TIPO DE TAREA ────────────────────────────────────
# Prioridad: Groq (veloc.) > OpenRouter (variedad) > Directo (precisión)

DISPATCH_TABLE = {
    # Groq NIVEL 1 — ultra-rápido
    "fast":               "groq-llama",
    "fast_code":          "groq-qwen-coder",
    "fast_reasoning":     "groq-deepseek-r1",
    "multilingual_fast":  "groq-mixtral",
    "chat":               "groq-llama",
    "summarize":          "groq-llama",
    # OpenRouter NIVEL 2 — modelos chinos
    "rag":                "qwen3-max",
    "multilingual":       "qwen3-max",
    "jewelry":            "qwen3-max",
    "latam":              "qwen3-max",
    "long_context":       "kimi",
    "documents":          "kimi",
    "analysis":           "kimi",
    "video_scripts":      "minimax",
    "multimedia_analysis":"minimax",
    "reasoning":          "gemini-or",
    "general":            "gemini-or",
    "firebase":           "gemini-or",
    "business":           "claude",
    "b2b":                "claude",
    "legal":              "claude",
    # Directo NIVEL 3 — precisión
    "code":               "deepseek",
    "math":               "deepseek",
    "structured_output":  "deepseek",
    "deep_reasoning":     "deepseek-r1",
    "complex_math":       "deepseek-r1",
    # Fallback
    "fallback":           "groq-llama",
}

# ─── GUARDRAILS: patrones bloqueados en input ────────────────────────────────

BLOCKED_PATTERNS = [
    r"sk-[a-zA-Z0-9\-]{20,}",
    r"sk-or-v1-[a-zA-Z0-9]{6,}",
    r"AIza[a-zA-Z0-9\-_]{20,}",
    r"\b(?:\d{4}[\s\-]?){4}\b",
    r"password\s*[:=]\s*\S+",
    r"BEGIN (RSA|EC|OPENSSH) PRIVATE",
]

# ─── ROUTER PRINCIPAL ────────────────────────────────────────────────────────

class AIRouter:
    """Router multi-modelo OpenClaw v2.1 — Groq + OpenRouter + Directo."""

    def __init__(self):
        self.session_id = f"ROUTER-{int(time.time())}"
        self._verify_keys()

    def _verify_keys(self):
        """Verifica disponibilidad de keys por tier."""
        tiers_ok = {1: False, 2: False, 3: False}
        missing = []
        checked = set()
        for key, cfg in MODELS.items():
            env_var = cfg["key_env"]
            if env_var not in checked:
                checked.add(env_var)
                val = os.getenv(env_var, "")
                if val and not val.startswith("tu_"):
                    tiers_ok[cfg["tier"]] = True
                else:
                    missing.append(env_var)

        print(f"\n[AI ROUTER v2.1] Session: {self.session_id}")
        print(f"  Tier 1 (Groq):       {'✅ ACTIVO' if tiers_ok[1] else '⚠️  Sin GROQ_API_KEY — registrar en console.groq.com'}")
        print(f"  Tier 2 (OpenRouter): {'✅ ACTIVO' if tiers_ok[2] else '❌ Sin OPENROUTER_API_KEY'}")
        print(f"  Tier 3 (Directo):    {'✅ ACTIVO' if tiers_ok[3] else '⚠️  Sin DeepSeek/Gemini key'}")
        print()

    def select_model(self, task_type: str) -> str:
        """Selecciona el modelo óptimo para el tipo de tarea."""
        model_key = DISPATCH_TABLE.get(task_type, "groq-llama")
        cfg = MODELS[model_key]
        # Si el modelo seleccionado no tiene key, escalar al siguiente tier
        if not os.getenv(cfg["key_env"], ""):
            if cfg["tier"] == 1:
                model_key = "qwen3-max"  # fallback Tier 2
            elif cfg["tier"] == 2:
                model_key = "deepseek"   # fallback Tier 3
        cfg = MODELS[model_key]
        print(f"[ROUTER] Tarea='{task_type}' → Tier {cfg['tier']} → {cfg['id']}")
        return model_key

    def call(
        self,
        prompt: str,
        task_type: str = "general",
        system: Optional[str] = None,
        model_override: Optional[str] = None,
    ) -> dict:
        """
        Llama al modelo óptimo y retorna respuesta estructurada.

        Returns:
            dict: model, response, tokens, latency_ms, success, tier
        """
        t0 = time.time()
        model_key = model_override if model_override else self.select_model(task_type)
        cfg = MODELS.get(model_key)
        if not cfg:
            return {"model": model_key, "response": f"ERROR: Modelo '{model_key}' no encontrado.", "tokens": 0, "latency_ms": 0, "success": False, "tier": 0}

        api_key = os.getenv(cfg["key_env"], "")
        if not api_key or api_key.startswith("tu_"):
            return {
                "model": cfg["id"],
                "response": f"ERROR: Key '{cfg['key_env']}' no configurada. Ver C:\\Users\\ipane\\.openclaw-master.env",
                "tokens": 0,
                "latency_ms": 0,
                "success": False,
                "tier": cfg["tier"],
            }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
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
                timeout=90,
            )
            resp.raise_for_status()
            data = resp.json()

            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
            elif "error" in data:
                err_msg = data["error"].get("message", str(data["error"]))
                raise ValueError(f"Provider Error: {err_msg}")
            else:
                raise ValueError(f"Invalid API response: {str(data)[:200]}")

            tokens = data.get("usage", {}).get("total_tokens", 0)
            latency = int((time.time() - t0) * 1000)

            return {
                "model": cfg["id"],
                "response": content,
                "tokens": tokens,
                "latency_ms": latency,
                "success": True,
                "tier": cfg["tier"],
            }

        except Exception as e:
            # Auto-fallback: Tier 1 falla → Tier 2, Tier 2 falla → Tier 3
            tier = cfg["tier"]
            fallback_map = {1: "qwen3-max", 2: "deepseek", 3: None}
            fallback_key = fallback_map.get(tier)
            if fallback_key and fallback_key != model_key and os.getenv(MODELS[fallback_key]["key_env"], ""):
                print(f"[ROUTER FALLBACK] {cfg['id']} falló ({e}). → {MODELS[fallback_key]['id']}")
                return self.call(prompt, task_type, system, model_override=fallback_key)

            return {
                "model": cfg["id"],
                "response": f"ERROR: {str(e)}",
                "tokens": 0,
                "latency_ms": int((time.time() - t0) * 1000),
                "success": False,
                "tier": tier,
            }

    def print_result(self, result: dict):
        """Imprime el resultado de forma legible."""
        status = "✅ OK" if result["success"] else "❌ FAIL"
        print(f"\n{'─'*65}")
        print(f"{status}  Tier {result.get('tier','?')} — Modelo: {result['model']}")
        print(f"   Tokens: {result['tokens']}  |  Latencia: {result['latency_ms']}ms")
        print(f"   Respuesta:")
        print(f"   {result['response'][:800]}")
        print(f"{'─'*65}")

    def benchmark_all_tiers(self):
        """Test rápido de todos los tiers disponibles."""
        test_prompt = "Responde en una línea: ¿Conectado y funcionando? Incluye tu nombre de modelo."
        tiers_to_test = [
            ("groq-llama",  "Tier 1 — Groq Llama 3.3 70B"),
            ("qwen3-max",   "Tier 2 — Qwen 3.8 Max (OpenRouter)"),
            ("deepseek",    "Tier 3 — DeepSeek V3 (Directo)"),
        ]
        print("\n[BENCHMARK] Test de conectividad multi-tier...\n")
        for model_key, label in tiers_to_test:
            print(f"Testing {label}...")
            result = self.call(test_prompt, model_override=model_key)
            self.print_result(result)


# ─── INSTANCIA GLOBAL ────────────────────────────────────────────────────────

router = AIRouter()


if __name__ == "__main__":
    router.benchmark_all_tiers()
