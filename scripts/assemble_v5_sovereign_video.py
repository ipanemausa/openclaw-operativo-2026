"""
==============================================================================
HB.OS 2026 — MASTERCLASS V5.0 SOBERANA (VOZ REAL GRABADA + CERO LOGINS)
==============================================================================
"""

import os
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
RUNTIME_V4 = ROOT / "runtime" / "productions" / "guillermo_real_voice_masterclass_v4"
RUNTIME_V5 = ROOT / "runtime" / "productions" / "guillermo_sovereign_masterpiece_v5"
RUNTIME_V5.mkdir(parents=True, exist_ok=True)

SOVEREIGN_AUDIO = ROOT / "runtime" / "productions" / "sovereign_local_voice" / "GUILLERMO_SOVEREIGN_AUTHENTIC_VOICE_48K.wav"
FINAL_V5_VIDEO = RUNTIME_V5 / "GUILLERMO_HOYOS_HBOS_SOVEREIGN_MASTERPIECE_V5_1080P.mp4"
FRAMES_DIR = RUNTIME_V4 / "frames"

def assemble_v5_sovereign():
    print("=" * 80)
    print("  🛡️ ENSAMBLANDO MASTERCLASS V5.0 SOBERANA CON TU VOZ REAL GRABADA PURA")
    print("=" * 80)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", "25",
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(SOVEREIGN_AUDIO),
        "-shortest",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(FINAL_V5_VIDEO)
    ]

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\n🏆 [ÉXITO SOBERANO TOTAL] Video V5.0 Generado:")
        print(f"   Archivo: {FINAL_V5_VIDEO}")
        print(f"   Audio: Voz Real Auténtica Grabada de Guillermo Hoyos (Cero Logins Externos)")
    else:
        print(f"[!] FFmpeg Error: {res.stderr}")

if __name__ == "__main__":
    assemble_v5_sovereign()
