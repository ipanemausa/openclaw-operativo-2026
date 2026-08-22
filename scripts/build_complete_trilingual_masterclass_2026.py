#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenClaw Trilingual Masterclass 1080p Production Engine (2026.8.0)
Genera las 3 Masterclasses Completas en 1080p FastStart:
1. Español (Acento Colombiano Paisa - Guillermo)
2. English (Oxford / Silicon Valley Executive)
3. 中文 Mandarín (Alibaba Cloud / Standard Mandarin)
"""

import os
import sys
import math
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import whisper

# Configurar codificación UTF-8 para consola
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
RUNTIME = ROOT / "runtime" / "masterclass_trilingue_2026"
RUNTIME.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 25

# Importar motor cósmico y de prosodia
sys.path.insert(0, str(ROOT / "scripts"))
from cosmic_universe_engine import render_cosmic_universe_frame
from sovereign_audio_prosody_engine import SovereignProsodyEngine

# Cargar Matriz Trilingüe Canónica
MATRIX_FILE = ROOT / "backend" / "database" / "trilingual_masterclass_matrix_2026.json"
with open(MATRIX_FILE, "r", encoding="utf-8") as f:
    TRILINGUAL_DATA = json.load(f)

TRILINGUAL_MODULES = TRILINGUAL_DATA["modules"]

prosody_engine = SovereignProsodyEngine()

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_module_speech(text: str, out_path: str, lang: str):
    if lang == "es":
        voice = "es-CO-GonzaloNeural"
        rate = "-8%"
        pitch = "-4Hz"
    elif lang == "en":
        voice = "en-US-AndrewMultilingualNeural"
        rate = "-6%"
        pitch = "-3Hz"
    elif lang == "zh":
        voice = "zh-CN-YunxiNeural"
        rate = "-4%"
        pitch = "-2Hz"
    else:
        voice = "es-CO-GonzaloNeural"
        rate = "-8%"
        pitch = "-4Hz"

    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def build_full_audio_for_language(lang: str):
    print(f"\n[FASE 1/4 - {lang.upper()}] Sintetizando 8 módulos en {lang.upper()}...")
    raw_files = []
    
    for i, mod in enumerate(TRILINGUAL_MODULES):
        text = mod["text"][lang]
        raw_path = str(RUNTIME / f"{lang}_raw_{i}.mp3")
        asyncio.run(synthesize_module_speech(text, raw_path, lang))
        raw_files.append(raw_path)

    # Masterizar cada audio a 48kHz con pausas de respiración
    master_files = []
    for i, raw in enumerate(raw_files):
        master_path = str(RUNTIME / f"{lang}_master_{i}.aac")
        prosody_engine._master_audio(Path(raw), Path(master_path))
        master_files.append(master_path)

    # Crear silencio de 1.0s entre módulos
    pause_path = str(RUNTIME / f"pause_10s_{lang}.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "1.0", "-c:a", "aac", "-b:a", "256k", pause_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Concatenar todos los módulos
    concat_list_path = str(RUNTIME / f"concat_{lang}.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for i, mf in enumerate(master_files):
            f.write(f"file '{mf.replace(os.sep, '/')}'\n")
            if i < len(master_files) - 1:
                f.write(f"file '{pause_path.replace(os.sep, '/')}'\n")

    full_audio_path = str(RUNTIME / f"master_audio_{lang}_48k.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c:a", "copy", full_audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    dur = get_audio_duration(full_audio_path)
    print(f"  [OK] Audio Maestro ({lang.upper()}): {dur:.2f}s ({dur/60:.2f} min)")
    return full_audio_path, dur, master_files

def align_words_for_language(whisper_model, master_files: list, lang: str):
    print(f"\n[FASE 2/4 - {lang.upper()}] Sincronizando subtítulos canónicos Ground Truth...")
    whisper_lang = "es" if lang == "es" else ("en" if lang == "en" else "zh")
    
    current_time_offset = 0.0
    module_timings = []
    
    for i, (mf, mod) in enumerate(zip(master_files, TRILINGUAL_MODULES)):
        dur = get_audio_duration(mf)
        mod_start = current_time_offset
        mod_end = mod_start + dur
        
        # Whisper solo para calcular timestamps [start, end]
        res = whisper_model.transcribe(mf, language=whisper_lang, word_timestamps=True)
        detected_words = []
        for seg in res.get("segments", []):
            for w in seg.get("words", []):
                detected_words.append(w)
                
        # Texto canónico exacto (Ground Truth)
        canonical_text = mod["text"][lang]
        canonical_tokens = canonical_text.split()
        
        aligned_words = []
        if len(detected_words) > 0 and len(canonical_tokens) > 0:
            scale = len(detected_words) / len(canonical_tokens)
            for c_idx, c_tok in enumerate(canonical_tokens):
                w_idx = min(int(c_idx * scale), len(detected_words) - 1)
                w_obj = detected_words[w_idx]
                aligned_words.append({
                    "word": c_tok,
                    "start": mod_start + w_obj["start"],
                    "end": mod_start + w_obj["end"]
                })
        else:
            tok_dur = dur / max(len(canonical_tokens), 1)
            for c_idx, c_tok in enumerate(canonical_tokens):
                aligned_words.append({
                    "word": c_tok,
                    "start": mod_start + c_idx * tok_dur,
                    "end": mod_start + (c_idx + 1) * tok_dur
                })
                
        module_timings.append({
            "num": mod["num"],
            "badge": mod["badge"][lang],
            "title": mod["title"][lang],
            "concept": mod["concept"][lang],
            "start": mod_start,
            "end": mod_end,
            "words": aligned_words
        })
        current_time_offset = mod_end + 1.0  # +1s de pausa
        
    return module_timings

def get_fonts():
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 26)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_concept = ImageFont.truetype("arial.ttf", 24)
        font_subs = ImageFont.truetype("arialbd.ttf", 36)
        font_brand = ImageFont.truetype("arialbd.ttf", 28)
    except:
        font_badge = font_title = font_concept = font_subs = font_brand = ImageFont.load_default()
    return font_badge, font_title, font_concept, font_subs, font_brand

def render_trilingual_masterclass(lang: str, whisper_model):
    print(f"\n============================================================")
    print(f"  [RENDER] COMPILANDO MASTERCLASS OPENCLAW ({lang.upper()}) 1080P")
    print(f"============================================================")
    
    # 1. Generar audio maestro
    full_audio_path, total_duration, master_files = build_full_audio_for_language(lang)
    
    # 2. Sincronizar palabras
    module_timings = align_words_for_language(whisper_model, master_files, lang)
    
    total_frames = int(total_duration * FPS)
    temp_frames_dir = RUNTIME / f"temp_frames_{lang}"
    temp_frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Cargar avatar oficial con bordado HB.OS
    avatar_path = ROOT / "assets" / "avatar_transparent_hbos.png"
    if not avatar_path.exists():
        avatar_path = ROOT / "assets" / "avatar_transparent.png"
    avatar_img = Image.open(str(avatar_path)).convert("RGBA")
    
    # Escalar avatar a 880x880 para visual cinematográfica
    avatar_h = 880
    avatar_w = int(avatar_img.width * (avatar_h / avatar_img.height))
    avatar_img = avatar_img.resize((avatar_w, avatar_h), Image.Resampling.LANCZOS)
    
    font_badge, font_title, font_concept, font_subs, font_brand = get_fonts()
    
    print(f"\n[FASE 3/4 - {lang.upper()}] Renderizando {total_frames} fotogramas Full HD 1080p...")
    
    for f_idx in range(total_frames):
        t_sec = f_idx / FPS
        
        # Encontrar módulo activo
        active_mod = module_timings[-1]
        for m in module_timings:
            if m["start"] <= t_sec <= m["end"] + 1.0:
                active_mod = m
                break
                
        # Renderizar fondo cósmico dinámico
        frame = render_cosmic_universe_frame(t_sec)
        
        # Micro-movimiento suave de respiración en el avatar
        breath_y = int(math.sin(t_sec * 1.5) * 4)
        avatar_x = WIDTH - avatar_w - 60
        avatar_y = HEIGHT - avatar_h + 10 + breath_y
        frame.paste(avatar_img, (avatar_x, avatar_y), avatar_img)
        
        draw = ImageDraw.Draw(frame)
        
        # ─── HEADER MINIMALISTA SUPERIOR ──────────────────────────────────────
        header_y = 50
        draw.text((70, header_y), "HB.OS", fill=(255, 215, 0), font=font_brand)
        draw.text((180, header_y + 4), "|  SOVEREIGN AI OPERATING SYSTEM 2026", fill=(180, 200, 230), font=font_concept)
        
        lang_label = "ESPAÑOL (PAISA MASTER)" if lang=="es" else ("ENGLISH (EXECUTIVE MASTER)" if lang=="en" else "中文 MANDARIN (SOVEREIGN MASTER)")
        draw.text((WIDTH - 480, header_y + 4), f"AUDIO: {lang_label}", fill=(120, 230, 180), font=font_concept)
        draw.line([(70, header_y + 45), (WIDTH - 70, header_y + 45)], fill=(255, 215, 0, 80), width=1)
        
        # ─── TARJETA PRINCIPAL DEL MÓDULO (LADO IZQUIERDO) ────────────────────
        box_x = 70
        box_y = 150
        
        # Badge de categoría
        draw.rectangle([(box_x, box_y), (box_x + 360, box_y + 42)], fill=(20, 35, 65, 230), outline=(255, 215, 0), width=2)
        draw.text((box_x + 16, box_y + 7), f"MÓDULO {active_mod['num']} // {active_mod['badge']}", fill=(255, 215, 0), font=font_badge)
        
        # Título principal
        title_y = box_y + 65
        draw.text((box_x, title_y), active_mod["title"], fill=(255, 255, 255), font=font_title)
        
        # Concepto clave
        concept_y = title_y + 65
        draw.text((box_x, concept_y), f"▶ {active_mod['concept']}", fill=(130, 200, 255), font=font_concept)
        
        # ─── SUBTÍTULOS KARAOKE GROUND TRUTH (INFERIOR) ──────────────────────
        sub_words = active_mod["words"]
        active_word_idx = -1
        for w_i, w_obj in enumerate(sub_words):
            if w_obj["start"] <= t_sec <= w_obj["end"]:
                active_word_idx = w_i
                break
            elif t_sec > w_obj["end"]:
                active_word_idx = w_i
                
        # Mostrar ventana de 8 palabras
        win_size = 8
        if active_word_idx != -1:
            start_w = max(0, active_word_idx - 3)
            end_w = min(len(sub_words), start_w + win_size)
            chunk = sub_words[start_w:end_w]
            
            sub_x = 70
            sub_y = HEIGHT - 180
            
            # Fondo del subtítulo
            draw.rectangle([(sub_x - 15, sub_y - 12), (WIDTH - avatar_w - 90, sub_y + 60)], fill=(5, 10, 20, 220), outline=(0, 150, 255, 120), width=1)
            
            cursor_x = sub_x
            for w_obj in chunk:
                is_active = (w_obj["start"] <= t_sec <= w_obj["end"])
                color = (255, 215, 0) if is_active else (220, 230, 245)
                w_str = w_obj["word"] + " "
                draw.text((cursor_x, sub_y), w_str, fill=color, font=font_subs)
                try:
                    w_bbox = font_subs.getbbox(w_str)
                    w_width = w_bbox[2] - w_bbox[0]
                except:
                    w_width = len(w_str) * 20
                cursor_x += w_width
                
        # Guardar fotograma
        frame_filename = temp_frames_dir / f"frame_{f_idx:06d}.jpg"
        frame.convert("RGB").save(str(frame_filename), quality=92)
        
        if f_idx % 600 == 0:
            print(f"    -> [{lang.upper()}] Fotograma {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%)...")

    # ─── FASE 4: CODIFICACIÓN FINAL CON FFMPEG FASTSTART ─────────────────────
    print(f"\n[FASE 4/4 - {lang.upper()}] Codificando Masterclass 1080p con FFmpeg FastStart...")
    
    output_filename = f"OpenClaw_Masterclass_{'Espanol' if lang=='es' else ('English' if lang=='en' else 'Mandarin')}_1080p.mp4"
    final_output = RUNTIME / output_filename
    
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(temp_frames_dir / "frame_%06d.jpg"),
        "-i", full_audio_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        str(final_output)
    ]
    
    subprocess.run(cmd_ffmpeg, check=True)
    
    # Limpiar fotogramas temporales
    import shutil
    shutil.rmtree(str(temp_frames_dir), ignore_errors=True)
    
    out_size_mb = final_output.stat().st_size / (1024 * 1024)
    print(f"\n============================================================")
    print(f"  [OK] MASTERCLASS {lang.upper()} GENERADA EXITOSAMENTE")
    print(f"  Ruta:     {final_output}")
    print(f"  Tamaño:   {out_size_mb:.2f} MB")
    print(f"  Duración: {total_duration:.2f} segundos ({total_duration/60:.2f} min)")
    print(f"============================================================")
    return str(final_output)

def render_all_three_masterclasses():
    print("\n[INIT] Cargando modelo Whisper para sincronización Ground Truth...")
    whisper_model = whisper.load_model("base")
    
    out_es = render_trilingual_masterclass("es", whisper_model)
    out_en = render_trilingual_masterclass("en", whisper_model)
    out_zh = render_trilingual_masterclass("zh", whisper_model)
    
    print("\n============================================================")
    print("  [OK] LAS 3 MASTERCLASSES (ESPAÑOL, ENGLISH, 中文 MANDARIN) LISTAS")
    print(f"  1. Español:  {out_es}")
    print(f"  2. English:  {out_en}")
    print(f"  3. 中文:     {out_zh}")
    print("============================================================")

if __name__ == "__main__":
    render_all_three_masterclasses()
