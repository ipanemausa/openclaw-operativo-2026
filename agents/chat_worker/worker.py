import redis
import os
import time
import requests

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

r = redis.from_url(REDIS_URL, decode_responses=True)
print("chat_worker iniciado — escuchando queue:chat", flush=True)

def call_gemini(mensaje, agente):
    system_prompt = f"Eres un agente de HB Jewelry especializado en {agente}. Responde en espanol, de forma concisa y util."
    payload = {"contents": [{"parts": [{"text": f"{system_prompt}\n\nUsuario: {mensaje}"}]}]}
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    try:
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error Gemini: {str(e)}"

while True:
    try:
        job = r.blpop("queue:chat", timeout=5)
        if job:
            _, job_id = job
            data = r.hgetall(f"chat:{job_id}")
            mensaje = data.get("mensaje", "")
            agente = data.get("agente", "general")
            print(f"[{job_id}] Procesando: {mensaje[:50]}", flush=True)
            r.hset(f"chat:{job_id}", "status", "processing")
            respuesta = call_gemini(mensaje, agente)
            r.hset(f"chat:{job_id}", mapping={"status": "completed", "respuesta": respuesta})
            print(f"[{job_id}] Completado", flush=True)
    except Exception as e:
        print(f"Error worker: {e}", flush=True)
        time.sleep(2)
