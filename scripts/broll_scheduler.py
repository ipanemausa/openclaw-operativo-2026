#!/usr/bin/env python3
"""
====================================================================
 OPENCLAW B-ROLL DYNAMIC SCHEDULER ENGINE (2026.7.1)
====================================================================
- FASE B DEL PLAN MAESTRO CLAUDE DC
- PROGRAMACIÓN AUTOMÁTICA DE TRANSICIONES A-ROLL ➔ B-ROLL ➔ A-ROLL
- DETECCIÓN DE KEYWORDS EDUCATIVAS DE IA, AUTOMATIZACIÓN Y NEGOCIOS
====================================================================
"""

import os
import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EDUCATIONAL_KEYWORDS = [
    r"automatizaci[oó]n|agentes|ia|inteligencia artificial|pilares|productividad|escudo|seguridad|nube",
    r"proceso|fricci[oó]n|comunidad|l[ií]deres|futuro|escalar|eficiencia|sistema"
]

def schedule_broll_events(teleprompter_json_path: str, output_schedule_path: str) -> dict:
    if not os.path.exists(teleprompter_json_path):
        # Fallback manifest si no existe
        teleprompter = {
            "total_duration": 34.26,
            "chunks": [
                {"text": "Hola, bienvenido a nuestro canal educativo de automatización e inteligencia artificial. Soy Guillermo.", "start": 0.0, "end": 7.5},
                {"text": "Hoy aprenderemos cómo estructurar los 7 pilares fundamentales para escalar tu empresa con agentes autónomos.", "start": 8.3, "end": 17.1},
                {"text": "Cada proceso se diseña para eliminar tareas repetitivas, reducir la fricción operativa y multiplicar la productividad.", "start": 17.9, "end": 26.8},
                {"text": "Nuestra meta es construir una comunidad sólida de líderes que dominen las herramientas del futuro hoy mismo.", "start": 27.6, "end": 34.26}
            ]
        }
    else:
        with open(teleprompter_json_path, "r", encoding="utf-8") as f:
            teleprompter = json.load(f)

    broll_events = []
    
    for chunk in teleprompter.get("chunks", []):
        text = chunk.get("text", "").lower()
        # Verificar si contiene palabras clave educativas
        matched = False
        for kw_pattern in EDUCATIONAL_KEYWORDS:
            if re.search(kw_pattern, text):
                matched = True
                break
                
        if matched:
            start_t = chunk.get("start", 0.0)
            end_t = chunk.get("end", start_t + 5.0)
            mid_t = round(start_t + (end_t - start_t) * 0.2, 2)
            broll_dur = round((end_t - start_t) * 0.6, 2)
            
            broll_events.append({
                "type": "broll_overlay",
                "start_time": mid_t,
                "end_time": round(mid_t + broll_dur, 2),
                "duration": broll_dur,
                "label": "Infografía Educativa de IA y Automatización",
                "keyword_trigger": text[:30] + "..."
            })

    schedule_output = {
        "version": "2026.7.1",
        "total_duration": teleprompter.get("total_duration", 34.26),
        "total_broll_events": len(broll_events),
        "events": broll_events
    }

    os.makedirs(os.path.dirname(output_schedule_path), exist_ok=True)
    with open(output_schedule_path, "w", encoding="utf-8") as f:
        json.dump(schedule_output, f, indent=2, ensure_ascii=False)

    print(f"✅ Programador B-Roll completado: {len(broll_events)} eventos agendados en: {output_schedule_path}")
    return schedule_output

if __name__ == "__main__":
    t_path = r"C:\openclaw\hb-jewelry\public\cadence_seo_manifest.json"
    out_path = r"C:\openclaw\hb-jewelry\public\broll_schedule.json"
    schedule_broll_events(t_path, out_path)
