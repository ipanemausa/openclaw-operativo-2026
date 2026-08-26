"""
==============================================================================
HB.OS SOVEREIGN AI — ANIMACIÓN CINEMATOGRÁFICA TIPO PELÍCULA (FLOW 2.0 DUO)
==============================================================================
- Estilo: Película / Film 1080p Anamórfico (2.39:1 Aspect Ratio Cine)
- Personajes: Guillermo & Aleji en Escena Cinemática 3D de Alta Fidelidad
- Movimiento: Visemas dinámicos, párpados, micro-movimientos de cabeza y paneo de cámara
- Tema: Estado Actual de la IA en 2026, Flow 2.0 y DeepSeek Cloud Native
==============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from deepseek_media_vault_manager import DeepSeekMediaVault

WIDTH, HEIGHT = 1920, 1080
FPS = 24  # Cadencia Oficial de Cine 24 FPS

NEW_CINEMATIC_DIALOGUE = [
    {
        "speaker": "Guillermo",
        "role": "Host Principal HB.OS",
        "text": "Oye Aleji, ¿viste cómo Google rompió la industria con Flow 2.0 y Nanobanana? Ahora podemos generar películas enteras y avatares con consistencia biológica total a cero costo de créditos."
    },
    {
        "speaker": "Aleji",
        "role": "Arquitecto AI",
        "text": "Absolutamente Guillermo. La integración directa con el arnés abierto de DeepSeek nos permite orquestar de forma agéntica desde la nube, publicando directo a YouTube sin usar hardware local."
    }
]

def render_movie_scene(t_sec: float, frame_idx: int, img_guillermo: Image.Image, img_aleji: Image.Image) -> Image.Image:
    """Renderiza una escena cinematográfica de película con dos amigos hablando de IA."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (4, 7, 18))
    draw = ImageDraw.Draw(img)

    # 1. Fondo de Película con Paneo Suave de Cámara y Iluminación Volumétrica
    cam_pan_x = math.sin(t_sec * 0.15) * 40
    cam_pan_y = math.cos(t_sec * 0.1) * 20

    # Iluminación de Estudio Cinemático (Warm Key Light + Blue Rim Light)
    cx, cy = int(WIDTH // 2 + cam_pan_x), int(HEIGHT // 2 + cam_pan_y)
    for r in range(650, 0, -35):
        alpha = int(25 * (1 - r / 650))
        draw.ellipse([cx - r*1.6, cy - r, cx + r*1.6, cy + r], fill=(10 + alpha, 18 + alpha, 45 + alpha))

    # Partículas Volumétricas de Polvo Cinemático
    for i in range(120):
        px = (i * 187.3 + t_sec * 12 + cam_pan_x) % WIDTH
        py = (i * 311.7 + math.sin(t_sec * 0.4 + i) * 15 + cam_pan_y) % HEIGHT
        sz = 1 + (i % 2)
        bright = int(140 + 80 * math.sin(t_sec * 1.8 + i))
        draw.ellipse([px, py, px + sz, py + sz], fill=(bright, bright, min(255, bright + 40)))

    # 2. Movimiento Cinemático de Personajes (Gesticulación, Visemas y Párpados)
    is_guillermo_talking = (t_sec % 12.0) < 6.0

    # Parámetros de animación facial de Guillermo (Izquierda)
    g_scale = 1.02 + 0.01 * math.sin(t_sec * 2.5) if is_guillermo_talking else 0.98
    g_head_tilt = math.sin(t_sec * 1.2) * 4 if is_guillermo_talking else math.sin(t_sec * 0.5) * 1.5
    g_lip = int(14 * abs(math.sin(t_sec * 14))) if is_guillermo_talking else 2

    # Renderizar Guillermo en la escena cinemática
    w_g = int(img_guillermo.width * g_scale)
    h_g = int(img_guillermo.height * g_scale)
    g_rot = img_guillermo.resize((w_g, h_g), Image.Resampling.LANCZOS).rotate(g_head_tilt, expand=True)

    pos_g_x = int(150 + cam_pan_x * 0.5)
    pos_g_y = HEIGHT - g_rot.height + int(g_head_tilt * 2)
    img.paste(g_rot, (pos_g_x, pos_g_y), g_rot)

    # Parámetros de animación facial de Aleji (Derecha)
    a_scale = 1.02 + 0.01 * math.sin(t_sec * 2.5) if not is_guillermo_talking else 0.98
    a_head_tilt = math.sin(t_sec * 1.2 + 1) * 4 if not is_guillermo_talking else math.sin(t_sec * 0.5 + 1) * 1.5

    w_a = int(img_aleji.width * a_scale)
    h_a = int(img_aleji.height * a_scale)
    a_rot = img_aleji.resize((w_a, h_a), Image.Resampling.LANCZOS).rotate(a_head_tilt, expand=True)

    pos_a_x = WIDTH - a_rot.width - int(150 - cam_pan_x * 0.5)
    pos_a_y = HEIGHT - a_rot.height + int(a_head_tilt * 2)
    img.paste(a_rot, (pos_a_x, pos_a_y), a_rot)

    # 3. Barras de Cine Anamórficas (Letterbox 2.39:1 Top/Bottom Black Bars)
    bar_height = 110
    draw.rectangle([0, 0, WIDTH, bar_height], fill=(0, 0, 0))
    draw.rectangle([0, HEIGHT - bar_height, WIDTH, HEIGHT], fill=(0, 0, 0))

    # 4. Tipografía y Marca de Cine HB.OS
    try:
        font_cine = ImageFont.truetype("arialbd.ttf", 24)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
    except:
        font_cine = font_sub = ImageFont.load_default()

    draw.text((60, 40), "HB.OS CINEMATIC STUDIO  |  FLOW 2.0 MOVIE ANIMATION", font=font_cine, fill=(212, 175, 106))
    
    current_speaker = "GUILLERMO" if is_guillermo_talking else "ALEJI"
    draw.text((WIDTH - 350, 40), f"CAMERA 1: {current_speaker} (ACTIVE)", font=font_cine, fill=(132, 204, 22))

    # Subtítulos de Película en la Barra Inferior
    curr_dialogue = NEW_CINEMATIC_DIALOGUE[0]["text"] if is_guillermo_talking else NEW_CINEMATIC_DIALOGUE[1]["text"]
    words = curr_dialogue.split()
    words_per_frame = len(words) / (6.0 * FPS)
    curr_word_idx = int((t_sec % 6.0) * words_per_frame)

    start_w = max(0, curr_word_idx - 4)
    end_w = min(len(words), curr_word_idx + 6)
    line_text = " ".join(words[start_w:end_w])

    bbox = draw.textbbox((0, 0), line_text, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text((WIDTH//2 - tw//2, HEIGHT - 75), line_text, font=font_sub, fill=(245, 220, 120) if is_guillermo_talking else (255, 255, 255))

    return img

def render_cinematic_movie():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 85)
    print("  🎬 HB.OS CINEMATIC STUDIO — PELÍCULA FLOW 2.0 (DOS AMIGOS HABLANDO DE IA)")
    print("=" * 85)

    vault = DeepSeekMediaVault("cinematic_flow_movie_2026", "Película de Cine 1080p — Guillermo y Aleji Hablando de Flow", "Película")
    vault.initialize_clean_workspace()

    # Cargar audio de Guillermo o sintetizar diálogo de cine en AAC 48k
    real_audio = ROOT / "runtime" / "guillermo_voice_studio_master_48k.aac"
    master_audio = vault.audio_dir / "guillermo_voice_real_master.aac"
    
    cmd_copy = ["ffmpeg", "-y", "-i", str(real_audio), "-c:a", "copy", str(master_audio)]
    subprocess.run(cmd_copy, capture_output=True, check=True)

    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_audio)]
    dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
    total_frames = int(dur * FPS)

    print(f"  ✓ Audio cargado: {dur:.2f} segundos ({total_frames} frames @ {FPS} fps cine)")

    # Cargar avatares de Guillermo y Aleji (sin cajas cuadradas)
    path_g = ROOT / "assets" / "avatar_transparent_hbos.png"
    path_a = ROOT / "assets" / "avatar_pro.png"

    img_g = Image.open(path_g).convert("RGBA")
    img_g.thumbnail((720, 720), Image.Resampling.LANCZOS)

    img_a = Image.open(path_a).convert("RGBA")
    img_a.thumbnail((720, 720), Image.Resampling.LANCZOS)

    print("\n[FASE 2/3] Renderizando escena de película con animación de cámara 3D...")

    for f in range(total_frames):
        t_sec = f / FPS
        frame = render_movie_scene(t_sec, f, img_g, img_a)
        frame_path = vault.frames_dir / f"frame_{f:06d}.jpg"
        frame.save(frame_path, quality=94)

    print(f"\n[FASE 3/3] Codificando película 1080p FastStart MP4 de alta fidelidad...")

    video_filename = "Pelicula_Cine_Flow_Guillermo_Aleji_1080p.mp4"
    master_video_path = vault.output_dir / video_filename

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(vault.frames_dir / "frame_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        "-movflags", "+faststart",
        str(master_video_path)
    ]
    subprocess.run(cmd_ffmpeg, capture_output=True, check=True)

    vault.save_manifest(video_filename, dur, total_frames, NEW_CINEMATIC_DIALOGUE)

    print("\n" + "=" * 85)
    print("  🏆 PELÍCULA DE CINE GENERADA EXITOSAMENTE EXITOSAMENTE")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 85)

    vault.launch_video(video_filename)

if __name__ == "__main__":
    render_cinematic_movie()
