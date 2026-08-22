"""
render_mod6_es.py — Re-render aislado del Módulo 6 ES con path escaping correcto para FFmpeg/Windows
"""
import subprocess
import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR    = Path(r"C:\openclaw\hb-jewelry\public\videos\youtube_30min_masterclass")
PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
SPACE_BG   = PUBLIC_DIR / "cosmic_space_smooth.png"
AVATAR     = PUBLIC_DIR / "avatar_transparent.png"

SCRIPT_ES = (
    "Concluimos con la hoja de ruta de implementacion para escalar tu negocio de "
    "joyeria o servicios profesionales a un estandar internacional sin friccion operativa. "
    "Gracias por acompanarnos en este analisis de OpenClaw 2026."
)

async def main():
    wav = OUT_DIR / "mod_6_es.wav"

    # Medir duracion
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprintwrappers=1:nokey=1", str(wav)],
        capture_output=True, text=True
    )
    dur = float(p.stdout.strip()) if p.stdout.strip() else 18.0
    frames = int(dur * 30) + 15
    print(f"Duracion: {dur:.2f}s | Frames: {frames}")

    # Generar ASS
    words = SCRIPT_ES.split()
    wd = int((dur * 1000) / max(len(words), 1) / 10)
    k_text = "".join(["{\\k" + str(wd) + "}" + w + " " for w in words])

    ass = OUT_DIR / "mod_6_es.ass"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CT,Arial Black,58,&H00FFFFFF,&H0000C5FF,&H00000000,&H80000000,-1,0,0,0,105,100,2,0,1,4,3,5,300,300,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:{int(dur//60):02d}:{dur%60:05.2f},CT,,0,0,0,,{{\\pos(960,880)}}{k_text.strip()}
"""
    ass.write_text(ass_content, encoding="utf-8")
    print(f"ASS escrito: {ass}")

    # CRITICAL: path correcto para FFmpeg subtitles en Windows
    # Paso 1: todos los \ -> /
    # Paso 2: el : de la unidad -> \:
    ass_ffmpeg = str(ass).replace("\\", "/").replace(":", "\\:")
    print(f"ASS path FFmpeg: {ass_ffmpeg}")

    out = OUT_DIR / "block_6_es.mp4"

    filter_graph = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
        f"zoompan=z='min(zoom+0.0006\\,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={frames}:s=1920x1080:fps=30[bg];"
        f"[1:v]scale=680:960:flags=lanczos,unsharp=5:5:1.2:5:5:1.2[avatar];"
        f"[bg][avatar]overlay=10:120[base];"
        f"[base]subtitles='{ass_ffmpeg}'[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{dur:.2f}", "-i", str(SPACE_BG),
        "-loop", "1", "-t", f"{dur:.2f}", "-i", str(AVATAR),
        "-i", str(wav),
        "-filter_complex", filter_graph,
        "-map", "[outv]", "-map", "2:a",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        str(out)
    ]

    print("Lanzando FFmpeg modulo 6 ES (sin timeout — zoompan tarda ~50min en CPU)...")
    print(f"filter_complex:\n{filter_graph}\n")

    # SIN timeout — zoompan 1920x1080 tarda ~50 minutos en CPU (normal)
    import time
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    elapsed = time.time() - t0

    if proc.returncode == 0:
        size = out.stat().st_size / 1024 / 1024
        print(f"OK: block_6_es.mp4 — {size:.1f} MB en {elapsed/60:.1f} min")
    else:
        print(f"ERROR FFmpeg ({elapsed:.0f}s):")
        print(stderr.decode('utf-8', errors='replace')[-800:])

if __name__ == "__main__":
    asyncio.run(main())
