"""
=============================================================================
OPENCLAW 2026 — PRUEBA REAL DE VOZ CLONADA (GUILLERMO HOYOS)
=============================================================================
Genera un archivo de audio real (.wav y .mp3) clonando la voz de Guillermo
a partir de su referencia acústica ('audio/guillermo_voice_reference.wav')
usando el modelo Zero-Shot XTTS-v2 con post-procesamiento DSP EBU R128 (-16 LUFS).
=============================================================================
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "audio"
REFERENCE_VOICE = AUDIO_DIR / "guillermo_voice_reference.wav"
OUTPUT_RAW = AUDIO_DIR / "PRUEBA_VOZ_GUILLERMO_RAW.wav"
OUTPUT_MASTER = AUDIO_DIR / "PRUEBA_VOZ_GUILLERMO_MASTER_16LUFS.mp3"

TEXT_TO_SYNTHESIZE = (
    "Esta es una prueba real y directa de mi voz, Guillermo Hoyos, "
    "procesada bajo la arquitectura soberana de OpenClaw 2026. "
    "El valor de la inteligencia artificial no está en vender suscripciones menores de veinte dólares, "
    "sino en la investigación profunda, la biotecnología y la infraestructura que transforma industrias enteras. "
    "Hoy demostramos que el código abierto y la factorización matemática superan cualquier barrera."
)

def run_voice_synthesis():
    print("=" * 65)
    print("  OPENCLAW 2026 — SÍNTESIS DIRECTA DE VOZ (GUILLERMO HOYOS)")
    print("=" * 65)
    print(f"[*] Archivo de referencia: {REFERENCE_VOICE}")
    print(f"[*] Texto a sintetizar:\n    \"{TEXT_TO_SYNTHESIZE}\"\n")

    if not REFERENCE_VOICE.exists():
        print(f"[ERROR] No se encontró el archivo de referencia: {REFERENCE_VOICE}")
        sys.exit(1)

    try:
        # Desactivar chequeo estricto de versión de tokenizers en transformers
        import transformers.utils.versions
        transformers.utils.versions.require_version_core = lambda *args, **kwargs: None
        import transformers.dependency_versions_check
        transformers.dependency_versions_check.require_version_core = lambda *args, **kwargs: None

        from TTS.api import TTS
        print("[*] Cargando modelo neural de clonación XTTS-v2...")
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[*] Dispositivo de inferencia: {device.upper()}")

        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("[*] Sintetizando fonemas con la huella acústica de Guillermo...")
        
        tts.tts_to_file(
            text=TEXT_TO_SYNTHESIZE,
            speaker_wav=str(REFERENCE_VOICE),
            language="es",
            file_path=str(OUTPUT_RAW)
        )
        print(f"[OK] Audio crudo generado: {OUTPUT_RAW}")

        # Masterización DSP Broadcast EBU R128 (-16 LUFS)
        print("[*] Aplicando masterización DSP (48kHz, -16 LUFS, EQ Barítono)...")
        eq_filter = (
            "highpass=f=80,"
            "equalizer=f=220:t=q:w=1.2:g=2.5,"
            "equalizer=f=3500:t=q:w=1.0:g=3.0,"
            "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
            "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(OUTPUT_RAW),
            "-af", eq_filter,
            "-c:a", "libmp3lame", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(OUTPUT_MASTER)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"\n[ÉXITO TOTAL] Master de audio generado en:")
        print(f"👉 {OUTPUT_MASTER}")
        print(f"Tamaño: {OUTPUT_MASTER.stat().st_size / 1024:.2f} KB")

    except Exception as e:
        print(f"[ERROR] Error durante la síntesis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_voice_synthesis()
