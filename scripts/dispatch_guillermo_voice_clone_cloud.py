"""
==============================================================================
OPENCLAW 2026 — CLOUD NEURAL VOICE CLONING DISPATCH ENGINE (GUILLERMO)
==============================================================================
- Entrada: Muestra acústica de Guillermo (48kHz WAV PCM)
- Endpoint: ElevenLabs Instant Voice Cloning / Cloud Neural API
- Idiomas: Español (ES), English (EN), 中文 Mandarín (ZH)
- Salida: Audio Master con el Timbre e Identidad Exacta de Guillermo
==============================================================================
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

SAMPLE_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
OUTPUT_DIR = ROOT / "runtime" / "guillermo_neural_voice_clone"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()

def clone_and_synthesize_trilingual(text_es: str, text_en: str, text_zh: str):
    print("=" * 75)
    print("  🧠 OPENCLAW — DISPARO DE CLONACIÓN NEURAL ZERO-SHOT (CLOUD GPU)")
    print("=" * 75)

    if not ELEVENLABS_KEY:
        print("❌ [BLOQUEO DE SEGURIDAD] ELEVENLABS_API_KEY no encontrada en .env")
        print("\n-> Para disparar la clonación neuronal real:")
        print("   1. Agrega tu clave en: C:\\Users\\ipane\\.openclaw-master.env")
        print("      ELEVENLABS_API_KEY=tu_api_key_aqui")
        print("   2. Ejecuta: powershell -File .\\scripts\\sync-master-env.ps1")
        print("   3. Vuelve a ejecutar este script.")
        print("=" * 75)
        return False

    headers = {
        "xi-api-key": ELEVENLABS_KEY
    }

    # 1. Verificar o crear la voz clonada de Guillermo
    print("\n[FASE 1/3] Consultando voces registradas en el endpoint neural...")
    res = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    
    if res.status_code != 200:
        print(f"❌ Error consultando endpoint ElevenLabs: HTTP {res.status_code} - {res.text}")
        return False

    voices = res.json().get("voices", [])
    guillermo_voice_id = None

    for v in voices:
        if "Guillermo" in v.get("name", ""):
            guillermo_voice_id = v["voice_id"]
            print(f"  ✓ Voz de Guillermo encontrada: ID = {guillermo_voice_id}")
            break

    # Si no existe, crear el clon instantáneo con la muestra de audio
    if not guillermo_voice_id:
        print(f"\n[FASE 2/3] Subiendo muestra de audio ({SAMPLE_AUDIO.name}) para clonación biométrica...")
        with open(SAMPLE_AUDIO, "rb") as f:
            files = {
                "files": (SAMPLE_AUDIO.name, f, "audio/wav")
            }
            data = {
                "name": "Guillermo_OpenClaw_Founder",
                "description": "Voz oficial de Guillermo para Masterclasses OpenClaw B2B (Barítono Cálido)"
            }
            res_clone = requests.post("https://api.elevenlabs.io/v1/voices/add", headers=headers, data=data, files=files)
            
            if res_clone.status_code != 200:
                print(f"❌ Error creando clon de voz: HTTP {res_clone.status_code} - {res_clone.text}")
                return False
                
            guillermo_voice_id = res_clone.json().get("voice_id")
            print(f"  🎉 ¡Voz Clonada con Éxito! Nuevo Voice ID: {guillermo_voice_id}")

    # 2. Sintetizar en los 3 idiomas con la voz clonada
    print("\n[FASE 3/3] Sintetizando Masterclass en los 3 idiomas con TU VOZ CLONADA...")
    
    languages = [
        ("es", text_es, "eleven_multilingual_v2"),
        ("en", text_en, "eleven_multilingual_v2"),
        ("zh", text_zh, "eleven_multilingual_v2")
    ]

    for lang, text, model_id in languages:
        print(f"\n  -> Sintetizando [{lang.upper()}] con tu voz...")
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{guillermo_voice_id}"
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.65,
                "similarity_boost": 0.90,  # Máxima fidelidad a tu timbre
                "style": 0.20,
                "use_speaker_boost": True
            }
        }
        
        t0 = time.time()
        res_tts = requests.post(tts_url, json=payload, headers=headers)
        elapsed = time.time() - t0

        if res_tts.status_code == 200:
            out_path = OUTPUT_DIR / f"Guillermo_Voice_Clone_{lang.upper()}.mp3"
            with open(out_path, "wb") as f_out:
                f_out.write(res_tts.content)
            print(f"    ✓ Audio [{lang.upper()}] generado en {elapsed:.2f}s -> {out_path} ({len(res_tts.content)/1024:.1f} KB)")
        else:
            print(f"    ❌ Error generando audio [{lang.upper()}]: HTTP {res_tts.status_code} - {res_tts.text}")

    print("\n" + "=" * 75)
    print("  🏆 CLONACIÓN Y SÍNTESIS CONCLUIDA EXITOSAMENTE")
    print("=" * 75)
    return True

if __name__ == "__main__":
    test_es = "Hola, soy Guillermo. Bienvenidos a la Masterclass de Inteligencia Artificial Soberana de OpenClaw."
    test_en = "Hello, I am Guillermo. Welcome to the OpenClaw Sovereign Artificial Intelligence Masterclass."
    test_zh = "你好，我是吉列尔莫。欢迎来到OpenClaw主权人工智能大师班。"
    clone_and_synthesize_trilingual(test_es, test_en, test_zh)
