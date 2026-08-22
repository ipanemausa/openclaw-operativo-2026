"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS PRÍSTINA BILINGÜE: ORTOGRAFÍA & MODELOS EXACTOS
==============================================================================
- Capa de Texto Prístina: Tipografía 100% exacta sin tocar la escritura original
- Nombres de Personas: Jensen Huang (NVIDIA), Dario Amodei (Anthropic)
- Entidades Colombia: MinTIC, Ruta N, EAFIT, Guardrails
- Modelos Americanos Exactos:
  * OpenAI: GPT-4o, GPT-4o mini, o1, o3-mini, DALL·E 3, Sora, Whisper
  * Google DeepMind: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0 Flash, Imagen 3, Gemma 2
  * Anthropic: Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus
  * Meta: Llama 3.1, Llama 3.2, Llama 3.3
  * xAI: Grok-2, Grok-3
  * Cohere / Amazon: Command R+, Amazon Nova
- Modelos Chinos Exactos:
  * DeepSeek: DeepSeek-V3, DeepSeek-R1, DeepSeek-Coder, DeepSeek-VL
  * Alibaba Cloud: Qwen 2.5, Qwen-VL, Qwen-Max
  * Baidu: Ernie Bot (Ernie 4.0 Turbo)
  * Zhipu AI (GLM): ChatGLM, GLM-4, GLM-4-Voice
  * Tencent: Hunyuan (Hunyuan Video, Hunyuan Large)
  * Moonshot AI: Kimi
  * 01.AI (Kai-Fu Lee): Yi-Lightning, Yi-1.5, Yi-Large
  * SenseTime: SenseNova
  * MiniMax: abab 6.5, Hailuo AI
- Avatar: HB.OS bordado directamente en los píxeles de la camisa (Sin cajas)
- Visual: Universo Cósmico Seamless (180 estrellas con paralaje)
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
RUNTIME = ROOT / "runtime" / "masterclass_pristina_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame

# ─── MÓDULOS CON TEXTO PRÍSTINO Y ORTOGRAFÍA 100% VERIFICADA ────────────────

PRISTINE_MODULES = [
    {
        "num": "01",
        "badge_es": "VISIÓN SOBERANA",
        "badge_en": "SOVEREIGN VISION",
        "title_es": "La Verdadera Soberanía en Inteligencia Artificial",
        "title_en": "True Sovereignty in Artificial Intelligence",
        "concept_es": "Acceso Universal sin Peajes ni Licencias Millonarias",
        "concept_en": "Universal Access with Zero SaaS Tax & Zero Licensing Fees",
        "text_es": "Hola a todos, les habla Guillermo. Bienvenidos a OpenClaw. Durante años, a las empresas y a los estudiantes les dijeron que para usar inteligencia artificial debían pagar costosas licencias en dólares. Hoy demostramos que con rigor, código abierto y arquitectura soberana, podemos competir al más alto nivel mundial a costo cero de licencias.",
        "text_en": "Hello everyone, this is Guillermo. Welcome to OpenClaw. For years, businesses and students were told they needed expensive recurring software licenses to access artificial intelligence. Today we demonstrate that with sovereign architecture and open-weight models, we can compete at the highest global level at zero licensing costs.",
        "sub_en": "Welcome. We demonstrate sovereign AI architecture built on open-weight models with zero licensing fees."
    },
    {
        "num": "02",
        "badge_es": "SÍNTESIS HUANG-AMODEI",
        "badge_en": "HUANG-AMODEI SYNTHESIS",
        "title_es": "Jensen Huang y Dario Amodei: La Fuerza Resultante",
        "title_en": "Jensen Huang & Dario Amodei: The Resultant Force",
        "concept_es": "Cómputo Masivo de NVIDIA + Guardrails de Seguridad de Anthropic",
        "concept_en": "NVIDIA Compute Scaling + Anthropic Safety Guardrails",
        "text_es": "En la vanguardia mundial conviven dos visiones fundamentales. Jensen Huang de NVIDIA impulsa el escalamiento masivo del cómputo. Dario Amodei de Anthropic exige seguridad estricta y control de riesgos. Nuestra arquitectura une ambas fuerzas: aceleramos el procesamiento distribuido, protegiendo al cien por ciento la privacidad de nuestros datos con Guardrails deterministas.",
        "text_en": "At the global forefront, two foundational visions unite. Jensen Huang of NVIDIA drives massive compute scaling. Dario Amodei of Anthropic demands strict safety and risk control. Our architecture combines both forces: scaling distributed compute while fully protecting proprietary enterprise data with deterministic Guardrails.",
        "sub_en": "Synthesizing Jensen Huang's compute scaling with Dario Amodei's safety guardrails to protect proprietary data."
    },
    {
        "num": "03",
        "badge_es": "MODELOS AMERICANOS",
        "badge_en": "AMERICAN AI MODELS",
        "title_es": "Ecosistema de Inteligencia Artificial de Estados Unidos",
        "title_en": "Leading American Artificial Intelligence Models",
        "concept_es": "OpenAI, Google DeepMind, Anthropic, Meta, xAI, Cohere y Amazon",
        "concept_en": "OpenAI, Google DeepMind, Anthropic, Meta, xAI, Cohere & Amazon",
        "text_es": "Nuestra plataforma se conecta con los modelos líderes de Estados Unidos: OpenAI con GPT-4o, GPT-4o mini, o1, o3-mini, DALL·E 3, Sora y Whisper. Google DeepMind con Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash, Imagen 3 y Gemma 2. Anthropic con Claude 3.5 Sonnet, Claude 3.5 Haiku y Claude 3 Opus. Meta con Llama 3.1, Llama 3.2 y Llama 3.3. xAI con Grok-2 y Grok-3. Y modelos empresariales como Command R+ de Cohere y Amazon Nova.",
        "text_en": "Our platform connects directly to leading American AI models: OpenAI with GPT-4o, GPT-4o mini, o1, o3-mini, DALL·E 3, Sora and Whisper. Google DeepMind with Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash, Imagen 3 and Gemma 2. Anthropic with Claude 3.5 Sonnet, Claude 3.5 Haiku and Claude 3 Opus. Meta with Llama 3.1, Llama 3.2 and Llama 3.3. xAI with Grok-2 and Grok-3. And enterprise engines like Cohere Command R+ and Amazon Nova.",
        "sub_en": "Full orchestration of American AI: OpenAI, Gemini 2.0, Claude 3.5 Sonnet, Llama 3.3, Grok-3 and Cohere."
    },
    {
        "num": "04",
        "badge_es": "MODELOS CHINOS",
        "badge_en": "CHINESE AI MODELS",
        "title_es": "Ecosistema de Inteligencia Artificial de Oriente y Asia",
        "title_en": "Leading Chinese & Asian Open-Weight AI Models",
        "concept_es": "DeepSeek, Alibaba Qwen, Baidu Ernie, Zhipu GLM, Tencent y Kimi",
        "concept_en": "DeepSeek, Alibaba Qwen, Baidu Ernie, Zhipu GLM, Tencent & Kimi",
        "text_es": "Asimismo, integramos los motores más potentes de Oriente: DeepSeek con DeepSeek-V3, DeepSeek-R1, DeepSeek-Coder y DeepSeek-VL. Alibaba Cloud con Qwen 2.5, Qwen-VL y Qwen-Max. Baidu con Ernie Bot y Ernie 4.0 Turbo. Zhipu AI con ChatGLM, GLM-4 y GLM-4-Voice. Tencent con Hunyuan Video y Hunyuan Large. Moonshot AI con Kimi. 01.AI con Yi-Lightning, Yi-1.5 y Yi-Large de Kai-Fu Lee. SenseTime con SenseNova y MiniMax con abab 6.5 y Hailuo AI.",
        "text_en": "Likewise, we integrate top open-weight engines from Asia: DeepSeek with DeepSeek-V3, DeepSeek-R1, DeepSeek-Coder and DeepSeek-VL. Alibaba Cloud with Qwen 2.5, Qwen-VL and Qwen-Max. Baidu with Ernie Bot and Ernie 4.0 Turbo. Zhipu AI with ChatGLM, GLM-4 and GLM-4-Voice. Tencent with Hunyuan Video and Hunyuan Large. Moonshot AI with Kimi. 01.AI with Yi-Lightning, Yi-1.5 and Yi-Large. SenseTime with SenseNova and MiniMax with abab 6.5 and Hailuo AI.",
        "sub_en": "Full orchestration of Chinese AI: DeepSeek-R1, Qwen 2.5, GLM-4, Hunyuan, Kimi and Yi-Lightning."
    },
    {
        "num": "05",
        "badge_es": "VENTAJA COMPARATIVA",
        "badge_en": "STRATEGIC ADVANTAGE",
        "title_es": "La Ventaja Estratégica de Colombia y Latinoamérica",
        "title_en": "The Unique Comparative Advantage of Latin America",
        "concept_es": "Libre Acceso a Oriente y Occidente sin Bloqueos Geopolíticos",
        "concept_en": "Unrestricted Access to Both Eastern & Western AI Without Geopolitical Friction",
        "text_es": "Aquí radica nuestra ventaja objetiva: la población en China está restringida por el estado para usar modelos americanos, y en Estados Unidos hay barreras regulatorias crecientes contra los modelos chinos. En Colombia y Latinoamérica tenemos la libertad de usar lo mejor de ambos mundos, combinando la visión de Claude y Gemini con la potencia abierta y a costo cero de DeepSeek y Qwen.",
        "text_en": "Here lies our greatest comparative advantage: users in China face state restrictions accessing American models, while the US faces rising barriers against Chinese engines. In Colombia and Latin America, we have full freedom to combine the best of both worlds, uniting Claude and Gemini with the zero-cost open power of DeepSeek and Qwen.",
        "sub_en": "Latin America uniquely accesses both Western intelligence and Asian open-weight power without geopolitical barriers."
    },
    {
        "num": "06",
        "badge_es": "GEOPOLÍTICA REGIONAL",
        "badge_en": "REGIONAL GEOPOLITICS",
        "title_es": "Colombia: Nodo Bioceánico y Capital del Talento",
        "title_en": "Colombia: Bioceanic Hub & Talent Capital",
        "concept_es": "Dos Océanos, Puerta a Suramérica y Alta Receptividad",
        "concept_en": "Two Oceans, Gateway to South America & Rapid AI Adoption",
        "text_es": "Colombia cuenta con una ubicación bioceánica privilegiada entre el Pacífico y el Atlántico, cercanía con Norteamérica y entrada a Suramérica. Pero lo más valioso es que nuestra gente tiene un interés y una velocidad de adopción de la inteligencia artificial superior a la de muchos países desarrollados. El momento de liderar la transformación productiva es ahora.",
        "text_en": "Colombia holds a strategic bioceanic position between the Pacific and Atlantic oceans, near North America and opening to South America. Even more importantly, our people demonstrate an AI adoption rate and enthusiasm higher than many developed nations. The time to lead this productive transformation is now.",
        "sub_en": "Colombia's bioceanic location and rapid AI adoption make it the natural technology hub for the Americas."
    },
    {
        "num": "07",
        "badge_es": "ECOSISTEMA NACIONAL",
        "badge_en": "NATIONAL ECOSYSTEM",
        "title_es": "Alianza con MinTIC, Ruta N y Universidades como EAFIT",
        "title_en": "National Alliance: MinTIC, Ruta N & Top Universities",
        "concept_es": "Democratización para Estudiantes, PYMEs y Grandes Industrias",
        "concept_en": "Empowering Students, SMEs and Enterprise Industries",
        "text_es": "Nuestra plataforma está lista para articularse con MinTIC, centros de innovación como Ruta N y universidades líderes como EAFIT. No venimos a gastar presupuestos en licencias propietarias cerradas; venimos a transferir una arquitectura soberana que capacita a miles de jóvenes y moderniza a nuestras empresas con bases de datos vectoriales Qdrant y Guardrails de seguridad.",
        "text_en": "Our architecture is built for partnerships with MinTIC, Ruta N, and top universities like EAFIT. We do not spend public budgets on closed proprietary licenses; we deliver a sovereign framework that trains youth and upgrades enterprises with Qdrant vector databases and security Guardrails.",
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
        "text_es": "La inteligencia artificial no es magia; es disciplina, práctica rigurosa y arquitectura técnica sólida. Con el sistema HB.OS demostramos que la soberanía digital está al alcance de todos. Todo lo que ven aquí es código real, soberano y verificado. Los invito a construir el futuro con nosotros. Bienvenidos a OpenClaw dos mil veintiséis.",
        "text_en": "Artificial intelligence is not magic; it is discipline, rigorous practice, and solid technical architecture. With HB.OS, we prove that digital sovereignty is accessible to everyone. Everything you see here is real, operational code. Join us in building the future. Welcome to OpenClaw 2026.",
        "sub_en": "AI is mastered through disciplined practice. Join us in building sovereign technology. Welcome to OpenClaw 2026."
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

async def synthesize_language_audios(lang: str):
    """Sintetiza audios en Español o Inglés con ecualización de estudio FM 48kHz (-16 LUFS)."""
    print(f"\n[FASE 1/5 - {lang.upper()}] Sintetizando locuciones...")
    voice_name = "es-CO-GonzaloNeural" if lang == "es" else "en-US-GuyNeural"
    rate_val = "-7%"  # Cadencia pausada para perfecta comprensión
    pitch_val = "-2Hz"

    for idx, item in enumerate(PRISTINE_MODULES):
        raw_mp3 = RUNTIME / f"{lang}_raw_{idx}.mp3"
        master_aac = RUNTIME / f"{lang}_master_{idx}.aac"
        text_content = item["text_es"] if lang == "es" else item["text_en"]

        comm = edge_tts.Communicate(text_content, voice=voice_name, rate=rate_val, pitch=pitch_val)
        await comm.save(str(raw_mp3))

        # Cadena de Ecualización Paramétrica FM Broadcast (-16 LUFS EBU R128)
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
        item[f"audio_{lang}"] = str(master_aac)
        item[f"duration_{lang}"] = dur
        title_str = item["title_es"] if lang == "es" else item["title_en"]
        print(f"  [OK] Módulo {item['num']}: {dur:.2f}s | '{title_str}'")

def extract_whisper_timestamps_for_lang(whisper_model, lang: str):
    """Extrae marcas de tiempo de Whisper para sincronizar el karaoke sobre el texto prístino."""
    print(f"\n[FASE 2/5 - {lang.upper()}] Extrayendo marcas de tiempo con Whisper...")
    for idx, item in enumerate(PRISTINE_MODULES):
        audio_file = item[f"audio_{lang}"]
        res = whisper_model.transcribe(audio_file, language=lang, word_timestamps=True)
        whisper_words = []
        for segment in res["segments"]:
            for w in segment.get("words", []):
                whisper_words.append({
                    "start": float(w["start"]),
                    "end": float(w["end"])
                })
        item[f"whisper_words_{lang}"] = whisper_words
        print(f"  [OK] Módulo {item['num']}: {len(whisper_words)} marcas temporales capturadas.")

def render_pristine_masterclass_for_language(lang: str, whisper_model):
    print("=" * 60)
    print(f"  [RENDER] RENDERIZANDO MASTERCLASS PRÍSTINA OPENCLAW ({lang.upper()}) 1080P")
    print("=" * 60)

    # 1. Sintetizar audios
    asyncio.run(synthesize_language_audios(lang))

    # 2. Marcas de tiempo de Whisper
    extract_whisper_timestamps_for_lang(whisper_model, lang)

    # 3. Ensamblar pista de audio continua con pausas de 1.2s
    print(f"\n[FASE 3/5 - {lang.upper()}] Ensamblando pista de audio continua con pausas...")
    pause_aac = RUNTIME / f"pause_12s_{lang}.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.2", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    concat_txt = RUNTIME / f"concat_{lang}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in PRISTINE_MODULES:
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
    print(f"  -> Avatar transparente cargado: {av_w}x{av_h} px")

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
    for item in PRISTINE_MODULES:
        t_start = curr_t
        t_end = curr_t + item[f"duration_{lang}"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.2

    frames_dir = RUNTIME / f"temp_frames_{lang}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 4/5 - {lang.upper()}] Renderizando {total_frames} fotogramas Full HD con texto prístino...")

    WORDS_PER_CHUNK = 8  # 8 palabras prístinas por bloque para lectura óptima

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
        whisper_words = item.get(f"whisper_words_{lang}", [])

        # TEXTO PRÍSTINO: Tomado directamente del original sin tocar su ortografía ni mayúsculas
        pristine_text = item["text_es"] if lang == "es" else item["text_en"]
        pristine_words = pristine_text.split()
        total_pristine_words = len(pristine_words)

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

        # ─── TELEPROMPTER KARAOKE SOBRE EL TEXTO PRÍSTINO ORIGINAL ───
        # Mapeo determinista de progreso temporal al índice de palabra prístina
        if len(whisper_words) > 0 and len(whisper_words) == total_pristine_words:
            active_w_idx = 0
            for w_i, w_info in enumerate(whisper_words):
                if w_info["start"] <= t_rel <= w_info["end"]:
                    active_w_idx = w_i
                    break
                elif t_rel > w_info["end"]:
                    active_w_idx = w_i + 1
        else:
            # Fallback proporcional exacto si el conteo de tokens de whisper difiere del de palabras
            dur_mod = max(0.1, item[f"duration_{lang}"])
            active_w_idx = int((t_rel / dur_mod) * total_pristine_words)

        chunk_idx = active_w_idx // WORDS_PER_CHUNK
        chunk_start = chunk_idx * WORDS_PER_CHUNK
        chunk_end = min(total_pristine_words, chunk_start + WORDS_PER_CHUNK)
        current_chunk_words = pristine_words[chunk_start:chunk_end]

        cursor_x = content_x
        cursor_y = content_y + 240
        line_height = 80
        max_line_w = content_w - 40

        for w_local_idx, word in enumerate(current_chunk_words):
            global_idx = chunk_start + w_local_idx
            word_str = word + " "
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
    output_name = "OpenClaw_Masterclass_Espanol_Pristina_1080p.mp4" if lang == "es" else "OpenClaw_Masterclass_English_Pristina_1080p.mp4"
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
    print(f"  [OK] MASTERCLASS PRÍSTINA {lang.upper()} GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} min)")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

def render_both_pristine_masterclasses():
    whisper_model = whisper.load_model("base")
    
    # 1. Generar Masterclass en Español
    video_es = render_pristine_masterclass_for_language("es", whisper_model)
    
    # 2. Generar Masterclass en Inglés
    video_en = render_pristine_masterclass_for_language("en", whisper_model)

    print("\n" + "=" * 60)
    print("  [OK] AMBAS MASTERCLASSES PRÍSTINAS RENDERIZADAS CON ÉXITO")
    print(f"  1. Español: {video_es}")
    print(f"  2. English: {video_en}")
    print("=" * 60)

if __name__ == "__main__":
    render_both_pristine_masterclasses()
