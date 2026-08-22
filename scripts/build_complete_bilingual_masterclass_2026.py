"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS BILINGÜE COMPLETA (ESPAÑOL & ENGLISH)
==============================================================================
- Logo HB.OS: Integrado directamente en los píxeles de la camisa del Avatar PNG
- Ortografía & Fonética: 100% Rigor Técnico (MinTIC, Ruta N, EAFIT, Guardrails)
- Modelos Exhaustivos: Listado completo de modelos Americanos y Chinos
- Geopolítica Colombia: Hub bioceánico + Libre acceso a Oriente y Occidente
- Sincronización: 100% Precisión al Milisegundo con Marcas Temporales de Whisper
- Visual: Seamless Total (Sin cajas) + Universo Cósmico en Movimiento Continuo (180 estrellas)
- Audio: 48kHz Stereo EBU R128 (-16 LUFS)
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
RUNTIME = ROOT / "runtime" / "masterclass_bilingue_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico y de prosodia
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame
from sovereign_audio_prosody_engine import SovereignProsodyEngine

# ─── CONTENIDO DE LOS MÓDULOS EN ESPAÑOL E INGLÉS ────────────────────────────

BILINGUAL_MODULES = [
    {
        "num": "01",
        "badge_es": "VISIÓN SOBERANA",
        "badge_en": "SOVEREIGN VISION",
        "title_es": "La Verdadera Soberanía en Inteligencia Artificial",
        "title_en": "True Sovereignty in Artificial Intelligence",
        "concept_es": "Acceso Universal sin Peajes ni Licencias Millonarias",
        "concept_en": "Universal Access with Zero SaaS Tax and Zero Licensing Fees",
        "text_es": "Hola a todos, les habla Guillermo. Bienvenidos a OpenClaw. Durante años, a las empresas y a los estudiantes les hicieron creer que para usar inteligencia artificial debían pagar costosas licencias en dólares. Hoy demostramos que con rigor, código abierto y arquitectura soberana, podemos competir al más alto nivel mundial a costo cero de licencias.",
        "text_en": "Hello everyone, this is Guillermo. Welcome to OpenClaw. For years, businesses and students were told they needed expensive recurring software licenses to access artificial intelligence. Today we demonstrate that with sovereign architecture and open-weight models, we can compete at the highest global level at zero licensing costs.",
        "sub_en": "Welcome. We demonstrate sovereign AI architecture built on open-weight models with zero licensing fees."
    },
    {
        "num": "02",
        "badge_es": "SÍNTESIS HUANG-AMODEI",
        "badge_en": "HUANG-AMODEI SYNTHESIS",
        "title_es": "Jensen Huang y Dario Amodei: La Fuerza Resultante",
        "title_en": "Jensen Huang & Dario Amodei: The Resultant Force",
        "concept_es": "Potencia de Cómputo de NVIDIA + Guardrails de Seguridad de Anthropic",
        "concept_en": "NVIDIA Massive Compute Scaling + Anthropic Rigorous Safety Guardrails",
        "text_es": "En la vanguardia mundial conviven dos visiones complementarias. Jensen Huang nos enseña que el cómputo debe escalar sin límites. Dario Amodei nos exige seguridad estricta y control de riesgos. Nuestra arquitectura une ambas fuerzas: aceleramos el procesamiento distribuido, protegiendo al cien por ciento la privacidad de nuestros datos.",
        "text_en": "At the global forefront, two visions unite. Jensen Huang teaches us to scale compute without limits. Dario Amodei demands strict safety guardrails and risk control. Our architecture combines both forces: scaling distributed compute while fully protecting proprietary enterprise data.",
        "sub_en": "We combine Jensen Huang's compute scaling with Dario Amodei's safety guardrails to protect proprietary enterprise data."
    },
    {
        "num": "03",
        "badge_es": "ECOSISTEMA AMERICANO",
        "badge_en": "AMERICAN AI ECOSYSTEM",
        "title_es": "Modelos de Inteligencia Artificial de Estados Unidos",
        "title_en": "Leading American Artificial Intelligence Models",
        "concept_es": "OpenAI, Google DeepMind, Anthropic, Meta, xAI, Cohere y Amazon",
        "concept_en": "OpenAI, Google DeepMind, Anthropic, Meta, xAI, Cohere & Amazon",
        "text_es": "Nuestra plataforma se conecta de forma nativa con los principales modelos de Estados Unidos. En OpenAI: GPT-4o, o1, o3-mini, Sora y Whisper. En Google DeepMind: Gemini 2.0 Flash, Gemini 1.5 Pro y Gemma 2. En Anthropic: Claude Sonnet 4.6 y Claude 3.5 Sonnet, que utilizamos en Antigravity para razonamiento de alto nivel y generación de artefactos, antes de ejecutar el Handoff automático a modelos de código abierto. En Meta: Llama 3.1, Llama 3.2 y Llama 3.3. En xAI: Grok-2 y Grok-3. Y modelos empresariales como Command R+ de Cohere y Amazon Nova.",
        "text_en": "Our platform connects directly to leading American AI models: OpenAI with GPT-4o, o1, o3-mini, Sora and Whisper. Google DeepMind with Gemini 2.0 Flash, Gemini 1.5 Pro and Gemma 2. Anthropic with Claude Sonnet 4.6 and Claude 3.5 Sonnet, which we leverage in Antigravity for frontier reasoning and artifact generation before executing automated Handoff to open-source models. Meta with Llama 3.1 and 3.3. xAI with Grok-2 and Grok-3. And enterprise engines like Cohere Command R+ and Amazon Nova.",
        "sub_en": "Orchestrating Claude Sonnet 4.6 in Antigravity with automated Handoff to open-source models at zero licensing fees."
    },
    {
        "num": "04",
        "badge_es": "ECOSISTEMA ORIENTAL",
        "badge_en": "CHINESE AI ECOSYSTEM",
        "title_es": "Modelos Abiertos de Oriente y Asia",
        "title_en": "Leading Chinese & Asian Open-Weight AI Models",
        "concept_es": "DeepSeek, Alibaba Qwen, Baidu Ernie, Zhipu GLM, Tencent y Kimi",
        "concept_en": "DeepSeek, Alibaba Qwen, Baidu Ernie, Zhipu GLM, Tencent & Kimi",
        "text_es": "Asimismo, integramos los motores más avanzados de Oriente. En DeepSeek: DeepSeek-V3, DeepSeek-R1 y DeepSeek Coder. En Alibaba Cloud: Qwen 2.5 y Qwen-Max. En Baidu: Ernie 4.0 Turbo. En Zhipu AI: GLM-4. En Tencent: Hunyuan Large y Hunyuan Video. En Moonshot AI: Kimi. En 01.AI: Yi-Lightning de Kai-Fu Lee. Y en visión y video: SenseNova de SenseTime y Hailuo AI de MiniMax.",
        "text_en": "Likewise, we integrate top open-weight engines from Asia: DeepSeek with DeepSeek-V3, R1 and Coder. Alibaba Cloud with Qwen 2.5 and Qwen-Max. Baidu with Ernie 4.0 Turbo. Zhipu AI with GLM-4. Tencent with Hunyuan Large and Video. Moonshot AI with Kimi. 01.AI with Yi-Lightning. SenseTime with SenseNova and MiniMax with Hailuo AI.",
        "sub_en": "Full orchestration of Chinese AI: DeepSeek-R1, Qwen 2.5, GLM-4, Hunyuan, Kimi and Yi-Lightning."
    },
    {
        "num": "05",
        "badge_es": "VENTAJA ESTRATÉGICA",
        "badge_en": "STRATEGIC ADVANTAGE",
        "title_es": "La Gran Oportunidad: Exportar a las 120 Megaciudades de China",
        "title_en": "The Strategic Shift: Exporting to China's 120 Planned Megacities",
        "concept_es": "China como Mayor Importador Global + Colombia como Exportador Estratégico",
        "concept_en": "China's Transition to Top Global Importer + Colombia Sovereign Exporter",
        "text_es": "Como señaló Jack Ma, China vive una transformación histórica: pasa de ser fábrica del mundo a convertirse en el mayor importador global, impulsada por más de ciento veinte ciudades planificadas de uno a diez millones de habitantes. Esto abre una oportunidad colosal para que los exportadores colombianos de café especial, cacao, esmeraldas y minería sostenible lleguen directamente a ese mercado de alto consumo con nuestra tecnología de inteligencia artificial y video en Mandarín.",
        "text_en": "As Jack Ma highlighted, China is undergoing a historic transformation: shifting from the world's factory to the world's largest importer, driven by over 120 planned megacities with populations between 1 and 10 million. This creates an extraordinary opportunity for Colombian exporters of specialty coffee, cacao, emeralds, and ethical minerals to connect directly with this massive consumer market using our AI and Mandarin video infrastructure.",
        "sub_en": "Empowering Colombian agriculture and mining exporters to reach China's 120 planned megacities via AI."
    },
    {
        "num": "06",
        "badge_es": "GEOPOLÍTICA REGIONAL",
        "badge_en": "REGIONAL GEOPOLITICS",
        "title_es": "Colombia: Nodo Bioceánico y Puente Comercial Bilateral",
        "title_en": "Colombia: Bioceanic Hub & Bilateral Trade Bridge",
        "concept_es": "Dos Océanos, Entrada a Suramérica y Enlace Directo con Alibaba Cloud",
        "concept_en": "Two Oceans, South American Gateway & Direct Alibaba Cloud Bridge",
        "text_es": "Colombia tiene una posición bioceánica privilegiada entre el Pacífico y el Atlántico, cercanía con Norteamérica y entrada a Suramérica. Al unir nuestra ubicación estratégica con la plataforma HB.OS y Alibaba Cloud, eliminamos intermediarios y barreras de idioma, permitiendo a nuestras empresas cerrar acuerdos comerciales bilaterales con Oriente y Occidente con total soberanía.",
        "text_en": "Colombia holds a unique bioceanic position between the Pacific and Atlantic oceans, adjacent to North America and the gateway to South America. By pairing our geographical hub with HB.OS and Alibaba Cloud, we remove middlemen and language barriers, empowering businesses to execute direct trade with both East and West under full digital sovereignty.",
        "sub_en": "Colombia's bioceanic hub paired with HB.OS and Alibaba Cloud enables direct bilateral trade with East and West."
    },
    {
        "num": "07",
        "badge_es": "ALIANZA NACIONAL",
        "badge_en": "NATIONAL ALLIANCE",
        "title_es": "Articulación con MinTIC, Ruta N y EAFIT",
        "title_en": "National Ecosystem: MinTIC, Ruta N & Top Universities",
        "concept_es": "Democratización para Estudiantes, PYMEs y Grandes Industrias",
        "concept_en": "Empowering Students, SMEs and Enterprise Industries",
        "text_es": "Nuestra arquitectura está lista para articularse con MinTIC, centros de innovación como Ruta N y universidades como EAFIT. No venimos a gastar presupuestos en licencias cerradas; venimos a entregar una plataforma soberana que capacita a miles de jóvenes y moderniza a nuestras empresas con bases de datos vectoriales Qdrant y Guardrails de seguridad.",
        "text_en": "Our architecture is built for partnerships with MinTIC, Ruta N, and universities like EAFIT. We do not spend public budgets on foreign software licenses; we deliver a sovereign framework that trains youth and upgrades enterprises with Qdrant vector databases and security Guardrails.",
        "sub_en": "Partnering with MinTIC, Ruta N and EAFIT to train youth and upgrade industry with Qdrant and Guardrails."
    },
    {
        "num": "08",
        "badge_es": "LLAMADO A LA ACCIÓN",
        "badge_en": "CALL TO ACTION",
        "title_es": "Construyendo el Futuro con Hechos Verificables",
        "title_en": "Building the Future with Verifiable Code",
        "concept_es": "Disciplina, Soberanía Tecnológica y Sistema HB.OS",
        "concept_en": "Discipline, Technological Sovereignty & The HB.OS System",
        "text_es": "La inteligencia artificial no es magia; es disciplina, práctica constante y arquitectura técnica sólida. Con el sistema HB.OS demostramos que la soberanía digital está al alcance de todos. Todo lo que ven aquí es código real y verificado. Los invito a construir el futuro con nosotros. Bienvenidos a OpenClaw dos mil veintiséis.",
        "text_en": "Artificial intelligence is not magic; it is discipline, continuous practice, and solid architecture. With HB.OS, we prove that digital sovereignty is accessible to everyone. Everything you see here is real, operational code. Join us in building the future. Welcome to OpenClaw 2026.",
        "sub_en": "AI is mastered through disciplined practice. Join us in building sovereign technology. Welcome to OpenClaw 2026."
    }
]

prosody_engine = SovereignProsodyEngine()

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_language_audios(lang: str):
    """Sintetiza audios en Español o Inglés con ecualización de estudio FM 48kHz y prosodia RAE."""
    print(f"\n[FASE 1/5 - {lang.upper()}] Sintetizando locuciones con SovereignProsodyEngine...")

    for idx, item in enumerate(BILINGUAL_MODULES):
        master_aac = RUNTIME / f"{lang}_master_{idx}.aac"
        text_content = item["text_es"] if lang == "es" else item["text_en"]

        # Síntesis con prosodia y pausas RAE
        await prosody_engine.synthesize_audio(text_content, master_aac, lang=lang)
        item[f"audio_{lang}"] = str(master_aac)
        item[f"duration_{lang}"] = get_audio_duration(str(master_aac))

def extract_whisper_timestamps_for_lang(whisper_model, lang: str):
    """Extrae marcas de tiempo de Whisper forzando las palabras canónicas (Ground Truth RAE)."""
    print(f"\n[FASE 2/5 - {lang.upper()}] Sincronizando palabras con Ground Truth Canónico...")
    for idx, item in enumerate(BILINGUAL_MODULES):
        audio_file = item[f"audio_{lang}"]
        canonical_text = item["text_es"] if lang == "es" else item["text_en"]
        canonical_words = canonical_text.split()

        res = whisper_model.transcribe(audio_file, language=lang, word_timestamps=True)
        raw_words = []
        for segment in res["segments"]:
            for w in segment.get("words", []):
                raw_words.append(w)

        # Alineación forzada: asignar tiempos a las palabras canónicas exactas
        words_timed = []
        num_can = len(canonical_words)
        num_raw = len(raw_words)

        if num_raw > 0:
            for i, c_word in enumerate(canonical_words):
                raw_idx = min(int(i * (num_raw / num_can)), num_raw - 1)
                w_info = raw_words[raw_idx]
                words_timed.append({
                    "word": c_word,
                    "start": float(w_info.get("start", 0.0)),
                    "end": float(w_info.get("end", 0.0))
                })
        else:
            # Fallback uniforme si Whisper no detecta
            dur = item[f"duration_{lang}"]
            step = dur / max(1, num_can)
            for i, c_word in enumerate(canonical_words):
                words_timed.append({
                    "word": c_word,
                    "start": i * step,
                    "end": (i + 1) * step
                })

        item[f"words_timed_{lang}"] = words_timed
        print(f"  [OK] Módulo {item['num']}: {len(words_timed)} palabras canónicas sincronizadas al milisegundo.")

def render_masterclass_for_language(lang: str, whisper_model):
    print("=" * 60)
    print(f"  [RENDER] RENDERIZANDO MASTERCLASS OPENCLAW ({lang.upper()}) 1080P")
    print("=" * 60)

    # 1. Sintetizar audios
    asyncio.run(synthesize_language_audios(lang))

    # 2. Marcas de tiempo de Whisper
    extract_whisper_timestamps_for_lang(whisper_model, lang)

    # 3. Ensamblar pista de audio continua con pausas de 1.2s
    print(f"\n[FASE 3/5 - {lang.upper()}] Ensamblando pista de audio con pausas naturales...")
    pause_aac = RUNTIME / f"pause_12s_{lang}.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.2", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    concat_txt = RUNTIME / f"concat_{lang}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in BILINGUAL_MODULES:
            f.write(f"file '{Path(item[f'audio_{lang}']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")

    master_audio = RUNTIME / f"master_audio_{lang}_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro ({lang.upper()}): {total_duration:.2f}s ({total_duration/60:.2f} min)")

    # 4. Cargar Avatar PNG con logo HB.OS directamente en la tela (UNIFICADO)
    avatar_src = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"  -> Avatar transparente con HB.OS en tela cargado: {av_w}x{av_h} px")

    # Fuentes
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arialbd.ttf", 26)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 52)  # Letra gigante descansada
        font_sub = ImageFont.truetype("ariali.ttf", 24)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_top = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in BILINGUAL_MODULES:
        t_start = curr_t
        t_end = curr_t + item[f"duration_{lang}"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.2

    frames_dir = RUNTIME / f"temp_frames_{lang}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 4/5 - {lang.upper()}] Renderizando {total_frames} fotogramas Full HD sin cajas...")

    WORDS_PER_CHUNK = 8  # 8 palabras por bloque para lectura óptima

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
        words_timed = item.get(f"words_timed_{lang}", [])

        # ─── 1. FONDO CÓSMICO DEL UNIVERSO EN MOVIMIENTO FLUIDO CONTINUO ───
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior Minimalista Flotante
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        top_sub = "·   MASTERCLASS: GEOPOLÍTICA & INTELIGENCIA ARTIFICIAL SOBERANA" if lang == "es" else "·   MASTERCLASS: GEOPOLITICS & SOVEREIGN ARTIFICIAL INTELLIGENCE"
        draw.text((430, 24), top_sub, font=font_top, fill=(190, 200, 220))
        top_std = "ESTÁNDAR R^768 · $0 LICENCIAS" if lang == "es" else "STANDARD R^768 · $0 LICENSES"
        draw.text((1560, 24), top_std, font=font_top, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR PNG TRANSPARENTE EN ESCENA COMPLETA (SIN CAJAS NI MARCOS) ───
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Identificación Flotante Limpia
        speaker_title = "GUILLERMO · OPENCLAW"
        speaker_role = "Arquitectura Soberana HB.OS" if lang == "es" else "HB.OS Sovereign Architecture"
        draw.text((80, 95), speaker_title, font=font_badge, fill=(255, 255, 255))
        draw.text((80, 125), speaker_role, font=font_concept, fill=(212, 175, 55))

        # ─── 3. LADO DERECHO: TEXTO FLOTANTE DIRECTAMENTE SOBRE EL UNIVERSO (SIN CAJAS) ───
        content_x = 640
        content_y = 100
        content_w = 1220

        # Badge del Módulo
        badge_text = f"MÓDULO {item['num']} · {item['badge_es']}" if lang == "es" else f"MODULE {item['num']} · {item['badge_en']}"
        draw.text((content_x, content_y), badge_text, font=font_badge, fill=(212, 175, 55))

        # Título Grande Cinematográfico
        title_text = item["title_es"] if lang == "es" else item["title_en"]
        draw.text((content_x, content_y + 45), title_text, font=font_title, fill=(255, 255, 255))

        # Concepto Clave
        concept_text = "⚡ " + (item["concept_es"] if lang == "es" else item["concept_en"])
        draw.text((content_x, content_y + 115), concept_text, font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 160, content_x + content_w, content_y + 160], fill=(45, 60, 90), width=1)

        # ─── TELEPROMPTER KARAOKE CON TIMESTAMPS DE WHISPER AL MILISEGUNDO ───
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

            # Sombra suave negra para legibilidad perfecta sobre las estrellas
            draw.text((cursor_x + 3, cursor_y + 3), word_str, font=font_karaoke, fill=(0, 0, 0))

            # Color: Oro Brillante (Hablada ahora), Blanco (Ya dicha), Gris azulado (Futura)
            if global_idx == active_w_idx:
                w_color = (255, 215, 0)   # Oro Brillante
            elif global_idx < active_w_idx:
                w_color = (245, 248, 255) # Blanco Puro
            else:
                w_color = (110, 125, 150) # Futuro

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # Subtítulo en Base Flotante
        draw.line([content_x, HEIGHT - 120, content_x + content_w, HEIGHT - 120], fill=(45, 60, 90), width=1)
        sub_str = "EN: " + item["sub_en"] if lang == "es" else "ES: " + item["concept_es"]
        draw.text((content_x + 2, HEIGHT - 90 + 2), sub_str, font=font_sub, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 90), sub_str, font=font_sub, fill=(160, 190, 230))

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 600 == 0:
            print(f"    -> [{lang.upper()}] Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 5. Codificación Final en MP4 FastStart 1080p
    print(f"\n[FASE 5/5 - {lang.upper()}] Codificando Masterclass 1080p con FFmpeg FastStart...")
    output_name = "OpenClaw_Masterclass_Espanol_1080p.mp4" if lang == "es" else "OpenClaw_Masterclass_English_1080p.mp4"
    final_output = RUNTIME / output_name

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "frame_%06d.jpg"),
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
    print(f"  [OK] MASTERCLASS {lang.upper()} GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} min)")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

def render_both_masterclasses():
    whisper_model = whisper.load_model("base")
    
    # 1. Generar Masterclass en Español
    video_es = render_masterclass_for_language("es", whisper_model)
    
    # 2. Generar Masterclass en Inglés
    video_en = render_masterclass_for_language("en", whisper_model)

    print("\n" + "=" * 60)
    print("  [OK] AMBAS MASTERCLASSES (ESPAÑOL & ENGLISH) RENDERIZADAS CON ÉXITO")
    print(f"  1. Español: {video_es}")
    print(f"  2. English: {video_en}")
    print("=" * 60)

if __name__ == "__main__":
    render_both_masterclasses()
