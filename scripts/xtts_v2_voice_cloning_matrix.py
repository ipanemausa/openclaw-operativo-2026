"""
==============================================================================
OPENCLAW 2026 — MOTOR STANDALONE DE CLONACIÓN DE VOZ XTTS-v2 (GPU NVIDIA)
==============================================================================
"""

import os
import sys
import subprocess
from pathlib import Path
import torch

try:
    from TTS.api import TTS
except ImportError:
    TTS = None

ROOT = Path(__file__).parent.parent
AUDIO_DIR = ROOT / "runtime" / "voice_clone_xtts"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
REFERENCE_VOICE = ROOT / "audio" / "guillermo_voice_reference.wav"

def init_xtts_model():
    """Inicializa el modelo XTTS-v2 en GPU NVIDIA si está disponible."""
    if TTS is None:
        print("[ERROR] Coqui TTS no está instalado. Ejecuta: pip install coqui-tts")
        sys.exit(1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n[INIT] Inicializando XTTS-v2 en dispositivo: {device.upper()}")
    if device == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        print(f"       GPU Detectada: {gpu_name} (VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB)")
    else:
        print("       [WARN] GPU no detectada, ejecutando en CPU.")

    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    return tts

def clone_voice_speech(tts_engine, text: str, output_name: str, language: str = "es") -> Path:
    """Clona la voz de Guillermo a partir del texto y la muestra de referencia."""
    raw_wav = AUDIO_DIR / f"{output_name}_raw.wav"
    master_aac = AUDIO_DIR / f"{output_name}_master_48k.aac"

    print(f"\n[SINTESIS] Generando audio en [{language.upper()}]: '{text[:60]}...'")
    
    tts_engine.tts_to_file(
        text=text,
        speaker_wav=str(REFERENCE_VOICE),
        language=language,
        file_path=str(raw_wav)
    )

    eq_chain = (
        "highpass=f=80,"
        "equalizer=f=220:t=q:w=1.2:g=2.5,"
        "equalizer=f=3500:t=q:w=1.0:g=3.0,"
        "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
        "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(raw_wav),
        "-af", eq_chain,
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        str(master_aac)
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"  [OK] Master Broadcast Generado: {master_aac}")
    return master_aac

if __name__ == "__main__":
    if TTS is None:
        print("[AVISO] Para ejecutar XTTS-v2 con tu GPU NVIDIA, instala: pip install coqui-tts")
    else:
        engine = init_xtts_model()
        test_text = "Bienvenidos a OpenClaw 2026. Esta es mi voz real clonada con el motor XTTS en GPU NVIDIA."
        if REFERENCE_VOICE.exists():
            clone_voice_speech(engine, test_text, "test_guillermo_voice", language="es")
        else:
            print(f"[INFO] Coloca tu archivo de voz de 15 segundos en: {REFERENCE_VOICE}")
