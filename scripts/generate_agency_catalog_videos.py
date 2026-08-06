import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=========================================================")
print(" 🚀 GENERADOR MAESTRO DE VIDEOS PARA AGENCIA DE IA B2B   ")
print("=========================================================")

PUBLIC_DIR = Path(r"C:\openclaw\hb-jewelry\public")
VIDEOS_DIR = PUBLIC_DIR / "videos" / "agencia"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

AGENCY_CAMPAIGNS = [
    {
        "id": "agencia-b2b-intro",
        "name": "agencia_ai_b2b_master.mp4",
        "title": "🚀 Agencia IA: Asesoría & Automatización Empresarial",
        "tag": "AGENCIA B2B (15s)",
        "dur": "0:15",
        "description": "Presentación ejecutiva de automatización de procesos, WhatsApp $0 y agentes autónomos para empresas."
    },
    {
        "id": "real-estate-ai",
        "name": "real_estate_ai_promo.mp4",
        "title": "🏢 Real Estate IA: Citas 24/7 & Calificación de Leads",
        "tag": "REAL ESTATE IA",
        "dur": "0:20",
        "description": "Demostración de agentes de Inteligencia Artificial para agencias inmobiliarias y venta de propiedades."
    },
    {
        "id": "servicios-profesionales-ai",
        "name": "servicios_profesionales_ai.mp4",
        "title": "💼 Servicios Profesionales & Salud: Agendas Autónomas",
        "tag": "SERVICIOS & SALUD",
        "dur": "0:18",
        "description": "Automatización de agendamiento de citas, filtro de clientes y atención médica/legal 24/7."
    }
]

manifest_path = PUBLIC_DIR / "videos" / "agencia_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(AGENCY_CAMPAIGNS, f, indent=2, ensure_ascii=False)

print(f"✅ Manifiesto de Agencia generado en: {manifest_path}")
