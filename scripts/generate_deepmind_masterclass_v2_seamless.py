"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS CÓSMICA SEAMLESS V2.0: DEEPMIND & DEMIS HASSABIS
Bilingüe: Español (ES) & Inglés (EN)
Diseño: 100% Sin Cajas | B-Roll Holográfico con Bordes Suaves | Teleprompter Centrado
==============================================================================
"""

import os
import sys
import math
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts

ROOT = Path(__file__).parent.parent
PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_deepmind_hassabis_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
CAPTURES_DIR = ROOT / "capturas_recientes"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Módulos bilingües
MODULES_BILINGUAL = [
    {
        "module_id": "MOD_01",
        "chapter_num": 1,
        "title_es": "El Dominio de los Juegos y la Búsqueda Exponencial",
        "title_en": "Mastering Games and Exponential Search Spaces",
        "concept_es": "De AlphaGo (Move 37) a AlphaStar en Tiempo Real",
        "concept_en": "From AlphaGo (Move 37) to Real-Time AlphaStar",
        "capture_start": 1,
        "capture_end": 8,
        "text_es": (
            "Bienvenidos a OpenClaw 2026. Para comprender el futuro de la inteligencia artificial, "
            "debemos analizar los hitos fundamentales de Demis Hassabis y Google DeepMind. "
            "Desde la histórica jugada número treinta y siete de AlphaGo contra Lee Sedol, "
            "hasta la maestría táctica en tiempo real con AlphaStar en StarCraft dos, "
            "la IA demostró que el aprendizaje por refuerzo profundo es capaz de descubrir "
            "estrategias totalmente nuevas e intuitivas."
        ),
        "text_en": (
            "Welcome to OpenClaw 2026. To understand where general artificial intelligence is heading, "
            "we must examine the fundamental breakthroughs of Demis Hassabis and Google DeepMind. "
            "From AlphaGo's historic move thirty-seven against Lee Sedol, to real-time tactical mastery "
            "in StarCraft two with AlphaStar, artificial intelligence proved that deep reinforcement learning "
            "discovers entirely new, intuitive strategies."
        )
    },
    {
        "module_id": "MOD_02",
        "chapter_num": 2,
        "title_es": "El Gran Momento Decisivo: AlphaFold",
        "title_en": "The Watershed Moment: AlphaFold",
        "concept_es": "Resolviendo el Enigma del Plegamiento 3D de Proteínas",
        "concept_en": "Solving the 50-Year 3D Protein Folding Challenge",
        "capture_start": 9,
        "capture_end": 16,
        "text_es": (
            "El punto de inflexión decisivo ocurrió cuando DeepMind aplicó estos principios a la ciencia pura. "
            "Durante cincuenta años, el problema del plegamiento de proteínas fue el mayor misterio biológico. "
            "Con AlphaFold, predijeron la estructura tridimensional de más de doscientos millones de proteínas, "
            "mapeando prácticamente todo el universo biológico conocido y ahorrando siglos de experimentación."
        ),
        "text_en": (
            "The true watershed moment arrived when DeepMind brought these algorithms to fundamental science. "
            "For fifty years, protein folding stood as biology's grand challenge. "
            "With AlphaFold, they mapped the 3D structures of over two hundred million proteins, "
            "covering nearly the entire known biological universe and accelerating decades of research into seconds."
        )
    },
    {
        "module_id": "MOD_03",
        "chapter_num": 3,
        "title_es": "Arquitectura Molecular: El Poro Nuclear",
        "title_en": "Molecular Architecture: The Nuclear Pore Complex",
        "concept_es": "Mapeando la Máquina Biológica Más Intrincada de la Célula",
        "concept_en": "Mapping the Cell's Most Intricate Molecular Gateway",
        "capture_start": 17,
        "capture_end": 22,
        "text_es": (
            "AlphaFold permitió modelar complejos macromoleculares gigantescos como el complejo del poro nuclear, "
            "la compuerta que regula el transporte genético en la célula humana. Lo que antes requería años "
            "de cristalografía y microscopía crioelectrónica, ahora se modela con precisión atómica directa."
        ),
        "text_en": (
            "AlphaFold enabled the modeling of massive macromolecular assemblies like the nuclear pore complex, "
            "the cellular gateway that governs genetic transport. What once required decades of crystallography "
            "and cryo-electron microscopy can now be simulated directly at atomic resolution."
        )
    },
    {
        "module_id": "MOD_04",
        "chapter_num": 4,
        "title_es": "Genómica y Diseño de Fármacos in Silico",
        "title_en": "Genomics and in Silico Drug Design",
        "concept_es": "AlphaGenome y el 98% del ADN No Codificante",
        "concept_en": "AlphaGenome and Decoding Non-Coding DNA",
        "capture_start": 23,
        "capture_end": 28,
        "text_es": (
            "A través de AlphaGenome, la investigación avanza hacia el descifrado del noventa y ocho por ciento "
            "del genoma que antes se consideraba no codificante. Esto permite el diseño de fármacos in silico "
            "y la predicción de acoplamientos moleculares para acelerar terapias de alta precisión."
        ),
        "text_en": (
            "Through initiatives like AlphaGenome, research is now decoding the ninety-eight percent of the genome "
            "previously thought to be non-coding. This powers in silico drug discovery, predicting molecular binding "
            "to accelerate personalized therapeutics at unprecedented speeds."
        )
    },
    {
        "module_id": "MOD_05",
        "chapter_num": 5,
        "title_es": "Modelos de Mundo y Robótica Física",
        "title_en": "World Models and Embodied Robotics",
        "concept_es": "Internalizando Física, Espacio 3D, Causa y Efecto",
        "concept_en": "Internalizing 3D Physics, Space, Cause and Effect",
        "capture_start": 29,
        "capture_end": 34,
        "text_es": (
            "Demis Hassabis destaca que la frontera de la robótica requiere Modelos de Mundo. "
            "Para interactuar con la materia, los agentes autónomos deben comprender la física tridimensional, "
            "la causalidad y el espacio real, permitiendo a los robots actuar con destreza y seguridad."
        ),
        "text_en": (
            "Demis Hassabis emphasizes that the future of robotics demands World Models. "
            "To interact with the physical universe, autonomous agents must internalize 3D spatial physics, "
            "causality, and material dynamics, enabling embodied robots to act dexterously and safely."
        )
    },
    {
        "module_id": "MOD_06",
        "chapter_num": 6,
        "title_es": "Soberanía Computacional y Ciencia Autónoma",
        "title_en": "Computational Sovereignty and Autonomous Science",
        "concept_es": "La IA como el Microscopio Definitivo del Siglo XXI",
        "concept_en": "AI as the Ultimate Microscope of the 21st Century",
        "capture_start": 35,
        "capture_end": 40,
        "text_es": (
            "En OpenClaw concebimos la IA no solo como un asistente, sino como el microscopio definitivo "
            "para la aceleración científica humana. Unificando gobernanza vectorial, modelos abiertos y "
            "automatización determinista, construimos la infraestructura soberana del futuro."
        ),
        "text_en": (
            "At OpenClaw, we envision AI not merely as an assistant, but as the ultimate scientific microscope "
            "for human discovery. Uniting vector governance, open-weight foundation models, and deterministic "
            "automation, we build the sovereign AI infrastructure of tomorrow."
        )
    }
]

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_language_audio(lang="es"):
    print(f"\n[FASE 1/4] Sintetizando locucion ({lang.upper()}) con calibracion acustica...")
    voice_name = "es-CO-GonzaloNeural" if lang == "es" else "en-US-ChristopherNeural"
    rate_val = "-6%" if lang == "es" else "-4%"

    for mod in MODULES_BILINGUAL:
        text_content = mod["text_es"] if lang == "es" else mod["text_en"]
        raw_mp3 = PROD_DIR / f"{mod['module_id']}_{lang}_raw.mp3"
        master_aac = PROD_DIR / f"{mod['module_id']}_{lang}_master_48k.aac"

        comm = edge_tts.Communicate(text_content, voice=voice_name, rate=rate_val, pitch="-2Hz")
        await comm.save(str(raw_mp3))

        eq_chain = (
            "highpass=f=80,"
            "equalizer=f=220:t=q:w=1.2:g=2.8,"
            "equalizer=f=500:t=q:w=1.5:g=-2.2,"
            "equalizer=f=3500:t=q:w=1.0:g=3.8,"
            "equalizer=f=10000:t=q:w=1.0:g=2.2,"
            "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
            "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(master_aac)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        dur = get_audio_duration(str(master_aac))
        mod[f"audio_file_{lang}"] = str(master_aac)
        mod[f"duration_{lang}"] = dur
        print(f"  [OK] {mod['module_id']} ({lang}) | Duracion: {dur:.2f}s")

def assemble_soundtrack(lang="es") -> tuple[Path, float]:
    pause_file = PROD_DIR / "pause_1s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", str(pause_file)
    ]
    subprocess.run(cmd_pause, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    concat_txt = PROD_DIR / f"concat_audio_{lang}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for mod in MODULES_BILINGUAL:
            f.write(f"file '{Path(mod[f'audio_file_{lang}']).as_posix()}'\n")
            f.write(f"file '{pause_file.as_posix()}'\n")

    master_audio_path = PROD_DIR / f"PROD_20260824_DEEPMIND_AUDIO_{lang.upper()}_V2.0.aac"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(master_audio_path)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    total_dur = get_audio_duration(str(master_audio_path))
    return master_audio_path, total_dur

# Función para aplicar desvanecimiento suave (feathering) a las imágenes B-Roll
def create_holographic_broll(image_path: Path, target_w=820, target_h=460) -> Image.Image:
    im = Image.open(image_path).convert("RGBA")
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Crear máscara radial / viñeta suave
    mask = Image.new("L", (target_w, target_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    
    # Rectángulo interior con borde difuso
    margin = 35
    draw_mask.rectangle([margin, margin, target_w - margin, target_h - margin], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    
    # Aplicar máscara a la imagen
    im.putalpha(mask)
    return im

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

def render_seamless_frames(lang="es", total_duration=170.0):
    frames_dir = PROD_DIR / f"frames_v2_{lang}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "frontend" / "public" / "avatars" / "avatar_transparent.png"

    raw_av = Image.open(avatar_path).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    all_captures = sorted(list(CAPTURES_DIR.glob("Screenshot 2026-08-24*.png")))
    broll_w, broll_h = 840, 472
    broll_cache = {}
    for i, cap_p in enumerate(all_captures, 1):
        try:
            broll_cache[i] = create_holographic_broll(cap_p, broll_w, broll_h)
        except Exception as e:
            pass

    timeline = []
    curr_t = 0.0
    for mod in MODULES_BILINGUAL:
        t_start = curr_t
        t_end = curr_t + mod[f"duration_{lang}"]
        timeline.append({"mod": mod, "start": t_start, "end": t_end})
        curr_t = t_end + 1.0

    try:
        font_top = ImageFont.truetype("arialbd.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 52)
    except Exception:
        font_top = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()

    total_frames = int(total_duration * FPS)
    WORDS_PER_CHUNK = 8

    print(f"\n[FASE 3/4] Renderizando {total_frames} fotogramas Seamless V2 ({lang.upper()}) sin cajas...")

    for f_idx in range(total_frames):
        t = f_idx / FPS
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (4, 6, 18, 255))
        draw = ImageDraw.Draw(frame)

        # 1. Fondo cósmico
        draw_deep_cosmos(draw, t)

        # Barra superior minimalista flotante (Línea dorada sin cajas)
        draw.line([60, 50, WIDTH - 60, 50], fill=(212, 175, 55), width=1)
        draw.text((60, 20), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 20), "·   SOVEREIGN AI RESEARCH & DEMIS HASSABIS DEEPMIND ARCHIVE", font=font_top, fill=(190, 200, 220))
        draw.text((1600, 20), "ESTANDAR R^768 · 48KHZ", font=font_top, fill=(100, 220, 150))

        active = None
        for entry in timeline:
            if entry["start"] <= t <= entry["end"]:
                active = entry
                break

        if active:
            mod = active["mod"]
            local_t = t - active["start"]
            progress = max(0.0, min(1.0, local_t / mod[f"duration_{lang}"]))

            # Título y Concepto Flotante
            title_txt = mod["title_es"] if lang == "es" else mod["title_en"]
            concept_txt = mod["concept_es"] if lang == "es" else mod["concept_en"]
            text_speech = mod["text_es"] if lang == "es" else mod["text_en"]

            # 2. B-Roll Holográfico Flotante (Lado Izquierdo Superior)
            cap_start = mod["capture_start"]
            cap_end = mod["capture_end"]
            num_caps = cap_end - cap_start + 1
            curr_cap_idx = cap_start + int(progress * num_caps)
            curr_cap_idx = min(cap_end, max(cap_start, curr_cap_idx))

            broll_x, broll_y = 70, 90
            if curr_cap_idx in broll_cache:
                holo_img = broll_cache[curr_cap_idx]
                # Efecto flotante suave
                float_offset = int(math.sin(t * 1.5) * 4)
                frame.paste(holo_img, (broll_x, broll_y + float_offset), holo_img)
                # Etiqueta minimalista flotante (sin recuadro invasivo)
                draw.text((broll_x + 10, broll_y + broll_h + 10), f">> DEEPMIND SLIDE #{curr_cap_idx:02d}/40", font=font_badge, fill=(56, 189, 248))

            # 3. Avatar de Guillermo a la Derecha (PNG 100% Transparente sin Marcos)
            av_float = int(math.sin(t * 1.2) * 5)
            av_x = WIDTH - av_w - 20
            av_y = HEIGHT - av_h + av_float
            frame.paste(avatar_png, (av_x, av_y), avatar_png)

            # 4. Encabezados Flotantes de Capítulo
            header_x = 940
            header_y = 100
            draw.text((header_x, header_y), f"CAPITULO {mod['chapter_num']} · DEEPMIND MASTERCLASS", font=font_badge, fill=(212, 175, 55))
            draw.text((header_x, header_y + 40), title_txt, font=font_title, fill=(255, 255, 255))
            draw.text((header_x, header_y + 110), ">> " + concept_txt, font=font_concept, fill=(100, 225, 185))
            draw.line([header_x, header_y + 160, WIDTH - 60, header_y + 160], fill=(45, 60, 90), width=1)

            # 5. TELEPROMPTER KARAOKE CENTRADO Y RESPONSIVE EN LA FRANJA INFERIOR (SIN CAJAS)
            words = text_speech.split()
            tot_words = len(words)
            active_w_idx = int(progress * tot_words)
            active_w_idx = min(tot_words - 1, max(0, active_w_idx))

            chunk_idx = active_w_idx // WORDS_PER_CHUNK
            chunk_start = chunk_idx * WORDS_PER_CHUNK
            chunk_end = min(tot_words, chunk_start + WORDS_PER_CHUNK)
            current_chunk = words[chunk_start:chunk_end]

            cursor_x = 80
            cursor_y = HEIGHT - 270
            line_h = 75
            max_line_w = WIDTH - av_w - 140

            for w_loc, word in enumerate(current_chunk):
                global_idx = chunk_start + w_loc
                word_str = word + " "
                bbox = font_karaoke.getbbox(word_str)
                w_w = bbox[2] - bbox[0]

                if cursor_x + w_w > max_line_w:
                    cursor_x = 80
                    cursor_y += line_h

                # Sombra suave detrás de cada palabra para legibilidad perfecta sobre estrellas
                draw.text((cursor_x + 3, cursor_y + 3), word_str, font=font_karaoke, fill=(0, 0, 0))

                if global_idx == active_w_idx:
                    w_color = (255, 215, 0)   # Oro activo
                elif global_idx < active_w_idx:
                    w_color = (245, 248, 255) # Blanco hablado
                else:
                    w_color = (120, 135, 160) # Futuro suave

                draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
                cursor_x += w_w

            # Barra de progreso inferior en oro
            prog_pct = t / total_duration
            draw.rectangle([0, HEIGHT - 6, int(WIDTH * prog_pct), HEIGHT], fill=(212, 175, 55))

        else:
            draw.text((WIDTH//2 - 300, HEIGHT//2), "OPENCLAW 2026 — SOVEREIGN AI", fill=(148, 163, 184), font=font_title)

        frame_file = frames_dir / f"seamless_{f_idx:06d}.jpg"
        frame.convert("RGB").save(str(frame_file), quality=92)

        if f_idx % 300 == 0:
            print(f"    -> Progreso ({lang}): {f_idx}/{total_frames} frames ({f_idx/total_frames*100:.1f}%)")

    print(f"  [OK] Renderizado completado ({lang}).")
    return frames_dir

def encode_video(lang="es", master_audio=None) -> Path:
    print(f"\n[FASE 4/4] Codificando Video Maestro FastStart 1080p ({lang.upper()})...")
    frames_dir = PROD_DIR / f"frames_v2_{lang}"
    output_mp4 = PROD_DIR / f"PROD_20260824_DEEPMIND_{lang.upper()}_SEAMLESS_V2.0.mp4"

    cmd_encode = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "seamless_%06d.jpg"),
        "-i", str(master_audio),
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
    print(f"  [OK] Video {lang.upper()} compilado en: {output_mp4}")
    return output_mp4

def main():
    print("=" * 75)
    print("  OPENCLAW 2026: SEAMLESS V2.0 (ESPAÑOL & INGLES) — DEEPMIND MASTERPIECE")
    print("=" * 75)

    # 1. Producción en Español
    asyncio.run(synthesize_language_audio("es"))
    master_audio_es, dur_es = assemble_soundtrack("es")
    render_seamless_frames("es", dur_es)
    mp4_es = encode_video("es", master_audio_es)

    # 2. Producción en Inglés
    asyncio.run(synthesize_language_audio("en"))
    master_audio_en, dur_en = assemble_soundtrack("en")
    render_seamless_frames("en", dur_en)
    mp4_en = encode_video("en", master_audio_en)

    print("\n[OK] AMBAS VERSIONES (ES & EN) COMPILADAS EXITOSAMENTE EN V2.0.")

if __name__ == "__main__":
    main()
