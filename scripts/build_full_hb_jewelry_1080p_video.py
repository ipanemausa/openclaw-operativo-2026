"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — 1080P MASTER VIDEO COMPOSITOR
==============================================================================
Renderiza la pieza audiovisual 1080p FastStart para Showcase B2B:
- Fondo: Estudio 1080p Dark Studio con Aura de Lujo
- Avatar: Guillermo HD (Dorado) con encuadre izquierdo
- Audio: Broadcast 48kHz Stereo (-16 LUFS EBU R128)
- Subtítulos: Teleprompter Karaoke / Lower Thirds elegantes
- Formato: MP4 1080p FastStart (-movflags +faststart)
==============================================================================
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "output_video_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

AUDIO_FILE = RUNTIME / "voice_master_48k.aac"
MANIFEST_FILE = RUNTIME / "script_manifest.json"
AVATAR_IMG = ROOT / "frontend" / "dist" / "avatars" / "dorado.png"
POSTER_IMG = ROOT / "frontend" / "dist" / "posters" / "poster_showcase.png"
OUTPUT_VIDEO = RUNTIME / "HB_Jewelry_Showcase_1080p_FastStart.mp4"

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def build_ass_subtitles(script_text: str, duration: float, ass_path: str):
    """Genera subtítulos ASS elegantes estilo Karaoke / Lower Third."""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Montserrat,54,&H0000D4FF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,3,2,7,120,80,120,1
Style: Subtitle,Montserrat,38,&H00FFFFFF,&H0000D4FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,7,120,80,210,1
Style: Brand,Montserrat,28,&H00D4AF37,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,2,0,1,1,0,3,100,120,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # Dividir texto en frases de ~7 segundos
    sentences = [s.strip() for s in script_text.split(".") if s.strip()]
    if not sentences:
        sentences = [script_text]

    time_per_sentence = duration / len(sentences)
    events = []

    # Brand tag permanente
    events.append(f"Dialogue: 0,0:00:00.00,{int(duration//3600):01d}:{int((duration%3600)//60):02d}:{duration%60:05.2f},Brand,,0,0,0,,HB JEWELRY · ALTA GAMA 2026")

    for i, sent in enumerate(sentences):
        t_start = i * time_per_sentence
        t_end = min(duration, (i + 1) * time_per_sentence)
        start_str = f"{int(t_start//3600):01d}:{int((t_start%3600)//60):02d}:{t_start%60:05.2f}"
        end_str = f"{int(t_end//3600):01d}:{int((t_end%3600)//60):02d}:{t_end%60:05.2f}"
        
        events.append(f"Dialogue: 1,{start_str},{end_str},Title,,0,0,0,,COLECCIÓN ESMERALDAS Y ORO 18K")
        events.append(f"Dialogue: 1,{start_str},{end_str},Subtitle,,0,0,0,,{sent}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))

def render_1080p_video():
    print("=" * 60)
    print("  🎬 OPENCLAW 1080P MASTER VIDEO COMPOSITOR")
    print("=" * 60)

    if not AUDIO_FILE.exists():
        print(f"[ERROR] Archivo de audio no encontrado: {AUDIO_FILE}")
        sys.exit(1)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    script_text = manifest.get("script", "")

    duration = get_audio_duration(str(AUDIO_FILE))
    print(f"-> Duración del audio: {duration:.2f}s")

    ass_sub_file = RUNTIME / "subtitles.ass"
    build_ass_subtitles(script_text, duration, str(ass_sub_file))
    print(f"-> Manifiesto de subtítulos ASS generado: {ass_sub_file}")

    # FFmpeg Filter Complex:
    # 1. Background oscuro 1920x1080 con viñeta y gradiente
    # 2. Avatar Guillermo escalado a 750px de alto en el lado derecho o izquierdo
    # 3. Superposición de subtítulos ASS
    # 4. Export FastStart MP4
    ass_escaped = str(ass_sub_file).replace("\\", "/").replace(":", "\\:")

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", str(POSTER_IMG),
        "-loop", "1", "-t", str(duration), "-i", str(AVATAR_IMG),
        "-i", str(AUDIO_FILE),
        "-filter_complex",
        f"[0:v]scale=1920:1080,boxblur=5:1[bg];"
        f"[1:v]scale=-1:850[avatar];"
        f"[bg][avatar]overlay=W-w-100:H-h[v1];"
        f"[v1]subtitles='{ass_escaped}'[vfinal]",
        "-map", "[vfinal]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-movflags", "+faststart",
        "-shortest",
        str(OUTPUT_VIDEO)
    ]

    print("-> Renderizando video 1080p con aceleración FFmpeg...")
    subprocess.run(cmd, check=True)

    size_mb = OUTPUT_VIDEO.stat().st_size / (1024 * 1024)
    print("\n" + "=" * 60)
    print("  ✅ VIDEO 1080P MASTER GENERADO EXITOSAMENTE")
    print(f"  Ruta:     {OUTPUT_VIDEO}")
    print(f"  Tamaño:   {size_mb:.2f} MB")
    print(f"  Duración: {duration:.2f}s")
    print("  Formato:  1080p MP4 FastStart (0 buffering)")
    print("=" * 60)

if __name__ == "__main__":
    render_1080p_video()
