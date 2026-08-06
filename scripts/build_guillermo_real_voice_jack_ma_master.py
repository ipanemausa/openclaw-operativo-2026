import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================================")
print(" 🎙️ MASTER COMPOSITOR CON VOZ REAL DE GUILLERMO Y AVATAR COMPLETO")
print("====================================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
OUT_DIR = PUBLIC_DIR / "videos" / "jack_ma_style"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MP4 = OUT_DIR / "jack_ma_b2b_full_master.mp4"
ASS_SUBTITLE_FILE = OUT_DIR / "karaoke_subtitles_real_voice.ass"

# 1. Localizar la Voz Real de Guillermo (48kHz WAV o MP3)
real_voice_wav = PUBLIC_DIR / "videos" / "real_voice_master" / "guillermo_voice_fm_48k.wav"
if not real_voice_wav.exists():
    real_voice_wav = PUBLIC_DIR / "real_guillermo_voice.mp3"

print(f"🔊 Usando archivo de Voz Real de Guillermo: {real_voice_wav}")

# 2. Localizar el Video del Avatar de Guillermo con Movimiento de Boca y Expresión
avatar_vid = PUBLIC_DIR / "videos" / "guillermo_940f_master.mp4"
if not avatar_vid.exists():
    avatar_vid = PUBLIC_DIR / "tiktok_showcase.mp4"

print(f"👤 Usando Video de Avatar Guillermo HD: {avatar_vid}")

# 3. Crear Subtítulos Karaoke ASS alineados a la Voz Real de Guillermo en el lado derecho
ass_content = """[Script Info]
Title: Jack Ma Style Real Voice Karaoke
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaraokeStyle,Montserrat,46,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,3,2,6,650,100,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:06.00,KaraokeStyle,,0,0,0,,{\\k40}Bienvenidos {\\k30}a {\\k40}nuestra {\\k50}agencia {\\k40}de {\\k50}inteligencia {\\k50}artificial {\\k50}y {\\k60}asesoría {\\k60}empresarial.
Dialogue: 0,0:00:06.20,0:00:12.00,KaraokeStyle,,0,0,0,,{\\k50}Automatizamos {\\k40}los {\\k50}procesos {\\k40}de {\\k30}tu {\\k50}empresa, {\\k40}optimizamos {\\k50}ventas {\\k40}por {\\k60}WhatsApp.
Dialogue: 0,0:00:12.30,0:00:18.00,KaraokeStyle,,0,0,0,,{\\k50}Y {\\k50}reducimos {\\k40}tus {\\k50}costos {\\k50}operativos {\\k40}al {\\k60}cien {\\k50}por {\\k60}ciento.
"""

with open(ASS_SUBTITLE_FILE, "w", encoding="utf-8") as f:
    f.write(ass_content)

print(f"📝 Archivo de Subtítulos Karaoke ASS generado: {ASS_SUBTITLE_FILE}")

# 4. Compilar con FFmpeg:
# Canvas: Fondo Espacial Cósmico HD 1080p (cosmic_space_bg.png)
# Capa Avatar: Avatar Guillermo recortado y posicionado en el lado izquierdo (x=60, y=100)
# Capa Subtítulos: Karaoke ASS dorado quemado en el lado derecho
# Audio: Pista de VOZ REAL de Guillermo (48kHz)

cosmic_bg = PUBLIC_DIR / "cosmic_space_bg.png"
ass_path_clean = str(ASS_SUBTITLE_FILE).replace("\\", "/").replace(":", "\\:")

cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", str(cosmic_bg), # Fondo Cósmico 1080p
    "-i", str(avatar_vid), # Video Avatar Guillermo
    "-i", str(real_voice_wav), # Voz Real de Guillermo
    "-filter_complex",
    f"[1:v]scale=720:960:flags=lanczos,unsharp=5:5:1.5:5:5:1.5,eq=contrast=1.12:brightness=0.02:saturation=1.18[avatar_left];"
    f"[0:v][avatar_left]overlay=60:120[base];"
    f"[base]subtitles='{ass_path_clean}'[outv]",
    "-map", "[outv]",
    "-map", "2:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-shortest",
    "-c:a", "aac", "-b:a", "256k",
    str(FINAL_MP4)
]

print("⚙️ Ejecutando renderizado FFmpeg con VOZ REAL DE GUILLERMO y AVATAR IZQUIERDA...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0:
    size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
    print(f"=========================================================")
    print(f" ✅ VIDEO CON VOZ REAL Y AVATAR COMPLETO CREADO: {FINAL_MP4} ({size_mb:.2f} MB)")
    print(f"=========================================================")
else:
    print(f"❌ Error en FFmpeg render:\n{res.stderr[-600:]}")
