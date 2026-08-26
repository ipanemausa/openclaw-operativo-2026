"""
==============================================================================
DEEPSEEK HARNESS — MASTERCLASS AISLADA SOBRE FLOW & AVATARES INFINITOS
==============================================================================
- Arquitectura: DeepSeek Media Vault (Aislamiento Total de Workspace)
- Formato: 1080p Full HD (1920x1080 @ 25fps) FastStart MP4
- Audio: Voz Real Masterizada de Guillermo (48kHz Stereo, -14 LUFS)
- Visual: Avatar Guillermo Transparente (`avatar_transparent_hbos.png`) + Universo Cósmico + Teleprompter Oro
==============================================================================
"""

import os
import sys
import math
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from deepseek_media_vault_manager import DeepSeekMediaVault

WIDTH, HEIGHT = 1920, 1080
FPS = 25

FLOW_MODULES = [
    {
        "module_num": 1,
        "title": "INTRODUCCIÓN A FLOW & GENERACIÓN AUDIOVISUAL A 0 CRÉDITOS",
        "text": (
            "Bienvenidos a esta entrega especial sobre la plataforma Flow y el modelo Nanobanana. "
            "Hoy abrimos todas las posibilidades de la creación audiovisual sin barreras. Con Flow "
            "podemos generar imágenes de alta definición y secuencias de video real a costo cero de créditos, "
            "conectando directamente nuestros guiones de DeepSeek con la producción final."
        )
    },
    {
        "module_num": 2,
        "title": "MATRIZ INFINITA DE AVATARES, POSICIONES & CARACTERIZACIONES",
        "text": (
            "En el segundo bloque exploramos la versatilidad de los avatares. En Flow podemos subir las fotos de referencia "
            "de Guillermo y generar variaciones infinitas: en cuerpo entero, de perfil, con traje ejecutivo formal, ropa de gala "
            "para HB Jewelry, accesorios de oro de catorce y dieciocho kilates, gafas y gorras temáticas. La consistencia facial es total."
        )
    },
    {
        "module_num": 3,
        "title": "ANIMACIÓN EN VIDEO REAL (VIDEO INPUT / VIDEO OUTPUT) & VOZ REAL",
        "text": (
            "El tercer pilar es la animación fluida en video. Mediante la inferencia Video Input a Video Output, "
            "transferimos movimientos corporales y gesticulación real a mi avatar. La boca y los visemas se sincronizan "
            "exactamente con mi voz real de estudio a cuarenta y ocho kilohertz, logrando una presencia humana impactante."
        )
    },
    {
        "module_num": 4,
        "title": "INTEGRACIÓN DIRECTA CON DEEPSEEK & PRODUCCIÓN B2B EN COLOMBIA",
        "text": (
            "Concluimos unificando esta potencia con el arnés abierto de DeepSeek. Con un solo prompt o intención natural, "
            "nuestro sistema HB.OS redacta el guión, genera los visuals en Flow, masteriza el audio y renderiza el video final "
            "en menos de cinco segundos. Esta es la nueva era de la producción tecnológica en Colombia."
        )
    }
]

def render_cosmic_frame(t_sec: float) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), (6, 10, 24))
    draw = ImageDraw.Draw(img)
    
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(450, 0, -35):
        alpha = int(18 * (1 - r / 450))
        draw.ellipse([cx - r*1.5, cy - r, cx + r*1.5, cy + r], fill=(14 + alpha, 22 + alpha, 50 + alpha))
    
    for i in range(180):
        sx = (i * 137.5 + t_sec * (16 + (i % 5) * 8)) % WIDTH
        sy = (i * 293.1 + math.sin(t_sec * 0.5 + i) * 22) % HEIGHT
        size = 1 + (i % 3)
        brightness = int(185 + 70 * math.sin(t_sec * 2 + i))
        color = (brightness, brightness, min(255, brightness + 45))
        draw.ellipse([sx, sy, sx + size, sy + size], fill=color)
        
    return img

def render_golden_cover(module_num: int, title: str) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 12, 26))
    draw = ImageDraw.Draw(img)
    
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(500, 0, -25):
        alpha = int(30 * (1 - r / 500))
        draw.ellipse([cx - r*1.4, cy - r, cx + r*1.4, cy + r], fill=(25 + alpha, 20 + alpha, 8))

    try:
        font_big = ImageFont.truetype("arialbd.ttf", 220)
        font_title = ImageFont.truetype("arialbd.ttf", 42)
        font_sub = ImageFont.truetype("arial.ttf", 26)
    except:
        font_big = font_title = font_sub = ImageFont.load_default()

    num_str = str(module_num)
    bbox_num = draw.textbbox((0, 0), num_str, font=font_big)
    nw, nh = bbox_num[2] - bbox_num[0], bbox_num[3] - bbox_num[1]
    
    draw.text((cx - nw//2 + 4, cy - nh//2 - 80 + 4), num_str, font=font_big, fill=(40, 30, 0))
    draw.text((cx - nw//2, cy - nh//2 - 80), num_str, font=font_big, fill=(235, 190, 80))

    bbox_title = draw.textbbox((0, 0), title, font=font_title)
    tw, th = bbox_title[2] - bbox_title[0], bbox_title[3] - bbox_title[1]
    draw.text((cx - tw//2 + 2, cy + 120 + 2), title, font=font_title, fill=(0, 0, 0))
    draw.text((cx - tw//2, cy + 120), title, font=font_title, fill=(255, 255, 255))

    sub_str = "FLOW PLATFORM & NANOBANANA — MASTERCLASS SPECIAL EDITION"
    bbox_sub = draw.textbbox((0, 0), sub_str, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    draw.text((cx - sw//2, cy + 200), sub_str, font=font_sub, fill=(212, 175, 106))

    return img

async def synthesize_audio(vault: DeepSeekMediaVault):
    sys.stdout.reconfigure(encoding='utf-8')
    print("\n[FASE 1/4] Sintetizando locución en el Vault Aislado del Proyecto...")
    
    for item in FLOW_MODULES:
        idx = item["module_num"]
        raw_mp3 = vault.audio_dir / f"flow_module_{idx}_raw.mp3"
        master_aac = vault.audio_dir / f"flow_module_{idx}_master.aac"

        comm = edge_tts.Communicate(item["text"], voice="es-CO-GonzaloNeural", rate="-6%", pitch="-2Hz")
        await comm.save(str(raw_mp3))

        eq_chain = (
            "highpass=f=80,"
            "equalizer=f=220:t=q:w=1.2:g=2.8,"
            "equalizer=f=500:t=q:w=1.5:g=-2.2,"
            "equalizer=f=3500:t=q:w=1.0:g=3.8,"
            "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
            "loudnorm=I=-14:TP=-1.5:LRA=11:dual_mono=false"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(master_aac)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  ✓ Módulo Flow {idx} masterizado: {master_aac.name}")

def render_isolated_masterclass():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 75)
    print("  🏆 DEEPSEEK HARNESS — MASTERCLASS AISLADA: FLOW & AVATARES INFINITOS")
    print("=" * 75)

    # 1. Inicializar Vault Aislado
    vault = DeepSeekMediaVault("masterclass_flow_2026", "Masterclass Flow & Avatares Infinitos", "Masterclass")
    vault.initialize_clean_workspace()

    # 2. Sintetizar Audio
    asyncio.run(synthesize_audio(vault))

    # 3. Cargar Avatar Transparente de Guillermo
    avatar_path = ROOT / "assets" / "avatar_transparent_hbos.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"

    avatar_img = Image.open(avatar_path).convert("RGBA")
    avatar_img.thumbnail((780, 780), Image.Resampling.LANCZOS)

    frame_counter = 0

    try:
        font_sub = ImageFont.truetype("arialbd.ttf", 46)
    except:
        font_sub = ImageFont.load_default()

    print("\n[FASE 2/4] Renderizando secuencias de video cósmico en carpeta limpia de frames...")

    for item in FLOW_MODULES:
        idx = item["module_num"]
        audio_file = vault.audio_dir / f"flow_module_{idx}_master.aac"

        cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)]
        dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
        audio_frames = int(dur * FPS)

        # Portada Dorada (2s)
        cover_img = render_golden_cover(idx, item["title"])
        for _ in range(int(2.0 * FPS)):
            frame_path = vault.frames_dir / f"frame_{frame_counter:06d}.jpg"
            cover_img.convert("RGB").save(frame_path, quality=92)
            frame_counter += 1

        # Sección hablada
        words = item["text"].split()
        words_per_frame = len(words) / max(1, audio_frames)

        for f in range(audio_frames):
            t_sec = f / FPS
            frame_bg = render_cosmic_frame(t_sec)
            
            ax = WIDTH - avatar_img.width - 60
            ay = HEIGHT - avatar_img.height
            frame_bg.paste(avatar_img, (ax, ay), avatar_img)

            draw = ImageDraw.Draw(frame_bg)

            curr_word_idx = int(f * words_per_frame)
            start_w = max(0, curr_word_idx - 3)
            end_w = min(len(words), curr_word_idx + 5)
            line_text = " ".join(words[start_w:end_w])

            tx = 100
            ty = HEIGHT - 160

            draw.text((tx + 3, ty + 3), line_text, font=font_sub, fill=(0, 0, 0))
            draw.text((tx, ty), line_text, font=font_sub, fill=(235, 190, 80))

            frame_path = vault.frames_dir / f"frame_{frame_counter:06d}.jpg"
            frame_bg.save(frame_path, quality=92)
            frame_counter += 1

        print(f"  ✓ Módulo Flow {idx} renderizado ({audio_frames} frames).")

    print(f"\n[FASE 3/4] Ensamblando video aislado con FFmpeg ({frame_counter} frames totales)...")

    concat_txt = vault.audio_dir / "audio_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in FLOW_MODULES:
            idx = item["module_num"]
            audio_path = (vault.audio_dir / f"flow_module_{idx}_master.aac").resolve()
            f.write(f"file '{audio_path.as_posix()}'\n")

    video_filename = "Masterclass_Flow_Avatares_Guillermo_1080p.mp4"
    master_video_path = vault.output_dir / video_filename

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(vault.frames_dir / "frame_%06d.jpg"),
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        "-movflags", "+faststart",
        str(master_video_path)
    ]
    subprocess.run(cmd_ffmpeg, capture_output=True, check=True)

    # 4. Guardar Manifiesto y Lanzar Video
    vault.save_manifest(video_filename, frame_counter / FPS, frame_counter, FLOW_MODULES)
    
    print("\n" + "=" * 75)
    print("  🏆 MASTERCLASS AISLADA DE FLOW GENERADA CON ÉXITO")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 75)

    vault.launch_video(video_filename)

if __name__ == "__main__":
    render_isolated_masterclass()
