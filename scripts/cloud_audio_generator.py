"""
=============================================================================
OPENCLAW 2026 — CLOUD GPU NEURAL AUDIO SYNTHESIZER
=============================================================================
Ejecuta la síntesis directamente en la infraestructura GPU en la nube
sin dependencias de compilación local en Windows.
=============================================================================
"""

import os
import sys
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "audio"
AUDIO_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = AUDIO_DIR / "DISCURSO_MAESTRO_GUILLERMO_CLOUD_GPU.mp3"

env_file = Path("C:/Users/ipane/.openclaw-master.env")
env_dict = {}
for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env_dict[k.strip()] = v.strip().strip('"').strip("'")

openai_key = env_dict.get("OPENAI_API_KEY", "")

TEXT = (
    "Esta es una prueba de la arquitectura soberana de OpenClaw 2026. "
    "El verdadero valor de la inteligencia artificial no está en vender suscripciones menores de veinte dólares, "
    "sino en la investigación profunda, la biotecnología y la infraestructura que transforma industrias enteras. "
    "El código abierto y la factorización matemática superan cualquier barrera."
)

def synthesize_on_cloud_gpu():
    print("=" * 65)
    print("  OPENCLAW 2026 — SÍNTESIS NEURAL EN CLOUD GPU (NUBE)")
    print("=" * 65)
    print(f"[*] Enviando texto a cluster de GPU en la nube...")
    print(f"[*] Texto:\n    \"{TEXT}\"\n")

    payload = {
        "model": "tts-1-hd",
        "input": TEXT,
        "voice": "onyx",  # Barítono profundo de alta definición
        "response_format": "mp3",
        "speed": 0.95
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload).encode("utf-8")
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            audio_data = response.read()
            with open(OUTPUT_FILE, "wb") as f:
                f.write(audio_data)
            
            print(f"[ÉXITO TOTAL] Audio sintetizado en Cloud GPU y guardado en:")
            print(f"👉 {OUTPUT_FILE}")
            print(f"Tamaño: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")
            return OUTPUT_FILE
    except Exception as e:
        print(f"[ERROR] Falló la síntesis en nube: {e}")
        sys.exit(1)

if __name__ == "__main__":
    synthesize_on_cloud_gpu()
