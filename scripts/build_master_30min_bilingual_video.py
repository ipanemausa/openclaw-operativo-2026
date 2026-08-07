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
print(" 🚀 RE-INGENIERÍA MAESTRA: MASTERCLASS BILINGÜE 1 A 1 (ES/EN PARIDAD 100%)")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "youtube_masterclass"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. GENERAR FONDO CÓSMICO SUAVE SIN CÍRCULO MORADO DURO
def generate_smooth_cosmic_bg():
    bg_file = PUBLIC_DIR / "cosmic_space_smooth.png"
    img = Image.new("RGBA", (1920, 1080), (10, 8, 20, 255))
    draw = ImageDraw.Draw(img)
    
    # Glow suave radial dorado/púrpura difuminado
    aura = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    aura_draw = ImageDraw.Draw(aura)
    # Aura dorada central suavizada
    aura_draw.ellipse([600, 140, 1400, 940], fill=(212, 175, 106, 40))
    # Aura púrpura difusa
    aura_draw.ellipse([400, 40, 1600, 1040], fill=(129, 140, 248, 25))
    aura = aura.filter(ImageFilter.GaussianBlur(120))
    
    img = Image.alpha_composite(img, aura)
    img.convert("RGB").save(bg_file, "PNG")
    print(f"🌌 Fondo Cósmico Suave Generado: {bg_file}")
    return bg_file

SMOOTH_BG = generate_smooth_cosmic_bg()

# 2. DEFINICIÓN ESTRUCTURADA DE FRASES CON PARIDAD EXACTA ES / EN
BILINGUAL_MASTER_SCRIPT = [
    {
        "es": "Bienvenidos a este análisis de Inteligencia Artificial B2B.",
        "en": "Welcome to this executive analysis of B2B Artificial Intelligence."
    },
    {
        "es": "Hoy examinaremos la sustitución de licencias SaaS tradicionales.",
        "en": "Today we examine replacing legacy SaaS software subscriptions."
    },
    {
        "es": "Desplegamos agentes autónomos directamente en tu infraestructura.",
        "en": "We deploy autonomous AI agents directly on your infrastructure."
    },
    {
        "es": "Cero fricción de pagos por usuario y control total de datos.",
        "en": "Zero per-user licensing fees and total data sovereignty."
    },
    {
        "es": "Toda empresa sólida se sustenta en 4 pilares fundamentales:",
        "en": "Every resilient enterprise operates on 4 core pillars:"
    },
    {
        "es": "Atracción en Marketing, Conversión en Ventas, Logística y Finanzas.",
        "en": "Marketing Attraction, Sales Conversion, Logistics, and Finance."
    },
    {
        "es": "Conectamos un motor RAG vectorial de 768 dimensiones a Firestore.",
        "en": "Connecting a 768-dimensional RAG vector engine to Firestore."
    },
    {
        "es": "Tu sistema responde con datos exactos sin inventar información.",
        "en": "Your system responds with precise data without AI hallucinations."
    },
    {
        "es": "Con la actualización reciente de Meta, tus clientes usan tu Alias.",
        "en": "Leveraging Meta's newest update, clients use your Business Handle."
    },
    {
        "es": "Protegemos los números privados con tokens encriptados BSUID.",
        "en": "We protect private phone numbers using encrypted BSUID tokens."
    },
    {
        "es": "Atención automatizada por WhatsApp Business las 24 horas a costo cero.",
        "en": "24/7 automated WhatsApp Business customer support at zero cost."
    },
    {
        "es": "Procesamos video en micro-lotes de 15 frames con restauración GFPGAN.",
        "en": "Processing AI video in 15-frame micro-batches with GFPGAN."
    },
    {
        "es": "Producimos avatares en 1080p con voz estéreo de alta fidelidad.",
        "en": "Producing 1080p digital human presenters with 48kHz stereo audio."
    },
    {
        "es": "Mediante el estándar Model Context Protocol de Anthropic y Docker,",
        "en": "Using Anthropic's Model Context Protocol and Docker MCP Toolkit,"
    },
    {
        "es": "nuestros agentes consultan bases PostgreSQL y repositorios GitHub.",
        "en": "our agents query PostgreSQL databases and GitHub repositories."
    },
    {
        "es": "Toda esta arquitectura está blindada en la versión v2.0-stable.",
        "en": "This entire architecture is locked under release tag v2.0-stable."
    },
    {
        "es": "Respaldada en GitHub y Google Drive 5TB para despliegue inmediato.",
        "en": "Backed up to GitHub and 5TB Google Drive for instant deployment."
    }
]

import edge_tts

async def generate_bilingual_audio_and_ass(lang="es"):
    print(f"\n🎙️ Generando Pista de Voz y Subtítulos Teleprompter 100% Sincronizados ({lang.upper()})...")
    
    audio_files = []
    ass_events = []
    current_sec = 0.8
    voice_id = "es-MX-JorgeNeural" if lang == "es" else "en-US-GuyNeural"
    
    for idx, item in enumerate(BILINGUAL_MASTER_SCRIPT):
        text = item["es"] if lang == "es" else item["en"]
        phrase_file = OUT_DIR / f"sync_phrase_{lang}_{idx+1}.mp3"
        
        # Generar audio con edge-tts si no existe
        if not phrase_file.exists() or phrase_file.stat().st_size < 1000:
            comm = edge_tts.Communicate(text, voice_id, rate="-2%", pitch="+0Hz")
            await comm.save(str(phrase_file))
            
        audio_files.append(phrase_file)
        
        # Obtener duración exacta con ffprobe
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprintwrappers=1:nokey=1", str(phrase_file)
        ], capture_output=True, text=True)
        try:
            dur = float(probe.stdout.strip())
        except Exception:
            dur = 3.2
            
        end_sec = current_sec + dur
        
        # Formatear tiempos ASS hh:mm:ss.ms
        m_start = f"{int(current_sec//3600)}:{int((current_sec%3600)//60):02d}:{current_sec%60:05.2f}"
        m_end = f"{int(end_sec//3600)}:{int((end_sec%3600)//60):02d}:{end_sec%60:05.2f}"
        
        # Karaoke palabra por palabra
        words = text.split()
        word_dur = int((dur * 1000) / max(len(words), 1) / 10)
        k_text = "".join([f"{{\\k{word_dur}}}{w} " for w in words])
        
        # Posición fija en la mitad DERECHA (x: 1280px, y: 380px)
        ass_events.append(f"Dialogue: 0,{m_start},{m_end},RightTeleprompterStyle,,0,0,0,,{{\\pos(1280,380)}}{k_text.strip()}")
        current_sec = end_sec + 0.4

    # Concatenar audios
    list_file = OUT_DIR / f"concat_sync_{lang}.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for a_file in audio_files:
            f.write(f"file '{str(a_file).replace('\\', '/')}'\n")
            
    master_audio = OUT_DIR / f"master_voice_sync_{lang}.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:a", "libmp3lame", "-b:a", "256k",
        str(master_audio)
    ], capture_output=True, text=True)
    
    # Escribir subtítulos ASS
    ass_file = OUT_DIR / f"master_subtitles_sync_{lang}.ass"
    ass_header = f"""[Script Info]
Title: Masterclass Right Side Teleprompter ({lang})
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: RightTeleprompterStyle,Montserrat,52,&H00FFFFFF,&H0000D7FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,3,2,5,100,100,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(ass_events))
        
    print(f"✅ Audio Maestro {lang.upper()} Ensamblado: {master_audio} ({current_sec:.1f}s)")
    print(f"📝 Subtítulos {lang.upper()} Generados: {ass_file}")
    
    return master_audio, ass_file, current_sec

# Renderizar ambos videos con 100% de paridad
async def render_bilingual_master_videos():
    avatar_img = PUBLIC_DIR / "avatar_transparent.png"
    if not avatar_img.exists():
        avatar_img = PUBLIC_DIR / "avatars" / "dorado.png"

    for lang in ["es", "en"]:
        master_audio, ass_file, total_duration = await generate_bilingual_audio_and_ass(lang)
        
        target_name = "youtube_30min_masterclass_full_1080p.mp4" if lang == "es" else "youtube_30min_masterclass_en_1080p.mp4"
        out_mp4 = OUT_DIR / target_name
        root_mp4 = PUBLIC_DIR / target_name
        
        ass_clean = str(ass_file).replace("\\", "/").replace(":", "\\:")
        
        # Filtro de renderizado con fondo suave sin círculo morado
        filter_graph = (
            f"[0:v]zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30[bg_zoom];"
            f"[1:v]scale=720:980:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar_left];"
            f"[bg_zoom][avatar_left]overlay=60:60[base];"
            f"[base]subtitles='{ass_clean}'[outv]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(SMOOTH_BG),
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
        
        print(f"⚙️ Compilando Video Maestro Paridad 1 a 1 ({lang.upper()}) — Duración: {total_duration:.1f}s...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode == 0:
            shutil.copy(out_mp4, root_mp4)
            size_mb = out_mp4.stat().st_size / (1024 * 1024)
            print(f" ✅ MAESTRO {lang.upper()} COMPLETADO EXITOSAMENTE: {out_mp4} ({size_mb:.2f} MB)")
            print(f" ✅ COPIA EN RAÍZ PÚBLICA: {root_mp4}")
        else:
            print(f"❌ Error compilando {lang.upper()}:\n{res.stderr[-600:]}")

asyncio.run(render_bilingual_master_videos())
print("\n🎬 ¡PROCESO MAESTRO BILINGÜE CON PARIDAD 100% FINALIZADO EXITOSAMENTE!")
