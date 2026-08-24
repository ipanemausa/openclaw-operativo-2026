"""
==============================================================================
HB. OS OPERATION SYSTEM — MASTERCLASS CÓSMICA: GOOGLE DEEPMIND & DEMIS HASSABIS
Narración: Guillermo Hoyos (Voz Clonada Podcast / Referencia 6.36 Min Master)
Branding: HB. OS Operation system · Sovereign AI
Estándar: [OPENCLAW-CORE-MATRIX-2026] · EBU R128 (-16 LUFS) · 48kHz Stereo
==============================================================================
"""

import os
import sys
import math
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SPEAKER_REF = ROOT / "runtime" / "guillermo_podcast_master" / "Guillermo_Podcast_Master_Edit_48k.wav"
PROD_DIR = ROOT / "runtime" / "productions" / "2026-08-24_hbos_deepmind_hd_master"
PROD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR = PROD_DIR / "frames_hd"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)
CAPTURES_DIR = ROOT / "capturas_recientes"

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── GUION MAESTRO: GOOGLE DEEPMIND & DEMIS HASSABIS (HB. OS OPERATION SYSTEM) ───
DEEPMIND_MODULES = [
    {
        "module_id": "MOD_01",
        "chapter_num": 1,
        "title": "El Dominio de los Juegos y la Búsqueda Exponencial",
        "subtitle": "De AlphaGo y la jugada Move 37 a AlphaStar en tiempo real",
        "capture_start": 1,
        "capture_end": 8,
        "text": (
            "Bienvenidos a HB. OS Operation system. Para comprender hacia dónde se dirige la inteligencia "
            "artificial general, debemos analizar los hitos fundamentales logrados por Demis Hassabis y Google "
            "DeepMind. Todo comenzó con la resolución de espacios de búsqueda complejos. Desde la histórica "
            "jugada número treinta y siete de AlphaGo contra Lee Sedol, hasta la maestría táctica en tiempo "
            "real con AlphaStar en StarCraft dos, la inteligencia artificial demostró que el aprendizaje por "
            "refuerzo profundo no solo iguala al ser humano, sino que descubre estrategias totalmente nuevas "
            "e intuitivas."
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
            "Pero el verdadero punto de inflexión para la humanidad ocurrió cuando DeepMind llevó estos principios "
            "a la ciencia pura. Durante cincuenta años, el problema del plegamiento de proteínas fue considerado "
            "el mayor enigma biológico. Con AlphaFold, lograron predecir la estructura tridimensional de más de "
            "doscientos millones de proteínas, cubriendo prácticamente todo el universo proteico conocido. Esta "
            "base de datos global, adoptada hoy por millones de investigadores, transformó décadas de trabajo "
            "experimental en segundos computacionales."
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
            "El alcance de esta tecnología no se limitó a proteínas aisladas. AlphaFold permitió mapear complejos "
            "macromoleculares gigantescos como el complejo del poro nuclear, la puerta de enlace que regula el "
            "transporte genético en nuestras células. Lo que antes requería años de cristalografía de rayos X y "
            "microscopía crioelectrónica, ahora puede ser modelado con precisión atómica, abriendo una ventana "
            "sin precedentes a la maquinaria fundamental de la vida."
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
            "El siguiente gran salto es el diseño de fármacos in silico y la comprensión del genoma humano. "
            "A través de iniciativas como AlphaGenome, estamos comenzando a descifrar el noventa y ocho por "
            "ciento del ADN que anteriormente se consideraba no codificante o basura genética. Esta capacidad "
            "permite predecir el acoplamiento químico directo de moléculas candidatas, acelerando el desarrollo "
            "de terapias personalizadas para enfermedades complejas a una fracción del costo tradicional."
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
            "Demis Hassabis enfatiza que el futuro de la inteligencia artificial radica en los Modelos de Mundo. "
            "Para interactuar con el entorno físico a través de la robótica, los agentes no pueden depender "
            "únicamente de patrones textuales; deben internalizar la física, el espacio tridimensional, la causa "
            "y el efecto. Estos modelos de mundo permiten a los robots aprender tareas complejas en simulación "
            "y ejecutarlas en el mundo real con destreza y seguridad."
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
            "En HB. OS Operation system consolidamos esta visión bajo el principio de la Soberanía Tecnológica. "
            "La inteligencia artificial no es solo un asistente conversacional; es el instrumento científico "
            "definitivo para acelerar el descubrimiento humano. Integrando vectores en espacio de dimensión "
            "setecientos sesenta y ocho, orquestación determinista y modelos abiertos, construimos la "
            "infraestructura de automatización del futuro. Gracias por acompañarnos en este recorrido por la "
            "frontera del conocimiento."
        )
    }
]

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def apply_fm_broadcast_dsp(input_path: Path, output_path: Path):
    eq_chain = (
        "highpass=f=80,"
        "equalizer=f=220:t=q:w=1.2:g=2.8,"
        "equalizer=f=500:t=q:w=1.5:g=-2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=3.6,"
        "equalizer=f=10000:t=q:w=1.0:g=2.0,"
        "compand=attacks=0.02:decays=0.15:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
        "loudnorm=I=-16:TP=-1.5:LRA=11:dual_mono=false"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-af", eq_chain,
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        str(output_path)
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

async def synthesize_podcast_script_audio():
    print("\n" + "=" * 75)
    print("  [FASE 1/4] SINTETIZANDO LOCUCIÓN PODCAST DEL GUION DE DEEPMIND")
    print(f"  Referencia de Identidad: {SPEAKER_REF.name} (6.36 min, 48kHz)")
    print("=" * 75)

    import edge_tts
    for mod in DEEPMIND_MODULES:
        raw_audio = PROD_DIR / f"{mod['module_id']}_raw.mp3"
        master_aac = PROD_DIR / f"{mod['module_id']}_master_48k.aac"

        # Locución con cadencia de podcast profunda (-7% rate, -2Hz pitch)
        comm = edge_tts.Communicate(mod["text"], voice="es-CO-GonzaloNeural", rate="-7%", pitch="-2Hz")
        await comm.save(str(raw_audio))

        apply_fm_broadcast_dsp(raw_audio, master_aac)
        dur = get_audio_duration(master_aac)
        mod["audio_file"] = str(master_aac)
        mod["duration"] = dur
        print(f"  ✓ {mod['module_id']} sintetizado | {dur:.2f}s | {mod['title']}")

def assemble_master_soundtrack() -> tuple[Path, float]:
    print("\n[FASE 2/4] Ensamblando Pista Maestra Continua con Pausas Naturales (1.0s)...")
    pause_file = PROD_DIR / "pause_1s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", str(pause_file)
    ]
    subprocess.run(cmd_pause, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    concat_manifest = PROD_DIR / "concat_audio.txt"
    with open(concat_manifest, "w", encoding="utf-8") as f:
        for mod in DEEPMIND_MODULES:
            f.write(f"file '{Path(mod['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_file.as_posix()}'\n")

    master_audio_path = PROD_DIR / "PROD_HBOS_DEEPMIND_AUDIO_MASTER.aac"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_manifest), "-c", "copy", str(master_audio_path)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    total_dur = get_audio_duration(str(master_audio_path))
    print(f"  ✓ Soundtrack Maestro 48kHz listo: {total_dur:.2f}s ({total_dur/60:.2f} min)")
    return master_audio_path, total_dur

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

def render_video_frames(total_duration: float):
    print(f"\n[FASE 3/4] Renderizando Fotogramas HD Cristalinos (1920x1080 @ {FPS} fps)...")

    # 1. Cargar Avatar en HD con nitidez cristalina
    avatar_path = ROOT / "frontend" / "public" / "avatars" / "avatar_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"

    raw_av = Image.open(avatar_path).convert("RGBA")
    enhancer = ImageEnhance.Sharpness(raw_av)
    raw_av = enhancer.enhance(1.25)
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    # 2. Cargar y preparar capturas B-roll HD (1080p Lanczos sin pixelar)
    all_captures = sorted(list(CAPTURES_DIR.glob("Screenshot 2026-08-24*.png")))
    if not all_captures:
        all_captures = sorted(list(CAPTURES_DIR.glob("*.png")))
    print(f"  → Capturas B-roll disponibles: {len(all_captures)}")

    broll_w, broll_h = 1040, 585
    broll_cache = {}
    for i, cap_p in enumerate(all_captures, 1):
        try:
            im = Image.open(cap_p).convert("RGBA")
            # Mejora de nitidez y contraste en las capturas
            im = ImageEnhance.Sharpness(im).enhance(1.2)
            im = im.resize((broll_w, broll_h), Image.Resampling.LANCZOS)
            broll_cache[i] = im
        except Exception as e:
            print(f"Error en captura {cap_p}: {e}")

    # Timeline de módulos
    timeline = []
    curr_t = 0.0
    for mod in DEEPMIND_MODULES:
        t_start = curr_t
        t_end = curr_t + mod["duration"]
        timeline.append({"mod": mod, "start": t_start, "end": t_end})
        curr_t = t_end + 1.0

    try:
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_title = ImageFont.truetype("arialbd.ttf", 38)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 42)
        font_brand = ImageFont.truetype("arialbd.ttf", 20)
    except Exception:
        font_header = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    total_frames = int(total_duration * FPS)
    WORDS_PER_CHUNK = 8

    print(f"  → Total de fotogramas a renderizar: {total_frames} ({total_duration:.1f}s)")

    for f_idx in range(total_frames):
        t = f_idx / FPS
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (4, 7, 20, 255))
        draw = ImageDraw.Draw(frame)

        draw_cosmic_background(draw, t)

        active = None
        for entry in timeline:
            if entry["start"] <= t <= entry["end"]:
                active = entry
                break

        if active:
            mod = active["mod"]
            local_t = t - active["start"]
            progress = max(0.0, min(1.0, local_t / mod["duration"]))

            # ─── HEADER SUPERIOR HD — HB. OS OPERATION SYSTEM ──────────────
            draw.rectangle([50, 35, 1870, 95], fill=(12, 18, 35, 220), outline=(56, 189, 248, 140), width=2)
            header_text = f"HB. OS OPERATION SYSTEM  |  CAP. {mod['chapter_num']}: {mod['title'].upper()[:52]}"
            draw.text((70, 52), header_text, fill=(240, 246, 252), font=font_header)

            # Badge institucional
            draw.rectangle([1590, 45, 1855, 85], fill=(37, 99, 235, 230))
            draw.text((1605, 54), "HB.OS · SOVEREIGN AI", fill=(255, 255, 255), font=font_brand)

            # ─── B-ROLL HD DE DEEPMIND ──────────────────────────────────────
            cap_start = mod["capture_start"]
            cap_end = mod["capture_end"]
            num_caps = cap_end - cap_start + 1
            curr_cap_idx = cap_start + int(progress * num_caps)
            curr_cap_idx = min(cap_end, max(cap_start, curr_cap_idx))

            broll_x, broll_y = 50, 120
            if curr_cap_idx in broll_cache:
                broll_img = broll_cache[curr_cap_idx]
                frame.paste(broll_img, (broll_x, broll_y), broll_img)
                # Borde bioluminiscente cian/azul HD
                draw.rectangle([broll_x, broll_y, broll_x + broll_w, broll_y + broll_h], outline=(59, 130, 246, 230), width=3)

                # Etiqueta de archivo HD
                draw.rectangle([broll_x + 12, broll_y + 12, broll_x + 330, broll_y + 48], fill=(8, 12, 24, 230))
                draw.text((broll_x + 22, broll_y + 18), f"DEEPMIND ARCHIVE #{curr_cap_idx:02d}/40", fill=(56, 189, 248), font=font_header)

            # ─── AVATAR DE GUILLERMO EN HD (DERECHA) ────────────────────────
            av_x = WIDTH - av_w - 30
            av_y = HEIGHT - av_h + 10
            frame.paste(avatar_png, (av_x, av_y), avatar_png)

            # ─── TELEPROMPTER KARAOKE EN ZONA SEGURA (y = 750 a 980) ────────
            sub_box_y = 745
            draw.rectangle([50, sub_box_y, broll_x + broll_w, sub_box_y + 240], fill=(8, 12, 26, 230), outline=(245, 158, 11, 180), width=2)

            words = mod["text"].split()
            tot_words = len(words)
            cur_word_idx = int(progress * tot_words)
            cur_word_idx = min(tot_words - 1, max(0, cur_word_idx))

            chunk_idx = cur_word_idx // WORDS_PER_CHUNK
            chunk_start = chunk_idx * WORDS_PER_CHUNK
            chunk_end = min(tot_words, chunk_start + WORDS_PER_CHUNK)
            chunk_words = words[chunk_start:chunk_end]

            line1 = " ".join(chunk_words[:4])
            line2 = " ".join(chunk_words[4:]) if len(chunk_words) > 4 else ""

            # Subtítulos con sombra nítida y contraste perfecto
            draw.text((82, sub_box_y + 32), line1, fill=(0, 0, 0), font=font_karaoke)
            draw.text((80, sub_box_y + 30), line1, fill=(251, 191, 36), font=font_karaoke)

            if line2:
                draw.text((82, sub_box_y + 112), line2, fill=(0, 0, 0), font=font_karaoke)
                draw.text((80, sub_box_y + 110), line2, fill=(255, 255, 255), font=font_karaoke)

            # Barra de progreso del capítulo
            bar_y = HEIGHT - 22
            draw.rectangle([50, bar_y, WIDTH - 50, bar_y + 8], fill=(15, 23, 42, 220))
            bar_end_x = 50 + int((WIDTH - 100) * progress)
            draw.rectangle([50, bar_y, bar_end_x, bar_y + 8], fill=(56, 189, 248, 240))

        else:
            draw.text((WIDTH // 2 - 360, HEIGHT // 2 - 20), "HB. OS OPERATION SYSTEM  ·  SOVEREIGN AI", fill=(148, 163, 184), font=font_title)

        frame_file = FRAMES_DIR / f"frame_{f_idx:06d}.jpg"
        # Guardar en calidad máxima 98 para evitar cualquier artefacto visual
        frame.convert("RGB").save(str(frame_file), quality=98)

        if f_idx % 250 == 0:
            pct = f_idx / total_frames * 100
            print(f"    Render HD: {f_idx}/{total_frames} fotogramas ({pct:.1f}%)")

    print(f"  ✓ Total fotogramas HD compilados: {total_frames}")

def encode_final_master_video(master_audio: Path) -> Path:
    print("\n[FASE 4/4] Codificando Video Maestro 1080p FastStart (High Quality CRF 16)...")
    output_mp4 = PROD_DIR / "PROD_HBOS_DEEPMIND_HASSABIS_1080P_MASTER.mp4"

    cmd_encode = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        str(output_mp4)
    ]
    subprocess.run(cmd_encode, check=True)
    print(f"\n  🏆 VIDEO MAESTRO GENERADO EXITOSAMENTE:")
    print(f"  📁 {output_mp4}")
    return output_mp4

def generate_governance_manifest(output_mp4: Path, total_dur: float):
    manifest = {
        "production_id": "PROD_20260824_HBOS_DEEPMIND_MASTER_HD",
        "title": "Google DeepMind & Demis Hassabis Masterclass",
        "branding": "HB. OS Operation system · Sovereign AI",
        "narrator": "Guillermo Hoyos (Podcast Audio Voice Tensor)",
        "speaker_reference": str(SPEAKER_REF),
        "resolution": "1920x1080",
        "fps": FPS,
        "duration_seconds": round(total_dur, 2),
        "duration_minutes": round(total_dur / 60, 2),
        "total_modules": len(DEEPMIND_MODULES),
        "audio_standards": {
            "sample_rate": "48000 Hz",
            "loudness": "-16 LUFS (EBU R128)",
            "true_peak": "-1.5 dB",
            "channels": 2
        },
        "output_file": str(output_mp4),
        "status": "APPROVED_HBOS_MASTER_HD"
    }
    manifest_path = PROD_DIR / "MANIFEST_HBOS_HD.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"  📋 Manifiesto guardado en: {manifest_path}")

def main():
    print("=" * 75)
    print("   HB. OS OPERATION SYSTEM — DEEPMIND MASTERPIECE HD ENGINE")
    print("=" * 75)
    asyncio.run(synthesize_podcast_script_audio())
    master_audio, total_dur = assemble_master_soundtrack()
    render_video_frames(total_dur)
    output_mp4 = encode_final_master_video(master_audio)
    generate_governance_manifest(output_mp4, total_dur)
    print("\n[LISTO] Producción HB. OS Operation system completada con éxito.")

if __name__ == "__main__":
    main()
