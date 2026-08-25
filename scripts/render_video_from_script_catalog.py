"""
==============================================================================
HB.OS 2026 — ORQUESTADOR DINÁMICO DE VIDEO POR ÍNDICE DE GUIONES (V6.0)
==============================================================================
Rompe el bucle de reutilización de audio fijo. Cada script del catálogo
se sintetiza dinámicamente con su texto específico y se ensambla con sus
viñetas e infografías correspondientes.
==============================================================================
"""

import os
import sys
import time
import math
import json
import subprocess
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(r"C:\Users\ipane\.openclaw-master.env")

CATALOG_FILE = ROOT / "backend" / "database" / "script_catalog.json"
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()

WIDTH, HEIGHT = 1920, 1080
FPS = 25

AVATAR_PATH = ROOT / "assets" / "avatar_transparent_hbos.png"
if not AVATAR_PATH.exists():
    AVATAR_PATH = ROOT / "assets" / "avatar_transparent.png"

INFOGRAPHICS = [
    ROOT / "assets" / "slide_1.png",
    ROOT / "assets" / "slide_2.png",
    ROOT / "capturas_recientes" / "Screenshot 2026-08-23 061158.png",
    ROOT / "capturas_recientes" / "Screenshot 2026-08-23 061219.png"
]

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def generate_audio_for_script(script_data, audio_output_path):
    """Sintetiza el audio dinámico con el texto EXACTO del guion seleccionado."""
    print(f"\n[1/3] Sintetizando audio exclusivo para el guión: '{script_data['title']}'...")
    audio_output_path.parent.mkdir(parents=True, exist_ok=True)
    
    script_text = script_data["script_text"]
    
    # Inferencia TTS con ElevenLabs o Edge-TTS Fallback de alta fidelidad
    if ELEVENLABS_KEY:
        headers = {"xi-api-key": ELEVENLABS_KEY}
        voice_id = "pNInz6obpgDQGcFmaJgB" # Perfil Barítono Calibrado Expresivo
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        payload = {
            "text": script_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.42, "similarity_boost": 0.92, "style": 0.30}
        }
        res = requests.post(tts_url, json=payload, headers=headers)
        if res.status_code == 200:
            with open(audio_output_path, "wb") as f:
                f.write(res.content)
            print(f"  ✓ Audio exclusivo generado con ElevenLabs: {audio_output_path.name}")
            return True
            
    # Fallback Edge-TTS
    import edge_tts
    import asyncio
    async def run_edge():
        communicate = edge_tts.Communicate(script_text, "es-MX-JorgeNeural", rate="-6%", pitch="-2Hz")
        await communicate.save(str(audio_output_path))
    asyncio.run(run_edge())
    print(f"  ✓ Audio exclusivo generado con motor neural: {audio_output_path.name}")
    return True

def render_video_by_script_id(script_id="hbos_advancements_2026_08_25"):
    print("=" * 85)
    print(f"  🎬 RENDERING DINÁMICO POR ÍNDICE DE GUIONES: [{script_id}]")
    print("=" * 85)

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    if script_id not in catalog["scripts"]:
        print(f"[!] ID de guión no encontrado: {script_id}")
        return

    script_data = catalog["scripts"][script_id]
    audio_path = ROOT / script_data["audio_file"]
    video_output = ROOT / script_data["video_output"]
    video_output.parent.mkdir(parents=True, exist_ok=True)

    # 1. Generar audio específico si no existe
    if not audio_path.exists():
        generate_audio_for_script(script_data, audio_path)

    # 2. Cargar Avatar HD Transparente
    avatar_img = None
    if AVATAR_PATH.exists():
        avatar_img = Image.open(AVATAR_PATH).convert("RGBA")
        aspect = avatar_img.width / avatar_img.height
        new_h = 880
        new_w = int(new_h * aspect)
        avatar_img = avatar_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Cargar Infografías
    loaded_infos = []
    for p in INFOGRAPHICS:
        if p.exists():
            try:
                im = Image.open(p).convert("RGBA")
                im.thumbnail((500, 360), Image.Resampling.LANCZOS)
                loaded_infos.append(im)
            except:
                pass

    duration_sec = 25
    total_frames = duration_sec * FPS
    font_title = get_font(28)
    font_bullet = get_font(28)

    frames_dir = video_output.parent / "frames"
    frames_dir.mkdir(exist_ok=True)

    # Estrellas
    np.random.seed(42)
    num_stars = 220
    stars_x = np.random.randint(0, WIDTH, num_stars)
    stars_y = np.random.randint(0, HEIGHT, num_stars)
    stars_speed = np.random.uniform(0.6, 2.8, num_stars)
    stars_size = np.random.randint(1, 4, num_stars)

    bullets = script_data["bullets"]

    print(f"\n[2/3] Generando {total_frames} fotogramas Full HD para el guión: '{script_data['title']}'...")

    for i in range(total_frames):
        t = i / FPS

        # A. Fondo Sideral Dinámico
        img = Image.new("RGBA", (WIDTH, HEIGHT), (6, 10, 22, 255))
        draw = ImageDraw.Draw(img)

        for s in range(num_stars):
            sy = (stars_y[s] + t * stars_speed[s] * 22) % HEIGHT
            sx = stars_x[s]
            brightness = int(160 + 90 * math.sin(t * 3.5 + s))
            r_size = stars_size[s]
            draw.ellipse([sx, sy, sx + r_size, sy + r_size], fill=(brightness, brightness, 255, 220))

        # B. Infografías en Disolución Suave (Firmamento)
        if loaded_infos:
            cycle_time = 6.0
            info_idx = int(t / cycle_time) % len(loaded_infos)
            phase = (t % cycle_time) / cycle_time
            alpha = int((phase / 0.2) * 180) if phase < 0.2 else (int(((1.0 - phase) / 0.2) * 180) if phase > 0.8 else 180)
            
            curr_info = loaded_infos[info_idx].copy()
            r, g, b, a = curr_info.split()
            a = a.point(lambda p: int(p * (alpha / 255.0)))
            curr_info.putalpha(a)
            img.paste(curr_info, (80, 180), curr_info)

        # C. Avatar Transparente HD de Guillermo
        if avatar_img:
            avatar_x = WIDTH - avatar_img.width - 30
            avatar_y = HEIGHT - avatar_img.height
            img.paste(avatar_img, (avatar_x, avatar_y), avatar_img)

        # D. Header Superior
        draw.text((80, 45), f"HB OS · {script_data['title'].upper()}", font=font_title, fill=(212, 175, 106, 255))

        # E. Teleprompter por Viñetas (Bullets) al CENTRO (Resaltado Amarillo Vivo #facc15)
        center_x = 420
        center_start_y = 260
        active_bullet = int(t / 5) % len(bullets)

        for b_idx, bullet_text in enumerate(bullets):
            by = center_start_y + b_idx * 70
            if b_idx < active_bullet:
                color = (212, 175, 106, 200)
            elif b_idx == active_bullet:
                color = (250, 204, 21, 255) # Amarillo Vivo
            else:
                color = (180, 195, 215, 140)

            draw.text((center_x, by), bullet_text, font=font_bullet, fill=color)

        frame_path = frames_dir / f"frame_{i:05d}.png"
        img.save(frame_path)

    # 3. Codificar con FFmpeg vinculando el AUDIO EXCLUSIVO de este guión
    print(f"\n[3/3] Codificando MP4 FastStart con el AUDIO EXCLUSIVO de ESE guión...")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-i", str(audio_path),
        "-shortest",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(video_output)
    ]

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\n🏆 [ÉXITO TOTAL] Video Generado para Guión '{script_id}':")
        print(f"   Video: {video_output}")
        print(f"   Audio Vinculado: {audio_path}")
    else:
        print(f"[!] FFmpeg Error: {res.stderr}")

if __name__ == "__main__":
    script_to_run = sys.argv[1] if len(sys.argv) > 1 else "hbos_advancements_2026_08_25"
    render_video_by_script_id(script_to_run)
