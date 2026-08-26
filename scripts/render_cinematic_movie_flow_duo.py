"""
==============================================================================
HB.OS SOVEREIGN AI — CINEMATIC MOVIE: DOS VARIANTES DE GUILLERMO HABLANDO DE IA & FLOW
==============================================================================
- Amigos en Escena: DOS VARIANTES DE GUILLERMO (Diferente Vestuario y Look)
  * Amigo 1 (Izquierda): Guillermo Ejecutivo (Traje Oscuro Formal)
  * Amigo 2 (Derecha): Guillermo Tech Founder (Tech Hoodie & Gorra HB.OS)
- Formato: 1080p 24FPS Cine Anamórfico (2.39:1 Aspect Ratio)
- Audio: 100% TU VOZ REAL DE GUILLERMO (runtime/guillermo_voice_studio_master_48k.aac)
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

REAL_AUDIO_PATH = ROOT / "runtime" / "guillermo_voice_studio_master_48k.aac"

GUILLERMO_DUO_DIALOGUE = [
    {
        "speaker": "Guillermo Ejecutivo",
        "text": "Hola Guillermo Tech. Mira la potencia de Flow 2.0: creamos avatares infinitos y videos a costo cero con tu voz real."
    },
    {
        "speaker": "Guillermo Tech Founder",
        "text": "Totalmente acuerdo Guillermo. Con el arnés abierto de DeepSeek en la nube, publicamos directo a YouTube sin usar la PC."
    }
]

def render_movie_guillermo_duo_scene(t_sec: float, frame_idx: int, img_g_exec: Image.Image, img_g_tech: Image.Image) -> Image.Image:
    """Renderiza una escena cinematográfica de película con dos avatares de Guillermo (diferente vestuario/look)."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (4, 7, 18))
    draw = ImageDraw.Draw(img)

    # 1. Paneo de Cámara 3D & Iluminación Volumétrica de Película
    cam_pan_x = math.sin(t_sec * 0.15) * 40
    cam_pan_y = math.cos(t_sec * 0.1) * 20

    cx, cy = int(WIDTH // 2 + cam_pan_x), int(HEIGHT // 2 + cam_pan_y)
    for r in range(650, 0, -35):
        alpha = int(25 * (1 - r / 650))
        draw.ellipse([cx - r*1.6, cy - r, cx + r*1.6, cy + r], fill=(10 + alpha, 18 + alpha, 45 + alpha))

    # Partículas de Polvo Cinemático
    for i in range(120):
        px = (i * 187.3 + t_sec * 12 + cam_pan_x) % WIDTH
        py = (i * 311.7 + math.sin(t_sec * 0.4 + i) * 15 + cam_pan_y) % HEIGHT
        sz = 1 + (i % 2)
        bright = int(140 + 80 * math.sin(t_sec * 1.8 + i))
        draw.ellipse([px, py, px + sz, py + sz], fill=(bright, bright, min(255, bright + 40)))

    # 2. Alternancia de Habla entre Guillermo Ejecutivo (Izquierda) y Guillermo Tech (Derecha)
    is_exec_talking = (t_sec % 12.0) < 6.0

    # Guillermo Ejecutivo (Izquierda - Traje Oscuro)
    g1_scale = 1.03 + 0.01 * math.sin(t_sec * 2.5) if is_exec_talking else 0.97
    g1_head_tilt = math.sin(t_sec * 1.2) * 3.5 if is_exec_talking else math.sin(t_sec * 0.5) * 1.2

    w_g1 = int(img_g_exec.width * g1_scale)
    h_g1 = int(img_g_exec.height * g1_scale)
    g1_rot = img_g_exec.resize((w_g1, h_g1), Image.Resampling.LANCZOS).rotate(g1_head_tilt, expand=True)

    pos_g1_x = int(140 + cam_pan_x * 0.5)
    pos_g1_y = HEIGHT - g1_rot.height + int(g1_head_tilt * 2)
    img.paste(g1_rot, (pos_g1_x, pos_g1_y), g1_rot)

    # Guillermo Tech Founder (Derecha - Look Casual Hoodie/Gorra)
    g2_scale = 1.03 + 0.01 * math.sin(t_sec * 2.5) if not is_exec_talking else 0.97
    g2_head_tilt = math.sin(t_sec * 1.2 + 1) * 3.5 if not is_exec_talking else math.sin(t_sec * 0.5 + 1) * 1.2

    w_g2 = int(img_g_tech.width * g2_scale)
    h_g2 = int(img_g_tech.height * g2_scale)
    g2_rot = img_g_tech.resize((w_g2, h_g2), Image.Resampling.LANCZOS).rotate(g2_head_tilt, expand=True)

    pos_g2_x = WIDTH - g2_rot.width - int(140 - cam_pan_x * 0.5)
    pos_g2_y = HEIGHT - g2_rot.height + int(g2_head_tilt * 2)
    img.paste(g2_rot, (pos_g2_x, pos_g2_y), g2_rot)

    # 3. Letterbox Anamórfico de Cine (2.39:1)
    bar_height = 110
    draw.rectangle([0, 0, WIDTH, bar_height], fill=(0, 0, 0))
    draw.rectangle([0, HEIGHT - bar_height, WIDTH, HEIGHT], fill=(0, 0, 0))

    try:
        font_cine = ImageFont.truetype("arialbd.ttf", 24)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
    except:
        font_cine = font_sub = ImageFont.load_default()

    draw.text((60, 40), "HB.OS CINEMATIC STUDIO  |  DOS VARIANTES DE GUILLERMO (IA & FLOW)", font=font_cine, fill=(212, 175, 106))
    
    active_name = "GUILLERMO EJECUTIVO" if is_exec_talking else "GUILLERMO TECH FOUNDER"
    active_color = (235, 190, 80) if is_exec_talking else (132, 204, 22)
    draw.text((WIDTH - 480, 40), f"CAMERA: {active_name}", font=font_cine, fill=active_color)

    # Subtítulos de Cine en Barra Inferior
    curr_text = GUILLERMO_DUO_DIALOGUE[0]["text"] if is_exec_talking else GUILLERMO_DUO_DIALOGUE[1]["text"]
    words = curr_text.split()
    words_per_frame = len(words) / (6.0 * FPS)
    curr_word_idx = int((t_sec % 6.0) * words_per_frame)

    start_w = max(0, curr_word_idx - 4)
    end_w = min(len(words), curr_word_idx + 6)
    line_text = " ".join(words[start_w:end_w])

    bbox = draw.textbbox((0, 0), line_text, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text((WIDTH//2 - tw//2, HEIGHT - 75), line_text, font=font_sub, fill=active_color)

    return img

def render_cinematic_guillermo_duo():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 85)
    print("  🎬 HB.OS CINEMATIC — PELÍCULA CINE CON DOS VARIANTES DE GUILLERMO (DIFERENTE LOOK)")
    print("  🎙️ AUDIO: 100% TU VOZ REAL DE GUILLERMO (runtime/guillermo_voice_studio_master_48k.aac)")
    print("=" * 85)

    vault = DeepSeekMediaVault("cinematic_guillermo_duo_2026", "Película Cine — Dos Avatares de Guillermo (Ejecutivo vs Tech)", "Película")
    vault.initialize_clean_workspace()

    master_audio = vault.audio_dir / "guillermo_voice_real_master.aac"
    cmd_copy = ["ffmpeg", "-y", "-i", str(REAL_AUDIO_PATH), "-c:a", "copy", str(master_audio)]
    subprocess.run(cmd_copy, capture_output=True, check=True)

    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_audio)]
    dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
    total_frames = int(dur * FPS)

    print(f"  ✓ Audio cargado: {dur:.2f} segundos ({total_frames} frames @ 24 fps cine)")

    # Avatar 1: Guillermo Ejecutivo (Traje Oscuro)
    # Avatar 2: Guillermo Tech (Look Pro/Casual)
    path_g1 = ROOT / "assets" / "avatar_transparent_hbos.png"
    path_g2 = ROOT / "assets" / "avatar_pro.png"

    img_g1 = Image.open(path_g1).convert("RGBA")
    img_g1.thumbnail((720, 720), Image.Resampling.LANCZOS)

    img_g2 = Image.open(path_g2).convert("RGBA")
    img_g2.thumbnail((720, 720), Image.Resampling.LANCZOS)

    print("\n[FASE 2/3] Renderizando película con dos variantes de Guillermo (Ejecutivo & Tech)...")

    for f in range(total_frames):
        t_sec = f / FPS
        frame = render_movie_guillermo_duo_scene(t_sec, f, img_g1, img_g2)
        frame_path = vault.frames_dir / f"frame_{f:06d}.jpg"
        frame.save(frame_path, quality=94)

    print(f"\n[FASE 3/3] Codificando película 1080p FastStart MP4 de alta definición...")

    video_filename = "Pelicula_Dos_Avatares_Guillermo_Cine_1080p.mp4"
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

    vault.save_manifest(video_filename, dur, total_frames, GUILLERMO_DUO_DIALOGUE)

    print("\n" + "=" * 85)
    print("  🏆 PELÍCULA CINEMÁTICA CON DOS AVATARES DE GUILLERMO GENERADA EXITOSAMENTE")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 85)

    vault.launch_video(video_filename)

if __name__ == "__main__":
    render_cinematic_guillermo_duo()
