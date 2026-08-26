"""
==============================================================================
DEEPSEEK HARNESS — DIÁLOGO DIÁDICO: DOS AVATARES DE GUILLERMO HABLANDO DE IA & FLOW
==============================================================================
- Avatar 1: Guillermo Ejecutivo Formal (Slot #01 - Traje Oscuro)
- Avatar 2: Guillermo Tech Founder (Slot #11 - Tech Hoodie HB.OS)
- Audio: 100% TU VOZ REAL DE GUILLERMO (runtime/guillermo_voice_studio_master_48k.aac)
- Tema: La Revolución de la Inteligencia Artificial y la Plataforma Flow
- Formato: 1080p Full HD (1920x1080 @ 25fps) FastStart MP4
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

DIALOGUE_TRANSCRIPT = [
    {"speaker": "Guillermo Ejecutivo", "text": "Hola Guillermo Tech. ¿Cómo ves la aceleración exponencial de la IA y el impacto de Flow?"},
    {"speaker": "Guillermo Tech", "text": "Increíble. Con la plataforma Flow y Nanobanana creamos avatares y videos a costo cero con tu voz real."}
]

def render_dialogue_frame(t_sec: float, frame_idx: int, avatar_1: Image.Image, avatar_2: Image.Image) -> Image.Image:
    """Renderiza el fotograma del diálogo cara a cara entre dos avatares de Guillermo."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (6, 12, 28))
    draw = ImageDraw.Draw(img)
    
    # Fondo ambiental dual
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(500, 0, -30):
        alpha = int(20 * (1 - r / 500))
        draw.ellipse([cx - r*1.4, cy - r, cx + r*1.4, cy + r], fill=(12 + alpha, 22 + alpha, 55 + alpha))

    # Grid futurista
    for x in range(0, WIDTH, 100):
        draw.line([(x, 0), (x, HEIGHT)], fill=(18, 35, 70), width=1)
    for y in range(0, HEIGHT, 100):
        draw.line([(0, y), (WIDTH, y)], fill=(18, 35, 70), width=1)

    # 180 Estrellas
    for i in range(180):
        sx = (i * 137.5 + t_sec * 15) % WIDTH
        sy = (i * 293.1 + math.sin(t_sec * 0.5 + i) * 20) % HEIGHT
        size = 1 + (i % 3)
        brightness = int(180 + 75 * math.sin(t_sec * 2 + i))
        draw.ellipse([sx, sy, sx + size, sy + size], fill=(brightness, brightness, min(255, brightness + 50)))

    # Determinar qué avatar está hablando (se alternan cada 8.5 segundos)
    is_speaker_1 = (t_sec % 17.0) < 8.5

    # Posicionar Avatar 1 (Ejecutivo) a la Izquierda
    scale_1 = 1.05 if is_speaker_1 else 0.95
    w1 = int(avatar_1.width * scale_1)
    h1 = int(avatar_1.height * scale_1)
    av1_resized = avatar_1.resize((w1, h1), Image.Resampling.LANCZOS)
    
    ax1 = 120
    ay1 = HEIGHT - h1
    img.paste(av1_resized, (ax1, ay1), av1_resized)

    # Posicionar Avatar 2 (Tech Founder) a la Derecha
    scale_2 = 0.95 if is_speaker_1 else 1.05
    w2 = int(avatar_2.width * scale_2)
    h2 = int(avatar_2.height * scale_2)
    av2_resized = avatar_2.resize((w2, h2), Image.Resampling.LANCZOS)

    ax2 = WIDTH - w2 - 120
    ay2 = HEIGHT - h2
    img.paste(av2_resized, (ax2, ay2), av2_resized)

    # Marco activo sobre el avatar que habla
    try:
        font_name = ImageFont.truetype("arialbd.ttf", 24)
        font_sub = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font_name = font_sub = ImageFont.load_default()

    if is_speaker_1:
        draw.rectangle([ax1 - 10, ay1 - 10, ax1 + w1 + 10, HEIGHT], outline=(235, 190, 80), width=3)
        draw.text((ax1, ay1 - 45), "🗣️ GUILLERMO EJECUTIVO (HABLANDO)", font=font_name, fill=(235, 190, 80))
    else:
        draw.rectangle([ax2 - 10, ay2 - 10, ax2 + w2 + 10, HEIGHT], outline=(132, 204, 22), width=3)
        draw.text((ax2, ay2 - 45), "🗣️ GUILLERMO TECH (RESPONDIENDO)", font=font_name, fill=(132, 204, 22))

    # Header de la Escena
    draw.text((60, 40), "HB.OS (OPERATING SYSTEM) · DIÁLOGO DE AVATARES SOBRE IA & FLOW", font=font_name, fill=(212, 175, 106))

    # Subtítulos del diálogo
    current_speech = DIALOGUE_TRANSCRIPT[0]["text"] if is_speaker_1 else DIALOGUE_TRANSCRIPT[1]["text"]
    words = current_speech.split()
    words_per_frame = len(words) / (8.5 * FPS)
    curr_word_idx = int((t_sec % 8.5) * words_per_frame)
    
    start_w = max(0, curr_word_idx - 3)
    end_w = min(len(words), curr_word_idx + 5)
    line_text = " ".join(words[start_w:end_w])

    tx = 100
    ty = HEIGHT - 140
    draw.text((tx + 3, ty + 3), line_text, font=font_sub, fill=(0, 0, 0))
    draw.text((tx, ty), line_text, font=font_sub, fill=(235, 190, 80) if is_speaker_1 else (132, 204, 22))

    return img

def render_dialogue_video():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print("  🏆 DEEPSEEK HARNESS — RENDERIZANDO DIÁLOGO ENTRE DOS AVATARES DE GUILLERMO")
    print("  🎙️ AUDIO: 100% TU VOZ REAL DE GUILLERMO (runtime/guillermo_voice_studio_master_48k.aac)")
    print("=" * 80)

    vault = DeepSeekMediaVault("dialogue_two_avatars_2026", "Diálogo entre Dos Avatares Guillermo sobre IA & Flow", "Diálogo")
    vault.initialize_clean_workspace()

    if not REAL_AUDIO_PATH.exists():
        print(f"[ERROR] Archivo de tu voz real no encontrado: {REAL_AUDIO_PATH}")
        sys.exit(1)

    master_audio = vault.audio_dir / "guillermo_voice_real_master.aac"
    cmd_copy = ["ffmpeg", "-y", "-i", str(REAL_AUDIO_PATH), "-c:a", "copy", str(master_audio)]
    subprocess.run(cmd_copy, capture_output=True, check=True)

    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_audio)]
    dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
    total_frames = int(dur * FPS)

    print(f"  ✓ Tu voz real masterizada cargada: {dur:.2f} segundos ({total_frames} frames)")

    # Cargar Avatares 1 y 2
    path_av1 = ROOT / "assets" / "avatar_transparent_hbos.png"
    path_av2 = ROOT / "assets" / "avatar_pro.png"

    av1_img = Image.open(path_av1).convert("RGBA")
    av1_img.thumbnail((650, 650), Image.Resampling.LANCZOS)

    av2_img = Image.open(path_av2).convert("RGBA")
    av2_img.thumbnail((650, 650), Image.Resampling.LANCZOS)

    print("\n[FASE 2/3] Renderizando interacción cara a cara entre dos avatares...")

    for f in range(total_frames):
        t_sec = f / FPS
        frame = render_dialogue_frame(t_sec, f, av1_img, av2_img)
        frame_path = vault.frames_dir / f"frame_{f:06d}.jpg"
        frame.save(frame_path, quality=92)

    print(f"\n[FASE 3/3] Codificando video 1080p FastStart MP4 con TU VOZ REAL...")

    video_filename = "Dialogue_Two_Guillermo_Avatars_Flow_1080p.mp4"
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

    vault.save_manifest(video_filename, dur, total_frames, DIALOGUE_TRANSCRIPT)

    print("\n" + "=" * 80)
    print("  🏆 DIÁLOGO ENTRE DOS AVATARES DE GUILLERMO GENERADO CON ÉXITO")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 80)

    vault.launch_video(video_filename)

if __name__ == "__main__":
    render_dialogue_video()
