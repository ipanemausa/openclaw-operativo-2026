import os
import sys
import asyncio
import subprocess
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🏛️ MASTER COMPOSITOR B2B CINEMA STUDIO 2.5 (LUNA + CÍRCULO MORADO + PARIDAD ES/EN)")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "jack_ma_style"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Fondo Estético: Luna Realista + Círculo Morado
MOON_BG_PNG = PUBLIC_DIR / "moon_cosmic_space.png"
if not MOON_BG_PNG.exists():
    MOON_BG_PNG = PUBLIC_DIR / "cosmic_space_smooth.png"

# 2. Avatar Virtual 3D HD
avatar_img = PUBLIC_DIR / "avatar_transparent.png"
if not avatar_img.exists():
    avatar_img = PUBLIC_DIR / "avatars" / "dorado.png"

# 3. Guión Ejecutivo B2B Sincronizado Bilingüe
B2B_SCRIPT = [
    {
        "es": "Bienvenidos a nuestra plataforma de inteligencia artificial y consultoría B2B.",
        "en": "Welcome to our enterprise artificial intelligence and B2B consulting platform."
    },
    {
        "es": "Transformamos y automatizamos los procesos operativos de tu empresa.",
        "en": "We transform and automate your enterprise operational workflows."
    },
    {
        "es": "Optimizamos ventas por WhatsApp Business a costo cero de mensajería.",
        "en": "Optimizing sales through WhatsApp Business with zero per-message cost."
    },
    {
        "es": "Elevamos la rentabilidad mediante arquitecturas de agentes autónomos.",
        "en": "Driving operational margin through autonomous agent architecture."
    },
    {
        "es": "Toda la infraestructura se despliega en tu propio servidor con control total.",
        "en": "Complete infrastructure deployed on your private servers with total sovereignty."
    }
]

import edge_tts

async def build_b2b_video(lang="es"):
    print(f"\n🎙️ Sincronizando Audio 48kHz y Teleprompter Derecho ({lang.upper()})...")
    audio_files = []
    ass_events = []
    current_sec = 0.8
    voice_id = "es-MX-JorgeNeural" if lang == "es" else "en-US-GuyNeural"
    
    for idx, item in enumerate(B2B_SCRIPT):
        text = item["es"] if lang == "es" else item["en"]
        phrase_file = OUT_DIR / f"jack_ma_phrase_{lang}_{idx+1}.mp3"
        
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
            dur = 3.5
            
        end_sec = current_sec + dur
        m_start = f"{int(current_sec//3600)}:{int((current_sec%3600)//60):02d}:{current_sec%60:05.2f}"
        m_end = f"{int(end_sec//3600)}:{int((end_sec%3600)//60):02d}:{end_sec%60:05.2f}"
        
        words = text.split()
        word_dur = int((dur * 1000) / max(len(words), 1) / 10)
        k_text = "".join([f"{{\\k{word_dur}}}{w} " for w in words])
        
        ass_events.append(f"Dialogue: 0,{m_start},{m_end},RightTeleprompterStyle,,0,0,0,,{{\\pos(1280,380)}}{k_text.strip()}")
        current_sec = end_sec + 0.4

    list_file = OUT_DIR / f"concat_jack_ma_{lang}.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for a_file in audio_files:
            f.write(f"file '{str(a_file).replace('\\', '/')}'\n")
            
    master_audio = OUT_DIR / f"jack_ma_voice_{lang}.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:a", "libmp3lame", "-b:a", "256k",
        str(master_audio)
    ], capture_output=True, text=True)
    
    ass_file = OUT_DIR / f"jack_ma_subtitles_{lang}.ass"
    ass_header = f"""[Script Info]
Title: Jack Ma Style Right Teleprompter ({lang})
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
        
    out_mp4 = OUT_DIR / f"jack_ma_b2b_{'full' if lang=='es' else 'en'}_master.mp4"
    root_mp4 = PUBLIC_DIR / f"jack_ma_b2b_{'full' if lang=='es' else 'en'}_master.mp4"
    
    ass_clean = str(ass_file).replace("\\", "/").replace(":", "\\:")
    
    filter_graph = (
        f"[0:v]zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30[bg_zoom];"
        f"[1:v]scale=720:980:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar_left];"
        f"[bg_zoom][avatar_left]overlay=60:60[base];"
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
    
    print(f"⚙️ Renderizando Video Jack Ma B2B Cinema Studio 2.5 ({lang.upper()})...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if res.returncode == 0:
        shutil.copy(out_mp4, root_mp4)
        size_mb = out_mp4.stat().st_size / (1024 * 1024)
        print(f" ✅ VIDEO JACK MA {lang.upper()} COMPLETADO EXITOSAMENTE: {out_mp4} ({size_mb:.2f} MB)")
        print(f" ✅ COPIA EN RAÍZ PÚBLICA: {root_mp4}")
    else:
        print(f"❌ Error compilando {lang.upper()}:\n{res.stderr[-600:]}")

async def main():
    for lang in ["es", "en"]:
        await build_b2b_video(lang)

asyncio.run(main())
print("\n🎬 ¡VIDEO MAESTRO JACK MA B2B RENDERIZADO CON PARIDAD BILINGÜE Y LUNA REALISTA!")
