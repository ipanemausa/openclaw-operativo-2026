"""
==============================================================================
HB. OS OPERATION SYSTEM — MASTERCLASS CINEMÁTICA FULL BACKGROUND (DEEPMIND)
==============================================================================
- Diseño Visual: Las capturas B-Roll son el BACKGROUND COMPLETO (1920x1080 Full Screen).
- Cero cajas, marcos o ventanas encerradas.
- Transición suave de imágenes de fondo según el capítulo.
- Avatar transparente de Guillermo HD integrado a la derecha.
- Header superior minimalista: 'HB. OS OPERATION SYSTEM'
- Teleprompter inferior flotante limpio con karaoke.
==============================================================================
"""

import os
import sys
import math
import glob
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_deepmind_cinematic_full_bg"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

CAPTURES_DIR = ROOT / "capturas_recientes"
AVATAR_PATH = ROOT / "scripts" / "avatar_guillermo_hd.png"
AUDIO_MASTER = ROOT / "runtime" / "productions" / "2026-08-24_hbos_deepmind_hd_master" / "PROD_HBOS_DEEPMIND_AUDIO_MASTER.aac"
OUTPUT_VIDEO = PROD_DIR / "PROD_HBOS_DEEPMIND_CINEMATIC_FULL_BG_1080P.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# 6 Módulos de DeepMind
DEEPMIND_MODULES = [
    {
        "module_id": "MOD_01",
        "chapter_num": 1,
        "title": "El Dominio de los Juegos y la Búsqueda Exponencial",
        "subtitle": "De AlphaGo Move 37 a AlphaStar en tiempo real",
        "capture_start": 1,
        "capture_end": 8,
        "text": (
            "¡Bienvenidos a HB punto OS Operation system! Para comprender realmente hacia dónde se dirige la inteligencia "
            "artificial general... debemos analizar los hitos fundamentales logrados por Demis Hassabis y Google "
            "DeepMind. Todo comenzó con un desafío colosal: la resolución de espacios de búsqueda infinitos. Desde aquella histórica "
            "e inolvidable jugada número treinta y siete de AlphaGo contra Lee Sedol... hasta la maestría táctica en tiempo "
            "real con AlphaStar en StarCraft dos. La inteligencia artificial demostró que el aprendizaje por "
            "refuerzo profundo no solo iguala al ser humano... ¡sino que descubre estrategias totalmente nuevas, intuitivas y sorprendentes!"
        )
    },
    {
        "module_id": "MOD_02",
        "chapter_num": 2,
        "title": "El Gran Momento Decisivo: AlphaFold",
        "subtitle": "Resolviendo el desafío biológico de 50 años en 3D",
        "capture_start": 9,
        "capture_end": 16,
        "text": (
            "Pero el verdadero punto de inflexión para toda la humanidad... ocurrió cuando DeepMind llevó estos principios "
            "a la ciencia pura. ¡Durante cincuenta años!, el enigma del plegamiento de proteínas fue considerado "
            "el mayor misterio de la biología. Con AlphaFold... lograron lo impensable: predecir la estructura tridimensional de más de "
            "doscientos millones de proteínas, cubriendo prácticamente todo el universo biológico conocido. Esta "
            "base de datos global, adoptada hoy por millones de científicos... ¡transformó décadas de investigación en cuestión de segundos!"
        )
    },
    {
        "module_id": "MOD_03",
        "chapter_num": 3,
        "title": "Arquitectura Molecular: El Complejo del Poro Nuclear",
        "subtitle": "Mapeando la máquina biológica más intrincada de la célula",
        "capture_start": 17,
        "capture_end": 22,
        "text": (
            "El impacto de esta revolución no se detuvo en proteínas aisladas. AlphaFold permitió mapear complejos "
            "macromoleculares gigantescos... como el complejo del poro nuclear: la puerta de enlace que regula el "
            "transporte genético en nuestras células. Lo que antes exigía años interminables de cristalografía y microscopía "
            "crioelectrónica... ahora puede ser modelado con precisión atómica. ¡Una ventana sin precedentes a la maquinaria misma de la vida!"
        )
    },
    {
        "module_id": "MOD_04",
        "chapter_num": 4,
        "title": "Genómica y Diseño de Fármacos in Silico",
        "subtitle": "AlphaGenome y la exploración del noventa y ocho por ciento no codificante",
        "capture_start": 23,
        "capture_end": 28,
        "text": (
            "El siguiente gran salto de frontera... es el diseño de fármacos in silico y la comprensión profunda del genoma humano. "
            "A través de iniciativas como AlphaGenome, estamos comenzando a descifrar el noventa y ocho por "
            "ciento del ADN... que durante décadas se consideró erróneamente basura genética. Esta capacidad "
            "permite predecir el acoplamiento químico exacto de nuevas moléculas... acelerando el desarrollo "
            "de terapias que salvarán vidas, a una fracción del costo tradicional."
        )
    },
    {
        "module_id": "MOD_05",
        "chapter_num": 5,
        "title": "Modelos de Mundo y Robótica Física",
        "subtitle": "Cerrando la brecha entre la percepción digital y la acción material",
        "capture_start": 29,
        "capture_end": 34,
        "text": (
            "Demis Hassabis enfatiza con claridad: el futuro de la inteligencia artificial radica en los Modelos de Mundo. "
            "Para interactuar con la realidad física a través de la robótica... los agentes no pueden depender "
            "únicamente de texto; deben internalizar la física, el espacio tridimensional, la causa "
            "y el efecto. Estos modelos de mundo permiten a los robots aprender en simulación acelerada... ¡y actuar en el mundo real con destreza y total seguridad!"
        )
    },
    {
        "module_id": "MOD_06",
        "chapter_num": 6,
        "title": "Soberanía Computacional y Ciencia Autónoma",
        "subtitle": "La IA como el microscopio definitivo del siglo veintiuno",
        "capture_start": 35,
        "capture_end": 40,
        "text": (
            "En HB punto OS Operation system consolidamos esta visión bajo el principio inquebrantable de la Soberanía Tecnológica. "
            "La inteligencia artificial no es solo un asistente; es el instrumento científico "
            "definitivo para acelerar el conocimiento humano. Integrando vectores en dimensión "
            "setecientos sesenta y ocho, orquestación determinista y modelos abiertos... construimos la "
            "infraestructura de automatización del futuro. ¡Gracias por acompañarnos en esta masterclass!"
        )
    }
]

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def load_all_captures() -> list[Image.Image]:
    """Carga todas las capturas y las prepara en Full HD 1920x1080."""
    files = sorted(glob.glob(str(CAPTURES_DIR / "*.png")) + glob.glob(str(CAPTURES_DIR / "*.jpg")))
    images = []
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
            # Escalar a pantalla completa 1920x1080 manteniendo aspect ratio y crop central
            im_ratio = im.width / im.height
            target_ratio = WIDTH / HEIGHT
            if im_ratio > target_ratio:
                new_w = int(HEIGHT * im_ratio)
                im_scaled = im.resize((new_w, HEIGHT), Image.Resampling.LANCZOS)
                x_crop = (new_w - WIDTH) // 2
                im_cropped = im_scaled.crop((x_crop, 0, x_crop + WIDTH, HEIGHT))
            else:
                new_h = int(WIDTH / im_ratio)
                im_scaled = im.resize((WIDTH, new_h), Image.Resampling.LANCZOS)
                y_crop = (new_h - HEIGHT) // 2
                im_cropped = im_scaled.crop((0, y_crop, WIDTH, y_crop + HEIGHT))
            
            # Oscurecer sutilmente la imagen para que funcione como background cinematográfico
            enhancer = ImageEnhance.Brightness(im_cropped)
            im_dark = enhancer.enhance(0.55)
            images.append(im_dark)
        except Exception as e:
            print(f"Error cargando captura {f}: {e}")
    return images

def load_fonts():
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_text = ImageFont.truetype("arialbd.ttf", 34)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
    except Exception:
        font_header = font_title = font_text = font_badge = ImageFont.load_default()
    return font_header, font_title, font_text, font_badge

def render_cinematic_full_bg_video():
    print("=" * 80)
    print("  HB.OS — MASTERCLASS CINEMÁTICA FULL BACKGROUND (DEEPMIND)")
    print("=" * 80)

    if not AUDIO_MASTER.exists():
        print(f"❌ Error: Archivo de audio maestro no encontrado en {AUDIO_MASTER}")
        return

    total_duration = get_audio_duration(AUDIO_MASTER)
    total_frames = int(total_duration * FPS)
    print(f"  ✓ Duración del video: {total_duration:.2f}s ({total_duration/60:.2f} min)")
    print(f"  ✓ Total de fotogramas Full HD a compilar: {total_frames}")

    bg_captures = load_all_captures()
    print(f"  ✓ Total de fondos Full HD cargados: {len(bg_captures)}")

    font_header, font_title, font_text, font_badge = load_fonts()

    # Cargar Avatar de Guillermo en HD
    avatar_img = None
    if AVATAR_PATH.exists():
        av = Image.open(AVATAR_PATH).convert("RGBA")
        av_h = int(HEIGHT * 0.72)
        av_w = int(av.width * (av_h / av.height))
        avatar_img = av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    # Máscara de gradiente oscuro cinematográfico (viñeta de cine para lectura perfecta)
    grad_mask = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(grad_mask)
    # Header oscuro arriba
    for y in range(120):
        alpha = int(220 * (1 - y / 120))
        d_grad.line([(0, y), (WIDTH, y)], fill=(5, 8, 15, alpha))
    # Bottom teleprompter oscuro abajo
    for y in range(HEIGHT - 280, HEIGHT):
        prog = (y - (HEIGHT - 280)) / 280.0
        alpha = int(235 * (prog ** 1.2))
        d_grad.line([(0, y), (WIDTH, y)], fill=(3, 6, 12, alpha))
    # Derecha oscura para contrastar avatar
    for x in range(WIDTH - 700, WIDTH):
        prog = (x - (WIDTH - 700)) / 700.0
        alpha = int(140 * prog)
        d_grad.line([(x, 0), (x, HEIGHT)], fill=(2, 4, 8, alpha))

    # Pre-renderizar fotogramas
    dur_per_mod = total_duration / len(DEEPMIND_MODULES)

    print("\n[RENDER] Generando fotogramas cinemáticos Full Screen...")
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        mod_idx = min(int(t / dur_per_mod), len(DEEPMIND_MODULES) - 1)
        mod = DEEPMIND_MODULES[mod_idx]
        mod_t = t - (mod_idx * dur_per_mod)
        mod_progress = mod_t / dur_per_mod

        # Selección de fondo dinámico que cambia fluidamente
        cap_count = len(bg_captures)
        if cap_count > 0:
            cap_idx = int((t / total_duration) * cap_count) % cap_count
            bg_base = bg_captures[cap_idx].copy()
        else:
            bg_base = Image.new("RGB", (WIDTH, HEIGHT), (10, 14, 26))

        # Componer gradiente cinemático sobre el fondo
        frame = Image.alpha_composite(bg_base.convert("RGBA"), grad_mask)

        # Avatar integrado a la derecha
        if avatar_img:
            av_x = WIDTH - avatar_img.width - 40
            av_y = HEIGHT - avatar_img.height - 30
            # Sombra suave del avatar
            frame.paste(avatar_img, (av_x, av_y), avatar_img)

        draw = ImageDraw.Draw(frame)

        # ─── HEADER MINIMALISTA SUPERIOR (HB. OS OPERATION SYSTEM) ───
        draw.text((60, 30), "HB. OS OPERATION SYSTEM", fill=(255, 255, 255), font=font_header)
        draw.text((450, 30), f"|  CAP. {mod['chapter_num']}: {mod['title'].upper()}", fill=(0, 220, 255), font=font_header)
        
        # Badge Sovereign AI a la derecha
        draw.rectangle([(WIDTH - 280, 25), (WIDTH - 60, 65)], fill=(0, 45, 90, 200), outline=(0, 180, 255), width=1)
        draw.text((WIDTH - 265, 33), "HB.OS · SOVEREIGN AI", fill=(255, 255, 255), font=font_badge)

        # ─── TELEPROMPTER / SUBTÍTULOS INFERIORES CINEMÁTICOS ───
        words = mod["text"].split()
        words_per_window = 14
        total_windows = max(1, math.ceil(len(words) / words_per_window))
        window_idx = min(int(mod_progress * total_windows), total_windows - 1)
        start_w = window_idx * words_per_window
        window_words = words[start_w : start_w + words_per_window]
        
        line1 = " ".join(window_words[:7])
        line2 = " ".join(window_words[7:])

        # Caja de teleprompter limpia y elegante
        draw.text((70, HEIGHT - 200), line1, fill=(255, 205, 50), font=font_text)
        if line2:
            draw.text((70, HEIGHT - 145), line2, fill=(255, 255, 255), font=font_text)

        # Barra de progreso del capítulo
        prog_w = int((WIDTH - 140) * (t / total_duration))
        draw.line([(70, HEIGHT - 40), (WIDTH - 70, HEIGHT - 40)], fill=(40, 50, 70), width=3)
        draw.line([(70, HEIGHT - 40), (70 + prog_w, HEIGHT - 40)], fill=(0, 215, 255), width=3)

        # Guardar frame
        out_frame_path = FRAMES_DIR / f"frame_{frame_idx:06d}.jpg"
        frame.convert("RGB").save(out_frame_path, quality=94)

        if frame_idx % 400 == 0 or frame_idx == total_frames - 1:
            print(f"  -> Progreso Render Full BG: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

    # Compilar con FFmpeg FastStart
    print("\n[CODIFICANDO] Ensamblando video Full Background 1080p con FFmpeg...")
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
        str(OUTPUT_VIDEO)
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"\n🏆 VIDEO FULL BACKGROUND GENERADO EXITOSAMENTE:")
    print(f"📁 {OUTPUT_VIDEO}")

if __name__ == "__main__":
    render_cinematic_full_bg_video()
