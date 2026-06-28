import redis
import os
import time
import requests
import re

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
WRITE_FILE_URL = "http://claw-orchestrator:8090/api/hb/write-file"
FRONTEND_BASE = "frontend/src/components"

r = redis.from_url(REDIS_URL, decode_responses=True)
print("chat_worker iniciado — escuchando queue:chat", flush=True)

def call_gemini(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    try:
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error Gemini: {str(e)}"

def extract_code(text):
    match = re.search(r"```(?:jsx|javascript|js)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def es_comando_crear(mensaje):
    palabras = ["crea", "crear", "genera", "generar", "nuevo componente", "nueva pagina", "escribe el componente"]
    return any(p in mensaje.lower() for p in palabras)

def extraer_nombre_componente(mensaje):
    match = re.search(r"componente\s+(?:llamado\s+)?(\w+)", mensaje.lower())
    if match:
        nombre = match.group(1).capitalize()
        return nombre
    match = re.search(r"llamado\s+(\w+)|llamada\s+(\w+)|nombre\s+(\w+)", mensaje.lower())
    if match:
        nombre = (match.group(1) or match.group(2) or match.group(3)).capitalize()
        return nombre
    return "Nuevo"

def crear_componente(mensaje, agente):
    nombre = extraer_nombre_componente(mensaje)
    prompt = f"""Eres un experto en React y el sistema de diseno HB Jewelry.
El sistema usa clases CSS globales definidas en hb.css:
- hb-page, hb-page-header, hb-page-title, hb-page-subtitle
- hb-btn, hb-btn-sm, hb-form, hb-form-grid, hb-input, hb-select
- hb-card, hb-card-header, hb-card-name, hb-card-price, hb-card-meta
- hb-table-wrap, hb-table, hb-badge, hb-badge-green, hb-badge-red
- Colores: dorado #d4af6a, fondo #1a1a1a, texto #f0ede8

Genera SOLO el codigo JSX del componente React llamado {nombre}.
Importa hb.css con: import '../../styles/hb.css'
NO incluyas explicaciones, SOLO el codigo entre ```jsx y ```.

Tarea: {mensaje}"""

    respuesta_gemini = call_gemini(prompt)
    codigo = extract_code(respuesta_gemini)
    path = f"{FRONTEND_BASE}/{nombre}/{nombre}.jsx"

    try:
        r2 = requests.post(WRITE_FILE_URL, json={"path": path, "content": codigo}, timeout=10)
        if r2.status_code == 200:
            return f"Componente {nombre}.jsx creado en {path}. Vite recargara automaticamente."
        else:
            return f"Error escribiendo archivo: {r2.text}"
    except Exception as e:
        return f"Error llamando write-file: {str(e)}"

def chat_normal(mensaje, agente):
    system_prompt = f"Eres un agente de HB Jewelry especializado en {agente}. Responde en espanol, de forma concisa y util."
    prompt = f"{system_prompt}\n\nUsuario: {mensaje}"
    return call_gemini(prompt)

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

            if es_comando_crear(mensaje):
                print(f"[{job_id}] Modo IDE — creando componente", flush=True)
                respuesta = crear_componente(mensaje, agente)
            else:
                respuesta = chat_normal(mensaje, agente)

            r.hset(f"chat:{job_id}", mapping={"status": "completed", "respuesta": respuesta})
            print(f"[{job_id}] Completado", flush=True)
    except Exception as e:
        print(f"Error worker: {e}", flush=True)
        time.sleep(2)


