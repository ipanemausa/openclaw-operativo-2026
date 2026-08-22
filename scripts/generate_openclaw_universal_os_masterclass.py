"""
==============================================================================
OPENCLAW CLOUD 2026 — MASTERCLASS EDUCATIVA SISTEMA OPERATIVO UNIVERSAL $0 COSTO
==============================================================================
Contenido: Arquitectura Soberana B2B/B2C, Espacio Vectorial R^768, DAG CPM y $0 Costo
Formato: Video 1080p Master para YouTube
Visuales: Fondo Estudio Cósmico + Avatar HD Limpio + Teleprompter Karaoke Palabra por Palabra
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
RUNTIME = ROOT / "runtime" / "masterclass_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── GUION EDUCATIVO COMPLETO (SISTEMA OPERATIVO UNIVERSAL $0 COSTO) ─────────

MASTERCLASS_MODULES = [
    {
        "module": "INTRODUCCIÓN",
        "title": "EL NUEVO PARADIGMA: INTELIGENCIA ARTIFICIAL SOBERANA",
        "text": "Bienvenidos a la Masterclass Oficial de OpenClaw dos mil veintiséis. Hoy presentamos la arquitectura del primer Sistema Operativo Universal de Inteligencia Artificial Soberana a cero costo de licencias.",
        "en_sub": "Welcome to the OpenClaw 2026 Official Masterclass on Sovereign AI Operating Systems at zero licensing cost."
    },
    {
        "module": "MÓDULO 1: LA RUPTURA DEL MONOPOLIO",
        "title": "DESACOPLAMIENTO DE APIS CERRADAS",
        "text": "Durante años las empresas han dependido de modelos cerrados con altos costos recurrentes y riesgos de fuga de datos. Nuestro sistema rompe esa dependencia usando modelos de pesos abiertos como DeepSeek y Qwen.",
        "en_sub": "For years businesses relied on closed APIs with high recurrent costs. Our system eliminates that dependency using open-weight models."
    },
    {
        "module": "MÓDULO 2: GOBERNANZA VECTORIAL",
        "title": "ESPACIO LATENTE R SETECIENTOS SESENTA Y OCHO",
        "text": "La clave de la precisión matemática radica en nuestro espacio vectorial R setecientos sesenta y ocho. Mediante un filtro de similitud coseno superior a cero punto ochenta y dos, eliminamos por completo cualquier alucinación.",
        "en_sub": "Mathematical precision relies on our R768 vector space. With a cosine similarity threshold of 0.82, we achieve zero hallucination."
    },
    {
        "module": "MÓDULO 3: ORQUESTACIÓN Y TEORÍA DE COLAS",
        "title": "GRAFOS DIRIGIDOS ACÍCLICOS Y RUTA CRÍTICA",
        "text": "El flujo de trabajo se ejecuta bajo la metodología de la Ruta Crítica y Teoría de Colas. Cada tarea se procesa de forma asíncrona, garantizando latencias menores a cuatro segundos en computación distribuida.",
        "en_sub": "Workflows execute under Critical Path Method and Queueing Theory, ensuring sub-4-second distributed latencies."
    },
    {
        "module": "MÓDULO 4: SANDBOX Y SEGURIDAD TOTAL",
        "title": "PROTECCIÓN INMUTABLE DE DATOS PRIVADOS",
        "text": "Tus datos comerciales, catálogos y fórmulas nunca salen desprotegidos. El Sandbox Guardrail filtra credenciales, aplica límites de tasa y audita cada transacción en registros inmutables en tiempo real.",
        "en_sub": "Commercial data and catalog rules never leak. The Sandbox Guardrail filters credentials and logs immutable audit trails."
    },
    {
        "module": "MÓDULO 5: FÁBRICA MULTIMODAL",
        "title": "PRODUCCIÓN AUDIOVISUAL Y TELEPROMPTER EN VIVO",
        "text": "Convertimos el conocimiento empresarial en piezas audiovisuales de alta definición con audio estéreo en cuarenta y ocho kilohercios, normalización profesional y subtítulos sincronizados palabra por palabra.",
        "en_sub": "We transform enterprise knowledge into high-definition audiovisual assets with 48kHz stereo broadcast audio."
    },
    {
        "module": "CONCLUSIÓN",
        "title": "DEMOCRATIZACIÓN TECNOLÓGICA PARA JÓVENES Y EMPRESAS",
        "text": "Esta plataforma demuestra que no se requiere supercomputadores millonarios para competir a nivel mundial. La soberanía digital está ahora al alcance de estudiantes, emprendedores y empresas globales.",
        "en_sub": "This platform proves that high-level AI does not require millions in funding. Digital sovereignty is now universally accessible."
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

async def synthesize_module_audios():
    print("\n[PASO 1/4] Sintetizando locuciones vocales 48kHz con Edge-TTS...")
    for idx, item in enumerate(MASTERCLASS_MODULES):
        raw_mp3 = RUNTIME / f"speech_mod_{idx}.mp3"
        master_aac = RUNTIME / f"speech_mod_{idx}.aac"
        
        # Síntesis con cadencia amigable y respetuosa
        communicate = edge_tts.Communicate(item["text"], voice="es-MX-JorgeNeural", rate="-3%")
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
        print(f"  [OK] Modulo {idx+1}/{len(MASTERCLASS_MODULES)}: {dur:.2f}s | '{item['title']}'")

def render_masterclass_video():
    # 1. Generar audios
    asyncio.run(synthesize_module_audios())
    
    # 2. Concatenar Audio Maestro con pausas de 0.8s
    print("\n[PASO 2/4] Mezclando pista maestra con pausas de respiración...")
    pause_aac = RUNTIME / "pause_08s.aac"
    cmd_pause = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "0.8", "-c:a", "aac", "-b:a", "192k", str(pause_aac)
    ]
    subprocess.run(cmd_pause, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    concat_txt = RUNTIME / "concat_audio.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in MASTERCLASS_MODULES:
            f.write(f"file '{Path(item['audio_file']).as_posix()}'\n")
            f.write(f"file '{pause_aac.as_posix()}'\n")
            
    master_audio = RUNTIME / "master_soundtrack_48k.aac"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(master_audio)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    total_duration = get_audio_duration(str(master_audio))
    print(f"  [OK] Audio Maestro Total: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")
    
    # 3. Construir Fondos y Fotogramas con Teleprompter Karaoke
    print("\n[PASO 3/4] Generando video con Teleprompter Karaoke en tiempo real...")
    
    # Cargar Avatar limpio
    avatar_src = ROOT / "frontend" / "dist" / "avatars" / "dorado.png"
    avatar_img = Image.open(avatar_src).convert("RGBA")
    av_target_h = 780
    av_target_w = int(avatar_img.width * (av_target_h / avatar_img.height))
    avatar_img = avatar_img.resize((av_target_w, av_target_h), Image.Resampling.LANCZOS)
    
    # Fuentes
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 44)
        font_subtitle = ImageFont.truetype("arialbd.ttf", 26)
        font_text = ImageFont.truetype("arial.ttf", 36)
        font_en = ImageFont.truetype("ariali.ttf", 26)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_en = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Timeline de módulos
    timeline = []
    curr_t = 0.0
    for item in MASTERCLASS_MODULES:
        t_start = curr_t
        t_end = curr_t + item["duration"]
        timeline.append({"item": item, "start": t_start, "end": t_end})
        curr_t = t_end + 0.8  # pausa
        
    frames_dir = RUNTIME / "temp_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    total_frames = int(total_duration * FPS)
    print(f"  -> Renderizando {total_frames} fotogramas a {FPS} FPS...")
    
    for f_idx in range(total_frames):
        t = f_idx / FPS
        
        # Encontrar módulo activo
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
        
        # Canvas Base: Gradiente de Estudio Dark Slate / Navy Blue
        frame = Image.new("RGB", (WIDTH, HEIGHT), (14, 18, 28))
        draw = ImageDraw.Draw(frame)
        
        # Decoración geométrica de fondo (Glow sutil)
        draw.rectangle([0, 0, WIDTH, 90], fill=(22, 28, 42))
        draw.line([0, 90, WIDTH, 90], fill=(212, 175, 55), width=2)
        
        # Header Superior
        draw.text((60, 28), "OPENCLAW CLOUD 2026", font=font_badge, fill=(212, 175, 55))
        draw.text((360, 28), "·   SISTEMA OPERATIVO UNIVERSAL DE IA SOBERANA", font=font_badge, fill=(180, 190, 210))
        draw.text((1600, 28), "ESTÁNDAR R^768", font=font_badge, fill=(100, 220, 150))
        
        # Lado Izquierdo: Avatar con respiración suave
        av_float_y = int(math.sin(t * 1.5) * 4)
        av_pos_x = 70
        av_pos_y = 190 + av_float_y
        frame.paste(avatar_img, (av_pos_x, av_pos_y), avatar_img)
        
        # Lado Derecho: Teleprompter Card Elegante
        card_x = 720
        card_y = 140
        card_w = 1130
        card_h = 840
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(20, 26, 40), outline=(40, 52, 78), width=2)
        
        # Badge de Módulo
        draw.rounded_rectangle([card_x + 50, card_y + 40, card_x + 350, card_y + 80], radius=8, fill=(212, 175, 55))
        draw.text((card_x + 65, card_y + 48), item["module"], font=font_badge, fill=(15, 20, 30))
        
        # Título del Módulo
        draw.text((card_x + 50, card_y + 110), item["title"], font=font_title, fill=(255, 255, 255))
        draw.line([card_x + 50, card_y + 175, card_x + card_w - 50, card_y + 175], fill=(50, 65, 95), width=1)
        
        # Teleprompter Karaoke: Resaltar palabras según progreso temporal
        words = item["text"].split()
        total_words = len(words)
        active_word_idx = int((t_rel / max(0.1, dur_mod)) * total_words) if dur_mod > 0 else 0
        
        # Renderizado de texto en líneas con Karaoke Dorado
        cursor_x = card_x + 50
        cursor_y = card_y + 220
        max_line_w = card_w - 100
        line_height = 55
        
        for w_idx, word in enumerate(words):
            word_str = word + " "
            bbox = font_text.getbbox(word_str)
            w_width = bbox[2] - bbox[0]
            
            if cursor_x + w_width > card_x + 50 + max_line_w:
                cursor_x = card_x + 50
                cursor_y += line_height
                
            # Color: Dorado si es la palabra activa/leída, Gris claro si es futura
            if w_idx <= active_word_idx:
                w_color = (255, 215, 0) if w_idx == active_word_idx else (235, 240, 255)
            else:
                w_color = (120, 135, 160)
                
            draw.text((cursor_x, cursor_y), word_str, font=font_text, fill=w_color)
            cursor_x += w_width
            
        # Subtítulo en Inglés en la parte inferior de la tarjeta
        draw.line([card_x + 50, card_y + card_h - 110, card_x + card_w - 50, card_y + card_h - 110], fill=(50, 65, 95), width=1)
        draw.text((card_x + 50, card_y + card_h - 80), "EN: " + item["en_sub"], font=font_en, fill=(160, 185, 220))
        
        # Barra de progreso inferior
        progress_pct = t / total_duration
        draw.rectangle([0, HEIGHT - 8, int(WIDTH * progress_pct), HEIGHT], fill=(212, 175, 55))
        
        frame_file = frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.save(frame_file, quality=88)
        
        if f_idx % 200 == 0:
            print(f"    -> Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")
            
    # 4. Codificación Final en MP4 FastStart 1080p
    print("\n[PASO 4/4] Ensamblando video master 1080p con FFmpeg...")
    final_output = RUNTIME / "OpenClaw_Universal_OS_Masterclass_1080p.mp4"
    
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
    print("  🏆 MASTERCLASS 1080P UNIVERSAL GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos")
    print("  Visual:   Teleprompter Karaoke + Avatar Limpio + 48kHz Broadcast")
    print("=" * 60)
    
    # Limpieza de fotogramas temporales
    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    frames_dir.rmdir()
    
    return str(final_output)

if __name__ == "__main__":
    render_masterclass_video()
