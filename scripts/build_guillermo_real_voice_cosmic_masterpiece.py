"""
==============================================================================
OPENCLAW 2026 — VIDEO MAESTRO CON VOZ REAL DE GUILLERMO Y UNIVERSO CÓSMICO
==============================================================================
- Audio: VOZ REAL DE GUILLERMO MASTERIZADA (48kHz Stereo EBU R128 -16 LUFS)
- Visual: Avatar Guillermo PNG 100% Transparente Integrado (SIN CÍRCULOS NI CAJAS)
- Fondo: Universo Cósmico en Movimiento Continuo Suave (180 Estrellas)
- Texto: Teleprompter Flotante con Fuente Gigante (52pt) + Karaoke Oro Palabra por Palabra
- Formato: 1080p FastStart MP4
==============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "guillermo_real_voice_masterpiece"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame

# ─── PISTA Y TEXTO REAL DE GUILLERMO ────────────────────────────────────────

REAL_AUDIO_PATH = ROOT / "runtime" / "guillermo_voice_studio_master_48k.aac"

GUILLERMO_TRANSCRIPTION = (
    "¿Quieres convertirte en un gran vendedor, construir una comunidad sólida "
    "y aprovechar todas las ventajas que te ofrece la plataforma de TikTok? "
    "Si tu respuesta es sí, escúchame durante los próximos 3 minutos."
)

ENGLISH_SUBTITLE = (
    "EN: Do you want to become a top seller, build a solid community, "
    "and leverage the full power of modern platforms? Listen closely."
)

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def render_real_voice_masterpiece():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 60)
    print("  🎙️ OPENCLAW VIDEO CON VOZ REAL DE GUILLERMO & FONDO CÓSMICO")
    print("=" * 60)

    if not REAL_AUDIO_PATH.exists():
        print(f"[ERROR] Archivo de audio real no encontrado: {REAL_AUDIO_PATH}")
        sys.exit(1)

    duration = get_audio_duration(str(REAL_AUDIO_PATH))
    print(f"-> Duración de tu voz real: {duration:.2f} segundos")

    # Cargar Avatar PNG 100% Transparente Integrado
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    
    # Escalar a 860px de alto (proporción natural en pantalla)
    av_h = 860
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"-> Avatar PNG Transparente cargado: {av_w}x{av_h} px")

    # Fuentes
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 44)
        font_concept = ImageFont.truetype("arialbd.ttf", 24)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 52)  # Letra gigante descansada
        font_en = ImageFont.truetype("ariali.ttf", 26)
        font_speaker = ImageFont.truetype("arialbd.ttf", 26)
        font_role = ImageFont.truetype("arial.ttf", 20)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_speaker = ImageFont.load_default()
        font_role = ImageFont.load_default()
        font_top = ImageFont.load_default()

    frames_dir = RUNTIME / "temp_real_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(duration * FPS)
    print(f"-> Renderizando {total_frames} fotogramas Full HD con tu voz real...")

    words = GUILLERMO_TRANSCRIPTION.split()
    total_words = len(words)
    WORDS_PER_CHUNK = 8  # Bloques cortos de 8 palabras para lectura súper descansada

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # ─── 1. FONDO CÓSMICO EN MOVIMIENTO CONTINUO ───
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior de Control
        draw.rectangle([0, 0, WIDTH, 80], fill=(10, 14, 25))
        draw.line([0, 80, WIDTH, 80], fill=(212, 175, 55), width=2)
        draw.text((60, 26), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 26), "·   VOZ REAL DE GUILLERMO MASTERIZADA EN ESTUDIO (48kHz)", font=font_top, fill=(195, 205, 225))
        draw.text((1580, 26), "100% VOZ HUMANA REAL", font=font_top, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR PNG TRANSPARENTE INTEGRADO (SIN MARCOS) ───
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 50
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Lower Third de Identificación Flotante
        id_x = 70
        id_y = 110
        draw.rounded_rectangle([id_x, id_y, id_x + 460, id_y + 85], radius=10, fill=(14, 18, 30), outline=(40, 55, 80), width=1)
        draw.text((id_x + 22, id_y + 14), "GUILLERMO · EN PERSONA", font=font_speaker, fill=(255, 255, 255))
        draw.text((id_x + 22, id_y + 48), "Director de Arquitectura · OpenClaw", font=font_role, fill=(212, 175, 55))
        draw.ellipse([id_x + 420, id_y + 22, id_x + 438, id_y + 40], fill=(50, 220, 100))

        # ─── 3. LADO DERECHO: TEXTO FLOTANTE GIGANTE (52PT) CON KARAOKE ORO ───
        content_x = 640
        content_y = 110
        content_w = 1220

        # Título
        draw.text((content_x, content_y + 10), "CONSTRUCCIÓN DE COMUNIDAD Y VENTAS B2B", font=font_title, fill=(255, 255, 255))
        draw.text((content_x, content_y + 70), "⚡ ESTRATEGIA DE CRECIMIENTO EXPONENCIAL Y MONETIZACIÓN", font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 115, content_x + content_w, content_y + 115], fill=(45, 60, 90), width=1)

        # Cálculo de palabra activa según progreso temporal
        active_word_global_idx = int((t / max(0.1, duration)) * total_words)

        chunk_idx = active_word_global_idx // WORDS_PER_CHUNK
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(total_words, chunk_start + WORDS_PER_CHUNK)
        current_chunk_words = words[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = content_y + 200
        line_height = 80
        max_line_w = content_w - 40

        # Fondo sutil de respiración detrás del texto
        draw.rounded_rectangle([content_x - 20, cursor_y - 20, content_x + content_w, cursor_y + 360], radius=16, fill=(12, 16, 28), outline=(32, 44, 68), width=1)

        for w_local_idx, word in enumerate(current_chunk_words):
            global_w_idx = chunk_start + w_local_idx
            word_str = word + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            if global_w_idx == active_word_global_idx:
                w_color = (255, 215, 0)   # Oro brillante
            elif global_w_idx < active_word_global_idx:
                w_color = (245, 248, 255) # Blanco nítido
            else:
                w_color = (100, 115, 140) # Futuro

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # Subtítulo en Inglés
        draw.line([content_x, HEIGHT - 130, content_x + content_w, HEIGHT - 130], fill=(45, 60, 90), width=1)
        draw.text((content_x, HEIGHT - 100), ENGLISH_SUBTITLE, font=font_en, fill=(160, 190, 230))

        # Barra de progreso en oro
        progress_pct = t / duration
        draw.rectangle([0, HEIGHT - 8, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"real_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=90)

        if f_idx % 100 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n-> Codificando Video Maestro con Tu Voz Real...")
    final_output = RUNTIME / "Guillermo_Voz_Real_Cosmic_1080p_FastStart.mp4"

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "real_%06d.jpg"),
        "-i", str(REAL_AUDIO_PATH),
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

    size_mb = final_output.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print("  🏆 VIDEO MAESTRO CON TU VOZ REAL GENERADO CON ÉXITO")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {duration:.2f} segundos")
    print("  Audio:    100% TU VOZ REAL MASTERIZADA EN ESTUDIO")
    print("  Visual:   Avatar PNG Transparente Integrado + Universo Cósmico + Letra 52pt")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

if __name__ == "__main__":
    render_real_voice_masterpiece()
