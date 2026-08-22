#!/usr/bin/env python3
"""
================================================================================
OPENCLAW MODULAR CHUNK VIDEO GENERATOR (2026.7.1)
Renderizado modular de alta velocidad por bloques (Chunks de 5-10 min)
Integración nativa con Audio 48kHz Stereo EBU R128 + Teleprompter Subtitles
================================================================================
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

# Importar el motor de audio estandarizado
from audio_pipeline_48k import generate_broadcast_audio, probe_audio_stream

PUBLIC_DIR = r"C:\openclaw\hb-jewelry\public"
OUTPUT_DIR = os.path.join(PUBLIC_DIR, "videos", "masterclass_chunks")
FINAL_OUTPUT_PATH = os.path.join(PUBLIC_DIR, "videos", "masterclass_2026_final.mp4")

os.makedirs(OUTPUT_DIR, exist_ok=True)

AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar_transparent.png")
if not os.path.exists(AVATAR_PATH):
    AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar_pro.png")

def log_event(message, level="INFO"):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] [{level}] {message}")

def create_ass_subtitle(text_items, output_ass_path):
    """
    Crea subtítulos .ass estilizados (Montserrat / Arial, borde dorado, fondo translúcido).
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Teleprompter,Montserrat,48,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,2,5,850,80,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for item in text_items:
        start_str = format_ass_time(item["start"])
        end_str = format_ass_time(item["end"])
        text = item["text"].replace("\n", "\\N")
        events.append(f"Dialogue: 0,{start_str},{end_str},Teleprompter,,0,0,0,,{text}")
        
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def render_chunk(chunk_idx, script_text, output_mp4):
    """
    Genera audio 48k, subtítulos y renderiza el chunk de video con FFmpeg de forma acelerada.
    """
    log_event(f"--- [CHUNK {chunk_idx}] Iniciando generación modular ---")
    chunk_audio_path = os.path.join(OUTPUT_DIR, f"chunk_{chunk_idx}_audio.aac")
    chunk_sub_path = os.path.join(OUTPUT_DIR, f"chunk_{chunk_idx}_subs.ass")
    
    # 1. Generar audio 48k estandarizado
    audio_metrics = generate_broadcast_audio(script_text, chunk_audio_path, lang="es")
    duration = audio_metrics["duration"]
    
    # 2. Generar subtítulo
    sub_items = [{
        "start": 0.0,
        "end": duration,
        "text": script_text
    }]
    create_ass_subtitle(sub_items, chunk_sub_path)
    
    # Escapar path de subtítulos para filtro FFmpeg en Windows
    sub_filter_path = chunk_sub_path.replace("\\", "/").replace(":", "\\:")
    avatar_filter_path = AVATAR_PATH.replace("\\", "/").replace(":", "\\:")
    
    log_event(f"[CHUNK {chunk_idx}] Renderizando video 1080p ({duration:.2f}s) con aceleración FastStart...")
    
    # FFmpeg Filter Complex:
    # 1. Fondo gradiente cósmico (1920x1080)
    # 2. Superposición del avatar en el cuadrante izquierdo (x=80, y=180)
    # 3. Subtítulos teleprompter a la derecha
    filter_complex = (
        f"color=c=0x0a0a14:s=1920x1080:d={duration}[bg];"
        f"movie='{avatar_filter_path}'[raw_av];"
        f"[raw_av]scale=750:-1[av];"
        f"[bg][av]overlay=80:180[composite];"
        f"[composite]subtitles='{sub_filter_path}'[v]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=0x0a0a14:s=1920x1080:d={duration}",
        "-i", chunk_audio_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "copy",
        "-movflags", "+faststart",
        "-t", str(duration),
        str(output_mp4)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_event(f"[CHUNK {chunk_idx}] Chunk completado con éxito: {output_mp4}", "SUCCESS")
        return output_mp4
    except subprocess.CalledProcessError as e:
        log_event(f"[CHUNK {chunk_idx}] Error en renderizado FFmpeg: {e.stderr}", "ERROR")
        sys.exit(1)

def concatenate_chunks(chunk_paths, final_output):
    """
    Concatena todos los chunks en un archivo continuo sin recodificación (-c copy).
    """
    log_event("Concatenando chunks en archivo final unificado...")
    concat_list_file = os.path.join(OUTPUT_DIR, "concat_list.txt")
    
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for p in chunk_paths:
            # Formato FFmpeg concat: file 'C:/path/file.mp4'
            clean_path = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        "-movflags", "+faststart",
        str(final_output)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_event(f"Video final concatenado exitosamente en: {final_output}", "SUCCESS")
    except subprocess.CalledProcessError as e:
        log_event(f"Error concatenando chunks: {e.stderr}", "ERROR")
        sys.exit(1)

def run_masterclass_production():
    log_event("================================================================")
    log_event(" INICIANDO PRODUCCIÓN AUDIOVISUAL MODULAR (OPENCLAW 2026)")
    log_event("================================================================")
    
    # Bloques de guion demostrativos de alta cadencia
    script_modules = [
        "Bienvenidos al módulo 1. Arquitectura de Gobernanza Vectorial en R setecientos sesenta y ocho con normalización L2 unitaria y verificación anti alucinaciones.",
        "Módulo 2. Despliegue de infraestructura cloud resiliente: sincronización nativa en Google Drive cinco terabytes y distribución global a cero costo.",
        "Módulo 3. Automatización de agentes conversacionales para comercio electrónico de alta gama con catálogo de joyería fina y cierre por WhatsApp."
    ]
    
    chunk_files = []
    for idx, text in enumerate(script_modules, start=1):
        out_chunk = os.path.join(OUTPUT_DIR, f"chunk_{idx}.mp4")
        render_chunk(idx, text, out_chunk)
        chunk_files.append(out_chunk)
        
    concatenate_chunks(chunk_files, FINAL_OUTPUT_PATH)
    
    log_event("================================================================")
    log_event(" PRODUCCIÓN MODULAR CONCLUIDA CON ÉXITO")
    log_event("================================================================")
    return FINAL_OUTPUT_PATH

if __name__ == "__main__":
    run_masterclass_production()
