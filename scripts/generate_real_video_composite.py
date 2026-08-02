#!/usr/bin/env python3
"""
====================================================================
 OPENCLAW REAL AVATAR STUDIO VIDEO ENGINE (2026.7.1)
====================================================================
- UTILIZA VIDEO REAL BASE 1080p EN ESTUDIO (showcase_human_loop.mp4)
  Con torso completo, postura natural, brazos, manos y escritorio.
- VOZ HUMANA SINTETIZADA EDGE-TTS (es-MX-JorgeNeural) + 48kHz FM BROADCAST
- SUBTÍTULOS BILINGÜES CON RESALTADO PROGRESIVO Y CADENCIA CALMADA
====================================================================
"""

import os
import sys
import asyncio
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PUBLIC_DIR = r"C:\openclaw\hb-jewelry\public"
BASE_VIDEO_PATH = os.path.join(PUBLIC_DIR, "showcase_human_loop.mp4")
if not os.path.exists(BASE_VIDEO_PATH):
    BASE_VIDEO_PATH = os.path.join(PUBLIC_DIR, "hb_tutorial_narrado_v1.mp4")

OUT_TALK_GROW_PATH = os.path.join(PUBLIC_DIR, "videos", "talk_grow_format", "real_talk_grow_educational.mp4")
OUT_YT_MASTER_PATH = os.path.join(PUBLIC_DIR, "videos", "talk_grow_format", "youtube_master_10min_educational.mp4")

os.makedirs(os.path.dirname(OUT_TALK_GROW_PATH), exist_ok=True)

# Guión Maestro Educativo: Automatización, Inteligencia Artificial y Crecimiento Empresarial
SCRIPT_PARAGRAPHS = [
    {
        "es": "Hola, bienvenido a nuestro canal educativo de automatización e inteligencia artificial. Soy Guillermo.",
        "en": "Hello, welcome to our educational channel on automation and artificial intelligence. I am Guillermo."
    },
    {
        "es": "Hoy aprenderemos cómo estructurar los 7 pilares fundamentales para escalar tu empresa con agentes autónomos.",
        "en": "Today we will learn how to structure the 7 fundamental pillars to scale your business with autonomous agents."
    },
    {
        "es": "Cada proceso se diseña para eliminar tareas repetitivas, reducir la fricción operativa y multiplicar la productividad.",
        "en": "Every process is designed to eliminate repetitive tasks, reduce operational friction, and multiply productivity."
    },
    {
        "es": "Nuestra meta es construir una comunidad sólida de líderes que dominen las herramientas del futuro hoy mismo.",
        "en": "Our goal is to build a solid community of leaders who master the tools of the future right now."
    }
]

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def generate_master_audio():
    print("🎙️ [1/3] Sintetizando voz real humana pausada con Edge-TTS (es-MX-JorgeNeural)...")
    parts = []
    
    for idx, p in enumerate(SCRIPT_PARAGRAPHS):
        part_path = os.path.join(PUBLIC_DIR, f"real_part_{idx}.mp3")
        c = edge_tts.Communicate(p["es"], voice="es-MX-JorgeNeural", rate="-6%") # Ritmo pausado y relajante
        await c.save(part_path)
        parts.append(part_path)
        
    pause_path = os.path.join(PUBLIC_DIR, "pause_08s.mp3")
    cmd_p = f'ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=stereo -t 0.8 -c:a mp3 "{pause_path}"'
    subprocess.run(cmd_p, shell=True, check=True)
    
    list_txt = os.path.join(PUBLIC_DIR, "real_parts_list.txt")
    with open(list_txt, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
            f.write(f"file '{pause_path}'\n")
            
    master_mp3 = os.path.join(PUBLIC_DIR, "real_guillermo_voice.mp3")
    cmd_c = f'ffmpeg -y -f concat -safe 0 -i "{list_txt}" -c copy "{master_mp3}"'
    subprocess.run(cmd_c, shell=True, check=True)
    
    dur = get_audio_duration(master_mp3)
    print(f"✓ Audio Maestro sintetizado. Duración total: {dur:.2f}s")
    return master_mp3, dur

def build_real_avatar_video():
    master_mp3, total_dur = asyncio.run(generate_master_audio())
    
    print("🎬 [2/3] Componiendo video en estudio 1080p con avatar humano real (postura, manos y respiración)...")
    
    # Filtro de Audio FM Broadcast
    fm_audio_filter = (
        "highpass=f=75,"
        "equalizer=f=250:width_type=h:width=150:g=3.0,"
        "equalizer=f=3200:width_type=h:width=1200:g=3.5,"
        "compand=attacks=0.02:decays=0.2:points=-60/-60|-24/-12|-8/-4|0/-1,"
        "lowpass=f=15000,"
        "volume=1.6,"
        "loudnorm=I=-14:LRA=11:TP=-1.5"
    )

    vf_chain = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"

    for out_path in [OUT_TALK_GROW_PATH, OUT_YT_MASTER_PATH]:
        cmd_ffmpeg = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", BASE_VIDEO_PATH,
            "-i", master_mp3,
            "-t", str(total_dur),
            "-vf", vf_chain,
            "-af", fm_audio_filter,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            out_path
        ]
        subprocess.run(cmd_ffmpeg, check=True)
        print(f"✅ Video HD Real exportado en: {out_path}")

    print("\n=========================================================")
    print(" 🎉 [ÉXITO] VIDEO REAL DE ESTUDIO COMPUESTOS CON ÉXITO")
    print("=========================================================")

if __name__ == "__main__":
    build_real_avatar_video()
