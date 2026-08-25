"""
==============================================================================
HB.OS 2026 — MASTERCLASS VIDEO HD: ESPACIO SIDERAL, ASSETS PNG TRANSPARENTES,
TELEPROMPTER BULLETS WORD-KARAOKE & VOZ AUTÉNTICA DE GUILLERMO HOYOS
==============================================================================
"""

import os
import sys
import time
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "runtime" / "productions" / "guillermo_authentic_hd_masterpiece"
RUNTIME.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RUNTIME / "GUILLERMO_HOYOS_HBOS_AUTHENTIC_HD_MASTERPIECE_1080P.mp4"
AUDIO_TRACK = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"

# Dimensiones 1080p
WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Cargar assets PNG transparentes HD
ASSETS_DIR = ROOT / "assets" / "capturas_deepmind"
BG_ASSETS = list(ASSETS_DIR.glob("*.png")) if ASSETS_DIR.exists() else []

# Avatar HD transparente
AVATAR_PATH = ROOT / "assets" / "guillermo_avatar_transparent.png"
if not AVATAR_PATH.exists():
    AVATAR_PATH = ROOT / "frontend" / "public" / "avatars" / "guillermo_transparent.png"

# Puntos clave del Teleprompter por Viñetas (Bullets)
BULLETS = [
    "1. HB OS · Fábrica de IA Soberana y Descentralizada",
    "2. Macroeconomía de Abundancia & Costo Marginal -> $0.00",
    "3. Integración Directa: NVIDIA, DeepSeek, Alibaba & OpenAI",
    "4. Factorización Métrica R^768 (BAAI/bge-m3) & Cero Temp Bloat",
    "5. Arnés de Ingeniería Autónoma: CPM DAG & Backup Rclone 5TB"
]

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def render_masterpiece_frames():
    print("=" * 80)
    print("  🎬 PRODUCIENDO VIDEO HD CON ESPACIO SIDERAL, ASSETS PNG TRANSPARENTES")
    print("     TELEPROMPTER BULLETS WORD-KARAOKE & VOZ REAL AUTÉNTICA DE GUILLERMO")
    print("=" * 80)

    # Cargar avatar
    avatar_img = None
    if AVATAR_PATH.exists():
        avatar_img = Image.open(AVATAR_PATH).convert("RGBA")
        # Escalar Lanczos a altura proporcional 800px
        aspect = avatar_img.width / avatar_img.height
        new_h = 820
        new_w = int(new_h * aspect)
        avatar_img = avatar_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Duración basada en audio o 30 segundos de muestra HD
    duration_sec = 30
    total_frames = duration_sec * FPS
    
    font_title = get_font(32)
    font_bullet = get_font(26)
    font_badge = get_font(20)

    frames_dir = RUNTIME / "frames"
    frames_dir.mkdir(exist_ok=True)

    # Pre-generar estrellas del espacio sideral
    np.random.seed(42)
    num_stars = 180
    stars_x = np.random.randint(0, WIDTH, num_stars)
    stars_y = np.random.randint(0, HEIGHT, num_stars)
    stars_speed = np.random.uniform(0.5, 2.5, num_stars)
    stars_size = np.random.randint(1, 4, num_stars)

    print(f"\n[FASE 1/2] Renderizando {total_frames} fotogramas Full HD 1080p @ {FPS}fps...")

    for i in range(total_frames):
        t = i / FPS
        
        # 1. Fondo Espacio Sideral en Movimiento (Gradiente Dinámico HSL + Estrellas Paralaje)
        img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 14, 26, 255))
        draw = ImageDraw.Draw(img)

        # Mover estrellas
        for s in range(num_stars):
            sy = (stars_y[s] + t * stars_speed[s] * 20) % HEIGHT
            sx = stars_x[s]
            brightness = int(180 + 75 * math.sin(t * 3 + s))
            r_size = stars_size[s]
            draw.ellipse([sx, sy, sx + r_size, sy + r_size], fill=(brightness, brightness, 255, 230))

        # 2. Asset PNG Transparente HD flotante en el Background (Infografía / Banco IA)
        if BG_ASSETS:
            asset_idx = int(t / 6) % len(BG_ASSETS)
            bg_asset_path = BG_ASSETS[asset_idx]
            try:
                asset_img = Image.open(bg_asset_path).convert("RGBA")
                # Escalar e insertar en zona izquierda-centro con opacidad suave
                asset_img.thumbnail((550, 400), Image.Resampling.LANCZOS)
                # Crear fondo bioluminiscente alrededor del asset
                draw.rectangle([80, 220, 80 + asset_img.width + 20, 220 + asset_img.height + 20], fill=(20, 30, 65, 160), outline=(50, 100, 220, 200), width=2)
                img.paste(asset_img, (90, 230), asset_img)
            except Exception:
                pass

        # 3. Avatar Transparente HD de Guillermo (Posición Derecha con sombra paralela)
        if avatar_img:
            avatar_x = WIDTH - avatar_img.width - 80
            avatar_y = HEIGHT - avatar_img.height - 20
            # Sombra paralela bioluminiscente
            shadow = Image.new("RGBA", avatar_img.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.rectangle([0, 0, avatar_img.width, avatar_img.height], fill=(0, 150, 255, 30))
            img.paste(shadow, (avatar_x + 10, avatar_y + 10), shadow)
            img.paste(avatar_img, (avatar_x, avatar_y), avatar_img)

        # 4. Header Top Badge: HB.OS (SOVEREIGN AI)
        draw.rectangle([60, 40, 680, 95], fill=(15, 23, 42, 220), outline=(0, 220, 255, 255), width=2)
        draw.text((80, 53), "HB.OS (SOVEREIGN AI) · HIGH DEFINITION STUDIO", font=font_title, fill=(0, 220, 255, 255))

        # 5. Teleprompter por Viñetas (Bullets) con Karaoke Word Highlight
        bullet_box_x = 80
        bullet_box_y = 660
        draw.rectangle([bullet_box_x, bullet_box_y, bullet_box_x + 1100, bullet_box_y + 360], fill=(10, 16, 32, 230), outline=(212, 175, 106, 255), width=2)
        
        # Título del Teleprompter
        draw.text((bullet_box_x + 20, bullet_box_y + 15), "TELEPROMPTER MAESTRO · RUTA CRÍTICA & ARQUITECTURA", font=font_bullet, fill=(212, 175, 106, 255))

        # Resaltado activo por tiempo (Karaoke highlight)
        active_bullet = int(t / 5) % len(BULLETS)

        for b_idx, bullet_text in enumerate(BULLETS):
            by = bullet_box_y + 60 + b_idx * 55
            if b_idx < active_bullet:
                # Viñetas pasadas (Dorado HB)
                color = (212, 175, 106, 220)
                prefix = "✓ "
            elif b_idx == active_bullet:
                # Viñeta activa (Verde Neón Karaoke + Fondo de Resalte)
                draw.rectangle([bullet_box_x + 15, by - 5, bullet_box_x + 1080, by + 40], fill=(30, 60, 20, 200), outline=(132, 204, 22, 255), width=1)
                color = (132, 204, 22, 255)
                prefix = "▶ "
            else:
                # Viñetas futuras (Gris suave)
                color = (160, 175, 200, 180)
                prefix = "• "

            draw.text((bullet_box_x + 30, by + 4), prefix + bullet_text, font=font_bullet, fill=color)

        frame_path = frames_dir / f"frame_{i:05d}.png"
        img.save(frame_path)

    print("\n[FASE 2/2] Ensamblando video Full HD con FFmpeg FastStart...")

    # Comando FFmpeg para codificar a 1080p FastStart
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%05d.png")
    ]

    if AUDIO_TRACK.exists():
        ffmpeg_cmd.extend(["-i", str(AUDIO_TRACK), "-shortest"])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUTPUT_VIDEO)
    ])

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\n🏆 [ÉXITO TOTAL] Video HD Generado:")
        print(f"   Archivo: {OUTPUT_VIDEO}")
        print(f"   Especificaciones: 1920x1080 Full HD @ 25fps | FastStart MP4 | Audio 48kHz")
        print(f"   Branding: HB.OS (SOVEREIGN AI)")
    else:
        print(f"[!] FFmpeg Error: {res.stderr}")

if __name__ == "__main__":
    render_masterpiece_frames()
