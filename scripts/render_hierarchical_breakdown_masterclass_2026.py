"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS JERÁRQUICA EN BREAKDOWN CON VOZ CALIBRADA
==============================================================================
- Estructura Visual: BREAKDOWN JERÁRQUICO CON SANGRÍA (Sin párrafos densos con comas)
- Modelos Americanos & Chinos: Agrupados por Empresa con sub-modelos indentados
- Fonética Impecable: Nombres chinos y americanos pronunciados en inglés puro
- Cadencia: Pausada (-10% rate) con respiración natural entre empresas (1.0s)
- Avatar: Insignia HB.OS bordada en los píxeles de la tela (Cero capas desfasadas)
- Visual: Universo Cósmico Seamless Continuo (180 estrellas con paralaje)
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
RUNTIME = ROOT / "runtime" / "masterclass_breakdown_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame

# ─── MÓDULOS EN BREAKDOWN JERÁRQUICO ESTRUCTURADO ─────────────────────────────

HIERARCHICAL_MODULES = [
    {
        "num": "01",
        "badge": "VISIÓN SOBERANA",
        "title": "La Verdadera Soberanía en Inteligencia Artificial",
        "concept": "Arquitectura Abierta a Costo Cero para Empresas y Estudiantes",
        "speech_text": "Hola a todos, les habla Guillermo. Bienvenidos a OpenClaw. Durante años, a las empresas y a los estudiantes les dijeron que para usar inteligencia artificial debían pagar costosas licencias mensuales en dólares. Hoy demostramos que con rigor, código abierto y arquitectura soberana, podemos competir al más alto nivel mundial a costo cero de licencias.",
        "display_lines": [
            ("TITLE", "ARQUITECTURA SOBERANA A COSTO CERO"),
            ("BULLET", "• Independencia Total de Licencias Propietarias en Dólares"),
            ("BULLET", "• Orquestación Híbrida de Modelos Abiertos y Cerrados"),
            ("BULLET", "• Gobernanza Privada de Datos en Infraestructura Propia")
        ],
        "sub_en": "Welcome. We demonstrate sovereign AI architecture built on open models at zero licensing fees."
    },
    {
        "num": "02",
        "badge": "SÍNTESIS HUANG-AMODEI",
        "title": "Jensen Huang y Dario Amodei: La Fuerza Resultante",
        "concept": "Escalamiento Masivo de Cómputo + Guardrails Estrictos de Seguridad",
        "speech_text": "En la vanguardia mundial conviven dos visiones fundamentales. Jensen Huang de NVIDIA impulsa el escalamiento masivo del cómputo. Dario Amodei de Anthropic exige seguridad estricta y contención de riesgos. Nuestra arquitectura une ambas fuerzas: aceleramos el procesamiento distribuido, protegiendo al cien por ciento la privacidad de nuestros datos con Guardrails deterministas.",
        "display_lines": [
            ("TITLE", "SÍNTESIS DIALÉCTICA HUANG - AMODEI"),
            ("HEADER", "1. Jensen Huang · NVIDIA:"),
            ("INDENT", "   → Escalamiento masivo de cómputo y aceleración por hardware"),
            ("HEADER", "2. Dario Amodei · Anthropic:"),
            ("INDENT", "   → Seguridad innegociable y Guardrails de contención de riesgos"),
            ("HEADER", "3. HB.OS Resultante:"),
            ("INDENT", "   → Cómputo acelerado con privacidad absoluta y datos blindados")
        ],
        "sub_en": "Synthesizing Jensen Huang's compute scaling with Dario Amodei's safety guardrails."
    },
    {
        "num": "03",
        "badge": "MODELOS AMERICANOS",
        "title": "Catálogo Exhaustivo: Ecosistema de Estados Unidos",
        "concept": "Orquestación Multi-Proveedor de Motores Americanos",
        "speech_text": "Nuestra plataforma se conecta de forma nativa con los principales modelos de Estados Unidos. En OpenAI: GPT-4o, GPT-4o mini, o1, o3-mini, DALL·E 3, Sora y Whisper. En Google DeepMind: Gemini 2.0 Flash, Gemini 1.5 Pro, Imagen 3 y Gemma 2. En Anthropic: Claude 3.5 Sonnet, Claude 3.5 Haiku y Claude 3 Opus. En Meta: Llama 3.1, 3.2 y 3.3. En xAI: Grok-2 y Grok-3. Y motores empresariales como Command R+ de Cohere y Amazon Nova.",
        "display_lines": [
            ("TITLE", "AMERICAN ARTIFICIAL INTELLIGENCE MATRIX"),
            ("HEADER", "• OpenAI:"),
            ("INDENT", "   GPT-4o  ·  GPT-4o mini  ·  o1  ·  o3-mini  ·  DALL·E 3  ·  Sora  ·  Whisper"),
            ("HEADER", "• Google DeepMind:"),
            ("INDENT", "   Gemini 2.0 Flash  ·  Gemini 1.5 Pro  ·  Imagen 3  ·  Gemma 2"),
            ("HEADER", "• Anthropic:"),
            ("INDENT", "   Claude 3.5 Sonnet  ·  Claude 3.5 Haiku  ·  Claude 3 Opus"),
            ("HEADER", "• Meta & xAI:"),
            ("INDENT", "   Llama 3.1 / 3.2 / 3.3  ·  Grok-2  ·  Grok-3"),
            ("HEADER", "• Enterprise Deployments:"),
            ("INDENT", "   Cohere Command R+  ·  Amazon Nova (Titan / Nova Pro)")
        ],
        "sub_en": "Full orchestration of American AI: OpenAI, Gemini 2.0, Claude 3.5, Llama 3.3, Grok-3 and Cohere."
    },
    {
        "num": "04",
        "badge": "MODELOS CHINOS",
        "title": "Catálogo Exhaustivo: Ecosistema Abierto de Oriente",
        "concept": "Modelos Abiertos de Asia con Fonética Original en Inglés",
        "speech_text": "Asimismo, integramos los motores más potentes de Oriente. En DeepSeek: DeepSeek-V3, DeepSeek-R1, DeepSeek-Coder y DeepSeek-VL. En Alibaba Cloud: Qwen 2.5, Qwen-VL y Qwen-Max. En Baidu: Ernie Bot y Ernie 4.0 Turbo. En Zhipu AI: ChatGLM, GLM-4 y GLM-4-Voice. En Tencent: Hunyuan Video y Hunyuan Large. En Moonshot AI: Kimi. En 01.AI: Yi-Lightning, Yi-1.5 y Yi-Large de Kai-Fu Lee. En SenseTime: SenseNova. Y en MiniMax: abab 6.5 y Hailuo AI.",
        "display_lines": [
            ("TITLE", "CHINESE OPEN-WEIGHT AI MATRIX"),
            ("HEADER", "• DeepSeek:"),
            ("INDENT", "   DeepSeek-V3  ·  DeepSeek-R1  ·  DeepSeek-Coder  ·  DeepSeek-VL"),
            ("HEADER", "• Alibaba Cloud:"),
            ("INDENT", "   Qwen 2.5 (Tongyi Qianwen)  ·  Qwen-VL  ·  Qwen-Max"),
            ("HEADER", "• Baidu & Zhipu AI:"),
            ("INDENT", "   Ernie Bot (Ernie 4.0 Turbo)  ·  ChatGLM  ·  GLM-4  ·  GLM-4-Voice"),
            ("HEADER", "• Tencent & Moonshot AI:"),
            ("INDENT", "   Hunyuan (Hunyuan Video / Large)  ·  Kimi (Moonshot v1)"),
            ("HEADER", "• 01.AI, SenseTime & MiniMax:"),
            ("INDENT", "   Yi-Lightning  ·  Yi-Large  ·  SenseNova  ·  abab 6.5  ·  Hailuo AI")
        ],
        "sub_en": "Full orchestration of Chinese AI: DeepSeek-R1, Qwen 2.5, GLM-4, Hunyuan, Kimi and Yi-Lightning."
    },
    {
        "num": "05",
        "badge": "VENTAJA COMPARATIVA",
        "title": "La Ventaja Estratégica de Colombia y Latinoamérica",
        "concept": "Libre Acceso a Oriente y Occidente sin Barreras Geopolíticas",
        "speech_text": "Aquí radica nuestra ventaja objetiva: la población en China está restringida por el estado para usar modelos americanos, y en Estados Unidos hay barreras regulatorias crecientes contra los modelos chinos. En Colombia y Latinoamérica tenemos la libertad de usar lo mejor de ambos mundos, combinando la visión estratégica de Claude y Gemini con la potencia abierta y a costo cero de DeepSeek y Qwen.",
        "display_lines": [
            ("TITLE", "VENTAJA COMPARATIVA GEOPOLÍTICA"),
            ("HEADER", "• Restricción en China:"),
            ("INDENT", "   Bloqueo estatal al uso de modelos americanos de frontera"),
            ("HEADER", "• Restricción en Estados Unidos:"),
            ("INDENT", "   Barreras geopolíticas crecientes contra modelos abiertos chinos"),
            ("HEADER", "• Ventaja Soberana de Colombia & LATAM:"),
            ("INDENT", "   Libre acceso simultáneo a lo mejor de Oriente y Occidente sin fricción")
        ],
        "sub_en": "Latin America uniquely accesses both Western intelligence and Asian open-weight power without barriers."
    },
    {
        "num": "06",
        "badge": "GEOPOLÍTICA REGIONAL",
        "title": "Colombia: Nodo Bioceánico y Capital del Talento",
        "concept": "Dos Océanos, Puerta a Suramérica y Alta Velocidad de Adopción",
        "speech_text": "Colombia cuenta con una ubicación bioceánica privilegiada entre el Pacífico y el Atlántico, cercanía con Norteamérica y entrada a Suramérica. Pero lo más valioso es que nuestra gente tiene un interés y una velocidad de adopción de la inteligencia artificial superior a la de muchos países desarrollados. El momento de liderar la transformación productiva es ahora.",
        "display_lines": [
            ("TITLE", "COLOMBIA: NODO ESTRATÉGICO CONTINENTAL"),
            ("BULLET", "• Posición Bioceánica: Conexión simultánea con el Pacífico y el Atlántico"),
            ("BULLET", "• Puerta de Entrada: Bisagra comercial entre Norteamérica y Suramérica"),
            ("BULLET", "• Capital Humano: Velocidad y receptividad de adopción de IA de vanguardia")
        ],
        "sub_en": "Colombia's bioceanic location and rapid AI adoption make it the natural technology hub for the Americas."
    },
    {
        "num": "07",
        "badge": "ECOSISTEMA NACIONAL",
        "title": "Alianza con MinTIC, Ruta N y Universidades como EAFIT",
        "concept": "Democratización para Estudiantes, PYMEs y Grandes Industrias",
        "speech_text": "Nuestra plataforma está lista para articularse con MinTIC, centros de innovación como Ruta N y universidades líderes como EAFIT. No venimos a gastar presupuestos en licencias propietarias cerradas; venimos a transferir una arquitectura soberana que capacita a miles de jóvenes y moderniza a nuestras empresas con bases de datos vectoriales Qdrant y Guardrails de seguridad.",
        "display_lines": [
            ("TITLE", "ARTICULACIÓN NACIONAL PÚBLICO-PRIVADA"),
            ("HEADER", "• Ministerio MinTIC:"),
            ("INDENT", "   Transferencia de metodología soberana para capacitación masiva"),
            ("HEADER", "• Centros de Innovación (Ruta N):"),
            ("INDENT", "   Aceleración productiva de PYMEs y modernización de industrias"),
            ("HEADER", "• Universidades Líderes (EAFIT):"),
            ("INDENT", "   Gobernanza matemática en R^768, Qdrant y Guardrails perimetrales")
        ],
        "sub_en": "Partnering with MinTIC, Ruta N and EAFIT to train youth and upgrade industry with Qdrant and Guardrails."
    },
    {
        "num": "08",
        "badge": "LLAMADO A LA ACCIÓN",
        "title": "Construyendo el Futuro con Hechos Verificables",
        "concept": "Disciplina, Soberanía Tecnológica y Sistema HB.OS",
        "speech_text": "La inteligencia artificial no es magia; es disciplina, práctica rigurosa y arquitectura técnica sólida. Con el sistema HB.OS demostramos que la soberanía digital está al alcance de todos. Todo lo que ven aquí es código real, soberano y verificado. Los invito a construir el futuro con nosotros. Bienvenidos a OpenClaw dos mil veintiséis.",
        "display_lines": [
            ("TITLE", "SOBERANÍA DIGITAL CON HECHOS VERIFICABLES"),
            ("BULLET", "• Neuroplasticidad y Disciplina: Dominio técnico mediante la práctica real"),
            ("BULLET", "• Sistema HB.OS: Cero costo de licencias, máxima potencia y blindaje"),
            ("BULLET", "• Bienvenidos a OpenClaw 2026: Construyamos la soberanía tecnológica juntos")
        ],
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

async def synthesize_hierarchical_audios():
    """Sintetiza locuciones con cadencia pausada (-10% rate) y pronunciación impecable en inglés."""
    print("\n[FASE 1/4] Sintetizando locuciones pausadas con ecualización de estudio FM 48kHz (-16 LUFS)...")
    for idx, item in enumerate(HIERARCHICAL_MODULES):
        raw_mp3 = RUNTIME / f"h_raw_{idx}.mp3"
        master_aac = RUNTIME / f"h_master_{idx}.aac"

        # Cadencia pausada (-10% rate, -2Hz pitch) para máxima claridad y elegancia
        comm = edge_tts.Communicate(item["speech_text"], voice="es-CO-GonzaloNeural", rate="-10%", pitch="-2Hz")
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
        item["audio_file"] = str(master_aac)
        item["duration"] = dur
        print(f"  [OK] Módulo {item['num']}: {dur:.2f}s | '{item['title']}'")

def render_hierarchical_masterclass():
    print("=" * 60)
    print("  [RENDER] MASTERCLASS EN BREAKDOWN JERÁRQUICO CON HB.OS (1080P)")
    print("=" * 60)

    # 1. Sintetizar audios
    asyncio.run(synthesize_hierarchical_audios())

    # 2. Ensamblar pista de audio continua con pausas naturales (1.2s)
    print("\n[FASE 2/4] Ensamblando pista de audio continua con pausas...")
    pause_aac = RUNTIME / "pause_12s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.2", "-c:a", "aac", "-b:a", "256k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    concat_txt = RUNTIME / "concat_h.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in HIERARCHICAL_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")

    master_audio = RUNTIME / "master_audio_hierarchical_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f}s ({total_duration/60:.2f} min)")

    # 3. Cargar Avatar PNG con logo HB.OS limpio en los píxeles de la camisa
    avatar_src = ROOT / "assets" / "avatar_transparent.png"
    raw_av = Image.open(avatar_src).convert("RGBA")
    av_h = 880
    av_w = int(raw_av.width * (av_h / raw_av.height))
    avatar_png = raw_av.resize((av_w, av_h), Image.Resampling.LANCZOS)
    print(f"  -> Avatar transparente cargado: {av_w}x{av_h} px")

    # Fuentes Tipográficas Jerárquicas
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_title = ImageFont.truetype("arialbd.ttf", 44)
        font_concept = ImageFont.truetype("arialbd.ttf", 24)
        font_box_title = ImageFont.truetype("arialbd.ttf", 28)
        font_header = ImageFont.truetype("arialbd.ttf", 26)
        font_indent = ImageFont.truetype("arial.ttf", 23)
        font_bullet = ImageFont.truetype("arialbd.ttf", 24)
        font_sub = ImageFont.truetype("ariali.ttf", 24)
        font_top = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_concept = ImageFont.load_default()
        font_box_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_indent = ImageFont.load_default()
        font_bullet = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_top = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in HIERARCHICAL_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.2

    frames_dir = RUNTIME / "temp_frames_h"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(total_duration * FPS)
    print(f"\n[FASE 3/4] Renderizando {total_frames} fotogramas Full HD en Breakdown Jerárquico...")

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
        progress_in_mod = t_rel / dur_mod

        # ─── 1. FONDO CÓSMICO DEL UNIVERSO EN MOVIMIENTO FLUIDO CONTINUO ───
        frame = render_cosmic_universe_frame(t)
        draw = ImageDraw.Draw(frame)

        # Barra Superior Minimalista Flotante
        draw.line([60, 60, WIDTH - 60, 60], fill=(212, 175, 55), width=1)
        draw.text((60, 24), "OPENCLAW CORE MATRIX 2026", font=font_top, fill=(212, 175, 55))
        draw.text((430, 24), "·   CATÁLOGO JERÁRQUICO DE MODELOS & GEOPOLÍTICA REGIONAL", font=font_top, fill=(190, 200, 220))
        draw.text((1560, 24), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_top, fill=(100, 220, 150))

        # ─── 2. LADO IZQUIERDO: AVATAR PNG TRANSPARENTE CON LOGO HB.OS EN TELA ───
        av_float_y = int(math.sin(t * 1.3) * 5)
        av_x = 40
        av_y = HEIGHT - av_h + av_float_y
        frame.paste(avatar_png, (av_x, av_y), avatar_png)

        # Identificación Flotante Limpia
        draw.text((80, 95), "GUILLERMO · OPENCLAW", font=font_badge, fill=(255, 255, 255))
        draw.text((80, 125), "Arquitectura Soberana HB.OS", font=font_concept, fill=(212, 175, 55))

        # ─── 3. LADO DERECHO: ESTRUCTURA EN BREAKDOWN CON SANGRÍA (SIN CAJAS CORTANTES) ───
        content_x = 620
        content_y = 95
        content_w = 1240

        # Badge del Módulo
        draw.text((content_x, content_y), f"MÓDULO {item['num']} · {item['badge']}", font=font_badge, fill=(212, 175, 55))

        # Título Grande Cinematográfico
        draw.text((content_x, content_y + 40), item["title"], font=font_title, fill=(255, 255, 255))

        # Concepto Clave
        draw.text((content_x, content_y + 100), "⚡ " + item["concept"], font=font_concept, fill=(100, 225, 185))
        draw.line([content_x, content_y + 140, content_x + content_w, content_y + 140], fill=(45, 60, 90), width=1)

        # ─── RENDERIZADO DEL BREAKDOWN JERÁRQUICO CON SANGRÍA ───
        display_lines = item["display_lines"]
        total_lines = len(display_lines)
        active_line_idx = int(progress_in_mod * total_lines)

        cursor_y = content_y + 165
        for l_idx, (line_type, line_text) in enumerate(display_lines):
            # Sombra suave detrás de cada línea para máxima legibilidad
            if line_type == "TITLE":
                draw.text((content_x + 2, cursor_y + 2), line_text, font=font_box_title, fill=(0, 0, 0))
                draw.text((content_x, cursor_y), line_text, font=font_box_title, fill=(255, 215, 0))
                cursor_y += 45
            elif line_type == "HEADER":
                h_color = (255, 225, 120) if l_idx <= active_line_idx + 1 else (160, 175, 195)
                draw.text((content_x + 2, cursor_y + 2), line_text, font=font_header, fill=(0, 0, 0))
                draw.text((content_x, cursor_y), line_text, font=font_header, fill=h_color)
                cursor_y += 36
            elif line_type == "INDENT":
                i_color = (245, 248, 255) if l_idx <= active_line_idx + 1 else (110, 125, 145)
                draw.text((content_x + 24, cursor_y + 2), line_text, font=font_indent, fill=(0, 0, 0))
                draw.text((content_x + 22, cursor_y), line_text, font=font_indent, fill=i_color)
                cursor_y += 40
            elif line_type == "BULLET":
                b_color = (255, 255, 255) if l_idx <= active_line_idx else (130, 145, 165)
                draw.text((content_x + 12, cursor_y + 2), line_text, font=font_bullet, fill=(0, 0, 0))
                draw.text((content_x + 10, cursor_y), line_text, font=font_bullet, fill=b_color)
                cursor_y += 44

        # Subtítulo en Base Flotante
        draw.line([content_x, HEIGHT - 110, content_x + content_w, HEIGHT - 110], fill=(45, 60, 90), width=1)
        draw.text((content_x + 2, HEIGHT - 85 + 2), "EN: " + item["sub_en"], font=font_sub, fill=(0, 0, 0))
        draw.text((content_x, HEIGHT - 85), "EN: " + item["sub_en"], font=font_sub, fill=(160, 190, 230))

        # Barra de Progreso Inferior en Oro
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 6, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))

        frame_file = frames_dir / f"h_frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)

        if f_idx % 600 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n[FASE 4/4] Codificando Masterclass en Breakdown con FFmpeg FastStart...")
    final_output = RUNTIME / "OpenClaw_Masterclass_Breakdown_Jerarquico_1080p.mp4"

    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "h_frame_%06d.jpg"),
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
    print("  [OK] MASTERCLASS EN BREAKDOWN JERÁRQUICO GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} min)")
    print("=" * 60)

    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()

    return str(final_output)

if __name__ == "__main__":
    render_hierarchical_masterclass()
