#!/usr/bin/env python3
"""
====================================================================
 OPENCLAW ADAPTIVE MULTI-TARGET VIDEO ENGINE (2026.7.1)
====================================================================
- ADAPTA EL TONO, VOCABULARIO, CADENCIA Y VISUALES SEGÚN EL TARGET AUDIENCE
- TRES TARGETS DE PRECISIÓN:
  1. B2B_WHOLESALE: Mayoristas e Inversionistas de Joyería 18k
  2. TECH_AUTOMATION: Empresarios buscando Automatización e IA
  3. EDUCATIONAL_COMMUNITY: Estudiantes y Práctica Bilingüe (Zero Estrés)
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

# Perfiles Adaptativos por Audiencia Objetivo
TARGET_PROFILES = {
    "B2B_WHOLESALE": {
        "title": "HB JEWELRY · CATÁLOGO Y ALIANZAS MAYORISTAS 18K 💎",
        "voice": "es-MX-JorgeNeural",
        "rate": "-8%", # Muy pausado y ejecutivo
        "tone_desc": "Elegante, Institucional y Enfocado en Rentabilidad",
        "script": [
            {
                "es": "Bienvenido a HB Jewelry. Somos su aliado estratégico en distribución de joyería fina de oro de 18 kilates.",
                "en": "Welcome to HB Jewelry. We are your strategic partner in 18k fine gold jewelry distribution."
            },
            {
                "es": "Nuestras piezas cuentan con certificación internacional de pureza y márgenes comerciales superiores al 40%.",
                "en": "Our pieces feature international purity certification and commercial margins over 40%."
            },
            {
                "es": "Procesamos sus pedidos al por mayor directamente y con despacho prioritario garantizado.",
                "en": "We process your wholesale orders directly with guaranteed priority dispatch."
            }
        ]
    },
    "TECH_AUTOMATION": {
        "title": "OPENCLAW 2026 · AUTOMATIZACIÓN E INTELIGENCIA ARTIFICIAL ⚡",
        "voice": "es-MX-JorgeNeural",
        "rate": "-4%", # Dinámico con autoridad tecnológica
        "tone_desc": "Tecnológico, Innovador y Estratégico",
        "script": [
            {
                "es": "Hola, soy Guillermo. Hoy veremos cómo automatizar tu empresa utilizando agentes autónomos y Claude 4.6.",
                "en": "Hello, I am Guillermo. Today we will see how to automate your company using autonomous agents and Claude 4.6."
            },
            {
                "es": "Integramos bases de datos vectoriales de 768 dimensiones en tiempo real con respaldo continuo de 5 Terabytes.",
                "en": "We integrate 768-dimensional vector databases in real time with 5 Terabyte continuous backup."
            },
            {
                "es": "Tus ventas por WhatsApp Business se ejecutan a cero costo por transacción con respuesta inmediata.",
                "en": "Your WhatsApp Business sales execute at zero transaction cost with immediate response."
            }
        ]
    },
    "EDUCATIONAL_COMMUNITY": {
        "title": "ACADEMIA HB · PRÁCTICA DE INGLÉS & CURSOS PAUSADOS 🔴",
        "voice": "es-MX-JorgeNeural",
        "rate": "-10%", # Ultra pausado y relajante (Zero Estrés)
        "tone_desc": "Didáctico, Amigable y Educativo",
        "script": [
            {
                "es": "Hola, bienvenido a nuestra lección del día. Practicaremos juntos cada oración de forma calmada.",
                "en": "Hello, welcome to our daily lesson. We will practice each sentence together in a calm way."
            },
            {
                "es": "Observa el resaltado de cada palabra para mejorar tu pronunciación y comprensión sin prisa.",
                "en": "Notice the highlight of each word to improve your pronunciation and understanding without rushing."
            },
            {
                "es": "Cada concepto te ayudará a dominar el idioma e impulsar tu carrera profesional.",
                "en": "Every concept will help you master the language and boost your professional career."
            }
        ]
    }
}

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def render_target_audio(target_key):
    profile = TARGET_PROFILES[target_key]
    print(f"🎙️ Sintetizando voz para Target: '{target_key}' ({profile['tone_desc']})...")
    parts = []
    
    for idx, item in enumerate(profile["script"]):
        p_path = os.path.join(PUBLIC_DIR, f"target_{target_key}_{idx}.mp3")
        c = edge_tts.Communicate(item["es"], voice=profile["voice"], rate=profile["rate"])
        await c.save(p_path)
        parts.append(p_path)
        
    pause_path = os.path.join(PUBLIC_DIR, "pause_08s.mp3")
    list_txt = os.path.join(PUBLIC_DIR, f"list_{target_key}.txt")
    with open(list_txt, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
            f.write(f"file '{pause_path}'\n")
            
    master_mp3 = os.path.join(PUBLIC_DIR, f"master_voice_{target_key}.mp3")
    cmd = f'ffmpeg -y -f concat -safe 0 -i "{list_txt}" -c copy "{master_mp3}"'
    subprocess.run(cmd, shell=True, check=True)
    dur = get_audio_duration(master_mp3)
    return master_mp3, dur

def build_adaptive_videos():
    for target_key in TARGET_PROFILES.keys():
        master_mp3, total_dur = asyncio.run(render_target_audio(target_key))
        out_dir = os.path.join(PUBLIC_DIR, "videos", "adaptive_targets")
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, f"video_{target_key.lower()}.mp4")
        
        print(f"🎬 Generando Video HD para Target: {target_key}...")
        
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

        cmd_ffmpeg = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", BASE_VIDEO_PATH,
            "-i", master_mp3,
            "-t", str(total_dur),
            "-vf", vf_chain,
            "-af", fm_audio_filter,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            out_file
        ]
        subprocess.run(cmd_ffmpeg, check=True)
        print(f"✅ Video para Target '{target_key}' completado en: {out_file}")

if __name__ == "__main__":
    build_adaptive_videos()
