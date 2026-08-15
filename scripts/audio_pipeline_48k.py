#!/usr/bin/env python3
"""
================================================================================
OPENCLAW AUDIO ENGINE 48kHz STEREO EBU R128 (2026.7.1)
Módulo Maestro de Generación, Normalización y Validación de Audio
Garantiza 100% de compatibilidad con Windows Native Media Player y Web Audio API
================================================================================
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN MAESTRA DE AUDIO (ESTÁNDAR BROADCAST)
# ==============================================================================
SAMPLE_RATE = 48000
CHANNELS = 2
AUDIO_CODEC = "aac"
BITRATE = "192k"
LOUDNORM_FILTER = "loudnorm=I=-16:TP=-1.5:LRA=11"

DEFAULT_VOICE_ES = "es-MX-JorgeNeural"
DEFAULT_VOICE_EN = "en-US-GuyNeural"

def log_event(message, level="INFO"):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] [{level}] {message}")

def probe_audio_stream(file_path):
    """
    Verifica con ffprobe los metadatos de audio exactos:
    - Sample Rate == 48000
    - Channels == 2
    - Duración > 0
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,channels,codec_name,duration:format=duration",
        "-of", "json",
        str(file_path)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        
        streams = data.get("streams", [])
        if not streams:
            raise ValueError("No se detectó ningún stream de audio en el archivo.")
            
        stream = streams[0]
        sr = int(stream.get("sample_rate", 0))
        ch = int(stream.get("channels", 0))
        codec = stream.get("codec_name", "")
        
        # Duración desde stream o format
        dur = float(stream.get("duration") or data.get("format", {}).get("duration", 0.0))
        
        return {
            "sample_rate": sr,
            "channels": ch,
            "codec": codec,
            "duration": dur,
            "valid": (sr == SAMPLE_RATE and ch == CHANNELS and dur > 0)
        }
    except Exception as e:
        log_event(f"Falla al inspeccionar stream de audio: {e}", "ERROR")
        return {"valid": False, "error": str(e)}

async def synthesize_speech_async(text, output_mp3_path, voice=DEFAULT_VOICE_ES, rate="+0%", pitch="+0Hz"):
    """
    Sintetiza texto a voz usando Edge-TTS asíncrono con captura de eventos.
    """
    import edge_tts
    log_event(f"Sintetizando voz con Edge-TTS ({voice})...")
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_mp3_path)
    log_event(f"Audio crudo sintetizado en: {output_mp3_path}", "SUCCESS")

def process_and_standardize_audio(input_path, output_path):
    """
    Convierte cualquier archivo de audio de entrada a AAC 48,000 Hz Stereo
    con normalización EBU R128 (-16 LUFS).
    """
    log_event(f"Procesando y normalizando audio hacia estándar broadcast 48k: {output_path}")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-ar", str(SAMPLE_RATE),
        "-ac", str(CHANNELS),
        "-c:a", AUDIO_CODEC,
        "-b:a", BITRATE,
        "-af", LOUDNORM_FILTER,
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_event("Transcodificación FFmpeg completada exitosamente.", "SUCCESS")
    except subprocess.CalledProcessError as e:
        log_event(f"Error en transcodificación FFmpeg: {e.stderr}", "ERROR")
        sys.exit(1)
        
    # Validación estricta con ffprobe
    metrics = probe_audio_stream(output_path)
    if not metrics.get("valid"):
        log_event(f"El audio generado violó los estándares de calidad: {metrics}", "FAIL")
        sys.exit(1)
        
    log_event(f"Audio 100% validado: {metrics['sample_rate']}Hz, {metrics['channels']} canales, {metrics['duration']:.2f}s", "SUCCESS")
    return metrics

def generate_broadcast_audio(text, output_path, lang="es"):
    """
    Función de entrada todo-en-uno: Texto -> Síntesis -> Normalización 48k -> Verificación.
    """
    voice = DEFAULT_VOICE_ES if lang == "es" else DEFAULT_VOICE_EN
    temp_raw = output_path + ".temp_raw.mp3"
    
    try:
        asyncio.run(synthesize_speech_async(text, temp_raw, voice=voice))
        metrics = process_and_standardize_audio(temp_raw, output_path)
        return metrics
    finally:
        if os.path.exists(temp_raw):
            try:
                os.remove(temp_raw)
            except OSError:
                pass

if __name__ == "__main__":
    sample_text = (
        "Bienvenidos a la Masterclass 2026 de HB Jewelry y OpenClaw. "
        "Hoy demostraremos la arquitectura de gobernanza vectorial en espacio R setecientos sesenta y ocho, "
        "con automatización de video de alta fidelidad y procesamiento cloud a cero costo operativo."
    )
    test_out = r"C:\openclaw\hb-jewelry\public\videos\test_audio_48k.aac"
    log_event("Ejecutando prueba unitaria del módulo de audio 48kHz...")
    res = generate_broadcast_audio(sample_text, test_out, lang="es")
    print(f"\n[TEST_RESULT] Audio 48k generado y verificado con éxito: {json.dumps(res, indent=2)}")
