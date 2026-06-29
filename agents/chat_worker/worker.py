import redis
import os
import time
import requests
import re

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
WRITE_FILE_URL = "http://claw-orchestrator:8090/api/hb/write-file"
FRONTEND_BASE = "frontend/src/components"

r = redis.from_url(REDIS_URL, decode_responses=True)
print("chat_worker iniciado — DeepSeek", flush=True)

def call_deepseek(prompt, system="Eres un agente de HB Jewelry. Responde en espanol."):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096
    }
    try:
        resp = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error DeepSeek: {str(e)}"

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
        return match.group(1).capitalize()
    match = re.search(r"llamado\s+(\w+)|llamada\s+(\w+)", mensaje.lower())
    if match:
        return (match.group(1) or match.group(2)).capitalize()
    return "Nuevo"

def crear_componente(mensaje):
    nombre = extraer_nombre_componente(mensaje)
    system = """Eres un experto en React y el sistema de diseno HB Jewelry.
Clases CSS disponibles en hb.css:
hb-page, hb-page-header, hb-page-title, hb-page-subtitle,
hb-btn, hb-btn-sm, hb-form, hb-form-grid, hb-input, hb-select,
hb-card, hb-card-header, hb-card-name, hb-card-price, hb-card-meta,
hb-table-wrap, hb-table, hb-badge, hb-badge-green, hb-badge-red.
Colores: dorado #d4af6a, fondo #1a1a1a, texto #f0ede8.
Genera SOLO codigo JSX. Importa con: import '../../styles/hb.css'
NO incluyas explicaciones. Solo el codigo entre ```jsx y ```."""

    respuesta = call_deepseek(mensaje, system=system)
    codigo = extract_code(respuesta)
    path = f"{FRONTEND_BASE}/{nombre}/{nombre}.jsx"

    try:
        r2 = requests.post(WRITE_FILE_URL, json={"path": path, "content": codigo}, timeout=10)
        if r2.status_code == 200:
            return f"Componente {nombre}.jsx creado en {path}. Vite recargara automaticamente."
        else:
            return f"Error escribiendo archivo: {r2.text}"
    except Exception as e:
        return f"Error llamando write-file: {str(e)}"

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
                respuesta = crear_componente(mensaje)
            else:
                system = f"Eres un agente de HB Jewelry especializado en {agente}. Responde en espanol, de forma concisa y util."
                respuesta = call_deepseek(mensaje, system=system)

            r.hset(f"chat:{job_id}", mapping={"status": "completed", "respuesta": respuesta})
            print(f"[{job_id}] Completado", flush=True)
    except Exception as e:
        print(f"Error worker: {e}", flush=True)
        time.sleep(2)
