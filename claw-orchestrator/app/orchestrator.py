from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime, timezone
import json, os, pathlib, redis, threading, time
import docker

app = Flask(__name__)
CORS(app)
HANDOFFS_DIR = pathlib.Path("/handoffs")
LOGS_DIR     = pathlib.Path("/logs")
ESTADO_PATH  = pathlib.Path("/app/claw-estado.json")
HANDOFFS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

redis_client = redis.Redis(
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

def get_ready_tasks(tareas):
    ready = []
    for nombre, t in tareas.items():
        if t["estado"] != "pendiente":
            continue
        deps = t.get("depends_on", [])
        if all(tareas.get(d, {}).get("estado") == "completada" for d in deps):
            ready.append(nombre)
    return ready

def dag_worker():
    while True:
        try:
            estado = load_estado()
            tareas = estado.get("tareas", {})
            ready  = get_ready_tasks(tareas)
            for nombre in ready:
                redis_client.lpush("queue:tareas", nombre)
                tareas[nombre]["estado"] = "en_cola"
                print(f"[DAG] {nombre} en_cola", flush=True)
            if ready:
                estado["ultima_actualizacion"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                save_estado(estado)
        except Exception as e:
            print(f"[DAG] error: {e}", flush=True)
        time.sleep(10)

def task_executor():
    import task_executor as ex
    ex.run()

def get_stack_status():
    try:
        client = docker.from_env()
        containers = []
        for c in client.containers.list(all=True):
            ports = ",".join([str(v[0]["HostPort"]) for v in (c.ports or {}).values() if v])
            containers.append({"name": c.name, "status": c.status, "ports": ports})
        return containers
    except Exception as e:
        return [{"error": str(e)}]

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "claw-orchestrator", "port": 8090})

@app.route("/stack")
def stack():
    return jsonify({"containers": get_stack_status()})

@app.route("/api/radio/input", methods=["POST"])
def radio_input():
    body       = request.get_json(force=True)
    prompt     = body.get("prompt", "")
    duration   = int(body.get("duration", 5))
    resolution = body.get("resolution", "1280x720")
    style      = body.get("style", "cinematic")
    if not prompt:
        return jsonify({"error": "prompt requerido"}), 400
    job_id = f"veo-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(f"veo:{job_id}", mapping={
        "prompt": prompt, "duration": str(duration),
        "resolution": resolution, "style": style,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    redis_client.lpush("queue:video_veo", job_id)
    return jsonify({"job_id": job_id, "status": "queued"}), 202

@app.route("/api/radio/publish", methods=["GET"])
def radio_publish():
    job_id = request.args.get("job_id")
    if not job_id:
        return jsonify({"error": "job_id requerido"}), 400
    data = redis_client.hgetall(f"veo:{job_id}")
    if not data:
        return jsonify({"error": "job no encontrado"}), 404
    return jsonify({"job_id": job_id, "status": data.get("status"),
                    "video_url": data.get("video_url", ""), "prompt": data.get("prompt"),
                    "created_at": data.get("created_at")})

@app.route("/api/chat/input", methods=["POST"])
def chat_input():
    body = request.get_json(force=True)
    mensaje = body.get("mensaje", "")
    agente  = body.get("agente", "main")
    if not mensaje:
        return jsonify({"error": "mensaje requerido"}), 400
    job_id = f"chat-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(f"chat:{job_id}", mapping={
        "mensaje": mensaje, "agente": agente,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    redis_client.lpush("queue:chat", job_id)
    print(f"[CHAT] job {job_id} encolado — agente: {agente}", flush=True)
    return jsonify({"job_id": job_id, "status": "queued"}), 202

@app.route("/api/chat/status/<job_id>")
def chat_status(job_id):
    def generate():
        for _ in range(30):
            data = redis_client.hgetall(f"chat:{job_id}")
            status = data.get("status", "queued")
            respuesta = data.get("respuesta", "")
            yield f"data: {json.dumps({'status': status, 'respuesta': respuesta})}\n\n"
            if status == "completed":
                break
            time.sleep(1)
    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.route("/api/hb/write-file", methods=["POST"])
def write_file():
    b = request.get_json(force=True)
    rel_path = b.get("path", "").lstrip("/")
    content  = b.get("content", "")
    if not rel_path or not content:
        return jsonify({"error": "path y content requeridos"}), 400
    if not rel_path.startswith("frontend/src/"):
        return jsonify({"error": "ruta no permitida — solo frontend/src/"}), 403
    try:
        full_path = pathlib.Path("/") / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        print(f"[WRITE] {full_path}", flush=True)
        return jsonify({"status": "ok", "path": str(full_path)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/hb/productos", methods=["GET"])
def get_productos():
    keys = redis_client.keys("hb:producto:*")
    productos = [redis_client.hgetall(k) for k in sorted(keys)]
    return jsonify({"productos": productos})

@app.route("/api/hb/productos", methods=["POST"])
def add_producto():
    b = request.get_json(force=True)
    pid = f"hb:producto:{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(pid, mapping={
        "id": pid, "nombre": b.get("nombre",""), "precio": str(b.get("precio",0)),
        "stock": str(b.get("stock",0)), "categoria": b.get("categoria",""),
        "descripcion": b.get("descripcion",""),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({"status": "ok", "id": pid}), 201

@app.route("/api/hb/ventas", methods=["GET"])
def get_ventas():
    keys = redis_client.keys("hb:venta:*")
    ventas = [redis_client.hgetall(k) for k in sorted(keys)]
    return jsonify({"ventas": ventas})

@app.route("/api/hb/ventas", methods=["POST"])
def add_venta():
    b = request.get_json(force=True)
    vid = f"hb:venta:{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(vid, mapping={
        "id": vid, "producto": b.get("producto",""), "cantidad": str(b.get("cantidad",1)),
        "precio": str(b.get("precio",0)), "canal": b.get("canal",""),
        "cliente": b.get("cliente",""),
        "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({"status": "ok", "id": vid}), 201

@app.route("/api/hb/ordenes", methods=["GET"])
def get_ordenes():
    keys = redis_client.keys("hb:orden:*")
    ordenes = [redis_client.hgetall(k) for k in sorted(keys)]
    return jsonify({"ordenes": ordenes})

@app.route("/api/hb/ordenes", methods=["POST"])
def add_orden():
    b = request.get_json(force=True)
    oid = f"hb:orden:{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}"
    redis_client.hset(oid, mapping={
        "id": oid, "cliente": b.get("cliente",""), "producto": b.get("producto",""),
        "cantidad": str(b.get("cantidad",1)), "precio": str(b.get("precio",0)),
        "canal": b.get("canal","Instagram"), "estado": b.get("estado","Pendiente"),
        "notas": b.get("notas",""),
        "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({"status": "ok", "id": oid}), 201

@app.route("/api/hb/ordenes/<oid>", methods=["PATCH"])
def update_orden(oid):
    b = request.get_json(force=True)
    key = oid if oid.startswith("hb:orden:") else f"hb:orden:{oid}"
    redis_client.hset(key, "estado", b.get("estado","Pendiente"))
    return jsonify({"status": "ok"})

@app.route("/handoff", methods=["POST"])
def create_handoff():
    body = request.get_json(force=True)
    ts   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    h    = {
        "id":             f"HO-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp":      ts,
        "from":           body.get("from", "claude"),
        "to":             body.get("to", "copilot"),
        "tareas_activas": body.get("tareas", []),
        "notas":          body.get("notas", "")
    }
    HANDOFFS_DIR.mkdir(exist_ok=True)
    (HANDOFFS_DIR / f"{h['id']}.json").write_text(json.dumps(h, indent=2, ensure_ascii=False))
    return jsonify({"handoff": h, "id": h["id"]})

@app.route("/handoffs")
def list_handoffs():
    files = sorted(HANDOFFS_DIR.glob("*.json"), reverse=True)[:20]
    return jsonify({"handoffs": [{"id": json.loads(f.read_text())["id"]} for f in files]})

@app.route("/api/tareas", methods=["GET"])
def get_tareas():
    estado = load_estado()
    return jsonify({"tareas": estado.get("tareas", {})})

@app.route("/api/tareas/<nombre>/completar", methods=["POST"])
def completar_tarea(nombre):
    estado = load_estado()
    tareas = estado.get("tareas", {})
    if nombre not in tareas:
        return jsonify({"error": "tarea no encontrada"}), 404
    tareas[nombre]["estado"] = "completada"
    tareas[nombre]["completada_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    estado["ultima_actualizacion"]  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    save_estado(estado)
    return jsonify({"tarea": nombre, "estado": "completada"})

# ═══════════════════════════════════════════════════════════════
# ECC — Estado Cognitivo Centralizado
# Agregado: 2026-07-10
# Riesgo: CERO — solo agrega endpoints nuevos /api/ecc/*
# No modifica ningún endpoint existente
# ═══════════════════════════════════════════════════════════════

ECC_STATE_KEY    = "ecc:state"
ECC_AUDIT_STREAM = "ecc:audit"
ECC_VERSION_KEY  = "ecc:version"

def ecc_init_state():
    """Inicializa el estado ECC en Redis si no existe."""
    if not redis_client.exists(ECC_STATE_KEY):
        initial = {
            "version": "1",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "system_stable": "true",
            "last_actor": "system",
            "last_action": "ecc_initialized",
            "last_action_validated": "true",
            "active_task": "",
            "active_task_locked_by": "",
            "pending_sync": "false",
            "pending_commit": "false",
            "docker_healthy": "true",
            "services_count": "6",
            "drift_detected": "false",
            "drift_details": ""
        }
        redis_client.hset(ECC_STATE_KEY, mapping=initial)
        redis_client.set(ECC_VERSION_KEY, "1")
        print("[ECC] Estado inicial creado en Redis", flush=True)

def ecc_read_state():
    """Lee el estado ECC completo desde Redis."""
    state = redis_client.hgetall(ECC_STATE_KEY)
    if not state:
        ecc_init_state()
        state = redis_client.hgetall(ECC_STATE_KEY)
    return state

def ecc_write_state(updates, actor="system", expected_version=None):
    """
    Escribe al estado ECC con optimistic locking.
    Si expected_version no coincide con la versión actual, rechaza la escritura.
    """
    current_version = int(redis_client.get(ECC_VERSION_KEY) or "0")
    if expected_version is not None and int(expected_version) != current_version:
        return False, current_version, "version_conflict"
    new_version = current_version + 1
    updates["version"] = str(new_version)
    updates["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    redis_client.hset(ECC_STATE_KEY, mapping=updates)
    redis_client.set(ECC_VERSION_KEY, str(new_version))
    return True, new_version, "ok"

def ecc_gate_in(task_name, actor):
    """
    Gate Guard de entrada: verifica si el sistema está estable
    y si no hay otra tarea activa. Bloquea la tarea si todo OK.
    Retorna (allowed, reason, state).
    """
    state = ecc_read_state()
    warnings = []
    # Verificar estabilidad
    if state.get("system_stable") != "true":
        warnings.append("system_not_stable")
    # Verificar si hay tarea activa
    active = state.get("active_task", "")
    if active and active != "":
        return False, f"task_locked_by_{state.get('active_task_locked_by','unknown')}", state
    # Verificar sync pendiente
    if state.get("pending_sync") == "true":
        warnings.append("pending_sync")
    if state.get("pending_commit") == "true":
        warnings.append("pending_commit")
    # Bloquear tarea
    version = state.get("version", "0")
    ok, new_v, reason = ecc_write_state({
        "active_task": task_name,
        "active_task_locked_by": actor,
        "last_actor": actor,
        "last_action": f"gate_in:{task_name}"
    }, actor=actor, expected_version=version)
    if not ok:
        return False, reason, state
    # Registrar en audit
    redis_client.xadd(ECC_AUDIT_STREAM, {
        "version": str(new_v),
        "actor": actor,
        "action": "gate_in",
        "task": task_name,
        "result": "allowed",
        "warnings": json.dumps(warnings),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return True, "allowed" if not warnings else f"allowed_with_warnings:{','.join(warnings)}", state

def ecc_gate_out(task_name, actor, success=True):
    """
    Gate Guard de salida: desbloquea la tarea,
    actualiza estado y registra en audit.
    """
    state = ecc_read_state()
    version = state.get("version", "0")
    updates = {
        "active_task": "",
        "active_task_locked_by": "",
        "last_actor": actor,
        "last_action": f"gate_out:{task_name}",
        "last_action_validated": "true" if success else "false"
    }
    ok, new_v, reason = ecc_write_state(updates, actor=actor, expected_version=version)
    # Registrar en audit
    redis_client.xadd(ECC_AUDIT_STREAM, {
        "version": str(new_v) if ok else version,
        "actor": actor,
        "action": "gate_out",
        "task": task_name,
        "result": "success" if success else "failed",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return ok, reason

def ecc_detect_drift():
    """
    Detecta drift entre claw-estado.json y el estado ECC en Redis.
    Compara timestamps y verifica coherencia.
    """
    drift_issues = []
    # Leer estado del archivo
    file_state = load_estado()
    # Leer estado ECC
    ecc_state = ecc_read_state()
    # Comparar: si hay tarea activa en ECC pero el DAG no la conoce
    active_task = ecc_state.get("active_task", "")
    if active_task:
        tareas = file_state.get("tareas", {})
        if active_task not in tareas:
            drift_issues.append(f"ECC tiene tarea activa '{active_task}' que no existe en claw-estado.json")
    # Verificar Docker health
    try:
        containers = get_stack_status()
        running = [c for c in containers if c.get("status") == "running"]
        expected = int(ecc_state.get("services_count", "6"))
        if len(running) != expected:
            drift_issues.append(f"Esperados {expected} containers running, encontrados {len(running)}")
    except Exception as e:
        drift_issues.append(f"Error verificando Docker: {str(e)}")
    return drift_issues

# ── ECC Endpoints ────────────────────────────────────────────

@app.route("/api/ecc/state", methods=["GET"])
def ecc_get_state():
    """Retorna el estado ECC completo."""
    state = ecc_read_state()
    return jsonify({"ecc": state})

@app.route("/api/ecc/action", methods=["POST"])
def ecc_register_action():
    """
    Registra una acción en el ECC.
    Body: {"actor": "...", "action": "...", "task": "...", "gate": "in|out|none"}
    """
    b = request.get_json(force=True)
    actor  = b.get("actor", "unknown")
    action = b.get("action", "unknown")
    task   = b.get("task", "")
    gate   = b.get("gate", "none")
    if gate == "in" and task:
        allowed, reason, state = ecc_gate_in(task, actor)
        return jsonify({"allowed": allowed, "reason": reason, "state": state})
    elif gate == "out" and task:
        success = b.get("success", True)
        ok, reason = ecc_gate_out(task, actor, success)
        return jsonify({"completed": ok, "reason": reason})
    else:
        # Registro simple sin gate
        state = ecc_read_state()
        version = state.get("version", "0")
        ok, new_v, reason = ecc_write_state({
            "last_actor": actor,
            "last_action": action
        }, actor=actor, expected_version=version)
        redis_client.xadd(ECC_AUDIT_STREAM, {
            "version": str(new_v) if ok else version,
            "actor": actor,
            "action": action,
            "task": task or "none",
            "result": "registered",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        return jsonify({"registered": ok, "version": new_v if ok else int(version), "reason": reason})

@app.route("/api/ecc/validate", methods=["POST"])
def ecc_validate():
    """Fuerza una validación del sistema y actualiza el estado ECC."""
    drift_issues = ecc_detect_drift()
    state = ecc_read_state()
    version = state.get("version", "0")
    is_stable = len(drift_issues) == 0
    ecc_write_state({
        "system_stable": "true" if is_stable else "false",
        "drift_detected": "false" if is_stable else "true",
        "drift_details": json.dumps(drift_issues) if drift_issues else "",
        "last_actor": "validator",
        "last_action": "system_validation"
    }, actor="validator", expected_version=version)
    # Registrar en audit
    redis_client.xadd(ECC_AUDIT_STREAM, {
        "actor": "validator",
        "action": "system_validation",
        "result": "stable" if is_stable else "drift_detected",
        "issues": json.dumps(drift_issues),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    return jsonify({
        "stable": is_stable,
        "issues": drift_issues,
        "containers_checked": True
    })

@app.route("/api/ecc/audit", methods=["GET"])
def ecc_get_audit():
    """Retorna las últimas N entradas del audit stream."""
    count = int(request.args.get("count", 20))
    entries = redis_client.xrevrange(ECC_AUDIT_STREAM, count=count)
    audit = []
    for entry_id, data in entries:
        data["id"] = entry_id
        audit.append(data)
    return jsonify({"audit": audit, "count": len(audit)})

@app.route("/api/ecc/lock", methods=["POST"])
def ecc_lock_task():
    """Lock manual de una tarea."""
    b = request.get_json(force=True)
    task = b.get("task", "")
    actor = b.get("actor", "manual")
    if not task:
        return jsonify({"error": "task requerido"}), 400
    allowed, reason, state = ecc_gate_in(task, actor)
    return jsonify({"locked": allowed, "reason": reason})

@app.route("/api/ecc/unlock", methods=["POST"])
def ecc_unlock_task():
    """Unlock manual de una tarea."""
    b = request.get_json(force=True)
    actor = b.get("actor", "manual")
    state = ecc_read_state()
    active = state.get("active_task", "")
    if not active:
        return jsonify({"error": "no hay tarea bloqueada"}), 400
    ok, reason = ecc_gate_out(active, actor, success=True)
    return jsonify({"unlocked": ok, "task": active, "reason": reason})

@app.route("/api/ecc/drift", methods=["GET"])
def ecc_get_drift():
    """Detecta y retorna drift entre claw-estado.json y Redis ECC."""
    issues = ecc_detect_drift()
    return jsonify({
        "drift_detected": len(issues) > 0,
        "issues": issues,
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })

# ═══════════════════════════════════════════════════════════════
# Fin ECC
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    ecc_init_state()  # Inicializar ECC al arrancar
    threading.Thread(target=dag_worker, daemon=True).start()
    threading.Thread(target=task_executor, daemon=True).start()
    app.run(host="0.0.0.0", port=8090, debug=False)