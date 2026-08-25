"""
==============================================================================
HB.OS 2026 — RE-ENSAMBLAJE DE VIDEO HD CON NARRACIÓN EXPRESIVA VIVA
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
RUNTIME_VIDEO = ROOT / "runtime" / "productions" / "guillermo_authentic_hd_masterpiece"
AUDIO_EXPRESSIVE = ROOT / "runtime" / "productions" / "guillermo_expressive_voice" / "GUILLERMO_EXPRESSIVE_VOICE_MASTER_48K.mp3"

FINAL_EXPRESSIVE_VIDEO = RUNTIME_VIDEO / "GUILLERMO_HOYOS_HBOS_EXPRESSIVE_HD_1080P.mp4"
FRAMES_DIR = RUNTIME_VIDEO / "frames"

def reassemble_video():
    print("=" * 80)
    print("  🎬 RE-ENSAMBLANDO VIDEO FULL HD 1080P CON NARRACIÓN EXPRESIVA VIVA")
    print("=" * 80)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", "25",
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_EXPRESSIVE),
        "-shortest",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(FINAL_EXPRESSIVE_VIDEO)
    ]

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\n🏆 [ÉXITO TOTAL] Video HD Expresivo Generado:")
        print(f"   Archivo: {FINAL_EXPRESSIVE_VIDEO}")
    else:
        print(f"[!] FFmpeg Error: {res.stderr}")

if __name__ == "__main__":
    reassemble_video()
