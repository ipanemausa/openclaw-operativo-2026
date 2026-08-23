"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS TRILINGÜE DEFINITIVA JENSEN HUANG NVIDIA STAGE
==============================================================================
Genera las 3 Masterclasses en 1080p FastStart en los 3 Idiomas:
  1. Español (Acento Colombiano Barítono - Perfil Guillermo)
  2. English (Oxford / Silicon Valley Executive B2B)
  3. 中文 Mandarín (Alibaba Cloud / Sovereign AI Matrix)

Incorpora en las 3 versiones:
  - Escenario Dinámico Jensen Huang con transición lumínica y cromática
  - 4 Infografías de Arquitectura NVIDIA integradas en el fondo
  - Pistas de Audio Calibradas bajo norma EBU R128 (-16 LUFS / 48kHz Stereo)
  - Avatar Transparente con bordado HB.OS integrado en escena completa
  - Teleprompter Dinámico en Oro (54pt) con sombra suave
==============================================================================
"""

import os
import sys
import math
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_trilingue_jh_2026"
PUBLIC_DIR = ROOT / "frontend" / "public" / "videos"
RUNTIME.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor de escenario JH NVIDIA
sys.path.insert(0, str(ROOT / "scripts"))
from jh_nvidia_stage_engine import render_jh_stage_frame

MATRIX_FILE = ROOT / "backend" / "database" / "trilingual_masterclass_matrix_2026.json"
with open(MATRIX_FILE, "r", encoding="utf-8") as f:
    TRILINGUAL_DATA = json.load(f)

TRILINGUAL_MODULES = TRILINGUAL_DATA["modules"]

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_speech(text: str, out_path: str, lang: str):
    if lang == "es":
        voice = "es-CO-GonzaloNeural"
        rate = "-8%"
        pitch = "-4Hz"
    elif lang == "en":
        voice = "en-US-AndrewMultilingualNeural"
        rate = "-6%"
        pitch = "-3Hz"
    elif lang == "zh":
        voice = "zh-CN-YunxiNeural"
        rate = "-4%"
        pitch = "-2Hz"
    else:
        voice = "es-CO-GonzaloNeural"
        rate = "-8%"
        pitch = "-4Hz"

    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def build_audio_track_for_lang(lang: str):
    print(f"\n[FASE 1/4 - {lang.upper()}] Generando locución calibrada ({lang.upper()})...")
    raw_files = []
    
    for i, mod in enumerate(TRILINGUAL_MODULES):
        text = mod["text"][lang]
        raw_path = str(RUNTIME / f"{lang}_raw_{i}.mp3")
        asyncio.run(synthesize_speech(text, raw_path, lang))
        raw_files.append(raw_path)

    # Masterización acústica EBU R128
    master_files = []
    eq_chain = (
        "highpass=f=80,"
        "equalizer=f=220:t=q:w=1.2:g=2.8,"
        "equalizer=f=500:t=q:w=1.5:g=-2.2,"
        "equalizer=f=3500:t=q:w=1.0:g=3.8,"
        "equalizer=f=10000:t=q:w=1.0:g=2.2,"
        "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
        "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
    )

    for i, raw in enumerate(raw_files):
        master_path = str(RUNTIME / f"{lang}_master_{i}.aac")
        cmd = [
            "ffmpeg", "-y", "-i", raw,
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            master_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        master_files.append(master_path)

    # Pausa entre módulos de 1.0s
    pause_path = str(RUNTIME / f"pause_{lang}.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", pause_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    concat_txt = str(RUNTIME / f"concat_{lang}.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for i, mf in enumerate(master_files):
            f.write(f"file '{Path(mf).as_posix()}'\n")
            f.write(f"file '{Path(pause_path).as_posix()}'\n")

    master_audio = str(RUNTIME / f"master_soundtrack_{lang}_48k.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c:a", "copy", master_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_dur = get_audio_duration(master_audio)
    print(f"  [OK] Audio Maestro ({lang.upper()}): {total_dur:.2f}s ({total_dur/60:.2f} min)")
    return master_audio, total_dur, master_files

def render_single_language_video(lang: str):
    print("=" * 70)
    print(f"  🎬 RENDERIZANDO MASTERCLASS JH NVIDIA 1080P: [{lang.upper()}]")
    print("=" * 70)

    # 1. Pista de audio
    master_audio, total_duration, master_files = build_audio_track_for_lang(lang)

    # 2. Avatar Transparente
    avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_path).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    # 3. Tipografía
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 52)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_badge = font_title = font_concept = font_karaoke = font_top = ImageFont.load_default()

    # 4. Línea de tiempo
    timeline = []
    curr_t = 0.0
    for i, mod in enumerate(TRILINGUAL_MODULES):
        dur = get_audio_duration(master_files[i])
        t_start = curr_t
        t_end = curr_t + dur
        timeline.append({
            "mod": mod,
            "start": t_start,
            "end": t_end,
            "duration": dur
        })
        curr_t = t_end + 1.0

    frames_dir = RUNTIME / f"temp_frames_{lang}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 3/4 - {lang.upper()}] Renderizando {total_frames} fotogramas Full HD con Escenario JH NVIDIA...")

    WORDS_PER_CHUNK = 8

    for f_idx in range(total_frames):
        t = f_idx / FPS

        active_entry = timeline[-1]
        for entry in timeline:
            if entry["start"] <= t <= entry["end"] + 1.0:
                active_entry = entry
                break

        mod = active_entry["mod"]
        t_rel = max(0.0, t - active_entry["start"])
        dur_mod = max(0.1, active_entry["duration"])

        # Fondo Dinámico Jensen Huang
        frame = render_jh_stage_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        
        lang_title = "ESPAÑOL MASTER" if lang == "es" else ("ENGLISH MASTER" if lang == "en" else "中文 MANDARIN MASTER")
        draw.text((430, 24), f"·   NVIDIA STUDIO ARCHITECTURE [{lang_title}]", font=font_top, fill=(190, 200, 220))
        draw.text((1580, 24), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # Avatar Transparente Lado Izquierdo
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        draw.text((80, 95), "GUILLERMO · OPENCLAW", font=font_badge, fill=(255, 255, 255))
        draw.text((80, 125), "Arquitectura Soberana B2B / HB Jewelry", font=font_concept, fill=(212, 175, 55))

        # Lado Derecho: Contenido Flotante
        content_x = 640
        content_y = 100
        content_w = 1220

        draw.text((content_x, content_y), f"MÓDULO {mod['num']} // {mod['badge'][lang]}", font=font_badge, fill=(212, 175, 55))
        draw.text((content_x, content_y + 45), mod["title"][lang], font=font_title, fill=(255, 255, 255))
        draw.text((content_x, content_y + 115), "⚡ " + mod["concept"][lang], font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 160, content_x + content_w, content_y + 160], fill=(45, 60, 90), width=1)

        # Teleprompter Karaoke en Oro (52pt)
        words = mod["text"][lang].split()
        total_words = len(words)
        active_word_global_idx = int((t_rel / dur_mod) * total_words) if dur_mod > 0 else 0

        chunk_idx = active_word_global_idx // WORDS_PER_CHUNK
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(total_words, chunk_start + WORDS_PER_CHUNK)
        current_chunk_words = words[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = content_y + 240
        line_height = 80
        max_line_w = content_w - 40

        for w_local_idx, word in enumerate(current_chunk_words):
            global_w_idx = chunk_start + w_local_idx
            word_str = word + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            draw.text((cursor_x + 3, cursor_y + 3), word_str, font=font_karaoke, fill=(0, 0, 0))

            if global_w_idx == active_word_global_idx:
                w_color = (255, 215, 0)
            elif global_w_idx < active_word_global_idx:
                w_color = (245, 248, 255)
            else:
                w_color = (110, 125, 150)

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 400 == 0:
            print(f"    -> [{lang.upper()}] Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 5. Codificación MP4 FastStart 1080p
    print(f"\n[FASE 4/4 - {lang.upper()}] Codificando Masterclass 1080p con FFmpeg FastStart...")
    
    lang_suffix = "Espanol" if lang == "es" else ("English" if lang == "en" else "Mandarin")
    output_filename = f"OpenClaw_Masterclass_{lang_suffix}_JH_NVIDIA_1080p.mp4"
    final_runtime = RUNTIME / output_filename
    final_public = PUBLIC_DIR / output_filename

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "frame_%06d.jpg"),
        "-i", master_audio,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_runtime)
    ]
    subprocess.run(cmd_render, check=True)

    import shutil
    shutil.copy2(final_runtime, final_public)

    # Limpiar fotogramas
    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    size_mb = final_runtime.stat().st_size / (1024 * 1024)
    print(f"\n============================================================")
    print(f"  🏆 MASTERCLASS {lang.upper()} GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_public}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} min)")
    print(f"============================================================")
    return str(final_public)

def render_all_languages():
    print("=" * 70)
    print("  🚀 OPENCLAW TRILINGUAL JH NVIDIA PRODUCTION ENGINE")
    print("============================================================")
    
    out_es = render_single_language_video("es")
    out_en = render_single_language_video("en")
    out_zh = render_single_language_video("zh")

    print("\n" + "=" * 70)
    print("  🎉 TRILOGÍA DE VIDEOS MAESTROS COMPLETADA EXITOSAMENTE")
    print(f"  1. Español:   {out_es}")
    print(f"  2. English:   {out_en}")
    print(f"  3. 中文 (ZH): {out_zh}")
    print("=" * 70)

if __name__ == "__main__":
    render_all_languages()
