"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS CÓSMICA CON AVATAR PNG TRANSPARENTE
==============================================================================
- Fondo: Universo en movimiento continuo suave (180 estrellas + nebulosas de plasma)
- Avatar: Guillermo PNG 100% Transparente sin marco cuadrado de foto
- Audio: Locución Humanizada 48kHz Stereo EBU R128 (-16 LUFS)
- Teleprompter: Karaoke Dinámico en Oro sobre tarjeta de cristal translúcido
- Formato: 1080p FastStart MP4 para YouTube
==============================================================================
"""

import os
import sys
import math
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_cosmica_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico y guión humanizado
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame
from generate_full_10min_humanized_masterclass import HUMAN_MODULES, get_audio_duration

async def prepare_master_audio():
    """Verifica o reutiliza los audios humanizados ya sintetizados."""
    source_audio = ROOT / "runtime" / "masterclass_humanizada_10m" / "master_soundtrack_human_48k.aac"
    target_audio = RUNTIME / "master_audio_48k.aac"
    
    if source_audio.exists():
        import shutil
        shutil.copyfile(source_audio, target_audio)
        print(f"[AUDIO] Reutilizando pista maestra de 48kHz: {target_audio}")
    else:
        print("[AUDIO] Sintetizando pista maestra...")
        from generate_full_10min_humanized_masterclass import synthesize_human_audios
        await synthesize_human_audios()
        
    return str(target_audio)

def render_cosmic_masterclass():
    print("=" * 60)
    print("  🌌 OPENCLAW COSMIC MASTERCLASS (AVATAR PNG TRANSPARENTE)")
    print("=" * 60)

    # 1. Pista de audio
    master_audio_path = asyncio.run(prepare_master_audio())
    total_duration = get_audio_duration(master_audio_path)
    print(f"-> Duración total: {total_duration:.2f}s ({total_duration/60:.2f} minutos)")

    # 2. Cargar Avatar PNG 100% Transparente
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    
    # Escalar avatar a 820px de alto
    av_h = 820
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"-> Avatar PNG transparente cargado: {av_w}x{av_h} px")

    # Fuentes
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 38)
        font_text = ImageFont.truetype("arial.ttf", 32)
        font_en = ImageFont.truetype("ariali.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
        font_diagram = ImageFont.truetype("arialbd.ttf", 22)
        font_speaker = ImageFont.truetype("arialbd.ttf", 24)
        font_role = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_diagram = ImageFont.load_default()
        font_speaker = ImageFont.load_default()
        font_role = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in HUMAN_MODULES:
        t_start = curr_t
        t_end = curr_t + item.get("duration", 30.0)
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.0

    frames_dir = RUNTIME / "temp_cosmic_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"-> Renderizando {total_frames} fotogramas Full HD con fondo cósmico en movimiento...")

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

        # ─── 1. FONDO CÓSMICO EN MOVIMIENTO SUAVE ───
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior de Control
        draw.rectangle([0, 0, WIDTH, 80], fill=(12, 16, 28))
        draw.line([0, 80, WIDTH, 80], fill=(212, 175, 55), width=2)
        draw.text((60, 26), "OPENCLAW CORE MATRIX 2026", font=font_badge, fill=(212, 175, 55))
        draw.text((390, 26), "·   SISTEMA OPERATIVO UNIVERSAL & SOBERANÍA DIGITAL", font=font_badge, fill=(190, 200, 220))
        draw.text((1560, 26), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_badge, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR PNG TRANSPARENTE FLOTANTE (SIN CAJAS SÓLIDAS) ───
        av_float_y = int(math.sin(t * 1.5) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y  # Apoyado naturalmente en la base
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Lower Third de Identificación elegante y translúcido
        tag_x = 70
        tag_y = 110
        draw.rounded_rectangle([tag_x, tag_y, tag_x + 480, tag_y + 90], radius=10, fill=(15, 20, 32), outline=(40, 55, 80), width=1)
        draw.text((tag_x + 25, tag_y + 16), "GUILLERMO · OPENCLAW", font=font_speaker, fill=(255, 255, 255))
        draw.text((tag_x + 25, tag_y + 52), "Arquitectura Soberana B2B / HB Jewelry", font=font_role, fill=(212, 175, 55))
        draw.ellipse([tag_x + 435, tag_y + 24, tag_x + 453, tag_y + 42], fill=(50, 220, 100))

        # ─── 3. LADO DERECHO: TELEPROMPTER CRISTAL TRANSLÚCIDO CON KARAOKE ORO ───
        card_x = 680
        card_y = 110
        card_w = 1180
        card_h = 900
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(12, 16, 26), outline=(35, 48, 72), width=2)

        # Badges
        draw.rounded_rectangle([card_x + 50, card_y + 30, card_x + 220, card_y + 68], radius=6, fill=(212, 175, 55))
        draw.text((card_x + 65, card_y + 38), item["module"], font=font_badge, fill=(10, 15, 25))

        draw.rounded_rectangle([card_x + 235, card_y + 30, card_x + 600, card_y + 68], radius=6, fill=(24, 34, 54))
        draw.text((card_x + 250, card_y + 38), item["badge"], font=font_badge, fill=(212, 175, 55))

        # Título
        draw.text((card_x + 50, card_y + 85), item["title"], font=font_title, fill=(255, 255, 255))

        # Banner Técnico
        draw.rounded_rectangle([card_x + 50, card_y + 145, card_x + card_w - 50, card_y + 195], radius=6, fill=(20, 28, 45), outline=(42, 60, 90), width=1)
        draw.text((card_x + 70, card_y + 158), "⚡ ARTEFACTO: " + item["diagram"], font=font_diagram, fill=(100, 220, 180))

        draw.line([card_x + 50, card_y + 215, card_x + card_w - 50, card_y + 215], fill=(35, 48, 72), width=1)

        # Teleprompter Karaoke Dinámico en Oro
        words = item["text"].split()
        total_words = len(words)
        active_word_idx = int((t_rel / dur_mod) * total_words) if dur_mod > 0 else 0

        cursor_x = card_x + 50
        cursor_y = card_y + 245
        max_line_w = card_w - 100
        line_height = 46

        for w_idx, word in enumerate(words):
            word_str = word + " "
            bbox = font_text.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > card_x + 50 + max_line_w:
                cursor_x = card_x + 50
                cursor_y += line_height

            if w_idx <= active_word_idx:
                w_color = (255, 215, 0) if w_idx == active_word_idx else (240, 245, 255)
            else:
                w_color = (95, 110, 135)

            draw.text((cursor_x, cursor_y), word_str, font=font_text, fill=w_color)
            cursor_x += w_width

        # Subtítulo en Inglés en la base
        draw.line([card_x + 50, card_y + card_h - 90, card_x + card_w - 50, card_y + card_h - 90], fill=(35, 48, 72), width=1)
        draw.text((card_x + 50, card_y + card_h - 65), "EN: " + item["en_sub"], font=font_en, fill=(145, 175, 210))

        # Barra de progreso inferior
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 8, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"cosmic_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 500 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n-> Codificando Masterclass Cósmica 1080p con FFmpeg FastStart...")
    final_output = RUNTIME / "OpenClaw_Masterclass_Cosmica_PNG_1080p.mp4"

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "cosmic_%06d.jpg"),
        "-i", str(master_audio_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_output)
    ]
    subprocess.run(cmd_render, check=True)

    size_mb = final_output.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print("  🏆 MASTERCLASS CÓSMICA 1080P GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print("  Avatar:   PNG 100% Transparente sin marcos")
    print("  Fondo:    Universo en movimiento continuo suave (180 estrellas)")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

if __name__ == "__main__":
    render_cosmic_masterclass()
