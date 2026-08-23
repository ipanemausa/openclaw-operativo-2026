"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS MAGNA BILINGÜE EXHAUSTIVA (10 MÓDULOS COMPLETOS)
==============================================================================
- CERO SUPRESIÓN: Incluye Geopolítica, Adopción en Colombia vs USA, Educación,
  Empresas (Micro/Medianas/Grandes), Agro-Exportación Alibaba (Jack Ma),
  Ecosistemas Americanos (OpenAI/Anthropic), Ecosistema Chino Open-Weight,
  Hardware NVIDIA (Omniverse/Atención) y Alianzas MinTIC / Ruta N / EAFIT.
- Voz Calibrada de Guillermo: Barítono Paisa (100.87 Hz, 48kHz Stereo EBU R128)
- Formato Podcast Anchor: Balas con Sangría 24px + Subtítulos Karaoke Sincronizados
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

sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame
from sovereign_audio_prosody_engine import SovereignProsodyEngine

# ─── LOS 10 MÓDULOS COMPLETOS SIN OMISIÓN DE NINGÚN CONCEPTO HISTÓRICO ──────

BILINGUAL_MODULES = [
    {
        "num": "01",
        "badge_es": "VISIÓN & IDENTIDAD",
        "badge_en": "SOVEREIGN IDENTITY",
        "title_es": "La Autenticidad de la Voz y la Soberanía Tecnológica",
        "title_en": "Authentic Voice & Technological Sovereignty",
        "concept_es": "Identidad del Fundador y Cero Costo en Licencias de Software",
        "concept_en": "Founder Identity & Zero SaaS Tax via Open-Weight Models",
        "bullets_es": [
            "• Identidad Vocal: La voz humana como firma biométrica inconfundible.",
            "• Soberanía Digital: Competir globalmente sin pagar rentas en dólares.",
            "• Arquitectura Soberana: Control absoluto de los datos en servidores propios."
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
        "badge_es": "GEOPOLÍTICA & ADOPCIÓN",
        "badge_en": "GEOPOLITICS & ADOPTION",
        "title_es": "La Ventaja Estratégica de Colombia y la Adopción de IA",
        "title_en": "Colombia's Strategic Edge & High AI Adoption Momentum",
        "concept_es": "Libre Conexión con Oriente y Occidente + Mayor Apertura que en USA",
        "concept_en": "Dual Access to US & Chinese AI + Higher Receptivity than Developed Nations",
        "bullets_es": [
            "• Posición Bioceánica: Colombia como puente neutral entre América, Asia y Europa.",
            "• Doble Acceso: Capacidad única de orquestar modelos americanos y modelos chinos abiertos.",
            "• Alta Adopción: En Colombia hay avidez y entusiasmo por la IA, frente al escepticismo de países desarrollados."
        ],
        "bullets_en": [
            "• Bioceanic Hub: Colombia as a neutral bridge connecting the Americas, Asia, and Europe.",
            "• Dual Access: Unique capability to orchestrate American models and Chinese open-weight models.",
            "• Rapid Adoption: Colombia exhibits high enthusiasm for AI compared to skepticism in developed nations."
        ],
        "text_es": "Colombia cuenta con una ventaja geopolítica excepcional: nuestra posición bioceánica y neutralidad nos permite conectar libremente tanto con los ecosistemas de Estados Unidos como con los modelos de código abierto de China. Además, mientras en países desarrollados e incluso en Estados Unidos existe repulsión o miedo regulatorio hacia la adopción, en Colombia los jóvenes y empresarios tienen un apetito enorme por aprender y transformar sus negocios con inteligencia artificial.",
        "text_en": "Colombia holds an exceptional geopolitical advantage: our bioceanic position and neutrality allow us to connect seamlessly with both US proprietary ecosystems and Chinese open-weight models. Furthermore, while developed nations and parts of the United States face regulatory hesitation, in Colombia students and entrepreneurs possess a powerful drive to adopt AI and transform their industries.",
        "sub_en": "Colombia's bioceanic neutrality enables dual orchestration of US and Chinese AI with rapid adoption."
    },
    {
        "num": "03",
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
        "num": "04",
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
        "num": "05",
        "badge_es": "MODELOS OPEN-WEIGHT",
        "badge_en": "OPEN-WEIGHT FRONTIER",
        "title_es": "Ecosistema Oriental: DeepSeek, Qwen, GLM, Kimi y Yi",
        "title_en": "Leading Asian Open Models: DeepSeek, Qwen, GLM, Kimi & Yi",
        "concept_es": "Soberanía Tecnológica Absoluta con Modelos de Código Abierto",
        "concept_en": "Absolute Technological Sovereignty Powered by Open-Weight Models",
        "bullets_es": [
            "• DeepSeek-R1 & V3: Razonamiento abierto de nivel frontera a $0 licencias.",
            "• Alibaba Qwen 2.5: Excelencia multilingüe, matemáticas y orquestación B2B.",
            "• Zhipu GLM-4, Moonshot Kimi & 01.AI Yi-Lightning: Motores globales de alta fidelidad."
        ],
        "bullets_en": [
            "• DeepSeek-R1 & V3: Frontier open reasoning matching proprietary models at zero license cost.",
            "• Alibaba Qwen 2.5: Multilingual mastery, advanced mathematics, and enterprise B2B orchestration.",
            "• Zhipu GLM-4, Moonshot Kimi & 01.AI Yi-Lightning: Global high-throughput open engines."
        ],
        "text_es": "Asimismo, integramos los motores de código abierto más avanzados de Oriente. En DeepSeek contamos con DeepSeek-R1 y V3 para razonamiento matemático puro. En Alibaba Cloud disponemos de Qwen 2.5. En Zhipu AI integramos GLM-4. En Moonshot AI aprovechamos Kimi para ventanas de contexto masivas. Y en cero uno punto a-i utilizamos Yi-Lightning de Kai-Fu Lee. Esto garantiza que nuestras empresas nunca queden atrapadas en monopolios cerrados.",
        "text_en": "Likewise, we integrate top open-weight engines from Asia: DeepSeek with DeepSeek-R1 and V3 for pure mathematical logic. Alibaba Cloud with Qwen 2.5. Zhipu AI with GLM-4. Moonshot AI with Kimi for massive context windows. And 01.AI with Yi-Lightning. This guarantees that our enterprises are never locked into foreign monopolies.",
        "sub_en": "Full open-weight stack: DeepSeek-R1, Qwen 2.5, GLM-4, Kimi, and Yi-Lightning at zero software cost."
    },
    {
        "num": "06",
        "badge_es": "HARDWARE & WORLD MODELS",
        "badge_en": "HARDWARE & WORLD MODELS",
        "title_es": "NVIDIA Omniverse, Chips Multimodales y Modelos de Mundo",
        "title_en": "NVIDIA Omniverse, Multimodal Chips & World Models",
        "concept_es": "Mecanismo de Atención, Reconstrucción 4K y Simulación Espacial 3D",
        "concept_en": "Attention Mechanisms, Neural 4K DLSS & 3D Spatial Simulation",
        "bullets_es": [
            "• Mecanismo de Atención: Matrices de relevancia semántica token a token en espacio latente.",
            "• Especialización de Chips: Tensor Cores acelerando visión, audio y lenguaje simultáneamente.",
            "• World Models (Fei-Fei Li & Omniverse): Gemelos digitales 3D con física y luz real en 1080p."
        ],
        "bullets_en": [
            "• Attention Mechanism: Semantic token-to-token relationships in latent mathematical space.",
            "• Multimodal Chips: Specialized Tensor Cores accelerating computer vision, speech, and text.",
            "• World Models (Fei-Fei Li & Omniverse): 3D digital twins with real-world physical ray tracing."
        ],
        "text_es": "Como demuestra Jensen Huang, el hardware de NVIDIA no solo procesa datos; simula la física del mundo real. El mecanismo de atención permite a los Transformers entender la relación profunda entre cada palabra. Con NVIDIA Omniverse y los modelos de mundo de la doctora Fei-Fei Li, creamos gemelos digitales de productos con física de luz real y renderizado neuronal en tiempo real.",
        "text_en": "As Jensen Huang demonstrates, NVIDIA hardware simulates physical reality. The attention mechanism enables Transformers to calculate semantic relationships across every word. Pairing NVIDIA Omniverse with Doctor Fei-Fei Li's spatial world models allows us to render 3D product digital twins with physical ray tracing in real time.",
        "sub_en": "Simulating physical reality with NVIDIA attention mechanisms, Omniverse, and 3D world models."
    },
    {
        "num": "07",
        "badge_es": "EDUCACIÓN & JÓVENES",
        "badge_en": "EDUCATION & TALENT",
        "title_es": "Democratización Educativa y Neuroplasticidad Aplicada",
        "title_en": "Educational Democratization & Applied Neuroplasticity",
        "concept_es": "Capacitación Real en Lógica y Arquitectura sin Barreras Económicas",
        "concept_en": "Empowering Students with Logic, Architecture & Zero Software Cost",
        "bullets_es": [
            "• Acceso Universal: Estudiantes aprenden sobre modelos abiertos sin costo de suscripción.",
            "• Neuroplasticidad: Estimulación del razonamiento lógico y resolución de problemas reales.",
            "• Formación de Élite: Preparar a la juventud en ingeniería de datos y orquestación de IA."
        ],
        "bullets_en": [
            "• Universal Access: Students master open models with zero subscription barriers.",
            "• Neuroplasticity: Fostering deep logical reasoning and real-world problem solving.",
            "• Elite Training: Preparing the next generation in data engineering and AI orchestration."
        ],
        "text_es": "Nuestro compromiso con la educación es total. Los jóvenes y estudiantes de Colombia no pueden quedarse como simples consumidores de tecnología; deben ser creadores. Con OpenClaw les entregamos un laboratorio abierto donde aprenden arquitectura de datos, lógica de sistemas y neuroplasticidad aplicada, sin que una tarjeta de crédito o una suscripción extranjera limite su potencial de aprendizaje.",
        "text_en": "Our commitment to education is foundational. Students and youth must not remain passive consumers; they must become creators. Through OpenClaw we deliver an open laboratory where they master data architecture, logic, and applied neuroplasticity, without credit card barriers or foreign subscriptions limiting their potential.",
        "sub_en": "Democratizing AI education for students through open architecture and applied logic."
    },
    {
        "num": "08",
        "badge_es": "EMPRESARIOS & COMERCIO",
        "badge_en": "ENTERPRISE & SMES",
        "title_es": "Modernización para Micro, Medianas y Grandes Empresas",
        "title_en": "Modernization for Micro, Medium & Enterprise Businesses",
        "concept_es": "Bases de Datos Vectoriales R^768 y Automatización Comercial B2B",
        "concept_en": "R^768 Vector Memory & Automated B2B Commercial Workflows",
        "bullets_es": [
            "• Comerciantes & Microempresas: Catálogos e inventarios digitalizados en minutos.",
            "• Medianas & Grandes Industrias: Bases vectoriales privadas para cotizaciones automáticas.",
            "• $0 Licencias: Reinvertir el ahorro de software en crecimiento y contratación local."
        ],
        "bullets_en": [
            "• Merchants & Small Business: Product catalogs and inventories digitized in minutes.",
            "• Medium & Large Enterprise: Private vector databases powering automated quotes.",
            "• Zero Licensing Tax: Reinvesting software savings into growth and local talent."
        ],
        "text_es": "Para los empresarios —desde el comerciante de mostrador hasta la mediana y gran industria— OpenClaw representa un salto de productividad gigantesco. Tomamos sus catálogos, inventarios y listas de precios, y los convertimos en bases de datos vectoriales en espacio R 768. Sus clientes reciben cotizaciones instantáneas y atención veinticuatro siete con agentes inteligentes, eliminando costos recurrentes de software.",
        "text_en": "For businesses—from local retail merchants to mid-sized and large enterprises—OpenClaw provides a quantum leap in productivity. We convert product catalogs, inventories, and pricing matrices into 768-dimensional vector memory. Customers receive instant automated quotes 24/7 through intelligent agents at zero recurring software overhead.",
        "sub_en": "Upgrading retail, SMEs, and large enterprise with instant automated vector quoting."
    },
    {
        "num": "09",
        "badge_es": "AGRO & EXPORTACIÓN",
        "badge_en": "AGRICULTURE & TRADE",
        "title_es": "Exportar a China: El Partnership Estratégico con Alibaba",
        "title_en": "Exporting to China: Strategic Partnership with Alibaba",
        "concept_es": "Café, Cacao y Esmeraldas Directo a las 120 Megaciudades de Jack Ma",
        "concept_en": "Colombian Coffee, Cacao & Emeralds Directly to China's 120 Megacities",
        "bullets_es": [
            "• La Tesis de Jack Ma: China como el mayor importador mundial en 120 megaciudades.",
            "• Alianza con Alibaba Cloud: Vitrina digital B2B directa sin intermediarios abusivos.",
            "• Video en Mandarín: Promoción de café especial, cacao y gemología con avatares IA."
        ],
        "bullets_en": [
            "• Jack Ma's Vision: China as the top global importer across 120 planned megacities.",
            "• Alibaba Cloud Bridge: Direct B2B digital storefront eliminating predatory middlemen.",
            "• Mandarin AI Video: Promoting specialty coffee, cacao, and emeralds with AI avatars."
        ],
        "text_es": "En el sector agrícola y exportador, aplicamos la visión de Jack Ma: China dejó de ser solo la fábrica del mundo y hoy es el mayor importador global, impulsada por ciento veinte megaciudades de alto consumo. A través de nuestra integración con Alibaba Cloud y Alibaba punto com, conectamos directamente a los productores de café especial, cacao, esmeraldas y joyería con compradores mayoristas en China, promocionando sus cosechas con videos y agentes en Mandarín.",
        "text_en": "For agriculture and exporters, we implement Jack Ma's core insight: China is now the world's leading importer across 120 planned megacities. By partnering through Alibaba Cloud and Alibaba.com, we connect Colombian producers of specialty coffee, cacao, and emeralds directly to Chinese wholesale buyers, marketing their products with multilingual video and AI agents.",
        "sub_en": "Empowering Colombian agriculture and mining exporters to reach China's 120 megacities via Alibaba."
    },
    {
        "num": "10",
        "badge_es": "ALIANZA & CIERRE",
        "badge_en": "NATIONAL ALLIANCE",
        "title_es": "Articulación con MinTIC, Ruta N, Universidad EAFIT y Futuro",
        "title_en": "Alliance with MinTIC, Ruta N, EAFIT University & The Future",
        "concept_es": "Soberanía Tecnológica Nacional y Código 100% Verificable",
        "concept_en": "National Tech Sovereignty Powered by Real, Production Code",
        "bullets_es": [
            "• MinTIC & Ruta N: Reducir la fuga de capitales y construir soberanía digital en Colombia.",
            "• Universidad EAFIT: Alianza académica para formación práctica de ingeniería de vanguardia.",
            "• Bienvenidos al Futuro: Construyamos soberanía digital con hechos y código real."
        ],
        "bullets_en": [
            "• MinTIC & Ruta N: Retaining domestic capital and building sovereign digital capacity.",
            "• EAFIT University: Academic partnership for practical frontier engineering education.",
            "• Welcome to the Future: Join us in building digital sovereignty with real code."
        ],
        "text_es": "Esta arquitectura está lista para articularse con MinTIC, el Ministerio de Comercio, Ruta N y la Universidad EAFIT. No venimos a pedir presupuestos para licencias extranjeras; venimos a entregar una plataforma soberana que capacita a miles de jóvenes, moderniza a nuestras industrias y potencia las exportaciones colombianas hacia el mundo. Los invito a construir el futuro con nosotros. Bienvenidos a OpenClaw dos mil veintiséis.",
        "text_en": "This architecture is ready to partner with MinTIC, the Ministry of Commerce, Ruta N, and EAFIT University. We do not consume budgets on foreign software licenses; we deliver a sovereign platform that trains youth, modernizes industry, and accelerates Colombian exports worldwide. Join us in building the future. Welcome to OpenClaw 2026.",
        "sub_en": "Partnering with MinTIC, Ruta N, and EAFIT University to lead sovereign AI. Welcome to OpenClaw."
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
    print(f"\n[FASE 1/5 - {lang.upper()}] Sintetizando 10 módulos con la voz calibrada de Guillermo...")
    for idx, item in enumerate(BILINGUAL_MODULES):
        master_aac = RUNTIME / f"{lang}_master_{idx}.aac"
        text_content = item["text_es"] if lang == "es" else item["text_en"]
        await prosody_engine.synthesize_audio(text_content, master_aac, lang=lang)
        item[f"audio_{lang}"] = str(master_aac)
        item[f"duration_{lang}"] = get_audio_duration(str(master_aac))

def extract_whisper_timestamps_for_lang(whisper_model, lang: str):
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
    print(f"  [RENDER] RENDERIZANDO MASTERCLASS MAGNA OPENCLAW ({lang.upper()}) 1080P")
    print("=" * 60)

    asyncio.run(synthesize_language_audios(lang))
    extract_whisper_timestamps_for_lang(whisper_model, lang)

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

    avatar_src = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)

    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_concept = ImageFont.truetype("arialbd.ttf", 24)
        font_bullet = ImageFont.truetype("arial.ttf", 22)
        font_karaoke = ImageFont.truetype("arialbd.ttf", 40)
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

        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior
        draw.line([60, 50, WIDTH - 60, 50], fill=(212, 175, 55), width=1)
        draw.text((60, 20), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        top_sub = "·   PODCAST MASTERCLASS MAGNA: GEOPOLÍTICA, EDUCACIÓN & COMERCIO GLOBAL" if lang == "es" else "·   MAGNA PODCAST MASTERCLASS: GEOPOLITICS, EDUCATION & GLOBAL TRADE"
        draw.text((430, 20), top_sub, font=font_top, fill=(190, 200, 220))
        top_std = "ESTÁNDAR R^768 · $0 LICENCIAS" if lang == "es" else "STANDARD R^768 · $0 LICENSES"
        draw.text((1560, 20), top_std, font=font_top, fill=(100, 220, 150))

        # Avatar Izquierdo
        av_float_y = int(math.sin(t * 1.4) * 4)
        av_x = 30
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        draw.text((70, 75), "GUILLERMO · OPENCLAW FOUNDER", font=font_badge, fill=(255, 255, 255))
        role_label = "Arquitectura Soberana & Comercio B2B" if lang == "es" else "Sovereign Architecture & Global B2B"
        draw.text((70, 102), role_label, font=font_concept, fill=(212, 175, 55))

        # Contenido Derecho en Balas
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

        bullets_list = item["bullets_es"] if lang == "es" else item["bullets_en"]
        b_y = content_y + 145
        for b_str in bullets_list:
            draw.text((content_x + 20, b_y), b_str, font=font_bullet, fill=(220, 230, 245))
            b_y += 38

        draw.line([content_x, b_y + 10, content_x + content_w, b_y + 10], fill=(45, 60, 90), width=1)

        # Karaoke al milisegundo
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

        # Subtítulo Base
        draw.line([content_x, HEIGHT - 105, content_x + content_w, HEIGHT - 105], fill=(45, 60, 90), width=1)
        sub_str = "EN: " + item["sub_en"] if lang == "es" else "ES: " + item["concept_es"]
        draw.text((content_x + 1, HEIGHT - 80 + 1), sub_str, font=font_sub, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 80), sub_str, font=font_sub, fill=(160, 190, 230))

        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 800 == 0:
            print(f"    -> [{lang.upper()}] Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # Codificación FastStart MP4
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
    print("  [OK] AMBAS MASTERCLASSES MAGNAS (10 MÓDULOS) RENDERIZADAS CON ÉXITO")
    print(f"  1. Español: {video_es}")
    print(f"  2. English: {video_en}")
    print("=" * 60)

if __name__ == "__main__":
    render_both_masterclasses()
