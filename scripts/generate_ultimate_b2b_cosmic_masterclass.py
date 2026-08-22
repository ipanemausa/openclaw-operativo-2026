"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS DEFINITIVA: ARQUITECTURA SOBERANA B2B & UNIVERSAL
==============================================================================
- Visual: Avatar PNG Transparente Integrado (SIN CÍRCULOS NI CAJAS)
- Fondo: Universo Cósmico en Movimiento Continuo Suave
- Texto: Bloques Cortos de 2 Líneas en Fuente Gigante (48pt-52pt) + Karaoke Oro
- Locución: Voz Colombiana Cálida y Pausada con Ecualización FM Broadcast (-16 LUFS)
- Nombres de Modelos: English Original ("DeepSeek", "Qwen", "Gemini", "Claude", "OpenClaw")
- Pedagogía: Explicación profunda y accesible de cada concepto técnico
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
RUNTIME = ROOT / "runtime" / "masterclass_definitiva_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame

# ─── 10 CAPÍTULOS DE ALTO IMPACTO PEDAGÓGICO Y CIENTÍFICO ────────────────────

DEFINITIVE_MODULES = [
    {
        "chapter_num": "01",
        "category": "HISTORIA Y VISIÓN",
        "title": "La Revolución de la Inteligencia Artificial Soberana",
        "concept": "Arquitectura Universal a Costo Cero para Latinoamérica",
        "text": "Hola a todos, les habla Guillermo. Les doy una bienvenida muy especial a esta sesión técnica. Durante años, a las empresas y a los estudiantes les dijeron que para usar inteligencia artificial debían pagar costosas licencias mensuales en dólares. Hoy les demostramos que es posible construir una plataforma de alto nivel, con modelos abiertos, gobernanza de datos y costo cero de licencias.",
        "en_sub": "Welcome. We demonstrate an enterprise-grade Sovereign AI platform built on open models at zero licensing fees."
    },
    {
        "chapter_num": "02",
        "category": "SÍNTESIS DIALÉCTICA",
        "title": "Jensen Huang y Dario Amodei: La Fuerza Resultante",
        "concept": "Cómputo Masivo Acelerado + Gobernanza y Contención de Riesgos",
        "text": "En el panorama mundial de la inteligencia artificial conviven dos visiones poderosas. Por un lado, Jensen Huang de NVIDIA impulsa el escalamiento masivo del cómputo. Por otro lado, Dario Amodei de Anthropic exige seguridad rigurosa y control de riesgos. Nuestra arquitectura une ambas fuerzas: aprovechamos el cómputo distribuido sin límites, protegiendo al cien por ciento la privacidad de nuestros datos.",
        "en_sub": "We synthesize NVIDIA's compute scaling with Anthropic's safety guardrails to protect proprietary enterprise data."
    },
    {
        "chapter_num": "03",
        "category": "ENRUTADOR HÍBRIDO",
        "title": "El Puente Global: Modelos de Oriente y Occidente",
        "concept": "Orquestación Multi-Modelo: DeepSeek, Qwen, Gemini y Claude",
        "text": "En lugar de depender de un solo proveedor, implementamos un Router Multi-Modelo inteligente. Para análisis de negocio y visión estratégica utilizamos Claude y Gemini. Pero para lógica matemática profunda y generación de código determinista, conectamos DeepSeek y Qwen de Alibaba. El sistema conmuta entre ellos automáticamente en tres segundos.",
        "en_sub": "Our multi-model router combines western strategic analysis with DeepSeek and Qwen open-weight logic engines in 3 seconds."
    },
    {
        "chapter_num": "04",
        "category": "MEMORIA CORPORATIVA",
        "title": "Bases de Datos Vectoriales y Retrieval-Augmented Generation",
        "concept": "Indexación Privada en Qdrant para Cero Alucinaciones",
        "text": "El mayor temor de un empresario es que la inteligencia artificial invente información. Para resolverlo usamos la técnica RAG con bases de datos vectoriales Qdrant. Todo el catálogo, inventario y reglas contables se almacenan de forma privada. Cuando un usuario consulta, el sistema busca en los documentos verificados y responde con la verdad exacta.",
        "en_sub": "Private Qdrant vector databases anchor LLM responses directly to verified business documents, eliminating hallucinations."
    },
    {
        "chapter_num": "05",
        "category": "RIGOR MATEMÁTICO",
        "title": "Gobernanza Vectorial en Espacio R Setecientos Sesenta y Ocho",
        "concept": "Métrica Euclidiana y Filtro de Similitud Coseno Mayor a 0.82",
        "text": "Para superar el escrutinio técnico de universidades como EAFIT y centros como Ruta N, proyectamos las consultas en un espacio vectorial de setecientas sesenta y ocho dimensiones. Aplicamos un filtro de similitud coseno estricto de cero punto ochenta y dos. Si un dato no alcanza esta certeza matemática, es descartado de inmediato.",
        "en_sub": "Mathematical governance projects queries into R768 space, enforcing a strict 0.82 cosine similarity threshold."
    },
    {
        "chapter_num": "06",
        "category": "SEGURIDAD INTEGRAL",
        "title": "Sandbox Guardrail: Protección de Credenciales y Auditoría",
        "concept": "Filtro de Datos Sensibles en Tiempo Real y Registro JSON Inmutable",
        "text": "La soberanía de datos exige seguridad perimetral. Cada solicitud atraviesa un Sandbox Guardrail que inspecciona el texto antes de salir a la red. Si detecta por error una API Key, una tarjeta o una contraseña, bloquea la transacción al instante. Al mismo tiempo, registra una bitácora JSON inmutable para control fiscal y regulatorio.",
        "en_sub": "Our Sandbox Guardrail inspects all outbound payloads, intercepting credentials and logging immutable JSON audit trails."
    },
    {
        "chapter_num": "07",
        "category": "ORQUESTACIÓN ASÍNCRONA",
        "title": "Teoría de Colas y Método de la Ruta Crítica",
        "concept": "Grafos Dirigidos Acíclicos (DAG) con Latencia Medida de 3.3 Segundos",
        "text": "Para que un computador convencional funcione como un supercomputador, desacoplamos la coordinación del cómputo pesado. Modelamos las tareas como un grafo dirigido acíclico en la Ruta Crítica. Nuestra máquina local sólo actúa como director de orquesta, logrando tiempos de respuesta de tres segundos y medio sin saturar los recursos locales.",
        "en_sub": "Queueing Theory and Critical Path Methods decouple local lightweight coordination from cloud heavy compute."
    },
    {
        "chapter_num": "08",
        "category": "FÁBRICA AUDIOVISUAL",
        "title": "Producción Broadcast 48kHz y Teleprompter Dinámico",
        "concept": "Normalización Internacional EBU R128 (-16 LUFS) y Video FastStart",
        "text": "El conocimiento debe comunicarse con la más alta calidad. Nuestra fábrica audiovisual genera locución estéreo a cuarenta y ocho kilohercios bajo la norma internacional EBU R ciento veintiocho a menos dieciséis LUFS. El teleprompter resalta cada palabra en tiempo real, permitiendo una reproducción fluida en YouTube con cero almacenamiento previo.",
        "en_sub": "Enterprise knowledge transforms into broadcast-quality 48kHz stereo media with word-by-word real-time teleprompter sync."
    },
    {
        "chapter_num": "09",
        "category": "GEOPOLÍTICA REGIONAL",
        "title": "Colombia: Nodo Estratégico de Innovación en América Latina",
        "concept": "Alianza con MinTIC, Alcaldías, Gobernaciones y Universidades",
        "text": "Colombia cuenta con una ubicación geográfica bioceánica única entre el Pacífico y el Atlántico. Nuestro país tiene el talento para liderar la adopción de inteligencia artificial soberana en la región. Esta plataforma está lista para articularse con MinTIC, secretarías de desarrollo y universidades para capacitar a miles de jóvenes y fortalecer a nuestras empresas.",
        "en_sub": "Colombia is strategically positioned to lead Latin America's sovereign AI ecosystem with MinTIC and top universities."
    },
    {
        "chapter_num": "10",
        "category": "LLAMADO A LA ACCIÓN",
        "title": "Construyendo el Futuro Productivo con Hechos Verificables",
        "concept": "Neuroplasticidad, Disciplina y Soberanía Tecnológica",
        "text": "Amigos, estudiantes y empresarios: la inteligencia artificial se conquista practicando y construyendo. La neurociencia nos enseña que el aprendizaje enfocado expande nuestra capacidad de raciocinio y crea nuevas oportunidades de desarrollo. Lo que han visto hoy es código real, soberano y verificado. Los invito a dar el salto. Bienvenidos a OpenClaw dos mil veintiséis.",
        "en_sub": "AI is mastered through disciplined practice. We invite students and enterprises to lead this verifiable digital sovereignty journey."
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

async def synthesize_colombian_speech():
    print("\n[FASE 1/4] Sintetizando 10 módulos con Voz Colombiana Cálida (es-CO-GonzaloNeural)...")
    for idx, item in enumerate(DEFINITIVE_MODULES):
        raw_mp3 = RUNTIME / f"def_raw_{idx}.mp3"
        master_aac = RUNTIME / f"def_master_{idx}.aac"

        # Locución colombiana pausada, amigable y respetuosa (-6% rate, -2Hz pitch)
        comm = edge_tts.Communicate(item["text"], voice="es-CO-GonzaloNeural", rate="-6%", pitch="-2Hz")
        await comm.save(str(raw_mp3))

        # Cadena de Masterización Acústica FM Broadcast
        eq_chain = (
            "highpass=f=80,"
            "equalizer=f=220:t=q:w=1.2:g=2.5,"
            "equalizer=f=500:t=q:w=1.5:g=-2.0,"
            "equalizer=f=3500:t=q:w=1.0:g=3.5,"
            "equalizer=f=10000:t=q:w=1.0:g=2.0,"
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
        print(f"  [OK] Cap {item['chapter_num']}: {dur:.2f}s | '{item['title']}'")

def render_definitive_masterclass():
    # 1. Sintetizar audios con voz colombiana cálida
    asyncio.run(synthesize_colombian_speech())

    # 2. Mezclar pista maestra con pausas de respiración (1.2s entre capítulos)
    print("\n[FASE 2/4] Mezclando pista de audio maestra con pausas naturales (1.2s)...")
    pause_aac = RUNTIME / "pause_12s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.2", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    concat_txt = RUNTIME / "concat_def.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in DEFINITIVE_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")

    master_audio = RUNTIME / "master_audio_definitive_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f}s ({total_duration/60:.2f} minutos)")

    # 3. Cargar Avatar PNG 100% Transparente Integrado (SIN CÍRCULOS NI FOTOS CUADRADAS)
    print("\n[FASE 3/4] Renderizando fotogramas 1080p con Universo Dinámico y Texto Flotante Grande...")
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    
    # Escalar avatar a 860px de alto (proporción natural en pantalla)
    av_h = 860
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"  -> Avatar transparente cargado: {av_w}x{av_h} px")

    # Fuentes Tipográficas Grandes y Descansadas
    try:
        font_chapter = ImageFont.truetype("arialbd.ttf", 26)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arialbd.ttf", 24)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 48)  # Fuente grande de lectura descansada
        font_en = ImageFont.truetype("ariali.ttf", 24)
        font_speaker = ImageFont.truetype("arialbd.ttf", 26)
        font_role = ImageFont.truetype("arial.ttf", 20)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_chapter = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_speaker = ImageFont.load_default()
        font_role = ImageFont.load_default()
        font_top = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in DEFINITIVE_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.2

    frames_dir = RUNTIME / "temp_def_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"  -> Renderizando {total_frames} fotogramas Full HD a {FPS} FPS...")

    # Pre-calcular bloques de palabras para lectura descansada (máximo 12 palabras por pantalla)
    WORDS_PER_CHUNK = 10

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
        dur_mod = max(0.1, active_mod["end"] - active_mod["start"])

        # ─── 1. FONDO CÓSMICO DEL UNIVERSO EN MOVIMIENTO SUAVE ───
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior de Control Cósmica
        draw.rectangle([0, 0, WIDTH, 80], fill=(10, 14, 25))
        draw.line([0, 80, WIDTH, 80], fill=(212, 175, 55), width=2)
        draw.text((60, 26), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 26), "·   MASTERCLASS MAGNA DE INTELIGENCIA ARTIFICIAL SOBERANA", font=font_top, fill=(195, 205, 225))
        draw.text((1580, 26), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR PNG TRANSPARENTE EN ESCENA COMPLETA (SIN MARCOS) ───
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 50
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Lower-Third de Identificación Flotante Elegante
        id_x = 70
        id_y = 110
        draw.rounded_rectangle([id_x, id_y, id_x + 460, id_y + 85], radius=10, fill=(14, 18, 30), outline=(40, 55, 80), width=1)
        draw.text((id_x + 22, id_y + 14), "GUILLERMO · OPENCLAW", font=font_speaker, fill=(255, 255, 255))
        draw.text((id_x + 22, id_y + 48), "Arquitectura Soberana B2B / HB Jewelry", font=font_role, fill=(212, 175, 55))
        draw.ellipse([id_x + 420, id_y + 22, id_x + 438, id_y + 40], fill=(50, 220, 100))

        # ─── 3. LADO DERECHO: TEXTO FLOTANTE DE GRAN FORMATO Y LECTURA DESCANSADA ───
        content_x = 640
        content_y = 110
        content_w = 1220

        # Badge del Capítulo y Categoría
        draw.rounded_rectangle([content_x, content_y, content_x + 190, content_y + 42], radius=6, fill=(212, 175, 55))
        draw.text((content_x + 18, content_y + 8), f"CAPÍTULO {item['chapter_num']}", font=font_chapter, fill=(10, 14, 25))

        draw.rounded_rectangle([content_x + 205, content_y, content_x + 590, content_y + 42], radius=6, fill=(22, 32, 52))
        draw.text((content_x + 220, content_y + 8), item["category"], font=font_chapter, fill=(212, 175, 55))

        # Título Grande del Capítulo
        draw.text((content_x, content_y + 60), item["title"], font=font_title, fill=(255, 255, 255))

        # Concepto Clave Subtitulado
        draw.text((content_x, content_y + 125), "⚡ " + item["concept"], font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 170, content_x + content_w, content_y + 170], fill=(45, 60, 90), width=1)

        # ─── TELEPROMPTER EN BLOQUES CORTOS Y FUENTE GIGANTE (48PT) ───
        words = item["text"].split()
        total_words = len(words)
        active_word_global_idx = int((t_rel / dur_mod) * total_words) if dur_mod > 0 else 0

        # Determinar qué bloque de palabras mostrar en este segundo
        chunk_idx = active_word_global_idx // WORDS_PER_CHUNK
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(total_words, chunk_start + WORDS_PER_CHUNK)
        current_chunk_words = words[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = content_y + 230
        line_height = 70
        max_line_w = content_w - 40

        # Fondo sutil de respiración detrás del texto activo
        draw.rounded_rectangle([content_x - 20, cursor_y - 20, content_x + content_w, cursor_y + 360], radius=16, fill=(12, 16, 28), outline=(32, 44, 68), width=1)

        for w_local_idx, word in enumerate(current_chunk_words):
            global_w_idx = chunk_start + w_local_idx
            word_str = word + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            # Color: Oro brillante para palabra hablada en este instante, Blanco para ya habladas, Gris azulado para futuras
            if global_w_idx == active_word_global_idx:
                w_color = (255, 215, 0)   # Oro brillante
            elif global_w_idx < active_word_global_idx:
                w_color = (245, 248, 255) # Blanco nítido
            else:
                w_color = (100, 115, 140) # Futuro

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # Subtítulo en Inglés en la Base Flotante
        draw.line([content_x, HEIGHT - 130, content_x + content_w, HEIGHT - 130], fill=(45, 60, 90), width=1)
        draw.text((content_x, HEIGHT - 100), "EN: " + item["en_sub"], font=font_en, fill=(160, 190, 230))

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 8, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"def_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 600 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n[FASE 4/4] Codificando Masterclass Definitiva 1080p con FFmpeg FastStart...")
    final_output = RUNTIME / "OpenClaw_Masterclass_Definitiva_B2B_1080p.mp4"

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "def_%06d.jpg"),
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
    print("  🏆 MASTERCLASS DEFINITIVA B2B GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print("  Visual:   Avatar PNG Integrado + Universo Cósmico + Letra Gigante 48pt")
    print("  Voz:      Locución Colombiana Cálida y Pausada con Ecualización FM")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

if __name__ == "__main__":
    render_definitive_masterclass()
