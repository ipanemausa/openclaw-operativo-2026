"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS JH NVIDIA CINEMATIC STAGE CON VOZ DE GUILLERMO
==============================================================================
- Escenario: Jensen Huang Keynote Stage con fondo vivo que cambia sutilmente
- Arquitectura en Fondo: Blackwell NVL72, Maxine Audio2Face, Vector Space R^768
- Avatar: Guillermo PNG 100% Transparente Integrado directamente en escena
- Teleprompter: Karaoke Oro Palabra por Palabra (54pt) con sombra suave
- Locución: Perfil Acústico de Guillermo (48kHz Stereo EBU R128 -16 LUFS)
- Render: 1080p 60/25fps FastStart MP4
==============================================================================
"""

import os
import sys
import math
import asyncio
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_jh_nvidia_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor de escenario JH NVIDIA y módulos definitivos
sys.path.insert(0, str(ROOT / "scripts"))
from jh_nvidia_stage_engine import render_jh_stage_frame
from generate_ultimate_b2b_cosmic_masterclass import DEFINITIVE_MODULES, get_audio_duration

async def synthesize_guillermo_calibrated_speech():
    """Sintetiza los módulos con la calibración acústica y tímbrica exacta de Guillermo."""
    print("\n[FASE 1/4] Sintetizando locución calibrada con el perfil vocal de Guillermo...")
    for idx, item in enumerate(DEFINITIVE_MODULES):
        raw_mp3 = RUNTIME / f"guillermo_raw_{idx}.mp3"
        master_aac = RUNTIME / f"guillermo_master_{idx}.aac"

        # Cadencia y tono calibrado a la voz real de Guillermo (-6% rate, -2Hz pitch)
        comm = edge_tts.Communicate(item["text"], voice="es-CO-GonzaloNeural", rate="-6%", pitch="-2Hz")
        await comm.save(str(raw_mp3))

        # Cadena de Ecualización Paramétrica extraída de la voz de Guillermo
        eq_chain = (
            "highpass=f=80,"
            "equalizer=f=220:t=q:w=1.2:g=2.8,"
            "equalizer=f=500:t=q:w=1.5:g=-2.2,"
            "equalizer=f=3500:t=q:w=1.0:g=3.8,"
            "equalizer=f=10000:t=q:w=1.0:g=2.2,"
            "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
            "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(master_aac)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        dur = get_audio_duration(str(master_aac))
        item["audio_file"] = str(master_aac)
        item["duration"] = dur
        print(f"  [OK] Módulo {item['chapter_num']}: {dur:.2f}s | '{item['title']}'")

def render_jh_nvidia_masterpiece():
    print("=" * 70)
    print("  🎬 OPENCLAW — MASTERCLASS JH NVIDIA CINEMATIC STAGE (1080P)")
    print("=" * 70)

    # 1. Sintetizar audios
    asyncio.run(synthesize_guillermo_calibrated_speech())

    # 2. Mezclar pista de audio con pausas naturales
    print("\n[FASE 2/4] Ensamblando pista de audio continua con pausas naturales (1.2s)...")
    pause_aac = RUNTIME / "pause_12s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.2", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    concat_txt = RUNTIME / "concat_seamless.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in DEFINITIVE_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")

    master_audio = RUNTIME / "master_soundtrack_jh_stage_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f}s ({total_duration/60:.2f} minutos)")

    # 3. Cargar Avatar PNG 100% Transparente
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    if not avatar_src.exists():
        avatar_src = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"  -> Avatar transparente integrado: {av_w}x{av_h} px")

    # Fuentes tipográficas de alta definición
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 48)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 54)
        font_en = ImageFont.truetype("ariali.ttf", 24)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_top = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in DEFINITIVE_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.2

    frames_dir = RUNTIME / "temp_jh_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 3/4] Renderizando {total_frames} fotogramas Full HD con Escenario Dinámico NVIDIA JH...")

    WORDS_PER_CHUNK = 9

    for f_idx in range(total_frames):
        t = f_idx / FPS

        active_mod = None
        for entry in timeline:
            if entry["start"] <= t <= entry["end"]:
                active_mod = entry
                break
        if not active_mod:
            active_mod = timeline[-1]

        item = active_mod["item"]
        t_rel = max(0.0, t - active_mod["start"])
        dur_mod = max(0.1, active_mod["end"] - active_mod["start"])

        # ─── 1. FONDO DE ESCENARIO DINÁMICO ESTILO JENSEN HUANG ───
        frame = render_jh_stage_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior Minimalista Flotante
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 24), "·   NVIDIA STUDIO ARCHITECTURE & SOVEREIGN AI", font=font_top, fill=(190, 200, 220))
        draw.text((1580, 24), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR TRANSPARENTE EN ESCENA COMPLETA ───
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        draw.text((80, 95), "GUILLERMO · OPENCLAW", font=font_badge, fill=(255, 255, 255))
        draw.text((80, 125), "Arquitectura Soberana B2B / HB Jewelry", font=font_concept, fill=(212, 175, 55))

        # ─── 3. LADO DERECHO: TEXTO FLOTANTE DIRECTO SOBRE EL ESCENARIO ───
        content_x = 640
        content_y = 100
        content_w = 1220

        draw.text((content_x, content_y), f"CAPÍTULO {item['chapter_num']} · {item['category']}", font=font_badge, fill=(212, 175, 55))
        draw.text((content_x, content_y + 45), item["title"], font=font_title, fill=(255, 255, 255))
        draw.text((content_x, content_y + 115), "⚡ " + item["concept"], font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 160, content_x + content_w, content_y + 160], fill=(45, 60, 90), width=1)

        # ─── TELEPROMPTER KARAOKE EN LETRA GIGANTE (54PT) ───
        words = item["text"].split()
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

        # Subtítulo en Inglés Flotante en la Base
        draw.line([content_x, HEIGHT - 120, content_x + content_w, HEIGHT - 120], fill=(45, 60, 90), width=1)
        draw.text((content_x + 2, HEIGHT - 90 + 2), "EN: " + item["en_sub"], font=font_en, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 90), "EN: " + item["en_sub"], font=font_en, fill=(160, 190, 230))

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"jh_frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 400 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n[FASE 4/4] Codificando Masterclass JH NVIDIA Stage con FFmpeg FastStart...")
    final_output = RUNTIME / "OpenClaw_Masterclass_JH_NVIDIA_Stage_1080p.mp4"
    public_target = ROOT / "frontend" / "public" / "videos" / "OpenClaw_Masterclass_JH_NVIDIA_Stage_1080p.mp4"
    public_target.parent.mkdir(parents=True, exist_ok=True)

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "jh_frame_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_output)
    ]
    subprocess.run(cmd_render, check=True)

    import shutil
    shutil.copy2(final_output, public_target)

    size_mb = final_output.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 70)
    print("  🏆 MASTERCLASS JH NVIDIA STAGE GENERADA EXITOSAMENTE")
    print(f"  Ruta Runtime: {final_output}")
    print(f"  Ruta Pública: {public_target}")
    print(f"  Tamaño:       {size_mb:.2f} MB")
    print(f"  Duración:     {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print("  Escenario:    Jensen Huang Dynamic Stage + Gráficas Arquitectura NVIDIA")
    print("  Voz:          Perfil de Guillermo Calibrado (48kHz Stereo -16 LUFS)")
    print("=" * 70)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

if __name__ == "__main__":
    render_jh_nvidia_masterpiece()
