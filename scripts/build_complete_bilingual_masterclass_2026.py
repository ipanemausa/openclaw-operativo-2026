"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS BILINGÜE COMPLETA (ESPAÑOL & ENGLISH)
==============================================================================
- Estándar "Podcast Anchor": Dicción nítida, cadencia reflexiva y pausas calibradas
- Estructura Visual: Breakdown Jerárquico en Balas (Bullets) + Diagramas NVIDIA/Transformer
- Audio: 48kHz Stereo EBU R128 (-16 LUFS), Barítono Cálido (100.87 Hz)
- Video: 1080p FastStart MP4 a 25 FPS sin cajas ni marcos
==============================================================================
"""

import os
import sys
import math
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
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

# ─── CONTENIDO ESTRUCTURADO PODCAST ANCHOR (BALAS & EXPLICACIÓN INDIVIDUAL) ──

BILINGUAL_MODULES = [
    {
        "num": "01",
        "badge_es": "VISIÓN & IDENTIDAD",
        "badge_en": "SOVEREIGN IDENTITY",
        "title_es": "La Autenticidad de la Voz y la Soberanía Tecnológica",
        "title_en": "Authentic Voice & Technological Sovereignty",
        "concept_es": "Inspiración en Jensen Huang y Fei-Fei Li: Identidad y Cero Peajes",
        "concept_en": "Jensen Huang & Fei-Fei Li: True Identity & Zero SaaS Tax",
        "bullets_es": [
            "• Identidad Vocal: La voz humana como firma biométrica inconfundible del fundador.",
            "• Soberanía Digital: Competir al más alto nivel global sin pagar rentas eternas en dólares.",
            "• Arquitectura Soberana: Control absoluto de los datos en infraestructura propia."
        ],
        "bullets_en": [
            "• Vocal Identity: Human voice as the founder's authentic biometric signature.",
            "• Digital Sovereignty: Competing globally without recurring SaaS tax.",
            "• Sovereign Architecture: Complete data ownership on dedicated local hardware."
        ],
        "text_es": "Hola a todos, les habla Guillermo. Bienvenidos a OpenClaw. Como enseñan pioneros como Jensen Huang y la doctora Fei-Fei Li, la verdadera tecnología no es depender de cajas negras; es construir identidad y soberanía. Durante años nos hicieron creer que para usar inteligencia artificial debíamos pagar licencias millonarias. Hoy demostramos que con arquitectura soberana y modelos abiertos, competimos al más alto nivel mundial a costo cero de licencias.",
        "text_en": "Hello everyone, this is Guillermo. Welcome to OpenClaw. As pioneers like Jensen Huang and Doctor Fei-Fei Li demonstrate, true technology is about identity and sovereignty. For years we were told we had to pay expensive recurring licenses. Today we prove that with open-weight models and sovereign architecture, we compete at the highest global level at zero licensing costs.",
        "sub_en": "True AI sovereignty built on open-weight models and authentic vocal biometric identity."
    },
    {
        "num": "02",
        "badge_es": "ECOSISTEMA OPENAI",
        "badge_en": "OPENAI ECOSYSTEM",
        "title_es": "Desglose Individual de Modelos OpenAI",
        "title_en": "Individual Breakdown of OpenAI Models",
        "concept_es": "GPT-4o, o1 y o3-mini: Propósito Específico y Diferencias Clave",
        "concept_en": "GPT-4o, o1 & o3-mini: Specific Capabilities & Key Differences",
        "bullets_es": [
            "• GPT-4o: Modelo insignia multimodal para texto, visión y audio en tiempo real.",
            "• o1: Razonamiento profundo paso a paso (Chain-of-Thought) para ciencias complejas.",
            "• o3-mini: Razonador ultra-rápido y eficiente para programación pesada."
        ],
        "bullets_en": [
            "• GPT-4o: Flagship multimodal model for real-time text, vision, and audio.",
            "• o1: Deep step-by-step reasoning (Chain-of-Thought) for complex science.",
            "• o3-mini: High-speed lightweight reasoner optimized for intensive coding."
        ],
        "text_es": "Miremos primero el ecosistema de OpenAI, desglosando cada modelo por su función real. Por un lado tenemos a GPT-4o, su modelo insignia multimodal que procesa texto, visión y audio en tiempo real con alta velocidad. Para tareas de razonamiento profundo crearon la serie o1, que piensa paso a paso antes de responder. Y tienen a o3-mini, optimizado para programación pesada y matemáticas con extrema eficiencia.",
        "text_en": "Let us examine the OpenAI ecosystem, breaking down each model by its exact purpose. First, GPT-4o is their flagship multimodal model for real-time text, vision, and audio. For deep reasoning, they built the o1 series, which thinks step-by-step before answering. And o3-mini provides high-speed, lightweight reasoning optimized for advanced coding.",
        "sub_en": "OpenAI breakdown: GPT-4o for multimodal speed, o1 for deep reasoning, and o3-mini for coding."
    },
    {
        "num": "03",
        "badge_es": "ECOSISTEMA ANTHROPIC",
        "badge_en": "ANTHROPIC ECOSYSTEM",
        "title_es": "La Familia Claude: Seguridad y Código de Precisión",
        "title_en": "The Claude Family: Constitutional Safety & Precision Code",
        "concept_es": "Claude 3.5 Sonnet, Claude 3.5 Haiku y Claude Opus 4.6",
        "concept_en": "Claude 3.5 Sonnet, Claude 3.5 Haiku & Claude Opus 4.6",
        "bullets_es": [
            "• Claude 3.5 Sonnet: El estándar de oro en generación de software y análisis técnico.",
            "• Claude 3.5 Haiku: Máxima velocidad y bajo coste para flujos masivos de datos.",
            "• Claude Opus 4.6: Capacidad analítica superior para documentos corporativos extensos."
        ],
        "bullets_en": [
            "• Claude 3.5 Sonnet: The gold standard for software engineering and technical design.",
            "• Claude 3.5 Haiku: Blazing speed and low latency for high-volume pipelines.",
            "• Claude Opus 4.6: Superior analytical reasoning for massive enterprise context."
        ],
        "text_es": "Ahora pasemos a Anthropic y su familia Claude, reconocida por su rigor en código y seguridad constitucional. Su estrella es Claude 3.5 Sonnet, el modelo más preciso del mundo para arquitectura de software y generación de código limpio. Si necesitas rapidez extrema para miles de consultas diarias, está Claude 3.5 Haiku. Y en la cima analítica se encuentra Claude Opus, diseñado para procesar contextos gigantescos sin perder el rigor conceptual.",
        "text_en": "Now let us examine Anthropic and the Claude family, recognized for precision code and constitutional safety. Claude 3.5 Sonnet is the global benchmark for clean software engineering and architecture. Claude 3.5 Haiku delivers high-throughput speed for daily queries. And Claude Opus handles massive analytical contexts with flawless continuity.",
        "sub_en": "Anthropic breakdown: Claude 3.5 Sonnet for code mastery, Haiku for speed, and Opus for deep analysis."
    },
    {
        "num": "04",
        "badge_es": "SOBERANÍA OPENCLAW",
        "badge_en": "OPENCLAW SOVEREIGNTY",
        "title_es": "Modelos Open-Weight: DeepSeek, Qwen y Soberanía Local",
        "title_en": "Open-Weight Frontier: DeepSeek, Qwen & Local Sovereignty",
        "concept_es": "DeepSeek-R1 y Qwen 2.5: Inferencia Local con Cero Dependencia Externa",
        "concept_en": "DeepSeek-R1 & Qwen 2.5: Local Inference with Zero External Lock-in",
        "bullets_es": [
            "• DeepSeek-R1: Razonamiento matemático abierto de nivel o1 a costo de licencia cero.",
            "• Alibaba Qwen 2.5: Excelencia multilingüe, código y orquestación B2B.",
            "• Memoria Vectorial R^768: Gobernanza de datos privada con BAAI/bge-m3 y Qdrant."
        ],
        "bullets_en": [
            "• DeepSeek-R1: Open reasoning matching frontier proprietary models at zero licensing cost.",
            "• Alibaba Qwen 2.5: Multilingual mastery, coding, and enterprise B2B orchestration.",
            "• R^768 Vector Memory: Private enterprise data governance using BAAI/bge-m3 and Qdrant."
        ],
        "text_es": "Frente a las APIs cerradas, en OpenClaw construimos sobre modelos de pesos abiertos de primer nivel mundial. Integramos DeepSeek-R1 para razonamiento lógico avanzado y Alibaba Qwen 2.5 para orquestación empresarial. Al operar estos modelos en infraestructura propia con bases de datos vectoriales en espacio R 768, protegemos la privacidad de tu negocio y eliminamos las facturas en dólares.",
        "text_en": "In contrast to closed APIs, OpenClaw builds directly on world-class open-weight models. We integrate DeepSeek-R1 for open frontier reasoning and Alibaba Qwen 2.5 for enterprise orchestration. By deploying these models on sovereign infrastructure with 768-dimensional vector memory, we protect data privacy and eliminate recurring software tax.",
        "sub_en": "OpenClaw sovereign stack: DeepSeek-R1, Qwen 2.5, and private R^768 vector memory at zero license fee."
    },
    {
        "num": "05",
        "badge_es": "HARDWARE & WORLD MODELS",
        "badge_en": "HARDWARE & WORLD MODELS",
        "title_es": "NVIDIA Omniverse, Chips Multimodales y Modelos de Mundo",
        "title_en": "NVIDIA Omniverse, Multimodal Chips & World Models",
        "concept_es": "Mecanismo de Atención, Reconstrucción 4K y Simulación Espacial 3D",
        "concept_en": "Attention Mechanisms, Neural 4K DLSS & 3D Spatial Simulation",
        "bullets_es": [
            "• Mecanismo de Atención: Relaciones semánticas palabra por palabra en espacio latente.",
            "• Especialización de Chips: Visión, audio y lenguaje acelerados por Tensor Cores.",
            "• World Models (Omniverse): Simulación de física real y gemelos digitales de joyería."
        ],
        "bullets_en": [
            "• Attention Mechanism: Semantic word-to-word relationships in latent mathematical space.",
            "• Chip Acceleration: Specialized Tensor Cores for vision, speech, and language.",
            "• World Models (Omniverse): Physical simulation and 3D digital twins for high jewelry."
        ],
        "text_es": "Como explica Jensen Huang, el hardware de NVIDIA no solo procesa datos; simula la física del mundo real. El mecanismo de atención permite a los Transformers entender la relación profunda entre cada palabra. Con NVIDIA Omniverse y los modelos espaciales de la doctora Fei-Fei Li, creamos gemelos digitales de piezas de joyería con física de luz real y renderizado neuronal en tiempo real.",
        "text_en": "As Jensen Huang highlights, NVIDIA hardware does not simply process data; it simulates real-world physics. The attention mechanism enables Transformers to calculate semantic relationships across every word. Pairing NVIDIA Omniverse with Doctor Fei-Fei Li's spatial models allows us to render 3D jewelry digital twins with accurate physical lighting in real time.",
        "sub_en": "Harnessing NVIDIA attention mechanisms, Omniverse simulation, and spatial 3D world models."
    },
    {
        "num": "06",
        "badge_es": "COMERCIO GLOBAL",
        "badge_en": "GLOBAL TRADE",
        "title_es": "De Guangzhou y Miami a las 120 Megaciudades de China",
        "title_en": "From Guangzhou & Miami to China's 120 Planned Megacities",
        "concept_es": "45 Años de Experiencia en Importaciones y Arbitraje B2B Global",
        "concept_en": "45 Years of Field Mastery in Global B2B Import & Export Operations",
        "bullets_es": [
            "• Experiencia Real: 20 años en Downtown Miami importando de Guangzhou, Tailandia y Brasil.",
            "• Factorías de Precisión: Trabajo directo con Xuping, Gemsme y manufactura de Liwan.",
            "• Exportación Inteligente: Conectar café, cacao y joyería colombiana con China usando IA."
        ],
        "bullets_en": [
            "• Proven Field Mastery: 20 years in Downtown Miami importing from Guangzhou, Thailand, and Brazil.",
            "• Factory Partnerships: Direct supply chains with Xuping, Gemsme, and Liwan manufacturing hubs.",
            "• Smart Trade: Connecting Colombian emeralds, coffee, and jewelry to China via AI video."
        ],
        "text_es": "Esta arquitectura nace de cuarenta y cinco años de experiencia en comercio exterior. Durante veinte años en el Downtown de Miami importé directamente desde factorías en Guangzhou como Xuping y Gemsme, así como de Tailandia, Brasil e India. Hoy aplicamos esa misma lógica de arbitraje global para que los exportadores colombianos de joyería, café y minerales lleguen directamente a las ciento veinte megaciudades de China con agentes inteligentes.",
        "text_en": "This architecture is built on 45 years of practical global trade experience. For 20 years in Downtown Miami, I imported directly from precision factories in Guangzhou like Xuping and Gemsme, as well as Thailand, Brazil, and India. Today we apply that same global trade logic so Colombian exporters can reach China's 120 planned megacities using sovereign AI agents.",
        "sub_en": "Applying 45 years of global trade mastery to export Colombian value to China's 120 megacities."
    },
    {
        "num": "07",
        "badge_es": "ALIANZA NACIONAL",
        "badge_en": "NATIONAL ALLIANCE",
        "title_es": "Alianza Estratégica con MinTIC, Ruta N y EAFIT",
        "title_en": "Strategic Alliance with MinTIC, Ruta N & Top Universities",
        "concept_es": "Capacitación Soberana para Jóvenes, PYMEs y Gremios Exportadores",
        "concept_en": "Empowering Students, SMEs & Exporters with Open Sovereign AI",
        "bullets_es": [
            "• Democratización Real: Enseñar arquitectura de IA aplicada sin costo de licencias.",
            "• Modernización Industrial: Integración de bases vectoriales para empresas locales.",
            "• Neuroplasticidad & Lógica: Formación enfocada en razonamiento y modelos de negocio."
        ],
        "bullets_en": [
            "• True Democratization: Teaching applied AI architecture at zero licensing software cost.",
            "• Industrial Modernization: Deploying local vector stores for Colombian businesses.",
            "• Applied Neuroplasticity: Education centered on logic, reasoning, and real enterprise value."
        ],
        "text_es": "Nuestra plataforma está diseñada para articularse con MinTIC, centros de innovación como Ruta N y universidades como EAFIT. No venimos a gastar presupuestos públicos en licencias extranjeras; venimos a entregar un marco soberano que capacita a miles de jóvenes y moderniza a nuestras empresas con bases vectoriales, neuroplasticidad y disciplina operativa.",
        "text_en": "Our platform is built to partner with MinTIC, innovation hubs like Ruta N, and top universities like EAFIT. We do not consume public budgets on foreign software licenses; we deliver a sovereign framework that trains youth and upgrades enterprises with vector memory and operational discipline.",
        "sub_en": "Partnering with MinTIC, Ruta N and EAFIT to train talent and upgrade industry via sovereign AI."
    },
    {
        "num": "08",
        "badge_es": "LLAMADO A LA ACCIÓN",
        "badge_en": "CALL TO ACTION",
        "title_es": "Construyendo Soberanía con Hechos Verificables",
        "title_en": "Building Sovereignty with Verifiable Code",
        "concept_es": "Disciplina, Arquitectura y el Ecosistema OpenClaw 2026",
        "concept_en": "Discipline, Architecture & The OpenClaw 2026 Ecosystem",
        "bullets_es": [
            "• Código Verificable: Arquitectura 100% real operando en producción.",
            "• Ecosistema HB.OS: La unión de inteligencia artificial, comercio y marca personal.",
            "• Bienvenidos al Futuro: Construyamos soberanía digital juntos."
        ],
        "bullets_en": [
            "• Verifiable Code: 100% production-ready architecture operational today.",
            "• HB.OS Ecosystem: Uniting artificial intelligence, global trade, and authentic voice.",
            "• Welcome to the Future: Join us in building digital sovereignty."
        ],
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
    """Sintetiza audios en Español o Inglés con ecualización FM 48kHz y prosodia calibrada."""
    print(f"\n[FASE 1/5 - {lang.upper()}] Sintetizando locuciones con SovereignProsodyEngine...")
    for idx, item in enumerate(BILINGUAL_MODULES):
        master_aac = RUNTIME / f"{lang}_master_{idx}.aac"
        text_content = item["text_es"] if lang == "es" else item["text_en"]
        await prosody_engine.synthesize_audio(text_content, master_aac, lang=lang)
        item[f"audio_{lang}"] = str(master_aac)
        item[f"duration_{lang}"] = get_audio_duration(str(master_aac))

def extract_whisper_timestamps_for_lang(whisper_model, lang: str):
    """Extrae marcas de tiempo de Whisper forzando las palabras canónicas exactas."""
    print(f"\n[FASE 2/5 - {lang.upper()}] Sincronizando palabras con Whisper...")
    for idx, item in enumerate(BILINGUAL_MODULES):
        audio_file = item[f"audio_{lang}"]
        canonical_text = item["text_es"] if lang == "es" else item["text_en"]
        canonical_words = canonical_text.split()

        res = whisper_model.transcribe(audio_file, language=lang, word_timestamps=True)
        raw_words = []
        for segment in res.get("segments", []):
            for w in segment.get("words", []):
                raw_words.append(w)

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
            dur = item[f"duration_{lang}"]
            step = dur / max(1, num_can)
            for i, c_word in enumerate(canonical_words):
                words_timed.append({
                    "word": c_word,
                    "start": i * step,
                    "end": (i + 1) * step
                })

        item[f"words_timed_{lang}"] = words_timed
        print(f"  [OK] Módulo {item['num']}: {len(words_timed)} palabras sincronizadas.")

def render_masterclass_for_language(lang: str, whisper_model):
    print("=" * 60)
    print(f"  [RENDER] RENDERIZANDO MASTERCLASS OPENCLAW ({lang.upper()}) 1080P")
    print("=" * 60)

    # 1. Sintetizar audios
    asyncio.run(synthesize_language_audios(lang))

    # 2. Marcas de tiempo de Whisper
    extract_whisper_timestamps_for_lang(whisper_model, lang)

    # 3. Ensamblar pista continua con pausas calibradas de 1.0s
    print(f"\n[FASE 3/5 - {lang.upper()}] Ensamblando pista de audio maestra...")
    pause_aac = RUNTIME / f"pause_10s_{lang}.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
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

    # 4. Cargar Avatar PNG transparente
    avatar_src = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    # Fuentes
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
        font_title = ImageFont.truetype("arialbd.ttf", 40)
        font_concept = ImageFont.truetype("arialbd.ttf", 24)
        font_bullet = ImageFont.truetype("arial.ttf", 22)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 42)
        font_sub = ImageFont.truetype("ariali.ttf", 22)
        font_top = ImageFont.truetype("arialbd.ttf", 20)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_bullet = ImageFont.load_default()
        font_karaoke = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_top = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in BILINGUAL_MODULES:
        t_start = curr_t
        t_end = curr_t + item[f"duration_{lang}"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.0

    frames_dir = RUNTIME / f"temp_frames_{lang}"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 4/5 - {lang.upper()}] Renderizando {total_frames} fotogramas 1080p...")

    WORDS_PER_CHUNK = 9

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

        # 1. Fondo Cósmico Continuo
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior
        draw.line([60, 50, WIDTH - 60, 50], fill=(212, 175, 55), width=1)
        draw.text((60, 20), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        top_sub = "·   PODCAST MASTERCLASS: SOBERANÍA & COMERCIO GLOBAL" if lang == "es" else "·   PODCAST MASTERCLASS: SOVEREIGNTY & GLOBAL TRADE"
        draw.text((430, 20), top_sub, font=font_top, fill=(190, 200, 220))
        top_std = "ESTÁNDAR R^768 · $0 LICENCIAS" if lang == "es" else "STANDARD R^768 · $0 LICENSES"
        draw.text((1560, 20), top_std, font=font_top, fill=(100, 220, 150))

        # 2. Lado Izquierdo: Avatar con micro-respiración
        av_float_y = int(math.sin(t * 1.4) * 4)
        av_x = 30
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Identificación de Guillermo
        draw.text((70, 75), "GUILLERMO · OPENCLAW FOUNDER", font=font_badge, fill=(255, 255, 255))
        role_label = "Arquitectura Soberana & Comercio B2B" if lang == "es" else "Sovereign Architecture & Global B2B"
        draw.text((70, 102), role_label, font=font_concept, fill=(212, 175, 55))

        # 3. Lado Derecho: Contenido Jerárquico en Balas (Breakdown)
        content_x = 640
        content_y = 80
        content_w = 1220

        badge_text = f"MÓDULO {item['num']} · {item['badge_es']}" if lang == "es" else f"MODULE {item['num']} · {item['badge_en']}"
        draw.text((content_x, content_y), badge_text, font=font_badge, fill=(212, 175, 55))

        title_text = item["title_es"] if lang == "es" else item["title_en"]
        draw.text((content_x, content_y + 35), title_text, font=font_title, fill=(255, 255, 255))

        concept_text = "⚡ " + (item["concept_es"] if lang == "es" else item["concept_en"])
        draw.text((content_x, content_y + 90), concept_text, font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 130, content_x + content_w, content_y + 130], fill=(45, 60, 90), width=1)

        # Visual Bullets en Pantalla (Breakdown con Sangría de 24px)
        bullets_list = item["bullets_es"] if lang == "es" else item["bullets_en"]
        b_y = content_y + 145
        for b_str in bullets_list:
            draw.text((content_x + 20, b_y), b_str, font=font_bullet, fill=(220, 230, 245))
            b_y += 38

        draw.line([content_x, b_y + 10, content_x + content_w, b_y + 10], fill=(45, 60, 90), width=1)

        # 4. Teleprompter Karaoke al Milisegundo
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
        cursor_y = b_y + 35
        line_height = 60
        max_line_w = content_w - 40

        for w_local_idx, w_data in enumerate(current_chunk):
            global_idx = chunk_start + w_local_idx
            word_str = w_data["word"] + " "
            bbox = font_karaoke.getbbox(word_str)
            w_width = bbox[2] - bbox[0]

            if cursor_x + w_width > content_x + max_line_w:
                cursor_x = content_x
                cursor_y += line_height

            draw.text((cursor_x + 2, cursor_y + 2), word_str, font=font_karaoke, fill=(0, 0, 0))

            if global_idx == active_w_idx:
                w_color = (255, 215, 0)
            elif global_idx < active_w_idx:
                w_color = (245, 248, 255)
            else:
                w_color = (110, 125, 150)

            draw.text((cursor_x, cursor_y), word_str, font=font_karaoke, fill=w_color)
            cursor_x += w_width

        # 5. Subtítulo en Base Flotante
        draw.line([content_x, HEIGHT - 105, content_x + content_w, HEIGHT - 105], fill=(45, 60, 90), width=1)
        sub_str = "EN: " + item["sub_en"] if lang == "es" else "ES: " + item["concept_es"]
        draw.text((content_x + 1, HEIGHT - 80 + 1), sub_str, font=font_sub, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 80), sub_str, font=font_sub, fill=(160, 190, 230))

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 600 == 0:
            print(f"    -> [{lang.upper()}] Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 6. Codificación Final en MP4 FastStart 1080p
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
    video_es = render_masterclass_for_language("es", whisper_model)
    video_en = render_masterclass_for_language("en", whisper_model)

    print("\n" + "=" * 60)
    print("  [OK] AMBAS MASTERCLASSES (ESPAÑOL & ENGLISH) RENDERIZADAS CON ÉXITO")
    print(f"  1. Español: {video_es}")
    print(f"  2. English: {video_en}")
    print("=" * 60)

if __name__ == "__main__":
    render_both_masterclasses()
