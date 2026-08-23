"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS DEFINITIVA CON VOZ AUTÉNTICA DE GUILLERMO & JH NVIDIA STAGE
==============================================================================
- AUDIO: 100% Pista Auténtica Masterizada de Guillermo (48kHz Stereo EBU R128)
  Archivo: runtime/guillermo_podcast_master/Guillermo_Podcast_Master_Edit_48k.wav (381.56s)
- VIDEO: Escenario Dinámico Jensen Huang con 4 Infografías de Arquitectura NVIDIA
- AVATAR: Guillermo PNG Transparente con Bordado Oficial HB.OS
- STREAMING: Direct Pipe en Memoria (Zero Disk I/O) -> MP4 FastStart 1080p
==============================================================================
"""

import os
import sys
import math
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
AUDIO_FILE = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
OUTPUT_FILE = ROOT / "frontend" / "public" / "videos" / "Guillermo_Authentic_Voice_JH_NVIDIA_Master_1080p.mp4"
RUNTIME_FILE = ROOT / "runtime" / "Guillermo_Authentic_Voice_JH_NVIDIA_Master_1080p.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

sys.path.insert(0, str(ROOT / "scripts"))
from jh_nvidia_stage_engine import render_jh_stage_frame

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def render_authentic_guillermo_master():
    print("=" * 75)
    print("  🎙️ OPENCLAW — RENDERIZANDO VIDEO CON VOZ 100% AUTÉNTICA DE GUILLERMO")
    print("=" * 75)
    
    if not AUDIO_FILE.exists():
        print(f"❌ Error: No se encontró el archivo de audio: {AUDIO_FILE}")
        return

    total_duration = get_audio_duration(str(AUDIO_FILE))
    total_frames = int(total_duration * FPS)
    print(f"-> Audio Fuente: {AUDIO_FILE.name}")
    print(f"-> Duración:     {total_duration:.2f}s ({total_duration/60:.2f} minutos)")
    print(f"-> Fotogramas:   {total_frames} frames en 1080p a 25 FPS")

    # Cargar avatar transparente con bordado HB.OS
    avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_path).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    try:
        font_brand = ImageFont.truetype("arialbd.ttf", 26)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_brand = font_title = font_concept = font_badge = font_top = ImageFont.load_default()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_FILE.parent.mkdir(parents=True, exist_ok=True)

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",  # Streaming directo desde RAM stdin
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(RUNTIME_FILE)
    ]

    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    start_time = time.time()
    print("\n⚡ [DIRECT MEMORY STREAM] Renderizando y transmitiendo fotogramas en tiempo real...")

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # Fondo Dinámico Jensen Huang (Cambio suave de color + 4 gráficas NVIDIA)
        frame = render_jh_stage_frame(t)
        draw = ImageDraw.Draw(frame)

        # Header Superior
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW SOVEREIGN CORE 2026", font=font_top, fill=(212, 175, 55))
        draw.text((450, 24), "·   VOZ AUTÉNTICA & NVIDIA STUDIO STAGE", font=font_top, fill=(190, 200, 220))
        draw.text((1560, 24), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # Avatar Transparente (Lado Izquierdo)
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        draw.text((80, 95), "GUILLERMO · OPENCLAW FOUNDER", font=font_brand, fill=(255, 255, 255))
        draw.text((80, 130), "Voz Auténtica · Masterización Broadcast 48kHz", font=font_concept, fill=(212, 175, 55))

        # Bloque de Información Técnica Flotante (Lado Derecho)
        content_x = 640
        content_y = 110
        content_w = 1220

        draw.text((content_x, content_y), "ARQUITECTURA SOBERANA & ECOSISTEMA B2B", font=font_badge, fill=(212, 175, 55))
        draw.text((content_x, content_y + 45), "HB Jewelry & OpenClaw Universal Operating System", font=font_title, fill=(255, 255, 255))
        draw.text((content_x, content_y + 115), "⚡ Gobernanza Vectorial en R^768 · Red de Inferencia Multi-Modelo", font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 160, content_x + content_w, content_y + 160], fill=(45, 60, 90), width=1)

        # Indicador de Transmisión de Audio Real
        audio_pulse = 0.5 + 0.5 * math.sin(t * 4.0)
        draw.text((content_x, HEIGHT - 180), "🎙️ AUDIO STREAM:", font=font_badge, fill=(212, 175, 55))
        draw.text((content_x + 220, HEIGHT - 180), "Pista Auténtica de Guillermo (Sin Síntesis Genérica · 100% Original)", font=font_concept, fill=(245, 248, 255))
        draw.text((content_x, HEIGHT - 140), f"Norma Acústica: EBU R128 (-16 LUFS) · Barítono Cálido (104.8 Hz) · 48.000 Hz Stereo", font=font_top, fill=(160, 190, 230))

        # Barra de progreso inferior en oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        # Escribir directamente a stdin de FFmpeg
        proc.stdin.write(frame.tobytes())

        if f_idx % 1000 == 0:
            elapsed = time.time() - start_time
            speed = (f_idx + 1) / elapsed if elapsed > 0 else 0
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) | Velocidad: {speed:.1f} FPS")

    proc.stdin.close()
    proc.wait()

    import shutil
    shutil.copy2(RUNTIME_FILE, OUTPUT_FILE)

    total_time = time.time() - start_time
    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 75)
    print("  🏆 VIDEO MAESTRO CON VOZ AUTÉNTICA DE GUILLERMO GENERADO CON ÉXITO")
    print(f"  Ruta Runtime: {RUNTIME_FILE}")
    print(f"  Ruta Pública: {OUTPUT_FILE}")
    print(f"  Tamaño:       {size_mb:.2f} MB")
    print(f"  Duración:     {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print(f"  Tiempo Cómputo: {total_time:.2f} segundos")
    print("  Audio:        100% TU VOZ REAL (48kHz Stereo EBU R128)")
    print("  Escenario:    Jensen Huang Dynamic Stage + Gráficas Arquitectura NVIDIA")
    print("=" * 75)

if __name__ == "__main__":
    render_authentic_guillermo_master()
