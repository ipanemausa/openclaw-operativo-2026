#!/usr/bin/env python3
"""
====================================================================
 OPENCLAW YOUTUBE PRACTICE & CONVERSATION VIDEO ENGINE (2026.7.1)
====================================================================
- SÍNTESIS DE VOZ REAL HUMANA (Edge-TTS 48kHz Estéreo FM Broadcast)
- SINCRONIZACIÓN PALABRA POR PALABRA (WORD-BY-WORD HIGHLIGHTING KARAOKE)
- CADENCIA PAUSADA, AMIGABLE Y CON AUTORIDAD (0.6s Pausas de Respiración)
- RENDERIZADO 1080p EN 4 CAPAS (Blur + Avatar 3D + Teleprompter + Voz FM)
====================================================================
"""

import os
import sys
import math
import json
import asyncio
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont

# Set UTF-8 stdout encoding for Windows PowerShell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PUBLIC_DIR = r"C:\openclaw\hb-jewelry\public"
OUT_TALK_GROW_PATH = os.path.join(PUBLIC_DIR, "videos", "talk_grow_format", "real_talk_grow_educational.mp4")
OUT_YT_MASTER_PATH = os.path.join(PUBLIC_DIR, "videos", "talk_grow_format", "youtube_master_10min_educational.mp4")

os.makedirs(os.path.dirname(OUT_TALK_GROW_PATH), exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Avatar Image
AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar_transparent.png")
if not os.path.exists(AVATAR_PATH):
    AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar_pro.png")

base_avatar_img = Image.open(AVATAR_PATH).convert("RGBA")
avatar_w = 800
avatar_h = int(base_avatar_img.height * (avatar_w / base_avatar_img.width))
base_avatar_img = base_avatar_img.resize((avatar_w, avatar_h), Image.Resampling.LANCZOS)

# Script Educativo Pausado con Estructura de Conversación y Práctica
SCRIPT_ITEMS = [
    {
        "es": "Hola, bienvenido a la academia HB Jewelry. Soy Guillermo, tu avatar de inteligencia artificial.",
        "en": "Hello, welcome to HB Jewelry academy. I am Guillermo, your AI avatar.",
        "voice": "es-MX-JorgeNeural"
    },
    {
        "es": "Hoy aprenderemos los 7 hacks avanzados para automatizar tu empresa con Claude 4.6.",
        "en": "Today we will learn the 7 advanced hacks to automate your business with Claude 4.6.",
        "voice": "es-MX-JorgeNeural"
    },
    {
        "es": "Hack 1: Prompting estructurado con protocolos blindados y artefactos interactivos.",
        "en": "Hack 1: Structured prompting with hard-armored protocols and interactive artifacts.",
        "voice": "es-MX-JorgeNeural"
    },
    {
        "es": "Hack 2: Integración de base de datos vectorial de 768 dimensiones en Firestore.",
        "en": "Hack 2: 768-dimensional vector database integration in Firestore.",
        "voice": "es-MX-JorgeNeural"
    },
    {
        "es": "Hack 3: Automatización de ventas por WhatsApp Business a cero costo por transacción.",
        "en": "Hack 3: Sales automation via WhatsApp Business at zero transaction cost.",
        "voice": "es-MX-JorgeNeural"
    },
    {
        "es": "Hack 4: Respaldo continuo en tiempo real hacia Google Drive de 5 Terabytes.",
        "en": "Hack 4: Continuous real-time backup to 5 Terabyte Google Drive.",
        "voice": "es-MX-JorgeNeural"
    },
    {
        "es": "Cada concepto está diseñado para brindarte seguridad, autoridad y crecimiento ilimitado.",
        "en": "Every concept is designed to give you security, authority, and unlimited growth.",
        "voice": "es-MX-JorgeNeural"
    }
]

def get_audio_duration(file_path):
    """Obtiene la duración exacta del audio usando ffprobe"""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_all_speech():
    """Paso 1: Genera archivos de audio individuales con Edge-TTS"""
    print("🎙️ [1/4] Sintetizando voz humana ecualizada con Edge-TTS (es-MX-JorgeNeural)...")
    audio_files = []
    
    for idx, item in enumerate(SCRIPT_ITEMS):
        out_wav = os.path.join(PUBLIC_DIR, f"speech_part_{idx}.mp3")
        c = edge_tts.Communicate(item["es"], voice=item["voice"], rate="-5%") # 5% más pausada para tono amigable
        await c.save(out_wav)
        dur = get_audio_duration(out_wav)
        item["audio_file"] = out_wav
        item["duration"] = dur
        print(f"   Part {idx+1}/{len(SCRIPT_ITEMS)}: Duración = {dur:.2f}s | Text = '{item['es'][:40]}...'")
        audio_files.append(out_wav)
        
    return audio_files

def apply_avatar_motion(avatar_base, t, speech_active):
    """Paso 2: Genera movimiento fisiológico calmado y lip-sync sincronizado"""
    frame_avatar = avatar_base.copy()
    
    # 1. Balanceo Fisiológico Lento (Respiración Calmada)
    body_x_shift = math.sin(t * 1.2) * 5
    body_y_shift = math.cos(t * 1.6) * 4
    
    # 2. Rotación de Cabeza Anatómica
    head_angle = math.sin(t * 1.0) * 1.5
    frame_avatar = frame_avatar.rotate(head_angle, resample=Image.Resampling.BICUBIC, expand=False)
    
    # 3. Movimiento Bucal cuando hay voz activa
    if speech_active:
        speech_amp = abs(math.sin(t * 14.0) * math.cos(t * 8.0))
        if speech_amp > 0.12:
            draw_av = ImageDraw.Draw(frame_avatar)
            mouth_center_x = int(avatar_w * 0.48)
            mouth_center_y = int(avatar_h * 0.38)
            mouth_w = int(24 + speech_amp * 20)
            mouth_h = int(6 + speech_amp * 16)
            
            # Cavidad Bucal
            draw_av.ellipse(
                [mouth_center_x - mouth_w//2, mouth_center_y - mouth_h//2,
                 mouth_center_x + mouth_w//2, mouth_center_y + mouth_h//2],
                fill=(35, 12, 12, 240)
            )
            # Lengua
            draw_av.ellipse(
                [mouth_center_x - mouth_w//3, mouth_center_y + 1,
                 mouth_center_x + mouth_w//3, mouth_center_y + mouth_h//2 - 1],
                fill=(190, 65, 65, 240)
            )

    # 4. Parpadeo Ocular Fisiológico (cada 3.8s)
    blink_cycle = (t * 1000) % 3800
    if 3500 < blink_cycle < 3650:
        draw_av = ImageDraw.Draw(frame_avatar)
        eye_y = int(avatar_h * 0.30)
        eye1_x = int(avatar_w * 0.43)
        eye2_x = int(avatar_w * 0.53)
        draw_av.line([eye1_x - 13, eye_y, eye1_x + 13, eye_y], fill=(40, 20, 15, 240), width=4)
        draw_av.line([eye2_x - 13, eye_y, eye2_x + 13, eye_y], fill=(40, 20, 15, 240), width=4)

    return frame_avatar, body_x_shift, body_y_shift

def render_practice_video():
    # 1. Sintetizar voz
    asyncio.run(synthesize_all_speech())
    
    # 2. Concatenar Audio Completo con Pausas
    print("🔊 [2/4] Mezclando audio maestro con pausas respiratorias (0.6s)...")
    concat_list_file = os.path.join(PUBLIC_DIR, "audio_concat_list.txt")
    pause_file = os.path.join(PUBLIC_DIR, "pause_06s.mp3")
    
    # Generar mp3 de pausa de 0.6s si no existe
    cmd_pause = 'ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=stereo -t 0.6 -c:a mp3 "' + pause_file + '"'
    subprocess.run(cmd_pause, shell=True, check=True)
    
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for idx, item in enumerate(SCRIPT_ITEMS):
            f.write(f"file '{item['audio_file']}'\n")
            f.write(f"file '{pause_file}'\n")
            
    master_audio = os.path.join(PUBLIC_DIR, "master_speech_voice.mp3")
    cmd_concat_audio = f'ffmpeg -y -f concat -safe 0 -i "{concat_list_file}" -c copy "{master_audio}"'
    subprocess.run(cmd_concat_audio, shell=True, check=True)
    
    total_audio_duration = get_audio_duration(master_audio)
    print(f"✓ Audio Maestro generado. Duración total: {total_audio_duration:.2f}s")
    
    # 3. Renderizar Fotogramas 1080p con Resaltado Palabra por Palabra (Word Karaoke Sync)
    print(f"🎬 [3/4] Renderizando fotogramas 1080p con Resaltado Palabra por Palabra...")
    temp_dir = os.path.join(PUBLIC_DIR, "temp_yt_frames")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 30)
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
    except Exception:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    total_frames = int(total_audio_duration * FPS)
    
    # Calcular marcas de tiempo para cada frase
    current_t_cursor = 0.0
    for item in SCRIPT_ITEMS:
        item["start_t"] = current_t_cursor
        item["end_t"] = current_t_cursor + item["duration"]
        current_t_cursor += item["duration"] + 0.6 # Pausa
        
    for f_idx in range(total_frames):
        t = f_idx / FPS
        
        # Encontrar item activo
        active_item = None
        speech_active = False
        for item in SCRIPT_ITEMS:
            if item["start_t"] <= t <= item["end_t"]:
                active_item = item
                speech_active = True
                break
            elif t < item["start_t"]:
                break
                
        if not active_item:
            # En pausa, mostrar la última frase en tono tenue
            active_item = SCRIPT_ITEMS[-1]
            speech_active = False

        # --- CAPA 1: Fondo Gradiente 3D HSL & Depth Blur ---
        base = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 255))
        draw = ImageDraw.Draw(base)

        for r in range(700, 0, -30):
            alpha = int(50 * (1 - r / 700))
            draw.ellipse([WIDTH/2 - r, HEIGHT/2 - r, WIDTH/2 + r, HEIGHT/2 + r], fill=(30, 27, 75, alpha))

        # --- CAPA 2: Avatar HD 3D Guillermo AI ---
        anim_avatar, body_x, body_y = apply_avatar_motion(base_avatar_img, t, speech_active)
        avatar_x = int(WIDTH - avatar_w - 60 + body_x)
        avatar_y = int(HEIGHT - avatar_h + body_y + 15)
        base.paste(anim_avatar, (avatar_x, avatar_y), anim_avatar)

        # --- HEADER SUPERIOR LIMPIO SIN CORDAL DE SOBREPOSICIÓN ---
        badge_x, badge_y = 60, 45
        badge_w, badge_h = 440, 52
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=26, fill=(30, 41, 59, 240), outline=(212, 175, 106, 160), width=2)
        draw.text((badge_x + 20, badge_y + 12), "GUILLERMO AI · PRÁCTICA & CURSOS 🔴", font=font_badge, fill=(212, 175, 106, 255))

        # --- CAPA 3: Teleprompter Resaltado Palabra por Palabra (Word-by-Word Karaoke Sync) ---
        # Caja contenedora del texto en el tercio inferior/medio
        box_x, box_y = 60, 380
        box_w, box_h = 1000, 420
        draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=16, fill=(15, 23, 42, 220), outline=(212, 175, 106, 80), width=2)

        # Título de la Frase Activa
        draw.text((box_x + 30, box_y + 25), "ESPAÑOL (VOZ REAL ECUALIZADA FM):", font=font_badge, fill=(212, 175, 106, 255))
        
        words = active_item["es"].split()
        if speech_active:
            item_dur = active_item["duration"]
            t_in_item = t - active_item["start_t"]
            progress_ratio = min(1.0, max(0.0, t_in_item / item_dur))
            active_word_idx = min(int(progress_ratio * len(words)), len(words) - 1)
        else:
            active_word_idx = len(words) - 1

        # Renderizar palabras con resaltado verde/dorado
        cur_x = box_x + 30
        cur_y = box_y + 70
        max_line_w = box_w - 60

        for w_idx, word in enumerate(words):
            word_str = word + " "
            bbox = draw.textbbox((0, 0), word_str, font=font_large)
            w_width = bbox[2] - bbox[0]

            if cur_x + w_width > box_x + max_line_w:
                cur_x = box_x + 30
                cur_y += 65

            # Determinar color de la palabra
            if w_idx == active_word_idx and speech_active:
                # PALABRA ACTIVA HABLANDO: Verde neón iluminado + caja de contraste
                draw.rounded_rectangle([cur_x - 4, cur_y - 2, cur_x + w_width + 2, cur_y + 52], radius=6, fill=(132, 204, 22, 240))
                draw.text((cur_x, cur_y), word_str, font=font_large, fill=(0, 0, 0, 255))
            elif w_idx < active_word_idx:
                # PALABRAS YA HABLADAS: Dorado cálido
                draw.text((cur_x, cur_y), word_str, font=font_large, fill=(212, 175, 106, 255))
            else:
                # PALABRAS FUTURAS: Blanco suave
                draw.text((cur_x, cur_y), word_str, font=font_large, fill=(226, 232, 240, 220))

            cur_x += w_width

        # Traducción al Inglés abajo
        draw.text((box_x + 30, box_y + 290), "ENGLISH (AUTOMATIC SUBTITLE):", font=font_badge, fill=(148, 163, 184, 255))
        draw.text((box_x + 30, box_y + 330), active_item["en"], font=font_sub, fill=(203, 213, 225, 255))

        # Oscilograma FM Broadcast inferior
        wave_y = HEIGHT - 50
        dot_spacing = 28
        num_dots = WIDTH // dot_spacing
        for i in range(num_dots):
            dot_x = i * dot_spacing + 15
            dot_h = int(abs(math.sin(t * 6 + i * 0.4) * math.cos(t * 2.5 + i * 0.2)) * 28) + 4
            draw.line([(dot_x, wave_y - dot_h), (dot_x, wave_y + dot_h)], fill=(212, 175, 106, 200) if speech_active else (71, 85, 105, 150), width=3)

        frame_path = os.path.join(temp_dir, f"frame_{f_idx:04d}.png")
        base.save(frame_path, "PNG")

    # 4. Ensamble de Video FFmpeg con Filtros de Audio FM Broadcast
    print("⚡ [4/4] Ensamblando video 1080p con cadena de audio FM Broadcast EBU R128 (-14 LUFS)...")
    
    fm_audio_filter = (
        "highpass=f=75,"
        "equalizer=f=250:width_type=h:width=150:g=3.0,"
        "equalizer=f=3200:width_type=h:width=1200:g=3.5,"
        "compand=attacks=0.02:decays=0.2:points=-60/-60|-24/-12|-8/-4|0/-1,"
        "lowpass=f=15000,"
        "volume=1.6,"
        "loudnorm=I=-14:LRA=11:TP=-1.5"
    )

    # Exportar a ambas rutas
    for out_p in [OUT_TALK_GROW_PATH, OUT_YT_MASTER_PATH]:
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(temp_dir, "frame_%04d.png"),
            "-i", master_audio,
            "-t", str(total_audio_duration),
            "-af", fm_audio_filter,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            out_p
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"✅ Video exportado exitosamente: {out_p}")

    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    print("\n=========================================================")
    print(" 🎉 [ÉXITO] VIDEO DE PRÁCTICA Y CONVERSACIÓN GENERADO CON ÉXITO")
    print("=========================================================")

if __name__ == "__main__":
    render_practice_video()
