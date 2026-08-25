"""
==============================================================================
HB.OS 2026 — MASTERCLASS DEFINITIVA V3.0 (VOZ REAL DE GUILLERMO GRABADA)
==============================================================================
- Audio: Voz real auténtica de Guillermo (Guillermo_Podcast_Master_Edit_48k.wav)
- Visual: Fondo Espacio Sideral + Infografías PNG HD (OpenAI, NVIDIA, DeepSeek, DeepMind)
- Avatar: Guillermo PNG Transparente HD con insignia HB.OS (SOVEREIGN AI)
- Teleprompter: Cajas de viñetas con resaltado activo en Verde Neón (#84cc16)
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
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "runtime" / "productions" / "guillermo_real_voice_masterclass_v3"
RUNTIME.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RUNTIME / "GUILLERMO_REAL_VOICE_MASTERCLASS_V3_1080P.mp4"
REAL_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

AVATAR_PATH = ROOT / "assets" / "avatar_transparent_hbos.png"
if not AVATAR_PATH.exists():
    AVATAR_PATH = ROOT / "assets" / "avatar_transparent.png"

# Infografías y capturas de frontera
INFOGRAPHICS = [
    ROOT / "assets" / "slide_1.png",
    ROOT / "assets" / "slide_2.png",
    ROOT / "capturas_recientes" / "Screenshot 2026-08-23 061158.png",
    ROOT / "capturas_recientes" / "Screenshot 2026-08-23 061219.png"
]

# Puntos clave del Teleprompter que resumen el trabajo real de hoy
TELEPROMPTER_BULLETS = [
    "1. HB OS · Fábrica de IA Soberana y Descentralizada (Guillermo Hoyos)",
    "2. Matriz Core: Inferencia Serverless DeepSeek-R1, Qwen 2.5 & Kimi K3",
    "3. Factorización Métrica R^768 (BAAI/bge-m3) & Cero Archivos Temporales",
    "4. Ruta Crítica CPM DAG: Orquestación Desatendida sin Bucles conversacionales",
    "5. Pipeline de Cierre: GitHub + Google Drive 5TB (rclone) + Firebase Cloud"
]

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def render_v3_masterpiece():
    print("=" * 85)
    print("  🎬 PRODUCIENDO MASTERCLASS V3.0 CON LA VOZ REAL DE GUILLERMO (AUDIO GRABADO)")
    print("     ESPACIO SIDERAL, INFOGRAFÍAS PNG HD & TELEPROMPTER POR VIÑETAS KARAOKE")
    print("=" * 85)

    # 1. Cargar Avatar HD Transparente
    avatar_img = None
    if AVATAR_PATH.exists():
        avatar_img = Image.open(AVATAR_PATH).convert("RGBA")
        aspect = avatar_img.width / avatar_img.height
        new_h = 850
        new_w = int(new_h * aspect)
        avatar_img = avatar_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 2. Renderizar frames (30 segundos para muestra en alta definición 1080p)
    duration_sec = 30
    total_frames = duration_sec * FPS
    
    font_title = get_font(30)
    font_bullet = get_font(24)
    font_sub = get_font(18)

    frames_dir = RUNTIME / "frames"
    frames_dir.mkdir(exist_ok=True)

    # Pre-generar estrellas
    np.random.seed(42)
    num_stars = 200
    stars_x = np.random.randint(0, WIDTH, num_stars)
    stars_y = np.random.randint(0, HEIGHT, num_stars)
    stars_speed = np.random.uniform(0.8, 3.0, num_stars)
    stars_size = np.random.randint(1, 4, num_stars)

    print(f"\n[1/2] Generando {total_frames} fotogramas Full HD 1080p...")

    for i in range(total_frames):
        t = i / FPS
        
        # A. Fondo Espacio Sideral Dinámico
        img = Image.new("RGBA", (WIDTH, HEIGHT), (8, 12, 24, 255))
        draw = ImageDraw.Draw(img)

        # Mover estrellas
        for s in range(num_stars):
            sy = (stars_y[s] + t * stars_speed[s] * 25) % HEIGHT
            sx = stars_x[s]
            brightness = int(170 + 85 * math.sin(t * 4 + s))
            r_size = stars_size[s]
            draw.ellipse([sx, sy, sx + r_size, sy + r_size], fill=(brightness, brightness, 255, 230))

        # B. Infografías de Inteligencia Artificial (NVIDIA, DeepSeek, DeepMind, OpenAI)
        info_idx = int(t / 7.5) % len(INFOGRAPHICS)
        info_path = INFOGRAPHICS[info_idx]
        if info_path.exists():
            try:
                info_img = Image.open(info_path).convert("RGBA")
                info_img.thumbnail((600, 420), Image.Resampling.LANCZOS)
                # Marco bioluminiscente alrededor de la infografía HD
                box_x, box_y = 70, 200
                draw.rectangle([box_x - 10, box_y - 10, box_x + info_img.width + 10, box_y + info_img.height + 10], fill=(15, 25, 50, 180), outline=(0, 200, 255, 220), width=2)
                img.paste(info_img, (box_x, box_y), info_img)
                draw.text((box_x, box_y + info_img.height + 15), f"INFOGRAFÍA ARQUITECTÓNICA DE FRONTERA [{info_idx+1}/4]", font=font_sub, fill=(0, 200, 255, 255))
            except Exception as e:
                pass

        # C. Avatar Transparente HD de Guillermo (A la derecha de la pantalla)
        if avatar_img:
            avatar_x = WIDTH - avatar_img.width - 50
            avatar_y = HEIGHT - avatar_img.height - 10
            # Sombra sutil de profundidad
            shadow = Image.new("RGBA", avatar_img.size, (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shadow)
            s_draw.rectangle([0, 0, avatar_img.width, avatar_img.height], fill=(0, 120, 220, 25))
            img.paste(shadow, (avatar_x + 12, avatar_y + 12), shadow)
            img.paste(avatar_img, (avatar_x, avatar_y), avatar_img)

        # D. Header de Marca Oficial: HB OS (SOVEREIGN AI)
        draw.rectangle([60, 40, 720, 100], fill=(12, 20, 38, 230), outline=(212, 175, 106, 255), width=2)
        draw.text((80, 55), "HB OS · SOVEREIGN AI & ARCHITECTURE STUDIO", font=font_title, fill=(212, 175, 106, 255))

        # E. Teleprompter por Viñetas (Bullets) con Karaoke Word Highlight
        bullet_box_x = 70
        bullet_box_y = 660
        draw.rectangle([bullet_box_x, bullet_box_y, bullet_box_x + 1150, bullet_box_y + 370], fill=(10, 16, 32, 240), outline=(0, 220, 255, 255), width=2)
        
        draw.text((bullet_box_x + 25, bullet_box_y + 15), "TELEPROMPTER EN VIVO · RUTA CRÍTICA & GOBERNANZA R^768", font=font_title, fill=(0, 220, 255, 255))

        active_bullet = int(t / 6) % len(TELEPROMPTER_BULLETS)

        for b_idx, bullet_text in enumerate(TELEPROMPTER_BULLETS):
            by = bullet_box_y + 65 + b_idx * 55
            if b_idx < active_bullet:
                color = (212, 175, 106, 220)
                prefix = "✓ "
            elif b_idx == active_bullet:
                # Viñeta activa en Verde Neón
                draw.rectangle([bullet_box_x + 20, by - 4, bullet_box_x + 1130, by + 42], fill=(25, 55, 20, 220), outline=(132, 204, 22, 255), width=1)
                color = (132, 204, 22, 255)
                prefix = "▶ "
            else:
                color = (160, 175, 200, 170)
                prefix = "• "

            draw.text((bullet_box_x + 35, by + 5), prefix + bullet_text, font=font_bullet, fill=color)

        frame_path = frames_dir / f"frame_{i:05d}.png"
        img.save(frame_path)

    # 3. Codificar con FFmpeg FastStart utilizando la VOZ REAL GRABADA DE GUILLERMO
    print("\n[2/2] Ensamblando video Full HD con la VOZ REAL GRABADA de Guillermo...")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-i", str(REAL_AUDIO),
        "-shortest",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUTPUT_VIDEO)
    ]

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\n🏆 [ÉXITO TOTAL] Video Masterclass V3.0 Generado:")
        print(f"   Archivo: {OUTPUT_VIDEO}")
        print(f"   Audio: Voz Real Auténtica Grabada de Guillermo")
        print(f"   Visual: Fondo Sideral + Infografías HD + Avatar Transparente + Teleprompter Karaoke")
    else:
        print(f"[!] FFmpeg Error: {res.stderr}")

if __name__ == "__main__":
    render_v3_masterpiece()
