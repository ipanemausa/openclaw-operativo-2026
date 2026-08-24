"""
==============================================================================
HB. OS OPERATION SYSTEM — VIDEO MAESTRO CON VOZ REAL DE GUILLERMO (6.36 MIN)
Narración: Guillermo Hoyos (100% VOZ HUMANA REAL GRABADA - ZERO SÍNTESIS SINTÉTICA)
Fuente de Audio: Guillermo_Podcast_Master_Edit_48k.wav (381.56s / 6.36 min)
Branding: HB. OS Operation system · Sovereign AI
Capturas B-Roll: 40 Capturas de DeepMind & Demis Hassabis en HD Cristalino
Estándar: [OPENCLAW-CORE-MATRIX-2026] · EBU R128 (-16 LUFS) · 48kHz Stereo
==============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REAL_VOICE_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_guillermo_real_voice_deepmind_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_real_voice_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
CAPTURES_DIR = ROOT / "capturas_recientes"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def init_stars(count=200):
    import random
    random.seed(42)
    stars = []
    for _ in range(count):
        stars.append({
            "x": random.uniform(0, WIDTH),
            "y": random.uniform(0, HEIGHT),
            "z": random.uniform(0.5, 3.8),
            "base_r": random.uniform(1.0, 2.5),
            "brightness": random.uniform(0.4, 1.0)
        })
    return stars

STARS = init_stars(200)

def draw_cosmic_background(draw: ImageDraw.Draw, t: float):
    for y in range(0, HEIGHT, 10):
        ratio = y / HEIGHT
        r = int(4 + ratio * 8)
        g = int(7 + ratio * 12)
        b = int(20 + ratio * 36)
        draw.rectangle([0, y, WIDTH, y + 10], fill=(r, g, b))

    for s in STARS:
        shift_x = (s["x"] - t * s["z"] * 15) % WIDTH
        shift_y = (s["y"] + math.sin(t * 0.35 + s["x"]) * 5) % HEIGHT
        rad = s["base_r"] * (0.8 + 0.25 * math.sin(t * 2.2 + s["y"]))
        alpha = int(220 * s["brightness"] * (0.7 + 0.3 * math.sin(t * 3.2 + s["x"])))
        draw.ellipse([shift_x - rad, shift_y - rad, shift_x + rad, shift_y + rad], fill=(215, 235, 255, alpha))

CHAPTERS = [
    {"start": 0.0, "end": 64.0, "cap": 1, "title": "EL DOMINIO DE LOS JUEGOS Y LA BÚSQUEDA EXPONENCIAL", "sub": "AlphaGo Move 37 & AlphaStar en Tiempo Real"},
    {"start": 64.0, "end": 128.0, "cap": 2, "title": "EL GRAN MOMENTO DECISIVO: ALPHAFOLD", "sub": "Resolviendo el Plegamiento de Proteínas en 3D"},
    {"start": 128.0, "end": 192.0, "cap": 3, "title": "ARQUITECTURA MOLECULAR & EL PORO NUCLEAR", "sub": "Mapeando la Maquinaria Fundamental de la Vida"},
    {"start": 192.0, "end": 256.0, "cap": 4, "title": "GENÓMICA Y DISEÑO DE FÁRMACOS IN SILICO", "sub": "AlphaGenome y Exploración del ADN No Codificante"},
    {"start": 256.0, "end": 320.0, "cap": 5, "title": "MODELOS DE MUNDO Y ROBÓTICA FÍSICA", "sub": "Cerrando la Brecha Digital y Acción Material"},
    {"start": 320.0, "end": 382.0, "cap": 6, "title": "SOBERANÍA COMPUTACIONAL Y CIENCIA AUTÓNOMA", "sub": "HB. OS Operation system · Espacio Vectorial R^768"}
]

def render_master_video():
    print("=" * 75)
    print("  HB. OS OPERATION SYSTEM — MASTERCLASS CON VOZ REAL DE GUILLERMO")
    print(f"  Pista de Audio Real: {REAL_VOICE_AUDIO.name}")
    print("=" * 75)

    if not REAL_VOICE_AUDIO.exists():
        print(f"ERROR: No se encontró {REAL_VOICE_AUDIO}")
        sys.exit(1)

    total_dur = get_audio_duration(REAL_VOICE_AUDIO)
    total_frames = int(total_dur * FPS)
    print(f"  ✓ Duración de tu voz grabada: {total_dur:.2f}s ({total_dur/60:.2f} minutos)")
    print(f"  ✓ Fotogramas HD a compilar: {total_frames}")

    # 1. Cargar Avatar en HD
    avatar_path = ROOT / "frontend" / "public" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"

    raw_av = Image.open(avatar_path).convert("RGBA")
    raw_av = ImageEnhance.Sharpness(raw_av).enhance(1.25)
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    av_x = WIDTH - av_w - 30

    # 2. Cargar las 40 capturas de DeepMind en HD
    all_captures = sorted(list(CAPTURES_DIR.glob("Screenshot 2026-08-24*.png")))
    if not all_captures:
        all_captures = sorted(list(CAPTURES_DIR.glob("*.png")))
    print(f"  ✓ Capturas HD disponibles: {len(all_captures)}")

    broll_w, broll_h = 1040, 585
    broll_cache = {}
    for i, cap_p in enumerate(all_captures, 1):
        try:
            im = Image.open(cap_p).convert("RGBA")
            im = ImageEnhance.Sharpness(im).enhance(1.2)
            im = im.resize((broll_w, broll_h), Image.Resampling.LANCZOS)
            broll_cache[i] = im
        except Exception as e:
            pass

    num_caps = len(all_captures)

    try:
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 24)
        font_tele = ImageFont.truetype("arialbd.ttf", 40)
    except Exception:
        font_header = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tele = ImageFont.load_default()

    for f_idx in range(total_frames):
        t = f_idx / FPS
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (4, 7, 20, 255))
        draw = ImageDraw.Draw(frame)

        draw_cosmic_background(draw, t)

        # Capítulo activo
        active_cap = CHAPTERS[-1]
        for c in CHAPTERS:
            if c["start"] <= t <= c["end"]:
                active_cap = c
                break

        # ─── HEADER SUPERIOR HD ───
        draw.rectangle([50, 35, 1870, 95], fill=(12, 18, 35, 220), outline=(56, 189, 248, 140), width=2)
        draw.text((70, 52), f"HB. OS OPERATION SYSTEM  |  CAP. {active_cap['cap']}: {active_cap['title'][:50]}", fill=(240, 246, 252), font=font_header)

        # Badge "VOZ REAL DE GUILLERMO"
        draw.rectangle([1500, 45, 1855, 85], fill=(37, 99, 235, 230))
        draw.text((1515, 54), "VOZ REAL · GUILLERMO HOYOS", fill=(255, 255, 255), font=font_badge)

        # ─── B-ROLL HD CAPTURA DEEPMIND ───
        curr_cap_idx = int((t / total_dur) * num_caps) + 1
        curr_cap_idx = min(num_caps, max(1, curr_cap_idx))

        broll_x, broll_y = 50, 120
        if curr_cap_idx in broll_cache:
            broll_img = broll_cache[curr_cap_idx]
            frame.paste(broll_img, (broll_x, broll_y), broll_img)
            draw.rectangle([broll_x, broll_y, broll_x + broll_w, broll_y + broll_h], outline=(59, 130, 246, 230), width=3)
            
            draw.rectangle([broll_x + 12, broll_y + 12, broll_x + 340, broll_y + 48], fill=(8, 12, 24, 230))
            draw.text((broll_x + 22, broll_y + 18), f"DEEPMIND ARCHIVE #{curr_cap_idx:02d}/{num_caps}", fill=(56, 189, 248), font=font_header)

        # ─── AVATAR DE GUILLERMO EN HD ───
        av_y = HEIGHT - av_h + 10
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # ─── TELEPROMPTER EN ZONA SEGURA (y = 745 a 985) ───
        sub_box_y = 745
        draw.rectangle([50, sub_box_y, broll_x + broll_w, sub_box_y + 240], fill=(8, 12, 26, 230), outline=(245, 158, 11, 180), width=2)

        # Texto indicativo de voz humana real en directo
        draw.text((82, sub_box_y + 32), "LOCUCIÓN ORIGINAL: GUILLERMO HOYOS (VOZ REAL)", fill=(0, 0, 0), font=font_tele)
        draw.text((80, sub_box_y + 30), "LOCUCIÓN ORIGINAL: GUILLERMO HOYOS (VOZ REAL)", fill=(251, 191, 36), font=font_tele)

        draw.text((82, sub_box_y + 102), f"Capítulo {active_cap['cap']}: {active_cap['title'][:44]}", fill=(0, 0, 0), font=font_tele)
        draw.text((80, sub_box_y + 100), f"Capítulo {active_cap['cap']}: {active_cap['title'][:44]}", fill=(255, 255, 255), font=font_tele)

        draw.text((82, sub_box_y + 162), f">> {active_cap['sub']}", fill=(0, 0, 0), font=font_sub)
        draw.text((80, sub_box_y + 160), f">> {active_cap['sub']}", fill=(100, 225, 185), font=font_sub)

        # Barra de progreso
        bar_y = HEIGHT - 22
        prog_pct = t / total_dur
        draw.rectangle([50, bar_y, WIDTH - 50, bar_y + 8], fill=(15, 23, 42, 220))
        draw.rectangle([50, bar_y, 50 + int((WIDTH - 100) * prog_pct), bar_y + 8], fill=(56, 189, 248, 240))

        frame_file = FRAMES_DIR / f"frame_{f_idx:06d}.jpg"
        frame.convert("RGB").save(str(frame_file), quality=98)

        if f_idx % 500 == 0:
            pct = f_idx / total_frames * 100
            print(f"  -> Progreso Render HD: {f_idx}/{total_frames} frames ({pct:.1f}%)")

    print(f"  ✓ {total_frames} fotogramas Full HD completados.")

    # Codificación con tu voz real
    output_mp4 = PROD_DIR / "PROD_HBOS_GUILLERMO_REAL_VOICE_DEEPMIND_1080P_MASTER.mp4"
    cmd_encode = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%06d.jpg"),
        "-i", str(REAL_VOICE_AUDIO),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-ac", "2",
        "-movflags", "+faststart",
        str(output_mp4)
    ]
    print("\n[CODIFICANDO] Compilando video final con TU VOZ REAL (FastStart 1080p)...")
    subprocess.run(cmd_encode, check=True)
    print(f"\n  🏆 VIDEO MAESTRO CON TU VOZ REAL GENERADO:")
    print(f"  📁 {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    render_master_video()
