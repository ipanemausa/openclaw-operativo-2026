import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🏛️ MASTER COMPOSITOR B2B — AVATAR VIRTUAL 3D + GUIÓN EJECUTIVO")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "jack_ma_style"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MP4 = OUT_DIR / "jack_ma_b2b_full_master.mp4"
ASS_SUBTITLE_FILE = OUT_DIR / "karaoke_subtitles_real_voice.ass"

# 1. Voz Real de Guillermo 48kHz
real_voice_wav = PUBLIC_DIR / "videos" / "real_voice_master" / "guillermo_voice_fm_48k.wav"
if not real_voice_wav.exists():
    real_voice_wav = PUBLIC_DIR / "real_guillermo_voice.mp3"

print(f"🔊 Usando archivo de Voz Real de Guillermo: {real_voice_wav}")

# 2. AVATAR VIRTUAL 3D HD — MIRANDO DE FRENTE AL PÚBLICO (Forward-Facing Frontal Pose)
avatar_img = PUBLIC_DIR / "avatars" / "dorado.png"
if not avatar_img.exists():
    avatar_img = PUBLIC_DIR / "avatars" / "desk_mic.png"
if not avatar_img.exists():
    avatar_img = PUBLIC_DIR / "avatar_pro.png"

print(f"👤 Usando Avatar Virtual 3D HD de Frente al Público: {avatar_img}")

# 3. GUIÓN PROFESIONAL NIVEL CONSULTORÍA EMPRESARIAL B2B (Sin exageraciones)
# Subtítulos Karaoke ASS con resaltado en Dorado Neón (&H0000D7FF&) y fuente de 84px
ass_content = """[Script Info]
Title: Jack Ma Style B2B Executive Script
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaraokeStyle,Montserrat,72,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,4,3,6,750,80,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:06.00,KaraokeStyle,,0,0,0,,{\\k40}Bienvenidos {\\k30}a {\\k40}nuestra {\\k50}plataforma {\\k40}de {\\k50}inteligencia {\\k50}artificial {\\k50}y {\\k60}consultoría {\\k60}empresarial {\\k50}B2B.
Dialogue: 0,0:00:06.20,0:00:12.50,KaraokeStyle,,0,0,0,,{\\k50}Transformamos {\\k40}y {\\k50}automatizamos {\\k40}los {\\k30}procesos {\\k50}operativos, {\\k40}optimizando {\\k50}ventas {\\k40}por {\\k60}WhatsApp {\\k50}a {\\k40}costo {\\k50}cero.
Dialogue: 0,0:00:12.80,0:00:18.50,KaraokeStyle,,0,0,0,,{\\k50}Y {\\k50}elevamos {\\k40}la {\\k50}productividad {\\k50}y {\\k40}rentabilidad {\\k50}con {\\k40}arquitectura {\\k60}de {\\k50}agentes {\\k60}autónomos.
"""

with open(ASS_SUBTITLE_FILE, "w", encoding="utf-8") as f:
    f.write(ass_content)

print(f"📝 Guión B2B Ejecutivo y Subtítulos Karaoke ASS generados: {ASS_SUBTITLE_FILE}")

# 4. Compilación FFmpeg:
# Fondo Espacial Cósmico HD 1080p (cosmic_space_bg.png)
# Avatar Virtual 3D HD escalado a la izquierda (x=80, y=100)
# Subtítulos Karaoke ASS ejecutivos a la derecha (72px)
# Voz Real de Guillermo 48kHz

cosmic_bg = PUBLIC_DIR / "cosmic_space_bg.png"
ass_path_clean = str(ASS_SUBTITLE_FILE).replace("\\", "/").replace(":", "\\:")

cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", str(cosmic_bg), # Fondo Cósmico 1080p
    "-loop", "1", "-i", str(avatar_img), # Avatar Virtual 3D HD
    "-i", str(real_voice_wav), # Voz Real de Guillermo
    "-filter_complex",
    f"[0:v]zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30[bg_zoom];"
    f"[1:v]scale=680:920:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar_left];"
    f"[bg_zoom][avatar_left]overlay=80:100[base];"
    f"[base]subtitles='{ass_path_clean}'[outv]",
    "-map", "[outv]",
    "-map", "2:a",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-shortest",
    "-c:a", "aac", "-b:a", "256k",
    str(FINAL_MP4)
]

print("⚙️ Ejecutando renderizado FFmpeg con AVATAR VIRTUAL 3D HD y GUIÓN EJECUTIVO B2B...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0:
    size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
    print(f"=========================================================")
    print(f" ✅ VIDEO B2B EJECUTIVO CREADO EXITOSAMENTE: {FINAL_MP4} ({size_mb:.2f} MB)")
    print(f"=========================================================")
else:
    print(f"❌ Error en FFmpeg render:\n{res.stderr[-600:]}")
