import redis
import json
import os
import time
import requests

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

r = redis.from_url(REDIS_URL)

print("chat_worker iniciado — escuchando queue:chat", flush=True)

def call_gemini(mensaje: str, agente: str) -> str:
    system_prompt = f"Eres un agente de HB Jewelry especializado en {agente}. Responde en español, de forma concisa y útil."
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nUsuario: {mensaje}"}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error Gemini: {str(e)}"

while True:
    try:
        job = r.blpop("queue:chat", timeout=5)
        if job:
            _, raw = job
            data = json.loads(raw)
            job_id = data.get("job_id", "unknown")
            mensaje = data.get("mensaje", "")
            agente = data.get("agente", "general")

            print(f"[{job_id}] Procesando: {mensaje[:50]}", flush=True)

            respuesta = call_gemini(mensaje, agente)

            result = {
                "job_id": job_id,
                "respuesta": respuesta,
                "agente": agente,
                "status": "completed"
            }
            r.setex(f"result:{job_id}", 300, json.dumps(result))
            print(f"[{job_id}] Completado ✅", flush=True)
    except Exception as e:
        print(f"Error worker: {e}", flush=True)
        time.sleep(2)
