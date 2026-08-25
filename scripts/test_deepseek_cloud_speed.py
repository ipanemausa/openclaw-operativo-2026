"""
=============================================================================
OPENCLAW 2026 — DEEPSEEK CLOUD REASONING BENCHMARK & LATENCY TEST
=============================================================================
Ejecuta una tarea de razonamiento directamente en los servidores de DeepSeek
midiendo la latencia en milisegundos y la tasa de generación de tokens.
=============================================================================
"""

import os
import sys
import json
import time
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

env_file = Path("C:/Users/ipane/.openclaw-master.env")
env_dict = {}
for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env_dict[k.strip()] = v.strip().strip('"').strip("'")

deepseek_key = env_dict.get("DEEPSEEK_API_KEY", "")

PROMPT = (
    "Sintetiza en 3 oraciones de alto impacto por qué la arquitectura de atención "
    "MLA (Multi-Head Latent Attention) y el código abierto superan en costo y velocidad a los modelos monolíticos cerrados."
)

def benchmark_deepseek_cloud():
    print("=" * 65)
    print("  OPENCLAW 2026 — BENCHMARK EN LA NUBE (DEEPSEEK CLOUD)")
    print("=" * 65)
    print(f"[*] Endpoint: https://api.deepseek.com/chat/completions")
    print(f"[*] Modelo: deepseek-chat (DeepSeek-V3)")
    print(f"[*] Enviando prompt a la nube...\n")

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres el núcleo de razonamiento soberano de OpenClaw HB.OS."},
            {"role": "user", "content": PROMPT}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {deepseek_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload).encode("utf-8")
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            t1 = time.time()
            elapsed_ms = (t1 - t0) * 1000
            res = json.loads(response.read().decode("utf-8"))
            
            content = res["choices"][0]["message"]["content"]
            usage = res.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            
            print(f"[ÉXITO TOTAL — INFERENCIA CLOUD EN TIEMPO RÉCORD]")
            print(f"⚡ Latencia Total: {elapsed_ms:.2f} ms ({elapsed_ms/1000:.2f} segundos)")
            print(f"⚡ Tokens Generados: {total_tokens} tokens")
            print(f"⚡ Velocidad: {total_tokens / (elapsed_ms/1000):.1f} tokens/segundo\n")
            print("--- RESPUESTA DE DEEPSEEK DESDE LA NUBE ---")
            print(content)
            print("------------------------------------------")

    except Exception as e:
        print(f"[ERROR] Error al consultar DeepSeek: {e}")

if __name__ == "__main__":
    benchmark_deepseek_cloud()
