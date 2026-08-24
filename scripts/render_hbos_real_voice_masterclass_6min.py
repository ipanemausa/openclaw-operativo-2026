"""
==============================================================================
HB.OS (OPERATING SYSTEM) — MASTERCLASS CON VOZ REAL DE GUILLERMO (6.36 MIN)
==============================================================================
- Audio: 100% Voz Real Grabada de Guillermo (Guillermo_Podcast_Master_Edit_48k.wav)
- Branding: HB.OS (OPERATING SYSTEM) · SOVEREIGN AI (Cero 'OpenClaw')
- Layout: 100% Responsive con Auto-Wrap dinámico (Cero textos cortados)
- B-Roll: 40 Capturas Transparentes Puras Flotantes en el Cosmos
- Teleprompter: Zona Segura Elevada (Protegido de Controles de Reproductor)
==============================================================================
"""

import os
import sys
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_deepmind_hassabis_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hbos_real_voice"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

TRANSPARENT_CAPTURES_DIR = ROOT / "capturas_recientes" / "pure_transparent_png"
REAL_VOICE_AUDIO = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def init_stars(count=200):
    import random
    random.seed(101)
    stars = []
    for _ in range(count):
        stars.append({
            "x": random.uniform(0, WIDTH),
            "y": random.uniform(0, HEIGHT),
            "z": random.uniform(0.5, 4.0),
            "base_r": random.uniform(1.0, 3.0),
            "brightness": random.uniform(0.4, 1.0)
        })
    return stars

STARS = init_stars(200)

def draw_deep_cosmos(draw: ImageDraw.Draw, t: float):
    for y in range(0, HEIGHT, 10):
        ratio = y / HEIGHT
        r = int(3 + ratio * 6)
        g = int(6 + ratio * 10)
        b = int(18 + ratio * 28)
        draw.rectangle([0, y, WIDTH, y + 10], fill=(r, g, b))

    for s in STARS:
        shift_x = (s["x"] - t * s["z"] * 16) % WIDTH
        shift_y = (s["y"] + math.sin(t * 0.3 + s["x"]) * 5) % HEIGHT
        rad = s["base_r"] * (0.8 + 0.25 * math.sin(t * 2.5 + s["y"]))
        alpha = int(220 * s["brightness"] * (0.7 + 0.3 * math.sin(t * 3.0 + s["x"])))
        draw.ellipse([shift_x - rad, shift_y - rad, shift_x + rad, shift_y + rad], fill=(220, 235, 255, alpha))

def wrap_text_to_lines(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Divide un texto en múltiples líneas para que NUNCA se corte."""
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        bbox = font.getbbox(test_line)
        if (bbox[2] - bbox[0]) <= max_w:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

CHAPTERS_INFO = [
    {"start": 0.0, "end": 65.0, "cap": 1, "title": "Arquitectura de IA Soberana & Modelos Abiertos", "sub": "Independencia Tecnológica y Despliegue en Edge"},
    {"start": 65.0, "end": 130.0, "cap": 2, "title": "Gobernanza Vectorial en Espacio R^768", "sub": "Inferencia Determinista y Cero Alucinación"},
    {"start": 130.0, "end": 195.0, "cap": 3, "title": "Orquestación DAG & Pipelines Asíncronos", "sub": "Automatización Desatendida y Respaldo Continuo"},
    {"start": 195.0, "end": 260.0, "cap": 4, "title": "Modelos de Mundo y Robótica Física", "sub": "Percepción Tridimensional y Causa-Efecto"},
    {"start": 260.0, "end": 325.0, "cap": 5, "title": "Producción Audiovisual Multimodal HD", "sub": "Voz Real de Estudio 48kHz (-16 LUFS) & FastStart MP4"},
    {"start": 325.0, "end": 382.0, "cap": 6, "title": "El Futuro de la Ciencia Autónoma", "sub": "La IA como Instrumento Definitivo de Innovación B2B"}
]

def render_hbos_video():
    print("=" * 70)
    print("  HB.OS (OPERATING SYSTEM) — MASTERCLASS VOZ REAL (6.36 MIN)")
    print("=" * 70)

    total_dur = get_audio_duration(str(REAL_VOICE_AUDIO))
    total_frames = int(total_dur * FPS)
    print(f"-> Audio Real de Guillermo: {total_dur:.2f}s ({total_dur/60:.2f} minutos)")
    print(f"-> Total Fotogramas a Renderizar: {total_frames}")

    # Avatar Guillermo
    avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "frontend" / "public" / "avatars" / "avatar_transparent.png"

    raw_av = Image.open(avatar_path).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    av_x = WIDTH - av_w - 20

    # Capturas Transparentes
    all_pure_trans = sorted(list(TRANSPARENT_CAPTURES_DIR.glob("*_pure_trans.png")))
    broll_w, broll_h = 840, 472
    broll_cache = {}
    for i, cap_p in enumerate(all_pure_trans, 1):
        try:
            im = Image.open(cap_p).convert("RGBA")
            im = im.resize((broll_w, broll_h), Image.Resampling.LANCZOS)
            broll_cache[i] = im
        except Exception:
            pass

    try:
        font_top = ImageFont.truetype("arialbd.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 40)
        font_sub = ImageFont.truetype("arial.ttf", 24)
        font_teleprompter = ImageFont.truetype("arialbd.ttf", 44)
    except Exception:
        font_top = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_teleprompter = ImageFont.load_default()

    num_total_caps = len(all_pure_trans)

    for f_idx in range(total_frames):
        t = f_idx / FPS
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (4, 6, 18, 255))
        draw = ImageDraw.Draw(frame)

        # 1. Fondo Cósmico
        draw_deep_cosmos(draw, t)

        # 2. Barra Superior Minimalista Flotante (HB.OS)
        draw.line([60, 50, WIDTH - 60, 50], fill=(212, 175, 55), width=1)
        draw.text((60, 20), "HB.OS (OPERATING SYSTEM)", font=font_top, fill=(212, 175, 55))
        draw.text((440, 20), "·   VOZ REAL DE GUILLERMO HOYOS & DEEPMIND ARCHIVE", font=font_top, fill=(190, 200, 220))
        draw.text((1560, 20), "ESTÁNDAR 48KHZ · -16 LUFS", font=font_top, fill=(100, 220, 150))

        # 3. Determinar Capítulo Activo
        active_cap = CHAPTERS_INFO[-1]
        for c in CHAPTERS_INFO:
            if c["start"] <= t <= c["end"]:
                active_cap = c
                break

        # 4. B-Roll Transparente Puro Flotante a la Izquierda
        cap_idx = int((t / total_dur) * num_total_caps) + 1
        cap_idx = min(num_total_caps, max(1, cap_idx))

        broll_x, broll_y = 60, 90
        if cap_idx in broll_cache:
            trans_img = broll_cache[cap_idx]
            float_offset = int(math.sin(t * 1.3) * 5)
            frame.paste(trans_img, (broll_x, broll_y + float_offset), trans_img)
            draw.text((broll_x + 10, broll_y + broll_h + 10), f">> HB.OS ARCHIVE SLIDE #{cap_idx:02d}/40", font=font_badge, fill=(56, 189, 248))

        # 5. Avatar a la Derecha con levitación
        av_float = int(math.sin(t * 1.2) * 5)
        av_y = HEIGHT - av_h + av_float
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # 6. Título y Subtítulo 100% Responsive a la Derecha (Sin Cortes)
        header_x = 940
        header_y = 95
        max_title_w = 460  # Ancho seguro antes de tocar el avatar

        draw.text((header_x, header_y), f"CAPÍTULO {active_cap['cap']} · MASTERCLASS", font=font_badge, fill=(212, 175, 55))
        
        # Auto-wrap dinámico del título
        title_lines = wrap_text_to_lines(active_cap["title"], font_title, max_title_w)
        curr_title_y = header_y + 38
        for tl in title_lines:
            draw.text((header_x, curr_title_y), tl, font=font_title, fill=(255, 255, 255))
            curr_title_y += 48

        # Auto-wrap del subtítulo
        sub_lines = wrap_text_to_lines(">> " + active_cap["sub"], font_sub, max_title_w)
        curr_sub_y = curr_title_y + 10
        for sl in sub_lines:
            draw.text((header_x, curr_sub_y), sl, font=font_sub, fill=(100, 225, 185))
            curr_sub_y += 30

        draw.line([header_x, curr_sub_y + 15, WIDTH - 60, curr_sub_y + 15], fill=(45, 60, 90), width=1)

        # 7. Teleprompter Elevado a Zona Segura (y = 750 a 860)
        # Sombra suave + texto dorado y blanco
        tele_y = HEIGHT - 290
        draw.text((82, tele_y + 2), "LOCUCIÓN EN DIRECTO: GUILLERMO HOYOS (VOZ REAL)", font=font_teleprompter, fill=(0, 0, 0))
        draw.text((80, tele_y), "LOCUCIÓN EN DIRECTO: GUILLERMO HOYOS (VOZ REAL)", font=font_teleprompter, fill=(255, 215, 0))
        
        draw.text((82, tele_y + 62), f"Tema: {active_cap['title']}", font=font_teleprompter, fill=(0, 0, 0))
        draw.text((80, tele_y + 60), f"Tema: {active_cap['title']}", font=font_teleprompter, fill=(245, 248, 255))

        # 8. Barra de Progreso Inferior
        prog_pct = t / total_dur
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * prog_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = FRAMES_DIR / f"frame_{f_idx:06d}.jpg"
        frame.convert("RGB").save(str(frame_file), quality=92)

        if f_idx % 500 == 0:
            print(f"  -> Renderizado: {f_idx}/{total_frames} frames ({f_idx/total_frames*100:.1f}%)")

    print(f"[OK] Renderizados {total_frames} fotogramas.")

    # Codificar MP4
    output_mp4 = PROD_DIR / "PROD_20260824_HBOS_REAL_VOICE_MASTERCLASS_6MIN.mp4"
    cmd_encode = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%06d.jpg"),
        "-i", str(REAL_VOICE_AUDIO),
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        str(output_mp4)
    ]
    subprocess.run(cmd_encode, check=True)
    print(f"[OK] Video Maestro con Voz Real de Guillermo compilado: {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    render_hbos_video()
