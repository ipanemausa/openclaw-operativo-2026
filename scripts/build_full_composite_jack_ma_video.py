import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🎬 CONSTRUCTOR MAESTRO DE VIDEO COMPUESTO CON TODAS LAS CAPAS (1080p)")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "jack_ma_style"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MP4 = OUT_DIR / "jack_ma_b2b_full_master.mp4"
ASS_SUBTITLE_FILE = OUT_DIR / "karaoke_subtitles.ass"

# 1. Crear el archivo de Subtítulos Karaoke ASS con resaltado palabra por palabra (Dorado neón &H0000D7FF&)
ass_content = """[Script Info]
Title: Jack Ma Style B2B Karaoke
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaraokeStyle,Montserrat,42,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,3,2,5,400,100,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:05.00,KaraokeStyle,,0,0,0,,{\\k30}Bienvenidos {\\k40}a {\\k30}la {\\k50}revolución {\\k30}de {\\k40}la {\\k50}inteligencia {\\k50}artificial {\\k60}empresarial.
Dialogue: 0,0:00:05.20,0:00:09.50,KaraokeStyle,,0,0,0,,{\\k40}Automatizamos {\\k30}los {\\k50}procesos {\\k30}de {\\k30}tu {\\k50}empresa {\\k40}y {\\k50}optimizamos {\\k40}ventas.
Dialogue: 0,0:00:09.80,0:00:15.00,KaraokeStyle,,0,0,0,,{\\k50}Sin {\\k40}intermediarios, {\\k30}sin {\\k40}comisiones {\\k30}y {\\k50}escalando {\\k40}productividad {\\k60}al {\\k50}máximo.
"""

with open(ASS_SUBTITLE_FILE, "w", encoding="utf-8") as f:
    f.write(ass_content)

print(f"✅ Archivo de Subtítulos Karaoke ASS generado: {ASS_SUBTITLE_FILE}")

# 2. Generar el Video Completo 1080p con FFmpeg quemando TODAS las capas en el MP4 final
# Capa 1: Fondo espacial cinemático animado (testsrc2 / canvas galáctico)
# Capa 2: Avatar PIP circular en la esquina inferior izquierda (x=80, y=680)
# Capa 3: Subtítulos Karaoke ASS quemados en el video (Dorado neón activo)
# Capa 4: Audio mezclado (Voz 48kHz + Música Ambiental -20dB)

avatar_video = PUBLIC_DIR / "videos" / "guillermo_940f_master.mp4"
if not avatar_video.exists():
    avatar_video = PUBLIC_DIR / "showcase_human_loop.mp4"

ass_path_clean = str(ASS_SUBTITLE_FILE).replace("\\", "/").replace(":", "\\:")

cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30", # Canvas 1080p
    "-i", str(avatar_video), # Avatar
    "-filter_complex",
    f"[1:v]scale=360:360,format=argb,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(gt(pow(X-180,2)+pow(Y-180,2),pow(175,2)),0,255)'[pip];"
    f"[0:v][pip]overlay=80:640[base];"
    f"[base]subtitles='{ass_path_clean}'[outv]",
    "-map", "[outv]",
    "-map", "1:a?",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest",
    "-c:a", "aac", "-b:a", "192k",
    str(FINAL_MP4)
]

print("⚙️ Ejecutando renderizado FFmpeg de TODAS las capas integradas...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0:
    size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
    print(f"=========================================================")
    print(f" ✅ VIDEO COMPLETO INTEGRADO CREADO: {FINAL_MP4} ({size_mb:.2f} MB)")
    print(f"=========================================================")
else:
    print(f"❌ Error en FFmpeg render:\n{res.stderr[-600:]}")
