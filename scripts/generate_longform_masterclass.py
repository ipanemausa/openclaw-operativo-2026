import os
import sys
import json
import asyncio
import subprocess
import shutil
from typing import Dict, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ==============================================================================
# CONFIGURACIÓN TÉCNICA Y GOBERNANZA VECTORIAL
# ==============================================================================
TARGET_VECTOR_DIM = 768
SIMILARITY_THRESHOLD = 0.82
SAMPLE_RATE = 48000
CHANNELS = 2
AUDIO_BITRATE = "192k"
VIDEO_FPS = 30
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
PIX_FMT = "yuv420p"
LOUDNORM_TARGET = "loudnorm=I=-16:TP=-1.5:LRA=11"

# ==============================================================================
# CAPA 1 & 2: DETECCIÓN DE HARDWARE Y ENRUTAMIENTO HÍBRIDO
# ==============================================================================
class HardwareRouter:
    @staticmethod
    def detect_video_encoder() -> Dict[str, str]:
        """Detecta aceleración GPU (NVENC) o recurre a CPU (libx264) de forma segura."""
        has_gpu = False
        try:
            res = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True)
            if "h264_nvenc" in res.stdout:
                gpu_check = subprocess.run(["nvidia-smi"], capture_output=True)
                if gpu_check.returncode == 0:
                    has_gpu = True
        except Exception:
            has_gpu = False

        if has_gpu:
            print("⚡ [HARDWARE] GPU NVIDIA detectada: Activando encoder por hardware (h264_nvenc).")
            return {"encoder": "h264_nvenc", "preset": "p4", "type": "GPU"}
        else:
            print("⚙️ [HARDWARE] Modo CPU Online: Usando codificador optimizado (libx264).")
            return {"encoder": "libx264", "preset": "ultrafast", "type": "CPU"}

# ==============================================================================
# CAPA 3: PIPELINE DE AUDIO Y RENDERIZADO DETERMINISTA (DAG)
# ==============================================================================
class AudioProcessor:
    @staticmethod
    async def synthesize(text: str, output_path: str, voice: str = "es-MX-JorgeNeural"):
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    @staticmethod
    def normalize_ebu_r128(input_raw: str, output_aac: str):
        cmd = [
            "ffmpeg", "-y",
            "-i", input_raw,
            "-af", LOUDNORM_TARGET,
            "-c:a", "aac",
            "-b:a", AUDIO_BITRATE,
            "-ar", str(SAMPLE_RATE),
            "-ac", str(CHANNELS),
            output_aac
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

class VideoCompositor:
    @staticmethod
    def render_chunk(image_path: str, audio_path: str, output_chunk: str, hw_config: Dict[str, str]):
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-framerate", str(VIDEO_FPS),
            "-i", image_path,
            "-i", audio_path,
            "-c:v", hw_config["encoder"],
            "-preset", hw_config["preset"],
            "-tune", "stillimage" if hw_config["type"] == "CPU" else "hq",
            "-pix_fmt", PIX_FMT,
            "-r", str(VIDEO_FPS),
            "-vsync", "cfr",
            "-s", f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
            "-c:a", "aac",
            "-b:a", AUDIO_BITRATE,
            "-ar", str(SAMPLE_RATE),
            "-ac", str(CHANNELS),
            "-shortest",
            output_chunk
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def concatenate_faststart(manifest_path: str, final_output: str):
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", manifest_path,
            "-c", "copy",
            "-movflags", "+faststart",
            final_output
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# ==============================================================================
# CAPA 4: AUDITORÍA E2E Y CIERRE
# ==============================================================================
def validate_output(file_path: str) -> bool:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    probe = json.loads(res.stdout)
    v_ok = any(s.get("codec_type") == "video" for s in probe.get("streams", []))
    a_ok = any(s.get("codec_type") == "audio" and int(s.get("sample_rate", 0)) == SAMPLE_RATE for s in probe.get("streams", []))
    return v_ok and a_ok

# ==============================================================================
# EJECUCIÓN ORQUESTADA
# ==============================================================================
async def main():
    print("==================================================================")
    print("🚀 INICIANDO ORQUESTADOR MAESTRO HÍBRIDO (CPU / GPU SELECTIVO)")
    print("==================================================================")
    
    hw_config = HardwareRouter.detect_video_encoder()
    
    os.makedirs("runtime/temp", exist_ok=True)
    os.makedirs("runtime/chunks", exist_ok=True)
    os.makedirs("runtime/final", exist_ok=True)
    
    manifest_json_path = "runtime/chunks/script_manifest_768.json"
    if os.path.exists(manifest_json_path):
        with open(manifest_json_path, "r", encoding="utf-8") as f:
            manifest_json = json.load(f)
        chunks_data = [
            {"text": c["script_text"], "img": f"runtime/slide_{c['chunk_id']}.png"}
            for c in manifest_json.get("chunks", [])
        ]
        print(f"📖 [RAG-768] Manifiesto cargado exitosamente: {len(chunks_data)} chunks.")
    else:
        chunks_data = [
            {"text": "Iniciando análisis y renderizado en arquitectura desacoplada.", "img": "runtime/slide1.png"},
            {"text": "Integración híbrida verificada con normalización de audio estéreo.", "img": "runtime/slide2.png"}
        ]
    
    # Generar slides base si no existen
    for c in chunks_data:
        if not os.path.exists(c["img"]):
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x0B0F19:s=1920x1080:d=1",
                "-vframes", "1", c["img"]
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    manifest_file = "runtime/chunks/concat_list.txt"
    entries = []

    for i, chunk in enumerate(chunks_data):
        raw_audio = f"runtime/temp/raw_{i}.mp3"
        norm_audio = f"runtime/temp/norm_{i}.aac"
        chunk_mp4 = f"runtime/chunks/chunk_{i}.mp4"
        
        print(f"[Procesando Segmento {i+1}/{len(chunks_data)}]")
        await AudioProcessor.synthesize(chunk["text"], raw_audio)
        AudioProcessor.normalize_ebu_r128(raw_audio, norm_audio)
        VideoCompositor.render_chunk(chunk["img"], norm_audio, chunk_mp4, hw_config)
        
        # En Windows FFmpeg concat requiere rutas con forward slashes
        abs_path = os.path.abspath(chunk_mp4).replace("\\", "/")
        entries.append(f"file '{abs_path}'")

    with open(manifest_file, "w", encoding="utf-8") as f:
        f.write("\n".join(entries) + "\n")

    final_video = "runtime/final/masterclass_e2e_complete.mp4"
    print("\n[Ensamblando Video Final con Stream Copy y Faststart]")
    VideoCompositor.concatenate_faststart(manifest_file, final_video)

    if validate_output(final_video):
        print(f"\n✅ PIPELINE COMPLETADO EXITOSAMENTE: {final_video}")
    else:
        print("\n❌ Error en la verificación del contenedor.")

if __name__ == "__main__":
    asyncio.run(main())
