import redis, json, os, time, pathlib
from datetime import datetime, timezone

ESTADO_PATH = pathlib.Path("/app/claw-estado.json")
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def load_estado():
    try:
        return json.loads(ESTADO_PATH.read_text(encoding="utf-8"))
    except:
        return {}

def save_estado(estado):
    ESTADO_PATH.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")

def ejecutar(nombre):
    print(f"[EXECUTOR] ejecutando: {nombre}", flush=True)
    # Aqui cada tarea tiene su logica
    time.sleep(2)  # simulacion — reemplazar con logica real
    return True

def run():
    print("[EXECUTOR] iniciado — escuchando queue:tareas", flush=True)
    while True:
        try:
            item = r.brpop("queue:tareas", timeout=5)
            if not item:
                continue
            _, nombre = item
            estado = load_estado()
            tareas = estado.get("tareas", {})
            if nombre not in tareas:
                print(f"[EXECUTOR] tarea desconocida: {nombre}", flush=True)
                continue
            tareas[nombre]["estado"] = "ejecutando"
            save_estado(estado)
            ok = ejecutar(nombre)
            tareas[nombre]["estado"] = "completada" if ok else "fallida"
            tareas[nombre]["completada_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            estado["ultima_actualizacion"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            save_estado(estado)
            print(f"[EXECUTOR] {nombre} → {'completada' if ok else 'fallida'}", flush=True)
        except Exception as e:
            print(f"[EXECUTOR] error: {e}", flush=True)
            time.sleep(3)

if __name__ == "__main__":
    run()
