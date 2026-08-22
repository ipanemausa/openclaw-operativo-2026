"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — AUTONOMIC AUDIOVISUAL PIPELINE (DAG CPM)
==============================================================================
Ruta Crítica Multimodal:
1. Generación de Guión Dinámico RAG 768D (DeepSeek / Qwen + Sandbox)
2. Síntesis Vocal Edge-TTS Broadcast 48kHz Stereo (-16 LUFS EBU R128)
3. Validación FFprobe determinista
4. Exportación de Asset Listo para Render / CDN

Política: $0 Costo Operativo / Cero Mocks / Ejecución Inmediata
==============================================================================
"""

import os
import sys
import json
import asyncio
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from rag_ai_bridge import rag_answer
from audio_pipeline_48k import generate_tts, process_audio_pipeline, validate_stream_ffprobe

OUTPUT_DIR = Path("runtime/output_video_2026")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def run_autonomic_audiovisual_pipeline(topic: str):
    print("=" * 60)
    print("  🎬 OPENCLAW AUTONOMIC AUDIOVISUAL ENGINE (CPM DAG)")
    print(f"  Tema: '{topic}'")
    print("=" * 60)

    # ─── NODO 1: Generación de Guión Dinámico vía RAG + DeepSeek ───────────
    print("\n[NODO 1/3] Generando guión comercial con RAG + DeepSeek...")
    query = (
        f"Genera un guión de locución de 30 segundos (máximo 70 palabras) "
        f"para un video promocional de HB Jewelry enfocado en: '{topic}'. "
        f"Tono elegante, persuasivo y comercial. Solo el texto de la locución, sin acotaciones ni corchetes."
    )
    result = rag_answer(query, task_type="jewelry")
    
    script_text = result["answer"].replace('"', '').replace('\n', ' ').strip()
    # Limpiar posibles textos extra
    if ":" in script_text and len(script_text.split(":")[0]) < 20:
        script_text = script_text.split(":", 1)[1].strip()

    print(f"  [OK] Guión generado ({len(script_text.split())} palabras | {result['latency_ms']}ms):")
    print(f"  \"{script_text}\"")

    # Guardar manifiesto del guión
    manifest_path = OUTPUT_DIR / "script_manifest.json"
    manifest_data = {
        "topic": topic,
        "model": result["model"],
        "tokens": result["tokens"],
        "script": script_text
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    # ─── NODO 2: Síntesis de Voz Broadcast 48kHz (Edge-TTS) ────────────────
    print("\n[NODO 2/3] Sintetizando audio broadcast 48kHz (-16 LUFS EBU R128)...")
    raw_audio_path = str(OUTPUT_DIR / "voice_raw.mp3")
    final_audio_path = str(OUTPUT_DIR / "voice_master_48k.aac")

    await generate_tts(script_text, raw_audio_path, voice="es-MX-JorgeNeural")
    process_audio_pipeline(raw_audio_path, final_audio_path)
    print(f"  [OK] Audio masterizado generado: {final_audio_path}")

    # ─── NODO 3: Validación Técnica FFprobe ────────────────────────────────
    print("\n[NODO 3/3] Validando stream con FFprobe...")
    is_valid = validate_stream_ffprobe(final_audio_path)
    
    print("\n" + "=" * 60)
    if is_valid:
        print("  ✅ PIPELINE AUDIOVISUAL COMPLETADO CON ÉXITO")
        print(f"  Asset de Audio: {final_audio_path}")
        print(f"  Manifiesto:     {manifest_path}")
        print("  Costo:          $0.00 USD")
    else:
        print("  ❌ Falló la validación FFprobe.")
    print("=" * 60)

    return is_valid

if __name__ == "__main__":
    topic_arg = sys.argv[1] if len(sys.argv) > 1 else "Colección Alta Joyería Esmeraldas y Oro 18K"
    asyncio.run(run_autonomic_audiovisual_pipeline(topic_arg))
