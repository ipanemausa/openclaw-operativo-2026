"""
==============================================================================
HB. OS OPERATION SYSTEM — MASTERCLASS DEFINITIVA DEEPMIND (CLEAN NO-CC MASTER)
==============================================================================
1. Audio: 100% TU VOZ REAL HUMANA (Guillermo_Podcast_Master_Edit_48k.wav, 6.36 min)
2. Avatar: Avatar Transparente HD Oficial de Guillermo (assets/avatar_transparent_hbos.png)
3. Capturas B-Roll: 40 Capturas de DeepMind 100% LIMPIAS (deepmind_clean_no_cc)
4. Teleprompter: Teleprompter de Masterclass centrado en la zona de orador
5. Branding: HB. OS OPERATION SYSTEM · SOVEREIGN AI
==============================================================================
"""

import os
import sys
import math
import glob
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_guillermo_deepmind_clean_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_DIR = ROOT / "capturas_recientes" / "deepmind_clean_no_cc"
AVATAR_PATH = ROOT / "assets" / "avatar_transparent_hbos.png"
AUDIO_MASTER = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
FINAL_VIDEO = PROD_DIR / "PROD_HBOS_GUILLERMO_DEEPMIND_CLEAN_NO_CC_1080P.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def load_clean_deepmind_captures():
    files = sorted(glob.glob(str(CLEAN_DIR / "*.png")))
    images = []
    card_w, card_h = 1060, 596
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
            im_scaled = im.resize((card_w, card_h), Image.Resampling.LANCZOS)
            images.append(im_scaled)
        except Exception as e:
            print(f"Error cargando {f}: {e}")
    return images

def init_stars(count=180):
    import random
    random.seed(2026)
    stars = []
    for _ in range(count):
        stars.append({
            "x": random.uniform(0, WIDTH),
            "y": random.uniform(0, HEIGHT),
            "z": random.uniform(0.5, 3.5),
            "r": random.uniform(1.0, 2.2),
            "alpha": random.uniform(0.3, 0.9)
        })
    return stars

STARS = init_stars(180)

def draw_cosmic_bg(draw: ImageDraw.Draw, t: float):
    for y in range(0, HEIGHT, 8):
        prog = y / HEIGHT
        r = int(4 + 8 * prog)
        g = int(8 + 14 * prog)
        b = int(18 + 32 * prog)
        draw.rectangle([(0, y), (WIDTH, y + 8)], fill=(r, g, b))

    for s in STARS:
        sx = (s["x"] - t * 12 * s["z"]) % WIDTH
        sy = s["y"]
        twinkle = 0.5 + 0.5 * math.sin(t * 2.0 + s["z"] * 3.0)
        c_val = int(255 * s["alpha"] * twinkle)
        draw.ellipse([(sx, sy), (sx + s["r"], sy + s["r"])], fill=(c_val, c_val, int(c_val * 1.1)))

def load_fonts():
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
        font_label = ImageFont.truetype("arialbd.ttf", 22)
        font_tele_title = ImageFont.truetype("arialbd.ttf", 24)
        font_teleprompter = ImageFont.truetype("arialbd.ttf", 32)
    except Exception:
        font_header = font_badge = font_label = font_tele_title = font_teleprompter = ImageFont.load_default()
    return font_header, font_badge, font_label, font_tele_title, font_teleprompter

def main():
    print("=" * 80)
    print("  HB.OS — MASTERCLASS DEEPMIND DEFINITIVA (CAPTURAS 100% LIMPIAS SIN CC)")
    print("=" * 80)

    total_duration = get_audio_duration(AUDIO_MASTER)
    total_frames = int(total_duration * FPS)
    print(f"  ✓ Tu Pista de Voz Real: {AUDIO_MASTER.name} ({total_duration:.2f}s / {total_duration/60:.2f} min)")
    print(f"  ✓ Total de fotogramas a compilar: {total_frames}")

    deepmind_caps = load_clean_deepmind_captures()
    print(f"  ✓ Capturas limpias de DeepMind cargadas: {len(deepmind_caps)}")

    if not AVATAR_PATH.exists():
        print(f"❌ Error: Avatar no encontrado en {AVATAR_PATH}")
        return
    av_raw = Image.open(AVATAR_PATH).convert("RGBA")
    target_av_h = 800
    target_av_w = int(av_raw.width * (target_av_h / av_raw.height))
    avatar_img = av_raw.resize((target_av_w, target_av_h), Image.Resampling.LANCZOS)
    print(f"  ✓ Avatar de Guillermo HD cargado ({target_av_w}x{target_av_h})")

    font_header, font_badge, font_label, font_tele_title, font_teleprompter = load_fonts()

    card_x, card_y = 60, 110
    card_w, card_h = 1060, 596

    print("\n[RENDER] Compilando fotogramas con B-Roll 100% limpio y Avatar...")
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
        draw = ImageDraw.Draw(frame)

        # 1. Fondo cósmico
        draw_cosmic_bg(draw, t)

        # 2. B-Roll de DeepMind 100% LIMPIO (cero subtítulos viejos)
        if len(deepmind_caps) > 0:
            cap_idx = int((t / total_duration) * len(deepmind_caps)) % len(deepmind_caps)
            cap_img = deepmind_caps[cap_idx]
            
            draw.rectangle([(card_x - 2, card_y - 2), (card_x + card_w + 2, card_y + card_h + 2)], outline=(0, 200, 255, 180), width=2)
            frame.paste(cap_img, (card_x, card_y))

            draw.rectangle([(card_x + 15, card_y + 15), (card_x + 310, card_y + 50)], fill=(0, 20, 45, 220), outline=(0, 180, 255, 200), width=1)
            draw.text((card_x + 25, card_y + 20), f"DEEPMIND ARCHIVE #{cap_idx+1:02d}/{len(deepmind_caps)}", fill=(0, 240, 255), font=font_label)

        # 3. Avatar Transparente de Guillermo
        av_pos_x = WIDTH - target_av_w - 40
        av_pos_y = HEIGHT - target_av_h - 10
        frame.paste(avatar_img, (av_pos_x, av_pos_y), avatar_img)

        # 4. Header Superior HB.OS
        draw.rectangle([(0, 0), (WIDTH, 75)], fill=(5, 12, 28, 230))
        draw.line([(0, 75), (WIDTH, 75)], fill=(0, 180, 255, 120), width=1)
        draw.text((60, 22), "HB. OS OPERATION SYSTEM", fill=(255, 255, 255), font=font_header)
        draw.text((450, 22), "|  GOOGLE DEEPMIND & DEMIS HASSABIS · MASTERCLASS", fill=(0, 220, 255), font=font_header)

        draw.rectangle([(WIDTH - 280, 18), (WIDTH - 60, 58)], fill=(0, 40, 85, 220), outline=(0, 180, 255, 200), width=1)
        draw.text((WIDTH - 265, 26), "HB.OS · SOVEREIGN AI", fill=(255, 255, 255), font=font_badge)

        # 5. TELEPROMPTER PROFESIONAL DE MASTERCLASS
        tele_y = HEIGHT - 310
        tele_h = 220
        draw.rectangle([(card_x, tele_y), (card_x + card_w, tele_y + tele_h)], fill=(6, 15, 35, 230), outline=(0, 180, 255, 180), width=1)
        
        draw.text((card_x + 30, tele_y + 20), "🎙️ TELEPROMPTER DE NARRACIÓN · GUILLERMO HOYOS", fill=(255, 205, 50), font=font_tele_title)
        draw.text((card_x + 30, tele_y + 70), "Soberanía Computacional, Modelos de Mundo y Ciencia Autónoma", fill=(255, 255, 255), font=font_teleprompter)
        draw.text((card_x + 30, tele_y + 120), "Espacio Vectorial R^768 · Orquestación DAG · Cómputo Elástico Cloud", fill=(0, 225, 255), font=font_teleprompter)

        # Barra de progreso
        prog_w = int((card_w - 60) * (t / total_duration))
        draw.line([(card_x + 30, tele_y + 180), (card_x + card_w - 30, tele_y + 180)], fill=(30, 50, 80), width=4)
        draw.line([(card_x + 30, tele_y + 180), (card_x + 30 + prog_w, tele_y + 180)], fill=(0, 220, 255), width=4)

        out_frame_path = FRAMES_DIR / f"frame_{frame_idx:06d}.jpg"
        frame.convert("RGB").save(out_frame_path, quality=94)

        if frame_idx % 600 == 0 or frame_idx == total_frames - 1:
            print(f"  -> Progreso Render HD: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

    # Codificación FFmpeg FastStart
    print("\n[CODIFICANDO] Ensamblando video Full HD con TU VOZ REAL y AVATAR...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%06d.jpg"),
        "-i", str(AUDIO_MASTER),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-shortest",
        "-movflags", "+faststart",
        str(FINAL_VIDEO)
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"\n🏆 VIDEO PERFECTO GENERADO EXITOSAMENTE:")
    print(f"📁 {FINAL_VIDEO}")

if __name__ == "__main__":
    main()
