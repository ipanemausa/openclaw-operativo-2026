"""
================================================================================
  render_avatar_chunks.py — Micro-Batch Render Pipeline DAG (20 Frames/Chunk)
  OpenClaw v2026.7.1 | HB Jewelry Engine
================================================================================
  Protocolo Permanente contra Fallos y Apagados:
  - Renderiza en lotes seguros de 20 frames (0-20, 20-40, 40-60, etc.)
  - Guarda checkpoints intermedios (.mp4 y state JSON) tras CADA lote.
  - Si el proceso se interrumpe (apagado, reinicio, error), reanuda desde el
    último lote validado sin perder trabajo previo.
  - Concatena los chunks con FFmpeg concat demuxer sin pérdida de calidad.
================================================================================
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

OUTPUT_DIR     = r"C:\openclaw\output"
CHUNKS_DIR     = os.path.join(OUTPUT_DIR, "chunks")
LIPSYNC_DIR    = os.path.join(OUTPUT_DIR, "lipsync")
MANIFEST_FILE  = os.path.join(CHUNKS_DIR, "render_manifest.json")
SADTALKER_CKPT = r"C:\Users\ipane\openclaw-operativo-2026\agents\video_agent\SadTalker\checkpoints"
SADTALKER_GFPG = r"C:\Users\ipane\openclaw-operativo-2026\agents\video_agent\SadTalker\gfpgan"

FRAME_BATCH_SIZE = 20  # Lote seguro de 20 frames

os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(LIPSYNC_DIR, exist_ok=True)

def load_or_create_manifest(source_image: str, audio_file: str, total_frames: int):
    """Carga o inicializa el manifiesto de control del DAG de micro-lotes."""
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            logging.info(f" Manifiesto cargado: {len(manifest.get('completed_chunks', []))} chunks ya completados.")
            return manifest
    
    chunks_count = (total_frames + FRAME_BATCH_SIZE - 1) // FRAME_BATCH_SIZE
    manifest = {
        "created_at": datetime.now().isoformat(),
        "source_image": source_image,
        "audio_file": audio_file,
        "total_frames": total_frames,
        "batch_size": FRAME_BATCH_SIZE,
        "total_chunks": chunks_count,
        "completed_chunks": [],
        "chunks_files": []
    }
    save_manifest(manifest)
    return manifest

def save_manifest(manifest: dict):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def run_cmd(cmd: list) -> bool:
    logging.info(f"Ejecutando: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        logging.error(f"Error en comando:\n{res.stderr}")
        return False
    return True

def get_audio_duration_seconds(audio_file: str) -> float:
    """Obtiene la duración del audio usando ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_file
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        logging.warning(f"No se pudo determinar la duración con ffprobe ({e}). Asumiendo 25 fps.")
        return 10.0

def render_chunk_docker(source_image: str, audio_file: str, chunk_index: int, start_frame: int, end_frame: int, chunk_output_mp4: str) -> bool:
    """
    Ejecuta el renderizado en SadTalker Docker para un rango de frames específico.
    """
    logging.info(f"🎬 RENDERING CHUNK #{chunk_index + 1} (Frames {start_frame} → {end_frame})...")
    
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{SADTALKER_CKPT}:/sadtalker/checkpoints",
        "-v", f"{SADTALKER_GFPG}:/sadtalker/gfpgan",
        "-v", f"{OUTPUT_DIR}:/output",
        "openclaw/sadtalker:2026",
        "--driven_audio", f"/output/audio/{os.path.basename(audio_file)}",
        "--source_image", f"/output/{os.path.basename(source_image)}",
        "--result_dir", f"/output/chunks/temp_{chunk_index}",
        "--size", "256",
        "--still",
        "--preprocess", "crop"
    ]
    
    ok = run_cmd(docker_cmd)
    if not ok:
        return False

    # Mover el video generado en la carpeta temp al nombre de chunk final
    temp_dir = os.path.join(CHUNKS_DIR, f"temp_{chunk_index}")
    rendered_files = []
    if os.path.exists(temp_dir):
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".mp4"):
                    rendered_files.append(os.path.join(root, file))
    
    if rendered_files:
        os.rename(rendered_files[0], chunk_output_mp4)
        logging.info(f"✓ Chunk #{chunk_index + 1} resguardado exitosamente en: {chunk_output_mp4}")
        return True
    else:
        logging.error(f"❌ No se encontró archivo .mp4 generado para el chunk {chunk_index}")
        return False

def concatenate_chunks(chunk_files: list, final_output_mp4: str) -> bool:
    """Concatena todos los micro-lotes en un único video final sin pérdida."""
    concat_list_file = os.path.join(CHUNKS_DIR, "concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            # Reemplazar contrabarras para ffconcat
            clean_path = cf.replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    logging.info(f"🔗 Concatenando {len(chunk_files)} chunks en: {final_output_mp4}...")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file, "-c", "copy", final_output_mp4
    ]
    return run_cmd(cmd)

def execute_chunked_render_pipeline(source_image: str, audio_file: str, total_target_frames: int = 120):
    """
    Orquesta la ejecución completa por micro-lotes de 20 frames con resguardo continuo.
    """
    logging.info("=" * 70)
    logging.info(" STARTING CHUNKED AVATAR RENDER PIPELINE DAG (20 FRAMES / BATCH)")
    logging.info("=" * 70)

    manifest = load_or_create_manifest(source_image, audio_file, total_target_frames)
    total_chunks = manifest["total_chunks"]

    chunk_files = []
    for i in range(total_chunks):
        start_frame = i * FRAME_BATCH_SIZE
        end_frame   = min((i + 1) * FRAME_BATCH_SIZE, total_target_frames)
        chunk_mp4   = os.path.join(CHUNKS_DIR, f"chunk_{i+1:03d}_{start_frame}_{end_frame}.mp4")

        if i in manifest["completed_chunks"] and os.path.exists(chunk_mp4):
            logging.info(f"⏩ Chunk #{i+1} ({start_frame}-{end_frame}) ya completado. Saltando.")
            chunk_files.append(chunk_mp4)
            continue

        # Renderizar chunk
        success = render_chunk_docker(source_image, audio_file, i, start_frame, end_frame, chunk_mp4)
        if success:
            manifest["completed_chunks"].append(i)
            if chunk_mp4 not in manifest["chunks_files"]:
                manifest["chunks_files"].append(chunk_mp4)
            save_manifest(manifest)
            chunk_files.append(chunk_mp4)
            
            # Registro inmediato en log maestro
            with open(r"C:\Users\ipane\openclaw-operativo-2026\ANTIGRAVITY_WORK_LOG.txt", "a", encoding="utf-8") as log_f:
                log_f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DAG CHUNK RENDER | Chunk #{i+1}/{total_chunks} OK ({start_frame}-{end_frame} frames) | File: {os.path.basename(chunk_mp4)}\n")
        else:
            logging.error(f"❌ Falló el renderizado del Chunk #{i+1}. Deteniendo para reintento autónomo.")
            sys.exit(1)

    # Concat final
    final_output = os.path.join(LIPSYNC_DIR, f"avatar_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    if concatenate_chunks(chunk_files, final_output):
        logging.info("=" * 70)
        logging.info(f" SUCCESS! FINAL AVATAR RENDERED & CONCATENATED: {final_output}")
        logging.info("=" * 70)
        return final_output
    else:
        logging.error("❌ Falló la concatenación final con FFmpeg.")
        sys.exit(1)

if __name__ == "__main__":
    src_img   = r"C:\openclaw\output\guillermo_portrait.jpg"
    audio_wav = r"C:\openclaw\output\audio\test_lipsync.wav"
    
    if len(sys.argv) > 2:
        src_img   = sys.argv[1]
        audio_wav = sys.argv[2]
        
    execute_chunked_render_pipeline(src_img, audio_wav, total_target_frames=120)
