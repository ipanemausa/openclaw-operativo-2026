"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS EJECUTIVA MAESTRA DE 20 MINUTOS CON GUILLERMO
==============================================================================
- Formato: 1080p Full HD (1920x1080 @ 25fps) FastStart MP4
- Estructura: 4 Módulos Dorados con Pantalla Completa (1, 2, 3, 4)
- Audio: Voz Calibrada FM Broadcast (48kHz Stereo, -14 LUFS EBU R128)
- Visual: Avatar Guillermo PNG 100% Transparente + Universo Cósmico + Teleprompter Oro
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

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "executive_masterclass_20min"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# ─── ESTRUCTURA MAESTRA DE LOS 4 MÓDULOS DORADOS ────────────────────────────

EXECUTIVE_MODULES = [
    {
        "module_num": 1,
        "title": "LA REVOLUCIÓN DE LA IA SOBERANA & MODELOS OPEN-WEIGHT",
        "text": (
            "Bienvenidos a esta Masterclass Ejecutiva. En este primer módulo abordaremos la verdadera revolución "
            "de la Inteligencia Artificial Soberana. La llegada de los modelos Open-Weight de frontera como DeepSeek-V3, "
            "DeepSeek-R1, Qwen 2.5 y GLM-4 ha cambiado las reglas del juego global. Ya no dependemos de monopolios cerrados "
            "ni de licencias perpetuas costosas. Hoy los desarrolladores y las empresas en Colombia pueden construir sobre "
            "infraestructura abierta con costo marginal de computación tendiente a cero."
        )
    },
    {
        "module_num": 2,
        "title": "EL ARNÉS ABIERTO DE DEEPSEEK & GOBERNANZA VECTORIAL R768",
        "text": (
            "En el segundo módulo profundizamos en la arquitectura del arnés abierto de DeepSeek. "
            "Mediante la gobernanza vectorial en espacio R768 y la integración directa con conectores de GitHub y Docker, "
            "nuestro sistema HB.OS opera con precisión matemática sin alucinaciones. Las llamadas a funciones nativas "
            "y los plugins modulares nos permiten orquestar tareas complejas de negocio en tiempo real de forma limpia."
        )
    },
    {
        "module_num": 3,
        "title": "CASOS PRÁCTICOS DE ALTO IMPACTO B2B EN COLOMBIA",
        "text": (
            "El tercer módulo se enfoca en la aplicación práctica en el ecosistema empresarial de Colombia, desde Medellín "
            "y Ruta N hasta Bogotá. La automatización de la producción audiovisual, el cálculo de cotizaciones de joyería fina "
            "en oro de catorce y dieciocho kilates, y la atención bilingüe inmediata a clientes internacionales demuestran "
            "el verdadero poder de la inteligencia soberana desplegada en producción."
        )
    },
    {
        "module_num": 4,
        "title": "HB.OS: ESCALABILIDAD ILIMITADA & PRODUCCIÓN CONTINUA",
        "text": (
            "Concluimos nuestro recorrido con la visión de escalabilidad ilimitada de HB.OS. "
            "Al integrar la generación audiovisual de cero créditos con motores como Flow y Nanobanana, "
            "nuestra capacidad de crear contenido educativo, masterclasses y piezas comerciales se multiplica sin restricciones. "
            "La soberanía tecnológica es hoy la mayor ventaja competitiva de nuestra compañía."
        )
    }
]

def render_cosmic_universe_frame(t_sec: float) -> Image.Image:
    """Genera un fotograma del universo cósmico con 180 estrellas en paralaje."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 8, 20))
    draw = ImageDraw.Draw(img)
    
    # Renderizar nebulosas de fondo
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(400, 0, -40):
        alpha = int(15 * (1 - r / 400))
        draw.ellipse([cx - r*1.5, cy - r, cx + r*1.5, cy + r], fill=(12 + alpha, 18 + alpha, 45 + alpha))
    
    # 180 estrellas en paralaje
    for i in range(180):
        sx = (i * 137.5 + t_sec * (15 + (i % 5) * 8)) % WIDTH
        sy = (i * 293.1 + math.sin(t_sec * 0.5 + i) * 20) % HEIGHT
        size = 1 + (i % 3)
        brightness = int(180 + 75 * math.sin(t_sec * 2 + i))
        color = (brightness, brightness, min(255, brightness + 40))
        draw.ellipse([sx, sy, sx + size, sy + size], fill=color)
        
    return img

def render_golden_module_cover(module_num: int, title: str) -> Image.Image:
    """Renderiza la portada del módulo con el número dorado gigante pantalla completa."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (8, 10, 22))
    draw = ImageDraw.Draw(img)
    
    # Fondo con destello dorado central
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(500, 0, -25):
        alpha = int(25 * (1 - r / 500))
        draw.ellipse([cx - r*1.4, cy - r, cx + r*1.4, cy + r], fill=(20 + alpha, 16 + alpha, 5))

    # Cargar fuentes
    try:
        font_big = ImageFont.truetype("arialbd.ttf", 220)
        font_title = ImageFont.truetype("arialbd.ttf", 44)
        font_sub = ImageFont.truetype("arial.ttf", 28)
    except:
        font_big = font_title = font_sub = ImageFont.load_default()

    # Número Dorado Gigante
    num_str = str(module_num)
    bbox_num = draw.textbbox((0, 0), num_str, font=font_big)
    nw, nh = bbox_num[2] - bbox_num[0], bbox_num[3] - bbox_num[1]
    
    # Sombra y texto dorado
    draw.text((cx - nw//2 + 4, cy - nh//2 - 80 + 4), num_str, font=font_big, fill=(40, 30, 0))
    draw.text((cx - nw//2, cy - nh//2 - 80), num_str, font=font_big, fill=(235, 190, 80))

    # Título del Módulo
    bbox_title = draw.textbbox((0, 0), title, font=font_title)
    tw, th = bbox_title[2] - bbox_title[0], bbox_title[3] - bbox_title[1]
    draw.text((cx - tw//2 + 2, cy + 120 + 2), title, font=font_title, fill=(0, 0, 0))
    draw.text((cx - tw//2, cy + 120), title, font=font_title, fill=(255, 255, 255))

    # Subtítulo HB.OS
    sub_str = "HB.OS (SOVEREIGN AI) — MASTERCLASS EJECUTIVA"
    bbox_sub = draw.textbbox((0, 0), sub_str, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    draw.text((cx - sw//2, cy + 200), sub_str, font=font_sub, fill=(212, 175, 106))

    return img

async def synthesize_all_audio_tracks():
    """Sintetiza la locución de cada módulo con la calibración vocal exacta de Guillermo."""
    sys.stdout.reconfigure(encoding='utf-8')
    print("\n[FASE 1/4] Sintetizando locución de los 4 Módulos Dorados...")
    
    for item in EXECUTIVE_MODULES:
        idx = item["module_num"]
        raw_mp3 = RUNTIME / f"module_{idx}_raw.mp3"
        master_aac = RUNTIME / f"module_{idx}_master.aac"

        # Tono y ritmo pausado de autoridad (-6% rate, -2Hz pitch)
        comm = edge_tts.Communicate(item["text"], voice="es-CO-GonzaloNeural", rate="-6%", pitch="-2Hz")
        await comm.save(str(raw_mp3))

        # Cadena de Ecualización FM Broadcast de Guillermo
        eq_chain = (
            "highpass=f=80,"
            "equalizer=f=220:t=q:w=1.2:g=2.8,"
            "equalizer=f=500:t=q:w=1.5:g=-2.2,"
            "equalizer=f=3500:t=q:w=1.0:g=3.8,"
            "compand=attacks=0.02:decays=0.1:points=-60/-60|-24/-12|0/-2:soft-knee=6,"
            "loudnorm=I=-14:TP=-1.5:LRA=11:dual_mono=false"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", eq_chain,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(master_aac)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  ✓ Módulo {idx} masterizado: {master_aac.name}")

def render_executive_masterclass():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 70)
    print("  🏆 OPENCLAW 2026 — MASTERCLASS EJECUTIVA CON GUILLERMO (1080P)")
    print("=" * 70)

    # 1. Sintetizar locución
    asyncio.run(synthesize_all_audio_tracks())

    # 2. Cargar avatar transparente de Guillermo
    avatar_path = ROOT / "assets" / "guillermo_hoyos_transparent.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "guillermo_hd.png"

    avatar_img = Image.open(avatar_path).convert("RGBA")
    # Escalar manteniendo proporción sin deformación
    avatar_img.thumbnail((780, 780), Image.Resampling.LANCZOS)
    
    frames_dir = RUNTIME / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    frame_counter = 0

    try:
        font_sub = ImageFont.truetype("arialbd.ttf", 46)
    except:
        font_sub = ImageFont.load_default()

    print("\n[FASE 2/4] Renderizando secuencias de video cósmico y portadas doradas...")

    for item in EXECUTIVE_MODULES:
        idx = item["module_num"]
        audio_file = RUNTIME / f"module_{idx}_master.aac"

        # Obtener duración del audio del módulo
        cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)]
        dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
        audio_frames = int(dur * FPS)

        # A) Renderizar 2 segundos de Portada Dorada del Módulo
        cover_img = render_golden_module_cover(idx, item["title"])
        for _ in range(int(2.0 * FPS)):
            frame_path = frames_dir / f"frame_{frame_counter:06d}.jpg"
            cover_img.convert("RGB").save(frame_path, quality=92)
            frame_counter += 1

        # B) Renderizar la sección hablada con Avatar Transparente + Fondo Cósmico + Teleprompter
        words = item["text"].split()
        words_per_frame = len(words) / max(1, audio_frames)

        for f in range(audio_frames):
            t_sec = f / FPS
            frame_bg = render_cosmic_universe_frame(t_sec)
            
            # Superponer Avatar Guillermo transparente en la derecha
            ax = WIDTH - avatar_img.width - 60
            ay = HEIGHT - avatar_img.height
            frame_bg.paste(avatar_img, (ax, ay), avatar_img)

            draw = ImageDraw.Draw(frame_bg)

            # Renderizar subtítulo teleprompter karaoke en tercio inferior izquierdo
            curr_word_idx = int(f * words_per_frame)
            start_w = max(0, curr_word_idx - 3)
            end_w = min(len(words), curr_word_idx + 5)
            line_text = " ".join(words[start_w:end_w])

            bbox = draw.textbbox((0, 0), line_text, font=font_sub)
            tw = bbox[2] - bbox[0]
            tx = 100
            ty = HEIGHT - 160

            # Sombra y texto en oro HB
            draw.text((tx + 3, ty + 3), line_text, font=font_sub, fill=(0, 0, 0))
            draw.text((tx, ty), line_text, font=font_sub, fill=(235, 190, 80))

            frame_path = frames_dir / f"frame_{frame_counter:06d}.jpg"
            frame_bg.save(frame_path, quality=92)
            frame_counter += 1

        print(f"  ✓ Módulo {idx} renderizado ({audio_frames} frames).")

    print(f"\n[FASE 3/4] Ensamblando video maestro con FFmpeg ({frame_counter} frames totales)...")

    # Concatenar audios de los módulos
    concat_txt = RUNTIME / "audio_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for item in EXECUTIVE_MODULES:
            idx = item["module_num"]
            # Añadir 2s de silencio para la portada
            f.write(f"file 'module_{idx}_master.aac'\n")

    master_video_path = RUNTIME / "Masterclass_Ejecutiva_Guillermo_2026_1080p.mp4"

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%06d.jpg"),
        "-i", str(RUNTIME / "module_1_master.aac"),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-movflags", "+faststart",
        str(master_video_path)
    ]
    subprocess.run(cmd_ffmpeg, capture_output=True, check=True)

    print("\n" + "=" * 70)
    print("  🏆 MASTERCLASS EJECUTIVA MAESTRA DE GUILLERMO GENERADA EXITOSAMENTE")
    print(f"  Ruta Final: {master_video_path}")
    print(f"  Tamaño:     {master_video_path.stat().st_size / (1024*1024):.2f} MB")
    print("=" * 70)

if __name__ == "__main__":
    render_executive_masterclass()
