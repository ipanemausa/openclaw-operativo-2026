#!/usr/bin/env python3
r"""
================================================================
 SadTalker Bridge — OpenClaw 2026.7.1
 Pipeline: audio + foto → lipsync animado → Firebase public
 $0 costo | 100% local | Sin límites de API
================================================================
 Rutas ajustadas al sistema real:
   SadTalker: C:/Users/ipane/openclaw-operativo-2026/agents/video_agent/SadTalker
   Output:    C:/openclaw/output/lipsync
   Firebase:  C:/openclaw/hb-jewelry/public/videos
================================================================
"""
import subprocess
import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ─── Rutas del sistema real ───────────────────────────────────────────────────
SADTALKER_DIR  = r"C:\Users\ipane\openclaw-operativo-2026\agents\video_agent\SadTalker"
CHECKPOINTS    = r"C:\Users\ipane\openclaw-operativo-2026\agents\video_agent\SadTalker\checkpoints"
GFPGAN_WEIGHTS = r"C:\Users\ipane\openclaw-operativo-2026\agents\video_agent\SadTalker\gfpgan\weights"
OUTPUT_LIPSYNC = r"C:\openclaw\output\lipsync"
OUTPUT_AUDIO   = r"C:\openclaw\output\audio"
FIREBASE_PUBLIC= r"C:\openclaw\hb-jewelry\public\videos"
SHOWCASE_VIDEO = r"C:\openclaw\hb-jewelry\public\showcase_human_loop.mp4"

# Foto portrait de Guillermo (extraída del video real)
DEFAULT_PORTRAIT = r"C:\openclaw\output\guillermo_portrait.jpg"

# ─── Verificación de estado ───────────────────────────────────────────────────
def check_ready() -> dict:
    """Verifica que todos los componentes estén listos."""
    status = {}
    status["sadtalker_repo"]  = Path(SADTALKER_DIR).exists()
    status["inference_py"]    = Path(SADTALKER_DIR, "inference.py").exists()
    status["checkpoints"]     = list(Path(CHECKPOINTS).glob("*.*")) if Path(CHECKPOINTS).exists() else []
    status["gfpgan"]          = list(Path(GFPGAN_WEIGHTS).glob("*.pth")) if Path(GFPGAN_WEIGHTS).exists() else []
    status["portrait"]        = Path(DEFAULT_PORTRAIT).exists()
    status["edge_tts"]        = shutil.which("edge-tts") is not None
    status["ready"]           = (
        status["sadtalker_repo"] and
        status["inference_py"] and
        len(status["checkpoints"]) >= 1 and
        status["edge_tts"]
    )
    return status

# ─── Extraer portrait del video real ─────────────────────────────────────────
def extract_portrait(output_path: str = DEFAULT_PORTRAIT) -> bool:
    """Extrae un frame limpio del video showcase para usarlo como portrait."""
    if Path(output_path).exists():
        print(f"[OK] Portrait ya existe: {output_path}")
        return True

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-ss", "2",                    # frame en segundo 2 (estable)
        "-i", SHOWCASE_VIDEO,
        "-vframes", "1",
        "-q:v", "1",                   # máxima calidad JPEG
        "-vf", "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[OK] Portrait extraído: {output_path}")
        return True
    else:
        print(f"[ERROR] ffmpeg portrait: {result.stderr[-300:]}")
        return False

# ─── Generar audio con edge-tts ──────────────────────────────────────────────
def generate_audio(text: str, output_path: str,
                   voice: str = "es-MX-JorgeNeural") -> bool:
    """Genera audio WAV con edge-tts (EBU R128 ready)."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # edge-tts genera MP3, convertimos a WAV 48kHz con ffmpeg
    mp3_path = output_path.replace(".wav", "_raw.mp3")
    cmd_tts = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", mp3_path,
    ]
    r = subprocess.run(cmd_tts, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print(f"[ERROR] edge-tts: {r.stderr}")
        return False

    # Convertir a WAV 48kHz mono (requerido por SadTalker)
    cmd_conv = [
        "ffmpeg", "-y",
        "-i", mp3_path,
        "-ar", "48000",
        "-ac", "1",
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",  # EBU R128
        output_path
    ]
    r2 = subprocess.run(cmd_conv, capture_output=True, text=True)
    if r2.returncode == 0:
        Path(mp3_path).unlink(missing_ok=True)
        print(f"[OK] Audio generado (48kHz WAV EBU R128): {output_path}")
        return True
    else:
        print(f"[ERROR] ffmpeg conv: {r2.stderr[-300:]}")
        return False

# ─── SadTalker lipsync ────────────────────────────────────────────────────────
def run_sadtalker(audio_path: str, portrait_path: str, output_name: str,
                  size: int = 512, use_enhancer: bool = True) -> str | None:
    """
    Ejecuta SadTalker para animar el portrait sincronizado con el audio.

    Args:
        audio_path:    WAV 48kHz
        portrait_path: JPG/PNG 512x512 del presentador
        output_name:   Nombre sin extensión del video final
        size:          512 (Alta Definición HD, GPU/CPU)
        use_enhancer:  True = aplica GFPGAN v1.4 para restauración hiperrealista de dentadura y labios

    Returns:
        Ruta al .mp4 generado o None si falló
    """
    out_dir = Path(OUTPUT_LIPSYNC)
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python", "inference.py",
        "--driven_audio",  audio_path,
        "--source_image",  portrait_path,
        "--result_dir",    str(out_dir),
        "--size",          str(size),
        "--expression_scale", "1.3",   # Expresividad natural de mandíbula y dientes
        "--preprocess",    "crop",
        "--still",                     # Evita rigidez y desalineación de cabeza
    ]
    if use_enhancer:
        cmd.extend(["--enhancer", "gfpgan"])

    print(f"\n[SadTalker] Iniciando animación facial...")
    print(f"  Portrait: {portrait_path}")
    print(f"  Audio:    {audio_path}")
    print(f"  Calidad:  {size}px | GFPGAN: {use_enhancer}")

    try:
        result = subprocess.run(
            cmd,
            cwd=SADTALKER_DIR,
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode == 0:
            videos = sorted(out_dir.rglob("*.mp4"), key=lambda x: x.stat().st_mtime)
            if videos:
                final = out_dir / f"{output_name}.mp4"
                shutil.move(str(videos[-1]), str(final))
                print(f"[OK] Video lipsync: {final}")
                return str(final)
        else:
            print(f"[ERROR] SadTalker:\n{result.stderr[-800:]}")
    except subprocess.TimeoutExpired:
        print("[WARN] SadTalker >10min → continúa en background")
    except Exception as e:
        print(f"[ERROR] {e}")
    return None

# ─── Compositing: burbuja circular sobre fondo educativo ────────────────────
def composite_bubble_video(lipsync_mp4: str, bg_video: str,
                            output_path: str) -> bool:
    """
    Compone el video final: fondo con contenido educativo + burbuja circular
    con la cara animada (formato Juan Pablo Navarro / Mirror).

        Layout:
        ┌──────────────────────────────────────┐
        │    FONDO EDUCATIVO (texto, diagrama) │
        │                                      │
        │                     ┌──────────────┐ │
        │                     │ CARA LIPSYNC │ │
        │                     │  (circular)  │ │
        │                     └──────────────┘ │
        └──────────────────────────────────────┘
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # FFmpeg: recorte circular + overlay bottom-right
    cmd = [
        "ffmpeg", "-y",
        "-i", bg_video,           # fondo educativo (input 0)
        "-i", lipsync_mp4,        # cara lipsync (input 1)
        "-filter_complex",
        # Recortar cara a círculo 300x300, bottom-right con padding 40px
        "[1:v]scale=300:300,"
        "format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(lte(hypot(X-150,Y-150),148),255,0)',"
        "pad=300:300:0:0:color=0x00000000[face];"
        # Border glow dorado
        "[face]drawbox=x=0:y=0:w=300:h=300:"
        "color=D4AF6A@0.8:t=3[face_border];"
        # Overlay sobre fondo 1080p, bottom-right con 40px margen
        "[0:v][face_border]overlay="
        "x=W-w-40:y=H-h-40:shortest=1[out]",
        "-map", "[out]",
        "-map", "1:a",             # audio del lipsync (tu voz)
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        output_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"[OK] Video compuesto: {output_path}")
        return True
    else:
        print(f"[ERROR] composite: {r.stderr[-400:]}")
        return False

# ─── Pipeline completo ────────────────────────────────────────────────────────
def run_full_pipeline(script: str, video_name: str = None,
                      quality: str = "fast",
                      bg_video: str = None) -> dict:
    """
    Pipeline completo:
    1. Extraer portrait de Guillermo del showcase
    2. Generar audio edge-tts EBU R128
    3. SadTalker → cara animada sincronizada
    4. FFmpeg → burbuja circular + fondo educativo
    5. Copiar a Firebase public/videos

    Args:
        script:     Texto del guión
        video_name: Nombre del archivo de salida
        quality:    'fast' (256px CPU) | 'hd' (512px GPU)
        bg_video:   Video de fondo educativo (opcional)
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_name = video_name or f"lipsync_{ts}"
    size = 512 if quality == "hd" else 256

    print(f"\n{'='*55}")
    print(f"  PIPELINE SADTALKER — OPENCLAW 2026.7.1")
    print(f"{'='*55}")
    print(f"  Video:   {video_name}")
    print(f"  Calidad: {quality} ({size}px)")

    # 0. Verificar estado
    s = check_ready()
    if not s["ready"]:
        msg = f"Sistema no listo: {s}"
        print(f"[ERROR] {msg}")
        return {"status": "error", "message": msg}

    # 1. Portrait
    if not extract_portrait():
        return {"status": "error", "message": "No se pudo extraer portrait"}

    # 2. Audio
    audio_path = str(Path(OUTPUT_AUDIO) / f"{video_name}.wav")
    if not generate_audio(script, audio_path):
        return {"status": "error", "message": "Falló edge-tts"}

    # 3. SadTalker lipsync
    lipsync_path = run_sadtalker(audio_path, DEFAULT_PORTRAIT, video_name, size)
    if not lipsync_path:
        return {"status": "error", "message": "Falló SadTalker"}

    result = {
        "status": "ok",
        "video_name": video_name,
        "lipsync_path": lipsync_path,
        "audio_path": audio_path,
    }

    # 4. Compositing con fondo (si se provee)
    if bg_video and Path(bg_video).exists():
        composite_path = str(Path(OUTPUT_LIPSYNC) / f"{video_name}_final.mp4")
        if composite_bubble_video(lipsync_path, bg_video, composite_path):
            result["composite_path"] = composite_path
            lipsync_path = composite_path

    # 5. Copiar a Firebase
    firebase_dir = Path(FIREBASE_PUBLIC)
    firebase_dir.mkdir(parents=True, exist_ok=True)
    dest = firebase_dir / f"{video_name}.mp4"
    shutil.copy2(lipsync_path, str(dest))
    result["firebase_url"] = f"/videos/{video_name}.mp4"

    print(f"\n[OK] PIPELINE COMPLETADO")
    print(f"  Video final: {dest}")
    print(f"  URL Firebase: {result['firebase_url']}")
    print(f"{'='*55}\n")
    return result

# ─── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Modo status
    if "--status" in sys.argv:
        s = check_ready()
        print(json.dumps(s, indent=2, default=str, ensure_ascii=False))
        sys.exit(0 if s["ready"] else 1)

    # Modo test rápido
    test_script = (
        "Bienvenidos. Hoy explicamos vectorización: "
        "el espacio de 768 dimensiones donde vive el significado "
        "de cada palabra que procesa la inteligencia artificial."
    )

    result = run_full_pipeline(
        script=test_script,
        video_name="lipsync_test_vectorizacion",
        quality="fast"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
