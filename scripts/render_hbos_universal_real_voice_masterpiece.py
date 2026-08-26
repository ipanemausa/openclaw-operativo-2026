"""
==============================================================================
HB.OS (OPERATING SYSTEM) · SOVEREIGN AI — MASTERCLASS NATIVA CON VOZ REAL DE GUILLERMO
==============================================================================
- Audio: 100% VOZ REAL DE GUILLERMO (runtime/guillermo_voice_studio_master_48k.aac)
- Branding Oficial: HB.OS (OPERATING SYSTEM) · SOVEREIGN AI
- Tema: Sistema Operativo Universal HB.OS & Ecosistema DeepSeek Cloud Native
- Visual: Micro-clips de Video B-Roll + Avatar HD Transparente + Teleprompter Oro 52pt
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
FPS = 25

REAL_AUDIO_PATH = ROOT / "runtime" / "guillermo_voice_studio_master_48k.aac"

HBOS_UNIVERSAL_TRANSCRIPTION = (
    "Bienvenidos a la presentación oficial de HB.OS, el Sistema Operativo Universal "
    "de Inteligencia Artificial Soberana. Conectado directamente a la nube de DeepSeek "
    "y ejecutando orquestación multimodal en tiempo real."
)

def render_hbos_cosmic_frame(t_sec: float, frame_idx: int) -> Image.Image:
    """Renderiza el fotograma dinámico de HB.OS con efectos de micro-video B-Roll."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (4, 8, 22))
    draw = ImageDraw.Draw(img)
    
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(480, 0, -30):
        alpha = int(22 * (1 - r / 480))
        draw.ellipse([cx - r*1.5, cy - r, cx + r*1.5, cy + r], fill=(10 + alpha, 20 + alpha, 55 + alpha))
    
    # Grid holográfica de HB.OS
    grid_size = 80
    for x in range(0, WIDTH, grid_size):
        draw.line([(x, 0), (x, HEIGHT)], fill=(15, 30, 65, 40), width=1)
    for y in range(0, HEIGHT, grid_size):
        draw.line([(0, y), (WIDTH, y)], fill=(15, 30, 65, 40), width=1)

    # 180 Estrellas y Partículas de Datos
    for i in range(180):
        sx = (i * 137.5 + t_sec * (18 + (i % 5) * 10)) % WIDTH
        sy = (i * 293.1 + math.sin(t_sec * 0.6 + i) * 25) % HEIGHT
        size = 1 + (i % 3)
        brightness = int(190 + 65 * math.sin(t_sec * 2.5 + i))
        draw.ellipse([sx, sy, sx + size, sy + size], fill=(brightness, brightness, min(255, brightness + 50)))

    # Inserción de Micro-Video B-Roll Holográfico (Módulo Flow) en el tercio izquierdo
    bx1, by1, bx2, by2 = 120, 180, 720, 520
    draw.rectangle([bx1 - 4, by1 - 4, bx2 + 4, by2 + 4], fill=(212, 175, 106))
    
    # Renderizador dinámico de micro-clip B-Roll dentro del recuadro
    broll_bg = Image.new("RGB", (bx2 - bx1, by2 - by1), (12, 24, 48))
    broll_draw = ImageDraw.Draw(broll_bg)
    
    # Onda de frecuencia e Inferencia de Flow en vivo
    for x in range(0, bx2 - bx1, 10):
        y_val = (by2 - by1)//2 + int(35 * math.sin(t_sec * 8 + x * 0.05))
        broll_draw.ellipse([x, y_val, x + 6, y_val + 6], fill=(132, 204, 22))

    try:
        font_broll = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_broll = ImageFont.load_default()

    broll_draw.text((20, 20), "FLOW ENGINE: NANOBANANA (0 COSTO)", font=font_broll, fill=(255, 255, 255))
    broll_draw.text((20, 50), "VIDEO-IN / VIDEO-OUT INFERENCE", font=font_broll, fill=(212, 175, 106))
    
    img.paste(broll_bg, (bx1, by1))
    return img

def render_hbos_masterclass():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print("  🏆 HB.OS (OPERATING SYSTEM) · DEEPSEEK UNIVERSAL ENGINE")
    print("  🎙️ AUDIO: 100% TU VOZ REAL DE GUILLERMO (0 SÍNTESIS SINTÉTICA)")
    print("=" * 80)

    vault = DeepSeekMediaVault("hbos_universal_core_2026", "HB.OS Universal Operating System — Voz Real Guillermo", "Masterclass")
    vault.initialize_clean_workspace()

    if not REAL_AUDIO_PATH.exists():
        print(f"[ERROR] Archivo de tu voz real no encontrado en: {REAL_AUDIO_PATH}")
        sys.exit(1)

    # Copiar tu audio real al vault
    master_audio = vault.audio_dir / "guillermo_voice_real_master.aac"
    cmd_copy = ["ffmpeg", "-y", "-i", str(REAL_AUDIO_PATH), "-c:a", "copy", str(master_audio)]
    subprocess.run(cmd_copy, capture_output=True, check=True)

    # Obtener duración exacta de tu voz real
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_audio)]
    dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
    total_frames = int(dur * FPS)

    print(f"  ✓ Tu voz real cargada: {dur:.2f} segundos ({total_frames} frames @ {FPS}fps)")

    # Cargar avatar transparente de Guillermo
    avatar_path = ROOT / "assets" / "avatar_transparent_hbos.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"

    avatar_img = Image.open(avatar_path).convert("RGBA")
    avatar_img.thumbnail((780, 780), Image.Resampling.LANCZOS)

    try:
        font_header = ImageFont.truetype("arialbd.ttf", 28)
        font_sub = ImageFont.truetype("arialbd.ttf", 44)
    except:
        font_header = font_sub = ImageFont.load_default()

    words = HBOS_UNIVERSAL_TRANSCRIPTION.split()
    words_per_frame = len(words) / max(1, total_frames)

    print("\n[FASE 2/3] Renderizando video con tu voz real y micro-clips de Flow...")

    for f in range(total_frames):
        t_sec = f / FPS
        frame = render_hbos_cosmic_frame(t_sec, f)
        draw = ImageDraw.Draw(frame)

        # Header Oficial de Marca Inmutable HB.OS
        draw.text((60, 40), "HB.OS (OPERATING SYSTEM) · SOVEREIGN AI", font=font_header, fill=(212, 175, 106))
        draw.text((60, 75), "DEEPSEEK PLATFORM NATIVE ENGINE", font=font_header, fill=(255, 255, 255))

        # Avatar Guillermo Transparente en la Derecha
        ax = WIDTH - avatar_img.width - 60
        ay = HEIGHT - avatar_img.height
        frame.paste(avatar_img, (ax, ay), avatar_img)

        # Teleprompter Karaoke en Oro HB
        curr_word_idx = int(f * words_per_frame)
        start_w = max(0, curr_word_idx - 3)
        end_w = min(len(words), curr_word_idx + 5)
        line_text = " ".join(words[start_w:end_w])

        tx = 100
        ty = HEIGHT - 160

        draw.text((tx + 3, ty + 3), line_text, font=font_sub, fill=(0, 0, 0))
        draw.text((tx, ty), line_text, font=font_sub, fill=(235, 190, 80))

        frame_path = vault.frames_dir / f"frame_{f:06d}.jpg"
        frame.save(frame_path, quality=92)

    print(f"\n[FASE 3/3] Codificando video final 1080p FastStart MP4 con TU VOZ REAL...")

    video_filename = "HB_OS_Universal_Masterclass_Voz_Real_Guillermo_1080p.mp4"
    master_video_path = vault.output_dir / video_filename

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(vault.frames_dir / "frame_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        "-movflags", "+faststart",
        str(master_video_path)
    ]
    subprocess.run(cmd_ffmpeg, capture_output=True, check=True)

    modules_meta = [{"module_num": 1, "title": "HB.OS UNIVERSAL OPERATING SYSTEM", "text": HBOS_UNIVERSAL_TRANSCRIPTION}]
    vault.save_manifest(video_filename, dur, total_frames, modules_meta)

    print("\n" + "=" * 80)
    print("  🏆 HB.OS UNIVERSAL MASTERCLASS CON TU VOZ REAL GENERADA CON ÉXITO")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 80)

    vault.launch_video(video_filename)

if __name__ == "__main__":
    render_hbos_masterclass()
