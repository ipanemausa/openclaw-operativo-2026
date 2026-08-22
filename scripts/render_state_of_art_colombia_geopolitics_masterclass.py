"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS MAGNA GEOPOLÍTICA & IA SOBERANA (ESTADO DEL ARTE)
==============================================================================
- Guion: Claro, directo, pedagógico (Estilo Huang / Amodei)
- Geopolítica: Posición bioceánica de Colombia + Ventaja comparativa de acceso abierto (Oriente y Occidente)
- Sincronización: 100% Determinista Palabra por Palabra mediante marcas temporales de Whisper
- Visual: Seamless Total (Sin cajas ni cortes) + Universo en Movimiento + Avatar PNG Transparente
- Tipografía: Títulos cinematográficos de alto impacto en Oro + Letra Gigante 54pt con sombra
- Nombres: English Original ("DeepSeek", "Qwen", "Gemini", "Claude", "OpenClaw", "Qdrant")
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
import whisper

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_geopolitica_colombia_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame

# ─── 8 CAPÍTULOS DE ALTO VALOR ESTRATÉGICO Y GEOPOLÍTICO ─────────────────────

GEOPOLITICAL_MODULES = [
    {
        "num": "01",
        "badge": "VISIÓN ESTRATÉGICA",
        "title": "La Verdadera Soberanía en Inteligencia Artificial",
        "concept": "Acceso Universal sin Peajes ni Licencias Millonarias",
        "text": "Hola a todos, les habla Guillermo. Bienvenidos a OpenClaw. Durante años, a las empresas y a los jóvenes les hicieron creer que para innovar en inteligencia artificial se necesitaban millones de dólares en licencias. Hoy demostramos que con rigor, código abierto y tecnología soberana, cualquier persona o empresa puede competir al más alto nivel sin pagar peajes extranjeros.",
        "en_sub": "Welcome. We prove that enterprise-grade AI innovation does not require millions in SaaS fees. Sovereignty is open to everyone."
    },
    {
        "num": "02",
        "badge": "SÍNTESIS HUANG-AMODEI",
        "title": "La Fuerza de Escalar Cómputo con Seguridad",
        "concept": "Uniendo la Potencia de NVIDIA con la Protección de Anthropic",
        "text": "Cuando escuchamos a Jensen Huang y a Dario Amodei, aprendemos algo fundamental: Huang nos enseña que el cómputo debe escalar sin límites para resolver problemas difíciles, mientras Amodei nos recuerda que la seguridad y el control de los datos son innegociables. Nosotros unimos ambas visiones: aceleramos el procesamiento pero manteniendo nuestros datos cien por ciento protegidos.",
        "en_sub": "We combine Jensen Huang's compute scaling with Dario Amodei's safety guardrails to ensure full proprietary data protection."
    },
    {
        "num": "03",
        "badge": "VENTAJA COMPARATIVA",
        "title": "El Puente Global: Lo Mejor de Oriente y Occidente",
        "concept": "Libertad de Elegir los Mejores Modelos del Mundo sin Bloqueos",
        "text": "Aquí existe una ventaja estratégica determinante: en China tienen restricciones para acceder a modelos americanos, y en Estados Unidos hay barreras crecientes contra los modelos chinos. En Colombia y Latinoamérica tenemos la libertad de usar lo mejor de ambos mundos: combinamos Claude y Gemini para estrategia, con DeepSeek y Qwen de Alibaba para lógica y código a costo cero.",
        "en_sub": "Latin America holds a unique advantage: unrestricted access to both Western models and Chinese open-weight engines like DeepSeek and Qwen."
    },
    {
        "num": "04",
        "badge": "DATOS REALES",
        "title": "Memoria Corporativa y Cero Alucinaciones",
        "concept": "Bases de Datos Vectoriales Qdrant con Búsqueda Matemática",
        "text": "El secreto para que la inteligencia artificial no invente datos es conectarla a la memoria de la empresa. Con bases de datos vectoriales privadas como Qdrant, indexamos manuales, inventarios y políticas financieras. Cuando alguien pregunta, el sistema responde únicamente con los hechos verificados de nuestros documentos, garantizando total precisión.",
        "en_sub": "Private Qdrant vector databases anchor every answer directly to verified enterprise records, eliminating hallucinations."
    },
    {
        "num": "05",
        "badge": "SEGURIDAD PERIMETRAL",
        "title": "Sandbox y Protección de Secretos Comerciales",
        "concept": "Filtrado en Tiempo Real de Claves y Registro Inmutable",
        "text": "Para operar con tranquilidad, construimos un Sandbox Guardrail que actúa como un filtro de seguridad en cada llamada. Si alguien introduce por error una contraseña, una tarjeta o una clave privada, el sistema la bloquea en milisegundos antes de que salga a la red, y deja un registro transparente para control legal y contable.",
        "en_sub": "Our Sandbox Guardrail inspects all outbound payloads, intercepting credentials and logging immutable audit trails."
    },
    {
        "num": "06",
        "badge": "GEOPOLÍTICA COLOMBIA",
        "title": "Colombia: Nodo Bioceánico y Capital del Talento",
        "concept": "Posición Estratégica, Dos Océanos y Receptividad Tecnológica",
        "text": "Colombia tiene una posición geográfica privilegiada: es la puerta de entrada a Suramérica, tiene costas en el Pacífico y el Atlántico, y cercanía directa con Norteamérica. Pero lo más valioso es que nuestra gente tiene un interés y una velocidad de adopción de la inteligencia artificial superior a la de muchos países desarrollados. El momento de liderar es ahora.",
        "en_sub": "Colombia's bioceanic location and high technological adoption speed make it the natural AI innovation hub for Latin America."
    },
    {
        "num": "07",
        "badge": "ALIANZA PÚBLICO-PRIVADA",
        "title": "Ecosistema Nacional con MinTIC y Universidades",
        "concept": "Democratización para Estudiantes, PYMEs y Grandes Industrias",
        "text": "Esta plataforma está diseñada para articularse con MinTIC, Ruta N, EAFIT, alcaldías y gobernaciones. No venimos a pedir presupuestos para comprar software cerrado; venimos a transferir una metodología probada que permite capacitar a miles de jóvenes y volver más productivas a nuestras microempresas y grandes corporaciones.",
        "en_sub": "Designed for partnerships with MinTIC and top universities to empower youth and upgrade regional enterprise productivity."
    },
    {
        "num": "08",
        "badge": "LLAMADO A LA ACCIÓN",
        "title": "Construyendo el Futuro con Hechos y sin Humo",
        "concept": "Disciplina, Aprendizaje Continuo y Soberanía Digital",
        "text": "La inteligencia artificial no es magia; es disciplina, práctica y arquitectura sólida. Cuando aprendemos con constancia, nuestro entendimiento se expande y alcanzamos la independencia tecnológica. Todo lo que ven aquí es código real y operativo. Los invito a construir con nosotros. Bienvenidos a OpenClaw dos mil veintiséis.",
        "en_sub": "AI mastery requires disciplined practice. We invite you to build with verifiable facts. Welcome to OpenClaw 2026."
    }
]

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_all_geopolitical_audios():
    """Sintetiza los 8 módulos con voz madura, autoritaria y cálida con ecualización de locución FM."""
    print("\n[FASE 1/5] Sintetizando locuciones vocales con ecualización de estudio FM...")
    for idx, item in enumerate(GEOPOLITICAL_MODULES):
        raw_mp3 = RUNTIME / f"geo_raw_{idx}.mp3"
        master_aac = RUNTIME / f"geo_master_{idx}.aac"

        # Locución madura, pausada y entusiasta (-6% rate, -2Hz pitch)
        comm = edge_tts.Communicate(item["text"], voice="es-CO-GonzaloNeural", rate="-6%", pitch="-2Hz")
        await comm.save(str(raw_mp3))

        # Cadena de Ecualización Paramétrica extraída de la voz de Guillermo en TikTok
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
        item["audio_file"] = str(master_aac)
        item["duration"] = dur
        print(f"  [OK] Módulo {item['num']}: {dur:.2f}s | '{item['title']}'")

def extract_whisper_word_timestamps(whisper_model):
    """Extrae las marcas de tiempo exactas palabra por palabra usando Whisper para sincronización 100% precisa."""
    print("\n[FASE 2/5] Extrayendo marcas de tiempo palabra por palabra con Whisper (Precisión al Milisegundo)...")
    for idx, item in enumerate(GEOPOLITICAL_MODULES):
        res = whisper_model.transcribe(item["audio_file"], language="es", word_timestamps=True)
        words_timed = []
        for segment in res["segments"]:
            for w in segment.get("words", []):
                w_text = w["word"].strip()
                if w_text:
                    words_timed.append({
                        "word": w_text,
                        "start": float(w["start"]),
                        "end": float(w["end"])
                    })
        item["words_timed"] = words_timed
        print(f"  [OK] Módulo {item['num']}: {len(words_timed)} palabras sincronizadas exactamente.")

def render_geopolitical_masterpiece():
    print("=" * 60)
    print("  🌌 OPENCLAW MASTERCLASS GEOPOLÍTICA & SOBERANÍA (1080P)")
    print("=" * 60)

    # 1. Sintetizar audios
    asyncio.run(synthesize_all_geopolitical_audios())

    # 2. Extraer marcas de tiempo exactas con Whisper
    whisper_model = whisper.load_model("base")
    extract_whisper_word_timestamps(whisper_model)

    # 3. Mezclar pista de audio continua con pausas de 1.2s entre módulos
    print("\n[FASE 3/5] Ensamblando pista de audio continua con pausas de respiración...")
    pause_aac = RUNTIME / "pause_12s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.2", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    concat_txt = RUNTIME / "concat_geo.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in GEOPOLITICAL_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")

    master_audio = RUNTIME / "master_audio_geopolitical_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f}s ({total_duration/60:.2f} minutos)")

    # 4. Cargar Avatar PNG Transparente
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    
    # Escalar avatar a 880px de alto
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"  -> Avatar transparente integrado: {av_w}x{av_h} px")

    # Fuentes
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 48)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 54)  # Letra gigante descansada
        font_en = ImageFont.truetype("ariali.ttf", 24)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_top = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in GEOPOLITICAL_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.2

    frames_dir = RUNTIME / "temp_geo_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 4/5] Renderizando {total_frames} fotogramas Full HD sin cajas con sincronización exacta...")

    WORDS_PER_CHUNK = 8  # 8 palabras por pantalla para máxima comodidad de lectura

    for f_idx in range(total_frames):
        t = f_idx / FPS

        active_mod = None
        for entry in timeline:
            if entry["start"] <= t <= entry["end"]:
                active_mod = entry
                break
        if not active_mod:
            active_mod = timeline[-1]

        item = active_mod["item"]
        t_rel = max(0.0, t - active_mod["start"])
        words_timed = item.get("words_timed", [])

        # ─── 1. FONDO CÓSMICO DEL UNIVERSO EN MOVIMIENTO FLUIDO ───
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior Minimalista Flotante
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 24), "·   MASTERCLASS: GEOPOLÍTICA REGIONAL & IA SOBERANA", font=font_top, fill=(190, 200, 220))
        draw.text((1580, 24), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR PNG TRANSPARENTE INTEGRADO (SIN MARCOS) ───
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Identificación Flotante Limpia
        draw.text((80, 95), "GUILLERMO · OPENCLAW", font=font_badge, fill=(255, 255, 255))
        draw.text((80, 125), "Arquitectura Soberana B2B / HB Jewelry", font=font_concept, fill=(212, 175, 55))

        # ─── 3. LADO DERECHO: TEXTO FLOTANTE DIRECTAMENTE SOBRE EL UNIVERSO (SIN CAJAS) ───
        content_x = 640
        content_y = 100
        content_w = 1220

        # Badge del Capítulo
        draw.text((content_x, content_y), f"MÓDULO {item['num']} · {item['badge']}", font=font_badge, fill=(212, 175, 55))

        # Título Grande Cinematográfico
        draw.text((content_x, content_y + 45), item["title"], font=font_title, fill=(255, 255, 255))

        # Concepto Clave
        draw.text((content_x, content_y + 115), "⚡ " + item["concept"], font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 160, content_x + content_w, content_y + 160], fill=(45, 60, 90), width=1)

        # ─── TELEPROMPTER KARAOKE CON TIMESTAMPS EXACTOS DE WHISPER ───
        # Encontrar palabra activa exacta según t_rel
        active_w_idx = 0
        for w_i, w_info in enumerate(words_timed):
            if w_info["start"] <= t_rel <= w_info["end"]:
                active_w_idx = w_i
                break
            elif t_rel > w_info["end"]:
                active_w_idx = w_i + 1

        total_words = len(words_timed)
        chunk_idx = active_w_idx // WORDS_PER_CHUNK
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(total_words, chunk_start + WORDS_PER_CHUNK)
        current_chunk = words_timed[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = content_y + 240
        line_height = 80
        max_line_w = content_w - 40

        for w_local_idx, w_data in enumerate(current_chunk):
            global_idx = chunk_start + w_local_idx
            word_str = w_data["word"] + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            # Sombra suave negra para legibilidad perfecta sobre el cosmos
            draw.text((cursor_x + 3, cursor_y + 3), word_str, font=font_karaoke, fill=(0, 0, 0))

            # Color: Oro Brillante si está siendo hablada, Blanco si ya fue dicha, Gris azulado para futuras
            if global_idx == active_w_idx:
                w_color = (255, 215, 0)   # Oro Brillante
            elif global_idx < active_w_idx:
                w_color = (245, 248, 255) # Blanco Puro
            else:
                w_color = (110, 125, 150) # Futuro

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # Subtítulo en Inglés Flotante en la Base
        draw.line([content_x, HEIGHT - 120, content_x + content_w, HEIGHT - 120], fill=(45, 60, 90), width=1)
        draw.text((content_x + 2, HEIGHT - 90 + 2), "EN: " + item["en_sub"], font=font_en, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 90), "EN: " + item["en_sub"], font=font_en, fill=(160, 190, 230))

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"geo_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 500 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 5. Codificación Final en MP4 FastStart 1080p
    print("\n[FASE 5/5] Codificando Masterclass Geopolítica 1080p con FFmpeg FastStart...")
    final_output = RUNTIME / "OpenClaw_Masterclass_Geopolitica_1080p_FastStart.mp4"

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "geo_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_output)
    ]
    subprocess.run(cmd_render, check=True)

    size_mb = final_output.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print("  🏆 MASTERCLASS GEOPOLÍTICA GENERADA CON ÉXITO")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print("  Sync:     100% Sincronización Palabra por Palabra con Whisper")
    print("  Diseño:   Seamless Total + Universo Cósmico + Letra 54pt")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

if __name__ == "__main__":
    render_geopolitical_masterpiece()
