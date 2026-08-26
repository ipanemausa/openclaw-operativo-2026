"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS MAESTRA SOBRE FLOW & AVATARES INFINITOS
==============================================================================
- Tema: Plataforma Flow, Modelo Nanobanana 0 Créditos, Avatares & Voz Real de Guillermo
- Formato: 1080p Full HD (1920x1080 @ 25fps) FastStart MP4
- Audio: Voz Real Masterizada de Guillermo (48kHz Stereo, -14 LUFS EBU R128)
- Visual: Avatar Guillermo PNG Transparente Perfeccionado + Universo Cósmico + Teleprompter Oro
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
RUNTIME = ROOT / "runtime" / "masterclass_flow_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── MÓDULOS DE LA MASTERCLASS DE FLOW ─────────────────────────────────────

FLOW_MASTERCLASS_MODULES = [
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

def render_cosmic_universe_frame(t_sec: float) -> Image.Image:
    """Genera un fotograma del universo cósmico con 180 estrellas en paralaje."""
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

def render_golden_flow_cover(module_num: int, title: str) -> Image.Image:
    """Renderiza la portada del módulo con número dorado gigante."""
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

async def synthesize_flow_audio_tracks():
    sys.stdout.reconfigure(encoding='utf-8')
    print("\n[FASE 1/4] Sintetizando locución calibrada de la Masterclass sobre Flow...")
    
    for item in FLOW_MASTERCLASS_MODULES:
        idx = item["module_num"]
        raw_mp3 = RUNTIME / f"flow_module_{idx}_raw.mp3"
        master_aac = RUNTIME / f"flow_module_{idx}_master.aac"

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

def render_flow_masterclass():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 70)
    print("  🏆 OPENCLAW 2026 — MASTERCLASS FLOW & AVATARES INFINITOS DE GUILLERMO")
    print("=" * 70)

    # 1. Sintetizar audio
    asyncio.run(synthesize_flow_audio_tracks())

    # 2. Cargar avatar transparente de Guillermo
    avatar_path = ROOT / "assets" / "avatar_transparent_hbos.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"

    avatar_img = Image.open(avatar_path).convert("RGBA")
    avatar_img.thumbnail((780, 780), Image.Resampling.LANCZOS)
    
    frames_dir = RUNTIME / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    frame_counter = 0

    try:
        font_sub = ImageFont.truetype("arialbd.ttf", 46)
    except:
        font_sub = ImageFont.load_default()

    print("\n[FASE 2/4] Renderizando secuencias de video cósmico y portadas de Flow...")

    for item in FLOW_MASTERCLASS_MODULES:
        idx = item["module_num"]
        audio_file = RUNTIME / f"flow_module_{idx}_master.aac"

        cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)]
        dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
        audio_frames = int(dur * FPS)

        # Portada Dorada (2 segundos)
        cover_img = render_golden_flow_cover(idx, item["title"])
        for _ in range(int(2.0 * FPS)):
            frame_path = frames_dir / f"frame_{frame_counter:06d}.jpg"
            cover_img.convert("RGB").save(frame_path, quality=92)
            frame_counter += 1

        # Sección hablada con Avatar Guillermo + Teleprompter Oro + Universo
        words = item["text"].split()
        words_per_frame = len(words) / max(1, audio_frames)

        for f in range(audio_frames):
            t_sec = f / FPS
            frame_bg = render_cosmic_universe_frame(t_sec)
            
            ax = WIDTH - avatar_img.width - 60
            ay = HEIGHT - avatar_img.height
            frame_bg.paste(avatar_img, (ax, ay), avatar_img)

            draw = ImageDraw.Draw(frame_bg)

            curr_word_idx = int(f * words_per_frame)
            start_w = max(0, curr_word_idx - 3)
            end_w = min(len(words), curr_word_idx + 5)
            line_text = " ".join(words[start_w:end_w])

            bbox = draw.textbbox((0, 0), line_text, font=font_sub)
            tx = 100
            ty = HEIGHT - 160

            draw.text((tx + 3, ty + 3), line_text, font=font_sub, fill=(0, 0, 0))
            draw.text((tx, ty), line_text, font=font_sub, fill=(235, 190, 80))

            frame_path = frames_dir / f"frame_{frame_counter:06d}.jpg"
            frame_bg.save(frame_path, quality=92)
            frame_counter += 1

        print(f"  ✓ Módulo Flow {idx} renderizado ({audio_frames} frames).")

    print(f"\n[FASE 3/4] Ensamblando video maestro de Flow con FFmpeg ({frame_counter} frames)...")

    concat_txt = RUNTIME / "audio_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in FLOW_MASTERCLASS_MODULES:
            idx = item["module_num"]
            audio_path = (RUNTIME / f"flow_module_{idx}_master.aac").resolve()
            f.write(f"file '{audio_path.as_posix()}'\n")

    master_video_path = RUNTIME / "Masterclass_Flow_Avatares_Guillermo_1080p.mp4"

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%06d.jpg"),
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        "-movflags", "+faststart",
        str(master_video_path)
    ]
    subprocess.run(cmd_ffmpeg, capture_output=True, check=True)

    print("\n" + "=" * 70)
    print("  🏆 MASTERCLASS FLOW & AVATARES GENERADA EXITOSAMENTE")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 70)

if __name__ == "__main__":
    render_flow_masterclass()
