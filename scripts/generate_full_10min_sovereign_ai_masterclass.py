"""
==============================================================================
OPENCLAW CLOUD 2026 — MASTERCLASS MAGNA (10 MINUTOS) — RIGOR TÉCNICO B2B
==============================================================================
Tema: ARQUITECTURA HÍBRIDA DE IA SOBERANA, GOBERNANZA VECTORIAL Y GEOPOLÍTICA
Público Objetivo: MinTIC, Ruta N, EAFIT, Universidades, PYMEs y Corporaciones B2B
Rigor: Anti-Humo / 100% Verificable / Síntesis Huang-Amodei / Modelo Geopolítico
==============================================================================
"""

import os
import sys
import json
import math
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_magna_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── 10 CAPÍTULOS MAESTROS DE RIGOR TÉCNICO Y GEOPOLÍTICO ───────────────────

MAGNA_MODULES = [
    {
        "module": "CAPÍTULO 1",
        "badge": "PARADIGMA ESTRATÉGICO",
        "title": "LA SÍNTESIS HUANG-AMODEI: CÓMPUTO ESCALABLE CON GOBERNANZA",
        "text": "El debate global de la inteligencia artificial enfrenta dos visiones: la aceleración del cómputo masivo defendida por Jensen Huang y la advertencia sobre riesgos de seguridad de Dario Amodei. Nuestra arquitectura no elige un bando; ejecuta una síntesis dialéctica. Tomamos la potencia del cómputo distribuido y le aplicamos gobernanza matemática local estricta.",
        "en_sub": "The global AI debate contrasts compute acceleration with safety governance. Our architecture executes a dialectic synthesis of both.",
        "diagram": "SÍNTESIS DIALÉCTICA: CÓMPUTO ABIERTO + GOBERNANZA VECTORIAL"
    },
    {
        "module": "CAPÍTULO 2",
        "badge": "ARQUITECTURA HÍBRIDA",
        "title": "HÍBRIDO GLOBAL: EL MEJOR VALOR DE ORIENTE Y OCCIDENTE",
        "text": "Las corporaciones tradicionales caen en la trampa del monocultivo de software pagando licencias cerradas por usuario. Nosotros orquestamos un enrutador inteligente multimodelo: utilizamos modelos de frontera occidentales para análisis de negocio y modelos de pesos abiertos chinos como DeepSeek y Qwen para razonamiento lógico y código determinista a costo cero.",
        "en_sub": "We break vendor lock-in by orchestrating western reasoning models with open-weight Chinese engines like DeepSeek and Qwen.",
        "diagram": "ROUTER MULTIMODELO: DEEPSEEK + QWEN + GEMINI (AUTO-FAILOVER)"
    },
    {
        "module": "CAPÍTULO 3",
        "badge": "ESCALAMIENTO DE DATOS",
        "title": "AMPLIACIÓN DE BASES DE DATOS LOCALES Y RAG FINANCIERO",
        "text": "El verdadero poder de una organización reside en sus datos propietarios. Mediante nuestro motor de recuperación aumentada con generación y bases vectoriales Qdrant, indexamos catálogos, estados financieros y manuales operativos. La inteligencia artificial no inventa datos; consulta la memoria corporativa verificada en tiempo real.",
        "en_sub": "Enterprise power lies in proprietary data. Our RAG engine retrieves verified business memory with zero fabrication.",
        "diagram": "PIPELINE RAG: QDRANT VECTOR DB + FINANCIAL WORKER :8093"
    },
    {
        "module": "CAPÍTULO 4",
        "badge": "RIGOR MATEMÁTICO",
        "title": "GOBERNANZA VECTORIAL EN ESPACIO R SETECIENTOS SESENTA Y OCHO",
        "text": "Para superar el escrutinio técnico universitario y empresarial, eliminamos la ambigüedad lingüística. Todo documento y consulta se proyecta en un espacio euclidiano unitario de setecientas sesenta y ocho dimensiones. Exigimos una similitud coseno mínima de cero punto ochenta y dos. Cualquier dato por debajo de este umbral es rechazado automáticamente.",
        "en_sub": "We eliminate ambiguity in R768 vector space with a cosine similarity threshold of 0.82 for zero-hallucination guarantees.",
        "diagram": "FILTRO VECTORIAL: S(e_q, e_d) >= 0.82 EN ESPACIO UNITARIO R^768"
    },
    {
        "module": "CAPÍTULO 5",
        "badge": "SANDBOX Y SEGURIDAD",
        "title": "ARNESES DE PROTECCIÓN Y FILTRADO INMUTABLE DE CREDENCIALES",
        "text": "La soberanía exige seguridad perimetral absoluta. Cada transacción atraviesa un Sandbox Guardrail que detecta y bloquea fugas de claves de interfaz, números financieros y contraseñas antes de que salgan a la red. Paralelamente, se genera un registro de auditoría en formato JSON inmutable para control fiscal y normativo.",
        "en_sub": "Perimeter security is enforced via a Sandbox Guardrail filtering credentials and logging immutable JSON audit trails.",
        "diagram": "SANDBOX LAYER: REGEX FILTER + RATE LIMITER + AUDIT JSONL"
    },
    {
        "module": "CAPÍTULO 6",
        "badge": "ORQUESTACIÓN DAG",
        "title": "TEORÍA DE COLAS Y MÉTODO DE LA RUTA CRÍTICA",
        "text": "La eficiencia operativa se modela como un grafo dirigido acíclico bajo la metodología de la Ruta Crítica y Teoría de Colas. Al desacoplar la orquestación ligera de la computación pesada en la nube, una máquina de oficina estándar coordina flujos masivos con latencias medidas de tres segundos.",
        "en_sub": "Workflows are modeled as Directed Acyclic Graphs under Critical Path Method, achieving 3.3s end-to-end latencies.",
        "diagram": "CPM DAG: SCHEDULER ASÍNCRONO + AUTO-ARBITRAJE DE CÓMPUTO"
    },
    {
        "module": "CAPÍTULO 7",
        "badge": "FÁBRICA MULTIMODAL",
        "title": "PRODUCCIÓN AUDIOVISUAL BROADCAST Y TELEPROMPTER EN VIVO",
        "text": "El conocimiento corporativo se transforma instantáneamente en valor público. Nuestra fábrica multimodal genera audio estéreo en cuarenta y ocho kilohercios normalizado bajo la norma internacional EBU R ciento veintiocho a menos dieciséis LUFS, acompañado de subtítulos karaoke dinámicos y reproducción instantánea de cero almacenamiento previo.",
        "en_sub": "Enterprise assets convert to 48kHz stereo broadcast audio under EBU R128 (-16 LUFS) with real-time dynamic teleprompter.",
        "diagram": "MULTIMODAL FACTORY: EDGE-TTS 48KHZ + EBU R128 + 1080P FASTSTART"
    },
    {
        "module": "CAPÍTULO 8",
        "badge": "GEOPOLÍTICA REGIONAL",
        "title": "COLOMBIA COMO HUB ESTRATÉGICO Y SOBERANÍA TECNOLÓGICA",
        "text": "Colombia ocupa una posición geopolítica privilegiada con acceso bioceánico entre el Pacífico y el Atlántico. En el contexto de la nueva economía digital, nuestro país puede liderar la adopción de inteligencia artificial abierta en Latinoamérica, articulando iniciativas de MinTIC, Ruta N, universidades y centros de desarrollo regional.",
        "en_sub": "Colombia's bioceanic position places it strategically to lead open sovereign AI adoption across Latin America.",
        "diagram": "ECOSISTEMA REGIONAL: MINTIC + RUTA N + EAFIT + INDUSTRIA LOCAL"
    },
    {
        "module": "CAPÍTULO 9",
        "badge": "IMPACTO SOCIAL Y PYMES",
        "title": "DEMOCRATIZACIÓN PARA ESTUDIANTES, EMPRENDEDORES Y EMPRESAS",
        "text": "Este desarrollo democratiza el acceso a tecnología de frontera. Un estudiante, una microempresa o una corporación manufacturera pueden operar con la misma sofisticación que un laboratorio de Silicon Valley sin pagar miles de dólares en tarifas recurrentes, fomentando el empleo calificado y la independencia productiva.",
        "en_sub": "Digital sovereignty levels the field for students and enterprises without prohibitive SaaS licensing barriers.",
        "diagram": "INCLUSIÓN PRODUCTIVA: $0 COSTO DE LICENCIAS · ADOPCIÓN UNIVERSAL"
    },
    {
        "module": "CAPÍTULO 10",
        "badge": "CONCLUSIÓN TÉCNICA",
        "title": "EL FUTURO ES SOBERANO, VERIFICABLE Y DE ALTO VALOR",
        "text": "Concluimos esta sesión con una certeza técnica demostrada: la inteligencia artificial soberana no es una promesa futura; es una realidad operativa probada en código, medible en milisegundos y respaldada en infraestructuras resilientes de cinco Terabytes. Bienvenidos al nuevo estándar OpenClaw dos mil veintiséis.",
        "en_sub": "Sovereign AI is an operational reality: verified in code, benchmarked in milliseconds and securely backed up.",
        "diagram": "OPENCLAW CORE MATRIX 2026: SOBERANÍA · PRECISIÓN · CRECIMIENTO"
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

async def synthesize_all_magna_audios():
    print("\n[FASE 1/4] Sintetizando 10 módulos con Edge-TTS 48kHz (-16 LUFS)...")
    for idx, item in enumerate(MAGNA_MODULES):
        raw_mp3 = RUNTIME / f"magna_raw_{idx}.mp3"
        master_aac = RUNTIME / f"magna_master_{idx}.aac"
        
        # Voz en español con cadencia amigable y pausada
        communicate = edge_tts.Communicate(item["text"], voice="es-MX-JorgeNeural", rate="-4%")
        await communicate.save(str(raw_mp3))
        
        # Normalización EBU R128 (-16 LUFS)
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            str(master_aac)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        dur = get_audio_duration(str(master_aac))
        item["audio_file"] = str(master_aac)
        item["duration"] = dur
        print(f"  [OK] {item['module']}: {dur:.2f}s | '{item['title'][:45]}...'")

def render_magna_masterclass():
    # 1. Sintetizar audios
    asyncio.run(synthesize_all_magna_audios())
    
    # 2. Mezclar pista maestra con pausas de 0.8s
    print("\n[FASE 2/4] Ensamblando pista de audio maestra con pausas de respiración...")
    pause_aac = RUNTIME / "pause_08s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "0.8", "-c:a", "aac", "-b:a", "192k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    concat_txt = RUNTIME / "concat_magna.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in MAGNA_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")
            
    master_audio = RUNTIME / "master_soundtrack_magna_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    
    # 3. Renderizar Fotogramas 1080p con Teleprompter Karaoke e Infografías
    print("\n[FASE 3/4] Generando fotogramas 1080p con Teleprompter Karaoke y Diapositivas Técnicas...")
    
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "dorado.png"
    avatar_img = Image.open(avatar_src).convert("RGBA")
    av_target_h = 760
    av_target_w = int(avatar_img.width * (av_target_h / avatar_img.height))
    avatar_img = avatar_img.resize((av_target_w, av_target_h), Image.Resampling.LANCZOS)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 40)
        font_subtitle = ImageFont.truetype("arialbd.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 34)
        font_en = ImageFont.truetype("ariali.ttf", 24)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
        font_diagram = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_diagram = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in MAGNA_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 0.8
        
    frames_dir = RUNTIME / "temp_magna_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    total_frames = int(total_duration * FPS)
    print(f"  -> Renderizando {total_frames} fotogramas a {FPS} FPS...")
    
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
        dur_mod = item["duration"]
        
        # Canvas: Dark Slate / Navy Blue
        frame = Image.new("RGB", (WIDTH, HEIGHT), (12, 16, 26))
        draw = ImageDraw.Draw(frame)
        
        # Header Top Bar
        draw.rectangle([0, 0, WIDTH, 85], fill=(20, 26, 40))
        draw.line([0, 85, WIDTH, 85], fill=(212, 175, 55), width=2)
        draw.text((60, 26), "OPENCLAW CORE MATRIX 2026", font=font_badge, fill=(212, 175, 55))
        draw.text((390, 26), "·   MASTERCLASS: ARQUITECTURA HÍBRIDA & SOBERANÍA DIGITAL", font=font_badge, fill=(190, 200, 220))
        draw.text((1580, 26), "ESTÁNDAR R^768 · $0 COSTO", font=font_badge, fill=(100, 220, 150))
        
        # Lado Izquierdo: Avatar con movimiento suave
        av_float_y = int(math.sin(t * 1.4) * 4)
        av_pos_x = 60
        av_pos_y = 190 + av_float_y
        frame.paste(avatar_img, (av_pos_x, av_pos_y), avatar_img)
        
        # Lado Derecho: Teleprompter Card
        card_x = 700
        card_y = 120
        card_w = 1160
        card_h = 880
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(18, 24, 38), outline=(38, 50, 75), width=2)
        
        # Badges
        draw.rounded_rectangle([card_x + 50, card_y + 35, card_x + 220, card_y + 72], radius=6, fill=(212, 175, 55))
        draw.text((card_x + 65, card_y + 42), item["module"], font=font_badge, fill=(15, 20, 30))
        
        draw.rounded_rectangle([card_x + 235, card_y + 35, card_x + 600, card_y + 72], radius=6, fill=(35, 48, 75))
        draw.text((card_x + 250, card_y + 42), item["badge"], font=font_badge, fill=(212, 175, 55))
        
        # Título
        draw.text((card_x + 50, card_y + 95), item["title"], font=font_title, fill=(255, 255, 255))
        
        # Banner Técnico / Diagrama del Módulo
        draw.rounded_rectangle([card_x + 50, card_y + 155, card_x + card_w - 50, card_y + 205], radius=6, fill=(26, 36, 56), outline=(50, 70, 105), width=1)
        draw.text((card_x + 70, card_y + 168), "⚡ ARTEFACTO: " + item["diagram"], font=font_diagram, fill=(100, 220, 180))
        
        draw.line([card_x + 50, card_y + 225, card_x + card_w - 50, card_y + 225], fill=(45, 60, 90), width=1)
        
        # Teleprompter Karaoke
        words = item["text"].split()
        total_words = len(words)
        active_word_idx = int((t_rel / max(0.1, dur_mod)) * total_words) if dur_mod > 0 else 0
        
        cursor_x = card_x + 50
        cursor_y = card_y + 255
        max_line_w = card_w - 100
        line_height = 50
        
        for w_idx, word in enumerate(words):
            word_str = word + " "
            bbox = font_text.getbbox(word_str)
            w_width = bbox[2] - bbox[0]
            
            if cursor_x + w_width > card_x + 50 + max_line_w:
                cursor_x = card_x + 50
                cursor_y += line_height
                
            if w_idx <= active_word_idx:
                w_color = (255, 215, 0) if w_idx == active_word_idx else (240, 245, 255)
            else:
                w_color = (110, 125, 150)
                
            draw.text((cursor_x, cursor_y), word_str, font=font_text, fill=w_color)
            cursor_x += w_width
            
        # Subtítulo en Inglés
        draw.line([card_x + 50, card_y + card_h - 95, card_x + card_w - 50, card_y + card_h - 95], fill=(45, 60, 90), width=1)
        draw.text((card_x + 50, card_y + card_h - 70), "EN: " + item["en_sub"], font=font_en, fill=(150, 180, 215))
        
        # Barra de progreso inferior
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 8, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))
        
        frame_file = frames_dir / f"magna_frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)
        
        if f_idx % 300 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")
            
    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n[FASE 4/4] Codificando Masterclass Magna 1080p con FFmpeg FastStart...")
    final_output = RUNTIME / "OpenClaw_Masterclass_Magna_1080p_FastStart.mp4"
    
    cmd_render = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", str(frames_dir / "magna_frame_%06d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_output)
    ]
    subprocess.run(cmd_render, check=True)
    
    size_mb = final_output.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print("  🏆 MASTERCLASS MAGNA 1080P GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print("  Visual:   Teleprompter Karaoke + Diapositivas Técnicas + Audio 48kHz")
    print("=" * 60)
    
    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()
    
    return str(final_output)

if __name__ == "__main__":
    render_magna_masterclass()
