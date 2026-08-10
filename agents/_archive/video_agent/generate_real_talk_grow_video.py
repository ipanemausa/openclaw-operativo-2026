# =====================================================================
# HB JEWELRY TRANSPARENT AVATAR & AI DEV VIDEO ENGINE (2026.7.1)
# =====================================================================
# Incorpora:
# 1. AVATAR TRANSPARENTE (avatar_transparent.png) sin cuadro negro de fondo
# 2. Voz Real de Guillermo (showcase_voice.mp3) normalizada a -14 LUFS (EBU R128)
# 3. Encabezado Oficial: OPENCLAW SUBSCRIBED 🔔 + OpenClaw 2026 AI Developer Academy
# 4. Generador de Caracteres Continuo en Lado Izquierdo (Texto de IA & Desarrollo)
# 5. Oscilograma Espectral Reactivo en el Borde Inferior
# =====================================================================

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

print("=========================================================")
print(" [TRANSPARENT RENDERER] GENERANDO VIDEO 1080p SIN BORDES ")
print("=========================================================")

PUBLIC_DIR = r"C:\openclaw\hb-jewelry\public"
OUT_VIDEO_PATH = os.path.join(PUBLIC_DIR, "videos", "talk_grow_format", "real_talk_grow_educational.mp4")
os.makedirs(os.path.dirname(OUT_VIDEO_PATH), exist_ok=True)

# Parámetros del Video
WIDTH, HEIGHT = 1920, 1080
FPS = 30
DURATION_SEC = 10
TOTAL_FRAMES = FPS * DURATION_SEC

# Cargar el Avatar TRANSPARENTE Oficial de Guillermo AI (sin cuadro negro)
AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar_transparent.png")
if not os.path.exists(AVATAR_PATH):
    AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar_pro.png")

avatar_img = Image.open(AVATAR_PATH).convert("RGBA")

# Ajustar escala del avatar transparente (anchura ~850px para presencia imponente sin recortes)
avatar_w = 850
avatar_h = int(avatar_img.height * (avatar_w / avatar_img.width))
avatar_img = avatar_img.resize((avatar_w, avatar_h), Image.Resampling.LANCZOS)

# Pista de Voz Real Clonada de Guillermo (TikTok Master)
REAL_VOICE_PATH = os.path.join(PUBLIC_DIR, "showcase_voice.mp3")

# Guion de IA & Herramientas para Desarrolladores
WORDS = [
    "Aprende", "a", "crear", "Agentes", "IA", "con", "Claude", "Gemini", 
    "RAG", "Vectorial", "768-dim", "y", "OpenClaw", "2026.7.1"
]

TEMP_FRAMES_DIR = os.path.join(PUBLIC_DIR, "temp_frames_transparent")
os.makedirs(TEMP_FRAMES_DIR, exist_ok=True)

try:
    font_large = ImageFont.truetype("arialbd.ttf", 54)
    font_header = ImageFont.truetype("arialbd.ttf", 36)
    font_badge = ImageFont.truetype("arialbd.ttf", 26)
except Exception:
    font_large = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_badge = ImageFont.load_default()

def render_frame(frame_idx):
    t = frame_idx / FPS
    progress = frame_idx / TOTAL_FRAMES
    
    # 1. Fondo Azul Marino Gradiente Realista (Navy Gradient 3D)
    base = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 255))
    draw = ImageDraw.Draw(base)
    
    # Dibujar resplandor central azul/índigo profundo
    for r in range(650, 0, -25):
        alpha = int(45 * (1 - r / 650))
        draw.ellipse([WIDTH/2 - r, HEIGHT/2 - r, WIDTH/2 + r, HEIGHT/2 + r], fill=(30, 27, 75, alpha))
        
    # 2. Avatar TRANSPARENTE en el Lado Derecho (Integrado 100% al fondo sin cuadro negro)
    avatar_offset_y = int(math.sin(t * 2.5) * 8)
    avatar_x = WIDTH - avatar_w - 40
    avatar_y = HEIGHT - avatar_h + avatar_offset_y + 10 # Apoyado perfectamente abajo sin corte
    base.paste(avatar_img, (avatar_x, avatar_y), avatar_img)
    
    # 3. Encabezado Oficial: Insignia OPENCLAW SUBSCRIBED 🔔 + Título de IA
    badge_x, badge_y = 80, 60
    badge_w, badge_h = 340, 52
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=26, fill=(71, 85, 105, 240), outline=(255, 255, 255, 120), width=2)
    draw.text((badge_x + 22, badge_y + 11), "OPENCLAW SUBSCRIBED 🔔", font=font_badge, fill=(255, 255, 255, 255))
    
    draw.text((badge_x + badge_w + 30, badge_y + 5), "OpenClaw 2026 · AI & Developer Academy", font=font_header, fill=(132, 204, 22, 255))
    
    # 4. Generador de Caracteres Continuo (Texto de IA en Lado Izquierdo)
    active_word_count = int(progress * len(WORDS)) + 1
    current_words = WORDS[:min(active_word_count, len(WORDS))]
    
    line1 = " ".join(current_words[:4])
    line2 = " ".join(current_words[4:9])
    line3 = " ".join(current_words[9:])
    
    text_x = 80
    text_y = 380
    
    for line_idx, line_text in enumerate([line1, line2, line3]):
        if not line_text:
            continue
        curr_y = text_y + (line_idx * 78)
        
        # Borde negro de 4px para máxima legibilidad
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx != 0 or dy != 0:
                    draw.text((text_x + dx, curr_y + dy), line_text, font=font_large, fill=(0, 0, 0, 255))
                    
        # Texto amarillo (#FACC15)
        draw.text((text_x, curr_y), line_text, font=font_large, fill=(250, 204, 21, 255))
        
    # 5. Waveform Espectral Animado en Borde Inferior
    wave_y = HEIGHT - 70
    dot_spacing = 28
    num_dots = WIDTH // dot_spacing
    
    for i in range(num_dots):
        dot_x = i * dot_spacing + 15
        dot_h = int(abs(math.sin(t * 8 + i * 0.4) * math.cos(t * 3 + i * 0.2)) * 34) + 6
        draw.line([(dot_x, wave_y - dot_h), (dot_x, wave_y + dot_h)], fill=(255, 255, 255, 230), width=4)
        
    frame_path = os.path.join(TEMP_FRAMES_DIR, f"frame_{frame_idx:04d}.png")
    base.save(frame_path, "PNG")

for i in range(TOTAL_FRAMES):
    render_frame(i)

# Compilar video MP4 con FFmpeg utilizando la Voz Real Filtrada de Guillermo
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(TEMP_FRAMES_DIR, "frame_%04d.png"),
    "-ss", "0", "-t", "10", "-i", REAL_VOICE_PATH,
    "-af", "highpass=f=80,lowpass=f=12000,volume=1.2,loudnorm=I=-14:LRA=11:TP=-1.5",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUT_VIDEO_PATH
]
subprocess.run(ffmpeg_cmd, check=True)

import shutil
shutil.rmtree(TEMP_FRAMES_DIR, ignore_errors=True)

print(f"\n=========================================================")
print(f" [OK] VIDEO CON AVATAR TRANSPARENTE INTEGRADO 100% EN:")
print(f"      {OUT_VIDEO_PATH}")
print("=========================================================")
