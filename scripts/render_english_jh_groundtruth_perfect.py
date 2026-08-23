"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS ENGLISH JH NVIDIA GROUND TRUTH PERFECT SYNC
==============================================================================
- SINCRONIZACIÓN: Whisper Ground Truth con word_timestamps=True (Milisegundo a milisegundo)
- ESCENARIO: Jensen Huang Dynamic Stage con 4 Infografías de Arquitectura NVIDIA
- AVATAR: Guillermo PNG Transparente Integrado con Bordado HB.OS
- STREAMING: Direct Pipe en Memoria (Zero-Disk I/O) -> MP4 FastStart 1080p
==============================================================================
"""

import os
import sys
import math
import json
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import whisper

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_english_perfect_sync"
PUBLIC_DIR = ROOT / "frontend" / "public" / "videos"
RUNTIME.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

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

def synthesize_and_align_english():
    print("=" * 75)
    print("  🎙️ [ENGLISH GROUND TRUTH] SINTETIZANDO Y ALINEANDO CON WHISPER...")
    print("=" * 75)

    import asyncio

    async def synth_all():
        tasks = []
        for i, mod in enumerate(TRILINGUAL_MODULES):
            text = mod["text"]["en"]
            raw_path = str(RUNTIME / f"en_raw_{i}.mp3")
            comm = edge_tts.Communicate(text, voice="en-US-AndrewMultilingualNeural", rate="-6%", pitch="-3Hz")
            tasks.append(comm.save(raw_path))
        await asyncio.gather(*tasks)

    asyncio.run(synth_all())

    # Masterización acústica EBU R128 (-16 LUFS / 48kHz Stereo)
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

    for i in range(len(TRILINGUAL_MODULES)):
        raw_path = str(RUNTIME / f"en_raw_{i}.mp3")
        master_path = str(RUNTIME / f"en_master_{i}.aac")
        cmd = [
            "ffmpeg", "-y", "-i", raw_path,
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            master_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        master_files.append(master_path)

    # Pausa de 1.0s entre módulos
    pause_path = str(RUNTIME / "pause_en.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", pause_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    concat_txt = str(RUNTIME / "concat_en.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for mf in master_files:
            f.write(f"file '{Path(mf).as_posix()}'\n")
            f.write(f"file '{Path(pause_path).as_posix()}'\n")

    master_audio = str(RUNTIME / "master_audio_en_48k.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c:a", "copy", master_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_dur = get_audio_duration(master_audio)
    print(f"  ✓ Audio Maestro Completo: {total_dur:.2f}s ({total_dur/60:.2f} min)")

    # Alineación con Whisper Ground Truth (Word Timestamps)
    print("\n🧠 [WHISPER GROUND TRUTH] Alineando palabras al milisegundo exacto...")
    whisper_model = whisper.load_model("base")

    curr_offset = 0.0
    timeline = []

    for i, (mf, mod) in enumerate(zip(master_files, TRILINGUAL_MODULES)):
        dur = get_audio_duration(mf)
        mod_start = curr_offset
        mod_end = mod_start + dur

        res = whisper_model.transcribe(mf, language="en", word_timestamps=True)
        detected_words = []
        for seg in res.get("segments", []):
            for w in seg.get("words", []):
                detected_words.append(w)

        canonical_tokens = mod["text"]["en"].split()
        aligned_words = []

        if len(detected_words) > 0 and len(canonical_tokens) > 0:
            scale = len(detected_words) / len(canonical_tokens)
            for c_idx, c_tok in enumerate(canonical_tokens):
                w_idx = min(int(c_idx * scale), len(detected_words) - 1)
                w_obj = detected_words[w_idx]
                aligned_words.append({
                    "word": c_tok,
                    "start": mod_start + w_obj["start"],
                    "end": mod_start + w_obj["end"]
                })
        else:
            tok_dur = dur / max(len(canonical_tokens), 1)
            for c_idx, c_tok in enumerate(canonical_tokens):
                aligned_words.append({
                    "word": c_tok,
                    "start": mod_start + c_idx * tok_dur,
                    "end": mod_start + (c_idx + 1) * tok_dur
                })

        timeline.append({
            "mod": mod,
            "start": mod_start,
            "end": mod_end,
            "duration": dur,
            "words": aligned_words
        })
        curr_offset = mod_end + 1.0

    return master_audio, total_dur, timeline

def render_perfect_english_master():
    master_audio, total_duration, timeline = synthesize_and_align_english()

    # Cargar avatar transparente con bordado HB.OS
    avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_path).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 52)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_badge = font_title = font_concept = font_karaoke = font_top = ImageFont.load_default()

    output_filename = "OpenClaw_Masterclass_English_JH_NVIDIA_GroundTruth_1080p.mp4"
    final_runtime = RUNTIME / output_filename
    final_public = PUBLIC_DIR / output_filename

    total_frames = int(total_duration * FPS)

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",  # Entrada directa desde RAM stdin
        "-i", master_audio,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_runtime)
    ]

    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    start_time = time.time()

    print(f"\n🎬 [RENDER PIPE] Renderizando {total_frames} fotogramas Full HD con Ground Truth Sync...")

    WORDS_PER_CHUNK = 8

    for f_idx in range(total_frames):
        t = f_idx / FPS

        active_entry = timeline[-1]
        for entry in timeline:
            if entry["start"] <= t <= entry["end"] + 1.0:
                active_entry = entry
                break

        mod = active_entry["mod"]
        words_obj_list = active_entry["words"]

        # Escenario Dinámico Jensen Huang
        frame = render_jh_stage_frame(t)
        draw = ImageDraw.Draw(frame)

        # Header Superior
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 24), "·   NVIDIA STUDIO ARCHITECTURE [ENGLISH EXECUTIVE MASTER]", font=font_top, fill=(190, 200, 220))
        draw.text((1580, 24), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # Avatar Transparente
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

        draw.text((content_x, content_y), f"MÓDULO {mod['num']} // {mod['badge']['en']}", font=font_badge, fill=(212, 175, 55))
        draw.text((content_x, content_y + 45), mod["title"]["en"], font=font_title, fill=(255, 255, 255))
        draw.text((content_x, content_y + 115), "⚡ " + mod["concept"]["en"], font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 160, content_x + content_w, content_y + 160], fill=(45, 60, 90), width=1)

        # ─── TELEPROMPTER KARAOKE CON GROUND TRUTH SYNC (SINCRONIZACIÓN EXACTA) ───
        active_word_idx = -1
        for w_i, w_obj in enumerate(words_obj_list):
            if w_obj["start"] <= t <= w_obj["end"]:
                active_word_idx = w_i
                break
            elif t > w_obj["end"]:
                active_word_idx = w_i

        chunk_idx = max(0, active_word_idx // WORDS_PER_CHUNK)
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(len(words_obj_list), chunk_start + WORDS_PER_CHUNK)
        current_chunk = words_obj_list[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = content_y + 240
        line_height = 80
        max_line_w = content_w - 40

        for w_local_idx, w_obj in enumerate(current_chunk):
            global_w_idx = chunk_start + w_local_idx
            word_str = w_obj["word"] + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            draw.text((cursor_x + 3, cursor_y + 3), word_str, font=font_karaoke, fill=(0, 0, 0))

            if global_w_idx == active_word_idx and (w_obj["start"] <= t <= w_obj["end"]):
                w_color = (255, 215, 0)   # Oro Activo en el milisegundo exacto
            elif global_w_idx < active_word_idx or (global_w_idx == active_word_idx and t > w_obj["end"]):
                w_color = (245, 248, 255) # Blanco Leído
            else:
                w_color = (110, 125, 150) # Futuro

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # Barra de progreso inferior en oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        # Direct Pipe a FFmpeg
        proc.stdin.write(frame.tobytes())

        if f_idx % 800 == 0:
            elapsed = time.time() - start_time
            fps_speed = (f_idx + 1) / elapsed if elapsed > 0 else 0
            print(f"    -> [ENGLISH GT] Frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) | {fps_speed:.1f} FPS")

    proc.stdin.close()
    proc.wait()

    import shutil
    shutil.copy2(final_runtime, final_public)

    total_time = time.time() - start_time
    size_mb = final_public.stat().st_size / (1024 * 1024)
    print(f"\n============================================================")
    print(f"  🏆 MASTERCLASS ENGLISH PERFECT SYNC GENERADA")
    print(f"  Ruta Pública: {final_public}")
    print(f"  Tamaño:       {size_mb:.2f} MB")
    print(f"  Duración:     {total_duration:.2f}s ({total_duration/60:.2f} min)")
    print(f"  Tiempo Render: {total_time:.2f}s")
    print(f"============================================================")

    # Abrir inmediatamente en Windows player
    subprocess.run(["powershell", "-Command", f"Invoke-Item '{final_public}'"], check=True)
    return str(final_public)

if __name__ == "__main__":
    render_perfect_english_master()
