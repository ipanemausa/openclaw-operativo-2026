#!/usr/bin/env python3
"""
====================================================================
 OPENCLAW INTENT MAPPER ENGINE (2026.7.1)
====================================================================
- MAPEA FRASES DE 1 LÍNEA A ACCIONES DEL SISTEMA
- EJECUTA AUTOMÁTICAMENTE: AUDITORÍA, VIDEO, DEPLOY, BACKUP, BUILD
====================================================================
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OPERATIVO_DIR = r"C:\Users\ipane\openclaw-operativo-2026"
FRONTEND_DIR = r"C:\openclaw\hb-jewelry"

INTENTS = {
    # 1. Auditoría de Salud
    r"audita.*app|audit.*app|run.*audit|revisar.*app|paneo.*general": {
        "action": "audit",
        "cmd": ["python", os.path.join(OPERATIVO_DIR, "scripts", "run_app_autonomic_audit.py")],
        "label": "🤖 Ejecutando Robot Auditor de Paneo General...",
        "timeout": 45
    },
    # 2. Generador de Video Educativo
    r"crea.*video|genera.*video|make.*video|nuevo.*video": {
        "action": "video",
        "cmd": ["python", os.path.join(OPERATIVO_DIR, "scripts", "generate_real_video_composite.py")],
        "label": "🎬 Iniciando generación de video en estudio 1080p...",
        "timeout": 300
    },
    # 3. Respaldo y Cierre de Jornada
    r"respalda.*cierra|cierra.*respalda|pipeline.*cierre|cierre": {
        "action": "backup_close",
        "cmd": ["powershell", "-ExecutionPolicy", "Bypass", "-File", os.path.join(OPERATIVO_DIR, "scripts", "pipeline-cierre.ps1")],
        "label": "💾 Ejecutando Pipeline DAG de Cierre y Respaldo 5TB...",
        "timeout": 300
    },
    # 4. Despliegue en Firebase Hosting
    r"deploya|deploy|publica.*firebase|firebase.*deploy": {
        "action": "deploy",
        "cmd": ["npx", "firebase", "deploy", "--only", "hosting"],
        "label": "🚀 Desplegando en Firebase Cloud Hosting...",
        "timeout": 120,
        "cwd": FRONTEND_DIR
    },
    # 5. Compilación Vite
    r"build|compila|npm.*build": {
        "action": "build",
        "cmd": ["npm.cmd", "run", "build"],
        "label": "⚙️ Compilando bundle de producción con Vite...",
        "timeout": 60,
        "cwd": FRONTEND_DIR
    }
}

def map_intent(phrase: str) -> dict:
    phrase_lower = phrase.lower().strip()
    for pattern, intent_data in INTENTS.items():
        if re.search(pattern, phrase_lower):
            return intent_data
    return None

def execute_intent(phrase: str) -> dict:
    intent = map_intent(phrase)
    if not intent:
        return {
            "status": "unknown",
            "message": f"No se reconoció la intención: '{phrase}'",
            "available_intents": ["AUDITA LA APP", "CREA VIDEO", "RESPALDA Y CIERRA", "DEPLOYA", "BUILD"]
        }
    
    print(f"⚡ {intent['label']}")
    try:
        kwargs = {
            "capture_output": True,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "timeout": intent.get("timeout", 60)
        }
        if "cwd" in intent:
            kwargs["cwd"] = intent["cwd"]
        
        result = subprocess.run(intent["cmd"], **kwargs)
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "action": intent["action"],
            "stdout": result.stdout[-1000:] if result.stdout else "",
            "stderr": result.stderr[-500:] if result.stderr else "",
            "returncode": result.returncode,
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "action": intent["action"], "message": "Tiempo límite de ejecución excedido"}
    except Exception as e:
        return {"status": "error", "action": intent["action"], "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        phrase = "AUDITA LA APP"
    else:
        phrase = " ".join(sys.argv[1:])
        
    res = execute_intent(phrase)
    print(json.dumps(res, indent=2, ensure_ascii=False))
