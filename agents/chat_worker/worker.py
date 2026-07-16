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
print("chat_worker iniciado — DeepSeek MULTI-TASK", flush=True)

def call_deepseek(prompt, system="Eres un agente de HB Jewelry. Responde en espanol."):
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "deepseek-chat", "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}], "max_tokens": 4096}
    try:
        resp = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error DeepSeek: {str(e)}"

def extract_code(text):
    match = re.search(r"```(?:jsx|javascript|js)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def extraer_nombre_componente(linea):
    match = re.search(r"componente\s+(?:llamado\s+)?(\w+)", linea.lower())
    if match:
        return match.group(1).capitalize()
    match = re.search(r"llamado\s+(\w+)|llamada\s+(\w+)", linea.lower())
    if match:
        return (match.group(1) or match.group(2)).capitalize()
    return None

def es_linea_crear(linea):
    palabras = ["crea ", "crear ", "genera ", "generar ", "modifica ", "actualiza "]
    return any(p in linea.lower() for p in palabras)

def fix_css_path(codigo):
    codigo = re.sub(r"""['"]\.\./styles/hb\.css['"]""", '"../../styles/hb.css"', codigo)
    return codigo

def crear_componente(linea):
    nombre = extraer_nombre_componente(linea)
    if not nombre:
        return f"No pude extraer nombre: {linea[:50]}"
    system = """Eres un experto en React y el sistema de diseno HB Jewelry.
Clases CSS disponibles en hb.css: hb-page, hb-page-header, hb-page-title, hb-page-subtitle, hb-btn, hb-btn-sm, hb-form, hb-form-grid, hb-input, hb-select, hb-card, hb-card-header, hb-card-name, hb-card-price, hb-card-meta, hb-table-wrap, hb-table, hb-badge, hb-badge-green, hb-badge-red.
Colores: dorado #d4af6a, fondo #1a1a1a, texto #f0ede8.
El componente esta en frontend/src/components/NombreComponente/NombreComponente.jsx
Para importar el CSS usa EXACTAMENTE esta linea: import "../../styles/hb.css";
Genera SOLO codigo JSX. NO incluyas explicaciones. Solo el codigo entre tres backticks jsx y tres backticks."""
    respuesta = call_deepseek(linea, system=system)
    codigo = extract_code(respuesta)
    codigo = fix_css_path(codigo)
    path = f"{FRONTEND_BASE}/{nombre}/{nombre}.jsx"
    try:
        r2 = requests.post(WRITE_FILE_URL, json={"path": path, "content": codigo}, timeout=10)
        if r2.status_code == 200:
            return f"Componente {nombre}.jsx creado."
        else:
            return f"Error {nombre}: {r2.text}"
    except Exception as e:
        return f"Error {nombre}: {str(e)}"

def procesar_mensaje(mensaje, agente):
    lineas = mensaje.strip().split("\n")
    tareas = [l.strip() for l in lineas if es_linea_crear(l.strip())]
    if tareas:
        resultados = []
        for tarea in tareas:
            print(f"  -> {tarea[:60]}", flush=True)
            resultado = crear_componente(tarea)
            resultados.append(resultado)
        return "\n".join(resultados)
    else:
        system = f"Eres un agente de HB Jewelry especializado en {agente}. Responde en espanol, de forma concisa y util."
        return call_deepseek(mensaje, system=system)

while True:
    try:
        job = r.blpop("queue:chat", timeout=5)
        if job:
            _, job_id = job
            data = r.hgetall(f"chat:{job_id}")
            mensaje = data.get("mensaje", "")
            agente = data.get("agente", "general")
            print(f"[{job_id}] Procesando {len(mensaje)} chars", flush=True)
            r.hset(f"chat:{job_id}", "status", "processing")
            respuesta = procesar_mensaje(mensaje, agente)
            r.hset(f"chat:{job_id}", mapping={"status": "completed", "respuesta": respuesta})
            print(f"[{job_id}] Completado", flush=True)
    except Exception as e:
        print(f"Error worker: {e}", flush=True)
        time.sleep(2)