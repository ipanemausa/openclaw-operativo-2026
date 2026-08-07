import os
import sys
import asyncio
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🎬 MOTOR AUDIOVISUAL CINEMÁTICO PERFECCIONADO 1080p (CINEMA STUDIO 2.5)")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "youtube_masterclass"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. LUNA CINEMÁTICA DIFUMINADA (DOF BOKEH BLUR) + CÍRCULO MORADO ESTÉTICO
MOON_BG_PNG = PUBLIC_DIR / "moon_cosmic_space_dof.png"

img = Image.new("RGBA", (1920, 1080), (6, 5, 16, 255))

# Círculo Morado Estético en el Centro/Derecha
aura = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
aura_draw = ImageDraw.Draw(aura)
aura_draw.ellipse([620, 80, 1560, 1020], fill=(129, 90, 248, 190))
aura_draw.ellipse([580, 40, 1600, 1060], fill=(212, 175, 106, 55))
aura = aura.filter(ImageFilter.GaussianBlur(35))
img = Image.alpha_composite(img, aura)

# Luna 3D Realista con Desenfoque de Profundidad (DOF Blur)
moon_img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
moon_draw = ImageDraw.Draw(moon_img)
moon_draw.ellipse([1400, 80, 1680, 360], fill=(240, 243, 246, 230), outline=(212, 175, 106, 170), width=3)
moon_draw.ellipse([1440, 80, 1720, 360], fill=(129, 90, 248, 110))
moon_img = moon_img.filter(ImageFilter.GaussianBlur(12))

img = Image.alpha_composite(img, moon_img)
img.convert("RGB").save(MOON_BG_PNG, "PNG")
print(f"🌌 Fondo Imagen Luna Difuminada (DOF Blur) Creado: {MOON_BG_PNG}")

# 2. GUION DE MASTERCLASS COMPLETA BILINGÜE
MASTERCLASS_EXTENDED_SCRIPT = [
    {
        "es": "Bienvenidos a la Masterclass Ejecutiva sobre la Revolución de Inteligencia Artificial B2B.",
        "en": "Welcome to the Executive Masterclass on the B2B Artificial Intelligence Revolution."
    },
    {
        "es": "Examinaremos detalladamente cómo sustituir suscripciones mensuales de software SaaS tradicional.",
        "en": "We will examine in detail how to replace legacy SaaS software subscriptions."
    },
    {
        "es": "Desplegamos agentes autónomos de Inteligencia Artificial directamente en tu servidor privado.",
        "en": "We deploy autonomous Artificial Intelligence agents directly on your private server."
    },
    {
        "es": "Logramos cero fricción operativa, cero licencias por usuario y control total de tus datos.",
        "en": "Achieving zero operational friction, zero per-user licensing, and total data sovereignty."
    },
    {
        "es": "Toda empresa sólida e inquebrantable se sustenta en cuatro pilares fundamentales:",
        "en": "Every resilient enterprise operates on four universal core pillars:"
    },
    {
        "es": "Atracción en Marketing, Conversión en Ventas, Logística y Finanzas.",
        "en": "Marketing Attraction, Sales Conversion, Logistics, and Finance."
    },
    {
        "es": "Conectamos un motor RAG vectorial de 768 dimensiones a tu base de datos Firestore.",
        "en": "Connecting a 768-dimensional RAG vector engine directly to your Firestore database."
    },
    {
        "es": "Tu sistema responde con precisión matemática basándose en documentos reales sin inventar información.",
        "en": "Your system responds with mathematical precision using verified documents without AI hallucinations."
    },
    {
        "es": "Aprovechando la actualización más reciente de Meta, tus clientes conversan mediante tu Alias empresarial.",
        "en": "Leveraging Meta's newest architecture, clients connect seamlessly via your business handle."
    },
    {
        "es": "Protegemos tus números telefónicos privados utilizando tokens encriptados BSUID.",
        "en": "We safeguard private phone numbers using encrypted BSUID tokens."
    },
    {
        "es": "Ofrecemos atención automatizada por WhatsApp Business las 24 horas del día a costo cero por mensaje.",
        "en": "Providing 24/7 automated WhatsApp Business customer support at zero cost per message."
    },
    {
        "es": "Procesamos video en micro-lotes de 15 fotogramas asistidos por restauración facial GFPGAN.",
        "en": "Processing AI video in 15-frame micro-batches enhanced by GFPGAN facial restoration."
    },
    {
        "es": "Producimos avatares humanos digitales en 1080p con voz estéreo de alta fidelidad 48kHz.",
        "en": "Producing 1080p digital human presenters with 48kHz FM broadcast stereo audio."
    },
    {
        "es": "Evitamos el pago de APIs en la nube y eliminamos por completo los costos por minuto de renderizado.",
        "en": "Eliminating cloud API subscription fees and zero per-minute rendering costs."
    },
    {
        "es": "Implementamos el estándar Model Context Protocol de Anthropic junto a Docker Desktop MCP Toolkit.",
        "en": "We implement Anthropic's Model Context Protocol standard alongside Docker Desktop MCP Toolkit."
    },
    {
        "es": "Nuestros agentes autónomos consultan bases de datos PostgreSQL y repositorios GitHub de forma aislada.",
        "en": "Our agents query PostgreSQL databases and GitHub repositories within isolated containers."
    },
    {
        "es": "Garantizamos la máxima seguridad corporativa en entornos totalmente herméticos.",
        "en": "Ensuring maximum corporate security within completely sealed operational environments."
    },
    {
        "es": "El futuro de las empresas de alto rendimiento es desplegar su propio ecosistema de Inteligencia Artificial.",
        "en": "The future of high-performing enterprises is deploying their proprietary AI ecosystem."
    },
    {
        "es": "Toda la arquitectura técnica de este sistema está blindada bajo el estándar v2.0-stable.",
        "en": "Our complete architecture is locked under the v2.0-stable enterprise standard."
    },
    {
        "es": "Se encuentra respaldada en GitHub y en Google Drive 5TB lista para despliegue inmediato.",
        "en": "Backed up to GitHub and 5TB Google Drive, ready for turnkey enterprise deployment."
    }
]

import edge_tts

async def build_master_audio_and_subtitles(lang="es"):
    print(f"\n🎙️ Sincronizando Pista de Voz y Subtítulos Teleprompter Acotados ({lang.upper()})...")
    audio_files = []
    ass_events = []
    current_sec = 0.8
    voice_id = "es-MX-JorgeNeural" if lang == "es" else "en-US-GuyNeural"
    
    for idx, item in enumerate(MASTERCLASS_EXTENDED_SCRIPT):
        text = item["es"] if lang == "es" else item["en"]
        phrase_file = OUT_DIR / f"full_phrase_{lang}_{idx+1}.mp3"
        
        if not phrase_file.exists() or phrase_file.stat().st_size < 1000:
            comm = edge_tts.Communicate(text, voice_id, rate="-2%", pitch="+0Hz")
            await comm.save(str(phrase_file))
            
        audio_files.append(phrase_file)
        
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprintwrappers=1:nokey=1", str(phrase_file)
        ], capture_output=True, text=True)
        try:
            dur = float(probe.stdout.strip())
        except Exception:
            dur = 4.0
            
        end_sec = current_sec + dur
        m_start = f"{int(current_sec//3600)}:{int((current_sec%3600)//60):02d}:{current_sec%60:05.2f}"
        m_end = f"{int(end_sec//3600)}:{int((end_sec%3600)//60):02d}:{end_sec%60:05.2f}"
        
        words = text.split()
        word_dur = int((dur * 1000) / max(len(words), 1) / 10)
        
        formatted_words = []
        for w_i, word in enumerate(words):
            if w_i > 0 and w_i % 6 == 0:
                formatted_words.append(f"\\N{{\\k{word_dur}}}{word}")
            else:
                formatted_words.append(f"{{\\k{word_dur}}}{word}")
                
        k_text = " ".join(formatted_words)
        ass_events.append(f"Dialogue: 0,{m_start},{m_end},RightTeleprompterBounded,,0,0,0,,{{\\pos(1300,380)}}{k_text}")
        current_sec = end_sec + 0.45

    list_file = OUT_DIR / f"full_concat_{lang}.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for a_file in audio_files:
            f.write(f"file '{str(a_file).replace('\\', '/')}'\n")
            
    master_audio = OUT_DIR / f"master_voice_full_{lang}.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:a", "libmp3lame", "-b:a", "256k",
        str(master_audio)
    ], capture_output=True, text=True)
    
    ass_file = OUT_DIR / f"master_subtitles_bounded_{lang}.ass"
    ass_header = f"""[Script Info]
Title: Bounded Right Teleprompter Subtitles ({lang})
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: RightTeleprompterBounded,Montserrat,44,&H00FFFFFF,&H0000D7FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,3,2,5,820,140,280,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(ass_events))
        
    print(f"✅ Audio Maestro {lang.upper()} Generado: {master_audio} ({current_sec:.1f}s)")
    print(f"📝 Subtítulos Acotados {lang.upper()} Generados: {ass_file}")
    
    return master_audio, ass_file, current_sec

async def render_cinematic_master_videos():
    avatar_img = PUBLIC_DIR / "avatar_transparent.png"
    if not avatar_img.exists():
        avatar_img = PUBLIC_DIR / "avatars" / "dorado.png"

    for lang in ["es", "en"]:
        master_audio, ass_file, total_duration = await build_master_audio_and_subtitles(lang)
        
        target_name = "youtube_30min_masterclass_full_1080p.mp4" if lang == "es" else "youtube_30min_masterclass_en_1080p.mp4"
        out_mp4 = OUT_DIR / target_name
        root_mp4 = PUBLIC_DIR / target_name
        
        ass_clean = str(ass_file).replace("\\", "/").replace(":", "\\:")
        
        filter_graph = (
            f"[0:v]zoompan=z='min(zoom+0.0005,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30[bg_zoom];"
            f"[bg_zoom]noise=alls=15:allf=t+u,format=gray,gblur=sigma=1.2[stars];"
            f"[stars]colorchannelmixer=rr=0.8:gg=0.8:bb=1.0[blue_stars];"
            f"[bg_zoom][blue_stars]blend=all_mode='screen':all_opacity=0.25[bg_stars];"
            f"[1:v]scale=720:980:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar_left];"
            f"[bg_stars][avatar_left]overlay=60:60[base];"
            f"[base]subtitles='{ass_clean}'[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(MOON_BG_PNG),
            "-loop", "1", "-i", str(avatar_img),
            "-i", str(master_audio),
            "-filter_complex", filter_graph,
            "-map", "[outv]",
            "-map", "2:a",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-shortest",
            "-c:a", "aac", "-b:a", "256k",
            str(out_mp4)
        ]
        
        print(f"⚙️ Compilando Video Maestro Cinemático 4 Capas ({lang.upper()}) — Duración: {total_duration:.1f}s...")
        res = subprocess.run(cmd, capture_output=True, text=True)

        if res.returncode == 0:
            shutil.copy(out_mp4, root_mp4)
            size_mb = out_mp4.stat().st_size / (1024 * 1024)
            print(f" ✅ MAESTRO CINEMÁTICO {lang.upper()} GENERADO: {out_mp4} ({size_mb:.2f} MB)")
            print(f" ✅ COPIA EN RAÍZ PÚBLICA: {root_mp4}")
        else:
            print(f"❌ Error compilando {lang.upper()}:\n{res.stderr[-600:]}")

asyncio.run(render_cinematic_master_videos())
print("\n🎬 ¡PROCESO DE RENDERIZADO MAESTRO COMPLETADO EXITOSAMENTE!")
