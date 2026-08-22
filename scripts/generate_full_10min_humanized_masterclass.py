"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS 10 MINUTOS HUMANIZADA Y DE ALTO IMPACTO
==============================================================================
- Duración: 8 a 10 Minutos Reales (~1.100 palabras / 10 Capítulos)
- Tono: Humanizado, cálido, testimonial, pedagógico y de alto rigor técnico
- Fonética: Ajustada naturalmente (Dip-Sik, Kiu-en, Open-Clo, Min-Tik)
- Visual: Avatar HD con marco circular dorado + Teleprompter Karaoke en tiempo real
- Audio: 48kHz Stereo Broadcast EBU R128 (-16 LUFS)
==============================================================================
"""

import os
import sys
import json
import math
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import edge_tts

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_humanizada_10m"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── 10 CAPÍTULOS HUMANIZADOS (8 A 10 MINUTOS TOTALES) ──────────────────────

HUMAN_MODULES = [
    {
        "module": "CAPÍTULO 1",
        "badge": "HISTORIA Y VISIÓN",
        "title": "EL DESPERTAR DE LA INTELIGENCIA ARTIFICIAL SOBERANA",
        "text": "Hola a todos. Les habla Guillermo. Quiero darles una bienvenida muy especial a esta Masterclass. Durante mucho tiempo nos hicieron creer que para participar en la revolución de la inteligencia artificial necesitábamos millones de dólares, supercomputadores inalcanzables o pagar suscripciones mensuales que ahogan a cualquier emprendedor. Hoy les quiero demostrar, con hechos y con código en mano, que eso no es verdad. Desde nuestra propia experiencia, combinando la visión de negocio con tecnología de vanguardia, hemos construido un Sistema Operativo Universal a costo cero que le devuelve el poder a las personas, a los estudiantes y a nuestras empresas.",
        "en_sub": "Welcome. We prove that participating in the AI revolution does not require millions in SaaS fees. Sovereignty is now accessible to all.",
        "diagram": "VISIÓN SOBERANA: DEMOCRATIZACIÓN TECNOLÓGICA REAL A $0 COSTO"
    },
    {
        "module": "CAPÍTULO 2",
        "badge": "LA GRAN SÍNTESIS",
        "title": "DARIO AMODEI Y JENSEN HUANG: LA FUERZA RESULTANTE",
        "text": "Cuando escuchamos a los líderes mundiales de la inteligencia artificial, vemos dos fuerzas muy claras. Por un lado, Jensen Huang de Envidia nos dice que el cómputo masivo y los modelos abiertos son el motor del futuro. Por otro lado, Dario Amodei de Antropic nos advierte sobre la necesidad urgente de seguridad, control y contención de riesgos. Nosotros tomamos lo mejor de ambos mundos: la capacidad de acelerar el cómputo distribuido sin límites, pero envolviéndolo en reglas de negocio estrictas y protección absoluta de nuestros datos privados. Esa combinación crea una fuerza superior para Latinoamérica.",
        "en_sub": "We synthesize Jensen Huang's open compute power with Dario Amodei's safety guardrails to protect proprietary data.",
        "diagram": "SÍNTESIS DIALÉCTICA: CÓMPUTO EXTERNO + ARNESES DE SEGURIDAD"
    },
    {
        "module": "CAPÍTULO 3",
        "badge": "EL PUENTE GLOBAL",
        "title": "INTEGRACIÓN HÍBRIDA: LO MEJOR DE ORIENTE Y OCCIDENTE",
        "text": "En lugar de casarnos con un solo proveedor extranjero, creamos un enrutador inteligente multimodelo. Para el análisis de mercado y la estrategia en español usamos modelos como Claude y Yéminai. Pero para el razonamiento lógico profundo, las matemáticas financieras y la generación de código determinista, conectamos modelos abiertos como Dip-Sik y Kiu-en de Alibaba. Esto nos permite obtener respuestas de nivel doctoral en tres segundos sin pagar un solo centavo por licencias comerciales.",
        "en_sub": "Our multi-model router combines western business reasoning with DeepSeek and Qwen open-weight engines at $0 license cost.",
        "diagram": "ROUTER MULTIMODELO: CLAUDE + GEMINI + DEEPSEEK + QWEN 72B"
    },
    {
        "module": "CAPÍTULO 4",
        "badge": "DATOS PROPIOS",
        "title": "ESCALAR NUESTRA MEMORIA: BASES VECTORIALES Y RAG LOCAL",
        "text": "Una de las mayores angustias de los empresarios es que la inteligencia artificial alucine o invente datos que comprometan a la empresa. Nuestra respuesta es la recuperación aumentada con generación. Conectamos bases de datos vectoriales privadas como Kiudrant directamente en nuestro entorno. El sistema indexa catálogos de joyas, listas de precios, políticas de garantía y manuales técnicos. Cuando un cliente o un estudiante pregunta, el sistema responde únicamente con la verdad de nuestros documentos.",
        "en_sub": "Private Qdrant vector databases anchor LLM responses directly to verified business documents, eliminating hallucinations.",
        "diagram": "ARQUITECTURA RAG: QDRANT VECTOR STORE + WORKER FINANCIERO :8093"
    },
    {
        "module": "CAPÍTULO 5",
        "badge": "RIGOR CIENTÍFICO",
        "title": "GOBERNANZA MATEMÁTICA EN ESPACIO R SETECIENTOS SESENTA Y OCHO",
        "text": "Para que nuestro desarrollo soporte el escrutinio técnico más riguroso de universidades como E-A-FIT o centros como Ruta N, formalizamos la comunicación en el espacio euclidiano R setecientos sesenta y ocho. Mediante el modelo B-A-A-I b-g-e m-tres, calculamos la similitud coseno entre la pregunta y la información guardada. Si la similitud matemática es menor a cero punto ochenta y dos, el sistema rechaza la respuesta por falta de certeza. Es la garantía absoluta de cero alucinaciones.",
        "en_sub": "Mathematical governance projects queries into R768 space, enforcing a strict 0.82 cosine similarity verification threshold.",
        "diagram": "FILTRO DETERMINISTA: SIMILITUD COSENO S(e_q, e_d) >= 0.82"
    },
    {
        "module": "CAPÍTULO 6",
        "badge": "SEGURIDAD Y SANDBOX",
        "title": "PROTECCIÓN PERIMETRAL: GUARDRAILS Y AUDITORÍA INMUTABLE",
        "text": "Muchos temen que al usar herramientas en la nube sus claves o secretos comerciales se filtren. En Open-Clo construimos un Sandbox Guardrail que actúa como un escudo protector en cada llamada. Si alguien intenta inyectar por error una clave de interfaz, un número de tarjeta o una contraseña, el guardrail bloquea la salida en milisegundos. Además, cada interacción queda guardada en un archivo de auditoría inmutable para total tranquilidad contable y legal.",
        "en_sub": "Our Sandbox Guardrail inspects all outbound payloads, intercepting credentials and logging immutable JSON audit trails.",
        "diagram": "ESCUDO SANDBOX: FILTRO REGEX + RATE LIMITING + REGISTRO JSONL"
    },
    {
        "module": "CAPÍTULO 7",
        "badge": "ORQUESTACIÓN ÁGIL",
        "title": "TEORÍA DE COLAS Y RUTA CRÍTICA PARA MÁXIMA VELOCIDAD",
        "text": "El secreto para que un computador modesto funcione como una estación de trabajo de última generación es la teoría de colas y los grafos dirigidos acíclicos. Separamos la coordinación liviana del cómputo pesado. Nuestro computador local sólo organiza el flujo de trabajo en la ruta crítica, mientras los clústeres en la nube ejecutan los procesos difíciles en segundos. Esto nos permite alcanzar latencias de tres segundos y medio sin sobrecalentar nuestros equipos.",
        "en_sub": "Queueing Theory and Critical Path Methods decouple local lightweight coordination from cloud heavy compute.",
        "diagram": "CPM DAG: RUTA CRÍTICA SINCRONIZADA CON LATENCIAS DE 3.3s"
    },
    {
        "module": "CAPÍTULO 8",
        "badge": "FÁBRICA AUDIOVISUAL",
        "title": "COMUNICACIÓN BROADCAST Y TELEPROMPTER EN TIEMPO REAL",
        "text": "El conocimiento no sirve de nada si se queda atrapado en un servidor. Por eso integramos una fábrica audiovisual completa. Generamos locución profesional estéreo en cuarenta y ocho kilohercios con normalización acústica internacional E-B-U R ciento veintiocho a menos dieciséis LUFS. Los subtítulos se sincronizan palabra por palabra en tiempo real, listos para reproducirse en YouTube o redes sociales con cero almacenamiento previo.",
        "en_sub": "Enterprise knowledge transforms into broadcast-quality 48kHz stereo media with word-by-word real-time teleprompter sync.",
        "diagram": "FÁBRICA MULTIMODAL: EDGE-TTS 48KHZ + TELEPROMPTER KARAOKE ORO"
    },
    {
        "module": "CAPÍTULO 9",
        "badge": "GEOPOLÍTICA COLOMBIA",
        "title": "COLOMBIA COMO FARO DE INNOVACIÓN TECNOLÓGICA EN LA REGIÓN",
        "text": "Colombia tiene una posición geográfica privilegiada en el mundo, uniendo el Pacífico con el Caribe. Nuestro país tiene el talento, la juventud y la creatividad para ser el centro de desarrollo de inteligencia artificial soberana de toda Latinoamérica. Este sistema no depende de contratos millonarios con corporaciones extranjeras; está listo para implementarse en convenios con el Min-Tik, alcaldías, gobernaciones y nuestras universidades para capacitar a miles de jóvenes.",
        "en_sub": "Colombia is strategically positioned to lead Latin America's sovereign AI ecosystem with MinTIC and top universities.",
        "diagram": "ECOSISTEMA NACIONAL: MINTIC + RUTA N + EAFIT + ALCALDÍAS"
    },
    {
        "module": "CAPÍTULO 10",
        "badge": "EL LLAMADO A LA ACCIÓN",
        "title": "EL FUTURO ES DE QUIENES CONSTRUYEN CON HECHOS Y SIN HUMO",
        "text": "Queridos amigos, estudiantes y empresarios: la inteligencia artificial no es para unos pocos elegidos. La neurociencia nos enseña que cuando aprendemos y practicamos con disciplina, nuestro cerebro crea nuevas conexiones que aceleran nuestro entendimiento. Lo que vieron hoy está funcionando en código real, respaldado en la nube y verificado. Los invito a que no se queden como simples espectadores. Es hora de crear, de producir y de liderar. Bienvenidos a Open-Clo dos mil veintiséis.",
        "en_sub": "AI is for creators who build with verifiable facts. We invite students and enterprises to lead this digital sovereignty journey.",
        "diagram": "OPENCLAW 2026: SOBERANÍA · LIBERTAD PRODUCTIVA · CRECIMIENTO"
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

async def synthesize_human_audios():
    print("\n[PASO 1/4] Sintetizando 10 módulos humanizados con Edge-TTS 48kHz (-16 LUFS)...")
    for idx, item in enumerate(HUMAN_MODULES):
        raw_mp3 = RUNTIME / f"human_raw_{idx}.mp3"
        master_aac = RUNTIME / f"human_master_{idx}.aac"
        
        # Voz en español con tono cálido, humano y pausado (-5% rate para máxima claridad)
        communicate = edge_tts.Communicate(item["text"], voice="es-MX-JorgeNeural", rate="-5%")
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

def prepare_circular_avatar(avatar_path: Path, size: int = 560) -> Image.Image:
    """Prepara el avatar Guillermo dentro de un marco circular con anillo dorado y sombra."""
    raw = Image.open(avatar_path).convert("RGB")
    raw = raw.resize((size, size), Image.Resampling.LANCZOS)
    
    # Máscara circular
    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((10, 10, size - 10, size - 10), fill=255)
    
    # Recortar circular
    circular_img = ImageOps.fit(raw, (size, size), centering=(0.5, 0.4))
    
    # Canvas con canal alfa
    final_av = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0))
    draw_av = ImageDraw.Draw(final_av)
    
    # Anillo exterior dorado brillante
    draw_av.ellipse((15, 15, size + 25, size + 25), outline=(212, 175, 55, 255), width=8)
    draw_av.ellipse((10, 10, size + 30, size + 30), outline=(255, 225, 100, 180), width=3)
    
    # Pegar avatar circular dentro del anillo
    final_av.paste(circular_img, (20, 20), mask=mask)
    return final_av

def render_10min_masterclass():
    # 1. Sintetizar audios
    asyncio.run(synthesize_human_audios())
    
    # 2. Mezclar pista maestra con pausas de 1.0s entre módulos
    print("\n[PASO 2/4] Mezclando pista maestra con pausas de respiración (1.0s)...")
    pause_aac = RUNTIME / "pause_1s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "192k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    concat_txt = RUNTIME / "concat_human.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in HUMAN_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")
            
    master_audio = RUNTIME / "master_soundtrack_human_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    
    # 3. Preparar Avatar Circular con Anillo Dorado
    print("\n[PASO 3/4] Generando fotogramas 1080p con Avatar HD, Teleprompter y Banners...")
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "dorado.png"
    avatar_canvas = prepare_circular_avatar(avatar_src, size=520)
    
    # Fuentes
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 38)
        font_text = ImageFont.truetype("arial.ttf", 32)
        font_en = ImageFont.truetype("ariali.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
        font_diagram = ImageFont.truetype("arialbd.ttf", 22)
        font_speaker = ImageFont.truetype("arialbd.ttf", 24)
        font_role = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_diagram = ImageFont.load_default()
        font_speaker = ImageFont.load_default()
        font_role = ImageFont.load_default()

    timeline = []
    curr_t = 0.0
    for item in HUMAN_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 1.0
        
    frames_dir = RUNTIME / "temp_human_frames"
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
        
        # Canvas Base: Fondo Estudio Azul Marino Oscuro Elegante
        frame = Image.new("RGB", (WIDTH, HEIGHT), (10, 14, 24))
        draw = ImageDraw.Draw(frame)
        
        # Header Superior
        draw.rectangle([0, 0, WIDTH, 80], fill=(18, 24, 38))
        draw.line([0, 80, WIDTH, 80], fill=(212, 175, 55), width=2)
        draw.text((60, 26), "OPENCLAW CORE MATRIX 2026", font=font_badge, fill=(212, 175, 55))
        draw.text((390, 26), "·   MASTERCLASS: ARQUITECTURA SOBERANA & SÍNTESIS HUANG-AMODEI", font=font_badge, fill=(190, 200, 220))
        draw.text((1560, 26), "ESTÁNDAR R^768 · $0 LICENCIAS", font=font_badge, fill=(100, 220, 150))
        
        # ─── LADO IZQUIERDO: AVATAR GUILLERMO CON MARCO DORADO Y TARJETA IDENTIFICACIÓN ───
        av_float_y = int(math.sin(t * 1.5) * 5)
        av_pos_x = 70
        av_pos_y = 130 + av_float_y
        frame.paste(avatar_canvas, (av_pos_x, av_pos_y), avatar_canvas)
        
        # Tarjeta de Presentador debajo del Avatar
        spk_y = av_pos_y + 570
        draw.rounded_rectangle([av_pos_x + 30, spk_y, av_pos_x + 530, spk_y + 110], radius=12, fill=(18, 24, 38), outline=(45, 60, 90), width=1)
        draw.text((av_pos_x + 60, spk_y + 20), "GUILLERMO · OPENCLAW", font=font_speaker, fill=(255, 255, 255))
        draw.text((av_pos_x + 60, spk_y + 60), "Director de Arquitectura · HB Jewelry", font=font_role, fill=(212, 175, 55))
        
        # Badge de Estado en Vivo (LED Verde)
        draw.ellipse([av_pos_x + 470, spk_y + 28, av_pos_x + 488, spk_y + 46], fill=(50, 220, 100))
        draw.text((av_pos_x + 410, spk_y + 26), "LIVE", font=font_role, fill=(100, 220, 150))
        
        # Badge de Métrica Inferior Izquierda
        draw.rounded_rectangle([av_pos_x + 30, spk_y + 130, av_pos_x + 530, spk_y + 200], radius=8, fill=(14, 20, 32), outline=(35, 45, 70), width=1)
        draw.text((av_pos_x + 50, spk_y + 145), "⚡ LATENCIA: 3.3s | SIMILITUD: S >= 0.82", font=font_role, fill=(130, 190, 230))
        draw.text((av_pos_x + 50, spk_y + 170), "🛡️ SANDBOX: ACTIVO | $0 COSTO OPERATIVO", font=font_role, fill=(100, 220, 150))
        
        # ─── LADO DERECHO: TELEPROMPTER KARAOKE Y CONTENIDO PEDAGÓGICO ───
        card_x = 680
        card_y = 110
        card_w = 1180
        card_h = 900
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(16, 22, 36), outline=(38, 52, 80), width=2)
        
        # Badges de Módulo y Categoría
        draw.rounded_rectangle([card_x + 50, card_y + 30, card_x + 220, card_y + 68], radius=6, fill=(212, 175, 55))
        draw.text((card_x + 65, card_y + 38), item["module"], font=font_badge, fill=(10, 15, 25))
        
        draw.rounded_rectangle([card_x + 235, card_y + 30, card_x + 600, card_y + 68], radius=6, fill=(30, 42, 68))
        draw.text((card_x + 250, card_y + 38), item["badge"], font=font_badge, fill=(212, 175, 55))
        
        # Título del Capítulo
        draw.text((card_x + 50, card_y + 85), item["title"], font=font_title, fill=(255, 255, 255))
        
        # Banner Técnico / Artefacto
        draw.rounded_rectangle([card_x + 50, card_y + 145, card_x + card_w - 50, card_y + 195], radius=6, fill=(24, 34, 54), outline=(48, 68, 105), width=1)
        draw.text((card_x + 70, card_y + 158), "📐 ARTEFACTO: " + item["diagram"], font=font_diagram, fill=(100, 220, 180))
        
        draw.line([card_x + 50, card_y + 215, card_x + card_w - 50, card_y + 215], fill=(40, 55, 85), width=1)
        
        # Teleprompter Karaoke Dinámico en Oro
        words = item["text"].split()
        total_words = len(words)
        active_word_idx = int((t_rel / max(0.1, dur_mod)) * total_words) if dur_mod > 0 else 0
        
        cursor_x = card_x + 50
        cursor_y = card_y + 245
        max_line_w = card_w - 100
        line_height = 46
        
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
                w_color = (105, 120, 145)
                
            draw.text((cursor_x, cursor_y), word_str, font=font_text, fill=w_color)
            cursor_x += w_width
            
        # Subtítulo en Inglés
        draw.line([card_x + 50, card_y + card_h - 90, card_x + card_w - 50, card_y + card_h - 90], fill=(40, 55, 85), width=1)
        draw.text((card_x + 50, card_y + card_h - 65), "EN: " + item["en_sub"], font=font_en, fill=(150, 180, 220))
        
        # Barra de progreso inferior
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 8, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))
        
        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)
        
        if f_idx % 400 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")
            
    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n[PASO 4/4] Ensamblando Masterclass 10 Minutos con FFmpeg...")
    final_output = RUNTIME / "OpenClaw_Masterclass_Humanizada_10m_1080p.mp4"
    
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
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(final_output)
    ]
    subprocess.run(cmd_render, check=True)
    
    size_mb = final_output.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print("  🏆 MASTERCLASS HUMANIZADA 10 MINUTOS GENERADA CON ÉXITO")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    print("  Avatar:   HD Circular con Marco Dorado y Tarjeta de Identificación")
    print("  Visual:   Teleprompter Karaoke Oro + Fonética Calibrada")
    print("=" * 60)
    
    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()
    
    return str(final_output)

if __name__ == "__main__":
    render_10min_masterclass()
