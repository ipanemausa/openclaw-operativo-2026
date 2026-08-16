import subprocess
import json
import asyncio
import os
import sys
import edge_tts

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ==============================================================================
# CONFIGURACIÓN ESTÁNDAR DE AUDIO (GOBERNANZA VECTORIAL)
# ==============================================================================
SAMPLE_RATE = 48000
CHANNELS = 2
BITRATE = "192k"
LOUDNORM_FILTER = "loudnorm=I=-16:TP=-1.5:LRA=11"
DEFAULT_VOICE = "es-MX-JorgeNeural"  # Alternativa: "en-US-GuyNeural"

async def generate_tts(text: str, output_raw_path: str, voice: str = DEFAULT_VOICE):
    """Genera audio base mediante Edge-TTS."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_raw_path)

def process_audio_pipeline(input_raw_path: str, output_final_path: str):
    """Aplica normalización EBU R128 y estandariza a 48kHz Stereo 192kbps AAC."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_raw_path,
        "-af", LOUDNORM_FILTER,
        "-c:a", "aac",
        "-b:a", BITRATE,
        "-ar", str(SAMPLE_RATE),
        "-ac", str(CHANNELS),
        output_final_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def validate_stream_ffprobe(audio_file_path: str) -> bool:
    """Valida mediante ffprobe la integridad técnica del stream de audio generado."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        audio_file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    probe_data = json.loads(result.stdout)
    
    for stream in probe_data.get("streams", []):
        if stream.get("codec_type") == "audio":
            codec = stream.get("codec_name")
            sample_rate = int(stream.get("sample_rate", 0))
            channels = int(stream.get("channels", 0))
            
            is_valid = (codec == "aac" and sample_rate == SAMPLE_RATE and channels == CHANNELS)
            print(f"[FFPROBE VALIDATION] Codec: {codec} | Sample Rate: {sample_rate}Hz | Channels: {channels} -> Valid: {is_valid}")
            return is_valid
            
    return False

async def main():
    os.makedirs("output/audio", exist_ok=True)
    raw_audio = "output/audio/temp_raw.mp3"
    final_audio = "output/audio/masterclass_48k_stereo.aac"
    
    sample_text = (
        "Iniciando el pipeline de audio estandarizado a 48 kilohercios estéreo. "
        "Normalización EBU R128 verificada y lista para la generación de masterclass de larga duración."
    )
    
    print("[1/3] Generando síntesis de voz con Edge-TTS...")
    await generate_tts(sample_text, raw_audio)
    
    print("[2/3] Procesando normalización EBU R128 y encoding 48kHz Stereo...")
    process_audio_pipeline(raw_audio, final_audio)
    
    print("[3/3] Validando streams con ffprobe...")
    valid = validate_stream_ffprobe(final_audio)
    
    if valid:
        if os.path.exists(raw_audio):
            os.remove(raw_audio)
        print("✅ Pipeline de audio validado con éxito.")
    else:
        print("❌ Error de validación: el stream no cumple con los estándares definidos.")

if __name__ == "__main__":
    asyncio.run(main())
