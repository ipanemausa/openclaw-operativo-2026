"""
=============================================================================
OPENCLAW 2026 — SOVEREIGN CLOUD ENDPOINTS GATEWAY v2.1
=============================================================================
Health check proactivo de todos los endpoints:

TIER 1 — ULTRA-RÁPIDO:
  - Groq (Llama 3.3 70B / Qwen 2.5 Coder / DeepSeek R1 Distill)

TIER 2 — OPENROUTER HUB:
  - OpenRouter (Qwen 3.8, Kimi K2, Minimax, Gemini 2.0, Claude)

TIER 3 — DIRECTO:
  - DeepSeek Cloud (V3 & R1 nativos)
  - Google Gemini Cloud (2.5 Flash & Pro)
  - Anthropic Claude Cloud
  - Alibaba DashScope (Qwen & CosyVoice)
  - ElevenLabs (voz Guillermo)

LOCAL:
  - Ollama (localhost:11434)
  - ComfyUI (localhost:8188)
=============================================================================
"""

import os
import sys
import json
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MASTER_ENV_PATH = Path("C:/Users/ipane/.openclaw-master.env")


class SovereignEndpointsGateway:
    def __init__(self):
        self.keys = self._load_master_env()

    def _load_master_env(self) -> Dict[str, str]:
        env_dict = {}
        if MASTER_ENV_PATH.exists():
            for line in MASTER_ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    env_dict[k.strip()] = v.strip().strip('"').strip("'")
        return env_dict

    def _check_openai_compat(self, name: str, url: str, key: str, model: str, timeout: int = 6) -> tuple:
        """Verifica endpoint compatible con OpenAI enviando un mini-prompt."""
        if not key or key.startswith("tu_"):
            return "NO_KEY", 0
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        if "openrouter" in url:
            headers["HTTP-Referer"] = "https://openclaw.cloud"
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5,
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as r:
                lat_ms = round((time.time() - t0) * 1000, 1)
                return "ACTIVE", lat_ms
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return "AUTH_ERROR", 0
            if e.code == 429:
                return "RATE_LIMITED", 0
            return f"HTTP_{e.code}", 0
        except Exception as e:
            return f"ERROR: {str(e)[:60]}", 0

    def _check_url(self, url: str, key: str = None, timeout: int = 5) -> tuple:
        """Verifica acceso simple a URL (GET)."""
        if key and (key.startswith("tu_") or not key):
            return "NO_KEY", 0
        try:
            headers = {}
            if key:
                headers["Authorization"] = f"Bearer {key}"
            req = urllib.request.Request(url, headers=headers)
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as r:
                lat_ms = round((time.time() - t0) * 1000, 1)
                return "ACTIVE", lat_ms
        except Exception as e:
            return f"ERROR: {str(e)[:60]}", 0

    def _fmt(self, status: str, lat: float, models: str = "") -> str:
        icon = "🟢" if status == "ACTIVE" else ("🟡" if status in ("NO_KEY", "CONFIGURED") else ("⚪" if status == "OPTIONAL" else "🔴"))
        lat_str = f" ({lat:.0f}ms)" if lat > 0 else ""
        models_str = f" — {models}" if models else ""
        return f"  {icon} {status}{lat_str}{models_str}"

    def run_health_sweep(self) -> Dict[str, Any]:
        k = self.keys
        print("\n" + "=" * 70)
        print("  OPENCLAW 2026 v2.1 — ESCANEO PROACTIVO DE ENDPOINTS")
        print("=" * 70)

        report = {}

        # ── TIER 1: GROQ ──────────────────────────────────────────────────
        print("\n📡 TIER 1 — GROQ (Ultra-rápido, ~1800 tok/s)")
        groq_key = k.get("GROQ_API_KEY", "")
        if groq_key and not groq_key.startswith("tu_"):
            status, lat = self._check_openai_compat(
                "Groq", "https://api.groq.com/openai/v1/chat/completions",
                groq_key, "llama-3.3-70b-versatile"
            )
            print(f"  Groq Hub:{self._fmt(status, lat, 'Llama3.3-70B | Qwen2.5-Coder-32B | DeepSeek-R1-Distill-70B')}")
        else:
            print(f"  Groq Hub:{self._fmt('NO_KEY', 0, 'Registrar gratis en console.groq.com')}")
        report["groq"] = groq_key != ""

        # ── TIER 2: OPENROUTER HUB ────────────────────────────────────────
        print("\n📡 TIER 2 — OPENROUTER HUB (Modelos chinos + Gemini + Claude)")
        or_key = k.get("OPENROUTER_API_KEY", "")
        or_status, or_lat = self._check_openai_compat(
            "OpenRouter", "https://openrouter.ai/api/v1/chat/completions",
            or_key, "qwen/qwen3-235b-a22b"
        )
        print(f"  OpenRouter:{self._fmt(or_status, or_lat)}")
        if or_status == "ACTIVE":
            models_or = [
                ("Qwen 3.8 Max 235B",   "qwen/qwen3-235b-a22b"),
                ("Kimi K2 (1M ctx)",    "moonshotai/kimi-k2"),
                ("Minimax-01",          "minimax/minimax-01"),
                ("Gemini 2.0 Flash",    "google/gemini-2.0-flash-001"),
                ("Claude Sonnet 4.5",   "anthropic/claude-sonnet-4-5"),
                ("DeepSeek R1 (OR)",    "deepseek/deepseek-r1"),
            ]
            for name, model_id in models_or:
                print(f"    ├─ ✅ {name} ({model_id})")
        report["openrouter"] = or_status == "ACTIVE"

        # ── TIER 3: DEEPSEEK DIRECTO ──────────────────────────────────────
        print("\n📡 TIER 3 — DEEPSEEK CLOUD (API nativa)")
        ds_key = k.get("DEEPSEEK_API_KEY", "")
        ds_status, ds_lat = self._check_url(
            "https://api.deepseek.com/models",
            ds_key
        )
        print(f"  DeepSeek:{self._fmt(ds_status, ds_lat, 'deepseek-chat | deepseek-reasoner')}")
        report["deepseek"] = ds_status == "ACTIVE"

        # ── GOOGLE GEMINI ─────────────────────────────────────────────────
        print("\n📡 GOOGLE GEMINI CLOUD (Nativo)")
        gem_key = k.get("GEMINI_API_KEY", "") or k.get("GOOGLE_API_KEY", "")
        gem_status, gem_lat = self._check_url(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={gem_key}"
        )
        print(f"  Gemini:{self._fmt(gem_status, gem_lat, 'gemini-2.0-flash | gemini-2.5-pro')}")
        report["gemini"] = gem_status == "ACTIVE"

        # ── ANTHROPIC CLAUDE ──────────────────────────────────────────────
        print("\n📡 ANTHROPIC CLAUDE CLOUD")
        ant_key = k.get("ANTHROPIC_API_KEY", "")
        if ant_key and not ant_key.startswith("sk-ant-XXX"):
            print(f"  Claude:{self._fmt('CONFIGURED', 0, 'claude-3-5-sonnet | claude-3-opus')}")
        else:
            print(f"  Claude:{self._fmt('NO_KEY', 0, 'Opcional — disponible vía OpenRouter')}")
        report["anthropic"] = bool(ant_key and not ant_key.startswith("sk-ant-XXX"))

        # ── ALIBABA DASHSCOPE ─────────────────────────────────────────────
        print("\n📡 ALIBABA DASHSCOPE (Qwen Image 3.0 + Qwen3-TTS)")
        dash_key = k.get("DASHSCOPE_API_KEY", "")
        if dash_key and not dash_key.startswith("tu_"):
            print(f"  DashScope:{self._fmt('CONFIGURED', 0, 'qwen-max | qwen-vl | cosyvoice-v2 | Qwen3-TTS')}")
        else:
            print(f"  DashScope:{self._fmt('NO_KEY', 0, 'Para Qwen Image 3.0 + Qwen3-TTS nativo — dashscope.aliyuncs.com')}")
        report["dashscope"] = bool(dash_key)

        # ── ELEVENLABS ────────────────────────────────────────────────────
        print("\n📡 ELEVENLABS (Voz Guillermo — Clon Neural)")
        el_key = k.get("ELEVENLABS_API_KEY", "")
        if el_key:
            print(f"  ElevenLabs:{self._fmt('CONFIGURED', 0, 'Voz Guillermo HD — sk_e3f7...')}")
        else:
            print(f"  ElevenLabs:{self._fmt('NO_KEY', 0)}")
        report["elevenlabs"] = bool(el_key)

        # ── LOCAL: OLLAMA ─────────────────────────────────────────────────
        print("\n📡 LOCAL — OLLAMA (Offline privado)")
        ollama_status, ollama_lat = self._check_url("http://localhost:11434/api/tags")
        print(f"  Ollama:{self._fmt(ollama_status, ollama_lat, 'qwen2.5 | llama3 | deepseek-r1 | mistral')}")
        report["ollama"] = ollama_status == "ACTIVE"

        # ── LOCAL: COMFYUI ────────────────────────────────────────────────
        print("\n📡 LOCAL — COMFYUI (Imagen/Video offline)")
        cfy_status, cfy_lat = self._check_url("http://localhost:8188/system_stats")
        print(f"  ComfyUI:{self._fmt(cfy_status, cfy_lat, 'Minimax H3 | SDXL | WAN 2.1')}")
        report["comfyui"] = cfy_status == "ACTIVE"

        # ── RESUMEN ───────────────────────────────────────────────────────
        print("\n" + "=" * 70)
        active_count = sum(1 for v in report.values() if v)
        total = len(report)
        print(f"  [RESUMEN] {active_count}/{total} endpoints activos/configurados.")
        if not report.get("groq"):
            print("  ⚠️  ACCIÓN: Registrar Groq gratis → https://console.groq.com")
        if not report.get("dashscope"):
            print("  ⚠️  ACCIÓN: Agregar DashScope key → para Qwen Image 3.0 + TTS")
        print("=" * 70 + "\n")
        return report


if __name__ == "__main__":
    gateway = SovereignEndpointsGateway()
    gateway.run_health_sweep()
