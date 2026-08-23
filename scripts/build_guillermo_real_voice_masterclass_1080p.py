"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS CON LA VOZ REAL DE GUILLERMO (1080P)
==============================================================================
- Pista de Audio: Voz Real de Guillermo (Guillermo_Podcast_Master_Edit_48k.mp3)
- Transcripción y Sincronización: Whisper Word-by-Word Timestamps
- Visual: Avatar HD + Breakdown en Balas + Fondo Cósmico + Diagramas de Atención
- Salida: 1080p FastStart MP4 a 25 FPS
==============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import whisper

ROOT = Path(__file__).parent.parent
MASTER_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.mp3"
OUTPUT_DIR = ROOT / "runtime" / "guillermo_podcast_master"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FINAL_VIDEO = OUTPUT_DIR / "Guillermo_Voz_Real_Masterclass_1080p.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame

# ─── MÓDULOS SINCRONIZADOS A LAS REFLEXIONES REALES DE GUILLERMO ─────────────

PODCAST_SECTIONS = [
    {
        "time_start": 0.0,
        "time_end": 68.0,
        "badge": "BIOMETRÍA VOCAL & JENSEN HUANG",
        "title": "La Voz Humana como Identidad y Reconocimiento Exacto",
        "concept": "Jensen Huang & Biometría: Paridad Acústica Total en Videos",
        "bullets": [
            "• Identidad Vocal: Captura de matices y calibración acústica de la voz.",
            "• Reconocimiento de Voz: Precisión para autenticación y seguridad biométrica.",
            "• Marca del Fundador: Generar confianza directa con cada espectador."
        ]
    },
    {
        "time_start": 68.0,
        "time_end": 260.0,
        "badge": "DESGLOSE DE ECOSISTEMAS",
        "title": "Ecosistemas de IA: OpenAI, Anthropic y OpenClaw",
        "concept": "Estructura en Balas: Explicar Cada Modelo por Separado con Pausas",
        "bullets": [
            "• OpenAI: Exponer GPT-4o, o1 y o3-mini uno a uno con su función específica.",
            "• Anthropic: Reseña de Claude 3.5 Sonnet, Haiku y Claude Opus.",
            "• OpenClaw: Soberanía de modelos abiertos (DeepSeek-R1, Qwen 2.5) a costo cero."
        ]
    },
    {
        "time_start": 260.0,
        "time_end": 335.0,
        "badge": "ESTILO PODCAST ANCHOR",
        "title": "Dicción de Noticiero con la Calidez de un Podcast Amigable",
        "concept": "Cero Lectura Rígida: Comunicación Fluida, Cercana y Profesional",
        "bullets": [
            "• Claridad de Noticiero: Articulación limpia de términos técnicos y conceptos.",
            "• Tono de Conversación: Explicar como en un podcast entre amigos y colegas.",
            "• Creación de Marca: Un estilo único, accesible y comprensible para todos."
        ]
    },
    {
        "time_start": 335.0,
        "time_end": 382.0,
        "badge": "GOBERNANZA DE RECURSOS",
        "title": "Inferencia Desacoplada y Cero Bloqueo de Antigravity",
        "concept": "Cómputo en la Nube (CPU/GPU) para Trabajar sin Límites",
        "bullets": [
            "• Cero Bloqueo: Antigravity 100% fluido durante toda la jornada de desarrollo.",
            "• Cómputo Asíncrono: Whisper, vectorización y video en segundo plano.",
            "• Continuidad Operativa: Escalar el ecosistema sin interrupciones técnicas."
        ]
    }
]

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def main():
    print("=" * 70)
    print(" [OPENCLAW 2026] MASTERCLASS 1080P CON LA VOZ REAL DE GUILLERMO")
    print("=" * 70)

    if not MASTER_AUDIO.exists():
        print(f"[ERROR] No se encontró el audio master de Guillermo en: {MASTER_AUDIO}")
        return

    total_duration = get_audio_duration(str(MASTER_AUDIO))
    print(f"-> Audio Real de Guillermo: {MASTER_AUDIO.name} ({total_duration:.2f} s / {total_duration/60:.2f} min)")

    # 1. Transcripción con Whisper para extraer marcas de tiempo de las palabras de Guillermo
    print("\n[1/4] Extrayendo marcas de tiempo fonéticas con Whisper de la voz real...")
    whisper_model = whisper.load_model("base")
    res = whisper_model.transcribe(str(MASTER_AUDIO), language="es", word_timestamps=True)

    words_timed = []
    for segment in res.get("segments", []):
        for w in segment.get("words", []):
            words_timed.append({
                "word": w.get("word", "").strip(),
                "start": float(w.get("start", 0.0)),
                "end": float(w.get("end", 0.0))
            })

    print(f"  [OK] {len(words_timed)} palabras de Guillermo sincronizadas al milisegundo.")

    # 2. Cargar Avatar PNG transparente
    print("\n[2/4] Preparando composición visual HD...")
    avatar_src = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    # Fuentes
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
        font_title = ImageFont.truetype("arialbd.ttf", 38)
        font_concept = ImageFont.truetype("arialbd.ttf", 24)
        font_bullet = ImageFont.truetype("arial.ttf", 22)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 40)
        font_sub = ImageFont.truetype("ariali.ttf", 22)
        font_top = ImageFont.truetype("arialbd.ttf", 20)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_bullet = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_top = ImageFont.load_default()

    frames_dir = OUTPUT_DIR / "temp_frames_real_voice"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[3/4] Renderizando {total_frames} fotogramas 1080p sobre la voz auténtica...")

    WORDS_PER_CHUNK = 9

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # Sección activa según el segundo actual
        active_sec = PODCAST_SECTIONS[-1]
        for sec in PODCAST_SECTIONS:
            if sec["time_start"] <= t < sec["time_end"]:
                active_sec = sec
                break

        # 1. Fondo Cósmico en Movimiento Continuo
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior
        draw.line([60, 50, WIDTH - 60, 50], fill=(212, 175, 55), width=1)
        draw.text((60, 20), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 20), "·   VOZ REAL DEL FUNDADOR: IDENTIDAD, ECOSISTEMAS & MARCA PERSONAL", font=font_top, fill=(190, 200, 220))
        draw.text((1560, 20), "VOZ REAL 48kHz · EBU R128", font=font_top, fill=(100, 220, 150))

        # 2. Lado Izquierdo: Avatar de Guillermo con micro-movimiento
        av_float_y = int(math.sin(t * 1.4) * 4)
        av_x = 30
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Identificación
        draw.text((70, 75), "GUILLERMO · OPENCLAW FOUNDER (VOZ REAL)", font=font_badge, fill=(255, 255, 255))
        draw.text((70, 102), "Locución Auténtica · Calibración Acústica 100.87 Hz", font=font_concept, fill=(212, 175, 55))

        # 3. Lado Derecho: Tarjetas Jerárquicas en Balas
        content_x = 640
        content_y = 80
        content_w = 1220

        draw.text((content_x, content_y), f"BLOQUE TEMÁTICO · {active_sec['badge']}", font=font_badge, fill=(212, 175, 55))
        draw.text((content_x, content_y + 35), active_sec["title"], font=font_title, fill=(255, 255, 255))

        concept_text = "⚡ " + active_sec["concept"]
        draw.text((content_x, content_y + 90), concept_text, font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 130, content_x + content_w, content_y + 130], fill=(45, 60, 90), width=1)

        # Balas con sangría de 24px
        b_y = content_y + 145
        for b_str in active_sec["bullets"]:
            draw.text((content_x + 20, b_y), b_str, font=font_bullet, fill=(220, 230, 245))
            b_y += 38

        draw.line([content_x, b_y + 10, content_x + content_w, b_y + 10], fill=(45, 60, 90), width=1)

        # 4. Teleprompter Karaoke Sincronizado a la Voz Real de Guillermo
        active_w_idx = 0
        for w_i, w_info in enumerate(words_timed):
            if w_info["start"] <= t <= w_info["end"]:
                active_w_idx = w_i
                break
            elif t > w_info["end"]:
                active_w_idx = w_i + 1

        total_words = len(words_timed)
        chunk_idx = active_w_idx // WORDS_PER_CHUNK
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(total_words, chunk_start + WORDS_PER_CHUNK)
        current_chunk = words_timed[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = b_y + 35
        line_height = 60
        max_line_w = content_w - 40

        for w_local_idx, w_data in enumerate(current_chunk):
            global_idx = chunk_start + w_local_idx
            word_str = w_data["word"] + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            draw.text((cursor_x + 2, cursor_y + 2), word_str, font=font_karaoke, fill=(0, 0, 0))

            if global_idx == active_w_idx:
                w_color = (255, 215, 0)   # Oro brillante (palabra que está diciendo Guillermo)
            elif global_idx < active_w_idx:
                w_color = (245, 248, 255) # Blanco (ya dicha)
            else:
                w_color = (110, 125, 150) # Futura

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # 5. Subtítulo en Base Flotante
        draw.line([content_x, HEIGHT - 105, content_x + content_w, HEIGHT - 105], fill=(45, 60, 90), width=1)
        sub_str = "OPENCLAW SOVEREIGN BROADCAST · LOCUCIÓN REAL MASTERIZADA EBU R128 (-16 LUFS)"
        draw.text((content_x + 1, HEIGHT - 80 + 1), sub_str, font=font_sub, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 80), sub_str, font=font_sub, fill=(160, 190, 230))

        # Barra de Progreso
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 800 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 6. Codificación FastStart MP4 1080p
    print("\n[4/4] Codificando Masterclass con FFmpeg FastStart 1080p...")
    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "frame_%06d.jpg"),
        "-i", str(MASTER_AUDIO),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(FINAL_VIDEO)
    ]
    subprocess.run(cmd_render, check=True)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    size_mb = FINAL_VIDEO.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 70)
    print("  [EXITO MASTER] VIDEO 1080P CON LA VOZ REAL DE GUILLERMO GENERADO")
    print(f"  Ruta:     {FINAL_VIDEO}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} min)")
    print("=" * 70)

if __name__ == "__main__":
    main()
