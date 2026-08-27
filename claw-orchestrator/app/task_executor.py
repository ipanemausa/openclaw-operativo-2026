import redis, json, os, time, pathlib
from datetime import datetime, timezone
try:
    from zero_cost_router import ZeroCostEdgeRouter
except ImportError:
    ZeroCostEdgeRouter = None

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
    
    # Delegar al ZeroCostEdgeRouter si la tarea lo requiere
    if ZeroCostEdgeRouter and any(k in nombre.lower() for k in ["edge", "chat", "resumen", "parsing", "multimodal"]):
        print(f"[EXECUTOR] Delegando {nombre} a Zero-Cost Edge Router...", flush=True)
        try:
            # Extraemos el tipo basado en el nombre para demostracion
            task_type = "rapido"
            for k in ["chat", "resumen", "parsing", "multimodal"]:
                if k in nombre.lower(): task_type = k
            
            res = ZeroCostEdgeRouter.route_task(task_type, f"Procesa la tarea: {nombre}")
            print(f"[EXECUTOR] Respuesta del Edge Router: {res[:100]}...", flush=True)
            return True
        except Exception as e:
            print(f"[EXECUTOR] Fallo en Edge Router: {e}", flush=True)
            return False

    # Aqui cada tarea tiene su logica tradicional
    time.sleep(2)  # simulacion — reemplazar con logica real
    return True

def ecc_gate(action, task_name, actor="executor", success=True):
    """Wrapper seguro para ECC gate — si falla, no bloquea nada."""
    try:
        ECC_STATE_KEY = "ecc:state"
        ECC_AUDIT_STREAM = "ecc:audit"
        ECC_VERSION_KEY = "ecc:version"
        if not r.exists(ECC_STATE_KEY):
            return  # ECC no inicializado, continuar sin bloquear
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if action == "in":
            version = r.hget(ECC_STATE_KEY, "version") or "0"
            new_v = int(version) + 1
            r.hset(ECC_STATE_KEY, mapping={
                "active_task": task_name,
                "active_task_locked_by": actor,
                "last_actor": actor,
                "last_action": f"executor_gate_in:{task_name}",
                "version": str(new_v),
                "timestamp": ts
            })
            r.set(ECC_VERSION_KEY, str(new_v))
            r.xadd(ECC_AUDIT_STREAM, {
                "version": str(new_v), "actor": actor,
                "action": "executor_gate_in", "task": task_name,
                "result": "started", "timestamp": ts
            })
        elif action == "out":
            version = r.hget(ECC_STATE_KEY, "version") or "0"
            new_v = int(version) + 1
            r.hset(ECC_STATE_KEY, mapping={
                "active_task": "",
                "active_task_locked_by": "",
                "last_actor": actor,
                "last_action": f"executor_gate_out:{task_name}",
                "last_action_validated": "true" if success else "false",
                "version": str(new_v),
                "timestamp": ts
            })
            r.set(ECC_VERSION_KEY, str(new_v))
            r.xadd(ECC_AUDIT_STREAM, {
                "version": str(new_v), "actor": actor,
                "action": "executor_gate_out", "task": task_name,
                "result": "success" if success else "failed", "timestamp": ts
            })
        print(f"[ECC] gate_{action}: {task_name}", flush=True)
    except Exception as e:
        print(f"[ECC] gate_{action} error (non-blocking): {e}", flush=True)

def run():
    print("[EXECUTOR] iniciado — escuchando queue:tareas:critical y queue:tareas", flush=True)
    while True:
        try:
            # Event Intelligence Layer: Prioridad a tareas críticas
            item = r.brpop(["queue:tareas:critical", "queue:tareas"], timeout=5)
            if not item:
                continue
            queue_name, data_str = item
            
            # Parse JSON metadata
            try:
                event_data = json.loads(data_str)
                nombre = event_data.get("task_id", data_str)
                print(f"[EXECUTOR] Recibido evento {queue_name}: {event_data.get('priority', 'normal')} prioridad", flush=True)
            except json.JSONDecodeError:
                nombre = data_str # Fallback for old format
                
            estado = load_estado()
            tareas = estado.get("tareas", {})
            if nombre not in tareas:
                print(f"[EXECUTOR] tarea desconocida: {nombre}", flush=True)
                continue
            ecc_gate("in", nombre)  # ECC Gate In (non-blocking)
            tareas[nombre]["estado"] = "ejecutando"
            save_estado(estado)
            ok = ejecutar(nombre)
            tareas[nombre]["estado"] = "completada" if ok else "fallida"
            tareas[nombre]["completada_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            estado["ultima_actualizacion"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            save_estado(estado)
            ecc_gate("out", nombre, success=ok)  # ECC Gate Out (non-blocking)
            print(f"[EXECUTOR] {nombre} → {'completada' if ok else 'fallida'}", flush=True)
        except Exception as e:
            print(f"[EXECUTOR] error: {e}", flush=True)
            time.sleep(3)

if __name__ == "__main__":
    run()
