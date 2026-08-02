#!/usr/bin/env python3
"""
====================================================================
 OPENCLAW CADENCE & YOUTUBE SEO ENGINE (2026.7.1)
====================================================================
- ANALIZA CADENCIA ZERO ESTRÉS (10-12 char/s, pausas 0.8s)
- GENERA MARCAS DE TIEMPO (TIMESTAMPS) Y CAPÍTULOS SEO YOUTUBE
====================================================================
"""

import os
import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CADENCE_PARAMS = {
    "chars_per_second": 11,
    "pause_sentence": 0.8,
    "pause_paragraph": 1.5,
    "pause_emphasis": 0.4,
    "lufs_target": -14.0
}

def analyze_cadence(text: str) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_time = 0.0
    
    for sentence in sentences:
        if not sentence.strip():
            continue
        words = sentence.split()
        duration = len(sentence) / CADENCE_PARAMS["chars_per_second"]
        chunks.append({
            "text": sentence,
            "start": round(current_time, 2),
            "duration": round(duration, 2),
            "end": round(current_time + duration, 2),
            "pause_after": CADENCE_PARAMS["pause_sentence"]
        })
        current_time += duration + CADENCE_PARAMS["pause_sentence"]
        
    return chunks

def format_timestamp(seconds: float) -> str:
    total_sec = int(seconds)
    mins = total_sec // 60
    secs = total_sec % 60
    return f"{mins:02d}:{secs:02d}"

def generate_youtube_seo_description(title: str, chunks: list, tags: list) -> str:
    total_dur = chunks[-1]["end"] if chunks else 0.0
    
    chapters = ["00:00 Introducción al Curso"]
    for idx, c in enumerate(chunks):
        if idx > 0 and idx % 2 == 0:
            chapters.append(f"{format_timestamp(c['start'])} Capítulo {idx//2 + 1}: {c['text'][:40]}...")
            
    chapters.append(f"{format_timestamp(total_dur * 0.9)} Resumen y Conclusión")
    
    hashtags = " ".join([f"#{t}" for t in tags])
    
    desc = f"""{title}

━━━━━━━━━━━━━━━━━━━━━━━━━
📌 CAPÍTULOS Y MARCAS DE TIEMPO
━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(chapters)}

━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 ENLACES EDUCATIVOS EN VIVO
━━━━━━━━━━━━━━━━━━━━━━━━━
Plataforma: https://hb-jewelry-cloud-2026-2dff9.web.app

{hashtags}
"""
    return desc

if __name__ == "__main__":
    sample_script = "Hola, bienvenido a nuestro canal educativo de automatización e inteligencia artificial. Hoy aprenderemos cómo estructurar los 7 pilares fundamentales para escalar tu empresa con agentes autónomos. Cada proceso se diseña para eliminar tareas repetitivas y multiplicar la productividad."
    chunks = analyze_cadence(sample_script)
    seo_desc = generate_youtube_seo_description("Curso Completo de IA y Automatización 2026", chunks, ["IA", "Automatizacion", "Productividad", "OpenClaw"])
    
    out_json = r"C:\openclaw\hb-jewelry\public\cadence_seo_manifest.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks, "seo": seo_desc}, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Cadencia y SEO manifest generados en: {out_json}")
