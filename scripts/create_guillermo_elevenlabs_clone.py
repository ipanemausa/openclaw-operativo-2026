import os
import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
audio_path = ROOT / "audio" / "guillermo_voice_reference.wav"
env_file = Path("C:/Users/ipane/.openclaw-master.env")

env_dict = {}
for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env_dict[k.strip()] = v.strip().strip('"').strip("'")

api_key = env_dict.get("ELEVENLABS_API_KEY", "")

print("[*] Iniciando clonación instantánea directa vía API de ElevenLabs...")
print(f"[*] Archivo de referencia: {audio_path} ({audio_path.stat().st_size / (1024*1024):.2f} MB)")

url = "https://api.elevenlabs.io/v1/voices/add"
headers = {
    "xi-api-key": api_key
}

data = {
    "name": "Guillermo HB.OS Sovereign Master",
    "description": "Clon de voz auténtico de Guillermo para OpenClaw HB.OS - Barítono cálido, autoridad pedagógica y cadencia reflexiva.",
    "labels": '{"accent": "colombian_warm", "gender": "male", "age": "mature", "use_case": "masterclasses"}'
}

files = [
    ("files", ("guillermo_voice_reference.wav", open(audio_path, "rb"), "audio/wav"))
]

try:
    response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
    print(f"Status code: {response.status_code}")
    res_json = response.json()
    print("Respuesta de ElevenLabs:", json.dumps(res_json, indent=2))
    
    voice_id = res_json.get("voice_id")
    if voice_id:
        print(f"\n[ÉXITO TOTAL] Clon de Guillermo creado con ID: {voice_id}")
        
        # Guardar en archivo de configuración local
        cfg_path = ROOT / "audio" / "guillermo_voice_id.json"
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump({"voice_id": voice_id, "name": "Guillermo HB.OS Sovereign Master"}, f, indent=2)
except Exception as e:
    print("[ERROR] Falló la creación del clon:", e)
