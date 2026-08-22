"""
==============================================================================
OPENCLAW 2026 — MASTERIZADOR Y ECUALIZADOR DE VOZ REAL DE GUILLERMO
==============================================================================
Aplica cadena de masterización acústica profesional FM Broadcast:
- High-Pass Filter (80Hz) anti-rumble
- Ecualización Paramétrica (Cálida, Presencia 3.5kHz y Brillo 10kHz)
- Compresión Dinámica Multibanda (Voz con autoridad y cercanía)
- Normalización EBU R128 (-16 LUFS EBU R128 / -1.5 dB TP)
- Formato: 48kHz Stereo AAC / WAV
==============================================================================
"""

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_VOICE = ROOT / "runtime" / "guillermo_voice_tiktok_raw.mp3"
MASTERED_VOICE = ROOT / "runtime" / "guillermo_voice_studio_master_48k.aac"
MASTERED_WAV = ROOT / "runtime" / "guillermo_voice_studio_master_48k.wav"

def master_guillermo_voice():
    print("=" * 60)
    print("  [VOICE] MASTERIZANDO Y ECUALIZANDO VOZ REAL DE GUILLERMO")
    print("=" * 60)

    if not RAW_VOICE.exists():
        print(f"[ERROR] Archivo no encontrado: {RAW_VOICE}")
        return False

    # Cadena de filtros FFmpeg para calidad de locutor de radio FM
    # 1. highpass: corta frecuencias subgraves menores a 80Hz
    # 2. equalizer: realce de graves cálidos (220Hz, +2.5dB), reducción de caja (500Hz, -2dB), realce de presencia (3500Hz, +3.5dB), brillo aéreo (10000Hz, +2dB)
    # 3. compand: compresor de estudio para dar consistencia y autoridad
    # 4. loudnorm: estándar internacional EBU R128 a -16 LUFS
    eq_chain = (
        "highpass=f=80,"
        "equalizer=f=220:t=q:w=1.2:g=2.5,"
        "equalizer=f=500:t=q:w=1.5:g=-2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=3.5,"
        "equalizer=f=10000:t=q:w=1.0:g=2.0,"
        "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
        "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(RAW_VOICE),
        "-af", eq_chain,
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-ac", "2",
        str(MASTERED_VOICE)
    ]
    
    cmd_wav = [
        "ffmpeg", "-y",
        "-i", str(RAW_VOICE),
        "-af", eq_chain,
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        "-ac", "2",
        str(MASTERED_WAV)
    ]

    print("-> Aplicando filtros de masterización acústica...")
    subprocess.run(cmd, check=True)
    subprocess.run(cmd_wav, check=True)

    print("\n" + "=" * 60)
    print("  [OK] VOZ REAL DE GUILLERMO MASTERIZADA CON EXITO")
    print(f"  Archivo AAC: {MASTERED_VOICE}")
    print(f"  Archivo WAV: {MASTERED_WAV}")
    print("  Estándar:    48.000 Hz Stereo · 256 kbps · -16 LUFS EBU R128")
    print("  Acústica:    Cálida, Autoridad Profesional, Accesible y Nítida")
    print("=" * 60)

    return True

if __name__ == "__main__":
    master_guillermo_voice()
