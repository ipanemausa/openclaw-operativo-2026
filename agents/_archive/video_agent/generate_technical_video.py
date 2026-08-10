# =====================================================================
# OPENCLAW TECHNICAL DEMO VIDEO GENERATOR (DAG NODE)
# =====================================================================
# Genera una demostración técnica de la arquitectura de OpenClaw Cloud 2026:
# - Gemini 2.0 Flash Live Voice Engine
# - Baileys WhatsApp Business $0 API
# - Firebase RAG Vector DB (768-dim)
# =====================================================================

import os
import json

print("=========================================================")
print("  GENERANDO VIDEO TECNICO DE ARQUITECTURA OPENCLAW 2026  ")
print("=========================================================")

technical_dialogue = [
    {"speaker": "Usuario", "text": "OpenClaw, cual es el estado de la arquitectura full-stack de HB Jewelry?"},
    {"speaker": "Guillermo AI", "text": "La arquitectura esta 100% activa. Contenedores Docker en puertos 8080, 8091 y 3001, vectorizacion RAG de 768 dimensiones e integracion con Google Drive 5TB."},
    {"speaker": "Usuario", "text": "Demuestra la velocidad del motor de voz y WhatsApp $0."},
    {"speaker": "Guillermo AI", "text": "Procesando latencia de sub-100ms con Gemini 2.0 Flash Live y recepcion de mensajes de clientes via Baileys +1 (954) 684-4445."}
]

output_file = "C:/openclaw/hb-jewelry/public/technical_demo_script.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(technical_dialogue, f, indent=2, ensure_ascii=False)

print(f"[OK] Dialogo tecnico generado en: {output_file}")
print("=========================================================")
