"""
==============================================================================
HB.OS 2026 — MASTERCLASS VIDEO V4.0: DISOLUCIÓN SUAVE EN EL FIRMAMENTO
TELEPROMPTER EN BULLETS FLOTANTE AL CENTRO CON RESALTADO AMARILLO
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
RUNTIME = ROOT / "runtime" / "productions" / "guillermo_real_voice_masterclass_v4"
RUNTIME.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = RUNTIME / "GUILLERMO_REAL_VOICE_MASTERCLASS_V4_1080P.mp4"
REAL_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

AVATAR_PATH = ROOT / "assets" / "avatar_transparent_hbos.png"
if not AVATAR_PATH.exists():
    AVATAR_PATH = ROOT / "assets" / "avatar_transparent.png"

# Infografías para disolución suave en el firmamento
INFOGRAPHICS = [
    ROOT / "assets" / "slide_1.png",
    ROOT / "assets" / "slide_2.png",
    ROOT / "capturas_recientes" / "Screenshot 2026-08-23 061158.png",
    ROOT / "capturas_recientes" / "Screenshot 2026-08-23 061219.png"
]

# Viñetas del Teleprompter al Centro (Bullets)
TELEPROMPTER_BULLETS = [
    "• HB OS · Fábrica de Inteligencia Artificial Soberana",
    "• Inferencia Serverless: DeepSeek R1, Qwen 2.5 & Kimi K3",
    "• Factorización R^768 (BAAI/bge-m3) & Cero Temp Bloat",
    "• Ruta Crítica CPM DAG: Ejecución Autónoma Desatendida",
    "• Sincronización Automática: GitHub + Drive 5TB + Firebase"
]

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def render_v4_masterpiece():
    print("=" * 85)
    print("  🎬 PRODUCIENDO MASTERCLASS V4.0 — DISOLUCIÓN SUAVE & BULLETS AMARILLOS AL CENTRO")
    print("=" * 85)

    # 1. Avatar HD Transparente
    avatar_img = None
    if AVATAR_PATH.exists():
        avatar_img = Image.open(AVATAR_PATH).convert("RGBA")
        aspect = avatar_img.width / avatar_img.height
        new_h = 880
        new_w = int(new_h * aspect)
        avatar_img = avatar_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Pre-cargar imágenes para disolución suave
    loaded_infos = []
    for p in INFOGRAPHICS:
        if p.exists():
            try:
                im = Image.open(p).convert("RGBA")
                im.thumbnail((500, 360), Image.Resampling.LANCZOS)
                loaded_infos.append(im)
            except:
                pass

    duration_sec = 30
    total_frames = duration_sec * FPS

    font_title = get_font(28)
    font_bullet = get_font(30)

    frames_dir = RUNTIME / "frames"
    frames_dir.mkdir(exist_ok=True)

    # Estrellas del Espacio Sideral
    np.random.seed(42)
    num_stars = 220
    stars_x = np.random.randint(0, WIDTH, num_stars)
    stars_y = np.random.randint(0, HEIGHT, num_stars)
    stars_speed = np.random.uniform(0.6, 2.8, num_stars)
    stars_size = np.random.randint(1, 4, num_stars)

    print(f"\n[1/2] Renderizando {total_frames} fotogramas Full HD 1080p...")

    for i in range(total_frames):
        t = i / FPS

        # A. Fondo Sideral Dinámico
        img = Image.new("RGBA", (WIDTH, HEIGHT), (6, 10, 22, 255))
        draw = ImageDraw.Draw(img)

        # Mover Estrellas
        for s in range(num_stars):
            sy = (stars_y[s] + t * stars_speed[s] * 22) % HEIGHT
            sx = stars_x[s]
            brightness = int(160 + 90 * math.sin(t * 3.5 + s))
            r_size = stars_size[s]
            draw.ellipse([sx, sy, sx + r_size, sy + r_size], fill=(brightness, brightness, 255, 220))

        # B. Imágenes en Disolución Suave (Fade-In / Fade-Out) en el Firmamento (Izquierda Superior)
        if loaded_infos:
            cycle_time = 7.5 # segundos por imagen
            info_idx = int(t / cycle_time) % len(loaded_infos)
            phase = (t % cycle_time) / cycle_time # 0.0 a 1.0
            
            # Opacidad suave: fade-in primeros 1.5s, fade-out ultimos 1.5s
            if phase < 0.2:
                alpha = int((phase / 0.2) * 180)
            elif phase > 0.8:
                alpha = int(((1.0 - phase) / 0.2) * 180)
            else:
                alpha = 180

            curr_info = loaded_infos[info_idx].copy()
            # Aplicar opacidad alfa
            r, g, b, a = curr_info.split()
            a = a.point(lambda p: int(p * (alpha / 255.0)))
            curr_info.putalpha(a)

            img.paste(curr_info, (80, 180), curr_info)

        # C. Avatar Transparente HD de Guillermo (Respetando Espacio a la Derecha)
        if avatar_img:
            avatar_x = WIDTH - avatar_img.width - 30
            avatar_y = HEIGHT - avatar_img.height
            img.paste(avatar_img, (avatar_x, avatar_y), avatar_img)

        # D. Header Superior Minimalista: HB OS (SOVEREIGN AI)
        draw.text((80, 45), "HB OS · SOVEREIGN AI & ARCHITECTURE STUDIO", font=font_title, fill=(212, 175, 106, 255))

        # E. Teleprompter por Viñetas (Bullets) Flotando al CENTRO de la Pantalla (CERO CAJAS)
        center_x = 420
        center_start_y = 260
        
        active_bullet = int(t / 6) % len(TELEPROMPTER_BULLETS)

        for b_idx, bullet_text in enumerate(TELEPROMPTER_BULLETS):
            by = center_start_y + b_idx * 70

            if b_idx < active_bullet:
                # Viñetas pasadas (Dorado suave)
                color = (212, 175, 106, 200)
            elif b_idx == active_bullet:
                # Viñeta activa (Resaltado Amarillo Vivo #facc15)
                color = (250, 204, 21, 255)
            else:
                # Viñetas futuras (Blanco grisáceo suave)
                color = (180, 195, 215, 140)

            # Dibujar texto flotante directo sin recuadro ni caja
            draw.text((center_x, by), bullet_text, font=font_bullet, fill=color)

        frame_path = frames_dir / f"frame_{i:05d}.png"
        img.save(frame_path)

    # 2. Codificar con FFmpeg FastStart utilizando la VOZ REAL GRABADA DE GUILLERMO
    print("\n[2/2] Ensamblando video V4.0 con la VOZ REAL GRABADA de Guillermo...")

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
        print(f"\n🏆 [ÉXITO TOTAL] Video Masterclass V4.0 Generado:")
        print(f"   Archivo: {OUTPUT_VIDEO}")
        print(f"   Diseño: Bullets al Centro Flotante (Amarillo #facc15) + Imágenes en Disolución Suave en el Firmamento")
    else:
        print(f"[!] FFmpeg Error: {res.stderr}")

if __name__ == "__main__":
    render_v4_masterpiece()
