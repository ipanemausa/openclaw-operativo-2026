"""
==============================================================================
HB. OS OPERATION SYSTEM — MASTERCLASS DEEPMIND CON NARRACIÓN Y TELEPROMPTER SINCRONIZADO
==============================================================================
- Guion: Curado en balas con pausas de respiración y prosodia de autoridad afable
- Audio: 100% Tu Voz Real Grabada (Guillermo_Podcast_Master_Edit_48k.wav)
- B-Roll: 40 Capturas de DeepMind 100% LIMPIAS (deepmind_clean_no_cc)
- Avatar: Avatar Transparente HD Oficial de Guillermo (assets/avatar_transparent_hbos.png)
- Teleprompter: Sincronizado dinámicamente con las balas del guion en zona segura
- Branding: HB. OS OPERATION SYSTEM · SOVEREIGN AI
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

PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_hbos_deepmind_synchronized_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_DIR = ROOT / "capturas_recientes" / "deepmind_clean_no_cc"
AVATAR_PATH = ROOT / "assets" / "avatar_transparent_hbos.png"
AUDIO_MASTER = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
FINAL_VIDEO = PROD_DIR / "PROD_HBOS_DEEPMIND_SYNCHRONIZED_MASTER_1080P.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── GUION MAESTRO CURADO EN BALAS JERÁRQUICAS DE RESPIRACIÓN ───
MASTER_MODULES = [
    {
        "chapter_num": 1,
        "title": "El Dominio de los Juegos y la Búsqueda Exponencial",
        "bullets": [
            "¡Bienvenidos a HB punto OS Operation system!",
            "Para comprender hacia dónde se dirige la IA general, analizamos los hitos de Demis Hassabis y DeepMind.",
            "Todo comenzó con un desafío colosal: la resolución de espacios de búsqueda infinitos.",
            "De la jugada 37 de AlphaGo contra Lee Sedol, a la maestría en tiempo real con AlphaStar en StarCraft II.",
            "El aprendizaje profundo no solo iguala la intuición humana: ¡descubre estrategias totalmente nuevas e invisibles!"
        ]
    },
    {
        "chapter_num": 2,
        "title": "El Gran Momento Decisivo: AlphaFold",
        "bullets": [
            "El verdadero punto de inflexión para la humanidad ocurrió cuando DeepMind llevó esto a la ciencia pura.",
            "¡Durante cincuenta años!, el enigma del plegamiento de proteínas fue el mayor misterio de la biología.",
            "Con AlphaFold predijeron la estructura 3D de más de doscientos millones de proteínas en el planeta.",
            "Esta base de datos global adoptada por millones de científicos aceleró décadas de trabajo en segundos."
        ]
    },
    {
        "chapter_num": 3,
        "title": "Arquitectura Molecular: El Complejo del Poro Nuclear",
        "bullets": [
            "El impacto de esta revolución no se detuvo en proteínas individuales aisladas.",
            "AlphaFold permitió mapear macromoléculas gigantescas como el Complejo del Poro Nuclear en nuestras células.",
            "Lo que antes exigía años de cristalografía de rayos X, ahora se modela con precisión atómica.",
            "¡Una ventana sin precedentes a la maquinaria fundamental de la vida misma!"
        ]
    },
    {
        "chapter_num": 4,
        "title": "Genómica y Diseño de Fármacos in Silico",
        "bullets": [
            "El siguiente gran salto de frontera es el diseño de fármacos in silico y la comprensión del genoma.",
            "Con AlphaGenome comenzamos a descifrar el 98% del ADN considerado erróneamente basura genética.",
            "Permite predecir el acoplamiento químico directo de nuevas moléculas y terapias personalizadas.",
            "Acelerando tratamientos que salvarán vidas a una fracción del costo tradicional."
        ]
    },
    {
        "chapter_num": 5,
        "title": "Modelos de Mundo y Robótica Física",
        "bullets": [
            "Demis Hassabis lo enfatiza con claridad: el futuro radica en los Modelos de Mundo.",
            "Para interactuar con el entorno mediante robótica, los agentes deben internalizar la física y el espacio.",
            "Comprender la masa, la inercia, la causa y el efecto en tres dimensiones.",
            "Permite a los robots aprender en simulación acelerada y actuar en el mundo real con destreza y seguridad."
        ]
    },
    {
        "chapter_num": 6,
        "title": "Soberanía Computacional y Ciencia Autónoma",
        "bullets": [
            "En HB punto OS Operation system consolidamos esta visión bajo la Soberanía Tecnológica.",
            "La inteligencia artificial es el instrumento científico definitivo para acelerar el conocimiento.",
            "Integrando vectores en espacio euclidiano R^768, grafos deterministas y modelos abiertos soberanos.",
            "Construimos la infraestructura de automatización del futuro. ¡Gracias por acompañarnos!"
        ]
    }
]

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def load_clean_captures():
    files = sorted(glob.glob(str(CLEAN_DIR / "*.png")))
    images = []
    card_w, card_h = 1060, 596
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
            im_scaled = im.resize((card_w, card_h), Image.Resampling.LANCZOS)
            images.append(im_scaled)
        except Exception as e:
            print(f"Error: {e}")
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
        font_bullet_active = ImageFont.truetype("arialbd.ttf", 30)
        font_bullet_dim = ImageFont.truetype("arialbd.ttf", 26)
    except Exception:
        font_header = font_badge = font_label = font_tele_title = font_bullet_active = font_bullet_dim = ImageFont.load_default()
    return font_header, font_badge, font_label, font_tele_title, font_bullet_active, font_bullet_dim

def main():
    print("=" * 80)
    print("  HB.OS — MASTERCLASS SINCRONIZADA: BALAS DE TELEPROMPTER + TU VOZ REAL")
    print("=" * 80)

    total_duration = get_audio_duration(AUDIO_MASTER)
    total_frames = int(total_duration * FPS)
    print(f"  ✓ Pista de Voz: {AUDIO_MASTER.name} ({total_duration:.2f}s / {total_duration/60:.2f} min)")
    print(f"  ✓ Fotogramas a compilar: {total_frames}")

    deepmind_caps = load_clean_captures()
    print(f"  ✓ Capturas limpias de DeepMind cargadas: {len(deepmind_caps)}")

    if not AVATAR_PATH.exists():
        print(f"❌ Error: Avatar no encontrado en {AVATAR_PATH}")
        return
    av_raw = Image.open(AVATAR_PATH).convert("RGBA")
    target_av_h = 800
    target_av_w = int(av_raw.width * (target_av_h / av_raw.height))
    avatar_img = av_raw.resize((target_av_w, target_av_h), Image.Resampling.LANCZOS)
    print(f"  ✓ Avatar de Guillermo HD cargado ({target_av_w}x{target_av_h})")

    font_header, font_badge, font_label, font_tele_title, font_bullet_active, font_bullet_dim = load_fonts()

    card_x, card_y = 60, 110
    card_w, card_h = 1060, 596

    dur_per_mod = total_duration / len(MASTER_MODULES)

    print("\n[RENDER] Compilando fotogramas sincronizados con el teleprompter en balas...")
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        mod_idx = min(int(t / dur_per_mod), len(MASTER_MODULES) - 1)
        mod = MASTER_MODULES[mod_idx]
        mod_t = t - (mod_idx * dur_per_mod)
        mod_progress = mod_t / dur_per_mod

        frame = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
        draw = ImageDraw.Draw(frame)

        # 1. Fondo Cósmico
        draw_cosmic_bg(draw, t)

        # 2. B-Roll de DeepMind 100% LIMPIO
        if len(deepmind_caps) > 0:
            cap_idx = int((t / total_duration) * len(deepmind_caps)) % len(deepmind_caps)
            cap_img = deepmind_caps[cap_idx]
            
            draw.rectangle([(card_x - 2, card_y - 2), (card_x + card_w + 2, card_y + card_h + 2)], outline=(0, 200, 255, 180), width=2)
            frame.paste(cap_img, (card_x, card_y))

            draw.rectangle([(card_x + 15, card_y + 15), (card_x + 310, card_y + 50)], fill=(0, 20, 45, 220), outline=(0, 180, 255, 200), width=1)
            draw.text((card_x + 25, card_y + 20), f"DEEPMIND ARCHIVE #{cap_idx+1:02d}/{len(deepmind_caps)}", fill=(0, 240, 255), font=font_label)

        # 3. Avatar Transparente de Guillermo integrado a la derecha
        av_pos_x = WIDTH - target_av_w - 40
        av_pos_y = HEIGHT - target_av_h - 10
        frame.paste(avatar_img, (av_pos_x, av_pos_y), avatar_img)

        # 4. Header Superior HB.OS
        draw.rectangle([(0, 0), (WIDTH, 75)], fill=(5, 12, 28, 230))
        draw.line([(0, 75), (WIDTH, 75)], fill=(0, 180, 255, 120), width=1)
        draw.text((60, 22), "HB. OS OPERATION SYSTEM", fill=(255, 255, 255), font=font_header)
        draw.text((450, 22), f"|  CAP. {mod['chapter_num']}: {mod['title'].upper()}", fill=(0, 220, 255), font=font_header)

        # Badge Sovereign AI
        draw.rectangle([(WIDTH - 280, 18), (WIDTH - 60, 58)], fill=(0, 40, 85, 220), outline=(0, 180, 255, 200), width=1)
        draw.text((WIDTH - 265, 26), "HB.OS · SOVEREIGN AI", fill=(255, 255, 255), font=font_badge)

        # 5. TELEPROMPTER EN BALAS JERÁRQUICAS (ZONA SEGURA CENTRADA)
        tele_y = HEIGHT - 330
        tele_h = 240
        draw.rectangle([(card_x, tele_y), (card_x + card_w, tele_y + tele_h)], fill=(6, 15, 35, 235), outline=(0, 180, 255, 180), width=1)
        
        draw.text((card_x + 30, tele_y + 15), "🎙️ TELEPROMPTER · NARRACIÓN GUILLERMO HOYOS", fill=(255, 205, 50), font=font_tele_title)

        # Bala activa actual dentro del módulo
        num_bullets = len(mod["bullets"])
        active_bullet_idx = min(int(mod_progress * num_bullets), num_bullets - 1)
        
        # Mostrar la bala activa en dorado/blanco grande
        active_text = mod["bullets"][active_bullet_idx]
        
        # Word wrap de la bala activa en 2 líneas
        words = active_text.split()
        if len(words) > 9:
            line1 = " ".join(words[:9])
            line2 = " ".join(words[9:])
        else:
            line1 = active_text
            line2 = ""

        draw.text((card_x + 30, tele_y + 65), f"• {line1}", fill=(255, 220, 60), font=font_bullet_active)
        if line2:
            draw.text((card_x + 55, tele_y + 110), line2, fill=(255, 255, 255), font=font_bullet_active)

        # Sub-bala siguiente en tenue (anticipación de lectura)
        if active_bullet_idx + 1 < num_bullets:
            next_text = mod["bullets"][active_bullet_idx + 1]
            if len(next_text) > 12:
                next_text = " ".join(next_text.split()[:11]) + "..."
            draw.text((card_x + 30, tele_y + 160), f"  → {next_text}", fill=(120, 160, 200), font=font_bullet_dim)

        # Barra de cadencia de narración
        prog_w = int((card_w - 60) * (t / total_duration))
        draw.line([(card_x + 30, tele_y + 215), (card_x + card_w - 30, tele_y + 215)], fill=(30, 50, 80), width=4)
        draw.line([(card_x + 30, tele_y + 215), (card_x + 30 + prog_w, tele_y + 215)], fill=(0, 220, 255), width=4)

        out_frame_path = FRAMES_DIR / f"frame_{frame_idx:06d}.jpg"
        frame.convert("RGB").save(out_frame_path, quality=94)

        if frame_idx % 600 == 0 or frame_idx == total_frames - 1:
            print(f"  -> Progreso Render HD: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

    # Codificación FastStart
    print("\n[CODIFICANDO] Ensamblando video Full HD sincronizado con TU VOZ REAL...")
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
    print(f"\n🏆 MASTERCLASS SINCRONIZADA GENERADA EXITOSAMENTE:")
    print(f"📁 {FINAL_VIDEO}")

if __name__ == "__main__":
    main()
